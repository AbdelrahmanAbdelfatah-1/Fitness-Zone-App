import tkinter as tk
from tkinter import messagebox
from Admin.utils import clear_frame, quick_sort
from Admin.data_storage import load_exercises, save_exercises

class ExerciseFrame(tk.Frame) :
    def __init__(self, parent, stack) :
        super().__init__(parent, bg="#111827")
        self.stack = stack
        self.exercises = load_exercises()
        self.sorted_keys = list(self.exercises.keys())
        quick_sort(self.sorted_keys)

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        # Header
        tk.Label(self, text="Exercise", font=("Arial", 28, "bold"), bg=self.Dark_Gray, fg="white")\
            .place(relx=0.5, rely=0.03, anchor="center")
        tk.Button(self, text="Back", command=self.go_back,
                  font=('Arial', 20, "bold"), bg=self.Dark_Gray, fg="white",
                  activebackground=self.Dark_Gray, activeforeground="white", relief='flat', bd=0)\
            .place(relx=0.9, rely=0.03, anchor="center")

        # Action buttons
        btn_width, btn_height = 10, 5
        tk.Button(self, text="Add", width=btn_width, height=btn_height, bg=self.Dark_Blue, fg="white",
                  font=("Arial", 15, "bold"), command=self.add_exercise).place(relx=0.2, rely=0.22, anchor="center")
        tk.Button(self, text="Update", width=btn_width, height=btn_height, bg=self.Dark_Blue, fg="white",
                  font=("Arial", 15, "bold"), command=self.update_exercise_ui).place(relx=0.5, rely=0.22, anchor="center")
        tk.Button(self, text="Delete", width=btn_width, height=btn_height, bg=self.Dark_Blue, fg="white",
                  font=("Arial", 15, "bold"), command=self.delete_exercise_ui).place(relx=0.8, rely=0.22, anchor="center")

        self.content_frame = tk.Frame(self, bg=self.Dark_Gray)
        self.content_frame.place(relx=0.5, rely=0.35, anchor="n", relwidth=0.85, relheight=0.55)

    def go_back(self):
        self.stack.pop()

    def search_exercise(self, query):
        all_names = []
        for cat in self.exercises:
            all_names.extend([ex["name"] for ex in self.exercises[cat]])
        return [name for name in all_names if query.lower() in name.lower()]

    # Scroll Helper
    def _add_mousewheel_scroll(self, canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Scrollable Frame Helper
    def _create_scrollable_frame(self, parent):
        canvas = tk.Canvas(parent, bg=self.Dark_Gray, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.Dark_Gray)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))
        self._add_mousewheel_scroll(canvas)
        return canvas, scrollable_frame


    def add_exercise(self):
        clear_frame(self.content_frame)
        canvas, scrollable_frame = self._create_scrollable_frame(self.content_frame)

        # Category Dropdown
        tk.Label(scrollable_frame, text="Category", fg="white", bg=self.Dark_Gray, font=("Arial", 14)).pack(anchor="w", pady=2, padx=7)
        options = ["Cardio", "Strength"]
        category_var = tk.StringVar()
        category_var.set(options[0])
        option_menu = tk.OptionMenu(scrollable_frame, category_var, *options)
        option_menu.config(font=("Arial", 14), bg="#1F2937", fg="white", activebackground="#004477",
                           activeforeground="white")
        option_menu["menu"].config(bg="#1F2937", fg="white", font=("Arial", 14))
        option_menu.pack(fill="x", pady=2, ipady=5, padx=7)

        entries = {}
        for field in ["Name", "YouTube URL", "Description", "Calories per hour"]:
            tk.Label(scrollable_frame, text=field, fg="white", bg=self.Dark_Gray, font=("Arial", 14)).pack(anchor="w", pady=2, padx=7)
            entry = tk.Entry(scrollable_frame, font=("Arial", 16), bd=2, relief="raised", fg="white", bg=self.Charcoal_Gray, insertbackground="white")
            entry.pack(fill="x", pady=2, ipady=5, padx=7)
            entries[field.lower()] = entry

        def save_new():
            cat = category_var.get()
            if not cat:
                return messagebox.showerror("Error", "Select category")
            if cat not in self.exercises:
                self.exercises[cat] = []

            try:
                cal = int(entries["calories per hour"].get())
            except ValueError:
                return messagebox.showerror("Error", "Calories per hour must be a number")

            new_ex = {
                "name": entries["name"].get(),
                "youtube": entries["youtube url"].get(),
                "description": entries["description"].get(),
                "calories_per_hour": cal
            }
            self.exercises[cat].append(new_ex)
            save_exercises(self.exercises)
            messagebox.showinfo("Success", f"{new_ex['name']} added")
            self.add_exercise()

        tk.Button(scrollable_frame, text="Save", fg="white", command=save_new, bg=self.Dark_Blue, font=("Arial", 14)).pack(pady=10, anchor="center", padx=7)


    def update_exercise_ui(self):
        self.listbox_ui(mode="update")

    def delete_exercise_ui(self):
        self.listbox_ui(mode="delete")

    def listbox_ui(self, mode="update") :
        clear_frame(self.content_frame)
        tk.Label(self.content_frame, text="Search Exercise:", fg="white", bg=self.Dark_Gray, font=("Arial", 17)).pack(anchor="w", pady=5, padx=7)
        search_entry = tk.Entry(self.content_frame, font=("Arial", 14), bd=2, relief="raised", fg="white", bg=self.Charcoal_Gray, insertbackground="white")
        search_entry.pack(fill="x", pady=(0,5), ipady=5, padx=7)

        result_box = tk.Listbox(self.content_frame, font=("Arial", 14), bd=2, relief="raised", activestyle="dotbox", bg=self.Charcoal_Gray, fg="lightblue")
        result_box.pack(fill="both", expand=True, pady=(0,5), padx=7)

        all_names = [ex["name"] for cat in self.exercises for ex in self.exercises[cat]]
        for name in all_names:
            result_box.insert(tk.END, name)

        def on_type(event=None):
            query = search_entry.get().strip()
            result_box.delete(0, tk.END)
            for name in self.search_exercise(query):
                result_box.insert(tk.END, name)

        search_entry.bind("<KeyRelease>", on_type)

        def perform_action() :
            if not result_box.curselection():
                return messagebox.showerror("Error", "Select an exercise")
            ex_name = result_box.get(result_box.curselection())
            selected_ex, selected_cat = None, None
            for cat, exercises_list in self.exercises.items():
                for ex in exercises_list:
                    if ex["name"] == ex_name:
                        selected_ex, selected_cat = ex, cat
                        break
                if selected_ex:
                    break
            if not selected_ex:
                return

            if mode == "update":
                self.edit_exercise(selected_ex, selected_cat)
            elif mode == "delete":
                if messagebox.askyesno("Confirm", f"Delete {ex_name}?"):
                    self.exercises[selected_cat].remove(selected_ex)
                    save_exercises(self.exercises)
                    messagebox.showinfo("Deleted", f"{ex_name} deleted")
                    on_type()

        result_box.bind("<Double-Button-1>", lambda e: perform_action())
        btn_text = "Edit Selected" if mode=="update" else "Delete Selected"
        tk.Button(self.content_frame, text=btn_text, command=perform_action, font=("Arial", 14), bg=self.Dark_Blue, fg="white").pack(pady=10, anchor="e", padx=7)

    def edit_exercise(self, selected_ex, selected_cat):
        clear_frame(self.content_frame)
        canvas, scrollable_frame = self._create_scrollable_frame(self.content_frame)

        tk.Label(scrollable_frame, text=f"💠 Update '{selected_ex['name']}'", fg="lightblue", bg=self.Dark_Gray, font=("Arial", 18)).pack(anchor="w", pady=5, padx=7)


        tk.Label(scrollable_frame, text="Category", fg="white",
                 bg=self.Dark_Gray, font=("Arial", 14)).pack(anchor="w",  pady=2 , padx=7)
        category_var = tk.StringVar()
        category_var.set(selected_cat)

        option_menu = tk.OptionMenu(scrollable_frame, category_var, "Cardio", "Strength")
        option_menu.config(font=("Arial", 14), bg="#1F2937", fg="white", activebackground="#004477",
                           activeforeground="white")
        option_menu["menu"].config(bg="#1F2937", fg="white", font=("Arial", 14))
        option_menu.pack(fill="x", pady=2, ipady=5, padx=7)

        f = {
            "Name": "name",
            "YouTube URL": "youtube",
            "Description": "description",
            "Calories per hour": "calories_per_hour"
        }

        entries = {}
        for field in ["Name", "YouTube URL", "Description", "Calories per hour"]:
            tk.Label(scrollable_frame, text=field, fg="white", bg=self.Dark_Gray, font=("Arial", 14)).pack(anchor="w", pady=2, padx=7)
            entry = tk.Entry(scrollable_frame, font=("Arial",16), bd=2, relief="raised", fg="white", bg=self.Charcoal_Gray, insertbackground="white")
            entry.insert(0, str(selected_ex[f[field]]))
            entry.pack(fill="x", pady=2, ipady=5, padx=7)
            entries[field.lower()] = entry

        def save_update():
            new_cat = category_var.get()
            try:
                cal = int(entries["calories per hour"].get())
            except ValueError:
                return messagebox.showerror("Error", "Calories per hour must be a number")

            if new_cat != selected_cat :
                self.exercises[selected_cat].remove(selected_ex)
                if new_cat not in self.exercises:
                    self.exercises[new_cat] = []
                self.exercises[new_cat].append(selected_ex)

            selected_ex["name"] = entries["name"].get()
            selected_ex["youtube"] = entries["youtube url"].get()
            selected_ex["description"] = entries["description"].get()
            selected_ex["calories_per_hour"] = cal

            save_exercises(self.exercises)
            messagebox.showinfo("Updated", f"{selected_ex['name']} updated")
            self.update_exercise_ui()

        tk.Button(scrollable_frame, text="Save", command=save_update, font=("Arial", 14), bg=self.Dark_Blue, fg="white").pack(pady=10, anchor="center", padx=7)


