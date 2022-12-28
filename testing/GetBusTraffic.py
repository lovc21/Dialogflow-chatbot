import json
import requests
import geocoder
from geopy.geocoders import Nominatim


def getbus(origin, destination):
    # Replace YOUR_API_KEY with your actual API key

    geolocator = Nominatim(user_agent="geoapiExercises")

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyDI2zzupi7vJWjgc5JvD-z3vumGdpsAqbg'

    g = geocoder.ip('me')
    location = geolocator.reverse(g.latlng)

    # Set the origin and destination for the route

    # Set the mode of transportation to 'transit' and the desired transit mode to 'bus'
    mode = 'walking'
    transit_mode = 'walking'

    nav_request = 'origin={}&destination={}&transit_mode={}&mode={}&key={}'.format(origin, destination, transit_mode,
                                                                                   mode, api_key)
    request = endpoint + nav_request
    # Make the request to the API

    # response = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin=%7B{origin}%7D&{destination}=%7Bdestination%7D&{mode}=%7Bmoden%7D&{transit_mode}=%7B{transit_mode}%7D&key=%7B{api_key}%7D%27)')
    response = requests.get(request)

    # Print the response from the API
    data = json.loads(response.text)



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
                    html_instructions = step["html_instructions"].replace("<b>","")
                    journey.append(html_instructions.replace("</b>",""))
                    distance = step["distance"]["text"]
                    journey.append(distance)
                #for smallStep in step["steps"]:
                    #if smallStep["travel_mode"] == "TRANSIT":
                        #busNumber = smallStep["distance"]["maneuver"]["html_instructions"]
                        #journey.append("TRANSIT")
                        #journey.append(busNumber)

                    #if smallStep["travel_mode"] == "WALKING":
                        #journey.append("WALKING")

                        #walkingStepst = smallStep["transit_details"]["line"]["short_name"]
                        #journey.append(walkingStepst)

                    #if smallStep["travel_mode"] == "DRIVING":
                        #journey.append("DRIVING")
                        #drivingStepts = smallStep["distance"]["maneuver"]["html_instructions"]
                        #journey.append(drivingStepts)
    print(journey)
    # for item in data:
    # print(item['currency'])



if __name__ == '__main__':
    origin = "P+R Dolgi most, Dolgi most, 1000 Ljubljana"
    destination = 'Letaliska, 1000 Ljubljana'
    getbus(origin, destination)
