class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_pay(self):
        return self.salary

    def __str__(self):
        return f"Employee(name={self.name}, salary={self.salary}"
