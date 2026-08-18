# Python concepts particularly useful for AI

# 1. Iterators

### Simple definition

An **iterator is something that gives you one item at a time**.

Imagine you have:

```python
numbers = [10, 20, 30, 40]
```

Instead of taking everything at once, an iterator can give:

```text
10 → next
20 → next
30 → next
40 → next
```

Python's `for` loop internally works with iterators.

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Behind the scenes, Python is essentially asking:

```text
"Give me the next item."
"Give me the next item."
"Give me the next item."
"No more items."
```

---

## `iter()` and `next()`

You can manually create an iterator:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```text
10
20
30
```

If you call:

```python
next(iterator)
```

again, there are no more values, so Python raises:

```text
StopIteration
```

### Why useful in AI?

AI applications often process data **one item at a time**:

```text
Documents
   ↓
Document 1
Document 2
Document 3
...
```

Instead of loading/processsing everything at once, iterators allow sequential processing.

---

# 2. Generators

Generators are **a special and very useful type of iterator**.

The easiest way to understand them:

> A generator produces values **one at a time when you ask for them**, instead of creating everything in memory at once.

Example:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Notice:

```python
yield
```

instead of:

```python
return
```

Now:

```python
gen = numbers()

print(next(gen))
print(next(gen))
print(next(gen))
```

Output:

```text
1
2
3
```

---

## `return` vs `yield`

Normal function:

```python
def numbers():
    return [1, 2, 3]
```

It creates the entire list:

```text
[1, 2, 3]
```

Generator:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Produces:

```text
1 → pause
2 → pause
3 → pause
```

This is extremely useful for **large data**.

---

## Why generators matter in AI

Imagine an LLM generates:

```text
Hello
Hello, how
Hello, how are
Hello, how are you?
```

You don't necessarily want to wait until the **entire response** is generated.

You can process/return pieces as they arrive:

```text
LLM
 ↓
"Hello"
 ↓
" how"
 ↓
" are"
 ↓
" you?"
```

This concept of producing things incrementally is closely related to how **streaming AI responses** work.

You'll encounter generators and async generators when working with AI APIs.

---

# 3. `async`

Now we're entering a very important area for AI.

Suppose your program needs to call:

```text
LLM API
```

The API might take 2 seconds to respond.

During those 2 seconds, your program is basically waiting.

With normal synchronous code:

```python
response = call_llm()
print(response)
```

Your program waits:

```text
Call LLM
   ↓
WAIT 2 seconds
   ↓
Get response
   ↓
Continue
```

With asynchronous programming, you can say:

> "While I'm waiting for this operation, do other useful work."

That's the basic idea behind `async`.

---

# 4. `await`

`await` basically means:

> **"Wait for this asynchronous operation to finish, but don't block the entire async system while waiting."**

Example:

```python
async def get_response():
    response = await call_llm()
    print(response)
```

Notice:

```python
async def
```

and:

```python
await
```

usually work together.

Think:

```text
async
 ↓
"This function can perform asynchronous work."

await
 ↓
"Wait for this particular async operation."
```

---

# 5. Why async is REALLY useful in AI

Imagine your AI agent needs to call 3 APIs:

```text
Weather API       → 2 sec
News API          → 2 sec
LLM API           → 2 sec
```

### Synchronous approach

You might do:

```text
Weather
 ↓ 2 sec

News
 ↓ 2 sec

LLM
 ↓ 2 sec

Total ≈ 6 sec
```

But these operations don't necessarily depend on each other.

With async:

```text
Weather ──────────→ 2 sec
News ─────────────→ 2 sec
LLM ──────────────→ 2 sec

Total ≈ 2 sec
```

That's why async programming is very common in:

* AI agents
* API calls
* Web scraping
* RAG systems
* FastAPI
* LLM applications
* Tool calling

---

# 6. `asyncio`

Okay, then what is `asyncio`?

Think of:

```text
async
await
```

as the **language features**.

And:

```text
asyncio
```

as Python's **toolkit for running asynchronous code**.

Example:

```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(2)
    print("World")

asyncio.run(hello())
```

Here:

```python
asyncio.run()
```

starts the asynchronous program.

---

# 7. The really important async example

Suppose:

```python
import asyncio

async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)
    print("Task 1 finished")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(2)
    print("Task 2 finished")
```

If you run them sequentially:

```python
await task1()
await task2()
```

roughly:

```text
Task 1 → 2 sec
Task 2 → 2 sec

Total ≈ 4 sec
```

But you can run them concurrently:

```python
await asyncio.gather(
    task1(),
    task2()
)
```

Now:

```text
Task 1 ──────→
              2 sec
Task 2 ──────→

Total ≈ 2 sec
```

This pattern is **very important for AI agents**.

For example:

```text
Agent
 │
 ├── Search Web
 ├── Query Database
 ├── Call API
 └── Retrieve Documents
```

If these operations are independent, async concurrency can make the agent much faster.

---

# 8. Type Hints

Python doesn't force you to specify types.

You can write:

```python
def add(a, b):
    return a + b
```

But you can tell Python developers what types you expect:

```python
def add(a: int, b: int) -> int:
    return a + b
```

This is called a **type hint**.

It says:

```text
a → int
b → int

return → int
```

---

## Why useful in AI?

AI applications can become huge.

Imagine:

```python
def process_document(
    document: str,
    chunk_size: int,
    metadata: dict
) -> list:
    ...
```

Now when you're working on the code, your editor can understand what is expected.

This makes large AI projects easier to maintain.

---

# 9. `typing`

`typing` is Python's module that provides tools for writing **more detailed type hints**.

For example:

```python
from typing import List

numbers: List[int] = [1, 2, 3]
```

