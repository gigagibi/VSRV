from tkinter import *
import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
sockets = {}
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


def do_scenario():
    if (scenario_condition_attribute_var.get() == 'turned' and scenario_condition_value_var.get() in ['1', 'on'] and sockets[scenario_condition_socket_var.get()].lbl_voltage['text'] != '0v') or + \
    (scenario_condition_attribute_var.get()=='turned' and scenario_condition_value_var.get() in ['0', 'off'] and sockets[scenario_condition_socket_var.get()].lbl_voltage['text'] == '0v') or + \
    (scenario_condition_attribute_var.get()=='voltage' and sockets[scenario_condition_socket_var.get()].lbl_voltage['text'] == scenario_condition_value_var.get()+'v'):
        if scenario_action_attribute_var.get() == 'turned':
            if scenario_action_value_var.get() in ['1', 'on'] and sockets[scenario_action_socket_var.get()].lbl_voltage['text']=='0v':
                turn(scenario_action_socket_var.get(), 'on')
            elif scenario_action_value_var.get() in ['0', 'off'] and sockets[scenario_action_socket_var.get()].lbl_voltage['text']!='0v':
                turn(scenario_action_socket_var.get(), 'off')


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




root = Tk()


root['bg'] = 'white'
root.title('тест')

create_socket('socket1')
create_socket('socket2')
create_socket('socket3')
create_socket('socket4')
create_socket('socket5')
create_socket('socket6')

scenario_frame = Frame(root)
scenario_condition_socket_var = StringVar(value='None')
scenario_condition_attribute_var = StringVar(value='None')
scenario_condition_value_var = StringVar(value='None')
scenario_action_socket_var = StringVar(value='None')
scenario_action_attribute_var = StringVar(value='None')
scenario_action_value_var = StringVar(value='None')
lbl_scenario_condition = Label(scenario_frame, text='Условие')
lbl_scenario_action = Label(scenario_frame, text='Действие')
sockets_keys = sockets.keys()
opt_scenario_action_socket = OptionMenu(
    scenario_frame, scenario_action_socket_var, *sockets_keys)
opt_scenario_action_attribute = OptionMenu(
    scenario_frame, scenario_action_attribute_var, *['None', 'turned'])
entry_scenario_action_value = Entry(
    scenario_frame, textvariable=scenario_action_value_var)
opt_scenario_condition_socket = OptionMenu(
    scenario_frame, scenario_condition_socket_var, *sockets_keys)
opt_scenario_condition_attribute = OptionMenu(
    scenario_frame, scenario_condition_attribute_var, *['None', 'turned', 'voltage'])
entry_scenario_condition_value = Entry(
    scenario_frame, textvariable=scenario_condition_value_var)


lbl_scenario_condition.grid(row=0, column=0)
opt_scenario_condition_socket.grid(row=1, column=0)
opt_scenario_condition_attribute.grid(row=1, column=1, columnspan=5)
entry_scenario_condition_value.grid(row=1, column=6)
lbl_scenario_action.grid(row=2, column=0)
opt_scenario_action_socket.grid(row=3, column=0)
opt_scenario_action_attribute.grid(row=3, column=1)
entry_scenario_action_value.grid(row=3, column=6)
scenario_frame.grid(row=1, column=0, columnspan=6)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if '/voltage' in topic:
        sockets[topic[:7]].lbl_voltage['text'] = payload+'v'
        if scenario_condition_socket_var.get()==topic[:7]:
            do_scenario()


def on_connect(client, userdata, flags, rc):
    for s in sockets:
        client.subscribe(s+'/voltage')
        client.subscribe(s+'/turn')


client.on_connect = on_connect
client.on_message = on_message


client.connect('localhost', 1883, 45)
client.loop_start()

root.mainloop()
