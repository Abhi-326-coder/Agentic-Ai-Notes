# 🚀 LEVEL 14 — ReAct

## 1. First understand the problem

A normal LLM works roughly like this:

```text
User
 ↓
LLM
 ↓
Answer
```

For example:

```text
User:
What is the population of India?

        ↓

LLM:
India has approximately 1.4 billion people.
```

The problem is that the LLM may **not actually know the latest information**.

An agent can instead do:

```text
User
 ↓
Reason
 ↓
Choose tool
 ↓
Act
 ↓
Observe result
 ↓
Reason again
 ↓
Choose another tool
 ↓
Observe
 ↓
Final answer
```

This is the basic idea behind **ReAct**.

---

# 2. What does ReAct mean?

**ReAct = Reason + Act**

The core loop is:

```text
Reason
  ↓
Act
  ↓
Observe
  ↓
Reason
  ↓
Act
  ↓
Observe
  ↓
...
```

The important insight is:

> An agent doesn't necessarily solve the entire problem in one LLM call.

Instead, it can **think about what information/action is needed, use a tool, inspect the result, and decide what to do next.**

---

# 3. Simple real-world analogy

Imagine you ask a human assistant:

> "Find out whether I should carry an umbrella tomorrow."

The assistant might do:

```text
Question
   ↓
"I need tomorrow's weather."
   ↓
Check weather app
   ↓
"70% chance of rain."
   ↓
"Rain probability is high."
   ↓
Recommend umbrella
```

That's essentially an agent loop.

---

# 4. ReAct architecture

A simplified architecture looks like:

```text
                  ┌──────────────┐
                  │    User      │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │     LLM      │
                  │   Reason     │
                  └──────┬───────┘
                         ↓
                   Choose Action
                         ↓
                  ┌──────────────┐
                  │     Tool     │
                  │ Search/DB/API│
                  └──────┬───────┘
                         ↓
                     Observation
                         ↓
                  ┌──────────────┐
                  │     LLM      │
                  │ Re-evaluate  │
                  └──────┬───────┘
                         ↓
                    Another action?
                     ↙         ↘
                   Yes          No
                    ↓            ↓
                  Tool       Final Answer
```

---

# 5. The three important components

You should remember these three words:

### Reason

The model determines:

> "What do I need to do?"

### Act

The model invokes a tool.

Examples:

```text
search()
calculator()
database()
weather_api()
send_email()
```

### Observe

The agent receives the tool's result.

Example:

```text
Search result:
India's population is approximately ...
```

Then the model reasons again.

---

# 6. Example: Calculator agent

Suppose the user asks:

> What is 27 × 43 + 100?

A simple LLM could calculate internally.

But imagine we want an agent that uses a calculator.

The flow becomes:

```text
User
 ↓
"What is 27 × 43 + 100?"
 ↓
Reason
 ↓
"I should use calculator."
 ↓
Act
 ↓
calculator("27 * 43 + 100")
 ↓
Observe
 ↓
1261
 ↓
Reason
 ↓
"I have the answer."
 ↓
Final answer
 ↓
1261
```

---

# 7. Minimal Python implementation

Before LangChain, I want you to understand the **concept without abstraction**.

We can simulate an agent:

```python
def calculator(expression):
    return eval(expression)


question = "What is 27 * 43 + 100?"

print("User:", question)

# Reason
print("Agent: I need a calculator.")

# Act
result = calculator("27 * 43 + 100")

# Observe
print("Tool result:", result)

# Reason
print("Agent: I now have the answer.")

# Final answer
print("Answer:", result)
```

Output:

```text
User: What is 27 * 43 + 100?

Agent: I need a calculator.

Tool result: 1261

Agent: I now have the answer.

Answer: 1261
```

This isn't a production ReAct agent, but it demonstrates the **core loop**.

---

# 8. A more interesting example

Suppose:

> "What is the population of India divided by 10?"

Now the agent needs **two steps**.

```text
User
 ↓
Question
 ↓
Reason
 ↓
Need India's population
 ↓
Search tool
 ↓
Observation
 ↓
Population = X
 ↓
Reason
 ↓
Need X / 10
 ↓
Calculator
 ↓
Observation
 ↓
Result
 ↓
Final answer
```

Notice something important:

### The second action depends on the first observation.

That's one of the most important concepts in agentic systems.

---

# 9. ReAct is NOT simply "thinking"

This is an important interview distinction.

People sometimes say:

> "ReAct means the AI thinks."

That's incomplete.

ReAct is about **interleaving reasoning/decision-making with actions and observations**.

Conceptually:

