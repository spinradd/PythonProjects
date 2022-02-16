import requests
import datetime as dt
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

API_KEY = YOUR_API_KEY
account_sid = YOUR_ACCOUNT_ID
auth_token = YOUR_AUTH_TOKEN
from_number = YOUR_PAID_FOR_NUMBER
CELL = YOUR_CELL_NUMBER
params = {
    "lat": YOUR_LATTITUDE,
    "lon": YOUR_LATTITUDE,
    "units": "imperial",
    "exclude": "daily,minutely,current",
    "appid": YOUR_APP_ID
}

# get weather information from your location
weather_re = requests.get(f'https://api.openweathermap.org/data/2.5/onecall', params)
weather_re.raise_for_status()

# convert weather to json format
hourly_list = weather_re.json()["hourly"]
hour = 0

# scan weather for the next twelve hours
while hour < 12:

    #if weather api code is < 700 --> it will rain
    if int(hourly_list[hour]["weather"][0]["id"]) < 700:

        # initialize twilio client
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ['https_proxy']}

        # get time of bad weather (UTC), convert to AM/PM
        proj_time = int(hourly_list[hour]["dt"])
        proj_time = dt.datetime.fromtimestamp(proj_time)
        proj_time = dt.datetime.strptime(f"{proj_time.hour}:00", "%H:%M")
        proj_time = proj_time.strftime("%I:%M %p")

        # text message to your cell phone
        client = Client(account_sid, auth_token, http_client=proxy_client)
        message = client.messages \
            .create(
            body=f"Bring an Umbrella. It will rain starting at {proj_time}",
            from_=from_number,
            to=f"={CELL}")
        print(message.status)
        hour += 1

        # breaks at the earliest hour of bad weather
        break
    hour += 1


