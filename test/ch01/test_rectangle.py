from exercises.ch01.e01.rectangle import Rectangle


def test_rectangle_happy_path():
    r = Rectangle(4, 6)

    print(r)

    assert r.area() == 24
    assert r.perimeter() == 20
    assert r.is_square() is False


def test_rectangle_squared():
    r = Rectangle(5, 5)
    assert r.is_square() is True
