from flask import jsonify, request
from werkzeug.datastructures import Headers
from app import app
from app.src.database import read_credential, scan_wifi_networks, config_wifi, update_credential, insertBLOB, readBLOB



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


@app.route('/api/updatePassword', methods=['POST'])
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


@app.route('/api/load-wifiNetworks', methods=['GET'])
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
        parameters = request.get_data()
        # .get_json()
        res = insertBLOB(parameters)
        return jsonify({'response': res})


@app.route('/api/img', methods=['GET'])
def read_img():
    if request.method == "GET":
        res = readBLOB()
        return res