```text
Reason → Act → Observe → Reason → Act → Observe
```

The **Act + Observe** part is what allows the model to interact with the outside world.

---

# 10. ReAct vs normal LLM

| Normal LLM                   | ReAct Agent                   |
| ---------------------------- | ----------------------------- |
| User → LLM → Answer          | User → Agent loop             |
| Usually one generation       | Multiple steps possible       |
| No external tools by default | Can use tools                 |
| Static knowledge/context     | Can obtain new information    |
| No environment interaction   | Can interact with environment |
| Simple tasks                 | Multi-step tasks              |

---

# 11. ReAct with tools

Imagine your agent has:

```python
tools = [
    search,
    calculator,
    database,
    weather
]
```

The LLM receives the question:

```text
What's the weather in Bengaluru and
convert the temperature from Celsius to Fahrenheit?
```

The agent could do:

```text
Reason:
I need weather information.

Act:
weather("Bengaluru")

Observe:
Temperature = 28°C

Reason:
I need to convert 28°C to Fahrenheit.

Act:
calculator("(28 * 9/5) + 32")

Observe:
82.4°F

Reason:
I have everything.

Final:
The temperature is 28°C (82.4°F).
```

That's a genuine **multi-step agentic workflow**.

---

# 12. Where LangChain comes in

Eventually, you don't want to manually write:

```python
reason()
act()
observe()
reason()
act()
```

Frameworks such as LangChain/LangGraph provide abstractions for building these workflows.

Conceptually:

```text
LLM
 ↓
Tool selection
 ↓
Tool execution
 ↓
Tool result
 ↓
LLM
 ↓
Tool selection
 ↓
...
```

But **don't learn the framework first**.

You should understand:

```text
LLM
Tool
Tool call
Observation
State
Loop
Termination
```

Then LangChain becomes much easier.

---

# 13. ReAct interview question

### Q: What is ReAct?

A strong answer:

> **ReAct stands for Reasoning and Acting. It is an agentic approach where an LLM interleaves decision-making with tool actions and observations. The model determines what action is needed, invokes an appropriate tool, receives the result, and uses that observation to decide the next step. This loop continues until the agent has enough information to produce a final answer.**

That's a good interview answer.

---

# 14. Why is ReAct useful?

Because many real-world tasks aren't:

```text
Input → Answer
```

They are:

```text
Input
 ↓
Understand
 ↓
Find information
 ↓
Perform operation
 ↓
Check result
 ↓
Perform another operation
 ↓
Generate answer
```

Examples:

### Research agent

```text
Question
 ↓
Search web
 ↓
Read articles
 ↓
Compare information
 ↓
Search missing information
 ↓
Summarize
```

### Coding agent

```text
User request
 ↓
Inspect repository
 ↓
Find relevant file
 ↓
Modify code
 ↓
Run tests
 ↓
Observe failure
 ↓
Fix code
 ↓
Run tests again
 ↓
Final result
```

### Customer support agent

```text
Customer question
 ↓
Check customer database
 ↓
Observe account status
 ↓
Check order database
 ↓
Observe order status
 ↓
Respond
```

That's why ReAct is fundamental to agentic AI.

---

# 15. ReAct limitation

There is an important issue.

More steps mean:

```text
More LLM calls
      ↓
More latency
      ↓
More cost
      ↓
More opportunities for errors
```

For example:

```text
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
LLM
```

can become expensive.

So production agents need:

* step limits
* timeouts
* tool validation
* error handling
* retries
* stopping conditions
* observability

---

# 🧠 LEVEL 15 — AGENT MEMORY

Now we reach another **very important agentic AI concept**.

The question is:

> How does an agent remember things?

---

# 16. The simplest chatbot

Imagine:

```text
User:
My name is Abhishek.

LLM:
Nice to meet you!

```

Then:

```text
User:
What's my name?

LLM:
I don't know.
```

Why?

Because an LLM doesn't automatically possess permanent memory of every conversation.

---

# 17. Conversation history

The simplest solution is:

```text
messages = [
    User: My name is Abhishek,
    Assistant: Nice to meet you!
]
```

Then when the next message arrives:

```text
User:
What's my name?
```

we send the history:

```text
[
    User: My name is Abhishek.
    Assistant: Nice to meet you.
    User: What's my name?
]
```

The LLM can then answer:

```text
Abhishek.
```

This is **conversation history**.

---

# 18. Important distinction

You should understand this carefully:

> **Conversation history is not exactly the same thing as memory.**

Conversation history is the messages that occurred.

Memory is information that the system decides to **retain, manage, retrieve, or use later**.

