from tkinter import *
import paho.mqtt.client as mqtt

sockets = ['socket1', 'socket2', 'socket3', 'socket4']
client = mqtt.Client()


def turn_on(socket):
    client.publish(topic=socket+'/turn', payload='1')
def turn_off(socket):
    client.publish(topic=socket+'/turn', payload='0')
    


root = Tk()

root['bg'] = 'white'
root.title('тест')
root.geometry('600x400')


frame1 = Frame(root, bg='grey', width=100, height=100)
lbl_voltage_1 = Label(frame1, text='0.0v', bg='white')
btn_on_1 = Button(frame1, text='нажми', bg='yellow', command=lambda: turn_on('socket1'))
btn_off_1 = Button(frame1, text='нажми', bg='yellow', command=lambda: turn_off('socket1'))
lbl_voltage_1.pack()
btn_on_1.pack()
btn_off_1.pack()
frame1.grid(row=0, column=0)


frame2 = Frame(root, bg='grey', width=100, height=100)
lbl_voltage_2 = Label(frame2, text='0.0v', bg='white')
btn_on_2 = Button(frame2, text='нажми', bg='yellow', command=lambda: turn_on('socket2'))
btn_off_2 = Button(frame2, text='нажми', bg='yellow', command=lambda: turn_off('socket2'))
lbl_voltage_2.pack()
btn_on_2.pack()
btn_off_2.pack()
frame2.grid(row=0, column=1)


frame3 = Frame(root, bg='grey', width=100, height=100)
lbl_voltage_3 = Label(frame3, text='0.0v', bg='white')
btn_on_3 = Button(frame3, text='нажми', bg='yellow', command=lambda: turn_on('socket3'))
btn_off_3 = Button(frame3, text='нажми', bg='yellow', command=lambda: turn_off('socket3'))
lbl_voltage_3.pack()
btn_on_3.pack()
btn_off_3.pack()
frame3.grid(row=0, column=2)


frame4 = Frame(root, bg='grey', width=100, height=100)
lbl_voltage_4 = Label(frame4, text='0.0v', bg='white')
btn_on_4 = Button(frame4, text='нажми', bg='yellow', command=lambda: turn_on('socket4'))
btn_off_4 = Button(frame4, text='нажми', bg='yellow', command=lambda: turn_off('socket4'))
lbl_voltage_4.pack()
btn_on_4.pack()
btn_off_4.pack()
frame4.grid(row=0, column=3)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    if '/voltage' in topic:
        socket_number=int(topic[6])
        print(str(socket_number) + ' || ' + payload + 'v')
        if(socket_number==1):
            lbl_voltage_1['text']=payload+'v'
        elif(socket_number==2):
            lbl_voltage_2['text']=payload+'v'
        elif(socket_number==3):
            lbl_voltage_3['text']=payload+'v'
        elif(socket_number==4):
            lbl_voltage_4['text']=payload+'v'

def on_connect(client, userdata, flags, rc):
    for s in sockets:
        client.subscribe(s+'/voltage')
        client.subscribe(s+'/turn')


client.on_connect=on_connect
client.on_message=on_message


client.connect("localhost", 1883, 45)
client.loop_start()
root.mainloop()