from exercises.ch01.e04.employee import Employee


class FullTimeEmployee(Employee):
    def __str__(self):
        return f"{self.name} (FullTime) - ${self.salary}"
