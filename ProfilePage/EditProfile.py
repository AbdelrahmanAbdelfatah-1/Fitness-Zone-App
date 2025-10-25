import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class edit_profile_page(tk.Toplevel) :
    def __init__(self, master, user, stack, manager):
        super().__init__(master)
        self.user = user
        self.stack = stack
        self.manager = manager

        self.Dark_Gray = "#111827"
        self.Dark_Blue = "#004477"

        self.title("Edit Profile")
        self.state("zoomed")
        self.configure(bg=self.Dark_Gray)

        # ------- Canvas + Scrollbar -----------
        canvas = tk.Canvas(self, bg=self.Dark_Gray, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg=self.Dark_Gray)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=self.winfo_screenwidth())

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_frame_configure)
        # -----------------------------------------------------------------

        main_frame = tk.Frame(scrollable_frame, bg=self.Dark_Gray, relief="raised", bd=2)
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        #  header
        header_frame = tk.Frame(main_frame, bg=self.Dark_Gray)
        header_frame.pack(fill="x", pady=10)

        back_button = tk.Button(
            header_frame, text="Back", font=("Arial", 15, "bold"),
            fg="white", bg=self.Dark_Gray, relief='flat', cursor='hand2',
            activebackground="white", command=self.stack.pop
        )
        back_button.pack(side="left", padx=20)

        title_label = tk.Label(
            header_frame,
            text="Edit Profile",
            bg=self.Dark_Gray,
            fg="white",
            font=("Helvetica", 26, "bold")
        )
        title_label.pack(padx=20)

        # Form
        form_frame = tk.Frame(main_frame, bg=self.Dark_Gray)
        form_frame.pack(fill="both", expand=True, pady=20)

        labels = ["Name", "Age", "Height (Cm)", "Weight (Kg)"]
        self.entries = {}

        for i, label in enumerate(labels, start=0):
            tk.Label(
                form_frame,
                text=label,
                bg=self.Dark_Gray,
                fg="white",
                font=("Helvetica", 18, "bold")
            ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

            entry = tk.Entry(form_frame, font=("Helvetica", 14), bg=self.Dark_Blue, fg="white", insertbackground="white")
            key = label.split()[0].lower()

            value = self.user.get(key) or self.user.get(key.capitalize())
            if value is not None:
                entry.insert(0, str(value))
            self.entries[key] = entry
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew", ipady=5)

        form_frame.grid_columnconfigure(1, weight=1)

        # Password
        tk.Label(form_frame, text="Password", bg=self.Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(
            row=4, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 14), bg=self.Dark_Blue, fg="white",
                                       insertbackground="white")
        self.password_entry.insert(0, self.user.get("password", ""))
        self.password_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew", ipady=5)

        # Gender
        gender_options = ["Male", "Female"]
        self.gender_var = tk.StringVar(self)
        self.gender_var.set(self.user.get("gender", "Male"))

        tk.Label(form_frame, text="Gender", bg=self.Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(
            row=5, column=0, padx=10, pady=10, sticky="w")

        gender_menu = tk.OptionMenu(form_frame, self.gender_var, *gender_options)
        gender_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white",
                           relief="flat", activebackground="#1ABC9C", activeforeground="white")
        gender_menu.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Goal
        goal_options = ["Lose Weight", "Maintain Weight", "Gain Weight"]
        self.goal_var = tk.StringVar(self)
        self.goal_var.set(self.user.get("goal", goal_options[0]))

        tk.Label(form_frame, text="Goal", bg=self.Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(
            row=6, column=0, padx=10, pady=10, sticky="w")

        goal_menu = tk.OptionMenu(form_frame, self.goal_var, *goal_options)
        goal_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white",
                         relief="flat", activebackground="#1ABC9C", activeforeground="white")
        goal_menu.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        # Activity
        activity_options = ["Active", "Moderately Active", "Inactive"]
        self.activity_var = tk.StringVar(self)
        self.activity_var.set(self.user.get("activity", activity_options[0]))

        tk.Label(form_frame, text="Activity Level", bg=self.Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(
            row=7, column=0, padx=10, pady=10, sticky="w")

        activity_menu = tk.OptionMenu(form_frame, self.activity_var, *activity_options)
        activity_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white",
                             relief="flat", activebackground="#1ABC9C", activeforeground="white")
        activity_menu.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        # Weekly Change
        weekly_change_options = [0.25, 0.5, 1, 1.25, 1.5, 2]
        self.weekly_change_var = tk.StringVar(self)
        self.weekly_change_var.set(str(self.user.get("weekly_change", weekly_change_options[0])))

        tk.Label(form_frame, text="Weekly Change (kg)", bg=self.Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(
            row=8, column=0, padx=10, pady=10, sticky="w")

        weekly_change_menu = tk.OptionMenu(form_frame, self.weekly_change_var, *weekly_change_options)
        weekly_change_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white",
                                  relief="flat", activebackground="#1ABC9C", activeforeground="white")
        weekly_change_menu.grid(row=8, column=1, padx=10, pady=10, sticky="ew")

        # Save Button
        save_btn = tk.Button(
            form_frame,
            text="Save Changes",
            command=self.save_changes,
            bg="#1ABC9C",
            fg="white",
            font=("Helvetica", 14, "bold"),
            relief="flat",
            bd=0,
            width=20,
            activebackground="#16A085",
            activeforeground="white"
        )
        save_btn.grid(row=9, column=0, columnspan=2, pady=40)

    def save_changes(self) :

        self.user["name"] = self.entries["name"].get()
        self.user["age"] = int(self.entries["age"].get())
        self.user["height"] = float(self.entries["height"].get())
        self.user["weight"] = float(self.entries["weight"].get())
        self.user["password"] = self.password_entry.get()
        self.user["gender"] = self.gender_var.get()
        self.user["goal"] = self.goal_var.get()
        self.user["activity"] = self.activity_var.get()
        self.user["weekly_change"] = float(self.weekly_change_var.get())

        self.manager.update_user(self.user["email"], self.user)

        logs = self.manager.load_file(self.manager.logs_file)

        today_date = self.manager.get_today_date()
        today_str = str(today_date)
        self.manager.ensure_log_for_date(self.user["email"], today_str)

        daily_cal_today = self.manager.calculate_daily_calories(
            self.user["goal"], self.user["weekly_change"],
            self.user["weight"], self.user["height"],
            self.user["age"], self.user["gender"], self.user["activity"]
        )
        logs[self.user["email"]][today_str]["daily_calories"] = daily_cal_today

        for date_str in logs.get(self.user["email"], {}):
            log_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if log_date > today_date:
                logs[self.user["email"]][date_str]["daily_calories"] = self.manager.calculate_daily_calories(
                    self.user["goal"], self.user["weekly_change"],
                    self.user["weight"], self.user["height"],
                    self.user["age"], self.user["gender"], self.user["activity"]
                )

        self.manager.save_file(self.manager.logs_file, logs)

        messagebox.showinfo("Success", "Profile updated successfully!")

        diary_page = self.stack.items[0]
        diary_page.refresh()

        from ProfilePage.Profile import profile_page
        self.stack.pop()
        profile_page(self.master, self.user, self.stack, self.manager)

