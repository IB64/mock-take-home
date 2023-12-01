from test_1 import is_log_line, get_dict
from test_2 import get_closest_court


def test_valid_log():
    """test to chek if is_log_line works as it should"""
    correct_line = "03/11/21 08:51:01 INFO    :.main: *************** RSVP Agent started ***************"
    correct_line_1 = "03/11/21 08:51:01 INFO    :...locate_configFile: Specified configuration file: /u/user10/rsvpd1.conf"
    incorrect_line = " 02 "
    assert is_log_line(correct_line) == True
    assert is_log_line(correct_line_1) == True
    assert is_log_line(incorrect_line) == None


def test_get_dict():
    """tests the function get_dict to see if it works as it should"""
    correct_line = "03/11/21 08:51:01 INFO    :.main: *************** RSVP Agent started ***************\n"
    expected = {
        "timestamp": "03/11/21 08:51:01",
        "log_level": "INFO",
        "message": ":.main: *************** RSVP Agent started ***************",
    }
    assert get_dict(correct_line) == expected


def test_get_closest_court():
    """tests whether the court with the shortest court is returned"""
    courts = [
        {"distance": 0.5},
        {"distance": 1.0}
    ]
    assert get_closest_court(courts) == {"distance": 0.5}
