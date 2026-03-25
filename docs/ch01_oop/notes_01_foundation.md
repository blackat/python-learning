# Object-Oriented Programming in Python

---

## 1. Classes & Objects

```python
class Dog:
    # Class attribute (shared by all instances)
    species = "Canis familiaris"

    # Constructor / initializer
    def __init__(self, name, age):
        # Instance attributes (unique to each object)
        self.name = name
        self.age = age

    # Instance method
    def bark(self):
        return f"{self.name} says Woof!"

    def __str__(self):          # Human-readable string
        return f"Dog(name={self.name}, age={self.age})"

    def __repr__(self):         # Developer-facing string
        return f"Dog('{self.name}', {self.age})"


# Creating objects (instances)
dog1 = Dog("Rex", 3)
dog2 = Dog("Buddy", 5)

print(dog1.bark())        # Rex says Woof!
print(dog1.species)       # Canis familiaris  (class attribute)
print(dog2.species)       # Canis familiaris  (same for all)
print(dog1)               # Dog(name=Rex, age=3)  → calls __str__
```

### What is `__repr__` ?

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


## 2. Inheritance

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

## 3. `super()` — Calling the Parent

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

## 4. Encapsulation — Public, Protected, Private

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

---

## 5. `@property` — Smart Attributes

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):               # Getter
        return self._radius

    @radius.setter
    def radius(self, value):        # Setter with validation
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):                 # Computed property (no setter needed)
        import math
        return math.pi * self._radius ** 2


c = Circle(5)
print(c.radius)    # 5       ← calls getter
print(c.area)      # 78.53   ← computed on the fly
c.radius = 10      # calls setter
# c.radius = -1    # ❌ ValueError
```

### 🔥 Important

`self._celsius` and `self_celsius` are the same thing. Here is why:

When you call `print(t.celsius)` Python runs the **getter**:

```python
@property
def celsius(self) -> float:
    return self._celsius  # ← reads from _celsius
```

So `t.celsius` and `t._celsius` **always return the same value**. The property `celsius` is just a clean public interface that reads from `_celsius` under the hood.

Think of it like this:

```
t.celsius       → triggers the getter → returns self._celsius
t._celsius      → direct access to the private attribute
```

Both give you the same number. The difference is:

- `t.celsius` — the **public door** — goes through the getter, which could have logic in it
- `t._celsius` — the **back door** — bypasses the getter, direct access

#### Depper

Let me walk through it step by step with a concrete mental model.

---

**Think of `_celsius` as a box and `celsius` as the window to that box**

```bash
┌─────────────────────────────┐
│   Temperature object        │
│                             │
│   _celsius = 100.0  ← box  │
│                             │
│   celsius  ← window to box │
└─────────────────────────────┘
```

`_celsius` is where the value physically lives in memory. `celsius` is the property — a controlled way to read from and write to that box.

---

**Three different ways to interact with the value:**

```python
t = Temperature(100)

# 1 — write through the public window (setter runs)
t.celsius = 50
# → setter checks value >= -273.15
# → stores 50 into self._celsius

# 2 — read through the public window (getter runs)
print(t.celsius)
# → getter returns self._celsius
# → prints 50

# 3 — direct back door access (no getter/setter, no validation)
print(t._celsius)
# → prints 50 directly, bypassing everything
```

All three see the same number. The difference is what happens in between.

---

**Why not just use `celsius` everywhere and forget `_celsius`?**

Because if you tried to store to `celsius` inside the class itself:

```python
@celsius.setter
def celsius(self, value):
    self.celsius = value   # ← WRONG
```

Python sees `self.celsius = value` and thinks — "celsius has a setter, let me call it." Which calls the setter. Which calls `self.celsius = value` again. Which calls the setter again. Forever.

```bash
setter called
  → self.celsius = value
      → setter called
          → self.celsius = value
              → setter called
                  → ...
                      → RecursionError 💥
