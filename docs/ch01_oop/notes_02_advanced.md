# Magic/Dunder Methods, Abstract Base Classes & Dataclasses

---

## 1. Magic / Dunder Methods

These let your objects behave like Python built-ins. The name "dunder" = **d**ouble **under**score.

### String Representation
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

---

### Comparison Methods
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

> 💡 **Shortcut:** Use `@functools.total_ordering` — define `__eq__` and ONE of `__lt__`/`__gt__`, and it fills in the rest automatically.

---

### Arithmetic Methods
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

---

### Container Methods
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

---

### Context Manager Methods
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

---

### Callable Objects
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

## 2. Abstract Base Classes (ABCs)

ABCs let you define **interfaces** — blueprints that force subclasses to implement specific methods.

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

> **Why use ABCs?** They prevent incomplete implementations. If a subclass forgets to implement `area()`, Python raises a `TypeError` immediately — catching bugs early.

---

## 3. Dataclasses

Dataclasses eliminate boilerplate for classes that primarily **store data**.

### The Problem They Solve
```python
# Without dataclass — lots of repetitive boilerplate
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
```

```python
# With dataclass — clean and automatic!
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0      # Default value

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p3 = Point(1.0, 2.0, 3.0)

print(p1)           # Point(x=1.0, y=2.0, z=0.0)  ← __repr__ auto-generated
print(p1 == p2)     # True                          ← __eq__ auto-generated
print(p1 == p3)     # False
```

---

### Advanced Dataclass Features
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

---

### Frozen Dataclasses (Immutable)
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

---

## Quick Reference

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

You now have a solid OOP foundation. Ready to move on to **Decorators** — one of Python's most powerful and elegant features?