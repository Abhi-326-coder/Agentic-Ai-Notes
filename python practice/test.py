# def nums():
#     yield 1
#     yield 2
#     yield 3
    
# gen = nums()
# print(next(gen))
# print(next(gen))
# print(next(gen))

import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(2)
    print("World")

asyncio.run(hello())
# hello()

def add(a:int, b:int)->int :
    return a + b

from typing import List, Dict

user : Dict[str, str] = {
    
}
def add(a:int, b:int)->int:
    return a+b

user = {
    
}

from dataclasses import dataclass

@dataclass
class User:
    name:str
    age:int
    email:str

@dataclass
class Document:
    content:str
    source:str
    page:int

doc = Document(
    content="Python is...",
    source="python.pdf",
    page=10
)

def logger(func):
    def wrapper():
        print("Function started")
        func()
        print("function ended")
        
    return wrapper

@logger 
def hello():
    print("hello")
    
hello()