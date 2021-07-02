from flask import jsonify, request
from app import app
from app.src.database import read_credential, update_credential, insert_blob, read_blob, restart_device
from app.src.wifi_config import scan_wifi_networks, config_wifi, wifi_networks
import base64


@app.route('/api/authentification', methods=['POST'])
def settings():
    credentials_database = read_credential()
    password_d = credentials_database[0][1]
    if request.method == "POST":
        password_req = request.get_json()
        if password_req['values']['confirmPassword'] == password_d:
            data = {'response': 'OK'}
        else:
            data = {'response': 'ERROR'}
        return jsonify(data)


@app.route('/api/update-password', methods=['POST'])
def update_password():
    if request.method == "POST":
        parameters = request.get_json()
        credential = read_credential()
        print(credential)
        old_password = credential[0][1]
        new_password = parameters['values']['newPassword']
        confirm_password = parameters['values']['confirmPassword']
        auth_password = parameters['values']['currentPassword']
        if old_password == auth_password:
            if new_password == confirm_password:
                update_credential(new_password)
                data = {'response': 'OK'}
            else:
                data = {'response': 'Bad Confirmation'}
        else:
            data = {'response': 'Bad Password'}
    return jsonify(data)


@app.route('/api/load-wifi-networks', methods=['GET'])
def load_wifi():
    data = scan_wifi_networks()
    return jsonify(data)


@app.route('/api/config-wifi', methods=['POST'])
def save_wifi():
    if request.method == "POST":
        parameters = request.get_json()
        SSID = parameters['values']['SSID']
        Password = parameters['values']['password']
        if config_wifi(SSID, Password):
            data = {'response': 'OK'}
        else:
            data = {'response': 'ERROR'}
    return jsonify(data)


@app.route('/api/change-img', methods=['POST'])
def save_img():
    if request.method == "POST":
        parameters = request.get_data()  # .get_json()
        res = insert_blob(parameters)
        return jsonify({'response': res})


@app.route('/api/img', methods=['GET'])
def read_img():
    if request.method == "GET":
        img = base64.b64encode(read_blob()).decode("utf-8")
        return jsonify({'img': img})


@app.route('/api/reset', methods=['POST'])
def reset():
    if request.method == "POST":
        parameters = request.get_json()
        restart = parameters['restartDevice']
        if restart:
            if restart_device():
                data = {'response': 'OK'}
            else:
                data = {'response': 'ERROR'}

    return data
