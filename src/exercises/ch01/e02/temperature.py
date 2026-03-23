class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius  # store only celsius as the source of truth

    @property
    def celsius(self):
        return self.celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self.celsius = value

    @property  # getter
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter  # setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9  # convert and store as celsius

    @property
    def kelvin(self):
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value):
        self.celsius = value - 273.15  # convert and store as celsius

    def __repr__(self) -> str:
        return f"Temperature(celsius={self._celsius})"
