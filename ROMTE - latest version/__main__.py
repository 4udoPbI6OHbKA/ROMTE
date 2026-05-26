import tkinter as tk

from load_tables import load_technical_table, load_requests_table
from windows import request_window, confirm_request_window, show_requests_table, delete_request_window
from removing_requests_functions import delete_request, execute_request
from technical_functions import update_rooms, decoding_id_string, get_current_datetime_str
from adding_requests_functions import create_new_request_entry, process_movement_request

class RegisterOfMovemenTechnicalEquipmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ROMTE")
        self.root.geometry("1500x900")
        self.root.resizable(False, False)

        self.top_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.top_frame.place(relwidth=1, relheight=0.1)
        self.top_frame.columnconfigure(1, weight=1)

        self.title_label = tk.Label(self.root, text="ROMTE\nРеестр перемещения технического оборудования",font="size=40", bg="white")
        self.title_label.pack(pady=2, ipadx=60, ipady=20)

        self.bottom_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.bottom_frame.place(rely=0.9, relwidth=1, relheight=0.1)
        self.bottom_frame.columnconfigure(1, weight=1)

        self.table_frame = tk.Frame(self.root, bg="#f0f0f0", highlightbackground="black", highlightthickness=1)
        self.table_frame.place(rely=0.1, relwidth=1, relheight=0.8)

        self.tree = None
        self.sсrollbar = None

        self.DB_NAME = "SchoolTechnicalEquipment.db"
        self.TABLE_NAME = "технический_реестр"
        self.REQUESTS_TABLE_NAME = "Запросы"
        self.load_technical_table()
        

        self.request_button = tk.Button(text="Запрос на\nперемещение", command=self.request_window)
        self.request_button.place(relx=0.065, rely=0.93, width=100, height=40)

        self.confirm_request_button = tk.Button(text="Выполнение\nзапроса", command=self.confirm_request_window)
        self.confirm_request_button.place(relx=0.265, rely=0.93, width=100, height=40)

        self.show_requests_button = tk.Button(text="Просмотр\nзапросов", command=self.show_requests_table)
        self.show_requests_button.place(relx=0.465, rely=0.93, width=100, height=40)
        
        self.delete_request_button = tk.Button(text="Удаление\nзапроса", command=self.delete_request_window)
        self.delete_request_button.place(relx=0.665, rely=0.93, width=100, height=40)

        self.exit_button = tk.Button(text="Выход", command=self.root.destroy)
        self.exit_button.place(relx=0.865, rely=0.93, width=100, height=40)

        
        self.requests_tree = None
        self.requests_scrollbar = None


        
    def request_window(self):
        return request_window(self)

    def confirm_request_window(self):
        return confirm_request_window(self)

    def show_requests_table(self):
        return show_requests_table(self)

    def delete_request_window(self):
        return delete_request_window(self)



    def load_technical_table(self):
        return load_technical_table(self)

    def load_requests_table(self):
        return load_requests_table(self)



    def update_rooms(self, event=None):
        return update_rooms(self)

    def decoding_id_string(self, id_string):
        return decoding_id_string(id_string)

    def get_current_datetime_str(self):
        return get_current_datetime_str(self)



    def create_new_request_entry(self, conn, cursor, requested_tech_count, original_id_string):
        return create_new_request_entry(self, conn, cursor, requested_tech_count, original_id_string)

    def process_movement_request(self):
        return process_movement_request(self)

        

    def execute_request(self):
        return execute_request(self)

    def delete_request(self):
        return delete_request(self)



if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterOfMovemenTechnicalEquipmentApp(root)
    root.mainloop()
