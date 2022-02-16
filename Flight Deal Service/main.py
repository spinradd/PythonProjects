#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from get_new_users import UserManager

USERNAME = YOUR_USERNAME
PASSWORD = YOUR_PASSWORD
HOME_AIRPORT = AIRPORT_CODE #ex: "ABC"
RECIPIENT_EMAIL = YOUR_EMAIL

# initialize classes
data_manager = DataManager()

# get destination data from google sheets
data_manager.destinations_data = data_manager.get_destination_data()

flight_search = FlightSearch()
notification_manager = NotificationManager()
users = UserManager()

# assume all destinations have valid airport codes
updates_needed_city = False
updates_needed_airport = False

# for each destination, if there is no destination code search for city and input airport code in json format
for row in range(0, len(data_manager.destinations_data)):
    if data_manager.destinations_data[row]["iataCode"] == "":
        city_code = flight_search.update_city_codes(data_manager.destinations_data[row]["location"])
        data_manager.destinations_data[row]["iataCode"] = city_code
        updates_needed_city = True

# update new airport codes to google sheet
if updates_needed_city:
    data_manager.update_new_codes()

# for each city in destinations search for potential flights based on specified parameters
for city in data_manager.destinations_data:

    # search for trip, if trip found return FlightDeal
    potential_trip = flight_search.search_for_flights(city)

    # if trip, see if it is within specified budget
    if potential_trip:

        # if forward flight and return flight are within budget, ...
        if potential_trip.price_f + potential_trip.price_r < city["lowestPrice"]:
            link = (f"https://www.kiwi.com/deep?"
                    f"affilid=davidspinradflightlink&"
                    f"adults=2&"
                    f"children=0&c"
                    f"currency=USD&"
                    f"departure={potential_trip.out_date_f}_{potential_trip.out_date_f}&"
                    f"destination={potential_trip.destination_airport_f}&"
                    f"infants=0&"
                    f"lang=en&"
                    f"origin={potential_trip.origin_airport_f}&"
                    f"sortBy=prices&"
                    f"return=no-return&"
                    f"stopNumber=1&")

            # if there are no stop over flights within trip plan message specified email
            if potential_trip.stop_overs_f == 0 and potential_trip.stop_overs_r == 0:

                message_txt = (
                    f"Subject: Flight Opportunities!!\n\n"
                    f"Round Trip: {potential_trip.origin_city_f} -> {potential_trip.destination_city_f}\n"
                    f"Departure: {potential_trip.out_date_f} Return: {potential_trip.return_date_r} for ${potential_trip.price_f}"
                    f"{link}")

                send_email = NotificationManager.send_email(to=RECIPIENT_EMAIL, message=message_txt)

            # if there are stop over flights, change message accordingly
            else:
                departure_link = (f"https://www.kiwi.com/deep?"
                        f"affilid=davidspinradflightlink&"
                        f"adults=2&"
                        f"children=0&c"
                        f"currency=USD&"
                        f"departure={potential_trip.out_date_f}_{potential_trip.out_date_f}&"
                        f"destination={potential_trip.destination_airport_f}&"
                        f"infants=0&"
                        f"lang=en&"
                        f"origin={potential_trip.origin_airport_f}&"
                        f"return=no-return&"
                        f"sortBy=prices&"
                        f"stopNumber=1&")
                return_link = (f"https://www.kiwi.com/deep?"
                        f"affilid=davidspinradflightlink&"
                        f"adults=2&"
                        f"children=0&c"
                        f"currency=USD&"
                        f"departure={potential_trip.return_date_r}_{potential_trip.return_date_r}&"
                        f"destination={potential_trip.destination_airport_r}&"
                        f"infants=0&"
                        f"lang=en&"
                        f"origin={potential_trip.origin_airport_r}&"
                        f"return=no-return&"
                        f"sortBy=prices&"
                        f"stopNumber=1&")
                message_txt = (
                    f"Subject: Flight Opportunities!!\n\n"
                    f"Flight: {potential_trip.origin_city_f} -> {potential_trip.destination_city_f}\n"
                    f"Departure: {potential_trip.out_date_f} via {potential_trip.via_city_f} for ${potential_trip.price_f}\n"
                    f"Link: {departure_link}"
                    f"Return: {potential_trip.origin_city_r} -> {potential_trip.destination_city_r}\n"
                    f"Departure: {potential_trip.return_date_r} via {potential_trip.via_city_r} for ${potential_trip.price_r}\n"
                    f"Link: {return_link}")

                send_email = NotificationManager.send_email(to=RECIPIENT_EMAIL, message=message_txt)

        else:
            print(f"Too expensive for {city['location']}, current cost is ${potential_trip.price_f + potential_trip.price_r}")













