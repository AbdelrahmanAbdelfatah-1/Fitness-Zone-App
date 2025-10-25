import tkinter as tk
from Admin.utils import Stack
from Admin.food import FoodFrame
from Admin.exercise import ExerciseFrame

class AdminPanel :

    def __init__(self) :
        self.root = tk.Tk()

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.root.state("zoomed")
        self.root.configure(bg = self.Dark_Gray)
        self.root.title("Admin Panel")
        self.stack = Stack()


        self.main = tk.Frame(self.root,relief = 'raised' , bd =2 , bg = self.Dark_Gray )
        self.main.pack(padx = 40 , pady = 40 ,fill = 'both', expand = True)

        self.header = tk.Frame(self.main, bg = self.Dark_Gray )
        self.header.pack(padx = 30, pady = 30 ,fill = 'x')

        logout_btn = tk.Button(self.header,text="Log out",fg ="white",
                               bg='red',font=('arial',16,'bold'),command=self.logout)
        logout_btn.pack(side = 'left' , fill = 'x' , padx = 5, pady = 5)

        self.main_frame = tk.Frame(self.main, bg="#111827")
        self.main_frame.pack(fill="both", expand=True)
        self.stack.push(self.main_frame)

        tk.Label(
            self.main_frame,
            text="Admin Panel",
            font=("Arial", 28, "bold"),
            bg="#111827",
            fg="white"
        ).pack(pady=5, fill="x")

        button_frame = tk.Frame(self.main_frame, bg="#111827")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(
            button_frame,
            text="Foods",
            font=("Arial", 24, "bold"),
            width=15,
            height=6,
            bg="#004477",
            fg="white",
            command=self.open_food
        ).pack(side="left", padx=70 )
        tk.Button(
            button_frame,
            text="Exercises",
            font=("Arial", 24, "bold"),
            width=15,
            height=6,
            bg="#004477",
            fg="white",
            command=self.open_exercise
        ).pack(side="left", padx=50)

    def open_food(self) :
        self.main_frame.pack_forget()
        frame = FoodFrame(self.main, self.stack)
        frame.pack(fill="both", expand=True)
        self.stack.push(frame)

    def open_exercise(self) :
        self.main_frame.pack_forget()
        frame = ExerciseFrame(self.main, self.stack)
        frame.pack(fill="both", expand=True)
        self.stack.push(frame)

    def run(self) :
        self.root.mainloop()

    def logout(self) :
        self.root.destroy()
        from LoginPage import login_page
        l = login_page()
        l.mainloop()


