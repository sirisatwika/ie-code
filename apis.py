import requests
from datetime import datetime, timedelta
import time
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from createcacert import createX509
from createsymkey import createSymKey


# creating a Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

  
@app.route('/')
@cross_origin()
def home():
    return "Welcome to Inteligent Edge!!!"
  
@app.route('/api/v1/gateway/provisionx509cert')
@cross_origin()
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
@cross_origin()
def provisiondevicecertx509():
    try:
        createX509()
        return 'Success'
    except Exception as e:
        return e

@app.route('/api/v1/device/provisionsymkey')
@cross_origin()
def provisiondevicesymmetrickey():
    try:
        symkey = createSymKey()
        return symkey
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/provisioned')
@cross_origin()
def getgatewayprovcount():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        gatewaycount = response.json()['totalCount']
        return str(gatewaycount)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/unprovisioned')
def getgatewayunprovcount():
    try:
        apiurl_prov = "http://localhost:59881/api/v2/device/all"
        response_prov = requests.get(apiurl_prov)
        gatewaycount_prov = response_prov.json()['totalCount']
        
        apiurl_tot = "http://localhost:59881/api/v2/deviceprofile/all"
        response_tot = requests.get(apiurl_tot)
        gatewaycount_tot = response_tot.json()['totalCount']
        return str(gatewaycount_tot - gatewaycount_prov)
    except Exception as e:
        return e
        
@app.route('/api/v1/gateway/count/total')
@cross_origin()
def getgatewaytotalcount():
    try:
        apiurl_tot = "http://localhost:59881/api/v2/deviceprofile/all"
        response_tot = requests.get(apiurl_tot)
        gatewaycount_tot = response_tot.json()['totalCount']
        return str(gatewaycount_tot)
    except Exception as e:
        return e


@app.route('/api/v1/gateway/count/online')
@cross_origin()
def getonlinecount():
    try:
        apiurl = "http://localhost:59881/api/v2/device/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        cnt = 0;
        for d in devicelist:
            if d['operatingState'] == "UP":
                cnt += 1
        return str(cnt)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/offline')
@cross_origin()
def getofflinecount():
    try:
        apiurl = "http://localhost:59880/api/v2/event/all"
        response = requests.get(apiurl)
        devicelist = response.json()['devices']
        cnt = 0;
        for d in devicelist:
            if d['operatingState'] == "DOWN":
                cnt += 1
        return str(cnt)
    except Exception as e:
        return e

@app.route('/api/v1/gateway/count/active')
@cross_origin()
def getactivecount():
    try:
    	curr_time = time.time_ns()
    	print(curr_time)
    	prev_time = datetime.now() - timedelta(seconds = 2)
    	prev_ns = int(time.mktime(prev_time.timetuple()) * pow(10, 9))
    	print(prev_ns)
        apiurl1 = f"http://localhost:59880/api/v2/event/start/{prev_ns}/end/{curr_time}"
        response = requests.get(apiurl1)
        return response.json();
    except Exception as e:
        return e


@app.route('/api/v1/gateway/profiles')
@cross_origin()
def getgatewayprofilelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceprofile/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e
        
@app.route('/api/v1/gateway/services')
@cross_origin()
def getgatewaydeviceservicelist():
    try:
        apiurl = "http://localhost:59881/api/v2/deviceservice/all"
        response = requests.get(apiurl)
        return response.json()
    except Exception as e:
        return e      
                 
if __name__ == '__main__':
    app.run('0.0.0.0',5000,debug = True)

