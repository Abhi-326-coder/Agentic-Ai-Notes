# Python API Interaction

## The `requests` Library

`requests` is Python's standard HTTP client — the tool you use to actually make the calls described in the previous message.

### Basic GET

```python
import requests

response = requests.get("https://api.example.com/users/123")

print(response.status_code)  # 200
print(response.json())       # parsed dict from JSON body
print(response.headers)      # response headers
```

### Basic POST (this is 90% of what you'll do with LLM APIs)

```python
import requests

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": "sk-ant-api03-xxxxxxxx",
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    },
    json={
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": "Hello, Claude"}
        ]
    }
)

data = response.json()
print(data["content"][0]["text"])
```

Note: `json=` on `requests` does two things for you automatically — serializes your dict to a JSON string, and sets the `Content-Type: application/json` header. That's the convenience most people don't realize they're getting.

### Query params and path params in `requests`

```python
# Path parameter — just string-format it into the URL
user_id = 123
requests.get(f"https://api.example.com/users/{user_id}")

# Query parameters — pass as a dict, requests builds the ?key=value string
requests.get(
    "https://api.example.com/orders",
    params={"status": "shipped", "limit": 10}
)
# -> GET /orders?status=shipped&limit=10
```

### Checking for errors properly

```python
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
elif response.status_code == 401:
    print("Auth failed — check your API key")
elif response.status_code == 429:
    print("Rate limited — back off and retry")
else:
    print(f"Error {response.status_code}: {response.text}")

# Or the shortcut — raises an exception on any 4xx/5xx
response.raise_for_status()
```

### Timeouts (always set these — a hung request will hang your whole app)

```python
requests.post(url, json=payload, timeout=30)
```

---

## JSON Serialization / Deserialization

This is the translation layer between **Python objects** and **JSON text** (which is what actually travels over HTTP — HTTP bodies are just strings/bytes, not Python objects).

- **Serialization** = Python object → JSON string (you do this to *send* data)
- **Deserialization** = JSON string → Python object (you do this to *read* a response)

```python
import json

# Serialize: Python dict -> JSON string
payload = {"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "hi"}]}
json_string = json.dumps(payload)
# '{"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "hi"}]}'

# Deserialize: JSON string -> Python dict
raw = '{"id": "msg_123", "content": [{"type": "text", "text": "Hi there"}]}'
parsed = json.loads(raw)
print(parsed["content"][0]["text"])  # "Hi there"
```

**With `requests`, you rarely call `json.dumps`/`json.loads` manually**:
- `requests.post(url, json=payload)` — serializes for you
- `response.json()` — deserializes for you

You only reach for raw `json.dumps`/`json.loads` when working outside `requests` (e.g., reading a JSON file, building a JSON string manually, or a lower-level HTTP client).

### Type mapping to know

| Python | JSON |
|---|---|
| `dict` | object `{}` |
| `list` | array `[]` |
| `str` | string |
| `int`/`float` | number |
| `True`/`False` | `true`/`false` |
| `None` | `null` |

A common gotcha: JSON has no tuple, set, or datetime type. Serializing those directly throws `TypeError` — convert to list/string first.

```python
import datetime
json.dumps({"time": datetime.datetime.now()})  # ❌ TypeError
json.dumps({"time": datetime.datetime.now().isoformat()})  # ✅ works
```

---

## The Full Loop: User → Backend → LLM API → Response

This is the pattern almost every agentic backend follows. A minimal but complete version:

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ANTHROPIC_API_KEY = "sk-ant-api03-xxxxxxxx"

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Receive the user's request (deserialize JSON body Flask gives you)
    user_data = request.get_json()
    user_message = user_data["message"]

    # 2. Your backend calls the LLM API (serialize + POST)
    llm_response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": user_message}]
        },
        timeout=30
    )

    if llm_response.status_code != 200:
        return jsonify({"error": "LLM call failed"}), 502

    # 3. Deserialize the LLM's response
    llm_data = llm_response.json()
    reply_text = llm_data["content"][0]["text"]

    # 4. Serialize and send YOUR response back to the user
    return jsonify({"reply": reply_text})
```

Trace the arrows:

```
User's browser/app
      │  POST /chat  {"message": "hello"}     ← JSON serialized by the client
      ▼
Your Backend (Flask route above)
      │  deserializes request.get_json()
      │
      │  POST /v1/messages  {...}             ← your backend serializes this
      ▼
LLM API (Anthropic)
      │  returns JSON                          ← your backend deserializes response.json()
      ▼
Your Backend
      │  extracts reply_text, re-serializes as {"reply": ...}
      ▼
User's browser/app                              ← deserializes to display it
```

Every hop is: **serialize → HTTP request → HTTP response → deserialize**, repeated. Once you can write the Flask block above from memory and explain each line, you understand the core mechanics of an agentic backend.