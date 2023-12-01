# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type
import os

import requests
import pandas as pd


BASE_URL = "https://www.find-court-tribunal.service.gov.uk"
OUTPUT_DIRECTORY = "test_2_output"
TIME_OUT = 5


def get_courts(postcode: str) -> dict:
    """calls the api and returns courts for the given address"""
    response = requests.get(
        f"{BASE_URL}/search/results.json?postcode={postcode}",
        timeout=TIME_OUT
    )
    json_obj = response.json()
    return json_obj


def get_desired_courts(desired_type: str, courts: list[dict]):
    """from the given courts, return the courts with the desired types"""
    desired_courts = []
    for court in courts:
        if desired_type in court["types"]:
            desired_courts.append(court)
    return desired_courts


def get_closest_court(courts: list[dict]) -> dict:
    """from a list of courts, return the court with the shortest distance"""
    shortest = 0
    position = 0
    for index, court in enumerate(courts):
        distance = court["distance"]
        if distance < shortest:
            shortest = distance
            position = index
    return courts[position]


def write_to_text_file(person: list, court: dict, file_path: str) -> None:
    """given a court, write the wanted details to an output file"""
    person_name = person[0]
    postcode = person[1]
    desire = person[2]
    court_name = court["name"]
    dx_number = court.get("dx_number")
    distance = court["distance"]
    with open(file_path, "a+", encoding="utf-8") as file:
        file.write("\n".join([
            f"Person: {person_name}",
            f"Postcode: {postcode}",
            f"Wanted Court: {desire}",
            f"Name of Court Found: {court_name}",
            f"DX Number (if applicable): {dx_number}",
            f"Distance: {distance}",
        ]) + "\n\n")


def main():
    """main logic of script"""
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    output_file_path = os.path.join(OUTPUT_DIRECTORY, "output.txt")

    data_frame = pd.read_csv("people.csv")
    people = data_frame.to_numpy()

    for person in people:
        postcode = person[1]
        court_type = person[2]
        courts_available = get_courts(postcode)
        courts_wanted = get_desired_courts(court_type, courts_available)
        closest_court = get_closest_court(courts_wanted)
        write_to_text_file(person, closest_court, output_file_path)


if __name__ == "__main__":
    main()
