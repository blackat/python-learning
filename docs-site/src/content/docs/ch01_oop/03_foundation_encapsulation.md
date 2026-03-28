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
