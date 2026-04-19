import tkinter as tk







class RegisterOfMovemenTechnicalEquipmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LibFeath")
        self.root.geometry("1500x900")
        self.root.resizable(False, False)

        self.entry_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.entry_frame.place(relwidth=1, relheight=0.1)
        self.entry_frame.columnconfigure(1, weight=1)

        self.entry_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.entry_frame.place(rely=0.9, relwidth=1, relheight=0.1)
        self.entry_frame.columnconfigure(1, weight=1)

        
if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterOfMovemenTechnicalEquipmentApp(root)
    root.mainloop()
