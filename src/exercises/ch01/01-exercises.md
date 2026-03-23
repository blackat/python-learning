# OOP Exercises

Here are 10 exercises organized by difficulty — beginner through advanced.

---

## 🟢 Beginner

### Exercise 1 — Basic Class
Create a `Rectangle` class that:
- Takes `width` and `height` in `__init__`
- Has an `area()` method
- Has a `perimeter()` method
- Has a `__str__` that returns `"Rectangle(width=W, height=H)"`
- Has a `is_square()` method that returns `True` if width equals height

```python
# Expected output:
r = Rectangle(4, 6)
print(r)                # Rectangle(width=4, height=6)
print(r.area())         # 24
print(r.perimeter())    # 20
print(r.is_square())    # False

s = Rectangle(5, 5)
print(s.is_square())    # True
```

---

### Exercise 2 — Class & Instance Attributes
Create a `BankAccount` class that:
- Tracks total number of accounts created (class attribute)
- Has `owner`, `balance` (instance attributes)
- Has `deposit(amount)` and `withdraw(amount)` methods
- `withdraw` should raise `ValueError` if funds are insufficient
- Has `get_account_count()` as a `@classmethod`
- Has `__str__` showing owner and balance

```python
# Expected output:
acc1 = BankAccount("Alice", 1000)
acc2 = BankAccount("Bob", 500)

acc1.deposit(200)
acc1.withdraw(100)
print(acc1)                         # BankAccount(owner=Alice, balance=1100)
print(BankAccount.get_account_count())  # 2
acc2.withdraw(1000)                 # ValueError: Insufficient funds
```

---

### Exercise 3 — Properties
Create a `Temperature` class that:
- Stores temperature internally in **Celsius**
- Exposes a `celsius` property with validation (cannot be below -273.15)
- Exposes a `fahrenheit` property that converts automatically
- Exposes a `kelvin` property that converts automatically
- All three properties have setters that update the internal value correctly

```python
# Expected output:
t = Temperature(100)
print(t.celsius)        # 100
print(t.fahrenheit)     # 212.0
print(t.kelvin)         # 373.15

t.fahrenheit = 32
print(t.celsius)        # 0.0

t.celsius = -300        # ValueError: Below absolute zero
```

---

## 🟡 Intermediate

### Exercise 4 — Inheritance
Model a company's staff. Create:
- `Employee` base class with `name`, `salary`, and `get_pay()` method
- `FullTimeEmployee(Employee)` — fixed monthly salary
- `PartTimeEmployee(Employee)` — hourly rate × hours worked
- `Manager(FullTimeEmployee)` — salary + sum of bonuses list
- All should have meaningful `__str__`
- A standalone function `print_payroll(employees)` that prints each employee's pay

```python
# Expected output:
staff = [
    FullTimeEmployee("Alice", 5000),
    PartTimeEmployee("Bob", 20, 80),      # $20/hr × 80hrs
    Manager("Carol", 7000, [500, 300]),   # salary + bonuses
]
print_payroll(staff)
# Alice (FullTime)  — $5000
# Bob   (PartTime)  — $1600
# Carol (Manager)   — $7800
```

---

### Exercise 5 — Magic Methods
Create a `Vector2D` class that supports:
- `__add__`, `__sub__`, `__mul__` (scalar), `__rmul__`
- `__neg__`, `__abs__` (magnitude)
- `__eq__` and `__lt__` (compare by magnitude)
- `__iter__` (so you can unpack: `x, y = vector`)
- `__repr__` and `__str__`
- A `normalize()` method returning a unit vector

```python
# Expected output:
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

---

### Exercise 6 — Abstract Base Classes
Design a **payment system**. Create:
- Abstract base class `PaymentMethod` with abstract methods `pay(amount)` and `refund(amount)`, and abstract property `name`
- `CreditCard(PaymentMethod)` — tracks spending limit and current balance
- `PayPal(PaymentMethod)` — tracks email and balance
- `CryptoCurrency(PaymentMethod)` — tracks coin type, amount, and exchange rate to USD
- A `checkout(cart_total, payment)` function that uses any payment method

```python
# Expected output:
card   = CreditCard("Alice", limit=1000, balance=800)
paypal = PayPal("alice@example.com", balance=500)
crypto = CryptoCurrency("BTC", amount=0.01, rate=45000)

