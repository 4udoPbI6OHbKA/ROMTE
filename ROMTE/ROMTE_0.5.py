import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

        self.DB_NAME = "SchoolTechnicalEquipment.db"
        self.TABLE_NAME = "технический_реестр"

    def request_window(self):
        self.win = tk.Toplevel(root)
        self.win.title("Запрос на перемещение")
        self.win.geometry("750x350")
        self.win.transient(self.root)
        self.win.grab_set()

        self.info_label_0 = tk.Label(self.win, text="Выбор технического оборудования(по ID)", bg="white")
        self.info_label_0.place(rely=0.05, relx=0.05, width=331)

        self.info_label_1 = tk.Label(self.win, text="1 - одно оборудование\n1:10 - множество\n 1:3, 6:10, 12 - несколько множеств и единиц оборудования", justify="left", bg="white")
        self.info_label_1.place(rely=0.15, relx=0.05)

        self.info_label_2 = tk.Label(self.win, text="Перенос в:", bg="white")
        self.info_label_2.place(rely=0.29, relx=0.5, width=278)

        self.ID_label = tk.Label(self.win, text="Оборудование:", bg="white")
        self.ID_label.place(rely=0.45, relx=0.05)

        self.ID_entry = tk.Entry(self.win)
        self.ID_entry.place(rely=0.45, relx=0.17, width=240)

        self.korpus_label = tk.Label(self.win, text="Корпус:", bg="white")
        self.korpus_label.place(rely=0.55, relx=0.5)

        self.available_korpus = ["Корпус 1", "Корпус 2", "Корпус 3"]
        self.korpus_combobox = ttk.Combobox(self.win, values=self.available_korpus, state="readonly")
        self.korpus_combobox.place(rely=0.55, relx=0.565, width=228)
        self.korpus_combobox.bind("<<ComboboxSelected>>", self.update_rooms)

        self.room_label = tk.Label(self.win, text="Помещение:", bg="white")
        self.room_label.place(rely=0.65, relx=0.5)

        self.room_combobox = ttk.Combobox(self.win, state="readonly")
        self.room_combobox.place(rely=0.65, relx=0.603, width=200)

        self.confirm_button = tk.Button(self.win, text="Подтвердить", command=self.process_movement_request)
        self.confirm_button.place(rely=0.85, relx=0.44)

        self.update_rooms()

    def update_rooms(self, event=None):
        """
        Обновляет список помещений в зависимости от выбранного корпуса.
        """
        selected_korpus = self.korpus_combobox.get()

        rooms_data = {
            "Корпус 1": ["Каб. 1", "Каб. 2", "Каб. 3"],
            "Корпус 2": ["Каб. 101", "Каб. 103", "Каб. 104"],
            "Корпус 3": ["Каб. 201", "Каб. 205", "Каб. 207"]
        }

        if selected_korpus and selected_korpus in rooms_data:
            available_rooms = rooms_data[selected_korpus]
        else:
            available_rooms = []

        self.room_combobox.config(values=available_rooms)
        self.room_combobox.set("")
        self.room_combobox.config(state="readonly" if available_rooms else "disabled")

    def parse_id_string(self, id_string):
        """
        Парсит строку с ID техники и возвращает список уникальных ID.
        Поддерживает форматы: "1", "1:10", "1:3, 6:10, 12".
        """
        unique_ids = set()
        if not id_string:
            return list(unique_ids)

        try:
            parts = id_string.split(',')
            for part in parts:
                part = part.strip()
                if ":" in part:
                    start_str, end_str = part.split(':')
                    start_id = int(start_str.strip())
                    end_id = int(end_str.strip())
                    for i in range(start_id, end_id + 1):
                        unique_ids.add(i)
                else:
                    unique_ids.add(int(part))
        except ValueError:
            messagebox.showerror("Ошибка ввода", f"Неверный формат ID: {id_string}. Пожалуйста, введите ID в правильном формате.")
            return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при парсинге ID: {e}")
            return None
        return sorted(list(unique_ids))

    def process_movement_request(self):
        """
        Обрабатывает запрос на перемещение: парсит ID, формирует новое местоположение,
        обновляет базу данных и перезагружает таблицу.
        """
        entered_ids_str = self.ID_entry.get()
        selected_korpus = self.korpus_combobox.get()
        selected_room = self.room_combobox.get()

        if not entered_ids_str:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите ID техники.")
            return
        if not selected_korpus:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите корпус.")
            return
        if not selected_room:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите помещение.")
            return

        equipment_ids = self.parse_id_string(entered_ids_str)
        if equipment_ids is None:
            return

        new_location = f"{selected_korpus}, {selected_room}"
        new_status = "Ожидает перемещения"

        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()

            updated_count = 0
            for eq_id in equipment_ids:
                cursor.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE ID = ?", (eq_id,))
                if cursor.fetchone()[0] == 0:
                    messagebox.showwarning("Предупреждение", f"Оборудование с ID {eq_id} не найдено в базе данных. Оно будет пропущено.")
                    continue

                cursor.execute(f"""
                    UPDATE {self.TABLE_NAME}
                    SET "Требуемое местоположение" = ?, Статус = ?
                    WHERE ID = ?
                """, (new_location, new_status, eq_id))
                updated_count += 1

            conn.commit()

            if updated_count > 0:
                messagebox.showinfo("Успех", f"Успешно обновлена информация для {updated_count} единиц техники.")
                self.load_technical_table()
                self.win.destroy()
            else:
                messagebox.showwarning("Предупреждение", "Не удалось обновить ни одну единицу техники. Возможно, введенные ID не существуют.")


        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Ошибка при обновлении базы данных: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")

    def load_technical_table(self):
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
            
            if not hasattr(self, 'tree'):
                self.tree = ttk.Treeview(self.table_frame, columns=column_names, show='headings')

                for col in column_names:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor='center')

                if not hasattr(self, 'sсrollbar'):
                    self.sсrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
                    self.tree.configure(yscrollcommand=self.sсrollbar.set)
                    self.sсrollbar.pack(side='right', fill='y')
                    self.tree.pack(side='left', fill='both', expand=True)
                else:
                    self.tree.pack(side='left', fill='both', expand=True)


            cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", tk.END, values=row)

            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterOfMovemenTechnicalEquipmentApp(root)
    root.mainloop()
