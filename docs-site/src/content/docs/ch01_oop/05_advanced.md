---
title: Magic/Dunder Methods, Abstract Base Classes & Dataclasses
description: Magic/dunder methods, Abstract Base Classes, and Dataclasses.
---

## Magic / Dunder Methods

Every Python built-in operation, `print()`, `len()`, `+`, `[]`, `with`, is secretly a method call. When you write `len(playlist)`, Python calls `playlist.__len__()`. When you write `a + b`, Python calls `a.__add__(b)`.

These are **dunder methods**, named for their **d**ouble **under**score prefix and suffix. By implementing them on your own classes you make your objects speak Python's native language. They stop being custom objects that need special handling and start behaving exactly like built-ins.

The name "magic methods" comes from the fact that Python calls them automatically, you never invoke `__len__` directly, you just call `len()` and Python handles the rest.

### String Representation

The first dunders worth knowing are the ones that control how your object appears as a string. Python calls `__str__` when you `print()` an object and `__repr__` when you inspect it in the REPL or debugger.

The convention is simple: `__str__` is for humans, readable and friendly while `__repr__` is for developers, unambiguous and ideally valid Python that could recreate the object.

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):      # For end users → print(book)
        return f"'{self.title}' by {self.author}"

    def __repr__(self):     # For developers → repr(book), debugging
        return f"Book('{self.title}', '{self.author}', {self.pages})"

b = Book("1984", "Orwell", 328)
print(b)        # '1984' by Orwell       ← __str__
print(repr(b))  # Book('1984', 'Orwell', 328)  ← __repr__
```

### Comparison Methods

By default, Python has no idea how to compare two instances of your class. `t1 > t2` will raise a `TypeError`. Implement the **comparison dunders** and your objects become fully comparable, sortable, and usable in conditions just like numbers or strings.

Each dunder maps directly to an operator:

| Dunder | Operator |
|--------|----------|
| `__eq__` | `==` |
| `__lt__` | `<` |
| `__le__` | `<=` |
| `__gt__` | `>` |
| `__ge__` | `>=` |

:::note[`@functools.total_ordering`]
You don't need to implement all comparison methods. You define the two that matter — `__eq__` (equality) and `__lt__` (less than) — and Python derives the rest mathematically:

- `a <= b` → `a < b or a == b`
- `a > b` → `not (a < b) and not (a == b)`
- `a >= b` → `not (a < b)`
```python
from functools import total_ordering

@total_ordering
class Temperature:
    def __eq__(self, other):
        return self.celsius == other.celsius   # your logic

    def __lt__(self, other):
        return self.celsius < other.celsius    # your logic

    # Python generates __le__, __gt__, __ge__ from the two above
```
:::

Here is the full manual implementation — all four comparison methods defined explicitly. Notice the last line: once you implement these dunders, `sorted()` works on your objects for free — no extra code needed.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):    # ==
        return self.celsius == other.celsius

    def __lt__(self, other):    # 
        return self.celsius < other.celsius

    def __le__(self, other):    # <=
        return self.celsius <= other.celsius

    def __gt__(self, other):    # >
        return self.celsius > other.celsius

    def __str__(self):
        return f"{self.celsius}°C"


t1 = Temperature(100)
t2 = Temperature(50)
t3 = Temperature(100)

print(t1 == t3)   # True
print(t1 > t2)    # True
print(t2 < t1)    # True

# Now you can even sort a list of Temperature objects!
temps = [Temperature(30), Temperature(10), Temperature(20)]
print(sorted(temps))   # [10°C, 20°C, 30°C]
```

:::note[`@functools.total_ordering`]
The implementation above defines all four methods manually. In practice you only need two: `__eq__` and `__lt__`. Let `@total_ordering` generate the rest.
:::

### Arithmetic Methods

Arithmetic dunders let your objects support mathematical operators. Each operator maps to a method: `+` calls `__add__`, `-` calls `__sub__`, `*` calls `__mul__`.

