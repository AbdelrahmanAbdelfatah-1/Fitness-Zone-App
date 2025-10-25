import tkinter as tk

class food_page(tk.Toplevel) :
    def __init__( self , fitness_manager , stack , user , meal_type,food_file = "Food.json" , logs_file = "Logs.json") :
        super().__init__()

        import os
        self.food_file = os.path.join(os.path.dirname(__file__), food_file)
        self.logs_file = os.path.join(os.path.dirname(__file__), logs_file)

        self.fitness_manager = fitness_manager
        self.stack = stack
        self.user = user
        self.meal_type = meal_type

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.title("Food Page")
        self.state('zoomed')
        self.configure(bg=self.Dark_Gray)

        self.food_data = self.fitness_manager.load_file(self.food_file)
        self.current_food_list = list(self.food_data.keys())
        self.create_widgets()

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
        main_frame = tk.Frame(scrollable_frame, bg="#111827", relief='raised', bd=2 )
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        # header frame
        header_frame = tk.Frame(main_frame, bg=self.Dark_Gray)
        header_frame.pack( fill="x", padx=20, pady=20)
        # back
        back_button = tk.Button(header_frame,text='← Back',font=('Arial',17,'bold'),
            background='#111827',foreground='white',
            relief='flat',activebackground='#0066A8',
            activeforeground='white',command = self.go_back )
        back_button.grid(row = 0 , column = 0 , padx = 5, pady = 5 , sticky='w')
        # sort btn
        sort_button = tk.Button(
            header_frame,
            text="Sort by Calories",
            font=('Arial', 17, 'bold'),
            background=self.Dark_Gray,
            foreground='white',
            relief='flat',
            bd = 0 ,
            activebackground=self.Dark_Gray ,
            activeforeground="white" ,
            command=self.sort_by_calories
        )
        sort_button.grid(row = 0 , column = 1 , padx = 5, pady = 5 , sticky='e')

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        # search Label
        search = tk.Label(main_frame , text="Search Food" , font=('Arial', 29 ,'bold')
                         , bg="#111827", fg="white",  )
        search.pack(padx = 20 ,pady=10)
        # frame + icon
        search_frame = tk.Frame(main_frame, bg="#111827")
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        # icon
        icon = tk.Label(search_frame, text="🔍", font=("Arial", 16), bg="#111827" , fg="white")
        icon.pack(side="left", padx=(5, 10))
        # search bar
        self.search_bar = tk.Entry(
            search_frame ,
            bg="#1F2937",
            fg="white",
            relief="flat",
            font=("Arial", 18),
            insertbackground="white"
        )

        self.search_bar.pack(fill="x", padx=5 , ipady=10)

        self.search_bar.insert(0, "Type to search...")
        self.search_bar.bind("<FocusIn>", self.clear_placeholder)
        self.search_bar.bind("<KeyRelease>", self.filter_foods)
        # all food frame
        self.food_frame = tk.Frame(main_frame, bg="#111827")
        self.food_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.display_foods(list(self.food_data.keys()))

    def display_foods(self,food_list) :

        self.current_food_list = food_list

        for thing in self.food_frame.winfo_children() :
            thing.destroy()

        for food_name in food_list :

            item_frame = tk.Frame(self.food_frame, bg = self.Dark_Blue , relief='raised', bd=2)
            item_frame.pack(fill='x', pady=5, padx=10)

            row_frame = tk.Frame(item_frame, bg=self.Dark_Blue)
            row_frame.pack(fill="x", pady=5, padx=5)

            tk.Label(row_frame, text=food_name.title(), font=("Arial", 19,'bold'),
                     bg=self.Dark_Blue, fg = "white",anchor="w").pack(side="left")

            add_btn = tk.Button(row_frame, text="Add",
                                font=("Arial", 15, "bold"),
                                bg = self.Charcoal_Gray, fg="white",relief="flat", command = lambda fname = food_name : self.go_to_foodpagedetails(fname) )
            add_btn.pack(side="right", padx=5)

    def filter_foods(self,event=None) :
        search = self.search_bar.get().lower()
        filtered = [food for food in self.food_data.keys() if search in food.lower()]
        self.display_foods(filtered)

    def clear_placeholder(self,event=None) :
        if self.search_bar.get() == "Type to search...":
            self.search_bar.delete(0, tk.END)

    def go_back(self):
        self.stack.pop()

    def go_to_foodpagedetails(self, food_name) :
        from FoodPageDetails.design_page import AddFoodPageDetails
        d = AddFoodPageDetails(self, food_name, self.user, self.stack, self.fitness_manager, meal_type=self.meal_type)
        self.stack.push(d)

    def merge_sort(self, items):
        if len(items) > 1:
            mid = len(items) // 2
            left_half = items[:mid]
            right_half = items[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i][1] < right_half[j][1]:
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
        foods_with_cal = []
        for food_name in self.current_food_list :
            food_info = self.food_data.get(food_name, {})
            cal = food_info.get("calories", 0)
            foods_with_cal.append((food_name, cal))

        sorted_foods = self.merge_sort(foods_with_cal)
        sorted_names = [f[0] for f in sorted_foods]

        self.display_foods(sorted_names)

