from tkinter import *
root = Tk()

root['bg'] = 'white'
root.title('тест')
a = StringVar()
entry = Entry(root, textvariable=a)

label = Label(root, textvariable=a)

entry.pack()
label.pack()
root.mainloop()
