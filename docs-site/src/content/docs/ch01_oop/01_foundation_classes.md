---
title: Classes & Objects
description: Classes & Objects
---

A **class** is a blueprint. It describes what an object *is* and what it can *do*. An **instance** is a concrete object created from that blueprint, each one carries its own data but shares the same behaviour.

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

:::tip[The Pythonic Way]
The Python philosophy, don't write boilerplate the language can generate for you, `dataclasses` eliminate the boilerplate that makes classes feel repetitive.

When a class primarily stores data, use `@dataclass`, it auto-generates
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

##### When to use what

| Situation | Use |
|-----------|-----|
| Primarily storing data | `@dataclass` |
| Need validation, properties, complex logic | plain `class` |
| Immutable data (like a coordinate) | `@dataclass(frozen=True)` |
| Need slots for memory efficiency | `@dataclass(slots=True)` |

##### The rule of thumb

Start with a `@dataclass`, upgrade to a plain class only when you need behaviour that dataclasses can't express cleanly.
:::
