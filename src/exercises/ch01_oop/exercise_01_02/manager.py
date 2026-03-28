from exercises.ch01_oop.exercise_01_02.employee import Employee


class Manager(Employee):
    def __init__(self, name, salary, bonuses: list[int]):
        super().__init__(name, salary + sum(bonuses))

    def __str__(self):
        return f"{self.name} (Manager) - ${self.salary}"
