from logging import Manager

from exercises.ch01.e04.full_time_employee import FullTimeEmployee
from exercises.ch01.e04.main import print_payroll
from exercises.ch01.e04.part_time_employee import PartTimeEmployee


def test_main():
    staff = [
        FullTimeEmployee("Alice", 5000),
        PartTimeEmployee("Bob", 20, 80),  # $20/hr × 80hrs
        Manager("Carol", 7000, [500, 300]),  # salary + bonuses
    ]

    print_payroll(staff)
