from lessons.ch01_oop.exercises.exercise_04.employee import Employee


class FullTimeEmployee(Employee):
    def __str__(self):
        return f"{self.name} (FullTime) - ${self.salary}"
