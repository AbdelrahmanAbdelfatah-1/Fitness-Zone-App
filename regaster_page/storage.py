import json
import os
from regaster_page.register_class import User
from datetime import datetime
from FitnessManeger import Manager

user_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Users.json")
logs_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logs.json")


def load_users():
    try :
        with open(user_file, "r") as file:
                data = json.load(file)
                return [User(
                    u["name"],
                    u["email"],
                    u["password"],
                    int(u["age"]),
                    u["gender"],
                    float( u["height"]),
                    float(u["weight"]),
                    u["goal"],
                    u["activity"],
                    float(u["weekly_change"]) ,
                    state=u.get("state", "user")
                ) for u in data]
    except:
        return []
def save_users(users):
    with open(user_file, "w") as file:
        data = []
        for u in users:
            data.append(u.to_dict())
        json.dump(data, file, indent=4)

def create_user_log(user) :
    if user["email"] == "admin@admin.com":
        return False
    m = Manager()
    logs = m.load_file(logs_file)
    if logs is None:
        logs = {}
    cal = m.calculate_daily_calories(
        user["goal"],
        user["weekly_change"],
        user["weight"],
        user["height"],
        user["age"],
        user["gender"],
        user["activity"]
    )
    if user["email"] not in logs :
        today = datetime.now().strftime("%Y-%m-%d")
        logs[user["email"]] = {
            today : {
                "daily_calories": cal ,
                "food_log": {
                    "breakfast": [],
                    "lunch": [],
                    "dinner": []
                },
                "exercise": [],
                "water": []
            }
        }
        m.save_file(logs_file,logs)
        return True
    return False
