import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class DialogFirst(tk.Toplevel):
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
        
        self.geometry('400x240+400+300')
        self.resizable(False, False)
        places = [50, 80, 110, 140]
        j = 0
        label_id = None
        if self.on_delete or self.on_pars:
            label_id = ttk.Label(self, text='ID')
            label_id.place(x=50, y=places[j])
            j += 1

        label_brand = ttk.Label(self, text='Бренд')
        label_brand.place(x=50, y=places[j])
        j += 1
        label_size = ttk.Label(self, text='Размер')
        label_size.place(x=50, y=places[j])
        j += 1
        label_cost = ttk.Label(self, text='Цена')
        label_cost.place(x=50, y=places[j])
        j = 0

        self.entry_id = None
        if self.on_delete or self.on_pars:
            self.entry_id = ttk.Entry(self)
            self.entry_id.place(x=200, y=places[j])
            j += 1    

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=places[j])
        j += 1
        self.combobox = ttk.Combobox(self, values=[u'', u'XS', u'S', u'M', u'L', u'XL'], state='readonly')
        self.combobox.current(0)
        self.combobox.place(x=200, y=places[j])
        j+=1
        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=places[j])

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)
        btn_add = None
        if self.on_delete:
            btn_add = ttk.Button(self, text='Удалить')
        elif self.on_pars:
            btn_add = ttk.Button(self, text='Показать')
        else:
            btn_add = ttk.Button(self, text='Добавить')    
        btn_add.place(x=220, y=170)
        btn_add.bind('<Button-1>', self.activate)

        self.grab_set()
        self.focus_set()    

    def activate(self, event):
        if self.on_delete:
            _id = self.entry_id.get()
            if _id == '':
                _id = '-1'
            money = self.entry_money.get() 
            if money == '':
                money = '-1'
            self.view.get_count(_id, self.entry_description.get(), self.combobox.get(), money)
            self.show_message(f'Будет удалено {self.view.fetchall()[0][0]}')
            self.view.delete_records(_id, self.entry_description.get(), self.combobox.get(), money)
        elif self.on_pars:
            money = self.entry_money.get() 
            if money == '':
                money = '-1'
            _id = self.entry_id.get()
            if _id == '':
                _id = '-1'
            self.view.view_records(_id, self.entry_description.get(), self.combobox.get(), money)
        else:
            if len(self.entry_description.get()) == 0 or len(self.entry_money.get()) == 0 or len(self.combobox.get()) == 0:
                self.show_message()
            else:
                self.view.records(self.entry_description.get(), self.combobox.get(), self.entry_money.get()) 

    def show_message(self, text ='Пожалуйста, введите значения всех полей' ):
        messagebox.showinfo('Оповещение',text)
        