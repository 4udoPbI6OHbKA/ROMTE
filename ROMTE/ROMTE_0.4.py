import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class RegisterOfMovemenTechnicalEquipmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ROMTE")
        self.root.geometry("1500x900")
        self.root.resizable(False, False)

        self.top_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.top_frame.place(relwidth=1, relheight=0.1)
        self.top_frame.columnconfigure(1, weight=1)

        self.bottom_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.bottom_frame.place(rely=0.9, relwidth=1, relheight=0.1)
        self.bottom_frame.columnconfigure(1, weight=1)

        self.table_frame = tk.Frame(self.root, bg="#f0f0f0", highlightbackground="black", highlightthickness=1)
        self.table_frame.place(rely=0.1, relwidth=1, relheight=0.8)
        self.load_technical_table()

        self.request_button = tk.Button(text="Запрос на\nперемещение", command=self.request_window)
        self.request_button.place(relx=0.1, rely=0.93, width=100, height=40)

    def request_window(self):
        self.win = tk.Toplevel(root)
        self.win.title("Запрос на перемещение")
        self.win.geometry("750x250")

        self.info_label_0 = tk.Label(self.win, text="Выбор технического оборудования(по ID)", bg="white")
        self.info_label_0.place(rely=0.17, relx=0.05, width=331)

        self.info_label_1 = tk.Label(self.win, text="1 - одно оборудование\n1:10 - множество\n 1:5, 8:10, 12 - несколько множеств и единиц оборудования", justify="left", bg="white")
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

        self.confirm_button = tk.Button(self.win, text="Подтвердить")
        self.confirm_button.place(rely=0.7, relx=0.44)

        self.update_rooms()

    def update_rooms(self, event=None):
        selected_korpus = self.korpus_combobox.get()

        rooms_data = {
            "Корпус 1": ["Каб. 112", "Каб. 212", "Каб. 312"],
            "Корпус 2": ["Каб. 11", "Каб. 13", "Каб. 104"],
            "Корпус 3": ["Каб. 201", "Каб. 205", "Каб. 207"]
        }

        if selected_korpus and selected_korpus in rooms_data:
            available_rooms = rooms_data[selected_korpus]
        else:
            available_rooms = []

        self.room_combobox.config(values=available_rooms)
        self.room_combobox.set("")
        self.room_combobox.config(state="readonly" if available_rooms else "disabled")

    def load_technical_table(self):
        db_name = "SchoolTechnicalEquipment.db"
        table_name = "технический_реестр"

        if not os.path.exists(db_name):
            print(f"Ошибка: Файл базы данных '{db_name}' не найден.")
            return

        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]

            self.tree = ttk.Treeview(self.table_frame, columns=column_names, show='headings')

            for col in column_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor='center')

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", tk.END, values=row)

            sсrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=sсrollbar.set)

            sсrollbar.pack(side='right', fill='y')
            self.tree.pack(side='left', fill='both', expand=True)

            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterOfMovemenTechnicalEquipmentApp(root)
    root.mainloop()