You can also describe dictionaries:

```python
from typing import Dict

user: Dict[str, str] = {
    "name": "Abhishek",
    "city": "Bangalore"
}
```

Modern Python allows cleaner syntax:

```python
numbers: list[int] = [1, 2, 3]

user: dict[str, str] = {
    "name": "Abhishek"
}
```

You'll frequently encounter:

```python
Optional
Union
Literal
Any
Callable
TypeVar
Protocol
```

But you don't need to master all of these immediately.

For AI development, initially understand:

```text
str
int
float
bool
list[T]
dict[K, V]
Optional[T]
```

---

# 10. Dataclasses

Imagine you're creating a user:

```python
class User:

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
```

This is repetitive.

Python gives you `dataclass`.

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str
```

Now:

```python
user = User(
    "Abhishek",
    20,
    "abc@example.com"
)
```

That's it.

Python automatically creates much of the boilerplate for you.

---

## Why useful in AI?

AI systems have lots of structured data:

```text
User
Message
Document
Chunk
Tool
AgentState
ModelResponse
Configuration
```

Dataclasses are convenient for representing these objects.

For example:

```python
@dataclass
class Document:
    content: str
    source: str
    page: int
```

Now:

```python
doc = Document(
    content="Python is...",
    source="python.pdf",
    page=10
)
```

Very clean.

---

# 11. Decorators

Decorators are initially confusing.

The simplest definition:

> **A decorator modifies or adds behavior to a function without changing the function's main code.**

Suppose:

```python
def hello():
    print("Hello")
```

We want to print:

```text
Function started
Hello
Function finished
```

We could use a decorator.

```python
def logger(func):

    def wrapper():
        print("Function started")
        func()
        print("Function finished")

    return wrapper
```

Then:

```python
@logger
def hello():
    print("Hello")
```

Now:

```python
hello()
```

produces:

```text
Function started
Hello
Function finished
```

---

## What does `@logger` mean?

This:

```python
@logger
def hello():
    ...
```

is basically saying:

```python
hello = logger(hello)
```

That's the important thing to understand.

---

## Why decorators matter in AI?

You'll see decorators in many Python frameworks.

For example:

```python
@app.get("/users")
def get_users():
    ...
```

The decorator tells the framework:

> "This function handles GET requests for `/users`."

You'll also encounter decorators for:

* caching
* authentication
* logging
* retries
* tool definitions
* API routes
* validation
* framework configuration

So you don't need to become a decorator expert immediately, but you **must understand what `@something` is doing conceptually**.

---

# 12. Context Managers

This one becomes very easy with a real-world analogy.

Imagine borrowing a book from a library:

```text
Open/borrow
    ↓
Use book
    ↓
Return book
```

You don't want to forget the final step.

A **context manager** helps manage resources automatically.

The most common example is opening a file:

```python
with open("data.txt") as file:
    data = file.read()
```

The important part is:

```python
with
```

Python handles the resource cleanup for you.

Conceptually:

```text
with
 ↓
Open resource
 ↓
Use resource
 ↓
Automatically clean up
```

Without it, you might write:

```python
file = open("data.txt")

data = file.read()

file.close()
```

The `with` version is safer and cleaner.

---

# Why context managers matter in AI

AI applications work with resources such as:

* files
* database connections
* network connections
* locks
* temporary resources
* model resources

For example:

```python
with open("documents.txt") as file:
    text = file.read()
```

You don't have to remember to manually close the file.

---

# Now connect all of these to an AI Agent

This is where these concepts start making sense.

Imagine you're building:

```text
             AI AGENT
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
     Search    Database    LLM
       │         │         │
       └─────────┼─────────┘
                 ↓
              Response
```

You could use:

### Iterators

Process search results one at a time:

```python
for result in results:
    process(result)
```

### Generators

Stream results:

```python
def generate_results():
    yield result1
    yield result2
```

### `async`

Perform API operations without unnecessarily blocking:

```python
async def search():
    ...
```

### `await`

Wait for an API response:

```python
result = await search()
```

### `asyncio`

Run independent operations concurrently:

```python
await asyncio.gather(
    search_web(),
    search_database(),
    get_weather()
)
```

### Type hints

Make your agent code understandable:

```python
def run_agent(query: str) -> str:
    ...
```

### Dataclasses

Represent structured agent data:

```python
@dataclass
class Message:
    role: str
    content: str
```

### Decorators

Frameworks can attach behavior to functions:

```python
@tool
def search_web(query: str):
    ...
```

### Context managers

Safely manage resources:

```python
with open("knowledge.txt") as file:
    data = file.read()
```

---

# The most important mental model

Don't try to memorize definitions.

Remember these **one-line meanings**:

```text
Iterator
↓
Give me the next item.


Generator
↓
I'll produce items one at a time.


async
↓
This function can work asynchronously.


await
↓
Wait for this async operation.


asyncio
↓
Python's toolkit for running async code.


Type hints
↓
Tell developers/tools what type of data is expected.


typing
↓
Tools for writing detailed type hints.


Dataclass
↓
Easy way to create classes mainly used for storing data.


Decorator
↓
Add/modify behavior around a function.


Context manager
↓
Set something up → use it → automatically clean it up.
```

## What you should prioritize for Agentic AI

I'd rank them like this for you:

**🔥 Must understand deeply**

1. `async`
2. `await`
3. `asyncio`
4. Generators
5. Iterators
6. Type hints

**🟢 Understand well**

7. Decorators
8. Dataclasses

**🟡 Basic understanding is enough initially**

9. Context managers

You don't need advanced Python before starting AI. But **async/await + generators + type hints** are particularly worth becoming comfortable with because you'll encounter them constantly when building real AI applications.
