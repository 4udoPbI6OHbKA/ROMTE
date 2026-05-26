from tkinter import messagebox
import sqlite3

def delete_request(self):
    request_id_str = self.request_ID_entry.get()

    if not request_id_str:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер запроса.")
        return

    try:
        request_id = int(request_id_str)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Номер запроса должен быть числом.")
        return

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT \"Кол-во техники\", \"ID техники\" FROM {self.REQUESTS_TABLE_NAME} WHERE \"Номер запроса\" = ?", (request_id,))
        request_data = cursor.fetchone()

        if request_data is None:
            messagebox.showerror("Ошибка", f"Запрос с номером {request_id} не найден.")
            return

        requested_tech_count, original_id_string = request_data

        equipment_ids_to_execute = self.decoding_id_string(original_id_string)
        if equipment_ids_to_execute is None:
            messagebox.showerror("Ошибка", "Не удалось разобрать ID техники из запроса.")
            return

        update_datetime_str = self.get_current_datetime_str()
        updated_count = 0

        for eq_id in equipment_ids_to_execute:
            cursor.execute(f"SELECT \"Текущее местоположение\", Статус FROM {self.TABLE_NAME} WHERE ID = ?", (eq_id,))
            tech_data = cursor.fetchone()

            if tech_data is None:
                messagebox.showwarning("Предупреждение", f"Оборудование с ID {eq_id} не найдено в техническом реестре. Пропуск.")
                continue

            current_location, current_status = tech_data
            new_status = "На месте"

            cursor.execute(f"""
                UPDATE {self.TABLE_NAME}
                SET "Требуемое местоположение" = ?, Статус = ?, "Последнее обновление статуса" = ?
                WHERE ID = ?
            """, (current_location, new_status, update_datetime_str, eq_id))
                
            updated_count += 1

        conn.commit()

        cursor.execute(f"DELETE FROM {self.REQUESTS_TABLE_NAME} WHERE \"Номер запроса\" = ?", (request_id,))
        conn.commit()

        messagebox.showinfo("Успех", f"Запрос №{request_id} удален. Обновлена информация для {updated_count} единиц техники.")
            
        self.load_technical_table()
        self.load_requests_table()
        self.dlt.destroy()

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при удалении запроса: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка при удалении запроса: {e}")
    finally:
        if conn:
            conn.close()


def execute_request(self):
    request_id_str = self.request_ID_entry.get()

    if not request_id_str:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер запроса.")
        return

    try:
        request_id = int(request_id_str)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Номер запроса должен быть числом.")
        return

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT \"Кол-во техники\", \"ID техники\" FROM {self.REQUESTS_TABLE_NAME} WHERE \"Номер запроса\" = ?", (request_id,))
        request_data = cursor.fetchone()

        if request_data is None:
            messagebox.showerror("Ошибка", f"Запрос с номером {request_id} не найден.")
            return

        requested_tech_count, original_id_string = request_data

        equipment_ids_to_execute = self.decoding_id_string(original_id_string)
        if equipment_ids_to_execute is None:
            messagebox.showerror("Ошибка", "Не удалось разобрать ID техники из запроса.")
            return

        update_datetime_str = self.get_current_datetime_str()
        updated_count = 0

        for eq_id in equipment_ids_to_execute:
            cursor.execute(f"SELECT \"Требуемое местоположение\" FROM {self.TABLE_NAME} WHERE ID = ?", (eq_id,))
            required_location_data = cursor.fetchone()

            if required_location_data is None:
                messagebox.showwarning("Предупреждение", f"Оборудование с ID {eq_id} не найдено в техническом реестре. Пропуск.")
                continue

            required_location = required_location_data[0]
            new_status = "На месте"

            cursor.execute(f"""
                UPDATE {self.TABLE_NAME}
                SET "Текущее местоположение" = ?, Статус = ?, "Последнее обновление статуса" = ?
                WHERE ID = ?
            """, (required_location, new_status, update_datetime_str, eq_id))
                
            updated_count += 1

        conn.commit()

        cursor.execute(f"DELETE FROM {self.REQUESTS_TABLE_NAME} WHERE \"Номер запроса\" = ?", (request_id,))
        conn.commit()

        messagebox.showinfo("Успех", f"Запрос №{request_id} выполнен. Обновлена информация для {updated_count} единиц техники.")
            
        self.load_technical_table()
        self.load_requests_table()
        self.conf.destroy()

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при выполнении запроса: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка при выполнении запроса: {e}")
    finally:
        if conn:
            conn.close()
