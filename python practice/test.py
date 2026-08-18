class Model:
    def __init__(self, name):
        self.name = name

    def predict(self, x):
        raise NotImplementedError

# class LinearModel(Model):
#     def __init__(self, name, weights):
#         super().__init__(name)   # call parent's __init__
#         self.weights = weights

#     def predict(self, x):
#         return sum(w * xi for w, xi in zip(self.weights, x))

# m = Model("gpt")
# model = LinearModel(20)
# print(model.predict(8))

class LinearModel(Model):
    def predict(self, x): return "linear prediction"

class TreeModel(Model):
    def predict(self, x): return "tree prediction"

for m in [LinearModel("l"), TreeModel("t")]:
    print(m.predict(None))  # same call, different behavior


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