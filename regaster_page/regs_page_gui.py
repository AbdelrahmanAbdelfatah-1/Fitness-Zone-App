import tkinter as tk
from tkinter import messagebox
from regaster_page.register_class import User
from regaster_page.storage import save_users , load_users , create_user_log
import re

def reg() :
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def regs_user():
        name = entry_name.get()
        mail = entry_mail.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        age = entry_age.get()
        height = entry_height.get()
        weight = entry_weight.get()
        gender = gender_var.get()
        goal = goal_var.get()
        activity = activity_var.get()
        weekly_change = weekly_change_var.get()

        if goal == "Select your goal":
            goal = None
        if activity == "Select your activity level":
            activity = None
        if weekly_change == "Select weekly change":
            weekly_change = None

        if not all([name, mail, password, confirm_password, age, gender, height, weight]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        if not is_valid_email(mail):
            messagebox.showerror("Error", "Invalid email format")
            return

        users = load_users()
        if any(u.email == mail for u in users):
            messagebox.showerror("Error", "Email already exists")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        new_user = User(
            name,
            mail,
            password,
            age,
            gender,
            height,
            weight,
            goal,
            activity,
            float(weekly_change) if weekly_change else 0
        )
        users.append(new_user)
        save_users(users)
        new_user_dic = new_user.to_dict()
        create_user_log(new_user_dic)
        messagebox.showinfo("Success", f"User {name} registered successfully!")

        entry_name.delete(0, tk.END)
        entry_mail.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_confirm_password.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_height.delete(0, tk.END)
        entry_weight.delete(0, tk.END)
        gender_var.set(gender_options[0])
        goal_var.set(goal_options[0])
        activity_var.set(activity_options[0])
        weekly_change_var.set(weekly_change_options[0])
        back_to_login()

    def back_to_login() :
        root.destroy()
        from LoginPage import login_page
        l = login_page()
        l.mainloop()


    Dark_Gray = "#111827"
    Dark_Blue = "#004477"

    root = tk.Tk()
    root.title("Fitness App")
    root.state("zoomed")
    root.configure(bg=Dark_Gray)

    # ------- Canvas + Scrollbar -----------
    canvas = tk.Canvas(root, bg=Dark_Gray, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg=Dark_Gray)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=root.winfo_screenwidth())

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    #-----------------------------------------------------------------

    main_frame = tk.Frame(scrollable_frame, bg=Dark_Gray, relief='raised', bd=2)
    main_frame.pack(expand=True, fill="both", padx=50, pady=50)

    # Back
    back_btn = tk.Button(
        main_frame,
        text="← Back",
        command=lambda: back_to_login(),
        bg= Dark_Gray ,
        fg="white",
        font=("Helvetica", 15, "bold"),
        relief="flat",
        activebackground = Dark_Blue ,
        activeforeground="white" ,
        cursor="hand2"
    )
    back_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Title
    title_label = tk.Label(
        main_frame,
        text="Register",
        bg=Dark_Gray,
        fg="white",
        font=("Helvetica", 26, "bold")
    )
    title_label.grid(row=0, column=1, columnspan=2, pady=20, sticky="n" )

    labels = ["Name", "Email", "Password", "Confirm Password", "Age", "Height (Cm) ", "Weight (Kg)"]
    entries = []

    for i, label in enumerate(labels,start=1) :
        tk.Label(
            main_frame,
            text=label,
            bg=Dark_Gray,
            fg="white",
            font=("Helvetica", 18, "bold")
        ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(main_frame, font=("Helvetica", 14) , bg=Dark_Blue , fg="white" , insertbackground="white")
        if "Password" in label:
            entry.config(show="*")
        entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew", ipady=5)
        entries.append(entry)

    main_frame.grid_columnconfigure(1, weight=1)

    entry_name, entry_mail, entry_password, entry_confirm_password, entry_age, entry_height, entry_weight = entries

    gender_options = ["Select Gender", "Male", "Female"]
    gender_var = tk.StringVar(root)
    gender_var.set(gender_options[0])

    tk.Label(main_frame, text="Gender", bg=Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(
        row=8, column=0, padx=10, pady=10, sticky="w")

    gender_menu = tk.OptionMenu(main_frame, gender_var, *gender_options)
    gender_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white",
                       relief="flat", activebackground="#1ABC9C", activeforeground="white")
    gender_menu.grid(row=8, column=1, padx=10, pady=10, sticky="ew")


    goal_options = ["Select your goal", "Lose Weight", "Maintain Weight", "Gain Weight"]
    goal_var = tk.StringVar(root)
    goal_var.set(goal_options[0])
    tk.Label(main_frame, text="Your Goal", bg=Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(row=9, column=0, padx=10, pady=10, sticky="w")
    goal_menu = tk.OptionMenu(main_frame, goal_var, *goal_options)
    goal_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white", relief="flat", activebackground="#1ABC9C", activeforeground="white")
    goal_menu.grid(row=9, column=1, padx=10, pady=10, sticky="ew")

    activity_options = ["Select your activity level", "Active", "Moderately Active", "Inactive"]
    activity_var = tk.StringVar(root)
    activity_var.set(activity_options[0])
    tk.Label(main_frame, text="Activity Level", bg=Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(row=10, column=0, padx=10, pady=10, sticky="w")
    activity_menu = tk.OptionMenu(main_frame, activity_var, *activity_options)
    activity_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white", relief="flat", activebackground="#1ABC9C", activeforeground="white")
    activity_menu.grid(row=10, column=1, padx=10, pady=10, sticky="ew")


    weekly_change_options = ["Select weekly change", 0.25, 0.5, 1, 1.25, 1.5, 2, 2.25, 2.5]
    weekly_change_var = tk.StringVar(root)
    weekly_change_var.set(weekly_change_options[0])
    tk.Label(main_frame, text="Weekly Change (kg)", bg=Dark_Gray, fg="white", font=("Helvetica", 18, "bold")).grid(row=11, column=0, padx=10, pady=10, sticky="w")
    weekly_change_menu = tk.OptionMenu(main_frame, weekly_change_var, *weekly_change_options)
    weekly_change_menu.config(width=28, font=("Helvetica", 12), bg="#34495E", fg="white", relief="flat", activebackground="#1ABC9C", activeforeground="white")
    weekly_change_menu.grid(row=11, column=1, padx=10, pady=10, sticky="ew")

    register_btn = tk.Button(
        main_frame,
        text="Register",
        command=regs_user,
        bg="#1ABC9C",
        fg="white",
        font=("Helvetica", 14, "bold"),
        relief="flat",
        bd=0,
        width=20,
        activebackground="#16A085",
        activeforeground="white"
    )
    register_btn.grid(row=12, column=0, columnspan=2, pady=40)
    root.mainloop()

