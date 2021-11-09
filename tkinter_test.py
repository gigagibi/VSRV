from tkinter import *
import paho.mqtt.client as mqtt
from mqtt import Mqtt
mqtt = Mqtt()


def on_click():
    # print('Нажал')
    title['text'] = 'нажал'
    mqtt.publish_press()
    
root = Tk()

root['bg'] = 'white'
root.title('тест')
root.geometry('400x600')

canvas = Canvas(root, height=200, width=300)
canvas.pack()


frame = Frame(root, bg='grey')
frame.place(relheight=0.8, relwidth=0.8)

title = Label(frame, text='Текст', bg='red')
button = Button(frame, text='нажми', bg='yellow', command=on_click)
title.pack()
button.pack()
mqtt.start()
root.mainloop()



