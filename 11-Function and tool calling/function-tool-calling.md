Absolutely. Since you’re learning **Agentic AI from the foundations upward**, Level 12 is a major milestone.

You already learned concepts like **LLMs, tokens, parameters, prompting, and structured outputs**. Now we connect them:

> **Structured output tells the LLM what format to return.**
> **Tool calling lets the LLM request an action from your application.**
> **Agents use tool calling + reasoning/decision-making + loops to accomplish tasks.**

Let's learn it like a mentor would teach you for both **real projects and interviews**.

---

# LEVEL 12 — Function Calling / Tool Calling

## 1. First: Why do we even need tools?

Imagine you ask an ordinary LLM:

> "What's the weather in Bangalore right now?"

An LLM has a problem.

The model itself doesn't inherently have access to the live weather.

Its normal flow is:

```text
User
  ↓
LLM
  ↓
Text response
```

It might say:

> "The weather in Bangalore is 24°C."

But where did that information come from?

It could be outdated or completely wrong.

The LLM needs access to an **external capability**.

For example:

```text
Weather API
Database
Calculator
Google Search
GitHub
Email
Calendar
Payment system
Your own backend
```

So we give the model **tools**.

Now the architecture becomes:

```text
User
  ↓
LLM
  ↓
Decides whether a tool is needed
  ↓
Tool call
  ↓
Your application executes tool
  ↓
Tool result
  ↓
LLM
  ↓
Final response
```

This is one of the fundamental patterns behind modern AI agents.

---

# 2. Function Calling vs Tool Calling

You'll hear both terms.

### Function calling

The model decides:

> "I want to call this function with these arguments."

Example:

```python
get_weather("Bangalore")
```

### Tool calling

This is the broader modern terminology.

A tool could be:

```text
Function
API
Database operation
Search engine
Code execution
Browser
File operation
MCP tool
```

So conceptually:

```text
Function calling ⊂ Tool calling
```

In practice, different AI frameworks/providers use slightly different terminology.

For Agentic AI, **tool calling** is the broader concept you should understand.

---

# 3. The Most Important Mental Model

This is the model I want you to remember.

## Normal LLM

```text
User
 ↓
LLM
 ↓
Text
```

## LLM with tools

```text
                  ┌──────────────┐
                  │     Tool     │
                  └──────▲───────┘
                         │
User → LLM → Tool Call ──┘
       │
       ↓
   Tool Result
       │
       ↓
      LLM
       │
       ↓
  Final Answer
```

The critical insight:

> **The LLM does not normally execute your function.**

The LLM **requests** a tool call.

Your application actually executes it.

This distinction is extremely important for interviews.

---

# 4. Example: Weather

User:

> "What's the weather in Bangalore?"

Suppose we provide this tool:

```python
get_weather(city)
```

The LLM might generate something conceptually like:

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Bangalore"
  }
}
```

Your application receives that.

Then your application executes:

```python
get_weather("Bangalore")
```

Suppose the tool returns:

```json
{
  "city": "Bangalore",
  "temperature": 24,
  "condition": "Cloudy"
}
```

That result goes back to the LLM.

Then the LLM produces:

> "It's currently 24°C and cloudy in Bangalore."

---

# 5. Very Important: The LLM isn't magically calling your function

This is probably the **#1 beginner misunderstanding**.

Suppose you have:

```python
def get_weather(city):
    return weather_api(city)
```

The LLM cannot simply reach into your Python process and execute:

```python
get_weather("Bangalore")
```

Instead:

```text
LLM
 ↓
"I want get_weather(city=Bangalore)"
 ↓
Your application
 ↓
Python executes get_weather()
 ↓
Result
 ↓
LLM
```

Think of the LLM as the **decision maker** and your program as the **executor**.

---

# 6. What is a Tool Schema?

Now we reach an important concept.

How does the LLM know what tools exist?

You provide a **tool definition/schema**.

For example:

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "Name of the city"
      }
    },
    "required": ["city"]
  }
}
```

This tells the model:

### Tool name

```text
get_weather
```

### What it does

```text
Get current weather for a city
```

### Arguments

```text
city
```

### Type

```text
string
```

### Required?

```text
yes
```

---

# 7. Why Tool Schemas Matter

Imagine giving the LLM this:

