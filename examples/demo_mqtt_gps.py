'''
  demo_echo.py - This is basic Finamon GNSS/4G Modem HAT Shield mqqt example.
'''
import json
import time
import os

from gps4ghat.BG77X import BG77X

gps_json_string = """{
    "imei": "0",
    "latitude": 0,
    "longitude": 0,
    "altitude": 0,
    "utc": 0
}"""

lat_org = 51.22904
lon_org = 6.71466
#----------------------------------------------------------------------------------------
#   network access and MQTT service data
#----------------------------------------------------------------------------------------

module = BG77X()
module.debug_print("MQTT client GNSS position demo")

mqtt_topic = os.environ.get("MQTT_TOPIC_GPS") + os.environ.get("MQTT_CLIENT_ID")
mqtt_receive_topic = os.environ.get("MQTT_TOPIC_RECEIVE") + os.environ.get("MQTT_CLIENT_ID")

mqtt_json = json.loads(gps_json_string)
mqtt_json['imei'] = module.getIMEI()
mqtt_json['latitude'] = lat_org
mqtt_json['longitude'] = lon_org
mqtt_json['altitude'] = 0
mqtt_json['utc'] = int(time.time())
mqtt_msg = json.dumps(mqtt_json)

contextID = "1"
if module.initNetwork(contextID):
    module.activatePdpContext(contextID, 5)

    mgtt_client_idx = 0
    mqtt_client_id_string = module.IMEI
    module.openMqttConnection(mgtt_client_idx, os.environ.get("MQTT_BROKER"), os.environ.get("MQTT_PORT"))
    module.connectMqttClient(mqtt_client_id_string, os.environ.get("MQTT_USERNAME"), os.environ.get("MQTT_PASSWORD"))
    
    module.subscribeToMqttTopic(mqtt_receive_topic)
    
    module.publishMqttMessage(mqtt_topic, mqtt_msg)
    
    wait_s = 10
    module.debug_print("wait " + str(wait_s) + " s message from topic: " + mqtt_receive_topic)    
    start_time = time.time()
    while(time.time() - start_time < wait_s):  
        if(module.waitUnsolicitedStill("+QMTRECV:", 1, 160)):
            json_start = module.response.find(',"{') + 2
            if json_start > 2:
                response_json = json.loads(module.response[json_start : -3])
                print("response: " + response_json['data']['response'])
                print("topic:    " + response_json['data']['topic'])
                break
   
    module.unsubscribeFromMqttTopic(mqtt_topic)
    module.unsubscribeFromMqttTopic(mqtt_receive_topic)

    module.disconnectMqttClient();
    module.closeConnection()
    module.deactivatePdpContext(contextID, 5)

module.close()
