import requests
from flask import Flask, jsonify, request
from createcacert import createX509
from createsymkey import createSymKey

# creating a Flask app
app = Flask(__name__)
  
@app.route('/')
def home():
    return "Welcome to Inteligent Edge!!!"
  
@app.route('/api/v1/gateway/provisionx509cert')
def provisiongatewaycertx509():
    try:
        createX509()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/gateway/provisionsymkey')
def provisiongatewaysymmetrickey():
    try:
        symkey = createSymKey()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/device/provisionx509cert')
def provisiondevicecertx509():
    try:
        createX509()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/device/provisionsymkey')
def provisiondevicesymmetrickey():
    try:
        symkey = createSymKey()
        return symkey
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count')
def getgatewaycount():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        gatewaycount = response.json['totalCount']
        return str(gatewaycount)
    except Exception as e:
        return e

@app.route('/api/v1/device/count')
def getdevicecount():
    try:
        apiurl = "http://<ip of gateway>:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicecount = response.json()['totalCount']
        return str(devicecount)
    except Exception as e:
        return e

@app.route('/api/v1/gatewayprofiles')
def getgatewayprofilelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e

@app.route('/api/v1/deviceprofiles')
def getdeviceprofilelist():
    try:
        apiurl = "http://<ip of gateway>:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return 

@app.route('/api/v1/gatewayui')
def getgatewayui():
    try:
        apiurl = "http://<ip of gateway>:4000"
        return apiurl
    except Exception as e:
        return e
  
if __name__ == '__main__':
    app.run('0.0.0.0',5000,debug = True)