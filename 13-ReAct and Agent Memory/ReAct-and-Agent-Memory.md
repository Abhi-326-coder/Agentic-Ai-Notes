# 🚀 LangChain — Level 1: What Problem Does It Solve?

Now we begin the **LangChain portion** of your roadmap.

And we're going to do this differently from a typical tutorial.

You already built a MiniAgent from scratch, so we'll use it as our reference implementation throughout.

---

# 1. First: What Is LangChain?

At the simplest level:

> **LangChain is a framework that provides abstractions and integrations for building applications around LLMs.**

It gives you standardized components for things like:

```text
Models
Messages
Prompts
Tools
Tool calling
Structured output
Agents
Retrieval
Memory/state
Tracing
```

Instead of manually writing every integration yourself, you can use LangChain's abstractions.

But here's the important distinction:

### LangChain is NOT the LLM.

```text
Gemini
   ↓
LLM
```

LangChain sits around the model:

```text
                Your Application
                       │
                   LangChain
              ┌────────┼────────┐
              ↓        ↓        ↓
           Model     Tools    Agents
              │
              ↓
           Gemini
```

---

# 2. Your MiniAgent vs LangChain

You already built:

```text id="6m7i7f"
mini-agent/
│
├── GeminiLLM
├── Tool schemas
├── Tool registry
├── Tool executor
├── Agent loop
├── State
├── Memory
└── Parser
```

LangChain gives you abstractions for many of these.

Conceptually:

| Your MiniAgent    | LangChain                |
| ----------------- | ------------------------ |
| `GeminiLLM`       | Chat model               |
| `types.Content`   | Messages                 |
| Tool schema       | Tool                     |
| `ToolManager`     | Tool system              |
| Agent loop        | Agent runtime            |
| Structured output | Structured output APIs   |
| Call parsing      | Tool-call abstraction    |
| Callbacks/logger  | Callbacks/tracing        |
| State/memory      | Message/state mechanisms |

The exact mapping isn't always one-to-one, but this mental model is useful.

---

# 3. Our First Goal

We're **not** going to build an agent immediately.

First we'll learn:

```text
LangChain
   ↓
Model
   ↓
Messages
   ↓
Prompt
   ↓
Tool
   ↓
Structured output
```

Then we'll combine them into an agent.

This is important because otherwise you'll write:

```python
create_agent(...)
```

and have absolutely no idea what's happening underneath.

---

# 4. Create a Separate LangChain Project

Don't destroy your MiniAgent.

Keep it.

I'd restructure your repository like:

```text id="9h5qpx"
agent-learning/
│
├── mini-agent/
│   └── ...
│
└── langchain-agent/
    └── ...
```

Your MiniAgent becomes your **reference implementation**.

Whenever we learn something in LangChain, we'll compare it against that project.

---

# 5. Create the LangChain Environment

Inside:

```text id="qz78st"
langchain-agent/
```

create:

```text id="lyz5uo"
langchain-agent/
│
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

Install the current LangChain core and Google Gemini integration:

```bash id="zjmy2u"
pip install -U langchain langchain-google-genai python-dotenv
```

LangChain's official Python docs currently separate the core framework from provider integrations; Gemini is provided through `langchain-google-genai`.

---

# 6. Environment Variable

Your `.env`:

```env id="4iv9zi"
GOOGLE_API_KEY=your_gemini_api_key
```

Don't commit this.

Your `.gitignore`:

```gitignore id="k8qf0r"
.env
__pycache__/
.venv/
```

---

# 7. Your First LangChain Program

Open:

```text id="q8g3os"
main.py
```

Write:

```python id="n7u6jv"
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)


response = model.invoke(
    "What is an AI agent?"
)


print(response.content)
```

Run:

```bash id="j3x6hc"
python main.py
```

You should get a normal Gemini response.

---

# 8. What Did LangChain Actually Do?

This:

```python id="l4h7qm"
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)
```

creates a LangChain **chat model**.

Then:

```python id="x0p0fz"
model.invoke(...)
```

runs it.

Compare that with your MiniAgent:

```python id="o1h3m5"
client.models.generate_content(
    model="gemini-2.5-flash",
    contents=...
)
```

You were directly using Google's SDK.

Now:

```text id="wzjz4u"
Your code
   ↓
LangChain
   ↓
Google Gemini integration
   ↓
Gemini API
```

LangChain is providing a standardized interface around the provider.

---

# 9. The First Important LangChain Concept: Messages

Instead of treating everything as strings, LangChain has message abstractions.

The common ones you'll encounter are:

```text id="0t4m4w"
SystemMessage
HumanMessage
AIMessage
ToolMessage
```

Conceptually:

```text id="c0cxv6"
SystemMessage
    ↓
