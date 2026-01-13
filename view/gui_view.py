import tkinter as tk
from tkinter import simpledialog, messagebox

class GuiView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Events")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        self.text = tk.Text(self, height=20, width=90, font=("Consolas", 10))
        self.text.pack(padx=10, pady=10, fill="both", expand=True)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10, fill="x")

        buttons_data = [
            ("Add Event", "add"),
            ("Load Events", "load"),
            ("Analyze", "analyze"),
            ("Register", "register"),
            ("Show List", "show_list"),
            ("Delete Event", "delete")
        ]

        for i in range(0, len(buttons_data), 2):
            row_frame = tk.Frame(button_frame, bg="#f0f0f0")
            row_frame.pack(fill="x", pady=5)

            btn1_text, _ = buttons_data[i]
            btn1 = tk.Button(row_frame, text=btn1_text, width=20, height=2, font=("Arial", 10, "bold"))
            btn1.pack(side="left", padx=10, expand=True, fill="x")

            if i + 1 < len(buttons_data):
                btn2_text, _ = buttons_data[i + 1]
                btn2 = tk.Button(row_frame, text=btn2_text, width=20, height=2, font=("Arial", 10, "bold"))
                btn2.pack(side="right", padx=10, expand=True, fill="x")

        self.buttons = [btn for row in button_frame.winfo_children() for btn in row.winfo_children()]

    def show_message(self, msg):
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def update(self, model):  # Observer
        self.show_message("List updated. Total events: " + str(len(model.events)))