For example:

```text
Conversation history:

User:
My name is Abhishek.

Assistant:
Nice to meet you.

User:
I am learning Agentic AI.

Assistant:
Great!

User:
Explain RAG.
```

A memory system might extract:

```text
User facts:

name = Abhishek
interest = Agentic AI
```

and store them separately.

---

# 19. Short-term memory

Short-term memory means:

> Information available during the current interaction/task.

For example:

```text
User:
My name is Abhishek.

Agent:
Nice to meet you.

User:
I'm learning Python.

Agent:
Great.

User:
What am I learning?

Agent:
Python.
```

The agent remembers because the relevant context is still available.

Conceptually:

```text
Conversation
      ↓
Current state
      ↓
LLM
```

---

# 20. Short-term memory = state

In modern agent architectures, you'll frequently hear:

> **State**

State represents information the agent needs while executing a task.

For example:

```python
state = {
    "user_name": "Abhishek",
    "query": "Find flights to Delhi",
    "search_results": [],
    "selected_flight": None
}
```

As the agent works:

```text
Initial state
 ↓
Search flights
 ↓
Update state
 ↓
Compare flights
 ↓
Update state
 ↓
Choose flight
 ↓
Final state
```

So:

> **State is the working information of the agent during execution.**

---

# 21. Example of agent state

Suppose we're building a shopping agent.

Initial:

```python
state = {
    "query": "laptop under ₹70,000",
    "products": [],
    "selected_product": None
}
```

After searching:

```python
state = {
    "query": "laptop under ₹70,000",
    "products": [
        "Laptop A",
        "Laptop B",
        "Laptop C"
    ],
    "selected_product": None
}
```

After analysis:

```python
state = {
    "query": "laptop under ₹70,000",
    "products": [
        "Laptop A",
        "Laptop B",
        "Laptop C"
    ],
    "selected_product": "Laptop B"
}
```

The state allows different agent steps to share information.

---

# 22. Long-term memory

Now imagine the conversation ends.

Tomorrow:

```text
User:
What's my name?
```

If the system still knows:

```text
Abhishek
```

that's persistent/long-term memory.

Conceptually:

```text
Conversation
     ↓
Extract useful information
     ↓
Memory Store
     ↓
Database / Vector DB / KV store
```

Later:

```text
New conversation
     ↓
Retrieve relevant memory
     ↓
LLM
     ↓
Personalized response
```

---

# 23. Short-term vs long-term memory

This is a very common interview question.

| Short-term                    | Long-term                  |
| ----------------------------- | -------------------------- |
| Current task/conversation     | Across conversations       |
| Temporary                     | Persistent                 |
| Usually held in state/context | Stored externally          |
| Conversation history          | Database/vector store/etc. |
| Lost when state is discarded  | Can survive sessions       |

Think:

```text
Short-term:

"My current working memory"


Long-term:

"My stored knowledge about the user"
```

---

# 24. Where is long-term memory stored?

There isn't one mandatory technology.

Depending on the application, you might use:

### SQL database

```text
PostgreSQL
MySQL
```

Good for structured information.

Example:

```text
user_id | name     | language
123     | Abhishek | Hindi
```

### Key-value store

```text
Redis
```

Good for fast retrieval/state.

### Vector database

```text
Pinecone
Weaviate
Qdrant
FAISS
```

Useful when memory is semantic.

For example:

```text
User previously said:
"I prefer learning through practical examples."
```

Later:

```text
Retrieve memories related to:
"How should I explain this?"
```

Semantic retrieval can find that preference.

---

# 25. Memory doesn't mean "store everything"

This is extremely important.

Bad architecture:

```text
Store every message forever
```

Better:

```text
Conversation
     ↓
Identify useful information
     ↓
Decide whether worth remembering
     ↓
Store memory
```

For example:

```text
User:
What's 2 + 2?

```

Probably not useful as long-term memory.

But:

```text
User:
I'm building an agriculture AI assistant.
```

might be useful for future conversations about that project.

---

# 26. Persistent memory

Persistent memory means the information survives beyond the current execution/session.

Example:

```text
Session 1
──────────────

User:
I prefer Java examples.

       ↓

Memory Store

language_preference = Java
```

Later:

```text
Session 2
──────────────

User:
Explain recursion.

       ↓

Retrieve memory

language_preference = Java

       ↓

Agent

Explain recursion using Java.
```

---

# 27. Context management

Now we reach a **very important practical concept**.

LLMs have a finite context window.

Suppose a conversation becomes:

```text
Message 1
Message 2
Message 3
...
Message 10,000
```

