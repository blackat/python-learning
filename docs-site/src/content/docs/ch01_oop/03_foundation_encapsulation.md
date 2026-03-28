---
title: "Encapsulation: public, protected and private"
description: How to control access within that hierarchy
---

In the example below, `BankAccount` demonstrates the three levels of access control Python uses by convention. `owner` is fully public, anyone can read or change it. `_account_no` is protected, accessible but signals "internal use only". `__balance` is private, name-mangled by Python to make accidental access harder, and exposed only through the controlled `get_balance()` method.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner          # public    → accessible anywhere
        self._account_no = "12345"  # protected → convention: don't touch outside class
        self.__balance = balance    # private   → name-mangled, hidden

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):          # Controlled access via method
        return self.__balance


acc = BankAccount("Alice", 1000)
print(acc.owner)           # Alice       ✅
print(acc._account_no)     # 12345       ⚠️ works but discouraged
# print(acc.__balance)     # ❌ AttributeError
print(acc.get_balance())   # 1000        ✅
```

:::note[When to use underscores]
Use `_name` only when you introduce a `@property` for that attribute. Plain attributes like `name` or `balance` need no underscore, store them directly.
:::

### The simple rule

You will see `@property` in the next chapter — for now just remember this:

| Situation | What to use |
|---|---|
| No `@property` | `self.name` — plain attribute, no underscore needed |
| Has `@property` | `self._name` inside the class, `self.name` outside |

## Class Methods & Static Methods

Not all methods need to work on a **specific instance**. Python gives you two alternatives:

- `@classmethod` for methods that work on the **class itself**
- `@staticmethod` for pure utility functions that don't need access to either the class or an instance.

In the example below:

- `Employee` uses a **class attribute** `_count` to track how many employees have been created
- `get_count()` reads that class-level data
- `from_string()` acts as an alternative constructor, a common pattern for creating objects from different input formats
- `is_valid_salary()` is a plain utility that could live anywhere but belongs here logically.

```python
class Employee:
    company = "TechCorp"
    _count = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee._count += 1

    @classmethod
    def get_count(cls):             # Works on the CLASS, not instance
        return f"Total employees: {cls._count}"

    @classmethod
    def from_string(cls, data):     # Alternative constructor
        name, salary = data.split(",")
        return cls(name, int(salary))

    @staticmethod
    def is_valid_salary(salary):    # Utility — no access to class/instance
        return salary > 0


e1 = Employee("Alice", 50000)
e2 = Employee.from_string("Bob,60000")   # Alternative constructor

print(Employee.get_count())              # Total employees: 2
print(Employee.is_valid_salary(50000))   # True
```

## Quick reference

A summary of the access control conventions and method types covered in this chapter.

### Access levels

| Convention | Syntax | Accessible from | Meaning |
|------------|--------|-----------------|---------|
| Public | `self.name` | Anywhere | No restrictions |
| Protected | `self._name` | Class and subclasses | Convention — don't touch outside |
| Private | `self.__name` | Class only | Name-mangled by Python |

### Method types

| Decorator | First argument | Has access to | Use for |
|-----------|---------------|---------------|---------|
| none | `self` | Instance + class | Regular behaviour |
| `@classmethod` | `cls` | Class only | Alternative constructors, class-level state |
| `@staticmethod` | none | Neither | Utility functions that belong logically |

### When to use what

| Situation | Use |
|-----------|-----|
| Regular behaviour on an instance | Instance method |
| Tracking class-level data like a counter | `@classmethod` |
| Creating objects from different input formats | `@classmethod` as alternative constructor |
| Pure utility with no class or instance needed | `@staticmethod` |
| Hiding implementation details | `_name` or `__name` |
| Controlled access to private data | Expose via a public method |

## Exercises

### Exercise 2 — Class & instance attributes

Create a `BankAccount` class that:

- Tracks total number of accounts created (class attribute)
- Has `owner` and `balance` as instance attributes
- Has `deposit(amount)` and `withdraw(amount)` methods
- `withdraw` should raise `ValueError` if funds are insufficient
- Has `get_account_count()` as a `@classmethod`
- Has `__str__` showing owner and balance
```python title="Expected output"
acc1 = BankAccount("Alice", 1000)
acc2 = BankAccount("Bob", 500)

acc1.deposit(200)
acc1.withdraw(100)
print(acc1)                          # BankAccount(owner=Alice, balance=1100)
print(BankAccount.get_account_count())  # 2
acc2.withdraw(1000)                  # ValueError: Insufficient funds
```

<details class="exercise">
<summary>Solution</summary>
<div>
```python title="exercise_03.py"
class BankAccount:
    totalAccounts = 0

    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner
        self.balance = balance
        BankAccount.totalAccounts += 1

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_balance(self) -> float:
        return self.balance

    def get_owner(self) -> str:
        return self.owner

    @classmethod
    def get_account_count(cls) -> int:
        return cls.totalAccounts

    def __str__(self) -> str:
        return f"BankAccount(owner={self.owner}, balance={self.balance})"
```

`totalAccounts` is a class attribute — it lives on the class, not on any instance, so it counts across all accounts. `get_account_count()` uses `cls` instead of `self` — it works on the class itself, not an instance. `withdraw` validates before modifying — if the check fails, `balance` is never touched.
```python title="test_exercise_03.py"
import pytest
from exercises.ch01_oop.exercise_03 import BankAccount

def test_balance_account():
    acc1 = BankAccount("Alice", 1000)
    acc2 = BankAccount("Bob", 500)

    acc1.deposit(200)
    acc1.withdraw(100)

    assert acc1.get_balance() == 1100
    assert acc1.get_owner() == "Alice"
    assert BankAccount.get_account_count() == 2

    with pytest.raises(ValueError, match="Insufficient funds"):
        acc2.withdraw(1000)
```

</div>
</details>