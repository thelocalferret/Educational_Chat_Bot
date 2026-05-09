from tkinter import *
from tkinter import ttk
root = Tk()

root.title('Bachelor Thesis')
root.geometry('720x400+150+100')
root.configure(bg='light blue')
root.resizable(False, False)

chat_history = Text(root, fg='black', border=2, bg='white', height=15, width=86, font=("calibri", 11))
chat_history.place(x=10, y=20)
prompt = StringVar()
question = Entry(root, textvariable = prompt, width=86, font=("calibri", 11))
question.place(x=10, y=350)

root.mainloop()