You can't blindly keep sending everything forever.

So agents need **context management**.

---

# 28. Context management techniques

Common techniques include:

### 1. Truncation

Keep only recent messages.

```text
Old messages ❌
Recent messages ✅
```

Example:

```python
messages = messages[-10:]
```

---

### 2. Summarization

Instead of keeping 100 messages:

```text
Message 1
Message 2
...
Message 100
```

create:

```text
Summary:

User is building an agriculture AI assistant.
They want multilingual voice interaction.
They are using Python for backend development.
```

Then:

```text
Summary + recent messages
```

go to the LLM.

---

### 3. Retrieval

Store information externally.

```text
Huge history
     ↓
Memory database
     ↓
Retrieve relevant information
     ↓
LLM context
```

This is closely related to **RAG**.

---

# 29. Memory architecture

A simplified production architecture could look like:

```text
                 USER
                   ↓
              ┌─────────┐
              │  Agent  │
              └────┬────┘
                   ↓
            ┌──────────────┐
            │ Current State│
            └──────┬───────┘
                   ↓
            ┌──────────────┐
            │ Memory Layer │
            └──────┬───────┘
                   ↓
       ┌───────────┴───────────┐
       ↓                       ↓
 Short-term                Long-term
   State                    Memory
       ↓                       ↓
 Current task             DB / Vector DB
       └───────────┬───────────┘
                   ↓
                  LLM
```

---

# 30. Let's build a tiny memory system

We can implement simple persistent memory ourselves.

```python
memory = {}

def remember(key, value):
    memory[key] = value

def recall(key):
    return memory.get(key)
```

Now:

```python
remember("name", "Abhishek")
remember("language", "Python")
```

Later:

```python
print(recall("name"))
```

Output:

```text
Abhishek
```

This demonstrates the fundamental idea.

---

# 31. Conversation memory

Let's make it slightly more realistic.

```python
conversation = []

def add_message(role, message):
    conversation.append({
        "role": role,
        "content": message
    })


add_message("user", "My name is Abhishek.")
add_message("assistant", "Nice to meet you!")

print(conversation)
```

Conceptually:

```text
conversation
     ↓
[
  {
    role: "user",
    content: "My name is Abhishek."
  },
  {
    role: "assistant",
    content: "Nice to meet you!"
  }
]
```

When another question comes:

```python
add_message("user", "What's my name?")
```

the model can receive the conversation.

---

# 32. Memory + ReAct together

Now combine Levels 14 and 15.

Imagine:

> "Find a good laptop for me."

The agent might know from memory:

```text
User preference:
Budget = ₹70,000
Preferred OS = Windows
```

Then:

```text
User
 ↓
Agent
 ↓
Retrieve memory
 ↓
User preferences
 ↓
Reason
 ↓
Search laptops
 ↓
Observe results
 ↓
Reason
 ↓
Compare products
 ↓
Final answer
```

This is much closer to a real agent.

---

# 33. Agent architecture you've learned so far

You should now visualize an agent as:

```text
                         USER
                           ↓
                    ┌─────────────┐
                    │    AGENT    │
                    └──────┬──────┘
                           ↓
                  ┌────────────────┐
                  │      STATE     │
                  └───────┬────────┘
                          ↓
                  ┌───────────────┐
                  │     MEMORY    │
                  └───────┬───────┘
                          ↓
                       ┌─────┐
                       │ LLM │
                       └──┬──┘
                          ↓
                       REASON
                          ↓
                        ACT
                          ↓
                       TOOL
                          ↓
                     OBSERVE
                          ↓
                        STATE
                          ↓
                        LLM
                          ↓
                   Continue / Stop
```

That is the mental model I want you to develop.

---

# 34. Very important terminology

You should be comfortable with these terms:

### Context

Information provided to the LLM for the current generation.

```text
Prompt
+
Conversation
+
Retrieved information
+
Tool results
```

---

### Conversation History

Previous messages in the conversation.

```text
User → Assistant → User → Assistant
```

---

### State

Information required to track the current execution/task.

```python
{
    "query": "...",
    "results": [],
    "current_step": 2
}
```

---

### Short-term memory

Information available during the current session/task.

---

### Long-term memory

Information persisted beyond the current session.

---

### Persistent memory

Memory stored somewhere durable so it can be retrieved later.

---

### Context management

Techniques used to control what information is sent to the LLM.

Examples:

```text
Truncation
Summarization
Retrieval
Filtering
Compression
```

---

# 35. Interview questions you should prepare

## Q1. What is ReAct?

**Answer:**

