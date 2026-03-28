---
title: Classes & Objects
description: What a class is
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

```bash frame="none"
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

```python title="Without __repr__"
rectangles = [Rectangle(4, 5), Rectangle(10, 2), Rectangle(3, 3)]
print(rectangles)

# Without `__repr__` you get:
# Useless — just the memory address.
# Three objects. No idea what is in them.
[<Rectangle object at 0x10f3a2b50>, <Rectangle object at 0x10f3a2c60>, <Rectangle object at 0x10f3a2d70>]
```

```python
# With `__repr__`:
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

print(rectangles)
[Rectangle(width=4, height=5), Rectangle(width=10, height=2), Rectangle(width=3, height=3)]
```

#### The convention

`__repr__` should ideally return a string that looks like valid Python code you could paste back into the interpreter to recreate the object.

Let's use REPL (Read, Evaluate, Print, Loop) to interact with the Python Interpreter and visually see the `__repr__` in action:

```bash title="__repr__ in action"
# Type python or python3 to start REPL
$ python

# Interact with the Python interpreter
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

## Quick reference

A summary of the core concepts covered in this chapter.

### Classes and instances

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Define a class | `class Dog:` | Create a blueprint |
| Create an instance | `Dog("Rex", 3)` | Concrete object from the blueprint |
| Class attribute | `species = "Canis familiaris"` | Shared by all instances |
| Instance attribute | `self.name = name` | Unique to each instance |
| Instance method | `def bark(self):` | Behaviour tied to an instance |

### String representation

| Method | Triggered by | For |
|--------|-------------|-----|
| `__str__` | `print(obj)`, `str(obj)` | End users — readable |
| `__repr__` | REPL, debugger, `repr(obj)` | Developers — unambiguous |

### `self`

| Concept | Meaning |
|---------|---------|
| `self` | Reference to the current instance |
| `dog1.bark()` | Python rewrites as `Dog.bark(dog1)` |
| Always first argument | Every instance method receives `self` automatically |

### Pythonic class design

| Situation | Use |
|-----------|-----|
| Primarily storing data | `@dataclass` |
| Need validation, properties, complex logic | plain `class` |
| Immutable data | `@dataclass(frozen=True)` |
| Memory efficiency | `@dataclass(slots=True)` |
| Only one representation needed | Define `__repr__` — `print()` falls back to it |