import json
import os

FOOD_FILE = os.path.join(os.path.dirname(__file__), "..", "Food.json")

def load_foods():
    if not os.path.exists(FOOD_FILE):
        return {}
    with open(FOOD_FILE, "r") as f :
        try:
            return json.load(f)
        except json.JSONDecodeError :
            return {}

def save_foods(food) :
    with open(FOOD_FILE, "w") as f:
        json.dump(food, f, indent=4)


EXERCISE_FILE = os.path.join(os.path.dirname(__file__), "..", "ExercisePages", "Exercises.json")

def load_exercises():
    if not os.path.exists(EXERCISE_FILE):
        return {}
    with open(EXERCISE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_exercises(exercises):
    with open(EXERCISE_FILE, "w") as f:
        json.dump(exercises, f, indent=4)
