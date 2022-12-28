# import flask dependencies
import json

from flask import Flask, request
import requests
import pymongo
import certifi

ca = certifi.where()


with open('config.json') as file:
    params = json.load(file)['params']

# initialize the flask app
app = Flask(__name__)

client = pymongo.MongoClient(params['cliente_url'])
db = client[params['db']]


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    query_result = req.get('queryResult')
    response = ""
    destination = ""

    # Set the origin and destination for the route
    origin = 'Bobrova,Ljubljana'
    print("neki")

    if query_result.get('action') == "get.naslov":
        destination = query_result.get("queryText") + ",Ljubljana"

        if getWeather() == "Thunderstorm":
            # use bus or drive
            text = "it looks like a Thunderstorm, i recommend to drive today\n"
            list = getBus(origin, destination, 3)

            start = " This is your start destiation: " + list[0].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            end = " This is your end destiation: " + list[1].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            list.pop(0)
            list.pop(1)

            result = ""

            for i, element in enumerate(list):
                if i % 2!=0:
                    number = "distance "
                else:
                    number = f"{i + 1}."

                result += number+f"{element}\n"

            response = text+"\n" + start+"\n" + end+"\n" +"\n"+ result+"\n"


        if getWeather() == "Drizzle":
            # use bus
            bus2 = ""
            bus3 = ""
            list = getBus(origin, destination, 1)
            start = " This is your start destiation: " + list[0].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            end = " This is your end destiation: " + list[1].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            bus1 = " 1. bus " + list[2]

            if len(list) == 4:
                bus2 = " 2. bus " + list[3]
            if len(list) == 5:
                bus3 = " 3. bus " + list[4]
            response = start + "\n" + end + "\n" + bus1 + "\n" + bus2 + "\n" + bus3 + "\n"

        if getWeather() == "Rain":
            # use bus

            bus2 = ""
            bus3 = ""
            list = getBus(origin, destination, 1)
            start = " This is your start destiation: " + list[0].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            end = " This is your end destiation: " + list[1].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            bus1 = " 1. bus " + list[2]

            if len(list) == 4:
                bus2 = " 2. bus " + list[3]
            if len(list) == 5:
                bus3 = " 3. bus " + list[4]
            response = start + "\n" + end + "\n" + bus1 + "\n" + bus2 + "\n" + bus3 + "\n"

        if getWeather() == "Snow":
            # use bus or drive
            text = "it looks like a snowy day i recommend to drive today\n"
            list = getBus(origin, destination, 3)
            start = " This is your start destiation: " + list[0].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            end = " This is your end destiation: " + list[1].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            list.pop(0)
            list.pop(1)

            result = ""

            for i, element in enumerate(list):
                if i % 2!=0:
                    number = "distance "
                else:
                    number = f"{i + 1}."

                result += number+f"{element}\n"

            response = text+"\n" + start+"\n" + end+"\n" +"\n"+ result+"\n"

        if getWeather() == "Clear":
            # Walk if it's not that far away
            list = getBus(origin, destination, 2)
            text = "it looks like a clear day a walk, will be the most optimal choice\n"

            start = " This is your start destiation: " + list[0].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            end = " This is your end destiation: " + list[1].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            list.pop(0)
            list.pop(1)

            result = ""

            for i, element in enumerate(list):
                if i % 2!=0:
                    number = "distance "
                else:
                    number = f"{i + 1}."

                result += number+f"{element}\n"

            response = text+"\n" + start+"\n" + end+"\n" +"\n"+ result+"\n"

        if getWeather() == "Clouds":
            # Walk if it's not that far away
            text = "it looks like a clear day a walk, will be the most optimal choice\n"
            list = getBus(origin, destination, 2)

            start = " This is your start destiation: " + list[0].replace("1000 Ljubljana, Slovenia", "Ljubljana")
            end = " This is your end destiation: " + list[1].replace("1000 Ljubljana, Slovenia", "Ljubljana")

            list.pop(0)
            list.pop(1)

            result = ""

            for i, element in enumerate(list):
                if i % 2!=0:
                    number = "distance "
                else:
                    number = f"{i + 1}."

                result += number+f"{element}\n"

            response = text+"\n" + start+"\n" + end+"\n" +"\n"+ result+"\n"

        print(response)

        query = req['queryResult']['queryText']
        result = req['queryResult']['fulfillmentText']

        data = {'query': query,
                'result': result,
                'response':response}

        col = db['chat_data']
        col.insert_one(data)

    return {
        "fulfillmentText": response,
        "source": "webhookdata"
    }


