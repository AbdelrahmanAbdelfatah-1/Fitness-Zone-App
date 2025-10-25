import json
import tkinter as tk
from tkinter import messagebox
import time


class login_page(tk.Tk) :
    def __init__(self) :
        super().__init__()
        try :
            with open("Users.json", "r") as file:
                self.users = json.load(file)
        except :
            self.users = []

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.title( "Login - FitnessPal" )
        self.state( "zoomed" )
        self.configure( bg = self.Dark_Gray )

        self.create_widgets()

    def create_widgets(self) :
        # main_frame
        main_frame = tk.Frame(self, bg = self.Dark_Gray , relief='raised', bd=2)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        tk.Label(main_frame, text="Welcome Back", font=("Arial", 28, "bold"), fg = "white" , bg = self.Dark_Gray).pack(pady=10)

        tk.Label(main_frame, text="Sign in to your account", font=("Arial", 15), fg = "white" ,background = self.Dark_Gray).pack(pady=3)

        tk.Label(main_frame, text="Email Address", font=("Arial", 18, "bold"), anchor='w', fg = "white" ,bg=self.Dark_Gray).pack(fill='x', padx=40, pady=20)

        self.user_email = tk.Entry(main_frame, font=("Arial", 15), width=30,
                                   bg = self.Charcoal_Gray , fg = "white" , insertbackground="white")
        self.user_email.pack(fill='x', padx=40, ipady=5)

        tk.Label(main_frame, text="Password", font=("Arial", 18, "bold"),
                 anchor='w', bg=self.Dark_Gray,fg="white").pack(fill='x', padx=40, pady=20)

        self.user_password = tk.Entry(main_frame, font=("Arial", 15), show="*", width=30,
                                      background=self.Charcoal_Gray ,fg = "white" , insertbackground="white")

        self.user_password.pack(fill='x', padx=40, ipady=5)

        tk.Button(main_frame, text='Sign In', font=("Arial", 15, "bold"), fg="white", width=15,
                  command=self.check_login, bg = self.Dark_Blue ).pack(pady=50, ipady=3)

        tk.Label(main_frame, text="Don't have an account ?",
                 font=("Arial", 15), bg=self.Dark_Gray,fg = "white").pack()

        tk.Button(main_frame, text='Create Account', font=("Arial", 15 , "bold"), fg="blue" , bg=self.Dark_Gray,
                  relief='flat', bd=0, activeforeground = "white", activebackground = self.Dark_Gray,
                  command=self.open_reg).pack()

    def check_login(self) :
        email = self.user_email.get().strip()
        password = self.user_password.get().strip()

        if not email or not password :
            messagebox.showwarning("Error", "Please enter both email and password")
            return

        user_found = None
        for user in self.users :
            if user["email"] == email :
                user_found = user
                break

        if not user_found:
            messagebox.showerror("Error", "Invalid email or password\nPlease try again.")
            return

        if not user_found.get("Account_status") :
            messagebox.showerror("Account Locked", "Your account has been closed please call the customer services.")
            return

        lock_time = user_found.get("Lock_time")
        if lock_time:
            remaining_time = time.time() - lock_time
            if remaining_time < 35:
                messagebox.showwarning("Locked", f"Your account is locked. Try again after {int(35 - remaining_time)} seconds.")
                self.user_email.delete(0, 'end')
                self.user_password.delete(0, 'end')
                return
            else :
                user_found["Lock_time"] = None
                user_found["Temp_failed_tries"] = 0

        if user_found["password"] == password :
            if email == "admin@gmail.com" and password == "admin123" :
                messagebox.showinfo("Admin Login", "Welcome Admin")
                user_found["Temp_failed_tries"] = 0
                user_found["perm_failed_tries"] = 0

                self.destroy()
                from Admin.DesignAdmin import AdminPanel
                d = AdminPanel()
                d.run()

            else :

                messagebox.showinfo("Login Successful", f"Welcome {user_found['name']}")
                user_found["Temp_failed_tries"] = 0
                user_found["perm_failed_tries"] = 0

                with open("Users.json", "w") as f :
                    json.dump(self.users, f, indent=4)

                from DairyPages.Diary import diary
                from Stack import Stack
                from FitnessManeger import Manager
                s = Stack()
                m = Manager()
                self.destroy()
                d = diary(user = user_found , stack = s , manager = m)
                s.push(d)
                d.mainloop()

        else :
            messagebox.showerror("Error", "Wrong password")
            self.user_email.delete(0, 'end')
            self.user_password.delete(0, 'end')

            user_found["Temp_failed_tries"] = user_found.get("Temp_failed_tries") + 1
            user_found["perm_failed_tries"] = user_found.get("perm_failed_tries") + 1

            if user_found["Temp_failed_tries"] >= 3:
                user_found["Lock_time"] = time.time()

            if user_found["perm_failed_tries"] >= 10:
                user_found["Account_status"] = False
                messagebox.showerror("Account Closed","Your account has been permanently locked due to too many failed attempts.")

            with open("Users.json", "w") as f :
                json.dump(self.users, f, indent=4)

    def open_reg(self) :
        self.destroy()
        from regaster_page import regs_page_gui
        regs_page_gui.reg()