```text
Tool:
get_weather
```

That's not enough.

The model doesn't know:

```text
What arguments?
What types?
Which arguments are required?
What does the tool do?
```

A schema provides structure.

For example:

```json
{
  "name": "get_weather",
  "description": "Get current weather",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"]
  }
}
```

Now the LLM knows:

```text
Tool = get_weather

Input:
city → string
```

---

# 8. Tool Arguments

Suppose the user says:

> "What's the weather in Bangalore?"

The model needs to construct:

```json
{
  "city": "Bangalore"
}
```

These are the **tool arguments**.

Another example:

```python
search_products(
    query="wireless headphones",
    max_price=3000
)
```

Arguments:

```json
{
  "query": "wireless headphones",
  "max_price": 3000
}
```

---

# 9. Tool Result

After your application executes the tool, it produces a result.

Example:

```json
{
  "temperature": 25,
  "humidity": 72,
  "condition": "Cloudy"
}
```

That is the **tool result**.

The LLM then receives it and can interpret it.

---

# 10. Complete Tool-Calling Loop

This is the architecture you should memorize.

```text
User
 │
 │ "What's the weather in Bangalore?"
 ↓
LLM
 │
 │ decides:
 │ "I need weather tool"
 ↓
Tool Call
 │
 │ get_weather(city="Bangalore")
 ↓
Application
 │
 │ executes function
 ↓
Weather API
 │
 ↓
Tool Result
 │
 │ temperature=25
 ↓
LLM
 │
 ↓
Final Answer
```

Or mathematically:

```text
User
 ↓
Model
 ↓
Tool Request
 ↓
Tool Execution
 ↓
Tool Result
 ↓
Model
 ↓
Answer
```

---

# 11. Let's Build a Simple Tool Calling System

Let's first understand the architecture without depending heavily on a particular provider.

Imagine we have:

```python
def get_weather(city):
    weather_data = {
        "Bangalore": {
            "temperature": 24,
            "condition": "Cloudy"
        },
        "Mumbai": {
            "temperature": 29,
            "condition": "Rainy"
        }
    }

    return weather_data.get(city)
```

Our application has this function.

Now we give the LLM the tool definition.

Conceptually:

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string"
                }
            },
            "required": ["city"]
        }
    }
]
```

The user asks:

```text
What's the weather in Bangalore?
```

The model could return:

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Bangalore"
  }
}
```

Your application then does:

```python
result = get_weather("Bangalore")
```

Result:

```python
{
    "temperature": 24,
    "condition": "Cloudy"
}
```

Then send the result back to the model.

---

# 12. Multiple Tools

This is where things become much more interesting.

Suppose you create an AI assistant with:

```text
Tools:

1. get_weather
2. search_web
3. calculator
4. get_user_profile
5. send_email
6. create_calendar_event
```

User:

> "What's the weather in Bangalore?"

The LLM chooses:

```text
get_weather
```

User:

> "Calculate 500 * 23."

LLM chooses:

```text
calculator
```

User:

> "Send an email to Rahul saying the meeting is postponed."

LLM chooses:

```text
send_email
```

This is **tool selection**.

---

# 13. Tool Selection

The model essentially has to answer:

> "Which available tool, if any, should I use?"

Suppose tools are:

```text
search_web
calculator
weather
send_email
```

User:

> "What is 25% of 800?"

The model should choose:

```text
calculator
```

Not:

```text
search_web
```

This is why tool descriptions matter.

Bad description:

```text
calculator
```

Better:

```text
Calculate mathematical expressions accurately.
Use this tool for arithmetic operations.
```

Good tool descriptions improve tool selection.

---

# 14. Tool Calling Does NOT Mean Every Question Needs a Tool

Suppose user says:

> "Explain recursion."

No tool is required.

The model can simply answer:

```text
Recursion is...
```

But:

> "Calculate 128 × 47"

Could use:

```text
calculator
```

And:

> "What's today's weather?"

Could use:

```text
weather
```

So:

```text
                ┌── Tool needed → Tool call
User → LLM ─────┤
                └── No tool → Direct answer
```

This decision is extremely important in agent design.

---

# 15. Tool Calling vs API Calling

This distinction is frequently misunderstood.

### Traditional API application

You explicitly write:

