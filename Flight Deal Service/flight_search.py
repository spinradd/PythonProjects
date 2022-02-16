import datetime as dt
from flight_data import FlightData1
import requests
from dateutil import parser


TEQUILA_END = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_API = {"apikey": YOUR_API_KEY}
HOME_AIRPORT_CODE = YOUR_AIRPORT_CODE

class FlightSearch:
    def __init__(self):
        self.one_week_out_fly_out = None
        self.six_month_out_fly_out = None
        self.get_flight_dates()
        self.tequila_endpoint = "https://tequila-api.kiwi.com/v2/search"
        self.destinations_to_check = []
        self.headers = {
            "apikey": YOUR_API_KEY,
        }
        self.tequila_params_to = {
            "fly_from": f"city:{HOME_AIRPORT_CODE}",
            "fly_to": "",
            "date_from": self.one_week_out_fly_out,
            "date_to": self.six_month_out_fly_out,
            "flight_type": "oneway",
            "max_stopovers": 0,
            "curr": "USD",
            "adults": 2,
            "sort": "price",
            "asc": 1,
            "limit": 50
        }
        self.tequila_params_back = {
            "fly_from": "",
            "fly_to": "fcity:{HOME_AIRPORT_CODE}",
            "date_from": "",
            "date_to": "",
            "flight_type": "oneway",
            "max_stopovers": 0,
            "curr": "USD",
            "adults": 2,
            "sort": "price",
            "asc": 1,
            "limit": 50
        }

    def update_city_codes(self, city_name):
        """search tequila api for city codes"""
        iata_params = {
            "term": city_name,
            "location_types": "city"
        }
        get_code = requests.get(url=TEQUILA_END, headers=TEQUILA_API, params=iata_params)
        try:
            code = get_code.json()["locations"][0]["code"]
        except IndexError:
            raise Exception(f"No City found for {city_name}")
        else:
            return code

    def update_airport_codes(self, city_name):
        """search tequila api for airport codes"""
        iata_params = {
            "term": city_name,
            "location_types": "airport"
        }
        get_code = requests.get(url=TEQUILA_END, headers=TEQUILA_API, params=iata_params)
        try:
            code = get_code.json()["locations"][0]["code"]
        except IndexError:
            raise Exception(f"No airport found in {city_name}")
        else:
            return code

    def get_flight_dates(self):
        """get flight date parameters for this search (today and 6 months from today)"""
        todays_date = dt.datetime.now()
        self.one_week_out_fly_out = todays_date + dt.timedelta(days=1)
        self.one_week_out_fly_out = self.one_week_out_fly_out.strftime("%d/%m/%Y")

        self.six_month_out_fly_out = dt.datetime.now() + dt.timedelta(weeks=26)
        self.six_month_out_fly_out = self.six_month_out_fly_out.strftime("%d/%m/%Y")

    def contact_tequila(self, flight_direction):
        """search for flights either outbound or inbound"""
        new_flight = requests.get(url=self.tequila_endpoint, params=flight_direction, headers=self.headers)
        new_flight.raise_for_status()
        return new_flight

    def search_for_flights(self, destinations):
        """entire trip function looks for forward flights and return flight seperately, round trip
        queries are less reliable"""

        #get forward flight
        self.tequila_params_to["fly_to"] = f"city:{destinations['iataCode']}"
        forward_flight = self.contact_tequila(self.tequila_params_to)
        try:
            forward_flight = forward_flight.json()["data"][0]
        except IndexError:
            print(f"No direct flights found from BOS to {destinations['location']}.")
            self.tequila_params_to["max_stopovers"] = 1
            forward_flight = self.contact_tequila(self.tequila_params_to)
            try:
                forward_flight = forward_flight.json()["data"][0]
            except IndexError:
                print(f"No flights from BOS to {destinations['location']} with 1 layover.")
                return None

        # if forward flights are found, specify window that return flights can be:
        # (7 days < time_in_foreign_city < 28 days)
        fly_back_date_min = parser.parse(forward_flight["route"][0]["local_departure"]) + dt.timedelta(days=7)
        fly_back_date_max = parser.parse(forward_flight["route"][0]["local_arrival"]) + dt.timedelta(days=28)
        fly_back_date_min = fly_back_date_min.strftime("%d/%m/%Y")
        fly_back_date_max = fly_back_date_max.strftime("%d/%m/%Y")

        # get return flight based on potential dates for stay in city
        self.tequila_params_back["fly_from"] = f"city:{destinations['iataCode']}"
        self.tequila_params_back["date_from"] = fly_back_date_min
        self.tequila_params_back["date_to"] = fly_back_date_max

        return_flight = self.contact_tequila(self.tequila_params_back)
        try:
            return_flight = return_flight.json()["data"][0]
        except IndexError:
            print(f"No direct flights found from {destinations['location']} to BOS.")
            self.tequila_params_back["max_stopovers"] = 1
            return_flight = self.contact_tequila(self.tequila_params_back)
            try:
                return_flight = return_flight.json()["data"][0]
            except IndexError:
                print(f"No flights from {destinations['location']} to BOS with 1 layover.")
                return None

        # if flights are to destination directly, initialize variables
        if forward_flight["route"][0]["cityTo"] == destinations['location']:
            via_city_f = "Direct"
        else:
            via_city_f = forward_flight["route"][0]["cityTo"]
        if return_flight["route"][0]["cityTo"] == "Boston":
            via_city_r = "Direct"
        else:
            via_city_r = return_flight["route"][0]["cityTo"]

        # create new trip - one forward flight and one return flight
        new_trip = FlightData1(
            price_f=forward_flight["price"],
            origin_city_f=forward_flight["cityFrom"],
            origin_airport_f=forward_flight["flyFrom"],
            destination_city_f=forward_flight["cityTo"],
            destination_airport_f=forward_flight["flyTo"],
            out_date_f=forward_flight["route"][0]["local_departure"].split("T")[0],
            stop_overs_f=self.tequila_params_to["max_stopovers"],
            via_city_f=via_city_f,

            price_r=return_flight["price"],
            origin_city_r=return_flight["cityFrom"],
            origin_airport_r=return_flight["flyFrom"],
            destination_city_r=return_flight["cityTo"],
            destination_airport_r=return_flight["flyTo"],
            return_date_r=return_flight["route"][0]["local_departure"].split("T")[0],
            stop_overs_r=self.tequila_params_back["max_stopovers"],
            via_city_r=via_city_r)

        return new_trip

