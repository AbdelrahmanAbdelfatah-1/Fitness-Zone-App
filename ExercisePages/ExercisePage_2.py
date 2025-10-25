import tkinter as tk
import tkinter.messagebox as messagebox
import os
import json
import webbrowser


class exercise_page_2 (tk.Toplevel) :
    def __init__(self , master , exercise_kind , user , stack , manager ) :
        super().__init__(master)

        self.exercise_kind = exercise_kind
        self.stack = stack
        self.manager = manager
        self.user = user
        self.master = master

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.JSON_PATH = os.path.join(self.BASE_DIR, "Exercises.json")
        self.IMAGES_DIR = os.path.join(self.BASE_DIR, "images")

        with open(self.JSON_PATH, "r") as json_file :
            self.data = json.load(json_file)

        self.filtered_exercises = self.data[self.exercise_kind]
        self.current_exercise_list = self.data[self.exercise_kind]

        self.title(f"{self.exercise_kind} Exercises")
        self.configure(bg = self.Dark_Gray)
        self.state('zoomed')

        self.create_widgets()
        self.show_exercises()


    def create_widgets(self) :

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

        # main frame
        self.main_frame = tk.Frame(scrollable_frame, bg="#111827", relief='raised', bd=2)
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        # header frame
        header_frame = tk.Frame(self.main_frame, bg = self.Dark_Gray)
        header_frame.pack(fill="x", padx=20, pady=20)
        # back
        back_button = tk.Button(header_frame, text='← Back', font=('Arial', 18, 'bold'),
                                background=self.Dark_Gray, foreground='white',
                                relief='flat', activebackground=self.Dark_Gray,
                                activeforeground='white', command=self.stack.pop)
        back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Sort
        sort_button = tk.Button(
            header_frame,
            text="Sort by Calories",
            font=('Arial', 17, 'bold'),
            background=self.Dark_Gray,
            foreground='white',
            relief='flat',
            bd=0,
            activebackground=self.Dark_Gray,
            activeforeground="white",
            command=self.sort_by_calories
        )
        sort_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        # Title
        title = tk.Label(self.main_frame , text=self.exercise_kind , font=('Arial',30, 'bold'),
                         bg=self.Dark_Gray , fg="white")
        title.pack()
        # frame + icon to search
        search_frame = tk.Frame(self.main_frame, bg="#111827")
        search_frame.pack(fill="x", padx=20, pady=(10, 20))
        # icon
        icon = tk.Label(search_frame, text="🔍", font=("Arial", 16), bg="#111827", fg="white")
        icon.pack(side="left", padx=(5, 10))
        # search bar
        self.search_bar = tk.Entry(
            search_frame,
            bg="#1F2937",
            fg="white",
            relief="flat",
            font=("Arial", 18),
            insertbackground="white"
        )
        self.search_bar.pack(fill="x", padx=10, ipady=10)

        self.search_bar.insert(0, "Type to search...")
        self.search_bar.bind("<FocusIn>", self.clear_placeholder)
        self.search_bar.bind("<KeyRelease>", self.search)

        # exercise frames
        self.exercises_frame = tk.Frame(self.main_frame, bg=self.Dark_Gray , relief='raised', bd=2)
        self.exercises_frame.pack(expand=True, fill="both", padx=30, pady=30)

    def show_exercises(self) :

        for widget in self.exercises_frame.winfo_children() :
            widget.destroy()

        for exercise in self.current_exercise_list :

            frame = tk.Frame(self.exercises_frame, bg=self.Charcoal_Gray, bd=2, relief="ridge", padx=10, pady=20)
            frame.pack(padx=10, pady=10,fill="both", expand=True)

            # Name as clickable link
            name_btn = tk.Button(frame, text=f"💠Link : {exercise["name"]}" , font=("Arial", 20, "bold") ,
                                 bg = self.Charcoal_Gray , fg="white", relief="flat",
                                 activebackground=self.Charcoal_Gray , bd = 0 , padx=0 , pady=0 ,
                                 highlightthickness=0 , activeforeground = "red" ,
                                 command = lambda url = exercise["youtube"] : webbrowser.open( url ) )
            name_btn.pack(anchor="w")

            # Description
            tk.Label(frame, text = f" description : {exercise['description']}" ,
                     bg = self.Charcoal_Gray , fg="lightblue", font=("Arial",18)).pack(anchor="w")
            # calories
            tk.Label(frame,text=f" Calories : {exercise['calories_per_hour']} cal / hour ",
                     bg=self.Charcoal_Gray, fg="lightblue", font=("Arial", 18)).pack(anchor="w")

            # Add button
            add = tk.Button(frame, text="Add", font=("Arial", 15), bg = self.Dark_Blue
                            , fg="white", relief="flat" , command = lambda ex = exercise : self.add_exercise(ex))
            add.pack(anchor="center")

    def add_exercise(self, exercise) :
        top = tk.Toplevel(self)
        top.title(f"Add {exercise['name']}")
        top.configure(bg=self.Dark_Gray)
        top.grab_set()

        window_width, window_height = 600 , 300
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        top.geometry(f"{window_width}x{window_height}+{x}+{y}")

        tk.Label(top, text=f"Enter the number of minutes you trained in {exercise['name']} : ",
                 font=("Arial", 16), bg=self.Dark_Gray, fg="white").pack(pady=20)

        entry = tk.Entry(top, font=("Arial", 14), bg=self.Charcoal_Gray, fg="white", insertbackground="white")
        entry.pack(pady=10)

        def save_minutes():
            try :
                minutes = float(entry.get())
                if minutes <= 0:
                    messagebox.showwarning("Invalid", "Please enter a valid number of minutes")
                    return

                calories_burned = round ( exercise['calories_per_hour'] * (minutes / 60) , 1 )

                logs = self.manager.load_file(self.manager.logs_file)
                today_str = self.stack.items[0].current_date.strftime("%Y-%m-%d")

                if self.user["email"] not in logs :
                    logs[self.user["email"]] = {}
                if today_str not in logs[self.user["email"]] :
                    logs[self.user["email"]][today_str] = {
                        "daily_calories": 0,
                        "food_log": {"breakfast": [], "lunch": [], "dinner": []},
                        "exercise": [],
                        "water": []
                    }

                logs[self.user["email"]][today_str]["exercise"].append(
                    {
                        "name": exercise['name'],
                        "minutes": minutes,
                        "calories": calories_burned
                    }
                )

                self.manager.save_file(self.manager.logs_file, logs)
                messagebox.showinfo("Exercise", "Exercise saved successfully")
                self.stack.items[0].refresh()
                top.destroy()

            except ValueError :
                tk.messagebox.showerror("Invalid Input", "Please enter a valid number of minutes")

        tk.Button(top, text="Save", font=("Arial", 14), bg=self.Dark_Blue, fg="white", relief="flat",
                  command=save_minutes).pack(pady=20)

    def search(self, event):
        s = self.search_bar.get().lower()
        if s.strip() == "":
            self.current_exercise_list = self.data[self.exercise_kind]  
        else:
            self.current_exercise_list = [ex for ex in self.data[self.exercise_kind] if s in ex["name"].lower()]
        self.show_exercises()

    def clear_placeholder(self,event=None) :
        if self.search_bar.get() == "Type to search...":
            self.search_bar.delete(0, tk.END)

    def merge_sort(self, items) :
        if len(items) > 1:
            mid = len(items) // 2
            left_half = items[:mid]
            right_half = items[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i]['calories_per_hour'] < right_half[j]['calories_per_hour']:
                    items[k] = left_half[i]
                    i += 1
                else:
                    items[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                items[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                items[k] = right_half[j]
                j += 1
                k += 1
        return items

    def sort_by_calories(self):
        self.current_exercise_list = self.merge_sort(self.current_exercise_list)
        self.show_exercises()
