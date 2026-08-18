# Python OOP + AI-Relevant Concepts

Here's a working reference for everything on your list, with the "why it matters for AI work" noted where relevant.

## OOP Basics

### Classes and Objects
A class is a blueprint; an object is an instance of it.

```python
class Model:
    pass

my_model = Model()  # my_model is an object/instance of Model
```

### `__init__` and Instance Variables
`__init__` runs when you create an object — it sets up instance variables (data unique to that object).

```python
class Model:
    def __init__(self, name, params=1_000_000):
        self.name = name          # instance variable
        self.params = params      # instance variable

gpt = Model("gpt-mini", 7_000_000)
print(gpt.name)  # gpt-mini
```

### Methods
Functions defined inside a class; `self` refers to the instance calling them.

```python
class Model:
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def summary(self):
        return f"{self.name}: {self.params:,} params"

print(gpt.summary())
```

### Inheritance
A subclass reuses and extends a parent class.

```python
class Model:
    def __init__(self, name):
        self.name = name

    def predict(self, x):
        raise NotImplementedError

class LinearModel(Model):
    def __init__(self, name, weights):
        super().__init__(name)   # call parent's __init__
        self.weights = weights

    def predict(self, x):
        return sum(w * xi for w, xi in zip(self.weights, x))
```

### Encapsulation
Convention-based in Python — no true `private`. `_x` = "internal, don't touch"; `__x` = name-mangled, harder to access accidentally.

```python
class Model:
    def __init__(self):
        self._cache = {}       # convention: internal use
        self.__secret_key = 1  # name-mangled to _Model__secret_key
```

Use `@property` when you want controlled access:

```python
class Model:
    def __init__(self, lr):
        self._lr = lr

    @property
    def lr(self):
        return self._lr

    @lr.setter
    def lr(self, value):
        if value <= 0:
            raise ValueError("learning rate must be positive")
        self._lr = value
```

### Polymorphism
Different classes respond to the same method call in their own way.

```python
class LinearModel(Model):
    def predict(self, x): return "linear prediction"

class TreeModel(Model):
    def predict(self, x): return "tree prediction"

for m in [LinearModel("l"), TreeModel("t")]:
    print(m.predict(None))  # same call, different behavior
```

### Abstract Classes (basic)
Use `abc` to force subclasses to implement certain methods — great for defining a common interface (e.g., all your model classes must have `predict` and `train`).

```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def predict(self, x):
        ...

    @abstractmethod
    def train(self, data):
        ...

# BaseModel() would raise TypeError — can't instantiate directly
class MyModel(BaseModel):
    def predict(self, x): return x
    def train(self, data): pass  # now this is instantiable
```

---

## AI-Relevant Python Concepts

### Iterators
An object implementing `__iter__` and `__next__`. Useful for streaming data batches without loading everything into memory.

```python
class BatchIterator:
    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= len(self.data):
            raise StopIteration
        batch = self.data[self.i:self.i + self.batch_size]
        self.i += self.batch_size
        return batch

for batch in BatchIterator(list(range(10)), 3):
    print(batch)  # [0,1,2] [3,4,5] [6,7,8] [9]
```

### Generators
A simpler way to write iterators using `yield`. Lazily produces values one at a time — essential for large datasets, token streaming, etc.

```python
def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

for batch in batch_generator(list(range(10)), 3):
    print(batch)
```

Why it matters: this is exactly the pattern behind data loaders and token-by-token LLM output streaming.

### async / await / asyncio
Lets you run I/O-bound work (API calls, file/network requests) concurrently instead of one-at-a-time. Critical for calling LLM APIs in parallel.

```python
import asyncio

async def fetch_completion(prompt):
    await asyncio.sleep(1)  # simulate network call
    return f"Response to: {prompt}"

async def main():
    prompts = ["Hello", "How are you", "Explain OOP"]
    tasks = [fetch_completion(p) for p in prompts]
    results = await asyncio.gather(*tasks)  # run concurrently
    print(results)

asyncio.run(main())
```

Without `asyncio.gather`, three 1-second calls take 3 seconds sequentially. With it, they run concurrently and finish in ~1 second.

### Type Hints & `typing`
Annotate expected types — doesn't enforce at runtime but helps tooling, readability, and catching bugs early (important in larger AI pipelines).

```python
from typing import List, Dict, Optional, Union, Callable

def embed(text: str) -> List[float]:
    return [0.1, 0.2, 0.3]

def get_config(overrides: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    return overrides or {}

def apply_fn(x: float, fn: Callable[[float], float]) -> float:
    return fn(x)
```

### Dataclasses
Auto-generates `__init__`, `__repr__`, `__eq__` for classes that mainly hold data — perfect for configs, model outputs, prompt templates.

```python
from dataclasses import dataclass, field

@dataclass
class GenerationConfig:
    temperature: float = 0.7
    max_tokens: int = 256
    stop_sequences: list = field(default_factory=list)  # avoid mutable default arg pitfall

config = GenerationConfig(temperature=0.9)
print(config)  # GenerationConfig(temperature=0.9, max_tokens=256, stop_sequences=[])
```

### Decorators
Wrap a function to add behavior without modifying it. Common in AI code for timing, retries, caching, logging.

```python
import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timed
def run_inference(x):
    time.sleep(0.5)
    return x * 2

run_inference(5)  # prints: run_inference took 0.50s
```

A retry decorator (very common when calling flaky APIs):

```python
def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
            raise Exception("All retries failed")
        return wrapper
    return decorator

@retry(times=3)
def call_api():
    ...
```

### Context Managers (basic)
`with` blocks that guarantee setup/cleanup — used for file handles, DB connections, or timing/resource-tracking blocks in ML code.

```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Elapsed: {time.time() - self.start:.2f}s")

with Timer():
    time.sleep(1)
```

The simpler way, using `contextlib`:

```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")

with timer():
    time.sleep(1)
```

---

## How these tend to combine in real AI code

A realistic pattern pulling several of these together — a config dataclass, an abstract base class, async calls, and a decorator:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
import asyncio

@dataclass
class LLMConfig:
    model_name: str
    temperature: float = 0.7

class BaseLLM(ABC):
    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        ...

class MockLLM(BaseLLM):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.5)
        return f"[{self.config.model_name}] response to: {prompt}"

async def main():
    llm = MockLLM(LLMConfig(model_name="test-model"))
    results = await asyncio.gather(*[llm.generate(p) for p in ["hi", "bye"]])
    print(results)

asyncio.run(main())
```

If you want, I can turn this into a short set of practice exercises (e.g., "build a `Dataset` class with a generator-based batching method" or "write an async rate-limited API wrapper") so you can apply each concept rather than just read it.