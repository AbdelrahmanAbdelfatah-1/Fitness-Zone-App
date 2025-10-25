import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import ImageTk
from FoodPageDetails.chart_utils import create_donut_image
from FoodPageDetails.ui_components import info_row, nut_col


class AddFoodPageDetails(tk.Toplevel) :
    def __init__(self, master, food_name, user, stack, manager, meal_type="dinner"):
        super().__init__(master)
        self.manager = manager
        self.meal_type = meal_type
        self.food_name = food_name
        self.user = user
        self.stack = stack

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.title(f"Add Food - {food_name}")
        self.state("zoomed")
        self.configure(bg=self.Dark_Gray)

        self.food_info = self.manager.load_file(self.manager.food_file)[self.food_name]

        carbs_calories = self.food_info['carbs'] * 4
        protein_calories = self.food_info['protein'] * 4
        fat_calories = self.food_info['fat'] * 9

        total_calories = carbs_calories + protein_calories + fat_calories

        if total_calories == 0:
            total_calories = 1

        carbs_perc = (carbs_calories / total_calories) * 100
        fat_perc = (fat_calories / total_calories) * 100
        protein_perc = (protein_calories / total_calories) * 100

        # main frame
        main_frame = tk.Frame(self, relief='raised', bd=2, bg=self.Dark_Gray)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Top bar
        top = tk.Frame(main_frame, bg=self.Dark_Blue, height=50)
        top.pack(fill="x")

        back = tk.Button(
            top, text="← Back", font=("Arial", 18),
            bg=self.Dark_Blue, bd=0, activebackground=self.Dark_Blue, fg="white",
            command=self.go_back
        )
        back.pack(side="left", padx=12, pady=8)

        tick = tk.Button(
            top, text="Add", font=("Arial", 16),
            fg="white", bg=self.Dark_Gray, bd=0, activebackground="#004477",
            command=self.add_food
        )
        tick.pack(side="right", padx=12)

        spacer = tk.Frame(main_frame, height=10, bg="#111827")
        spacer.pack(fill="x")

        # Food name
        food_frame = tk.Frame(main_frame, bg=self.Charcoal_Gray, pady=12, relief="raised", bd=2)
        food_frame.pack(fill="x", padx=12)
        food_label = tk.Label(food_frame, text=self.food_name, font=("Arial", 20, "bold"),
                              bg="#1F2937", fg="white")
        food_label.pack(anchor="w", padx=16)

        spacer = tk.Frame(main_frame, height=5, bg="#111827")
        spacer.pack(fill="x")

        # Info container
        info_container = tk.Frame(main_frame, bg=self.Dark_Gray, relief="raised", bd=2)
        info_container.pack(fill="x", pady=5, padx=12)
        info_row(info_container, "Meal", self.meal_type.title())
        self.grams_entry = info_row(info_container, "Number of Grams", "100", is_first=True)
        self.grams_var = tk.StringVar(value="100")
        self.grams_entry.config(textvariable=self.grams_var)
        self.grams_var.trace_add("write", self.update_nutrients)

        # Donut chart
        chart_container = tk.Frame(main_frame, bg=self.Dark_Gray, pady=12, relief="raised", bd=2)
        chart_container.pack(fill="x", pady=15, padx=12)

        size = 220
        slices = [
            (carbs_perc, (52, 189, 172)),
            (fat_perc, (153, 102, 204)),
            (protein_perc, (236, 170, 71))
        ]

        donut_img = create_donut_image(size, slices, f"{self.food_info['calories']}\nCal")
        donut_tk = ImageTk.PhotoImage(donut_img)

        row_frame = tk.Frame(chart_container, bg=self.Dark_Gray)
        row_frame.pack(fill="x", pady=10, padx=10)

        self.canvas_label = tk.Label(row_frame, image=donut_tk, bg=self.Dark_Gray)
        self.canvas_label.image = donut_tk
        self.canvas_label.pack(pady=10)

        nutrients = tk.Frame(row_frame, bg=self.Dark_Gray)
        nutrients.pack(pady=10)

        self.carbs_lbl = nut_col(nutrients, carbs_perc, self.food_info['carbs'], "Carbs")
        self.fat_lbl = nut_col(nutrients, fat_perc, self.food_info['fat'], "Fat")
        self.protein_lbl = nut_col(nutrients, protein_perc, self.food_info['protein'], "Protein")

        self.update_nutrients()

    def update_nutrients(self, *args) :

        s = self.grams_var.get()
        try:
            grams = int(s)
            if grams < 0:
                grams = 0
        except (ValueError, TypeError):
            grams = 0

        food_info = self.food_info

        calories_taken = (food_info["calories"] * grams) / 100
        protein_taken = (food_info["protein"] * grams) / 100
        carbs_taken = (food_info["carbs"] * grams) / 100
        fat_taken = (food_info["fat"] * grams) / 100

        carbs_calories = carbs_taken * 4
        protein_calories = protein_taken * 4
        fat_calories = fat_taken * 9

        total_calories = carbs_calories + protein_calories + fat_calories

        if total_calories == 0:
            total_calories = 1

        carbs_perc = (carbs_calories / total_calories) * 100
        fat_perc = (fat_calories / total_calories) * 100
        protein_perc = (protein_calories / total_calories) * 100

        slices = [
            (carbs_perc, (52, 189, 172)),
            (fat_perc, (153, 102, 204)),
            (protein_perc, (236, 170, 71))
        ]

        donut_img = create_donut_image(220, slices, f"{int(calories_taken)}\nCal")
        donut_tk = ImageTk.PhotoImage(donut_img)

        self.canvas_label.config(image=donut_tk)
        self.canvas_label.image = donut_tk

        self.carbs_lbl["pct_label"].config(text=f"{round(carbs_perc, 1)}%")
        self.carbs_lbl["grams_label"].config(text=f"{round(carbs_taken, 1)}g")

        self.fat_lbl["pct_label"].config(text=f"{round(fat_perc, 1)}%")
        self.fat_lbl["grams_label"].config(text=f"{round(fat_taken, 1)}g")

        self.protein_lbl["pct_label"].config(text=f"{round(protein_perc, 1)}%")
        self.protein_lbl["grams_label"].config(text=f"{round(protein_taken, 1)}g")

    def go_back(self):
        self.stack.pop()

    def add_food(self):
        s = self.grams_var.get()
        try:
            grams = int(s)
        except (ValueError, TypeError):
            grams = 0

        if grams <= 0 :
            messagebox.showwarning("Invalid", "Please enter a valid number of grams")
            return
        today_str = self.stack.items[0].current_date.strftime("%Y-%m-%d")
        self.manager.add_food(self.user["email"], self.food_name, grams, self.meal_type, today_str)
        messagebox.showinfo("Add Food", f"{self.food_name} added successfully")
        diary_page = self.stack.items[0]
        diary_page.refresh()
        self.stack.pop()