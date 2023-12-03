import pytest

from test_3 import sum_current_time


def test_correct_sum():
    """test whether the functions returns the correct sum"""
    assert sum_current_time("01:02:03") == 6
    assert sum_current_time("12:30:45") == 87
    assert sum_current_time("00:00:00") == 0


def test_sum_invalid_input():
    """tests whether the function raises an error in response to invalid input"""
    # More components than expected
    with pytest.raises(ValueError):
        sum_current_time("12:30:45:60")

    # Fewer components than expected
    with pytest.raises(ValueError):
        sum_current_time("12:30")

    # non-numeric
    with pytest.raises(ValueError):
        sum_current_time("12:30:abc")

    # empty component
    with pytest.raises(ValueError):
        sum_current_time("12:30:")

    # completely empty
    with pytest.raises(ValueError):
        sum_current_time("::")

    # negative values
    with pytest.raises(ValueError):
        sum_current_time("-12:30:45")

    # just wrong
    with pytest.raises(ValueError):
        sum_current_time("banana")

    # invalid type
    with pytest.raises(TypeError):
        sum_current_time(12)

    # invalid hour
    with pytest.raises(ValueError):
        sum_current_time("50:30:45")

    # invalid format
    with pytest.raises(ValueError):
        sum_current_time("9:3:4")

    # no leading 0
    with pytest.raises(ValueError):
        sum_current_time("1:30:45")
