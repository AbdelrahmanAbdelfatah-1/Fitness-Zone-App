import tkinter as tk
from tkinter import messagebox
from Admin.utils import clear_frame, quick_sort, binary_search
from Admin.data_storage import load_foods, save_foods


class FoodFrame(tk.Frame) :
    def __init__(self, parent, stack):
        super().__init__(parent, bg="#111827")
        self.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        self.stack = stack
        self.foods = load_foods()
        self.sorted_food_keys = list(self.foods.keys())
        quick_sort(self.sorted_food_keys)

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"
        self.Accent_Color = "#00B4D8"

        # Header
        header_frame = tk.Frame(self, bg=self.Dark_Gray)
        header_frame.pack(fill='x', pady=(0, 20))

        tk.Label(header_frame, text="Food Management", font=("Arial", 28, "bold"),
                 bg=self.Dark_Gray, fg="white").pack(side='left', padx=20, pady=10)

        tk.Button(header_frame, text="← Back", command=self.go_back,
                  font=('Arial', 16, "bold"), bg=self.Charcoal_Gray, fg="white",
                  activebackground=self.Dark_Blue, activeforeground="white",
                  relief='flat', bd=0, padx=20, pady=5).pack(side='right', padx=20)

        # buttons
        btn_frame = tk.Frame(self, bg=self.Dark_Gray)
        btn_frame.pack(fill='x', pady=20)

        btn_config = {
            "width": 15, "height": 3, "fg": "white", "font": ("Arial", 14, "bold"),
            "relief": "raised", "bd": 2
        }

        tk.Button(btn_frame, text="➕ Add Food", bg="#10B981",
                  command=self.add_food, **btn_config).pack(side='left', expand=True)

        tk.Button(btn_frame, text="✏️ Update Food", bg=self.Dark_Blue,
                  command=self.update_food_ui, **btn_config).pack(side='left', expand=True)

        tk.Button(btn_frame, text="🗑️ Delete Food", bg="#EF4444",
                  command=self.delete_food_ui, **btn_config).pack(side='left', expand=True)

        # Content frame
        self.content_frame = tk.Frame(self, bg=self.Dark_Gray, relief='sunken', bd=1)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value=f"Total Foods : {len(self.foods)}")
        status_bar = tk.Label(self, textvariable=self.status_var , bg=self.Charcoal_Gray,
                              fg="white", font=("Arial", 10), anchor='w')
        status_bar.pack(fill='x', side='bottom', ipady=5)

    def go_back(self) :
        self.stack.pop()

    def search_food(self, query) :

        idx , sorted_keys = binary_search(self.sorted_food_keys, query)
        if idx != -1 :
            return [sorted_keys[idx]]
        else :
            return [key for key in self.sorted_food_keys if query.lower() in key.lower()]

    def add_food(self) :
        clear_frame(self.content_frame)

        # scrollable
        container = self.create_scrollable_container(self.content_frame)
        scrollable_frame = container['frame']
        canvas = container['canvas']

        # title
        tk.Label(scrollable_frame, text="➕ Add New Food", fg=self.Accent_Color,
                 bg=self.Dark_Gray, font=("Arial", 20, "bold")).pack(anchor="w", pady=(5, 20), padx=5)

        entries = {}
        fields = ["Name", "Carbs (gm)", "Fat (gm)", "Protein (gm)", "Calories for 100 gm"]

        for field in fields :
            # Field label
            tk.Label(scrollable_frame, text=field, fg="white", bg=self.Dark_Gray,
                     font=("Arial", 14, "bold")).pack(anchor="w", pady=(15, 5), padx=7)

            # Entry field
            entry = tk.Entry(scrollable_frame, font=("Arial", 14), bd=2, relief="sunken",
                             justify="left", fg="white", bg=self.Charcoal_Gray,
                             insertbackground="white", width=30)
            entry.pack(fill="x", pady=5, ipady=5, padx=8)
            entries[field.split(' ')[0].lower()] = entry

            if field != "Name" :
                entry.config(validate="key", validatecommand=(
                    self.register(self.validate_numeric), '%P'
                ))

        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg=self.Dark_Gray)
        button_frame.pack(fill='x', pady=20)

        def save_new() :
            fname = entries["name"].get().strip().lower()
            if not fname :
                messagebox.showerror("Error", "❌ Food name is required!")
                return

            if fname in self.foods :
                messagebox.showerror("Error", f"❌ '{fname}' already exists!")
                return

            try :
                self.foods[fname] = {
                    "carbs": float(entries["carbs"].get() or 0),
                    "fat": float(entries["fat"].get() or 0),
                    "protein": float(entries["protein"].get() or 0),
                    "calories": float(entries["calories"].get() or 0),
                }
                save_foods(self.foods)
                messagebox.showinfo("Success", f"✅ '{fname}' added successfully!")
                self.sorted_food_keys = list(self.foods.keys())
                quick_sort(self.sorted_food_keys)
                self.status_var.set(f"Total Foods: {len(self.foods)} - Last Added: {fname}")

            except ValueError :
                messagebox.showerror("Error", "❌ Please enter valid numbers!")

        def clear_form() :
            for entry in entries.values() :
                entry.delete(0, tk.END)

        tk.Button(button_frame, text="💾 Save Food", command=save_new ,
                  font=("Arial", 14, "bold"), bg="#10B981", fg="white" ,
                  padx=20, pady=10).pack(side='left', padx=10)

        tk.Button(button_frame, text="🗑️ Clear", command=clear_form,
                  font=("Arial", 14), bg="#6B7280", fg="white",
                  padx=20, pady=10).pack(side='left', padx=10)

    def update_food_ui(self) :
        clear_frame(self.content_frame)

        # Search section
        search_frame = tk.Frame(self.content_frame, bg=self.Dark_Gray)
        search_frame.pack(fill='x', pady=10)

        tk.Label(search_frame, text="Search Food to Update : ", fg="white",
                 bg=self.Dark_Gray, font=("Arial", 17, "bold")).pack(anchor="w", pady=5, padx=7)

        search_entry = tk.Entry(search_frame, font=("Arial", 14), bd=2, relief="sunken",
                                justify="left", bg=self.Charcoal_Gray, insertbackground="white",
                                fg="white")
        search_entry.pack(fill="x", pady=(0, 10), ipady=8, padx=7)
        search_entry.focus()

        # Results section
        results_frame = tk.Frame(self.content_frame, bg=self.Dark_Gray)
        results_frame.pack(fill='both', expand=True)

        tk.Label(results_frame, text="Select Food (Double-click to edit) : ",
                 fg="white", bg=self.Dark_Gray, font=("Arial", 15, "bold")).pack(anchor="w", padx=7)

        result_box = tk.Listbox(results_frame, font=("Arial", 12), bd=2, relief="sunken",
                                activestyle="dotbox", bg=self.Charcoal_Gray, fg="lightblue",
                                selectbackground=self.Dark_Blue, selectforeground="white")
        result_box.pack(fill="both", expand=True, pady=(5, 10), padx=7)

        for key in self.sorted_food_keys:
            result_box.insert(tk.END, key)

        def on_type(event) :
            query = search_entry.get().strip()
            result_box.delete(0, tk.END)
            for key in self.search_food(query):
                result_box.insert(tk.END, key)

        def edit_selected(event=None) :
            if not result_box.curselection() :
                messagebox.showerror("Error", "❌ Please select a food to update!")
                return
            key = result_box.get(result_box.curselection())
            self.open_edit_form(key)

        search_entry.bind("<KeyRelease>", on_type)
        result_box.bind("<Double-1>", edit_selected)

    def open_edit_form(self, old_key) :

        clear_frame(self.content_frame)

        container = self.create_scrollable_container(self.content_frame)
        scrollable_frame = container['frame']

        # Form title
        tk.Label(scrollable_frame, text=f"Editing: '{old_key}'",
                 fg=self.Accent_Color, bg=self.Dark_Gray, font=("Arial", 18, "bold")).pack(
            anchor="w", pady=(0, 20), padx=7)

        food = self.foods[old_key]
        entries = {}

        fields = ["Name", "Carbs (gm)", "Fat (gm)", "Protein (gm)", "Calories for 100 gm"]

        for field in fields:
            tk.Label(scrollable_frame, text=field, fg="white", bg=self.Dark_Gray,
                     font=("Arial", 14, "bold")).pack(anchor="w", pady=(15, 5), padx=7)

            entry = tk.Entry(scrollable_frame, font=("Arial", 14), bd=2, relief="sunken",
                             justify="left", fg="white", bg=self.Charcoal_Gray,
                             insertbackground="white", width=30)

            if field == "Name" :
                entry.insert(0, old_key)
            else :
                field_key = field.split(' ')[0].lower()
                entry.insert(0, str(food[field_key]))

            entry.pack(fill="x", pady=5, ipady=8, padx=(7, 7))
            entries[field.split(' ')[0].lower()] = entry

            if field != "Name" :
                entry.config(validate="key", validatecommand=(
                    self.register(self.validate_numeric), '%P'
                ))

        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg=self.Dark_Gray)
        button_frame.pack(fill='x', pady=20)

        def save_update():

            new_name = entries["name"].get().strip().lower()

            if not new_name:
                messagebox.showerror("Error", "❌ Food name cannot be empty!")
                return

            try :
                updated_data = {
                    "carbs": float(entries["carbs"].get() or 0),
                    "fat": float(entries["fat"].get() or 0),
                    "protein": float(entries["protein"].get() or 0),
                    "calories": float(entries["calories"].get() or 0),
                }

                if new_name != old_key:
                    if new_name in self.foods and new_name != old_key:
                        messagebox.showerror("Error", f"❌ '{new_name}' already exists!")
                        return

                    del self.foods[old_key]
                    self.foods[new_name] = updated_data
                    action_msg = f"Renamed '{old_key}' to '{new_name}'"
                else :

                    self.foods[old_key] = updated_data
                    action_msg = f"Updated '{old_key}'"

                save_foods(self.foods)
                messagebox.showinfo("Success", f"✅ {action_msg} successfully!")

                self.sorted_food_keys = list(self.foods.keys())
                quick_sort(self.sorted_food_keys)
                self.status_var.set(f"Total Foods: {len(self.foods)} - Last Updated: {new_name}")

                self.update_food_ui()

            except ValueError:
                messagebox.showerror("Error", "❌ Please enter valid numbers!")

        def cancel_edit() :
            self.update_food_ui()

        tk.Button(button_frame, text="💾 Save Changes", command=save_update,
                  font=("Arial", 14, "bold"), bg=self.Dark_Blue, fg="white",
                  padx=20, pady=10).pack(side='left', padx=10)

        tk.Button(button_frame, text="❌ Cancel", command=cancel_edit,
                  font=("Arial", 14), bg="#6B7280", fg="white",
                  padx=20, pady=10).pack(side='left', padx=10)

    def delete_food_ui(self) :
        clear_frame(self.content_frame)

        search_frame = tk.Frame(self.content_frame, bg=self.Dark_Gray)
        search_frame.pack(fill='x', pady=10)

        tk.Label(search_frame, text="Search Food to Delete : ", fg="white",
                 bg=self.Dark_Gray, font=("Arial", 17, "bold")).pack(anchor="w", pady=5, padx=7)

        search_entry = tk.Entry(search_frame, font=("Arial", 14), bd=2, relief="sunken",
                                justify="left", bg=self.Charcoal_Gray, insertbackground="white",
                                fg="white")
        search_entry.pack(fill="x", pady=(0, 10), ipady=8, padx=7)
        search_entry.focus()

        # Results
        results_frame = tk.Frame(self.content_frame, bg=self.Dark_Gray)
        results_frame.pack(fill='both', expand=True)

        tk.Label(results_frame, text="Select Food (Double-click to delete):",
                 fg="white", bg=self.Dark_Gray, font=("Arial", 15, "bold")).pack(anchor="w", padx=7)

        result_box = tk.Listbox(results_frame, font=("Arial", 12), bd=2, relief="sunken",
                                activestyle="dotbox", bg=self.Charcoal_Gray, fg="lightblue",
                                selectbackground="#EF4444", selectforeground="white")
        result_box.pack(fill="both", expand=True, pady=(5, 10), padx=7)

        for key in self.sorted_food_keys:
            result_box.insert(tk.END, key)

        def on_type(event) :
            query = search_entry.get().strip()
            result_box.delete(0, tk.END)
            for key in self.search_food(query):
                result_box.insert(tk.END, key)

        def delete_selected(event=None) :
            if not result_box.curselection():
                messagebox.showerror("Error", "❌ Please select a food to delete!")
                return

            key = result_box.get(result_box.curselection())

            food_details = self.foods[key]
            detail_text = f"""
            Name: {key}
            Carbs: {food_details['carbs']}g
            Fat: {food_details['fat']}g
            Protein: {food_details['protein']}g
            Calories: {food_details['calories']}
                        """.strip()

            if messagebox.askyesno("Confirm Deletion",
                                   f"🗑️ Are you sure you want to delete?\n\n{detail_text}"):
                del self.foods[key]
                save_foods(self.foods)
                messagebox.showinfo("Deleted", f"✅ '{key}' deleted successfully!")

                # Update UI
                result_box.delete(0, tk.END)
                for k in self.search_food(search_entry.get().strip()):
                    result_box.insert(tk.END, k)

                self.sorted_food_keys = list(self.foods.keys())
                quick_sort(self.sorted_food_keys)
                self.status_var.set(f"Total Foods: {len(self.foods)} - Last Deleted: {key}")

        search_entry.bind("<KeyRelease>", on_type)
        result_box.bind("<Double-1>", delete_selected)

    def create_scrollable_container(self, parent) :
        canvas = tk.Canvas(parent, bg=self.Dark_Gray, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.Dark_Gray)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        return {'canvas': canvas, 'frame': scrollable_frame}

    def validate_numeric(self, value) :
        if value == "" or value == "-":
            return True
        try :
            float(value)
            return True
        except ValueError:
            return False