```python
weather = get_weather("Bangalore")
```

You already know which API to call.

### Tool-calling AI application

You provide multiple tools:

```text
weather
calculator
search
email
database
```

Then the model determines which one is appropriate.

```text
User
 ↓
LLM
 ↓
"I need calculator"
 ↓
Application executes calculator
```

Therefore:

> **Tool calling adds model-driven tool selection on top of normal programmatic execution.**

---

# 16. Tool Errors

Real systems fail.

Suppose:

```python
get_weather("Bangalore")
```

calls an external API.

Maybe:

```text
API timeout
```

or:

```text
Invalid API key
```

or:

```text
City not found
```

Your tool might return:

```json
{
  "success": false,
  "error": "Weather API timeout"
}
```

Then the LLM receives the error.

It can respond:

> "I couldn't retrieve the weather right now because the weather service timed out."

Or potentially retry, depending on your agent architecture.

---

# 17. Tool Validation

This is extremely important in production.

Suppose the tool expects:

```json
{
  "city": "Bangalore"
}
```

But the model generates:

```json
{
  "city": 123
}
```

That's invalid.

Your application should validate the arguments.

For example, using Pydantic:

```python
from pydantic import BaseModel


class WeatherArgs(BaseModel):
    city: str
```

Then:

```python
args = WeatherArgs(**tool_arguments)
```

If the model sends:

```json
{
  "city": 123
}
```

Pydantic can validate/coerce or reject depending on configuration.

The key principle:

> **Never blindly trust model-generated arguments.**

LLMs generate probabilistic outputs.

Your application should enforce deterministic validation.

---

# 18. Why Your Previous Level — Structured Outputs — Matters

This is where Level 11 connects directly to Level 12.

You learned:

```text
JSON
JSON Schema
Pydantic
Structured Output
Validation
```

Now:

```text
Structured Output
       +
Tool Schema
       ↓
Reliable Tool Calling
```

For example:

```python
class SearchArgs(BaseModel):
    query: str
    max_results: int
```

The model might request:

```json
{
  "query": "latest AI research",
  "max_results": 5
}
```

Your application validates it.

Then executes:

```python
search_web(
    query="latest AI research",
    max_results=5
)
```

This is why structured outputs and tool calling are closely related.

---

# 19. Python Example — Simple Agent Loop

Let's build the conceptual version.

```python
def get_weather(city):
    data = {
        "Bangalore": {
            "temperature": 24,
            "condition": "Cloudy"
        }
    }

    return data.get(city)


tools = {
    "get_weather": get_weather
}
```

Suppose the LLM returns:

```python
tool_call = {
    "name": "get_weather",
    "arguments": {
        "city": "Bangalore"
    }
}
```

Your application does:

```python
tool_name = tool_call["name"]
arguments = tool_call["arguments"]

tool = tools[tool_name]

result = tool(**arguments)

print(result)
```

Output:

```text
{'temperature': 24, 'condition': 'Cloudy'}
```

Then:

```python
# Send result back to LLM
```

The model can produce:

```text
The weather in Bangalore is currently 24°C and cloudy.
```

That's the basic mechanism.

---

# 20. Tool Registry

As your application grows, you don't want:

```python
if tool == "weather":
    ...

elif tool == "calculator":
    ...

elif tool == "search":
    ...

elif tool == "email":
    ...
```

Instead, you can create a tool registry.

```python
tools = {
    "get_weather": get_weather,
    "calculator": calculator,
    "search_web": search_web,
    "send_email": send_email
}
```

Then:

```python
tool = tools[tool_name]

result = tool(**arguments)
```

This becomes much easier to scale.

---

# 21. Security Problem 🚨

This is where beginner tutorials often stop, but production Agentic AI cannot.

Imagine you have:

```text
send_email
delete_file
transfer_money
execute_code
database_update
```

The LLM decides:

```text
send_email(...)
```

Should your application blindly execute it?

**Absolutely not.**

Tool calling introduces a huge security boundary.

You need:

```text
LLM
 ↓
Tool request
 ↓
Validation
 ↓
Authorization
 ↓
Permission check
 ↓
Execution
```

For dangerous actions, you may need:

```text
Human approval
```

For example:

