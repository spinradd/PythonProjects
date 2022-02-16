import requests
import datetime as dt
import os

APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

nutrients_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# enter in parameters of the exercise performed
nutrient_params = {
    "query": "I biked 20 km last night in 60 minutes",
    "gender": "male",
    "weight_kg": 95,
    "height_cm": 184.88,
    "age": 23
}

# get back raw data from request
nutrient_req = requests.post(url=nutrients_endpoint, json=nutrient_params, headers=headers)

# write data from nutrients api to google sheet
sheety_endpoint = os.environ["sheet_url"]

# get current time (time of exercise)
date = dt.datetime.now().strftime("%m/%d/%Y")
time = dt.datetime.now().strftime("%H:%M:%S")

# get activity name, duration, and calories from query
activity_name = nutrient_req.json()["exercises"][0]["name"]
duration = nutrient_req.json()["exercises"][0]["duration_min"]
calories = nutrient_req.json()["exercises"][0]["nf_calories"]

# put data into json format
row_contents = {
    "sheet1": {
        "date": date,
        "time": time,
        "exercise": activity_name,
        "duration": duration,
        "calories": calories
    }}


username = os.environ["username"]
password = os.environ["password"]


# add row of exercise dat to google sheet
add_row = requests.post(url=sheety_endpoint, json=row_contents, auth=(username, password))
add_row.raise_for_status()
