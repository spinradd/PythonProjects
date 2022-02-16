import requests
from datetime import datetime, timezone
import smtplib
import re
import json
import time
MY_LAT = float("Your Lattitude")
MY_LONG = float("Your Longitude")
GMAIL = "Your email@gmail.com"
PASSWORD = "Your password"


def is_iss_overhead():
    """check if ISS is overhead"""
    response_ISS = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_ISS.raise_for_status()
    longitude = float(response_ISS.json()["iss_position"]["longitude"])
    latitude = float(response_ISS.json()["iss_position"]["latitude"])
    if 5 >= latitude - MY_LAT >= -5 and 5 >= longitude - MY_LONG >= -5:
        return True
    else:
        return False


def is_dark():
    """check to see if its dark outside (so you can see the ISS)"""
    today = datetime.now(timezone.utc)
    date_today = today.strftime("%Y-%m-%d")

    parameters = {"lat": MY_LAT,
                  "lng": MY_LONG,
                  'date': date_today,
                  "formatted": 0
                  }
    response_SS = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response_SS.raise_for_status()
    sunrise = int(response_SS.json()["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(response_SS.json()["results"]["sunset"].split("T")[1].split(":")[0])

    if sunrise >= today.hour >= sunset:
        return True
    else:
        return False


def send_email(to=None, by=None, message=None, ):
    """send email"""
    domain = re.split("\.|@", by)
    try:
        with open("email_apis.json", "r") as data_file:
            domains = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        raise Exception(FileNotFoundError)
    domain_is_present = False
    for section in domain:
        if section in domains:
            domain = section
            domain_is_present = True
    if not domain_is_present:
        raise Exception("Domain does not exist (gmail, yahoo, outlook)")

    with smtplib.SMTP(domains[domain]["host"], port=domains[domain]["port"]) as connection:
        connection.starttls()
        connection.login(user=by, password=PASSWORD)
        connection.sendmail(from_addr=by,
                            to_addrs=to,
                            msg=message)

while True:
    time.sleep(60*30)
    if __name__ == "__main__":
        if not is_iss_overhead() and not is_dark():
            send_email(to="spinradd@gmail.com", by=GMAIL, message="Subject: ISS\n\nLook Up!" )


