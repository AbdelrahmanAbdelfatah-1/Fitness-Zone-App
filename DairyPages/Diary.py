import tkinter as tk
import tkinter.messagebox as messagebox
from DairyPages.food_card import FoodCard
from datetime import datetime,timedelta

class diary (tk.Tk) :
     def __init__(self , user , stack , manager ) :
        super().__init__()

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.state('zoomed')
        self.configure(bg=self.Dark_Gray)
        self.title("Diary")

        self.manager = manager
        self.user = user
        self.stack = stack
        self.current_date = datetime.today()

        self.previous_remaining_positive = True

        today_str = self.current_date.strftime("%Y-%m-%d")
        self.manager.ensure_log_for_date(self.user["email"], today_str)

        self.create_widgets()
        self.setup_data()
        self.create_cards()
        self.refresh()


     def create_widgets (self) :
        # ------- Canvas + Scrollbar -----------
        canvas = tk.Canvas(self, bg=self.Dark_Gray)
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

        # Main Frame
        self.main_frame = tk.Frame(scrollable_frame, bg = self.Dark_Gray , relief = 'raised' , bd = 2 )
        self.main_frame.pack( padx = 50 , pady = 50 ,expand = True ,fill = 'both' )

        # header frame
        header_frame = tk.Frame(self.main_frame, bg = self.Dark_Gray  )
        header_frame.pack(fill="x",expand=True)
        # Log out
        back_button = tk.Button(header_frame, text=" Log out ", font = ( "Arial" , 15 , "bold"),
                                fg = "white" , bg="red" , relief='flat', cursor='hand2',
                                activebackground="white" , command = self.logout)
        back_button.pack(side="left", padx=20, pady=20)
        # Profile
        pro_button = tk.Button(header_frame, text="Profile", font=("Arial", 15, "bold"),
                                fg="white", bg="red", relief='flat', cursor='hand2',
                                activebackground="white",command=self.profile)
        pro_button.pack(side="right", padx=20, pady=20)
        # Date Frame
        self.date_frame = tk.Frame(self.main_frame, bg = self.Dark_Gray  )
        self.date_frame.pack( padx=50 )

        # DairyPages Title
        title = tk.Label(self.main_frame,text="Diary",bg=self.Dark_Gray,fg='white',font=("Arial",26,"bold"))
        title.pack(padx=10, pady=20)

        self.calories_label = tk.Label( self.main_frame , text = "Cal - Food + Exc = ", bg = self.Dark_Gray
                                  , fg = 'white', font = ( "Helvetica", 25 , "bold" ) )
        self.calories_label.pack(pady=(5,15))

        tk.Label(self.main_frame, text="Daily Calories      -      Food      +     Exercise     =     Remaining"
                 , bg=self.Dark_Gray , fg = 'white', font=('Arial',16)).pack(pady=8)

     def logout (self) :
         self.destroy()
         from LoginPage import login_page
         l = login_page()
         l.mainloop()

     def profile (self) :
         from ProfilePage.Profile import profile_page
         p = profile_page(self.main_frame, self.user, self.stack, self.manager)
         self.stack.push(p)

     def setup_data(self) :

         self.prev_btn = tk.Button( self.date_frame , text=" < ", bg = self.Dark_Gray , fg="white" ,
                                   font=("Arial", 20, "bold"), relief='flat', command=self.go_prev_day )
         self.prev_btn.pack(side="left")

         self.date_label = tk.Label( self.date_frame , text=self.current_date.strftime("%Y-%m-%d") ,
                                    bg=self.Dark_Gray , fg="white", font=("Arial", 20, "bold"))
         self.date_label.pack(side="left", padx=10)

         self.next_btn = tk.Button(self.date_frame, text=">", bg=self.Dark_Gray, fg="white",
                                   font=("Arial", 20, "bold"), relief='flat', command=self.go_next_day)
         self.next_btn.pack(side="left")

     def go_prev_day(self) :
         self.current_date -= timedelta(days=1)
         self.update_date()

     def go_next_day(self) :
         self.current_date += timedelta(days=1)
         self.update_date()

     def update_date(self) :
         self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))
         today_str = self.current_date.strftime("%Y-%m-%d")
         self.manager.ensure_log_for_date(self.user["email"], today_str)
         self.refresh()

     def update_calories_data(self) :
         logs = self.manager.load_file(self.manager.logs_file)
         today_str = self.current_date.strftime("%Y-%m-%d")
         today_log = logs.get(self.user["email"], {}).get(today_str, None)

         if today_log is None :
             self.manager.ensure_log_for_date(self.user["email"], today_str)
             logs = self.manager.load_file(self.manager.logs_file)
             today_log = logs.get(self.user["email"], {}).get(today_str)

         daily_calories = today_log.get("daily_calories", 0)

         food_calories = 0
         for meal in ["breakfast", "lunch", "dinner"] :
             items = today_log["food_log"].get(meal, [])
             for item in items :
                 food_calories += item["calories"]

         exercise_calories = 0
         for exc in today_log.get("exercise", []) :
             exercise_calories += exc.get("calories", 0)

         remaining  = daily_calories - food_calories + exercise_calories
         remaining = round(remaining, 2)
         self.calories_label.config(text=f"{daily_calories}     -      {food_calories}     +      {exercise_calories}      =    {remaining}")

         if remaining < 0 and self.previous_remaining_positive:
             messagebox.showwarning(
                 "Calories Warning",
                 "⚠️ Your remaining calories have become negative!\n"
                 "This means you have exceeded your daily calorie limit.\n"
                 "You should reduce your food intake or increase your exercise."
             )
             self.previous_remaining_positive = False
         elif remaining >= 0:
             self.previous_remaining_positive = True


     def refresh(self) :
         self.update_calories_data()
         for card in self.cards_list:
             card.update(current_date=self.current_date)

     def create_cards (self) :
         meals = [
             {
                 "title" : "Breakfast" ,
                 "bg":"#e0f7fa" ,
                 "meal_type" : "breakfast"
             },
             {
                "title": "Lunch",
                "bg": "#e0f7fa",
                "meal_type": "lunch"
             },
             {
                 "title": "Dinner",
                 "bg": "#e0f7fa",
                 "meal_type": "dinner"
             },
             {
                 "title":"Exercise",
                 "bg":"#e0f7fa",
                 "meal_type" : "exercise"
             },
             {
                 "title":"Water",
                 "bg":"#e0f7fa",
                 "meal_type" : "water"
             }
         ]
         self.cards_list = []
         for meal in meals :
             card = FoodCard (
                 parent = self.main_frame ,
                 title = meal["title"] ,
                 manager = self.manager ,
                 user_email=self.user["email"] ,
                 card_type = meal["meal_type"] ,
                 user = self.user ,
                 stack= self.stack
             )
             card.pack(padx = 30 , pady = 30 , fill='x')
             self.cards_list.append(card)

