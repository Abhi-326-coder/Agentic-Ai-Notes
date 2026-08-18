# Python Fundamentals — Complete Guide

## Variables

A variable is a name that points to a value stored in memory. Python is dynamically typed — you don't declare a type; it's inferred.

```python
name = "Alice"
age = 30
age = "thirty"  # allowed, type can change
```

Naming rules: letters, digits, underscores; can't start with a digit; case-sensitive; can't use reserved words (`if`, `for`, etc.). Convention: `snake_case` for variables/functions.

---

## Data Types

### `int` — whole numbers
```python
x = 10
y = -3
```

### `float` — decimal numbers
```python
pi = 3.14
```

### `str` — text, immutable sequence of characters
```python
s = "hello"
s[0]        # 'h'
s + " world"  # concatenation
s * 2       # 'hellohello'
```

### `bool` — `True` or `False` (subclass of int: `True == 1`)
```python
is_valid = True
```

### `list` — ordered, **mutable**, allows duplicates
```python
nums = [1, 2, 3]
nums.append(4)
nums[0] = 99
```

### `tuple` — ordered, **immutable**, allows duplicates
```python
point = (3, 4)
# point[0] = 5  # Error! Can't modify
```

### `set` — unordered, **mutable**, no duplicates
```python
s = {1, 2, 2, 3}  # {1, 2, 3}
s.add(4)
```

### `dict` — key-value pairs, mutable, keys unique
```python
person = {"name": "Alice", "age": 30}
person["age"]        # 30
person["city"] = "NY"  # add new key
```

| Type | Ordered | Mutable | Duplicates |
|---|---|---|---|
| list | ✅ | ✅ | ✅ |
| tuple | ✅ | ❌ | ✅ |
| set | ❌ | ✅ | ❌ |
| dict | ✅ (3.7+) | ✅ (values) | keys: ❌ |

---

## Conditional Statements

```python
age = 20
if age < 13:
    print("child")
elif age < 20:
    print("teen")
else:
    print("adult")
```

`elif` can repeat; `else` is optional. Indentation (not braces) defines blocks — this is mandatory in Python.

---

## `for` loops

Iterate over any **iterable** (list, string, dict, range, etc.).

```python
for i in range(5):        # 0,1,2,3,4
    print(i)

for fruit in ["apple", "banana"]:
    print(fruit)

for key, value in person.items():
    print(key, value)
```

## `while` loops

Repeats **while** a condition is `True`. Risk: infinite loop if condition never becomes false.

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

`break` exits the loop early; `continue` skips to the next iteration.

---

## Functions

```python
def greet(name):
    return f"Hello, {name}!"

greet("Bob")
```

### Parameters and Arguments

- **Parameter**: variable in the function definition (`name`).
- **Argument**: actual value passed when calling (`"Bob"`).

```python
def add(a, b=10):       # b is a default parameter
    return a + b

add(5)          # 15 (uses default b)
add(5, 20)      # 25 (positional args)
add(a=5, b=20)  # 25 (keyword args)

def total(*args):        # variable positional args -> tuple
    return sum(args)

def info(**kwargs):      # variable keyword args -> dict
    print(kwargs)
```

### Return Values

`return` sends a value back to the caller and exits the function. No `return` statement → function returns `None`.

```python
def square(x):
    return x * x

result = square(4)  # 16
```

### Lambda Functions

Anonymous, single-expression functions.

```python
square = lambda x: x * x
square(5)  # 25

add = lambda a, b: a + b

# Common use: as key/argument to other functions
nums = [(1, 'b'), (2, 'a')]
sorted(nums, key=lambda x: x[1])  # sort by second element
```

### List/Dictionary Comprehensions

Concise way to build lists/dicts from iterables.

```python
squares = [x**2 for x in range(5)]          # [0,1,4,9,16]
evens = [x for x in range(10) if x % 2 == 0]  # filter

squares_dict = {x: x**2 for x in range(5)}  # {0:0, 1:1, 2:4,...}

# nested
matrix = [[i*j for j in range(3)] for i in range(3)]
```

