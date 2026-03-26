# What Does It Mean Pythonic?

**Pythonic** means writing code that follows Python's own idioms and philosophy — code that feels natural to the language rather than transplanted from another one.

The clearest summary is in **The Zen of Python** (`import this`):

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Readability counts.
```

## Un-pythonic vs pythonic

### Looping with an index (C-style thinking)

```python
# ❌
i = 0
while i < len(names):
    print(names[i])
    i += 1

# ✅
for name in names:
    print(name)
```

### Checking membership (Java-style thinking)

```python
# ❌
found = False
for item in items:
    if item == target:
        found = True

# ✅
found = target in items
```

**Swapping variables:**
```python
# ❌
temp = a
a = b
b = temp

# ✅
a, b = b, a
```

### Building a list

```python
# ❌
result = []
for x in numbers:
    if x > 0:
        result.append(x * 2)

# ✅
result = [x * 2 for x in numbers if x > 0]
```

### Opening a file

```python
# ❌
f = open("file.txt")
data = f.read()
f.close()

# ✅
with open("file.txt") as f:
    data = f.read()
```

### The underlying principle

Pythonic code is not about being clever — it is about using the language the way it was designed to be used. Python gives you tools like list comprehensions, context managers, unpacking, and iterators precisely so you do not need to work around them.

A useful test: if your Python looks like Java or C with different syntax, it probably is not pythonic yet.