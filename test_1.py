"""script to run task_1"""
import re

LOG_LEVELS = ("INFO", "TRACE", "WARNING")


def is_viable_date(date_str: str) -> bool:
    """checks whether the date in the log line is viable using a regex"""
    pattern = r"^(0[1-9]|1[0-9]|2[0-8])/(0[1-9]|1[0-2])/\d{2}$|^(29|30)/(0[13-9]|1[0-2])/\d{2}$|^(31)/(0[13578]|1[02])/\d{2}$"
    return bool(re.match(pattern, date_str))


def is_viable_time(time_str: str) -> bool:
    """checks whether the time in the log line is viable using a regex"""
    pattern = r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
    return bool(re.match(pattern, time_str))


def is_viable_log_level(log_level: str) -> bool:
    """checks whether the log level in the log is viable"""
    return bool(log_level in LOG_LEVELS)


def is_log_line(line) -> bool | None:
    """Takes a log line and returns True if it is a valid log line and returns None
    if it is not.
    """
    fragments = line.split(" ")
    if len(fragments) < 4:
        return None

    date = fragments[0]
    time = fragments[1]
    log_level = fragments[2]

    if not is_viable_date(date):
        return None
    if not is_viable_time(time):
        return None
    if not is_viable_log_level(log_level):
        return None

    return True


def get_dict(line) -> dict:
    """Takes a log line and returns a dict with
    `timestamp`, `log_level`, `message` keys
    """
    fragments = line.split(" ")
    while "" in fragments:
        fragments.remove("")

    date = fragments[0]
    time = fragments[1]
    timestamp = date + " " + time
    log_level = fragments[2]
    message = " ".join(fragments[3:])[:-1]
    return {
        "timestamp": timestamp,
        "log_level": log_level,
        "message": message
    }


# YOU DON'T NEED TO CHANGE ANYTHING BELOW THIS LINE
if __name__ == "__main__":
    # these are basic generators that will return
    # 1 line of the log file at a time
    def log_parser_step_1(log_file):
        f = open(log_file)
        for line in f:
            if is_log_line(line):
                yield line

    def log_parser_step_2(log_file):
        f = open(log_file)
        for line in f:
            if is_log_line(line):
                yield get_dict(line)

    # ---- OUTPUT --- #
    # You can print out each line of the log file line by line
    # by uncommenting this code below
    # for i, line in enumerate(log_parser("sample.log")):
    #     print(i, line)

    # ---- TESTS ---- #
    # DO NOT CHANGE

    def test_step_1():
        with open("tests/step1.log") as f:
            test_lines = f.readlines()
        actual_out = list(log_parser_step_1("sample.log"))

        if actual_out == test_lines:
            print("STEP 1 SUCCESS")
        else:
            print(
                "STEP 1 FAILURE: step 1 produced unexpecting lines.\n"
                "Writing to failure.log if you want to compare it to tests/step1.log"
            )
            with open("step-1-failure-output.log", "w") as f:
                f.writelines(actual_out)

    def test_step_2():
        expected = {
            "timestamp": "03/11/21 08:51:01",
            "log_level": "INFO",
            "message": ":.main: *************** RSVP Agent started ***************",
        }
        actual = next(log_parser_step_2("sample.log"))

        if expected == actual:
            print("STEP 2 SUCCESS")
        else:
            print(
                "STEP 2 FAILURE: your first item from the generator was not as expected.\n"
                "Printing both expected and your output:\n"
            )
            print(f"Expected: {expected}")
            print(f"Generator Output: {actual}")

    try:
        test_step_1()
    except Exception:
        print("step 1 test unable to run")

    try:
        test_step_2()
    except Exception:
        print("step 2 test unable to run")
