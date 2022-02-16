from twilio.rest import Client
import smtplib
import json
import re

TWILIO_SID = YOUR_TWILIO_SID
TWILIO_AUTH_TOKEN = YOUR_TWILIO_AUTH
TWILIO_VIRTUAL_NUMBER = YOUR_RECIPIENT_NUMBER
TWILIO_VERIFIED_NUMBER = YOUR_TWILIO_CREATED_NUMBER

GMAIL = YOUR_SENDER_EMAIL
PASSWORD = YOUR_EMAIL_PASSWORD


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        """send sms message"""
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_email(self, to=None, by=GMAIL, message=None):
        """send email"""
        domain = re.split("\.|@", by)
        try:
            with open("email_apis.json", "r") as data_file:
                domains = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            raise Exception(FileNotFoundError)

        # checks to see if email used it one of gmail, yahoo, or outlook
        domain_is_present = False
        for mail_services in domain:
            if mail_services in domains:
                domain = mail_services
                domain_is_present = True
        if not domain_is_present:
            raise Exception("Domain does not exist (gmail, yahoo, outlook)")

        with smtplib.SMTP(domains[domain]["host"], port=domains[domain]["port"]) as connection:
            connection.starttls()
            connection.login(user=by, password=PASSWORD)
            connection.sendmail(from_addr=by,
                                to_addrs=to,
                                msg=message)