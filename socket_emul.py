import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client()


class Socket:
    def __init__(self, name, turned, voltage, temperature, amperage, power):
        self.name = name
        self.turned = turned
        self.voltage = voltage
        self.temperature = temperature
        self.amperage = amperage
        self.power = power


sockets = {'socket1': Socket('socket1', True, 220, random.randint(30, 40), random.randint(5, 15), random.randint(10, 120)),
           'socket2': Socket('socket2', True, 220, random.randint(30, 40), random.randint(5, 15), random.randint(10, 120)),
           'socket3': Socket('socket3', True, 220, random.randint(30, 40), random.randint(5, 15), random.randint(10, 120)),
           'socket4': Socket('socket4', True, 220, random.randint(30, 40), random.randint(5, 15), random.randint(10, 120)),
           'socket5': Socket('socket5', True, 220, random.randint(30, 40), random.randint(5, 15), random.randint(10, 120)),
           'socket6': Socket('socket6', True, 220, random.randint(30, 40), random.randint(5, 15), random.randint(10, 120))}


def on_connect(client, userdata, flags, rc):
    for socket in sockets:
        client.subscribe(socket+'/turn')
        client.subscribe(socket+'/voltage')


def send_random_voltage(socket):
    if sockets[socket].turned == True:
        voltage = random.randint(100, 300)
        client.publish(topic=socket +
                       '/voltage', payload=str(voltage))
        sockets[socket].voltage = voltage
    else:
        print(socket + ' OFF')


def check_voltage(socket):
    if (sockets[socket].voltage <= 210 or sockets[socket].voltage >= 240) and sockets[socket].voltage != 0:
        sockets[socket].turned = False
        sockets[socket].voltage = 0
        client.publish(topic=socket+'/turn', payload='0')


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(topic + ' || ' + payload)

    if '/turn' in topic and 'socket' in topic:
        if payload == '1':
            print(topic)
            sockets[topic[:7]].turned = True
            sockets[topic[:7]].temperature = random.randint(30, 40)
            sockets[topic[:7]].amperage = random.randint(5, 15)
            sockets[topic[:7]].power = random.randint(10, 120)
            print(topic[:7])
            client.publish(topic=topic[:7]+'/voltage', payload='220')
            client.publish(topic=topic[:7]+'/amperage', payload=sockets[topic[:7]].amperage)
            client.publish(topic=topic[:7]+'/temperature', payload=sockets[topic[:7]].temperature)
            client.publish(topic=topic[:7]+'/power', payload=sockets[topic[:7]].power)
        elif payload == '0':
            sockets[topic[:7]].turned = False
            sockets[topic[:7]].temperature = 0
            sockets[topic[:7]].amperage = 0
            sockets[topic[:7]].power = 0
            client.publish(topic=topic[:7]+'/voltage', payload='0')
            client.publish(topic=topic[:7]+'/amperage', payload=sockets[topic[:7]].amperage)
            client.publish(topic=topic[:7]+'/temperature', payload=sockets[topic[:7]].temperature)
            client.publish(topic=topic[:7]+'/power', payload=sockets[topic[:7]].power)


client.connect("localhost", 1883, 45)
client.on_message = on_message
client.on_connect = on_connect
client.loop_start()

try:
    while True:
        time.sleep(1)
        tpc = 'socket'+str(random.randint(1, 6))
        # send_random_voltage(tpc)
        check_voltage(tpc)

except KeyboardInterrupt:
    print('exiting')
    client.disconnect()
    client.loop_stop()
