import requests

# get quiz questions from website
request_params = {"amount":100, "type":"boolean"}
api_request = requests.get("https://opentdb.com/api.php", params=request_params)
api_request.raise_for_status()

# store results as json
question_data = api_request.json()["results"]