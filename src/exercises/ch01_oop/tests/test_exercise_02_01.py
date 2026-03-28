import pytest

from exercises.ch01_oop.exercise_02_01 import Temperature


def test_temperature(capsys):
    t = Temperature(100)

    print(t.celsius)
    captured = capsys.readouterr()
    assert captured.out == "100\n"

    print(t.fahrenheit)
    captured = capsys.readouterr()
    assert captured.out == "212.0\n"

    print(t.kelvin)
    captured = capsys.readouterr()
    assert captured.out == "373.15\n"

    t.fahrenheit = 32
    print(t.celsius)
    captured = capsys.readouterr()
    assert captured.out == "0.0\n"

    with pytest.raises(ValueError, match="Temperature below absolute zero"):
        t.celsius = -300
