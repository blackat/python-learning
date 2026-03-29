from exercises.ch02_funcp.exercise_2_4_1 import celsius_to_fahrenheit


def test_celsius_to_fahrenheit():

    celsius = [0, 10, 20, 30, 40]

    # lazy returned collection
    lazy = celsius_to_fahrenheit(celsius)

    # list will force lazy collection to evaluate
    assert list(lazy) == [32.0, 50.0, 68.0, 86.0, 104.0]