> ReAct is an agentic pattern that combines reasoning and acting. The LLM decides which action to take, executes a tool, observes the result, and then uses that result to determine the next action or produce the final answer.

---

## Q2. What is the ReAct loop?

```text
Reason
 ↓
Act
 ↓
Observe
 ↓
Reason
 ↓
Act
 ↓
Observe
```

---

## Q3. Why do agents need tools?

Because LLMs alone may not have:

* real-time information
* access to databases
* ability to perform external actions
* deterministic computation
* access to private systems

Tools extend the capabilities of the LLM.

---

## Q4. What is short-term memory?

> Short-term memory is information maintained within the current conversation or task execution, commonly represented through conversation history and agent state.

---

## Q5. What is long-term memory?

> Long-term memory is information persisted outside the current conversation so that it can be retrieved and reused in future sessions.

---

## Q6. Difference between state and memory?

This is a **good interview question**.

Think:

```text
State = current execution information

Memory = information retained for future/current use
```

Example:

```text
State:

current_query = "Find flights"
search_results = [...]
selected_flight = None
```

Memory:

```text
User prefers window seats.
User usually flies from Bengaluru.
```

State is primarily about **what the agent is doing now**.

Memory is about **what information should be retained/recalled**.

---

# 36. ReAct vs RAG

Don't confuse these.

### RAG

```text
Question
 ↓
Retrieve information
 ↓
LLM
 ↓
Answer
```

### ReAct

```text
Question
 ↓
Reason
 ↓
Tool
 ↓
Observe
 ↓
Reason
 ↓
Another tool
 ↓
Observe
 ↓
Answer
```

RAG is primarily a **knowledge retrieval pattern**.

ReAct is an **action/decision loop**.

They can also be combined:

```text
Agent
 ↓
Reason
 ↓
RAG retrieval
 ↓
Observe
 ↓
Reason
 ↓
API
 ↓
Observe
 ↓
Answer
```

---

# 37. ReAct + Memory + RAG

This is where things start becoming really interesting.

A sophisticated agent can have:

```text
                   USER
                     ↓
                   AGENT
                     ↓
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Memory       Tools       RAG
          ↓          ↓          ↓
          └──────────┼──────────┘
                     ↓
                    LLM
                     ↓
                  Decision
                     ↓
                  Action
                     ↓
                 Observation
                     ↓
                   State
                     ↓
                 Continue
```

This is much closer to what you'll encounter in actual Agentic AI systems.

---

# 38. What you should NOT memorize

Don't memorize something like:

```text
ReAct = a specific LangChain class
```

That is framework knowledge, not conceptual knowledge.

Instead remember:

> **ReAct is a pattern where an LLM repeatedly decides what to do, takes an action through a tool, observes the result, and uses that result to decide what to do next.**

And:

> **Memory allows an agent to retain and retrieve useful information beyond a single model generation.**

Those two definitions will survive even when frameworks change.

---

# 🎯 Your mental model after Level 15

If I ask you:

> "What makes an AI system an agent?"

You should start thinking:

```text
LLM
 │
 ├── Tools
 │
 ├── State
 │
 ├── Memory
 │
 ├── Planning / Decision-making
 │
 └── Feedback loop
        │
        ↓
   Reason → Act → Observe
```

And when I ask:

> "How does it remember?"

You should think:

```text
Current conversation
        ↓
Short-term state/history
        ↓
Context management

Persistent information
        ↓
Long-term memory
        ↓
Database / vector store
```

---

# 🧪 Mini Project — Build before moving ahead

I strongly recommend that you build this tiny agent yourself before moving to the next level.

### Project: Personal Research Agent

Give it three tools:

```text
1. calculator()
2. search()
3. memory()
```

And make it capable of:

```text
User:
My name is Abhishek.

Agent:
I'll remember that.

User:
What is 25 * 42?

Agent:
Uses calculator.

User:
What is my name?

Agent:
Retrieves memory.

User:
Find information about LangChain and
tell me how many letters are in its name.

Agent:
Search → Observe → Calculator → Observe → Answer
```

The architecture should be:

```text
                 USER
                   ↓
                 AGENT
                   ↓
                REASON
                   ↓
          ┌────────┼────────┐
          ↓        ↓        ↓
     Calculator  Search   Memory
          ↓        ↓        ↓
          └────────┼────────┘
                   ↓
                OBSERVE
                   ↓
                 REASON
                   ↓
              FINAL ANSWER
```

**Once you can build and explain that without blindly copying a framework, you're genuinely understanding Agentic AI rather than just learning LangChain APIs.**
