import tkinter as tk

class exercise_page_1(tk.Toplevel) :

    def __init__(self , master , user , stack , manager ) :
        super().__init__(master)

        self.master = master
        self.user = user
        self.stack = stack
        self.manager = manager

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.title("Exercise Page")
        self.state('zoomed')
        self.configure(bg=self.Dark_Gray)

        self.create_widgets()

    def create_widgets(self) :
        # Header frame
        header_frame = tk.Frame(self, bg=self.Dark_Gray)
        header_frame.pack(fill="x", side="top", padx=20, pady=10)

        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Arial", 18, "bold"),
            bg=self.Dark_Gray,
            fg="white",
            relief="flat",
            bd=0,
            activebackground=self.Dark_Gray,
            activeforeground="white",
            command = self.stack.pop
        )
        back_btn.pack(side="left",padx=30, pady=30)
        # Title
        tk.Label(self, text = 'Choose One', font  = ( 'Arial' , 35 , 'bold' ) ,
                        bg  = self.Dark_Gray , fg = 'white' ).pack(pady=50)

        main_frame = tk.Frame( self , bg = self.Dark_Gray , relief='raised', bd=3 )
        main_frame.pack(fill='both', expand=True, padx=60, pady=60)

        main_frame.grid_columnconfigure(0, weight=1)  # left
        main_frame.grid_columnconfigure(1, weight=1)  # right
        main_frame.grid_rowconfigure(0, weight=1)

        # left frame
        left_frame = tk.Frame(main_frame, bg=self.Dark_Blue, relief='raised', bd=2)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        # right frame
        right_frame = tk.Frame(main_frame, bg=self.Dark_Blue, relief='raised', bd=2)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=50, pady=50)

        # Cardio button
        cardio_btn = tk.Button(left_frame, text = "Cardio" , font=("Arial", 35, 'bold'),bg = self.Dark_Blue , fg="white",
                relief='flat',bd=0,width=15,height=5,activebackground=self.Dark_Blue
                  ,activeforeground="white" , command = self.go_cardio)
        cardio_btn.pack(expand=True, pady=5)

       # Strength button
        strength_btn = tk.Button(right_frame, text="Strength", font=("Arial", 35, 'bold'), bg=self.Dark_Blue, fg="white",
                           relief='flat', bd=0, width=15, height=5, activebackground=self.Dark_Blue
                           , activeforeground="white",command = self.go_strength)
        strength_btn.pack(expand=True, pady=5)

    def go_cardio(self) :
        from ExercisePages.ExercisePage_2 import exercise_page_2
        e = exercise_page_2 (self,"Cardio",self.user,self.stack,self.manager)
        e.stack.push(e)

    def go_strength(self) :
        from ExercisePages.ExercisePage_2 import exercise_page_2
        e = exercise_page_2(self, "Strength", self.user, self.stack, self.manager)
        e.stack.push(e)
