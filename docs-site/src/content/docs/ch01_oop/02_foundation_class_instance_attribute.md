---
title: Class vs instance attributes
description: Class vs instance attributes.
---

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
