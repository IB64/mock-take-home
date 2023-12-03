from test_1 import is_log_line, get_dict, is_viable_date, is_viable_log_level, is_viable_time


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


def test_viable_date():
    """test to see date validation works"""
    assert is_viable_date("03/11/21") == True
    assert is_viable_date("25/10/23") == True


def test_not_viable_date():
    """test to see if incorrect dates return False"""
    assert is_viable_date("100/01/21") == False
    assert is_viable_date("12/25/21") == False
    assert is_viable_date("10/10/2000") == False
    assert is_viable_date("30/02/21") == False
    assert is_viable_date("//") == False


def test_viable_time():
    """test whether time validation works"""
    assert is_viable_time("08:51:01") == True
    assert is_viable_time("21:57:03") == True


def test_not_viable_time():
    """test whether time validation rejects invalid times"""
    assert is_viable_time("::") == False
    assert is_viable_time("-1:45:45") == False
    assert is_viable_time("25:54:54") == False
    assert is_viable_time("23:78:90") == False


def test_viable_log_level():
    """test whether log level validation works"""
    assert is_viable_log_level("WARNING") == True
    assert is_viable_log_level("INFO") == True


def test_not_viable_log_level():
    """test whether log level validation rejects invalid log levels"""
    assert is_viable_log_level("INF") == False
    assert is_viable_log_level("info") == False
    assert is_viable_log_level("INFORMATION") == False
