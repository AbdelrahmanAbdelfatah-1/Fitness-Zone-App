import tkinter as tk
from tkinter import messagebox

class FoodCard :
    def __init__(self, parent, title, manager, user_email, card_type, user, stack) :
        self.parent = parent
        self.title = title
        self.manager = manager
        self.user_email = user_email
        self.card_type = card_type
        self.stack = stack
        self.user = user

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.create_widgets()

    def create_widgets(self):
        # Card Frame
        self.card = tk.Frame(self.parent, bg=self.Dark_Gray, bd=2, relief='raised')
        # Header
        self.header = tk.Label(self.card, text=self.title, bg=self.Dark_Gray,
                               fg="white", font=("Arial", 20, "bold"))
        self.header.pack(anchor='w', padx=10, pady=5)
        # Items frame
        self.items_frame = tk.Frame(self.card, bg=self.Dark_Gray, relief='flat')
        self.items_frame.pack(anchor='w', padx=10, pady=5)
        # Add Button
        self.add_text = tk.Button(self.card, text='Add', bg=self.Dark_Blue,
                                  fg="white", font=("Helvetica", 15), relief="flat",
                                  command=self.go_to_food_page)
        self.add_text.pack(pady=5)

    def go_to_food_page(self) :
        if self.card_type in ["breakfast", "lunch", "dinner"]:
            from FoodPage import food_page
            f = food_page(self.manager, self.stack, self.user, meal_type=self.card_type)
            self.stack.push(f)
        elif self.card_type == "water":
            self.add_water()
        else :
            self.add_exercise()

    def add_water(self) :

        water_window = tk.Toplevel(self.parent)
        water_window.title("Water Intake")
        water_window.configure(bg=self.Dark_Gray)

        water_window.grab_set()

        window_width = 600
        window_height = 300

        screen_width = water_window.winfo_screenwidth()
        screen_height = water_window.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        water_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(
            water_window,
            text="Enter amount of water ( ml ) : ",
            bg=self.Dark_Gray,
            fg="white",
            font=("Arial", 15, "bold")
        )
        label.pack(pady=20)

        entry = tk.Entry(water_window, font=("Arial", 14), bg=self.Charcoal_Gray, fg="white",insertbackground="white")
        entry.pack(pady=10)

        def confirm() :
            try :
                amount = int(entry.get())
                if 50 <= amount <= 2000 :
                    today_str = self.stack.items[0].current_date.strftime("%Y-%m-%d")
                    logs = self.manager.load_file(self.manager.logs_file)

                    if self.user_email not in logs:
                        logs[self.user_email] = {}
                    if today_str not in logs[self.user_email]:
                        self.manager.ensure_log_for_date(self.user_email, today_str)
                        logs = self.manager.load_file(self.manager.logs_file)

                    logs[self.user_email][today_str]["water"].append(amount)
                    self.manager.save_file(self.manager.logs_file, logs)

                    messagebox.showinfo("Water Intake", f"Added {amount} ml of water")
                    self.update(self.stack.items[0].current_date)
                    water_window.destroy()
                else :
                    messagebox.showwarning("Invalid", "Value must be between 50 and 2000 ml")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        btn = tk.Button(
            water_window,
            text="Add Water",
            bg=self.Dark_Blue,
            fg="white",
            font=("Arial", 14, "bold"),
            relief="flat",
            cursor="hand2",
            command=confirm
        )
        btn.pack(pady=20)

    def add_exercise(self) :
        from ExercisePages.ExercisePage_1 import exercise_page_1
        e = exercise_page_1(self.parent, self.user,self.stack,self.manager)
        e.stack.push(e)
        e.mainloop()

    def pack(self, **kwargs) :
        self.card.pack(**kwargs)

    def update(self, current_date) :
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        today_str = current_date.strftime("%Y-%m-%d")
        self.manager.ensure_log_for_date(self.user_email, today_str)
        today_log = self.manager.get_today(self.user_email, today_str)

        if self.card_type in ["dinner", "lunch", "breakfast"] :
            items = today_log['food_log'][self.card_type]
            if not items:
                empty = tk.Label(self.items_frame, text="No items added yet",
                                 bg=self.Dark_Gray, relief='flat',
                                 fg="lightblue", font=("Helvetica", 15, "bold"))
                empty.pack(anchor='w')
            else :
                for item in items:
                    item_frame = tk.Frame(self.items_frame, bg=self.Dark_Gray, relief='flat')
                    item_frame.pack(anchor='w', fill="x", pady=3)

                    item_text = f"💠 {item['grams']} gm '{item['food']}' : {int(item['calories'])} Cal"
                    item_label = tk.Label(item_frame, text=item_text,
                                          bg=self.Dark_Gray, fg="lightblue", font=("Arial", 17))
                    item_label.pack(side="left", padx=10)

                    remove_btn = tk.Button(item_frame, text="Remove", bg=self.Dark_Gray, fg="red",
                                           font=("Arial", 12, "bold"),
                                           relief="flat", cursor="hand2",
                                           command=lambda i=item: self.remove_item(i, current_date))
                    remove_btn.pack(side="right", padx=10)

        elif self.card_type == "water" :

            water_logs = today_log.get("water", [])
            total_water = sum(water_logs)

            weight = self.user.get("weight")
            target_water = weight * 35
            remaining = max(0, target_water - total_water)

            summary = f"Target is ' {target_water} ' ml and you drunk ' {total_water} ' ml and the remaining is ' {remaining} ' ml"
            water_label = tk.Label(self.items_frame, text=summary,
                                   bg=self.Dark_Gray, fg="white", font=("Arial", 17, "bold"))
            water_label.pack(anchor='w', pady=(0, 10))

            if water_logs :
                for w in water_logs :
                    item_frame = tk.Frame(self.items_frame, bg=self.Dark_Gray, relief='flat')
                    item_frame.pack(anchor='w', fill="x", pady=2)

                    log_label = tk.Label(item_frame, text=f"💠you drunk {w} ml",
                                         bg=self.Dark_Gray, fg="lightblue", font=("Arial", 16))
                    log_label.pack(side="left", padx=10)

                    remove_btn = tk.Button(item_frame, text="Remove", bg=self.Dark_Gray, fg="red",
                                           font=("Arial", 12, "bold"),
                                           relief="flat", cursor="hand2",
                                           command=lambda amount=w: self.remove_water(amount, current_date))
                    remove_btn.pack(side="left", padx=10)

        elif self.card_type == "exercise" :

            exercises = today_log.get("exercise", [])

            if not exercises :

                empty = tk.Label(self.items_frame, text="No exercises added yet",
                                 bg=self.Dark_Gray , fg="lightblue", font=("Helvetica", 15, "bold"))
                empty.pack(anchor='w')

            else :

                for ex in exercises :

                    item_frame = tk.Frame(self.items_frame, bg=self.Dark_Gray, relief='flat')
                    item_frame.pack(anchor='w', fill="x", pady=3)

                    item_text = f"💠 {ex['name']} : {ex['minutes']} min , {int(ex['calories'])} Cal burned"
                    item_label = tk.Label(item_frame, text=item_text,
                                          bg=self.Dark_Gray, fg="lightblue", font=("Arial", 17))
                    item_label.pack(side="left", padx=10)

                    remove_btn = tk.Button(item_frame, text="Remove", bg=self.Dark_Gray, fg="red",
                                           font=("Arial", 12, "bold"),
                                           relief="flat", cursor="hand2",
                                           command=lambda i=ex: self.remove_exercise(i, current_date))
                    remove_btn.pack(side="right", padx=10)

    def remove_item(self, item, current_date) :
        today_str = current_date.strftime("%Y-%m-%d")
        logs = self.manager.load_file(self.manager.logs_file)

        today_log = logs.get(self.user_email, {}).get(today_str, None)

        if today_log and self.card_type in today_log["food_log"] :
            if item in today_log["food_log"][self.card_type] :
                if messagebox.askyesno("?",f"Are you sure you want to remove {item['food']} ? " ) :
                    today_log["food_log"][self.card_type].remove(item)

        self.manager.save_file(self.manager.logs_file, logs)
        self.update(current_date)

        diary_page = self.stack.items[0]
        diary_page.refresh()

    def remove_water(self, amount, current_date) :
        today_str = current_date.strftime("%Y-%m-%d")
        logs = self.manager.load_file(self.manager.logs_file)

        today_log = logs.get(self.user_email, {}).get(today_str, None)

        if today_log and "water" in today_log:
            if amount in today_log["water"] :
                if messagebox.askyesno("?",f"Are you sure you want to remove {amount} ?" ) :
                    today_log["water"].remove(amount)

        self.manager.save_file(self.manager.logs_file, logs)
        self.update(current_date)

        diary_page = self.stack.items[0]
        diary_page.refresh()

    def remove_exercise(self, exercise, current_date) :

        today_str = current_date.strftime("%Y-%m-%d")
        logs = self.manager.load_file(self.manager.logs_file)

        today_log = logs.get(self.user_email, {}).get(today_str, None)

        if today_log and "exercise" in today_log :
            if exercise in today_log["exercise"]:
                if messagebox.askyesno("?", f"Are you sure you want to remove {exercise['name']}?"):
                    today_log["exercise"].remove(exercise)

        self.manager.save_file(self.manager.logs_file, logs)
        self.update(current_date)

        diary_page = self.stack.items[0]
        diary_page.refresh()