`Vector` is the classic example: a 2D point in space with `x` and `y` coordinates. Adding two vectors adds their components, subtracting does the opposite, and multiplying by a scalar scales both dimensions.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):       # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):       # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):      # v1 * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):     # 3 * v1  (reversed)
        return self.__mul__(scalar)

    def __neg__(self):              # -v1
        return Vector(-self.x, -self.y)

    def __abs__(self):              # abs(v1) → magnitude
        return (self.x**2 + self.y**2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(2, 3)
v2 = Vector(1, 4)

print(v1 + v2)    # Vector(3, 7)
print(v1 - v2)    # Vector(1, -1)
print(v1 * 3)     # Vector(6, 9)
print(3 * v1)     # Vector(6, 9)  ← uses __rmul__
print(abs(v1))    # 3.605...
```

:::caution[Reflected version]
One subtlety worth knowing: `v1 * 3` calls `v1.__mul__(3)`, that's straightforward. But `3 * v1` is different, Python calls `(3).__mul__(v1)` first, which fails because integers don't know how to multiply with a `Vector`. Python then tries the **reflected version**: `v1.__rmul__(3)`. Without `__rmul__`, `3 * v1` raises a `TypeError`.
:::

### Container Methods

**Container dunders** make your objects behave like Python's **built-in collections**: lists, dicts, sets. Implement them and your class supports:

- `len()`
- indexing with `[]`
- `in` checks
- `for` loops without inheriting from anything.

:::note[Container dunders methods]

Container dunders are the methods that make your object behave like a Python collection: a list, dict, or set.

They map to operations you use on built-in containers every day:

| Operation | Dunder | Example |
|-----------|--------|---------|
| `len(obj)` | `__len__` | `len(playlist)` |
| `obj[key]` | `__getitem__` | `playlist[0]` |
| `obj[key] = val` | `__setitem__` | `playlist[0] = "new"` |
| `del obj[key]` | `__delitem__` | `del playlist[0]` |
| `x in obj` | `__contains__` | `"song" in playlist` |
| `for x in obj` | `__iter__` | `for song in playlist` |

:::

Implement them and your class becomes a **first-class citizen** alongside Python's own container types. Any code that works with lists, `sorted()`, `enumerate()`, list comprehensions, `for` loops will work with your object too, without inheriting from anything.

`Playlist` will support built-in collections operations out of the box.

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __len__(self):              # len(playlist)
        return len(self._songs)

    def __getitem__(self, index):   # playlist[0]
        return self._songs[index]

    def __setitem__(self, index, value):   # playlist[0] = "new song"
        self._songs[index] = value

    def __delitem__(self, index):   # del playlist[0]
        del self._songs[index]

    def __contains__(self, song):   # "song" in playlist
        return song in self._songs

    def __iter__(self):             # for song in playlist
        return iter(self._songs)

    def __repr__(self):
        return f"Playlist('{self.name}', {self._songs})"


p = Playlist("Chill Mix")
p.add("Song A")
p.add("Song B")
p.add("Song C")

print(len(p))            # 3
print(p[0])              # Song A
print("Song B" in p)     # True

for song in p:           # Iteration works!
    print(song)
```

### Context Manager Methods

The `with` statement is Python's way of saying: *"set something up, do some work, then tear it down, no matter what happens".* File handles, database connections, network sockets, locks, anything that needs guaranteed cleanup is a good candidate for a context manager. For instance, a file is guaranteed to close even if an exception is raised inside the block, **no explicit `try/finally` needed**:

```python
with open("file.txt") as f:
    data = f.read()
```

Any object can support this protocol by implementing two dunders:

- `__enter__` runs when execution enters the `with` block and returns the object bound to `as`
- `__exit__` runs when execution leaves, whether normally or because an exception was raised.

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):        # Called when entering `with` block
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):   # Called on exit
        if self.file:
            self.file.close()
        return False    # False = don't suppress exceptions


