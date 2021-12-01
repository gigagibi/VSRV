from tkinter import *
import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
sockets = {}


def turn(socket, mode, seconds=0):
    if seconds == 0:
        if mode == 'on':
            client.publish(topic=socket+'/turn', payload='1')
        if mode == 'off':
            client.publish(topic=socket+'/turn', payload='0')
    else:
        root.after(1000, lambda: turn(socket, mode, seconds-1))


def create_socket(socket_name):
    sockets[socket_name] = Socket(socket_name)


def timeout_into_seconds(timeout_val):
    time_massive = timeout_val.split(':')
    seconds = int(time_massive[0]) * 3600 + \
        int(time_massive[1]) * 60 + int(time_massive[2])
    return seconds


class Socket:
    def __init__(self, socket):
        self.frame = Frame(root, bg='grey', width=100, height=100)
        self.lbl_voltage = Label(self.frame, text='0v', bg='white')
        self.lbl_power = Label(self.frame, text='0w', bg='white')
        self.lbl_amperage = Label(self.frame, text='0a', bg='white')
        self.btn_on = Button(self.frame, text='Включить',
                             bg='yellow', command=lambda: turn(socket, 'on'))
        self.btn_off = Button(self.frame, text='Выключить',
                              bg='yellow', command=lambda: turn(socket, 'off'))

        self.timeout = StringVar(value='0:0:0')
        self.entry_timer = Entry(self.frame, textvariable=self.timeout)

        self.btn_timer_mode_on = Button(self.frame, text='Вкл по таймеру',
                                        bg='white', command=lambda: turn(socket, 'on', timeout_into_seconds(self.timeout.get())))
        self.btn_timer_mode_off = Button(self.frame, text='Выкл по таймеру',
                                         bg='white', command=lambda: turn(socket, 'off', timeout_into_seconds(self.timeout.get())))

        self.lbl_voltage.pack()
        self.lbl_power.pack()
        self.lbl_amperage.pack()
        self.btn_on.pack()
        self.btn_off.pack()
        self.entry_timer.pack()
        self.btn_timer_mode_on.pack()
        self.btn_timer_mode_off.pack()
        self.frame.grid(row=0, column=int(socket[6]))


root = Tk()

root['bg'] = 'white'
root.title('тест')

create_socket('socket1')
create_socket('socket2')
create_socket('socket3')
create_socket('socket4')
create_socket('socket5')
create_socket('socket6')


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    if '/voltage' in topic:
        socket_number = int(topic[6])
        print(str(socket_number) + ' || ' + payload + 'v')
        sockets[topic[:7]].lbl_voltage['text'] = payload+'v'


def on_connect(client, userdata, flags, rc):
    for s in sockets:
        client.subscribe(s+'/voltage')
        client.subscribe(s+'/turn')


client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 45)
client.loop_start()

root.mainloop()