```text
User:
"Transfer ₹50,000 to Rahul."

LLM:
transfer_money(...)

Application:
⚠️ Confirmation required.

User:
Confirm.

Application:
Execute transaction.
```

This is called **human-in-the-loop**.

---

# 22. Read Tools vs Write Tools

A very useful production distinction.

### Read-only tools

They retrieve information.

Examples:

```text
get_weather()
search_web()
get_user()
get_order()
query_database()
```

Usually lower risk.

### Write/action tools

They change something.

Examples:

```text
send_email()
delete_file()
create_order()
transfer_money()
update_database()
```

Higher risk.

A good agent architecture treats them differently.

---

# 23. Multiple Tool Calls

Sometimes one tool isn't enough.

User:

> "Find the weather in Bangalore and calculate 25% of 800."

Potentially:

```text
LLM
 ↓
weather("Bangalore")
 ↓
Result

LLM
 ↓
calculator("800 * 0.25")
 ↓
Result

LLM
 ↓
Final answer
```

Or the model/framework may request multiple tool calls together, depending on the API and orchestration layer.

This is why you should understand:

```text
Single tool call
Multiple tool calls
Sequential tools
Parallel tools
```

---

# 24. Sequential Tool Calls

Some tasks require one tool's output to become another tool's input.

Example:

> "Find the current CEO of Company X and tell me their age."

Potential workflow:

```text
search_company("Company X")
        ↓
CEO = John
        ↓
search_person("John")
        ↓
Age = 47
        ↓
LLM
        ↓
Final answer
```

This is sequential tool use.

---

# 25. Parallel Tool Calls

Suppose user asks:

> "What's the weather in Bangalore, Mumbai and Delhi?"

There is no dependency between them.

You could do:

```text
weather(Bangalore) ──┐
                     │
weather(Mumbai) ─────┼──→ Results → LLM
                     │
weather(Delhi) ──────┘
```

These can potentially execute in parallel.

This reduces latency.

Production systems care a lot about this.

---

# 26. Tool Calling vs Agent

This is a very important interview question.

### Tool calling

The model can request tools.

Example:

```text
LLM → weather → result → LLM
```

### Agent

An agent is a broader system that can:

```text
Observe
↓
Decide
↓
Act
↓
Observe result
↓
Decide again
↓
Act again
```

For example:

```text
User
 ↓
Agent
 ↓
Search web
 ↓
Observe result
 ↓
Search another source
 ↓
Observe result
 ↓
Calculate
 ↓
Observe result
 ↓
Generate final answer
```

So:

> **Tool calling is a capability. An agent is a system that can use capabilities/tools to pursue a goal, often across multiple steps.**

This distinction is excellent for interviews.

---

# 27. The Agent Loop

Memorize this.

```text
        ┌───────────────┐
        │     User      │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │      LLM      │
        └───────┬───────┘
                ↓
          Need a tool?
           /        \
         No          Yes
         ↓            ↓
      Answer       Tool Call
                       ↓
                 Tool Execution
                       ↓
                  Tool Result
                       ↓
                      LLM
                       │
                       └──────→ repeat
```

This loop is the heart of many agent architectures.

---

# 28. A More Realistic Example — AI Shopping Agent

Imagine you're building:

> **AI Shopping Assistant**

Tools:

```text
search_products()
get_product_details()
check_inventory()
calculate_shipping()
create_order()
```

User:

> "Find me a laptop under ₹70,000 with 16GB RAM."

Agent:

```text
LLM
 ↓
search_products(
    query="laptop",
    max_price=70000,
    ram="16GB"
)
 ↓
Results
 ↓
LLM
 ↓
Maybe get_product_details()
 ↓
Results
 ↓
LLM
 ↓
Final recommendation
```

Then user:

> "Buy the second one."

Now:

```text
LLM
 ↓
check_inventory()
 ↓
Result
 ↓
LLM
 ↓
create_order()
 ↓
Potential human confirmation
 ↓
Order created
```

This is a genuine agentic workflow.

---

# 29. Another Example — Coding Agent

Imagine a coding agent has:

```text
read_file()
write_file()
search_code()
run_tests()
run_terminal()
```

User:

> "Fix the failing login test."

Agent:

