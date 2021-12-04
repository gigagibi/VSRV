from tkinter import *
root = Tk()

def do_some(*args):
    print("VALUE IS CHANGED")

l = ["one", "two", "three"]
root['bg'] = 'white'
root.title('тест')
chosen_label = Label(root, text="chosen")
a = StringVar()
entry = Entry(root, textvariable=a)
options = OptionMenu(root, a, *l)
label = Label(root, textvariable=a)

entry.pack()
label.pack()
options.pack()
time_massive = '1:0:59'.split(':')
seconds = int(time_massive[0]) * 3600 + int(time_massive[1]) * 60 + int(time_massive[2])
print(seconds)
a.trace("w", do_some)
root.mainloop()
