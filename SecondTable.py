import tkinter as tk
from tkinter import ttk
from DialogSecond import DialogSecond
from tkinter import messagebox
from database import Database


class SecondTable(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.db = Database()
        self.init_main()

    def init_main(self):
        self.toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        btn_open_add = tk.Button(self.toolbar, text='Добавить значение', command=self.open_add,
         bd = 1, compound=tk.TOP)
        btn_open_add.pack(side=tk.LEFT)

        btn_open_del = tk.Button(self.toolbar, text='Удалить значение', command=self.open_delete, bd = 1,
         compound=tk.TOP)
        btn_open_del.pack(side=tk.LEFT)

        btn_open_pars = tk.Button(self.toolbar, text='Показать таблицу с параметрами', command=self.open_pars, bd = 1,
         compound=tk.TOP)
        btn_open_pars.pack(side=tk.LEFT)

        btn_update = tk.Button(self.toolbar, text='Обновить', command=self.view_records, bd = 1,
         compound=tk.TOP)
        btn_update.pack(side=tk.LEFT)
        
        btn_erase = tk.Button(self.toolbar, text='Очистить', command=self.erase, bd = 1,
         compound=tk.TOP)
        btn_erase.pack(side=tk.LEFT)

        columns = ('Brand', 'Location')
        self.tree = ttk.Treeview(self, column=columns, height=18, show='headings')
        headings = ['Бренд', 'Местоположение']
        widths = [200, 400]
        for i in range(len(columns)):
            self.tree.column(columns[i], width=widths[i], anchor=tk.CENTER)
            self.tree.heading(columns[i], text=headings[i])
    
        self.tree.pack()
        self.view_records()

    def records(self, brand, place):
        self.db.insert_location(brand, place)
        self.view_records()

    def get_count(self, brand, place):
        self.db.get_count_location(brand, place)

    def delete_records(self, brand, place):
        self.db.delete_location(brand, place)
        self.view_records()

    def fetchall(self):
        return self.db.c.fetchall()

    def view_records(self, brand='', place=''):
        self.db.show_location(brand, place)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_add(self):
        DialogSecond(self.root, self)

    def open_delete(self):
        DialogSecond(self.root, self, on_delete=True)

    def open_pars(self):
        DialogSecond(self.root, self, on_pars=True)

    def erase(self):
        self.db.erase_location()
        self.view_records()