with FileManager("test.txt", "w") as f:
    f.write("Hello!")
# File is automatically closed here, even if an error occurs
```

### Callable Objects

In Python, **functions are objects**. But the reverse is also possible: **<mark>objects can behave like functions</mark>**. Implement `__call__` and **your object becomes callable**: you can invoke it with `()` just like a function.

:::note[When to use it]
This is useful when you need a callable that also carries state, something a plain function can't do. A `Multiplier` that remembers its factor, a rate limiter that tracks call history, a validator that holds its rules. All are cleaner as callable objects than as functions with global state or closures.
:::

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):      # Makes the object callable like a function
        return value * self.factor


double = Multiplier(2)
triple = Multiplier(3)

print(double(5))    # 10
print(triple(5))    # 15
print(callable(double))  # True
```

---

## Abstract Base Classes (ABCs)

Inheritance lets subclasses reuse code. But what if you want to **<mark>enforce a contract</mark>**, guarantee that every subclass implements specific methods, rather than just hoping they do?

That's what Abstract Base Classes are for. An ABC defines the **interface**: the methods every subclass must implement without providing the implementation itself. If a subclass forgets to implement a required method, Python raises a `TypeError` the moment you try to instantiate it, not later when you call the missing method.

This catches bugs early and makes your intent explicit: `Shape` is not meant to be used directly, it's a blueprint that `Circle`, `Rectangle` and any future shape must follow.

```bash frame="none"
Shape (ABC — blueprint, cannot be instantiated)
├── Circle     must implement area() and perimeter()
└── Rectangle  must implement area() and perimeter()
```

```python
from abc import ABC, abstractmethod

class Shape(ABC):           # Inherit from ABC to make it abstract

    @abstractmethod
    def area(self):         # Subclasses MUST implement this
        pass

    @abstractmethod
    def perimeter(self):    # Subclasses MUST implement this
        pass

    def describe(self):     # Concrete method — shared by all shapes
        return f"I am a shape with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


# shape = Shape()     # ❌ TypeError: Can't instantiate abstract class
c = Circle(5)
r = Rectangle(4, 6)

print(c.area())         # 78.53
print(r.perimeter())    # 20
print(c.describe())     # I am a shape with area 78.54
print(r.describe())     # I am a shape with area 24.00

# Polymorphism — treat all shapes uniformly
shapes = [Circle(3), Rectangle(2, 5), Circle(7)]
for shape in shapes:
    print(f"Area: {shape.area():.2f}")
```

:::note[Why use ABCs?]
They prevent incomplete implementations. If a subclass forgets to implement `area()`, Python raises a `TypeError` immediately, catching bugs early.
:::

## Dataclasses

Dataclasses eliminate boilerplate for classes that primarily **<mark>store data</mark>**.

Every data class you write without `@dataclass` follows the same tedious pattern: write `__init__` to store the attributes, write `__repr__` so it prints nicely, write `__eq__` so equality comparison works. The logic is always the same, only the field names change.

`@dataclass` is Python's answer to this boilerplate. You declare the fields **with type hints** and Python generates `__init__`, `__repr__`, and `__eq__` automatically. The class stays focused on what it *is*, not on the ceremony of setting it up.

Then use tabs for the before/after:

```python title="Without @dataclass"
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p3 = Point(1.0, 2.0, 3.0)

print(p1)           # Point(x=1.0, y=2.0, z=0.0)  ← __repr__ auto-generated
print(p1 == p2)     # True                          ← __eq__ auto-generated
print(p1 == p3)     # False
```

```python title="With @dataclass"
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0
```

Same result, a third of the code.

### Advanced Dataclass Features

The basic `@dataclass` covers most cases, but **three advanced features** are worth knowing:

