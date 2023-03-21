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
        gatewaycount = response.json()['totalCount']
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

@app.route('/api/v1/gateway/profiles')
def getgatewayprofilelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e

@app.route('/api/v1/device/profiles')
def getdeviceprofilelist():
    try:
        apiurl = "http://<ip of gateway>:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e
        
@app.route('/api/v1/gateway/services')
def getgatewaydeviceservicelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceservice/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e

@app.route('/api/v1/device/services')
def getdevicedeviceservicelist():
    try:
        apiurl = "http://<ip of gateway>:59881/api/v2/deviceservices/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e

@app.route('/api/v1/gateway/ui')
def getgatewayui():
    try:
        apiurl = "http://localhost:4000"
        return apiurl
    except Exception as e:
        return e
          
if __name__ == '__main__':
    app.run('0.0.0.0',5000,debug = True)