checkout(200, card)     # Paid $200 via Credit Card. Remaining limit: $600
checkout(150, paypal)   # Paid $150 via PayPal. Remaining balance: $350
checkout(100, crypto)   # Paid $100 via BTC (0.00222 BTC). Remaining: 0.00778 BTC
```

---

## 🔴 Advanced

### Exercise 7 — Mixin Classes
Create a set of **mixin classes** and combine them:
- `SerializeMixin` — adds `to_dict()` and `to_json()` methods
- `ValidateMixin` — adds `validate()` that checks all required fields are non-empty
- `TimestampMixin` — adds `created_at` and `updated_at`, and an `update()` method that refreshes `updated_at`
- `ReprMixin` — auto-generates `__repr__` from instance `__dict__`
- A `User` class that inherits all four mixins

```python
# Expected output:
u = User(name="Alice", email="alice@example.com", age=30)
print(u.validate())         # True
print(u.to_dict())          # {'name': 'Alice', 'email': '...', 'age': 30}
print(u.to_json())          # '{"name": "Alice", ...}'
print(u.created_at)         # 2026-03-22 ...
u.update(email="new@x.com")
print(u.updated_at)         # Updated timestamp
print(repr(u))              # User(name=Alice, email=new@x.com, age=30)
```

---

### Exercise 8 — Context Manager Class
Build a `DatabaseConnection` class that acts as a context manager:
- `__init__` takes a connection string
- `__enter__` simulates connecting and returns itself
- `__exit__` simulates disconnecting, and **rolls back** if an exception occurred
- Has `execute(query)` method that logs all queries
- Has `commit()` method
- Raises `RuntimeError` if you call `execute()` outside a `with` block
- Tracks total queries executed as a class attribute

```python
# Expected output:
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

---

### Exercise 9 — Full OOP Design
Design a **Library Management System** with the following classes:
- `Book` — title, author, ISBN, available (bool)
- `Member` — name, member ID, list of borrowed books (max 3)
- `Library` — collection of books and members, with:
  - `add_book(book)` / `remove_book(isbn)`
  - `register_member(member)` / `remove_member(member_id)`
  - `borrow_book(member_id, isbn)` — with proper error handling
  - `return_book(member_id, isbn)`
  - `search_by_author(author)` — returns list of matching books
  - `available_books()` — returns all books not currently borrowed
  - `__str__` showing library stats

```python
# Expected:
lib = Library("City Library")
lib.add_book(Book("1984", "Orwell", "ISBN001"))
lib.add_book(Book("Dune", "Herbert", "ISBN002"))
lib.register_member(Member("Alice", "M001"))

lib.borrow_book("M001", "ISBN001")
print(lib.available_books())    # [Dune by Herbert]
lib.return_book("M001", "ISBN001")
print(lib.available_books())    # [1984 by Orwell, Dune by Herbert]
print(lib)                      # City Library — 2 books, 1 members
```

---

### Exercise 10 — Challenge
Implement a `Matrix` class that behaves like a mathematical matrix:
- `__init__` takes a 2D list
- `__add__`, `__sub__`, `__mul__` (matrix × matrix AND matrix × scalar)
- `__eq__`, `__repr__`
- `__getitem__` so `m[row][col]` works
- `transpose()` returning a new Matrix
- `determinant()` for 2×2 and 3×3 matrices
- `is_square()`, `rows`, `cols` as properties
- Raise `ValueError` for incompatible dimensions

```python
# Expected output:
m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[5, 6], [7, 8]])

print(m1 + m2)          # Matrix([[6, 8], [10, 12]])
print(m1 * m2)          # Matrix([[19, 22], [43, 50]])
print(m1 * 2)           # Matrix([[2, 4], [6, 8]])
print(m1.transpose())   # Matrix([[1, 3], [2, 4]])
print(m1.determinant()) # -2.0
print(m1[0][1])         # 2
print(m1.rows)          # 2
print(m1.cols)          # 2
print(m1.is_square())   # True
```

---

## Summary

| # | Exercise | Concepts Covered |
|---|---|---|
| 1 | Rectangle | Basic class, methods, `__str__` |
| 2 | BankAccount | Class attributes, `@classmethod`, validation |
| 3 | Temperature | `@property`, getters, setters, validation |
| 4 | Company Staff | Inheritance, `super()`, polymorphism |
| 5 | Vector2D | Magic methods, arithmetic, comparison |
| 6 | Payment System | ABCs, `@abstractmethod`, duck typing |
| 7 | Mixins | Multiple inheritance, mixin pattern |
| 8 | DatabaseConnection | Context managers, class state |
| 9 | Library System | Full OOP design, composition |
| 10 | Matrix | Advanced dunders, algorithms |

---

Would you like me to provide **solutions** for any of these exercises, or generate exercise sets for the other chapters?