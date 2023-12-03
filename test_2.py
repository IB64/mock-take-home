"""script to run task 2"""
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
    """from a list of courts, return the court with the shortest distance.
    If "distance" key is not found, then return an empty list"""
    shortest = float("inf")
    position = -1
    for index, court in enumerate(courts):
        # if no distance key, continue
        try:
            distance = court["distance"]
        except KeyError:
            continue
        if distance < shortest:
            shortest = distance
            position = index

    # if no courts with "distance" key is found, return empty dict
    if position < 0:
        return {}
    return courts[position]


def write_to_text_file(file_path: str, message: str):
    """write to .txt file"""
    with open(file_path, "a+", encoding="utf-8") as file:
        file.write(message)


def write_success(person: list, court: dict, file_path: str) -> None:
    """write the necessary details for a successful search"""
    person_name = person[0]
    postcode = person[1]
    desire = person[2]
    court_name = court["name"]
    dx_number = court.get("dx_number")
    distance = court["distance"]
    message = "\n".join([
        f"Person: {person_name}",
        f"Postcode: {postcode}",
        f"Wanted Court: {desire}",
        f"Name of Court Found: {court_name}",
        f"DX Number (if applicable): {dx_number}",
        f"Distance: {distance}",
    ]) + "\n\n"
    write_to_text_file(file_path, message)


def write_no_court_found(person: list, file_path: str):
    """write the message where no courts are found for a person"""
    person_name = person[0]
    postcode = person[1]
    desire = person[2]
    message = "\n".join([
        f"No court found for: {person_name}",
        f"Postcode: {postcode}",
        f"Wanted Court: {desire}"
    ]) + "\n\n"
    write_to_text_file(file_path, message)


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

        if not courts_available or not courts_wanted or not closest_court:
            write_no_court_found(person, output_file_path)
        else:
            write_success(person, closest_court, output_file_path)


if __name__ == "__main__":
    main()
