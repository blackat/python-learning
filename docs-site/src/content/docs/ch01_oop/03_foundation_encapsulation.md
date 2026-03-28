---
title: "Encapsulation: public, protected and private"
description: Encapsulation
---

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

### The simple rule

| Situation | What to use |
|---|---|
| No `@property` | `self.name` — plain attribute, no underscore needed |
| Has `@property` | `self._name` inside the class, `self.name` outside |

Your `Employee` class is perfectly written. You only need the underscore pattern when you introduce a `@property`.

---

## Class Methods & Static Methods

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