def getBus(origin, destination, type):
    # Google API key
    api_key = 'AIzaSyDI2zzupi7vJWjgc5JvD-z3vumGdpsAqbg'
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

    if type == 1:
        mode = 'transit'
        transit_mode = 'bus'
        nav_request = 'origin={}&destination={}&transit_mode={}&mode={}&key={}'.format(origin, destination,
                                                                                       transit_mode, mode, api_key)
        url = endpoint + nav_request
        response = requests.get(url)
        data = json.loads(response.text)
        list = getInstructions_bus(data)

    if type == 2:
        mode = 'walking'
        transit_mode = 'walking'
        nav_request = 'origin={}&destination={}&transit_mode={}&mode={}&key={}'.format(origin, destination,
                                                                                       transit_mode, mode, api_key)
        url = endpoint + nav_request
        response = requests.get(url)
        data = json.loads(response.text)
        list = getInstructions_walking(data)

    if type == 3:
        mode = 'DRIVING'
        transit_mode = 'DRIVING'
        nav_request = 'origin={}&destination={}&transit_mode={}&mode={}&key={}'.format(origin, destination,
                                                                                       transit_mode, mode, api_key)
        url = endpoint + nav_request
        response = requests.get(url)
        data = json.loads(response.text)
        list = getInstructions_driving(data)

    return list


def getInstructions_bus(data):
    journey = []

    for route in data["routes"]:
        for leg in route["legs"]:
            start_address = leg["start_address"]
            end_address = leg["end_address"]
            journey.append(start_address)
            journey.append(end_address)
            for step in leg["steps"]:
                if step["travel_mode"] == "TRANSIT":
                    busNumber = step["transit_details"]["line"]["short_name"]
                    journey.append(busNumber)
    return journey


def getInstructions_walking(data):
    journey = []

    for route in data["routes"]:
        for leg in route["legs"]:
            start_address = leg["start_address"]
            end_address = leg["end_address"]
            journey.append(start_address)
            journey.append(end_address)
            for step in leg["steps"]:
                print(step)
                if step["travel_mode"] == "WALKING":
                    html_instructions = step["html_instructions"].replace("<b>", "")
                    html_instructions = html_instructions.replace("/<wbr/>","")
                    html_instructions = html_instructions.replace("</div>","")
                    html_instructions = html_instructions.replace("<div style=","")
                    journey.append(html_instructions.replace("</b>", ""))
                    distance = step["distance"]["text"]
                    journey.append(distance)
    return journey


def getInstructions_driving(data):
    journey = []

    for route in data["routes"]:
        for leg in route["legs"]:
            start_address = leg["start_address"]
            end_address = leg["end_address"]
            journey.append(start_address)
            journey.append(end_address)
            for step in leg["steps"]:
                print(step)
                if step["travel_mode"] == "DRIVING":
                    html_instructions = step["html_instructions"].replace("<b>", "")
                    journey.append(html_instructions.replace("</b>", ""))
                    html_instructions = html_instructions.replace("/<wbr/>", "")
                    html_instructions = html_instructions.replace("</div>", "")
                    html_instructions = html_instructions.replace("<div style=", "")
                    journey.append(html_instructions.replace("</b>", ""))
                    distance = step["distance"]["text"]
                    journey.append(distance)
    return journey


def getWeather():
    # Set the API endpoint URL and your API key
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "f48e25f442b2b9290f9dcde8542d814c"
    Weather_description = ""
    Weather_main = ""
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
            # Weather_description = item['description']
            #Weather_main = item['main']
            Weather_main = "Drizzle"
    else:
        # If the request was unsuccessful, print an error message
        print("An error occurred:", response.status_code)

    return Weather_main


# run the app
if __name__ == '__main__':
    app.run()