- **`field(default_factory=list)`**: mutable defaults like lists and dicts must use `field(default_factory=...)` instead of a direct assignment. If you write `grades: list = []`, all instances share the same list, **a classic Python gotcha**.
- **`field(init=False, repr=False)`**: excludes a field from `__init__` and `__repr__`. Useful for auto-generated values like IDs that the caller should never set directly.
- **`__post_init__`**: runs automatically after `__init__`. Use it for validation or any setup that depends on the fields already being set.

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str
    age: int
    grades: List[float] = field(default_factory=list)  # Mutable default
    _id: int = field(init=False, repr=False)            # Not in __init__ or repr

    def __post_init__(self):            # Runs after __init__
        self._id = id(self)             # Auto-generate ID
        if self.age < 0:
            raise ValueError("Age cannot be negative")

    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0.0


s = Student("Alice", 20, [85.0, 92.0, 78.0])
print(s)                # Student(name='Alice', age=20, grades=[85.0, 92.0, 78.0])
print(s.average())      # 85.0
```

<details class="deeper">
<summary>Under the hood: field(default_factory=list)</summary>

<div>

In Python, **<mark>default values</mark>** in a class definition are created **once** when the class is defined, not each time you create an instance. So if you write:

```python
@dataclass
class Student:
    grades: list = []   # ❌ WRONG
```

Every `Student` shares the **<mark>exact same list object in memory</mark>**. Add a grade to one student and it appears on all of them:

```python
s1 = Student()
s2 = Student()

s1.grades.append(90)
print(s2.grades)   # [90]  ← s2 is contaminated!
```

`field(default_factory=list)` fixes this by calling `list()` **fresh for each new instance**:

```python
@dataclass
class Student:
    grades: list = field(default_factory=list)   # ✅ correct
```

Now every student gets their own independent list:

```python
s1 = Student()
s2 = Student()

s1.grades.append(90)
print(s2.grades)   # []  ← untouched
```

The same applies to any mutable default: dicts, sets, or custom objects. Immutable defaults like `int`, `str`, `float`, and `bool` are safe to use directly because they can't be modified in place.

</div>
</details>

:::note[Mutable vs. immutable]
A **mutable** object is one that can be changed after creation. A **immutable** object cannot.

| Mutable | Immutable |
|---------|-----------|
| `list` | `int` |
| `dict` | `str` |
| `set` | `float` |
| custom objects | `bool` |
| | `tuple` |

The problem with mutable defaults is precisely that they *can* be changed — so when two instances share the same default object, a change made through one instance is visible through the other.

Immutable defaults are safe because there's no way to modify them in place — `str` and `int` can't be mutated, so sharing them between instances is harmless.

```python
@dataclass
class Example:
    count: int = 0        # ✅ safe — int is immutable
    name: str = "Alice"   # ✅ safe — str is immutable
    tags: list = field(default_factory=list)   # ✅ safe — fresh list each time
    tags: list = []       # ❌ danger — shared list
```

:::

### Frozen Dataclasses (Immutable)

By default, dataclass instances are mutable, anyone can change `p.x = 999` **<mark>after creation</mark>**. Add `frozen=True` and Python makes the instance immutable: any attempt to modify a field after creation raises a `FrozenInstanceError`.

Frozen dataclasses gain one important property as a side effect, **<mark>they become hashable</mark>**. Regular mutable objects can't be used as dict keys or added to sets because their hash could change if their data changes. **A frozen dataclass has a fixed hash**, so it works anywhere a hashable object is expected.

```python
@dataclass(frozen=True)     # Makes instances immutable
class Coordinate:
    lat: float
    lon: float


c = Coordinate(40.7128, -74.0060)
print(c)            # Coordinate(lat=40.7128, lon=-74.006)
# c.lat = 0        # ❌ FrozenInstanceError — can't modify!

