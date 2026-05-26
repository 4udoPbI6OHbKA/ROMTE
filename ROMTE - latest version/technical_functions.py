from tkinter import messagebox
from datetime import datetime

def update_rooms(self, event=None):
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

def decoding_id_string(id_string):
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
        messagebox.showerror("Ошибка", f"Произошла ошибка при получении ID: {e}")
        return None
    return sorted(list(unique_ids))

def get_current_datetime_str(self):
    now = datetime.now()
    return now.strftime("%d.%m.%Y, %H:%M")
