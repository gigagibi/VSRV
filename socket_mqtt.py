import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client()

topics = ['socket1/voltage', 'socket1/turn', 'socket2/voltage',
          'socket2/turn', 'socket3/voltage', 'socket3/turn', 'socket4/voltage', 'socket4/turn']
sockets_turned = {'socket1' : True, 'socket2' : True, 'socket3' : False, 'socket4' : False}

def on_connect(client, userdata, flags, rc):
    client.subscribe([(topics[0], 0), (topics[1], 0), (topics[2], 0), (topics[3], 0),
                     (topics[4], 0), (topics[5], 0), (topics[6], 0), (topics[7], 0)])


def on_message(client, userdata, msg):
    topic = msg.topic.decode('utf-8')
    payload = msg.payload.decode('utf-8')
    print(topic + ' || ' + payload)

    if '/turn' in topic and 'socket' in topic:
        if payload=='1':
            sockets_turned[int(topic[6])] = True
        elif payload=='0':
            sockets_turned[int(topic[6])] = True
        

client.connect("localhost", 1883, 45)
client.loop_start()

try:
    while True:
        # time.sleep(5)
        tpc = 'socket'+str(random.randint(1, 4))
        if sockets_turned[tpc] == True:
            client.publish(topic=tpc +
                        '/voltage', payload=str(random.randint(100, 300)))
except KeyboardInterrupt:
    print('exiting')
    client.disconnect()
    client.loop_stop()
