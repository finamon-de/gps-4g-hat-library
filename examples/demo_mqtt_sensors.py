'''
  demo_echo.py - This is basic Finamon GNSS/4G Modem HAT Shield mqqt example.
'''
import json
import time
import os

from gps4ghat.BG77X  import BG77X
from gps4ghat.MC34X9 import MC34X9
from gps4ghat.MC34X9 import MC34X9_RANGE
from gps4ghat.GPS_4G_HAT_HW import GPS_4G_HAT_HW

sensors_json_string = """{
    "imei": "0",
    "x": 0,
    "y": 0,
    "z": 0,
    "status": 0,
    "utc": 0
}
"""

#----------------------------------------------------------------------------------------
#   network access and MQTT service data
#----------------------------------------------------------------------------------------

module = BG77X()
module.debug_print("MQTT client sensors information demo")

mqtt_topic = os.environ.get("MQTT_TOPIC_SENSORS") + os.environ.get("MQTT_CLIENT_ID")
mqtt_receive_topic = os.environ.get("MQTT_TOPIC_RECEIVE") + os.environ.get("MQTT_CLIENT_ID")
mqtt_json = json.loads(sensors_json_string)
mqtt_json['imei'] = module.getIMEI()

accel = MC34X9()

SAMPLE_RATE = 0x10
AM_DEBOUNCE = 5
AM_THRESHOLD = 150

accel.setStandbyMode()                      #Put accelerometer in standby mode
accel.setGPIOControl(0b00001100)            #Set GPIO control. Set bit 2 to 1 for INT active high, set bit 3 to 1 for INT push-pull
accel.setSampleRate(SAMPLE_RATE)            #Set the sample rate

accel.setInterrupt(0b00000100)              #Set the interrupt enable register, bit 0 enables tilt, bit 1 enables flip, bit 3 enables shake. Set bit 6 to 1 for autoclear
accel.setAnymotionThreshold(AM_THRESHOLD)   #Set tilt threshold
accel.setAnymotionDebounce(AM_DEBOUNCE)     #Set tilt debounce
accel.setMotionControl(0b00000100)          #Enable motion control features. Bit 0 enables tilt/flip, bit 2 enables anymotion (req for shake), bit 3 enables shake, bit 5 inverts z-axis

accel.setRange(MC34X9_RANGE.RANGE_2G.value) #Set accelerometer range
accel.clearInterrupts()                     #Clear the interrupt register
accel.resetMotionControl()                  #Reset the motion control
accel.setWakeMode()                         #Wake up accelerometer

accel.readAccel()

mqtt_json['x'] = accel.acc['Xg']
mqtt_json['y'] = accel.acc['Yg']
mqtt_json['z'] = accel.acc['Zg']
module.debug_print("X %5.3f  Y %5.3f Z %5.3f m/s^2" % (mqtt_json['x'], mqtt_json['y'], mqtt_json['z']))


shield = GPS_4G_HAT_HW()
mqtt_json['status'] = shield.getStatus()
module.debug_print("GPIO status: 0x%04X" % mqtt_json['status'])

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




