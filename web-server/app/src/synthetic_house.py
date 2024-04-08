import numpy as np

from typing import Union
from matplotlib import pyplot as plt
from cvxpy import Variable, Problem, Minimize, maximum, pos, neg

from .battery import Battery, BatteryParameters

class SyntheticHouse():
    
    def __init__(
        self, config
    ):
        
        self.batch_size = config['batch_size']
        self.steps = config['rollout_steps']
        self.current_step = 0
        self.grid_sell_rate = 0.25

        # Microgrid data

        self.pv_gen = np.array(config['pv']).astype(np.float32)
        self.demand = np.array(config['demand']).astype(np.float32)

        self.remaining_energy = np.subtract(self.demand, self.pv_gen)
        self.net_energy = np.zeros((self.batch_size, self.steps))
        self.price = np.array(config['price']).astype(np.float32)
        self.emission = np.array(config['emissions']).astype(np.float32)   

        # Components
        self.random_soc_0 = config['battery']['random_soc_0']
        self.battery = Battery(batch_size = self.batch_size, random_soc_0=self.random_soc_0, params = BatteryParameters(config['battery']))


    def compute_metrics(self):

        remaining_energy_to_step = self.remaining_energy[:self.current_step]

        # Compute battery performance

        price_without_battery = np.where(
            remaining_energy_to_step > 0,
            remaining_energy_to_step * self.price,
            remaining_energy_to_step * self.price * self.grid_sell_rate
        ).sum()

        price_with_battery = np.where(
            self.net_energy > 0,
            self.net_energy * self.price,
            self.net_energy * self.price * self.grid_sell_rate
        ).sum(axis=1).mean()

        emission_without_battery = np.where(
            remaining_energy_to_step > 0,
            remaining_energy_to_step * self.emission,
            0
        ).sum()

        emission_with_battery = np.where(
            self.net_energy > 0,
            self.net_energy * self.emission,
            0
        ).sum(axis=1).mean()

        # Compute metrics, we add a baseline of one to indicate when the battery didn't cause any improvement

        price_metric = price_with_battery - price_without_battery
        emission_metric = emission_with_battery - emission_without_battery

        return price_metric, emission_metric, price_with_battery, price_without_battery, emission_with_battery, emission_without_battery

    def execute_random_actions(self):

        for _ in range(self.steps):
            # Execute a random action
            action = np.random.uniform(-0.9, 0.9, (self.batch_size, 1))
            self.apply_action(action)

    def compute_optimal_actions(self):

        battery = Variable(self.steps + 1)
        action = Variable(self.steps)
        consumption = Variable(self.steps)

        constraints = []

        # Battery
        
        # Starts in 0.1
        constraints.append(battery[0] == self.battery.soc_min)
        
        # Max and min batteries
        for i in range(self.steps + 1):
            constraints.append(battery[i] <= self.battery.soc_max)
            constraints.append(battery[i] >= self.battery.soc_min)

        # Define optimization case

        obj = 0

        for i in range(self.steps):

            # Max and min battery charge

            constraints.append(action[i] <= self.battery.p_charge_max)
            constraints.append(action[i] >= -self.battery.p_discharge_max)



            # Update battery SOC

            # TODO: Make it work with the correct equation

            # p_charge = pos(action[i] * self.battery.efficiency)
            # p_discharge = neg(action[i] /  self.battery.efficiency)

            # constraints.append(battery[i+1] == battery[i] + (
            #     p_charge - p_discharge
            # )/self.battery.capacity)

            constraints.append(battery[i+1] == battery[i] + ((action[i] * self.battery.efficiency)/self.battery.efficiency)/self.battery.capacity )

            # Update net

            # constraints.append(consumption[i] == self.demand[i]-self.pv_gen[i] + p_charge - p_discharge)
            constraints.append(consumption[i] == self.demand[i] - self.pv_gen[i] + action[i] * self.battery.efficiency)

            obj += maximum(consumption[i] * (self.price[i] + self.emission[i]),0) 
            obj += maximum(-consumption[i] * self.price[i] * self.grid_sell_rate,0)  


        objective = Minimize(obj)
        prob = Problem(objective, constraints)
        solution = prob.solve()

        return solution, battery.value, action.value

    def execute_optimal_actions(self):

        _, _, actions = self.compute_optimal_actions()

        for i in range(self.steps):
            action = np.ones((self.batch_size, 1)) * actions[i]
            self.apply_action(action)
        
        return actions

    def observe(self) -> np.ndarray:

        terminal = self.current_step >= self.steps

        if not terminal:

            state = np.stack([
                np.ones(self.batch_size) * self.current_step % 24,
                self.battery.soc.squeeze(axis=-1)
            ], axis=1)

        else:

            state = np.stack([
                np.zeros(self.batch_size),
                np.ones(self.batch_size) * self.battery.soc_min
            ], axis=1)

        return state

    def apply_action(self, batt_action: np.array) -> Union[np.ndarray, np.ndarray]:

        # Apply action to battery and reach the new state

        p_charge, p_discharge, _ = self.battery.check_battery_constraints(power_rate=batt_action)
        self.battery.apply_action(p_charge = p_charge, p_discharge = p_discharge)

        # Compute the next step net energy

        self.net_energy[:,self.current_step] += (self.remaining_energy[self.current_step] + p_charge - p_discharge).squeeze()

        # Compute cost

        cost = np.where(
            self.net_energy[:,self.current_step] > 0,
            (self.net_energy[:,self.current_step]) * (self.price[self.current_step] + self.emission[self.current_step]),
            (self.net_energy[:,self.current_step]) * self.price[self.current_step] * self.grid_sell_rate
        ).reshape(self.batch_size,1)
        
        self.increment_step()

        return self.observe(), -cost

    def increment_step(self) -> None:
        self.current_step += 1

    def reset(self):
        """
            Resets the current time step.
        Returns
        -------
            None
        """
        self.current_step = 0
        self.generate_data()
        self.battery.reset()
