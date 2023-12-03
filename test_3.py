def validate_numbers(numbers: list):
    """Validates data in the format HH:MM:SS"""

    if len(numbers) != 3:
        raise ValueError("Invalid number of components")
    for num in numbers:
        if not num.isnumeric():
            raise ValueError("Non numeric value detected")
    hour = numbers[0]
    minutes = numbers[1]
    seconds = numbers[2]
    if int(hour) not in range(24):
        raise ValueError("Hour value too large")
    if int(minutes) not in range(60):
        raise ValueError("Minute value too large")
    if int(seconds) not in range(60):
        raise ValueError("Second value too large")
    if len(hour) != 2 or len(minutes) != 2 or len(seconds) != 2:
        raise ValueError("Invalid format")


def sum_current_time(time_str: str) -> int:
    """Sums the numbers of a time in the format HH:MM:SS
    e.g. 12:30:45 == 87"""

    if not isinstance(time_str, str):
        raise TypeError("Invalid input type")

    list_of_nums = time_str.split(":")
    validate_numbers(list_of_nums)

    return sum(int(num) for num in list_of_nums)