```text
LLM
 ↓
search_code("login")
 ↓
Result
 ↓
read_file("auth.py")
 ↓
Result
 ↓
LLM analyzes
 ↓
write_file(...)
 ↓
run_tests()
 ↓
Test fails
 ↓
LLM analyzes again
 ↓
write_file(...)
 ↓
run_tests()
 ↓
Tests pass
 ↓
Final answer
```

Notice what's happening.

The LLM isn't just generating text.

It is:

```text
Observe
↓
Decide
↓
Act
↓
Observe
↓
Decide
↓
Act
```

That's agentic behavior.

---

# 30. Function Calling Example Using Pydantic

Here's a simplified design.

```python
from pydantic import BaseModel


class WeatherArgs(BaseModel):
    city: str


def get_weather(args: WeatherArgs):
    data = {
        "Bangalore": {
            "temperature": 24,
            "condition": "Cloudy"
        },
        "Mumbai": {
            "temperature": 29,
            "condition": "Rainy"
        }
    }

    return data.get(args.city)
```

Now suppose the model gives:

```python
raw_arguments = {
    "city": "Bangalore"
}
```

Validate:

```python
args = WeatherArgs(**raw_arguments)
```

Execute:

```python
result = get_weather(args)
```

This gives you:

```text
LLM-generated arguments
        ↓
Pydantic validation
        ↓
Typed Python object
        ↓
Function execution
```

This pattern is very useful in production systems.

---

# 31. Tool Validation Layers

A robust system can have several layers.

```text
LLM
 ↓
Schema validation
 ↓
Argument validation
 ↓
Authentication
 ↓
Authorization
 ↓
Business rules
 ↓
Tool execution
 ↓
Result validation
 ↓
LLM
```

For example:

```text
LLM says:

transfer_money(
    from="A",
    to="B",
    amount=1000000
)
```

Your backend should check:

```text
Is the user authenticated?
        ↓
Does the user have permission?
        ↓
Is the account valid?
        ↓
Is amount within limits?
        ↓
Does balance exist?
        ↓
Does transaction require confirmation?
        ↓
Execute
```

**Never allow the LLM to bypass your backend's security rules.**

---

# 32. Tool Result Design

Don't return giant messy text if structured data is possible.

Bad:

```text
The weather service says that currently Bangalore is
experiencing cloudy weather and the temperature appears
to be around 24 degrees...
```

Better:

```json
{
  "city": "Bangalore",
  "temperature_c": 24,
  "condition": "Cloudy"
}
```

Structured results are easier for the LLM to interpret reliably.

---

# 33. Tool Errors Should Also Be Structured

Instead of:

```text
ERROR!!!
```

use:

```json
{
  "success": false,
  "error_code": "CITY_NOT_FOUND",
  "message": "Could not find the requested city."
}
```

Or:

```json
{
  "success": false,
  "error_code": "API_TIMEOUT",
  "retryable": true
}
```

Now your agent can reason about the failure.

---

# 34. Retry Logic

Suppose:

```text
Tool
 ↓
Timeout
```

The agent may retry.

But don't blindly retry forever.

You might implement:

```python
MAX_RETRIES = 3
```

Architecture:

```text
Tool
 ↓
Failure
 ↓
Retry?
 ├── Yes → Tool
 └── No → Error handling
```

Production agents need:

```text
timeouts
retries
rate limits
fallbacks
logging
monitoring
```

---

# 35. Tool Calling and Hallucination

Tool calling can reduce some hallucinations, but it doesn't eliminate them.

Without tools:

```text
"What is my account balance?"
```

LLM might hallucinate:

> "Your balance is ₹25,000."

With a database tool:

```text
get_balance(user_id)
```

the system can retrieve the real value.

But the model can still:

```text
choose the wrong tool
generate wrong arguments
misinterpret tool results
make unsupported conclusions
```

Therefore:

> **Tools improve grounding, but tool calling itself is not a guarantee of correctness.**

---

# 36. Tool Descriptions Are Part of Prompt Engineering

This connects directly to your Level 10.

Consider:

```text
Tool:
search()
```

versus:

```text
Tool:
search_web(query)

Description:
Search the internet for current information.
Use this when the user asks about recent events,
current information, or facts that may have changed.
Do not use it for basic arithmetic.
```

The second description gives the model much better guidance.

Therefore:

```text
Prompt Engineering
        +
Tool Descriptions
        +
Schemas
        ↓
Better tool selection
```

