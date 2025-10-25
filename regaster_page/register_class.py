class User :
    def __init__(self, name, email, password, age, gender, height, weight,
                 goal, activity, weekly_change, Account_status=True, Temp_failed_tries=0, perm_failed_tries=0,
                 Lock_time=None , state = "user" ) :
        self.state = state
        self.name = name
        self.email = email
        self.password = password
        self.age = int(age)
        self.gender = gender
        self.height = float(height)
        self.weight = float(weight)
        self.goal = goal
        self.activity = activity
        self.weekly_change = float(weekly_change)
        self.Account_status = Account_status
        self.Temp_failed_tries = int(Temp_failed_tries) if Temp_failed_tries is not None else 0
        self.perm_failed_tries = int(perm_failed_tries) if perm_failed_tries is not None else 0
        self.Lock_time = int(Lock_time) if Lock_time is not None else 0

    def to_dict(self) :
        return {
            "state": self.state,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "goal": self.goal,
            "activity": self.activity,
            "weekly_change": self.weekly_change,
            "Account_status": self.Account_status,
            "Temp_failed_tries": self.Temp_failed_tries,
            "perm_failed_tries": self.perm_failed_tries,
            "Lock_time": self.Lock_time,
        }