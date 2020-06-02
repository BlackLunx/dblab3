import tkinter as tk
from tkinter import ttk
from SecondTable import SecondTable
from FirstTable import FirstTable
from database import get_connection
from tkinter import messagebox
from sqlfunctions import creating

def clicked():
    root = tk.Tk()
    nb = ttk.Notebook(root)
    f1 = FirstTable(root)
    f2 = SecondTable(root)
    nb.pack()

    nb.add(f1, text='page1')
    nb.add(f2, text='page2')

    root.title('Database')
    root.geometry('650x450+300+200')
    root.resizable(False, False)
    root.mainloop()

def delete():
    connection = get_connection('postgres', 'postgres', 'postgres')
    c = connection.cursor()
    c.execute(creating)
    c.execute(f'''SELECT drop_database()''')
    c.close()
    messagebox.showinfo('Оповещение', 'Успешно удалено')

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Главный экран')
    window.geometry('200x200+400+400')
    btn = tk.Button(window, text='Создать и Открыть', command=clicked)
    btn2 = tk.Button(window, text='Удалить', command=delete)
    btn.grid(column=1, row=2)
    btn2.grid(column=2, row=2)
    window.mainloop()

    