# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import json
import base64
import binascii

MQTTHOST = "192.168.1.199"
MQTTPORT = 1883
mqttClient = mqtt.Client()
# 连接MQTT服务器
def on_mqtt_connect():
  mqttClient.connect(MQTTHOST, MQTTPORT, 60)
  mqttClient.loop_start()
# publish 消息
def on_publish(topic, payload, qos):
  mqttClient.publish(topic, payload, qos)
# 消息处理函数
def on_message_come(lient, userdata, msg):
  jsondata = str(msg.payload)
  text = json.loads( jsondata )
  base64str = text['data']
  decodestr = base64.b64decode(base64str.encode('utf-8')) 
  text['data'] = binascii.b2a_hex(decodestr)
  del text['applicationName']
  del text['deviceName']
  del text['applicationID']
  print(json.dumps(text))
  #print(msg.topic + " " + ":" + str(msg.payload))
  
# subscribe 消息
def on_subscribe():
  mqttClient.subscribe("application/#", 1)
  mqttClient.on_message = on_message_come # 消息到来处理函数
def main():
  on_mqtt_connect()
  on_subscribe()
  while True:
    pass
if __name__ == '__main__':
  main()
