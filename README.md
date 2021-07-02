# Egeo meter Iot Application

This application is created to simplify communication between the user and the *Onion omega*, this application must be run within *Onion omega*, with it the user will have a server with a platform that allows him to connect to Wi-Fi, restart the device, etc

## Contents:  
___ 
This project contains two folders:   
* ***scripts:*** Contains *Onion omega* configuration files, pass files and database configuration.   
* ***web-server:*** Contains the files and folders of the server.

## How to clone:   
___
step to step, to be concluded

## Requirements:   
___
* *Onion Omega* with SDcard memory expansion of at least 4GB.
* *Onion Omega* ready to use (ask [Cycle System](https://cyclesystem.org/ "Cycle System") for formatting instructions).
* **build** folder supplied by [Cycle System](https://cyclesystem.org/ "Cycle System").

## Installation:
___
>The *Onion Omega* must already be configured with SD card, you can consult with [Cycle System](https://cyclesystem.org/ "Cycle System") 
 the step by step for the preparation of the *Omega Onion*.   

1. You must be connected to the *Onion Omega* through the local Wifi network with the *Onion Omega* credentials.  

2. Add or replace the ***build*** folder (provided by [Cycle System](https://cyclesystem.org/ "Cycle System") ), to the ***app*** folder, inside the project's ***web-server*** folder.   

3. Inside ***web-server*** open the file **config_template.py**, there secure the path of **DATABASE_URI** in production mode as "**/root/egeo.sqlite**", save and change the name of this file to **config.py**.   

4. In your console go to the folder * scripts / copy_files_template / *, here you must give execution permission to "copy_files.sh" with:   
```bash
chmod +x copy_files.sh
```   
5. Run the file:  
```bash
./copy_files.sh <Ip address of your Onion Omega>
# Example
# ./copy_files.sh 192.168.3.1 
```   
6. Write the password (usually is "onioneer").   
7. Enter the "Onion" run on your console:   
```bash
ssh root@<Ip address of your Onion Omega>
```   
8. Write the password.  
9. Python3 must be installed inside the *Onion Omega*, inside the *Onion Omega*, Go to the folder "**/root/egeo_iot/scripts/onionConfiguration/**", and run script **4_install.sh**, to install python and its dependencies:   
```bash
sh 4_install.sh
```
10. Go to the folder "**/root/egeo_iot/scripts/**" and copy the file **rc.local** to the path "**/etc**", with:   
```bash
cp rc.local /etc
```
11. Reboot the *Onion Omega*, with:   
```bash
reboot 
```
If you can, turn the *Onion Omega* off and on