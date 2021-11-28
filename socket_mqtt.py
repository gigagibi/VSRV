import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client()

topics = ['socket1/voltage', 'socket1/turn', 'socket2/voltage',
          'socket2/turn', 'socket3/voltage', 'socket3/turn', 'socket4/voltage', 'socket4/turn']
sockets_turned = {'socket1': True, 'socket2': True,
                  'socket3': True, 'socket4': True}
sockets_voltages = {'socket1': 220,
                    'socket2': 220, 'socket3': 220, 'socket4': 220}


def on_connect(client, userdata, flags, rc):
    client.subscribe([(topics[0], 0), (topics[1], 0), (topics[2], 0), (topics[3], 0),
                     (topics[4], 0), (topics[5], 0), (topics[6], 0), (topics[7], 0)])


def send_random_voltage(socket):
    if sockets_turned[socket] == True:
        voltage=random.randint(100, 300)
        client.publish(topic=socket +
                       '/voltage', payload=str(voltage))
        sockets_voltages[socket]=voltage
    else:
        print(socket + ' OFF')


def check_voltage(socket):
    if (sockets_voltages[socket] <= 210 or sockets_voltages[socket] >= 240) and sockets_voltages[socket]!=0:
        sockets_turned[socket] = False
        sockets_voltages[socket]=0
        client.publish(topic=socket+'/turn', payload='0')


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(topic + ' || ' + payload)

    if '/turn' in topic and 'socket' in topic:
        if payload == '1':
            print(topic)
            sockets_turned[topic[:7]] = True
            print(topic[:7])
            client.publish(topic=topic[:7]+'/voltage', payload='220')
        elif payload == '0':
            print(topic)
            sockets_turned[topic[:7]] = False
            print(topic[:7])
            client.publish(topic=topic[:7]+'/voltage', payload='0')


client.connect("localhost", 1883, 45)
client.loop_start()
client.on_message = on_message
client.on_connect = on_connect
try:
    while True:
        time.sleep(1)
        # tpc = 'socket3'
        tpc = 'socket'+str(random.randint(1, 4))
        # send_random_voltage(tpc)
        check_voltage(tpc)

except KeyboardInterrupt:
    print('exiting')
    client.disconnect()
    client.loop_stop()