```

`self._celsius = value` breaks the loop because `_celsius` has no setter — it is just a plain attribute. Python stores the value directly without triggering anything.

---

**The naming convention visualised:**

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius      # ← uses the PUBLIC setter (with validation)

    @property
    def celsius(self):
        return self._celsius        # ← reads the PRIVATE storage

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError()
        self._celsius = value       # ← writes to PRIVATE storage directly
```

Reading the flow:

```python
Temperature(100)
  → __init__ runs
  → self.celsius = 100          calls setter ✓
      → validation passes
      → self._celsius = 100     stores directly ✓

t.celsius                       calls getter ✓
  → return self._celsius        reads directly ✓
  → returns 100
```

---

### The rule in one sentence

Inside the class, always read and write `_celsius` directly. Outside the class, always use `celsius`. The property bridges the two — it is the translation layer between the outside world and the internal storage.

---

### Getter and Setter, the Python way

When to use `@property`:

- You need **validation** on assignment
- You need to **compute** a value rather than store it
- You need **side effects** when a value changes — like updating a cache or notifying something
- You want to make an attribute **read-only** — define the getter but no setter

When NOT to use it:

- If the attribute is just storing a value with no logic — use a plain attribute. Do not add `@property` just to follow a Java habit.
- That is the most common mistake Python beginners make coming from other languages.

#### The practical takeaway

```python
self.celsius   # public — use freely from anywhere
self._celsius  # "private by convention" — please don't touch this from outside
self.__celsius # name-mangled — harder to access but still not truly private
```

The single underscore `_celsius` is a gentleman's agreement — it says *this is an internal implementation detail, don't rely on it.* **Nothing stops you from accessing it externally**, but you are signalling to other developers that they should not.

> In Python you do not need to make everything private by default like in Java. Start with public attributes. Use _name when you want to signal **internal use only**. Use `@property` when you need logic around access. That is the complete picture.

- **Java says:** I do not trust you, I will enforce access rules.
- **Python says:** I trust you, I will tell you my intentions through naming conventions and you will respect them.

---

**The full flow for `t.fahrenheit = 32`:**

```python
t.fahrenheit = 32
  → fahrenheit setter runs
  → self.celsius = (32 - 32) * 5 / 9  =  0.0
      → celsius setter runs
      → self._celsius = 0.0          ← stored here

print(t.celsius)
  → celsius getter runs
  → return self._celsius             ← reads 0.0
  → prints 0.0  ✓
```

`_celsius` is the **storage**. `celsius` is the **interface**. They always point to the same value — you just access it through the clean public name `celsius` rather than the internal `_celsius`.

---

### Plain attribute vs. `@property`

It is completely correct — because you have no `@property` defined for `name` or `salary`.

The recursion problem only happens when you define a `@property` with the same name as the attribute you are trying to store to. Here is the key distinction:

---

**No property — plain attribute — always correct:**

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name      # plain attribute, stored directly
        self.salary = salary  # plain attribute, stored directly
```

`self.name = name` just stores the value directly in memory. No getter, no setter, no interception. Simple and correct.

---

**With property — needs the underscore:**

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name       # plain attribute, fine
        self.salary = salary   # ← PROBLEM if you define @property salary below

    @property
    def salary(self):
        return self._salary    # reads from _salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("salary cannot be negative")
        self._salary = value   # stores to _salary
```

Now `self.salary = salary` in `__init__` triggers the setter — which is actually what you want here. And the setter stores to `self._salary` — no recursion.

---

**The simple rule:**

| Situation | What to use |
|---|---|
| No `@property` | `self.name` — plain attribute, no underscore needed |
| Has `@property` | `self._name` inside the class, `self.name` outside |

Your `Employee` class is perfectly written. You only need the underscore pattern when you introduce a `@property`.

---

## 6. Class Methods & Static Methods

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

## 7. Multiple Inheritance & MRO

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

---

**Want to go deeper into any of these?** The natural next steps are:

- **Magic/Dunder methods** (`__add__`, `__len__`, `__eq__`, etc.) — making your objects behave like built-ins
- **Abstract Base Classes** — enforcing interfaces
- **Dataclasses** — cleaner class definitions with less boilerplate