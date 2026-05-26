from tkinter import messagebox
import sqlite3


def create_new_request_entry(self, conn, cursor, requested_tech_count, original_id_string):
    try:
        cursor.execute(f"SELECT MAX(\"Номер запроса\") FROM {self.REQUESTS_TABLE_NAME}")
        max_request_num = cursor.fetchone()[0]
            
        new_request_num = 1 if max_request_num is None else max_request_num + 1

        cursor.execute(f"""
            INSERT INTO {self.REQUESTS_TABLE_NAME} ("Номер запроса", "Кол-во техники", "ID техники")
            VALUES (?, ?, ?)
        """, (new_request_num, requested_tech_count, original_id_string))
        print(f"Создан новый запрос №{new_request_num} с {requested_tech_count} единицами техники (ID: {original_id_string}).")
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при создании записи в таблице '{self.REQUESTS_TABLE_NAME}': {e}")
        return False
    except Exception as e:
        messagebox.showerror("Ошибка", f"Непредвиденная ошибка при создании запроса: {e}")
        return False

def process_movement_request(self):
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
        
    equipment_ids_parsed = self.decoding_id_string(entered_ids_str)
    if equipment_ids_parsed is None:
        return

    new_location = f"{selected_korpus}, {selected_room}"
    new_status = "Ожидает перемещения"
    update_datetime_str = self.get_current_datetime_str()

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.REQUESTS_TABLE_NAME}';")
        if cursor.fetchone() is None:
            try:
                cursor.execute(f"""
                    CREATE TABLE {self.REQUESTS_TABLE_NAME} (
                        "Номер запроса" INTEGER PRIMARY KEY AUTOINCREMENT,
                        "Кол-во техники" INTEGER,
                        "ID техники" TEXT
                    );
                """)
                conn.commit()
                print(f"Создана таблица '{self.REQUESTS_TABLE_NAME}'.")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось создать таблицу '{self.REQUESTS_TABLE_NAME}': {e}")
                return

        updated_count = 0
        skipped_count = 0
        valid_equipment_ids_for_request = []

        for eq_id in equipment_ids_parsed:
            cursor.execute(f"SELECT COUNT(*), Статус FROM {self.TABLE_NAME} WHERE ID = ?", (eq_id,))
            count_data = cursor.fetchone()
                
            if count_data is None or count_data[0] == 0:
                messagebox.showwarning("Предупреждение", f"Оборудование с ID {eq_id} не найдено в базе данных. Оно будет пропущено.")
                continue

            current_status = count_data[1]

            if current_status == "Ожидает перемещения":
                messagebox.showwarning("Предупреждение", f"Оборудование с ID {eq_id} уже ожидает перемещения и будет пропущено.")
                skipped_count += 1
                continue

            cursor.execute(f"""
                UPDATE {self.TABLE_NAME}
                SET "Требуемое местоположение" = ?, Статус = ?, "Последнее обновление статуса" = ?
                WHERE ID = ?
            """, (new_location, new_status, update_datetime_str, eq_id))
                
            updated_count += 1
            valid_equipment_ids_for_request.append(eq_id)

        conn.commit()

        if updated_count > 0:
            requested_tech_count = len(valid_equipment_ids_for_request)
            if self.create_new_request_entry(conn, cursor, requested_tech_count, entered_ids_str):
                conn.commit()
                message = f"Успешно обновлена информация для {updated_count} единиц техники. Создан новый запрос."
                if skipped_count > 0:
                        message += f"\n{skipped_count} единиц техники было пропущено (статус 'Ожидает перемещения' или не найдены)."
                messagebox.showinfo("Успех", message)
                self.load_technical_table()
                self.win.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать запись о запросе. Обновление техники было выполнено, но запрос не зарегистрирован.")
        else:
            message = "Не удалось обновить ни одну единицу техники."
            if skipped_count > 0:
                message += f" {skipped_count} единиц техники было пропущено (статус 'Ожидает перемещения' или не найдены)."
            messagebox.showwarning("Предупреждение", message)

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")
    finally:
        if conn:
            conn.close()

            
