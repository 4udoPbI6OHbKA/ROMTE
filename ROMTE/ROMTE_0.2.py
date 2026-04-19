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
        self.load_technical_registry()

        self.request_button = tk.Button(text="Запрос на\nперемещение")
        self.request_button.place(relx=0.1, rely=0.93, width=100, height=40)

    def load_technical_registry(self):
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
