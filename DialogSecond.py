import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class DialogSecond(tk.Toplevel):
    def __init__(self, root, app, on_delete=False, on_pars=False):
        self.root = root
        super().__init__(self.root)
        self.on_delete = on_delete
        self.on_pars = on_pars
        self.init_child()
        self.view = app
      

    def init_child(self):
        if self.on_delete:
            self.title('Удалить значение')
        elif self.on_pars:
            self.title('Показать с параметрами')
        else:
            self.title('Добавить значение')
        
        self.geometry('400x160+400+300')
        self.resizable(False, False)
        places = [50, 80]
        j = 0
        label_brand = ttk.Label(self, text='Бренд')
        label_brand.place(x=50, y=places[j])
        j += 1
        label_size = ttk.Label(self, text='Местоположение')
        label_size.place(x=50, y=places[j])
        j = 0
        self.entry_brand = ttk.Entry(self)
        self.entry_brand.place(x=200, y=places[j])
        j += 1
        self.entry_place = ttk.Entry(self)
        self.entry_place.place(x=200, y=places[j])

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=110)
        btn_add = None
        if self.on_delete:
            btn_add = ttk.Button(self, text='Удалить')
        elif self.on_pars:
            btn_add = ttk.Button(self, text='Показать')
        else:
            btn_add = ttk.Button(self, text='Добавить')    
        btn_add.place(x=220, y=110)
        btn_add.bind('<Button-1>', self.activate)

        self.grab_set()
        self.focus_set()    

    def activate(self, event):
        if self.on_delete:
            self.view.get_count(self.entry_brand.get(), self.entry_place.get())
            self.show_message(f'Будет удалено {self.view.fetchall()[0][0]}')
            self.view.delete_records(self.entry_brand.get(), self.entry_place.get())
        elif self.on_pars:
            self.view.view_records(self.entry_brand.get(), self.entry_place.get())
        else:
            if len(self.entry_brand.get()) == 0 or len(self.entry_place.get()) == 0:
                self.show_message()
            else:
                self.view.records(self.entry_brand.get(), self.entry_place.get()) 

    def show_message(self, text ='Пожалуйста, введите значения всех полей' ):
        messagebox.showinfo('Оповещение',text)