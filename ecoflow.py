import requests
import hmac
import hashlib
from datetime import timezone
import datetime
import random
import json
import os

BROKER_ADDRESS = os.environ.get("MQTT_BROKER_ADDRESS")
PORT = int(os.environ.get("MQTT_PORT"))
QOS = int(os.environ.get("MQTT_QOS"))

db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_pwd  = os.environ.get("DB_PWD")

accessKey=os.environ.get("ECOFLOW_ACCESSKEY")
secretKey=os.environ.get("ECOFLOW_SECRETKEY")
sn=os.environ.get("ECOFLOW_SN")

params = ""
nonce=f"{random.randint(0,999999):06d}"
server = "https://api.ecoflow.com"
endpoint = "/iot-open/sign/device/list"
# EcoFlow sample timestamp: timestamp=1671171709428 - has three sub-second digits!
timestamp=f"{int(datetime.datetime.now(timezone.utc).timestamp() * 1000)}"

def create_sig(url_params):
    signature = hmac.new(bytes(secretKey, 'latin-1'), msg=bytes(url_params, 'latin-1'), digestmod=hashlib.sha256).hexdigest()
    print(signature)
    return signature


def get_device_list():
    url_params = f"{params}accessKey={accessKey}&nonce={nonce}&timestamp={timestamp}"
    print(url_params)
    sig = create_sig(url_params)

    headers = {
                'accessKey': accessKey,
                'nonce': nonce,
                'timestamp': timestamp,
                'sign': sig
            }
    print(headers)
    url = f"{server}{endpoint}" # note: do NOT provide GET parameters
    print(url)

    r = requests.get(url, headers=headers)
    print(r)
    jso = r.json()
    return jso


def get_mqtt_certification():
    endpoint = "/iot-open/sign/certification"
    url_params = f"{params}accessKey={accessKey}&nonce={nonce}&timestamp={timestamp}"
    print(url_params)
    sig = create_sig(url_params)

    headers = {
                'accessKey': accessKey,
                'nonce': nonce,
                'timestamp': timestamp,
                'sign': sig
            }
    print(headers)
    url = f"{server}{endpoint}" # note: do NOT provide GET parameters
    print(url)

    r = requests.get(url, headers=headers)
    print(r)
    jso = r.json()
    return jso


def get_quota_all():
    endpoint = "/iot-open/sign/device/quota/all"
    params = f"sn={sn}"
    url_params = f"{params}&accessKey={accessKey}&nonce={nonce}&timestamp={timestamp}"
    print(url_params)
    sig = create_sig(url_params)

    headers = {
                'accessKey': accessKey,
                'nonce': nonce,
                'timestamp': timestamp,
                'sign': sig
            }
    print(headers)
    url = f"{server}{endpoint}?{params}"
    print(url)

    r = requests.get(url, headers=headers)
    print(r)
    jso = r.json()
    return jso


def set_quota():
    soc = 50
    endpoint = "/iot-open/sign/device/quota"
    params = {  'sn': sn,
                "params":
                    { "cmdSet": 32, "id": 49, "maxChgSoc": soc }
             }
    # The important things to keep in mind are
    # 1. we really need the JSON also for signature in this URL format
    # 2. the URL params MUST be alphabetically sorted (strange, but true)
    sig_params=f"params.cmdSet=32&params.id=49&params.maxChgSoc={soc}&sn={sn}&"
    url_params = f"{sig_params}accessKey={accessKey}&nonce={nonce}&timestamp={timestamp}"
    print(url_params)
    sig = create_sig(url_params)

    headers = {
                #'Content-type': 'application/json;charset=UTF-8',
                'accessKey': accessKey,
                'nonce': nonce,
                'timestamp': timestamp,
                'sign': sig
            }
    print(headers)
    url = f"{server}{endpoint}"
    #url = f"{server}{endpoint}?{sig_params}"
    print(url)

    r = requests.put(url, headers=headers, json=params)
    #r = requests.put(url, headers=headers)
    print(r)
    jso = r.json()
    return jso


#jso = get_device_list()
#jso = get_mqtt_certification()
#print(json.dumps(jso))
#jso = get_quota_all()
jso = set_quota()
print(json.dumps(jso))

