import pytest

from lessons.ch01_oop.exercises.exercise_03 import BankAccount


def test_balance_account():

    acc1 = BankAccount("Alice", 1000)
    acc2 = BankAccount("Bob", 500)

    acc1.deposit(200)
    acc1.withdraw(100)

    print(acc1)  # BankAccount(owner=Alice, balance=1100)
    assert acc1.get_balance() == 1100
    assert acc1.get_owner() == "Alice"

    print(BankAccount.get_account_count())

    assert BankAccount.get_account_count() == 2

    with pytest.raises(ValueError, match="Insufficient funds"):
        acc2.withdraw(1000)
