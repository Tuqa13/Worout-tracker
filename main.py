
import requests
from datetime import datetime
import os

# Login data:

GENDER = "female"
WEIGHT = 62.5
HEIGHT = 167.5
AGE = 20


APP_ID = os.environ["91b4b00c"]
APP_KEY = os.environ["6e63bb48271d56a9c265f22a5976843d	—"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_ENDPOINT = os.environ["https://api.sheety.co/074981b5bb33a1c35a03738e43db432d/myWorkouts/workouts"]

exercise_text = input("Tell me which exercises you did today: ")

exercise_body = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

header = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

response = requests.post(exercise_endpoint,
                         json=exercise_body,
                         headers=header).json()["exercises"]



for i in range(len(response)):
    sheety_data = {
        "workout": {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": response[i]["name"].title(),
            "duration": response[i]["duration_min"],
            "calories": response[i]["nf_calories"]
        }
    }

    bearer_headers = {
        "Authorization": f"Bearer {os.environ['TOKEN']}"
    }

    sheety_response = requests.post(os.environ.get(SHEET_ENDPOINT),
                                    json=sheety_data,
                                    headers=bearer_headers)
    print(sheety_response.text)

