import tkinter as tk

class profile_page(tk.Toplevel) :
    def __init__(self, master, user, stack, manager ) :
        super().__init__(master)
        self.user = user
        self.stack = stack
        self.manager = manager

        self.Dark_Gray = "#111827"
        self.Charcoal_Gray = "#1F2937"
        self.Dark_Blue = "#004477"

        self.title("Profile")
        self.state("zoomed")
        self.configure(bg=self.Dark_Gray)

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

        main_frame = tk.Frame(scrollable_frame, bg=self.Dark_Gray , relief = 'raised' , bd = 2)
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)

        # header frame
        header_frame = tk.Frame(main_frame, bg=self.Dark_Gray)
        header_frame.pack(fill="x", expand=True)
        # back
        back_button = tk.Button(header_frame, text="Back", font=("Arial", 15, "bold"),
                                fg="white", bg = self.Dark_Gray , relief='flat', cursor='hand2',
                                activebackground="white", command=self.stack.pop)
        back_button.pack(side="left", padx=20, pady=20)
        # Title
        title = tk.Label(main_frame, text="User Profile", font=("Arial", 24, "bold"), fg="white", bg=self.Dark_Gray)
        title.pack(pady=20)

        # Info
        info_frame = tk.Frame(main_frame, bg=self.Charcoal_Gray, bd=2, relief="raised")
        info_frame.pack(pady=20, padx=20,fill="x")

        for key , value in self.user.items() :
            if key == "Account_status" or  key == "Temp_failed_tries" or key == "Lock_time" or key == "perm_failed_tries" :
                continue
            row = tk.Frame(info_frame, bg="#1F2937")
            row.pack(fill="x", pady=5, padx=10)
            tk.Label(row, text=key.title(), font=("Arial", 16), fg="white", bg="#1F2937").pack(side="left")
            tk.Label(row, text=str(value), font=("Arial", 16), fg="white", bg="#1F2937").pack(side="right")

        # Buttons
        btns = tk.Frame(main_frame, bg="#111827")
        btns.pack(pady=20)

        edit_btn = tk.Button(btns, text="Edit Info", font=("Arial", 16),
                             bg="#004477", fg="white", command=self.edit_info)
        edit_btn.pack(anchor='center', padx=10)

    def edit_info(self) :
        from ProfilePage.EditProfile import edit_profile_page
        p = edit_profile_page(self, self.user, self.stack, self.manager)
        self.stack.push(p)
