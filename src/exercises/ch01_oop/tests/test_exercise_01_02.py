from exercises.ch01_oop.exercise_01_02.full_time_employee import FullTimeEmployee
from exercises.ch01_oop.exercise_01_02.manager import Manager
from exercises.ch01_oop.exercise_01_02.part_time_employee import PartTimeEmployee
from exercises.ch01_oop.exercise_01_02.utils import print_payroll


def test_utils(capsys):
    staff = [
        FullTimeEmployee("Alice", 5000),
        PartTimeEmployee("Bob", 20, 80),  # $20/hr × 80hrs
        Manager("Carol", 7000, [500, 300]),  # salary + bonuses
    ]

    print_payroll(staff)

    # test what is printed, capsys is injected by pytest automatically
    captured = capsys.readouterr()
    assert captured.out == (
        "Alice (FullTime) - $5000\nBob (PartTime) - $1600\nCarol (Manager) - $7800\n"
    )