---

# 37. Tool Calling and MCP

You'll eventually encounter **MCP — Model Context Protocol**.

Don't dive deeply into it yet, but understand the relationship.

Traditional:

```text
Application
 ↓
LLM
 ↓
Tools defined directly in application
```

MCP provides a standardized way for AI applications to discover and interact with tools/resources from external servers.

Conceptually:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tools / Resources
```

So MCP is related to the **tool ecosystem and interoperability**, while function/tool calling is the fundamental mechanism by which a model can request tool use.

You don't need to master MCP yet.

---

# 38. Interview Question: What is Function Calling?

A strong answer:

> Function calling is a capability where an LLM generates a structured request to invoke a predefined function or tool, including the required arguments. The application—not the LLM itself—validates those arguments, executes the function, and sends the result back to the model so it can generate the final response.

That's a very good interview answer.

---

# 39. Interview Question: Does the LLM execute the function?

**Answer: No.**

The LLM generates a tool call.

Your application executes it.

```text
LLM
 ↓
Tool request
 ↓
Application
 ↓
Function execution
```

This distinction is critical.

---

# 40. Interview Question: What is a Tool Schema?

Answer:

> A tool schema describes a tool's name, purpose, input parameters, parameter types, and required fields so the model knows when and how to request that tool.

Example:

```json
{
  "name": "get_weather",
  "parameters": {
    "city": {
      "type": "string"
    }
  }
}
```

---

# 41. Interview Question: Why use JSON Schema?

Because LLM outputs are probabilistic.

You want:

```text
Predictable structure
+
Validation
+
Type information
+
Required fields
```

Instead of:

```text
"maybe Bangalore weather..."
```

you want:

```json
{
  "city": "Bangalore"
}
```

---

# 42. Interview Question: How would you handle invalid tool arguments?

A good answer:

> I would validate tool arguments against a strict schema before execution. If validation fails, I would reject the call or return a structured validation error. I would also enforce application-level authorization and business rules independently of the model.

This last sentence is particularly important.

---

# 43. Interview Question: How do you secure tool calling?

Mention:

```text
Authentication
Authorization
Input validation
Output validation
Rate limiting
Timeouts
Audit logging
Least privilege
Human approval
Sandboxing
```

For example:

```text
LLM
 ↓
Tool request
 ↓
Schema validation
 ↓
Permission check
 ↓
Business rules
 ↓
Human confirmation if necessary
 ↓
Execution
```

---

# 44. Interview Question: What happens if a tool fails?

Answer:

> The tool should return a structured error. The agent can then decide whether to retry, use a fallback tool, ask the user for clarification, or gracefully report the failure.

Example:

```json
{
  "success": false,
  "error_code": "TIMEOUT",
  "retryable": true
}
```

---

# 45. Interview Question: Tool Calling vs RAG

Very important.

### RAG

Retrieves information.

```text
Question
 ↓
Retriever
 ↓
Documents
 ↓
LLM
```

### Tool calling

Allows the model to invoke an external capability.

```text
Question
 ↓
LLM
 ↓
Tool
 ↓
Result
 ↓
LLM
```

They can be combined.

For example:

```text
Agent
 ├── RAG search
 ├── Database tool
 ├── Web search
 └── Calculator
```

---

# 46. Tool Calling vs Structured Output

Another important interview question.

### Structured output

Controls the **format of the model's response**.

```json
{
  "name": "Abhishek",
  "score": 90
}
```

### Tool calling

Allows the model to **request an external action**.

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Bangalore"
  }
}
```

Relationship:

```text
Structured Outputs
       ↓
Reliable structured data

Tool Calling
       ↓
Structured requests for actions
```

---

# 47. Tool Calling vs Prompt Engineering

Prompt engineering:

```text
Tell the model what to do.
```

Tool calling:

```text
Give the model capabilities it can request.
```

Together:

```text
System Instructions
       +
Context
       +
Tool Definitions
       +
User Request
       ↓
LLM
       ↓
Decision
```

---

# 48. The Biggest Concept You Should Understand

Here's the progression you've been learning.

### Level 7

```text
LLM
```

### Level 8

```text
Tokens
```

### Level 9

```text
LLM Parameters
```

### Level 10

