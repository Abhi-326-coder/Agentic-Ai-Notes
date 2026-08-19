# def nums():
#     yield 1
#     yield 2
#     yield 3
    
# gen = nums()
# print(next(gen))
# print(next(gen))
# print(next(gen))

# import asyncio

# async def hello():
#     print("Hello")
#     await asyncio.sleep(2)
#     print("World")

# asyncio.run(hello())
# # hello()

# def add(a:int, b:int)->int :
#     return a + b

# from typing import List, Dict

# user : Dict[str, str] = {
    
# }
# def add(a:int, b:int)->int:
#     return a+b

# user = {
    
# }

# from dataclasses import dataclass

# @dataclass
# class User:
#     name:str
#     age:int
#     email:str

# @dataclass
# class Document:
#     content:str
#     source:str
#     page:int

# doc = Document(
#     content="Python is...",
#     source="python.pdf",
#     page=10
# )

# def logger(func):
#     def wrapper():
#         print("Function started")
#         func()
#         print("function ended")
        
#     return wrapper

# @logger 
# def hello():
#     print("hello")
    
# hello()

# import requests, os
# from dotenv import load_dotenv
# load_dotenv()

# api_key = os.getenv("ANTHROPIC_API_KEY")
# response = requests.post(
#     "https://api.anthropic.com/v1/messages",
#     headers={
#         "x-api-key": api_key,
#         "content-type": "application/json",
#         "anthropic-version": "2023-06-01"
#     },
#     json={
#         "model": "claude-sonnet-4-6",
#         "max_tokens": 1000,
#         "messages": [
#             {"role": "user", "content": "Hello, Claude"}
#         ]
#     }
# )

# data = response.json()
# print(data)
# print(data["content"][0]["text"])

# import requests

# user_id = 123
# response = requests.get(f"https://api.example.com/users/{user_id}")

# requests.get(
#     "https://api.example.com/orders",
#     params={"status":"shipped", "limit":10}
# )

# if response.status_code == 200:
#     data = response.json()
# elif response.status_code == 401:
#     print("Auth failed - check your api key")

# requests.post(url, json=payload, timeout=30)
# response.raise_for_status()

import json

# Serialize: Python dict -> JSON string
payload = {"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "hi"}]}
json_string = json.dumps(payload)
# '{"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "hi"}]}'

# Deserialize: JSON string -> Python dict
raw = '{"id": "msg_123", "content": [{"type": "text", "text": "Hi there"}]}'
parsed = json.loads(raw)
print(parsed["content"][0]["text"])  # "Hi there"