# Frozen dataclasses are hashable, so they can be used as dict keys or in sets
locations = {Coordinate(40.7, -74.0): "New York"}
```

## Quick Reference

A summary of all the dunders covered in this chapter — use this as a cheat sheet when you need a quick reminder of which method to implement.

| Dunder | Triggered by |
|---|---|
| `__str__` | `print(obj)`, `str(obj)` |
| `__repr__` | `repr(obj)`, debugging |
| `__len__` | `len(obj)` |
| `__getitem__` | `obj[key]` |
| `__contains__` | `x in obj` |
| `__iter__` | `for x in obj` |
| `__call__` | `obj()` |
| `__add__` | `obj + other` |
| `__eq__` | `obj == other` |
| `__lt__` | `obj < other` |
| `__enter__`/`__exit__` | `with obj:` |

---

## Exercises

### Exercise 4.1 — Magic methods <span class="badge yellow">Intermediate</span>

Create a `Vector2D` class that supports:

- `__add__`, `__sub__`, `__mul__` (scalar), `__rmul__`
- `__neg__`, `__abs__` (magnitude)
- `__eq__` and `__lt__` (compare by magnitude)
- `__iter__` (so you can unpack: `x, y = vector`)
- `__repr__` and `__str__`
- A `normalize()` method returning a unit vector
```python title="Expected output"
v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print(v1 + v2)          # Vector2D(4, 6)
print(v1 - v2)          # Vector2D(2, 2)
print(v1 * 3)           # Vector2D(9, 12)
print(3 * v1)           # Vector2D(9, 12)
print(abs(v1))          # 5.0
print(v1 > v2)          # True
x, y = v1               # Unpacking
print(x, y)             # 3 4
print(v1.normalize())   # Vector2D(0.6, 0.8)
```

<details class="exercise">
<summary>Solution</summary>
<div>

{/* TODO: add solution and tests */}

</div>
</details>

---

### Exercise 4.2 — Abstract Base Classes <span class="badge yellow">Intermediate</span>

Design a **payment system**. Create:

- Abstract base class `PaymentMethod` with abstract methods `pay(amount)` and `refund(amount)`, and abstract property `name`
- `CreditCard(PaymentMethod)` — tracks spending limit and current balance
- `PayPal(PaymentMethod)` — tracks email and balance
- `CryptoCurrency(PaymentMethod)` — tracks coin type, amount, and exchange rate to USD
- A `checkout(cart_total, payment)` function that uses any payment method

```python title="Expected output"
card   = CreditCard("Alice", limit=1000, balance=800)
paypal = PayPal("alice@example.com", balance=500)
crypto = CryptoCurrency("BTC", amount=0.01, rate=45000)

checkout(200, card)     # Paid $200 via Credit Card. Remaining limit: $600
checkout(150, paypal)   # Paid $150 via PayPal. Remaining balance: $350
checkout(100, crypto)   # Paid $100 via BTC (0.00222 BTC). Remaining: 0.00778 BTC
```

<details class="exercise">
<summary>Solution</summary>
<div>

{/* TODO: add solution and tests */}

</div>
</details>

### Exercise 4.3 — Context manager

Build a `DatabaseConnection` class that acts as a context manager:

- `__init__` takes a connection string
- `__enter__` simulates connecting and returns itself
- `__exit__` simulates disconnecting, and **rolls back** if an exception occurred
- Has `execute(query)` method that logs all queries
- Has `commit()` method
- Raises `RuntimeError` if you call `execute()` outside a `with` block
- Tracks total queries executed as a class attribute

```python title="Expected output"
with DatabaseConnection("postgresql://localhost/mydb") as db:
    db.execute("SELECT * FROM users")
    db.execute("INSERT INTO users VALUES ('Alice')")
    db.commit()
# Connecting to postgresql://localhost/mydb
# Query executed: SELECT * FROM users
# Query executed: INSERT INTO users VALUES ('Alice')
# Committed 2 queries
# Disconnecting cleanly

# On exception → rolls back instead of committing
with DatabaseConnection("postgresql://localhost/mydb") as db:
    db.execute("DELETE FROM users")
    raise RuntimeError("Something went wrong")
# Rolling back 1 queries
```

<details class="exercise">
<summary>Solution</summary>
<div>

{/* TODO: add solution and tests */}

</div>
</details>