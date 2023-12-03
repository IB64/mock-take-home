import re


def validate_numbers(time: str) -> None:
    """validates the time string to see if it fits the format HH:MM:SS
    otherwise raises an error"""
    pattern = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
    if not re.match(pattern, time):
        raise ValueError("Invalid format")


def sum_current_time(time_str: str) -> int:
    """Sums the numbers of a time in the format HH:MM:SS
    e.g. 12:30:45 == 87"""

    if not isinstance(time_str, str):
        raise TypeError("Invalid input type")
    validate_numbers(time_str)

    list_of_nums = time_str.split(":")

    return sum(int(num) for num in list_of_nums)
