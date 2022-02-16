import requests

SHEETY_USERNAME = YOUR_SHEETY_USERNAME
SHEETY_PASSWORD = YOUR_SHEETY_PASSWORD
SHEETY_ENDPOINT = YOUR_GOOGLE_SHEET_URL


class UserManager:
    def __init__(self):
      self.users = {}

    def add_user(self):
        """if new user, add to google sheets"""
        is_valid_name = False
        first_name = input("\nPlease enter in your first name: ")
        last_name = input("\nPlease enter in your last name: ")
        confirm_email = False
        while not confirm_email:
            email = input("\nPlease enter in your email: ")
            confirm = input("\nPlease confirm your email: ")
            if email == confirm:
                confirm_email = True
            else:
                print("\nEmails did not match, try again: ")
        new_row = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        update = requests.post(url=SHEETY_ENDPOINT, json=new_row, auth=(SHEETY_USERNAME, SHEETY_PASSWORD))
        update.raise_for_status()

    def get_users(self):
        """pull usr dat from google sheets"""
        users_info = requests.get(url=SHEETY_ENDPOINT, auth=(SHEETY_USERNAME, SHEETY_PASSWORD))
        users_info.raise_for_status()
        self.users = users_info.json()["users"]
        return self.users
