from tkinter import *
root = Tk()

root['bg'] = 'white'
root.title('тест')
a = StringVar()
entry = Entry(root, textvariable=a)

label = Label(root, textvariable=a)

entry.pack()
label.pack()
time_massive = '1:0:59'.split(':')
seconds = int(time_massive[0]) * 3600 + int(time_massive[1]) * 60 + int(time_massive[2])
print(seconds)
root.mainloop()
