import tkinter as tk
from tkinter import ttk
import sqlite3
import os

def load_technical_table(self):
    if self.tree:
        for item in self.tree.get_children():
            self.tree.delete(item)

    if not os.path.exists(self.DB_NAME):
        print(f"Ошибка: Файл базы данных '{self.DB_NAME}' не найден.")
        return

    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({self.TABLE_NAME});")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]

        if self.tree is None:
            self.tree = ttk.Treeview(self.table_frame, columns=column_names, show='headings')

            for col in column_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor='center')

            if self.sсrollbar is None:
                self.sсrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
                self.tree.configure(yscrollcommand=self.sсrollbar.set)
                self.sсrollbar.pack(side='right', fill='y')
                self.tree.pack(side='left', fill='both', expand=True)
            else:
                self.tree.pack(side='left', fill='both', expand=True)
        else:
            if not self.tree.winfo_ismapped():
                self.tree.pack(side='left', fill='both', expand=True)
                if self.sсrollbar:
                    self.sсrollbar.pack(side='right', fill='y')

        cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def load_requests_table(self):
    if self.requests_tree:
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)

    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.REQUESTS_TABLE_NAME}';")
        if cursor.fetchone() is None:
            print(f"Таблица '{self.REQUESTS_TABLE_NAME}' не найдена.")
            conn.close()
            return

        cursor.execute(f"PRAGMA table_info({self.REQUESTS_TABLE_NAME});")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]

        if self.requests_tree is None:
            self.requests_tree = ttk.Treeview(self.requests_tree_frame, columns=column_names, show='headings')
            for col in column_names:
                self.requests_tree.heading(col, text=col)
                self.requests_tree.column(col, width=150, anchor='center')
            self.requests_scrollbar = ttk.Scrollbar(self.requests_tree_frame, orient="vertical", command=self.requests_tree.yview)
            self.requests_tree.configure(yscrollcommand=self.requests_scrollbar.set)
            self.requests_scrollbar.pack(side='right', fill='y')
            self.requests_tree.pack(side='left', fill='both', expand=True)
        else:
            pass

        cursor.execute(f"SELECT * FROM {self.REQUESTS_TABLE_NAME}")
        rows = cursor.fetchall()

        for row in rows:
            self.requests_tree.insert("", tk.END, values=row)

        conn.close()

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных (Запросы): {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при загрузке запросов: {e}")

