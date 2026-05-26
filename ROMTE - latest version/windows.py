import tkinter as tk
from tkinter import ttk

def request_window(self):
    self.win = tk.Toplevel(self.root)
    self.win.title("Запрос на перемещение")
    self.win.geometry("750x250")
    self.win.transient(self.root)
    self.win.grab_set()

    self.info_label_0 = tk.Label(self.win, text="Выбор технического оборудования(по ID)", bg="white")
    self.info_label_0.place(rely=0.17, relx=0.05, width=331)

    self.info_label_1 = tk.Label(self.win, text="1 - одно оборудование\n1:10 - множество\n 1:3, 6:10, 12 - несколько множеств и единиц оборудования", justify="left", bg="white")
    self.info_label_1.place(rely=0.25, relx=0.05)

    self.info_label_2 = tk.Label(self.win, text="Перенос в:", bg="white")
    self.info_label_2.place(rely=0.29, relx=0.5, width=278)

    self.ID_label = tk.Label(self.win, text="Оборудование:", bg="white")
    self.ID_label.place(rely=0.5, relx=0.05)

    self.ID_entry = tk.Entry(self.win)
    self.ID_entry.place(rely=0.5, relx=0.17, width=240)

    self.korpus_label = tk.Label(self.win, text="Корпус:", bg="white")
    self.korpus_label.place(rely=0.39, relx=0.5)

    self.available_korpus = ["Корпус 1", "Корпус 2", "Корпус 3"]
    self.korpus_combobox = ttk.Combobox(self.win, values=self.available_korpus, state="readonly")
    self.korpus_combobox.place(rely=0.39, relx=0.565, width=228)
    self.korpus_combobox.bind("<<ComboboxSelected>>", self.update_rooms)

    self.room_label = tk.Label(self.win, text="Помещение:", bg="white")
    self.room_label.place(rely=0.49, relx=0.5)

    self.room_combobox = ttk.Combobox(self.win, state="readonly")
    self.room_combobox.place(rely=0.49, relx=0.603, width=200)

    self.confirm_button = tk.Button(self.win, text="Подтвердить", command=self.process_movement_request)
    self.confirm_button.place(rely=0.7, relx=0.44)

    self.update_rooms()


def confirm_request_window(self):
    self.conf = tk.Toplevel(self.root)
    self.conf.title("Выполнение запроса на перемещение")
    self.conf.geometry("750x350")
    self.conf.transient(self.root)
    self.conf.grab_set()

    self.requests_table_label = tk.Label(self.conf, text="Активные запросы:", bg="white")
    self.requests_table_label.place(rely=0.05, relx=0.05)

    self.requests_tree_frame = tk.Frame(self.conf)
    self.requests_tree_frame.place(rely=0.12, relx=0.05, width=650, height=250)

    requests_column_names = ["Номер запроса", "Кол-во техники", "ID техники"]

    self.requests_tree = ttk.Treeview(self.requests_tree_frame, columns=requests_column_names, show='headings')
    for col in requests_column_names:
        self.requests_tree.heading(col, text=col)
        self.requests_tree.column(col, width=150, anchor='center')

    self.requests_scrollbar = ttk.Scrollbar(self.requests_tree_frame, orient="vertical", command=self.requests_tree.yview)
    self.requests_tree.configure(yscrollcommand=self.requests_scrollbar.set)
    self.requests_scrollbar.pack(side='right', fill='y')
    self.requests_tree.pack(side='left', fill='both', expand=True)

    self.load_requests_table()

    self.request_ID_label = tk.Label(self.conf, text="Номер запроса:", bg="white")
    self.request_ID_label.place(rely=0.87, relx=0.05)

    self.request_ID_entry = tk.Entry(self.conf)
    self.request_ID_entry.place(rely=0.87, relx=0.175, width=240)

    self.confirm_execute_button = tk.Button(self.conf, text="Подтвердить\nвыполнение запроса", command=self.execute_request)
    self.confirm_execute_button.place(rely=0.85, relx=0.6)


def show_requests_table(self):
    self.req = tk.Toplevel(self.root)
    self.req.title("Просмотр таблицы запросов")
    self.req.geometry("750x350")
    self.req.transient(self.root)
    self.req.grab_set()

    self.requests_table_label = tk.Label(self.req, text="Активные запросы:", bg="white")
    self.requests_table_label.place(rely=0.05, relx=0.05)

    self.requests_tree_frame = tk.Frame(self.req)
    self.requests_tree_frame.place(rely=0.12, relx=0.05, width=650, height=250)

    requests_column_names = ["Номер запроса", "Кол-во техники", "ID техники"]

    self.requests_tree = ttk.Treeview(self.requests_tree_frame, columns=requests_column_names, show='headings')
    for col in requests_column_names:
        self.requests_tree.heading(col, text=col)
        self.requests_tree.column(col, width=150, anchor='center')

    self.requests_scrollbar = ttk.Scrollbar(self.requests_tree_frame, orient="vertical", command=self.requests_tree.yview)
    self.requests_tree.configure(yscrollcommand=self.requests_scrollbar.set)
    self.requests_scrollbar.pack(side='right', fill='y')
    self.requests_tree.pack(side='left', fill='both', expand=True)

    self.load_requests_table()


def delete_request_window(self):
    self.dlt = tk.Toplevel(self.root)
    self.dlt.title("Удаление запроса на перемещение")
    self.dlt.geometry("750x350")
    self.dlt.transient(self.root)
    self.dlt.grab_set()

    self.requests_table_label = tk.Label(self.dlt, text="Активные запросы:", bg="white")
    self.requests_table_label.place(rely=0.05, relx=0.05)

    self.requests_tree_frame = tk.Frame(self.dlt)
    self.requests_tree_frame.place(rely=0.12, relx=0.05, width=650, height=250)

    requests_column_names = ["Номер запроса", "Кол-во техники", "ID техники"]

    self.requests_tree = ttk.Treeview(self.requests_tree_frame, columns=requests_column_names, show='headings')
    for col in requests_column_names:
        self.requests_tree.heading(col, text=col)
        self.requests_tree.column(col, width=150, anchor='center')

    self.requests_scrollbar = ttk.Scrollbar(self.requests_tree_frame, orient="vertical", command=self.requests_tree.yview)
    self.requests_tree.configure(yscrollcommand=self.requests_scrollbar.set)
    self.requests_scrollbar.pack(side='right', fill='y')
    self.requests_tree.pack(side='left', fill='both', expand=True)

    self.load_requests_table()

    self.request_ID_label = tk.Label(self.dlt, text="Номер запроса:", bg="white")
    self.request_ID_label.place(rely=0.87, relx=0.05)

    self.request_ID_entry = tk.Entry(self.dlt)
    self.request_ID_entry.place(rely=0.87, relx=0.175, width=240)

    self.confirm_delete_button = tk.Button(self.dlt, text="Подтвердить\nудаление запроса", command=self.delete_request)
    self.confirm_delete_button.place(rely=0.85, relx=0.6)
