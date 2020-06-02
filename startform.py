from tkinter import *

def clicked():
    res = f'Привет, {txt.get()}'
    lbl.configure(text=res)

window = Tk()
window.title('Главный экран')
window.geometry('400x300')
lbl = Label(window, text='')
lbl.grid(column=0, row=0)
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
btn = Button(window, text='Создать', command=clicked)
btn.grid(column=2, row=0)
window.mainloop()