from test_2 import get_closest_court, get_desired_courts


def test_get_closest_court():
    """tests whether the court with the shortest court is returned"""
    courts = [
        {"distance": 0.5},
        {"distance": 1.0}
    ]
    assert get_closest_court(courts) == {"distance": 0.5}


def test_no_distance_key():
    """tests whether get_closest_court returns an empty dict when no courts with
    distance key is present"""

    # court with no distance key
    wrong_court = [
        {"fake": 100}
    ]
    assert get_closest_court(wrong_court) == {}


def test_get_desired_courts():
    """tests whether func get_desired_courts works with base cases"""
    desired_type = "Crown Court"
    courts = [
        {"types": "Crown Court"},
        {"types": "Fake Court"}
    ]
    assert get_desired_courts(desired_type, courts) == [
        {"types": "Crown Court"}]


def test_no_desired_courts():
    """tests whether get_desired_courts returns an empty list if no
    desired courts are present"""
    desired_type = "Crown Court"
    assert get_desired_courts(desired_type, [{"types": "Fake Court"}]) == []
