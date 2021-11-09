import paho.mqtt.client as mqtt

class Mqtt:
    # def __init__(self, topics):
    #   self.topics = topics

    client = mqtt.Client()
    def publish_press(self):
        self.client.publish(topic="my", payload="Pressed")

    def on_message(client, userdata, msg):
        print(msg.payload.decode("utf-8"))

    def on_connect(client, userdata, flags, rc):
        client.subscribe("my")

    def start(self):
        
        self.client.on_connect=Mqtt.on_connect
        self.client.on_message=Mqtt.on_message

        self.client.connect("localhost", 1883, 45)

        self.client.loop_start()