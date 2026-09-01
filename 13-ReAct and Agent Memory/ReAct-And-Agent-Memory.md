🚀 LEVEL 14 — ReAct
1. First understand the problem

A normal LLM works roughly like this:

User
 ↓
LLM
 ↓
Answer

For example:

User:
What is the population of India?

        ↓

LLM:
India has approximately 1.4 billion people.

The problem is that the LLM may not actually know the latest information.

An agent can instead do:

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

This is the basic idea behind ReAct.

2. What does ReAct mean?

ReAct = Reason + Act

The core loop is:

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

The important insight is:

An agent doesn't necessarily solve the entire problem in one LLM call.

Instead, it can think about what information/action is needed, use a tool, inspect the result, and decide what to do next.

3. Simple real-world analogy

Imagine you ask a human assistant:

"Find out whether I should carry an umbrella tomorrow."

The assistant might do:

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

That's essentially an agent loop.

4. ReAct architecture

A simplified architecture looks like:

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
5. The three important components

You should remember these three words:

Reason

The model determines:

"What do I need to do?"

Act

The model invokes a tool.

Examples:

search()
calculator()
database()
weather_api()
send_email()
Observe

The agent receives the tool's result.

Example:

Search result:
India's population is approximately ...

Then the model reasons again.

6. Example: Calculator agent

Suppose the user asks:

What is 27 × 43 + 100?

A simple LLM could calculate internally.

But imagine we want an agent that uses a calculator.

The flow becomes:

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
7. Minimal Python implementation

Before LangChain, I want you to understand the concept without abstraction.

We can simulate an agent:

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

Output:

User: What is 27 * 43 + 100?

Agent: I need a calculator.

Tool result: 1261

Agent: I now have the answer.

Answer: 1261

This isn't a production ReAct agent, but it demonstrates the core loop.

8. A more interesting example

Suppose:

"What is the population of India divided by 10?"

Now the agent needs two steps.

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

Notice something important:

The second action depends on the first observation.

That's one of the most important concepts in agentic systems.

9. ReAct is NOT simply "thinking"

This is an important interview distinction.

People sometimes say:

"ReAct means the AI thinks."

That's incomplete.

ReAct is about interleaving reasoning/decision-making with actions and observations.

Conceptually:

Reason → Act → Observe → Reason → Act → Observe

The Act + Observe part is what allows the model to interact with the outside world.

10. ReAct vs normal LLM
Normal LLM	ReAct Agent
User → LLM → Answer	User → Agent loop
Usually one generation	Multiple steps possible
No external tools by default	Can use tools
Static knowledge/context	Can obtain new information
No environment interaction	Can interact with environment
Simple tasks	Multi-step tasks
11. ReAct with tools

Imagine your agent has:

tools = [
    search,
    calculator,
    database,
    weather
]

The LLM receives the question:

What's the weather in Bengaluru and
convert the temperature from Celsius to Fahrenheit?

The agent could do:

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

That's a genuine multi-step agentic workflow.

12. Where LangChain comes in

Eventually, you don't want to manually write:

reason()
act()
observe()
reason()
act()

Frameworks such as LangChain/LangGraph provide abstractions for building these workflows.

Conceptually:

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

But don't learn the framework first.

You should understand:

LLM
Tool
Tool call
Observation
State
Loop
Termination

Then LangChain becomes much easier.

13. ReAct interview question
Q: What is ReAct?

A strong answer:

ReAct stands for Reasoning and Acting. It is an agentic approach where an LLM interleaves decision-making with tool actions and observations. The model determines what action is needed, invokes an appropriate tool, receives the result, and uses that observation to decide the next step. This loop continues until the agent has enough information to produce a final answer.

That's a good interview answer.

14. Why is ReAct useful?

Because many real-world tasks aren't:

Input → Answer

They are:

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

Examples:

Research agent
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
Coding agent
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
Customer support agent
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

That's why ReAct is fundamental to agentic AI.

15. ReAct limitation

There is an important issue.

More steps mean:

More LLM calls
      ↓
More latency
      ↓
More cost
      ↓
More opportunities for errors

For example:

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

can become expensive.

So production agents need:

step limits
timeouts
tool validation
error handling
retries
stopping conditions
observability