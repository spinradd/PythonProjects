import requests

SHEETY_USERNAME = YOUR_SHEETY_USERNAME
SHEETY_PASSWORD = YOUR_SHEETY_PASSWORD
SHEETY_ENDPOINT = SHEETY_URL


class DataManager:
    def __init__(self):
      self.destinations_data = {}

    def get_destination_data(self):
        """get destination city names from sheety api"""
        row_req = requests.get(url=SHEETY_ENDPOINT, auth=(SHEETY_USERNAME, SHEETY_PASSWORD))
        row_req.raise_for_status()
        self.destinations_data = row_req.json()["destinations"]
        return self.destinations_data

    def update_new_codes(self):
        """for each row in destinations data, update airport/destination code with code stored in data manager"""
        row= 1
        for city in self.destinations_data:
            row += 1
            print(city)
            updated_row = {
                "destinations": {
                    "iataCode": city["iataCode"]
                }
            }
            update = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=updated_row,
                                  auth=(SHEETY_USERNAME, SHEETY_PASSWORD))
            update.raise_for_status()