Instructions

HumanMessage
    ↓
User

AIMessage
    ↓
Model

ToolMessage
    ↓
Tool result
```

Notice something?

You already built this concept manually.

Your Gemini contents were effectively representing:

```text id="z4t9p3"
user
 ↓
model
 ↓
function call
 ↓
function response
```

LangChain gives you standardized message objects for this kind of interaction.

---

# 10. Try Messages

Change `main.py`:

```python id="7qj0n1"
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)


messages = [
    SystemMessage(
        content="You are a helpful AI tutor."
    ),
    HumanMessage(
        content="Explain AI agents in simple terms."
    ),
]


response = model.invoke(messages)


print(response.content)
```

Run:

```bash id="s3f4ep"
python main.py
```

---

# 11. Why `SystemMessage`?

Compare:

```text id="h7up83"
SystemMessage
"You are a helpful AI tutor."
```

with:

```text id="k8h6sc"
HumanMessage
"Explain AI agents."
```

They're different roles.

The model sees something conceptually like:

```text id="6l0wmm"
SYSTEM:
You are a helpful AI tutor.

USER:
Explain AI agents in simple terms.
```

This is why messages are more powerful than simply doing:

```python
prompt = "..."
```

---

# 12. Compare With Your MiniAgent

Your old code:

```python id="1yq7h9"
types.Content(
    role="user",
    parts=[
        types.Part.from_text(
            text=user_message
        )
    ]
)
```

LangChain:

```python id="z8p1n6"
HumanMessage(
    content=user_message
)
```

Conceptually:

```text id="1wz8hl"
Your implementation
        ↓
Gemini-specific Content

LangChain
        ↓
Provider-independent Message
```

That's one of the major reasons frameworks are useful.

---

# 13. The Next Concept: Tools

Now we get to something you already understand extremely well.

You created:

```text id="f0ry0e"
calculator
time
random_number
```

In LangChain, tools can be represented using the `@tool` decorator.

Create:

```text id="u5xwz3"
tools.py
```

Put:

```python id="jj0k6q"
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:
        return str(eval(expression))
    except Exception as error:
        return f"Calculation failed: {error}"


@tool
def random_number(minimum: int, maximum: int) -> int:
    """Generate a random integer between minimum and maximum."""

    import random

    if minimum > maximum:
        raise ValueError(
            "minimum cannot be greater than maximum."
        )

    return random.randint(
        minimum,
        maximum
    )
```

Notice:

```python id="3j5oxf"
@tool
```

That's doing a lot of work.

---

# 14. What Does `@tool` Actually Mean?

When you write:

```python id="4t1fvo"
@tool
def random_number(
    minimum: int,
    maximum: int
) -> int:
```

LangChain can derive information from:

```text id="5s4d4d"
Function name
       ↓
Type hints
       ↓
Docstring
       ↓
Tool schema
```

So your function:

```python id="v9n8z1"
random_number(minimum: int, maximum: int)
```

becomes a tool object that can expose:

```text id="5u8uwj"
Name:
random_number

Description:
Generate a random integer...

Arguments:
minimum: integer
maximum: integer
```

---

# 15. Compare This With What You Built

Your MiniAgent required:

```text id="7t6o6k"
schemas.py
       ↓
arguments.py
       ↓
registry.py
       ↓
formatters.py
       ↓
executor.py
```

LangChain:

```python id="2q2qgf"
@tool
def random_number(
    minimum: int,
    maximum: int
):
```

That's a **massive abstraction**.

LangChain is effectively saying:

> "Give me a properly typed Python function and I'll help turn it into a tool."

This is one of the first places where you can clearly see what a framework buys you.

---

# 16. Inspect the Tool

Add:

```python id="6c17dg"
print(random_number.name)
print(random_number.description)
print(random_number.args_schema)
```

So:

```python id="ihvym8"
from tools import random_number


print("Name:")
print(random_number.name)

print("\nDescription:")
print(random_number.description)

print("\nArguments:")
print(random_number.args_schema)
```

Run:

```bash id="1k9e7d"
python main.py
```

You should see information describing the tool's schema.

---

# 17. This Is the Part I Want You to Understand

Before LangChain:

```text id="f2o5jy"
Python Function
      ↓
You manually create schema
      ↓
Registry
      ↓
Formatter
      ↓
LLM
```

With LangChain:

```text id="qf2y5x"
Python Function
      ↓
@tool
      ↓
LangChain Tool
      ↓
