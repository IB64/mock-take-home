import os

import requests
import pandas as pd

# base url for the api
BASE_URL = "https://www.find-court-tribunal.service.gov.uk"
# folder to store output
OUTPUT_DIRECTORY = "test_2_output"
# timeout, in seconds, to call a get request to the api
TIME_OUT = 5


def get_courts(postcode: str) -> dict:
    """calls the api and returns courts for the given address"""
    response = requests.get(
        f"{BASE_URL}/search/results.json?postcode={postcode}",
        timeout=TIME_OUT
    )
    json_obj = response.json()
    return json_obj


def get_desired_courts(desired_type: str, courts: list[dict]) -> list:
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


def main() -> None:
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
