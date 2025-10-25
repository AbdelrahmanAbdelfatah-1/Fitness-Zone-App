import json
from datetime import date

class Manager :

    def __init__(self , food_file = "Food.json" , users_file = "Users.json" , logs_file = "Logs.json" ) :

        self.food_file = food_file
        self.users_file = users_file
        self.logs_file = logs_file

    def load_file(self, file) :
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            return data
        except:
            return {}

    def save_file(self, file , data ) :
        with open(file, 'w') as f :
            json.dump(data, f, indent=4)

    def calculate_daily_calories ( self , goal , weekly_change , weight , height, age, gender, activity_level ) :

        if gender.lower() == "male" :
            bmr = int ( ( 10 * weight ) + (6.25 * height) - (5 * age) + 5 )
        elif gender.lower() == "female" :
            bmr = int ( (10 * weight) + (6.25 * height) - (5 * age) - 161 )

        activity_factors = {
            "inactive": 1.2,
            "moderately active": 1.55,
            "active": 1.725,
        }

        factor =  activity_factors.get(activity_level.lower())
        daily_calories = bmr * factor

        if goal.lower() == "lose weight" :
            daily_calories -= ( weekly_change * 3500 ) / 7
        elif goal.lower() == "gain weight" :
            daily_calories += ( weekly_change * 3500 ) / 7

        return daily_calories

    def add_food(self, user_email , food_name , grams , meal , current_date ) :

        food = self.load_file(self.food_file)
        logs = self.load_file(self.logs_file)
        users = self.load_file(self.users_file)

        calories_taken = (food[food_name]["calories"] * grams) / 100
        protein_taken = (food[food_name]["protein"] * grams) / 100
        carbs_taken = (food[food_name]["carbs"] * grams) / 100
        fat_taken = (food[food_name]["fat"] * grams) / 100

        if isinstance(users, list) :
            user_data = next((u for u in users if u.get("email") == user_email), None)
        else :
            user_data = users.get(user_email)

        if not user_data:
            return

        daily_calories = self.calculate_daily_calories(
            user_data["goal"],
            user_data["weekly_change"],
            user_data["weight"],
            user_data["height"],
            user_data["age"],
            user_data["gender"],
            user_data["activity"]
        )

        if user_email not in logs:
            logs[user_email] = {}
        if current_date not in logs[user_email]:
            logs[user_email][current_date] = {
                "daily_calories": daily_calories,
                "food_log": {"breakfast": [], "lunch": [], "dinner": []},
                "exercise": [],
                "water": []
            }

        logs[user_email][current_date]["food_log"][meal].append(
            {
                "food": food_name,
                "grams": grams,
                "calories": calories_taken,
                "protein": protein_taken,
                "carbs": carbs_taken,
                "fat": fat_taken
            }
        )

        self.save_file(self.logs_file, logs)

    def get_today(self, user_email , date ) :
        logs = self.load_file(self.logs_file)
        return logs.get(user_email, {}).get(date, None)

    def get_today_date(self) :
        return date.today()

    def ensure_log_for_date(self, user_email, date_str) :

        logs = self.load_file(self.logs_file)
        users = self.load_file(self.users_file)

        if isinstance(users, list) :
            user_data = next((u for u in users if u.get("email") == user_email), None)
        else :
            user_data = users.get(user_email)

        if not user_data:
            return

        daily_calories = self.calculate_daily_calories(
            user_data["goal"],
            user_data["weekly_change"],
            user_data["weight"],
            user_data["height"],
            user_data["age"],
            user_data["gender"],
            user_data["activity"]
        )

        if user_email not in logs :
            logs[user_email] = {}

        if date_str not in logs[user_email] :
            logs[user_email][date_str] = {
                "daily_calories": daily_calories ,
                "food_log": {"breakfast": [], "lunch": [], "dinner": []},
                "exercise": [],
                "water": []
            }
            self.save_file(self.logs_file, logs)

    def update_user(self, email, updated_user_data) :

        users = self.load_file(self.users_file)
        if isinstance(users, list) :
            for i, u in enumerate(users) :
                if u.get("email") == email :
                    users[i] = updated_user_data
                    break
            else :
                users.append(updated_user_data)

        elif isinstance(users, dict):
            users[email] = updated_user_data
        else:
            users = [updated_user_data]

        self.save_file(self.users_file, users)


