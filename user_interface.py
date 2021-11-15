from tkinter import *
import paho.mqtt.client as mqtt

sockets = ['socket1', 'socket2', 'socket3', 'socket4']
client = mqtt.Client()


def turn_on(socket):
    client.publish(topic=socket+'/turn', payload='1')


def turn_off(socket):
    client.publish(topic=socket+'/turn', payload='0')


class Socket:
    def __init__(self, socket):
        self.frame = Frame(root, bg='grey', width=100, height=100)
        self.lbl_voltage = Label(self.frame, text='0.0v', bg='white')
        self.btn_on = Button(self.frame, text='нажми',
                             bg='yellow', command=lambda: turn_on(socket))
        self.btn_off = Button(self.frame, text='нажми',
                              bg='yellow', command=lambda: turn_off(socket))
        self.lbl_voltage.pack()
        self.btn_on.pack()
        self.btn_off.pack()
        self.frame.grid(row=0, column=int(socket[6]))


root = Tk()

root['bg'] = 'white'
root.title('тест')
root.geometry('600x400')


socket_panel_1 = Socket('socket1')
socket_panel_2 = Socket('socket2')
socket_panel_3 = Socket('socket3')
socket_panel_4 = Socket('socket4')


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    if '/voltage' in topic:
        socket_number = int(topic[6])
        print(str(socket_number) + ' || ' + payload + 'v')
        if(socket_number == 1):
            socket_panel_1.lbl_voltage['text'] = payload+'v'
        elif(socket_number == 2):
            socket_panel_2.lbl_voltage['text'] = payload+'v'
        elif(socket_number == 3):
            socket_panel_3.lbl_voltage['text'] = payload+'v'
        elif(socket_number == 4):
            socket_panel_4.lbl_voltage['text'] = payload+'v'


def on_connect(client, userdata, flags, rc):
    for s in sockets:
        client.subscribe(s+'/voltage')
        client.subscribe(s+'/turn')


client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 45)
client.loop_start()
root.mainloop()
