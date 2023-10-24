from datetime import datetime, timedelta
import time
import ssl
import paho.mqtt.client as paho
from paho import mqtt
import collections
import json
import yaml
from datetime import datetime

# setting callbacks for different events to see if it works, print the message etc.


def on_connect(client, userdata, flags, rc, properties=None):
    #print("CONNACK received with code %s." % rc)
    pass

# with this callback you can see if your publish was successful


def on_publish(client, userdata, mid, properties=None):
    print("Successfully published message: " + str(mid))

# print which topic was subscribed to


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# Amazon's certificate from Third party       # Root_CA_Certificate_Name
caPath = "AmazonRootCA1.pem.crt"
# <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
certPath = "38103a25d2_certificate.pem.crt"
# <Thing_Name>.private.key Thing's private key from Amazon
keyPath = "38103a25d2_private.pem.key"

broker = 'a1ckbk76w9swxa-ats.iot.us-east-1.amazonaws.com'
port = 8883
client = paho.Client()
client.on_connect = on_connect

client.tls_set(caPath, certfile=certPath, keyfile=keyPath,
               cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# client.username_pw_set('vladCom', 'iotProject21!') # set the credentials
client.connect(broker, port)  # connect to the broker

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.loop_start()
#name = input('Introduce the name for the person you want to see the data: ')
name = 'vlad'
reference = 'health'
topic = '/' + name.lower() + '/' + reference + '/';
client.subscribe(topic + '#')
while True:
    with open('heartdata.txt', 'r') as f:
        heartdata = f.read()
    payload = {
        "heart_rate": int(heartdata),
        "unit": "bpm"
        
    }
    client.publish(topic + 'heartdata', payload=json.dumps(payload))
    f.close()
    with open('stepsdata.txt', 'r') as f:
        stepsdata = f.read()
    payload = {
        "steps": int(float(stepsdata.replace(',', '.'))),
        "unit": "steps"
    }
    client.publish(topic + 'stepsdata', payload=json.dumps(payload))
    f.close()
    with open('activity.txt', 'r') as f:
        activitydata = f.read()
        payload = {
            "activity": activitydata,
            "unit": "kcal"
        }
    client.publish(topic + 'activity', payload=json.dumps(payload))
    f.close()
    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {
        'name': name,
        'reference': reference,
        'data': {
            'heart rate': {
                'value': int(heartdata),
                'unit': 'bpm',
                'topic': topic + 'heartdata'
            },
            'steps': {
                'value': int(float(stepsdata.replace(',', '.'))),
                'unit': 'steps',
                'topic': topic + 'stepsdata'
            },
            'activity': {
                'value': int(activitydata),
                'unit': 'kcal',
                'topic': topic + 'activity'
            }
        },
        'date and time': dt       
    }
    with open('data.yaml', 'a+') as f:
        yaml.dump(data, f, allow_unicode=True)
        f.write("*********************************************************\n")
    f.close()
    time.sleep(30)