---

## Exception Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("Can't divide by zero:", e)
except (TypeError, ValueError):
    print("Type or value issue")
else:
    print("Runs if no exception occurred")
finally:
    print("Always runs, error or not")
```

- `try`: code that might fail
- `except`: handle a specific error type
- `finally`: cleanup code, always executes (closing files, connections)
- `raise`: manually trigger an exception

```python
def check_age(age):
    if age < 0:
        raise ValueError("Age can't be negative")
```

---

## Modules, Packages, pip

- **Module**: a single `.py` file with reusable code (`import math`).
- **Package**: a folder of modules with an `__init__.py`.
- **pip**: Python's package installer, pulls from PyPI.

```python
import math
from math import sqrt
import numpy as np

math.sqrt(16)  # 4.0
```

```bash
pip install requests
pip list
pip uninstall requests
```

---

## Virtual Environments

Isolated Python environments so project dependencies don't conflict.

### `venv`
```bash
python -m venv myenv
source myenv/bin/activate     # Mac/Linux
myenv\Scripts\activate        # Windows
deactivate
```

### `requirements.txt`
Lists a project's dependencies for reproducibility.

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

---

## File Handling

```python
# Writing
with open("file.txt", "w") as f:
    f.write("Hello\n")

# Reading
with open("file.txt", "r") as f:
    content = f.read()        # whole file
    # or f.readline() / f.readlines()

# Appending
with open("file.txt", "a") as f:
    f.write("More text\n")
```

`with` auto-closes the file (equivalent to using `finally: f.close()`). Modes: `"r"` read, `"w"` write (overwrite), `"a"` append, `"rb"/"wb"` binary.

---

## JSON

```python
import json

data = {"name": "Alice", "age": 30}

json_str = json.dumps(data)          # dict -> JSON string
parsed = json.loads(json_str)        # JSON string -> dict

with open("data.json", "w") as f:
    json.dump(data, f)               # dict -> JSON file

with open("data.json", "r") as f:
    loaded = json.load(f)            # JSON file -> dict
```

---

## `os` module

```python
import os

os.getcwd()              # current working directory
os.listdir(".")           # list files in a directory
os.path.join("dir", "file.txt")  # OS-safe path joining
os.path.exists("file.txt")
os.mkdir("new_folder")
os.environ.get("HOME")   # read env variable
```

## `pathlib` (modern, object-oriented alternative to `os.path`)

```python
from pathlib import Path

p = Path("data") / "file.txt"   # path joining with /
p.exists()
p.name        # 'file.txt'
p.suffix      # '.txt'
p.parent      # 'data'
p.read_text()
p.write_text("hello")
```

---

## Environment Variables & `.env`

Store secrets/config (API keys, DB URLs) outside your code.

```bash
# .env file
API_KEY=abc123
DEBUG=True
```

```python
import os
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()  # reads .env into environment
api_key = os.environ.get("API_KEY")
```

`.env` should never be committed to version control (add to `.gitignore`).

---

## Quick Self-Check Questions

Try answering these — they cover every topic above:

1. What's the difference between a list and a tuple? When would you use each?
2. Why does `{1: "a"}["key"]` behave differently from `[1,2,3][5]` in terms of error type?
3. Write a function with a default parameter and call it two different ways.
4. What's the difference between `except Exception` and a bare `except:`?
5. What does `finally` guarantee that `except` doesn't?
6. Convert `[x for x in range(10) if x % 2 == 0]` into an equivalent `for` loop.
7. Why use a virtual environment instead of installing packages globally?
8. What does `with open(...) as f:` do for you automatically?
9. How would you safely read an environment variable that might not exist?
10. What's the difference between `os.path.join` and `pathlib`'s `/` operator — functionally, is there one?

Try these — I'll check your answers and clarify anything that's still fuzzy.