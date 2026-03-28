---
title: OOP — Foundation
description: Classes, inheritance, encapsulation, class methods, and MRO.
---

## Classes & Objects

A **class** is a blueprint. It describes what an object *is* and what it can *do*. An **instance** is a concrete object created from that blueprint — each one carries its own data but shares the same behaviour.

```python
class Dog:
    # Class attribute — shared by ALL instances
    species = "Canis familiaris"

    def __init__(self, name, age):
        # Instance attributes — unique to EACH object
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says Woof!"

    def __str__(self):       # print(dog)  → human-readable
        return f"Dog(name={self.name}, age={self.age})"

    def __repr__(self):      # repr(dog)   → developer-facing
        return f"Dog('{self.name}', {self.age})"
```

### The Pythonic Way

The Python philosophy, don't write boilerplate the language can generate for you.

**dataclasses** eliminate the boilerplate that makes classes feel repetitive:

:::tip[The Pythonic Way]
When a class primarily stores data, use `@dataclass` — it auto-generates
`__init__`, `__repr__`, and `__eq__` for you.
```python
from dataclasses import dataclass

@dataclass
class Dog:
    name: str
    age: int
    species: str = "Canis familiaris"  # default value

# Identical behaviour to the full class above
dog1 = Dog("Rex", 3)
dog2 = Dog("Buddy", 5)

print(dog1)          # Dog(name='Rex', age=3, species='Canis familiaris')
print(dog1 == dog2)  # False — __eq__ auto-generated
```

Use a plain `class` when you need custom logic, validation, or `@property`.
:::

```python
# ❌ Un-pythonic — lots of ceremony
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Dog(name={self.name}, age={self.age})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age
```

```python
# ✅ Pythonic — declare what matters, Python handles the rest
from dataclasses import dataclass

@dataclass
class Dog:
    name: str
    age: int
```

That single `@dataclass` decorator auto-generates `__init__`, `__repr__`, and `__eq__` for you.

#### When to use what

| Situation | Use |
|-----------|-----|
| Primarily storing data | `@dataclass` |
| Need validation, properties, complex logic | plain `class` |
| Immutable data (like a coordinate) | `@dataclass(frozen=True)` |
| Need slots for memory efficiency | `@dataclass(slots=True)` |

#### The rule of thumb

Start with a `@dataclass`, upgrade to a plain class only when you need behaviour that dataclasses can't express cleanly.

---

## Class vs instance attributes

`species` lives on the **class** — one value, shared by every dog you create. `name` and `age` live on the **instance** — each dog gets its own copy.

```python
dog1 = Dog("Rex", 3)
dog2 = Dog("Buddy", 5)

print(dog1.species)   # Canis familiaris  ← same for all
print(dog2.species)   # Canis familiaris  ← same for all
print(dog1.name)      # Rex              ← unique to dog1
print(dog2.name)      # Buddy            ← unique to dog2
```

Visually:

```
Dog (class)
│   species = "Canis familiaris"   ← shared
│
├── dog1 (instance)
│     name = "Rex", age = 3        ← unique
│
└── dog2 (instance)
      name = "Buddy", age = 5      ← unique
```

### `self` — the object talking to itself

Every method receives `self` as the first argument. It is how the object refers to itself — how `bark()` knows *which* dog is barking.

```python
print(dog1.bark())   # Rex says Woof!
print(dog2.bark())   # Buddy says Woof!
```

Python rewrites `dog1.bark()` as `Dog.bark(dog1)` under the hood — `self` is just `dog1` passed in automatically.

### `__str__` and `__repr__`

Both control how the object is displayed, but for different audiences:

| Method | Triggered by | For |
|--------|-------------|-----|
| `__str__` | `print(dog)`, `str(dog)` | End users — readable |
| `__repr__` | REPL, debugger, `repr(dog)` | Developers — unambiguous |

```python
print(dog1)    # Dog(name=Rex, age=3)   ← __str__
repr(dog1)     # Dog('Rex', 3)          ← __repr__
```

If you only define one, define `__repr__`, Python falls back to it when `__str__` is missing.

**The key idea:** the class is the mold, instances are the objects cast from it. The mold stays the same — each cast comes out with its own data.

### What is `__repr__`?

`__repr__` is a special Python method that defines the **string representation** of an object — what you see when you print or inspect it.

```python
rectangles = [Rectangle(4, 5), Rectangle(10, 2), Rectangle(3, 3)]
print(rectangles)

# Without `__repr__` you get:
# Useless — just the memory address.
# Three objects. No idea what is in them.
[<Rectangle object at 0x10f3a2b50>, <Rectangle object at 0x10f3a2c60>, <Rectangle object at 0x10f3a2d70>]

# With `__repr__`:
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

...
print(rectangles)
[Rectangle(width=4, height=5), Rectangle(width=10, height=2), Rectangle(width=3, height=3)]
```

#### The convention

`__repr__` should ideally return a string that looks like valid Python code you could paste back into the interpreter to recreate the object:

```python
>>> r = Rectangle(width=4, height=5)
>>> r
Rectangle(width=4, height=5)
>>> eval(repr(r))  # recreates the object
Rectangle(width=4, height=5)
```

#### `__repr__` vs `__str__`**

| | Purpose | Called by |
| -- | -- | -- |
| `__repr__` | Unambiguous, developer-facing | `repr()`, REPL, debugger |
| `__str__` | Human-readable, user-facing | `print()`, `str()` |

If you only define `__repr__` — `print()` will fall back to it. If you define both, `print()` uses `__str__` and the REPL uses `__repr__`.

For most classes defining just `__repr__` is enough.

---

## Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement speak()")

    def eat(self):
        return f"{self.name} is eating."


class Dog(Animal):          # Dog inherits from Animal
    def speak(self):        # Override parent method
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"


dog = Dog("Rex")
cat = Cat("Whiskers")

print(dog.speak())   # Rex says Woof!
print(cat.speak())   # Whiskers says Meow!
print(dog.eat())     # Rex is eating.  ← inherited from Animal

# Check relationships
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True  ← dog IS an Animal
print(issubclass(Dog, Animal))  # True
```

---

## `super()` — Calling the Parent

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)   # Call Animal's __init__
        self.breed = breed            # Add Dog-specific attribute

    def info(self):
        return f"{self.name} ({self.breed}), age {self.age}"

dog = Dog("Rex", 3, "Labrador")
print(dog.info())   # Rex (Labrador), age 3
```

---

## Encapsulation: Public, Protected, Private

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

---

## Multiple Inheritance & MRO

```python
class A:
    def hello(self):
        return "Hello from A"

class B(A):
    def hello(self):
        return "Hello from B"

class C(A):
    def hello(self):
        return "Hello from C"

class D(B, C):       # Inherits from both B and C
    pass

d = D()
print(d.hello())     # Hello from B

# MRO = Method Resolution Order — the lookup chain
print(D.__mro__)     # D → B → C → A → object
```
Python uses **C3 linearization** to determine which method wins. Always check `__mro__` when using multiple inheritance.

---

## Key Concepts Summary

| Concept | Purpose |
|---|---|
| `__init__` | Initialize object state |
| `self` | Reference to current instance |
| `super()` | Access parent class |
| `@property` | Controlled attribute access |
| `@classmethod` | Method that works on the class |
| `@staticmethod` | Utility method, no class/instance access |
| `__str__` / `__repr__` | String representations |
| `_x` / `__x` | Protected / private conventions |
