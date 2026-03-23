from exercises.ch01.e04.employee import Employee


class PartTimeEmployee(Employee):
    def __init__(self, name, salaryPerHour, workedHours):
        super().__init__(name, salaryPerHour * workedHours)

    def __str__(self):
        return f"{self.name} (PartTime) - ${self.salary}"
