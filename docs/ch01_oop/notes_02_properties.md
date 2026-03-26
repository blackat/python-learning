# Smart Attributes

## `@property`

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

### Important

`self._celsius` and `self_celsius` are the same thing. Here is why:

When you call `print(t.celsius)` Python runs the **getter**:

```python
@property
def celsius(self) -> float:
    return self._celsius  # ← reads from _celsius
```

So `t.celsius` and `t._celsius` **always return the same value**. The property `celsius` is just a clean public interface that reads from `_celsius` under the hood.

Think of it like this:

```python
t.celsius       → triggers the getter → returns self._celsius
t._celsius      → direct access to the private attribute
```

Both give you the same number. The difference is:

- `t.celsius` — the **public door** — goes through the getter, which could have logic in it
- `t._celsius` — the **back door** — bypasses the getter, direct access

### Deeper

Let me walk through it step by step with a concrete mental model.

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

#### Three different ways to interact with the value

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

#### Why not just use `celsius` everywhere and forget `_celsius`?

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

#### The naming convention visualised

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

### The rule in one sentence

Inside the class, always read and write `_celsius` directly. Outside the class, always use `celsius`. The property bridges the two — it is the translation layer between the outside world and the internal storage.

---

## Getter and Setter, the Python way

When to use `@property`:

- You need **validation** on assignment
- You need to **compute** a value rather than store it
- You need **side effects** when a value changes — like updating a cache or notifying something
- You want to make an attribute **read-only** — define the getter but no setter

When NOT to use it:

- If the attribute is just storing a value with no logic — use a plain attribute. Do not add `@property` just to follow a Java habit.
- That is the most common mistake Python beginners make coming from other languages.

### The practical takeaway

```python
self.celsius   # public — use freely from anywhere
self._celsius  # "private by convention" — please don't touch this from outside
self.__celsius # name-mangled — harder to access but still not truly private
```

The single underscore `_celsius` is a gentleman's agreement — it says *this is an internal implementation detail, don't rely on it.* **Nothing stops you from accessing it externally**, but you are signalling to other developers that they should not.

> In Python you do not need to make everything private by default like in Java. Start with public attributes. Use _name when you want to signal **internal use only**. Use `@property` when you need logic around access. That is the complete picture.

- **Java says:** I do not trust you, I will enforce access rules.
- **Python says:** I trust you, I will tell you my intentions through naming conventions and you will respect them.

### The full flow for `t.fahrenheit = 32`

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

### Plain attribute vs. `@property`

It is completely correct — because you have no `@property` defined for `name` or `salary`.

The recursion problem only happens when you define a `@property` with the same name as the attribute you are trying to store to. Here is the key distinction:

#### No property, plain attribute, always correct

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name      # plain attribute, stored directly
        self.salary = salary  # plain attribute, stored directly
```

`self.name = name` just stores the value directly in memory. No getter, no setter, no interception. Simple and correct.

#### With property needs the underscore

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