```text
Prompt Engineering
```

### Level 11

```text
Structured Outputs
```

### Level 12

```text
Tool Calling
```

And now:

```text
LLM
 ↓
Structured Decision
 ↓
Tool
 ↓
External World
 ↓
Result
 ↓
LLM
```

This is where an LLM starts becoming useful as a **system component**, rather than merely a text generator.

---

# 49. Your First Mental Model for Agents

Don't think:

> "An agent is an LLM that is super intelligent."

Think:

> **An agent is an application architecture in which an LLM can decide what actions to take, invoke tools, observe results, and continue until the task is complete or it needs human input.**

For example:

```text
                  ┌─────────────┐
                  │     LLM     │
                  └──────┬──────┘
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
           Search     Database   Calculator
              │          │          │
              └──────────┼──────────┘
                         ↓
                       Result
                         ↓
                        LLM
                         ↓
                    Final Answer
```

That's the architecture you should have in your head.

---

# 50. A Mini Project You Should Build

Since you're learning Agentic AI, **don't just read this**.

Build a tiny:

## 🤖 Personal AI Assistant

Give it these tools:

```text
1. calculator()
2. get_weather()
3. search_notes()
4. get_current_time()
```

Then ask:

```text
"What is 25% of 800?"
```

→ calculator

```text
"What is the weather in Bangalore?"
```

→ weather

```text
"Find my notes about Transformers."
```

→ search_notes

```text
"What time is it?"
```

→ time

And:

```text
"Explain what Transformers are."
```

→ no tool

Then make it more advanced:

```text
User
 ↓
LLM
 ↓
Tool selection
 ↓
Argument validation
 ↓
Tool execution
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

Once this works, you've built the **core mechanism of an agent** yourself.

---

# 51. Your Learning Checklist for Level 12

You should be able to explain all of these without notes:

### Fundamentals

* [ ] What is function calling?
* [ ] What is tool calling?
* [ ] Why do LLMs need tools?
* [ ] LLM vs tool-enabled LLM
* [ ] Tool schema
* [ ] Tool arguments
* [ ] Tool result
* [ ] Tool selection
* [ ] Tool execution

### Engineering

* [ ] Multiple tools
* [ ] Sequential tool calls
* [ ] Parallel tool calls
* [ ] Tool validation
* [ ] Tool errors
* [ ] Retry logic
* [ ] Tool result design
* [ ] Tool registry

### Production

* [ ] Authentication
* [ ] Authorization
* [ ] Input validation
* [ ] Output validation
* [ ] Rate limiting
* [ ] Timeouts
* [ ] Logging
* [ ] Human-in-the-loop
* [ ] Least privilege
* [ ] Dangerous tools

### Agentic AI

* [ ] Agent loop
* [ ] Observe → Decide → Act
* [ ] Tool calling vs agents
* [ ] Tool calling + RAG
* [ ] Tool calling + structured outputs
* [ ] Basic understanding of MCP

---

# 🎯 The One Diagram I Want You to Remember

```text
                         USER
                           │
                           ▼
                    ┌────────────┐
                    │    LLM     │
                    └─────┬──────┘
                          │
                 "Do I need a tool?"
                     /           \
                   NO             YES
                   │               │
                   ▼               ▼
               Answer        Tool Selection
                                   │
                                   ▼
                            Tool Arguments
                                   │
                                   ▼
                            VALIDATION
                                   │
                                   ▼
                            AUTHORIZATION
                                   │
                                   ▼
                           TOOL EXECUTION
                                   │
                                   ▼
                              TOOL RESULT
                                   │
                                   ▼
                                  LLM
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                     Need more?            Done
                         │                   │
                         └──→ Tool            ▼
                               loop        FINAL ANSWER
```

If you understand this diagram deeply, you've understood the **core of Level 12**.

And notice something important: **the LLM isn't the entire agent**.

The agent is the **whole system around the LLM**—tools, execution, validation, state, loops, permissions, and the model's decision-making.

That's the mental shift from **"learning LLMs" → "building Agentic AI systems."**

Next, the natural Level 13 after this is **Agents & Agent Loops**, where we'll take this exact tool-calling mechanism and learn **ReAct, planning, observation, action loops, memory/state, stopping conditions, and multi-step agents**.
