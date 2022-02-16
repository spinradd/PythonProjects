import smtplib
import os
import random
import pandas
import datetime as dt
import re
import json

def check_birthdays():
    """import birthday information from birthdays csv, return """
    birthdays = pandas.read_csv("birthdays.csv")
    today = dt.datetime.now()
    birthdays_today = birthdays[(birthdays["month"] == today.month) & (birthdays['day'] == today.day)]
    return birthdays_today

def send_email(to=None, by=None, message=None, ):
    """send email based on chosen domain"""
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
        connection.login(user=by, password=password)
        connection.sendmail(from_addr=by,
                            to_addrs=to,
                        msg=f"Subject: Happy Birthday!\n\n{message}")



if __name__=="__main__":

    # get birthdays today
    out_going_mail = check_birthdays()
    gmail = "Your Email@gmail.com"
    password = "Your Password"

    #for each birthday create template and send email
    for key, row in out_going_mail.iterrows():
        random_letter = random.choice(os.listdir("letter_templates"))
        random_letter = f"letter_templates/{random_letter}"

        with open(random_letter, "r") as letter_file:
            template = letter_file.read()
            letter = template.replace("[NAME]", row["name"])

        send_email(row["email"], gmail, letter)



