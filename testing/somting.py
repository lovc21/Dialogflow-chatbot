def getInstructions(data):
    journey = []

    for route in data["routes"]:
        for leg in route["legs"]:
            for step in leg["steps"]:
                for smallStep in step["steps"]:
                    if smallStep["travel_mode"] == "TRANSIT":

                        busNumber = smallStep["distance"]["maneuver"]["html_instructions"]
                        journey.append("TRANSIT")
                        journey.append(busNumber)

                    if smallStep["travel_mode"] == "WALKING":
                        journey.append("WALKING")

                        walkingStepst = smallStep["transit_details"]["line"]["short_name"]
                        journey.append(walkingStepst)

                    if smallStep["travel_mode"] == "DRIVING":
                        journey.append("DRIVING")
                        drivingStepts = smallStep["distance"]["maneuver"]["html_instructions"]
                        journey.append(drivingStepts)