LLM
```

LangChain didn't invent tool calling.

**You already implemented tool calling.**

LangChain is providing a standardized abstraction around it.

That's the distinction I want you to keep throughout this entire section.

---

# 18. Bind Tools to Gemini

Now we connect our tools to the model.

Create:

```text id="qk4wqk"
main.py
```

with:

```python id="cm6h5d"
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from tools import (
    calculator,
    random_number,
)


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)


tools = [
    calculator,
    random_number,
]


model_with_tools = model.bind_tools(
    tools
)


response = model_with_tools.invoke(
    "What is 25 multiplied by 4?"
)


print(response)
```

---

# 19. What Does `bind_tools()` Do?

This:

```python id="5ikgqz"
model.bind_tools(tools)
```

doesn't execute the tools.

It tells the model:

```text id="f3d4p8"
These tools are available.
```

Conceptually:

```text id="h6f4q1"
Gemini
  ↑
  │
Tool definitions
  │
  ├── calculator
  └── random_number
```

The model can then decide:

```text id="8pnj5b"
User:
What is 25 × 4?

Gemini:
I should call calculator.
```

Sound familiar?

That's exactly what your MiniAgent did.

---

# 20. Inspect the Response

Instead of:

```python id="x8z8c9"
print(response)
```

try:

```python id="9jz5g8"
print("CONTENT:")
print(response.content)

print("\nTOOL CALLS:")
print(response.tool_calls)
```

You should see something conceptually similar to:

```text id="9oz6cy"
CONTENT:

TOOL CALLS:

[
    {
        "name": "calculator",
        "args": {
            "expression": "25 * 4"
        },
        "id": "..."
    }
]
```

The exact representation can vary with LangChain/provider versions.

---

# 21. Look at the Similarity

Your MiniAgent:

```python id="4cc8f0"
tool_calls = get_tool_calls(response)
```

LangChain:

```python id="j5h24a"
response.tool_calls
```

You manually wrote:

```python id="e1h0mb"
json.loads(...)
```

LangChain handles the provider-specific representation and exposes a standardized structure.

That's abstraction.

---

# 22. But We Still Haven't Built an Agent

Right now:

```text id="9d2jca"
User
 ↓
Gemini
 ↓
Tool call
```

We still need:

```text id="y2j3hp"
Tool call
 ↓
Execute
 ↓
ToolMessage
 ↓
Gemini
 ↓
Final answer
```

You already implemented this manually.

So the next thing we'll do is build the LangChain version.

---

# 23. Your First LangChain Learning Checkpoint

At this point, you should understand:

### `ChatGoogleGenerativeAI`

```text
LangChain's Gemini model integration
```

### `invoke()`

```text
Send input to the model
```

### `SystemMessage`

```text
Model/application instructions
```

### `HumanMessage`

```text
User input
```

### `AIMessage`

```text
Model response
```

### `@tool`

```text
Turn a Python function into a LangChain tool
```

### `bind_tools()`

```text
Make tools available to the model
```

### `response.tool_calls`

```text
Structured representation of requested tool calls
```

---

# 🎯 Your Exercise

Before we continue, modify your LangChain project to include **all three** of your MiniAgent tools:

```text id="o8uh1g"
calculator
time
random_number
```

For example:

```python id="d2b8ct"
@tool
def time():
    """Return the current date and time."""
    ...
```

Then:

```python id="q2ijif"
tools = [
    calculator,
    time,
    random_number,
]

model_with_tools = model.bind_tools(tools)
```

Test:

```text id="z4s1bk"
What is 45 * 12?
```

Then:

```text id="bx0b44"
Generate a random number between 1 and 100.
```

Then:

```text id="c8r5ut"
What time is it?
```

And inspect:

```python id="i8gyj1"
print(response.tool_calls)
```

You should be able to see which tool Gemini requested.

---

# 🚀 What We'll Do Next

Next is **LangChain Level 2 — Actually Build the Agent**.

We'll take:

```text id="i7r1xn"
model
   +
tools
```

and build:

```text id="n8l1o2"
                USER
                  ↓
               AGENT
                  ↓
                LLM
                  ↓
             Tool call?
             ↙       ↘
           YES        NO
            ↓          ↓
          TOOL       ANSWER
            ↓
       Tool result
            ↓
        LLM again
            ↓
          ANSWER
```

Then we'll put your **MiniAgent and LangChain agent side-by-side**.

That's when you'll see very clearly:

> **"Ah — LangChain didn't make agents possible. It packaged the pieces I just built manually."**

And after that we'll move to **LangGraph**, where the question changes from:

> *"How do I call tools?"*

to:

> **"How do I orchestrate a stateful, branching, looping workflow?"**

That's the bridge you're ultimately aiming for.
