import json
import requests


def getWeather():
    # Set the API endpoint URL and your API key
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "f48e25f442b2b9290f9dcde8542d814c"

    # Set the city and country code for the location you want to get the weather for
    city = "Ljubljana"
    country_code = "SI"

    # Set the API parameters
    params = {
        "q": f"{city},{country_code}",
        "units": "metric",
        "appid": api_key,
    }

    # Make the API request
    response = requests.get(endpoint, params=params)

    # Check the status code of the response
    if response.status_code == 200:
        # If the request was successful, print the weather data
        data = json.loads(response.text)
        data_main = data['weather']
        for item in data_main:
            Weathe_description = item['description']
            Weathe_main = item['main']
            print(Weathe_main)

    else:
        # If the request was unsuccessful, print an error message
        print("An error occurred:", response.status_code)


if __name__ == '__main__':
    getWeather()