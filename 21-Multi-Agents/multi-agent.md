# LEVEL 26 — Multi-Agent Systems 🤖🤖🤖

You are now at one of the most important parts of Agentic AI.

You've already learned:

```text
Level 24 → LangChain
Level 25 → LangGraph
Level 26 → Multi-Agent Systems
```

And you've completed the LangGraph projects through:

```text
State
→ Tools
→ Multi-tools
→ Agentic RAG
→ Persistence
→ HITL
→ Streaming
→ Reliability
→ Durable execution
→ Subgraphs
```

So you're ready for this.

One important principle before we start:

> **Multi-agent does NOT automatically mean better.**

A single agent with good tools can often solve a problem more simply. Multiple agents become useful when responsibilities, context, tools, reasoning strategies, or ownership need to be separated.

Current LangGraph describes itself as a low-level orchestration framework for long-running, stateful agents and supports persistence, streaming, human-in-the-loop, and durable execution—the capabilities we're going to combine here. ([LangChain AI][1])

---

# 1. First: What is an Agent?

Before multi-agent, make sure your definition of an agent is solid.

A simplified agent:

```text
USER
 ↓
LLM
 ↓
Decision
 ↓
Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Decision
 ↓
...
```

For example:

```text
User:
"What's the weather in Bengaluru?"

        ↓

LLM

        ↓

Decides:
"I need weather tool"

        ↓

Weather Tool

        ↓

"28°C"

        ↓

LLM

        ↓

"Currently Bengaluru is 28°C."
```

One agent is responsible for everything.

---

# 2. Single Agent Architecture

```text
                  SINGLE AGENT
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Research        Coding         Database
      Tools           Tools           Tools
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                      LLM
                       ↓
                    Answer
```

This can work extremely well.

For example, your AI assistant might have:

```text
Tools:
- web_search
- calculator
- database
- email
- weather
- calendar
```

The LLM decides which tool to use.

---

# 3. So why do we need multiple agents?

Imagine you ask:

> "Research Tesla's latest technology developments, analyze the engineering implications, write a technical report, and review it for factual consistency."

That's multiple responsibilities:

```text
Research
Analysis
Writing
Review
```

You could give one agent:

```text
20 tools
10 instructions
huge context
many responsibilities
```

But eventually you get:

```text
┌───────────────────────────────┐
│           ONE AGENT           │
│                               │
│ Research                      │
│ Coding                        │
│ Analysis                      │
│ Writing                       │
│ Testing                       │
│ Review                        │
│ Database                      │
│ Web                           │
│ ...                           │
└───────────────────────────────┘
```

The agent has to reason about everything.

Instead:

```text
                    SUPERVISOR
                         │
             ┌───────────┼───────────┐
             ↓           ↓           ↓
          Research      Code       Writer
           Agent        Agent       Agent
             │           │           │
             └───────────┼───────────┘
                         ↓
                       Final
```

Now each agent has a narrower responsibility.

---

# 4. The first critical distinction

You need to understand these two architectures:

### Single agent + multiple tools

```text
             AGENT
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
    Search   Database  Calculator
```

### Multiple agents

```text
           SUPERVISOR
          /     |      \
         ↓      ↓       ↓
    Research  Coding  Writer
```

They are **not the same thing**.

---

# 5. Single agent vs multi-agent

| Single Agent                 | Multi-Agent               |
| ---------------------------- | ------------------------- |
| One reasoning loop           | Multiple reasoning loops  |
| Many tools                   | Specialized tools/context |
| Simple architecture          | More complex architecture |
| Easier debugging             | Harder debugging          |
| Lower orchestration overhead | More coordination         |
| Good for focused tasks       | Good for decomposed tasks |
| Shared context naturally     | Context can be isolated   |

Don't jump to multi-agent just because it sounds more advanced.

---

# 6. When should you use Multi-Agent?

A good rule:

Use multiple agents when there is a **meaningful separation of responsibility**.

For example:

```text
Research agent
```

needs:

```text
Search
Browser
Retrieval
Citation
```

while:

```text
Coding agent
```

needs:

```text
Code execution
Files
Git
Testing
```

and:

```text
Review agent
```

needs:

```text
Evaluation
Critique
Validation
```

Their tools and prompts are fundamentally different.

That's a good multi-agent problem.

---

# 7. Your Level 26 roadmap

We're going to learn this in layers.

```text
LEVEL 26
│
├── 1. Single Agent
│
├── 2. Why Multi-Agent?
│
├── 3. Worker Agents
│
├── 4. Supervisor Agent
│
├── 5. Agent Routing
│
├── 6. Agent Delegation
│
├── 7. Agent Communication
│
├── 8. Shared State
│
├── 9. Sequential Agents
│
├── 10. Parallel Agents
│
├── 11. Hierarchical Agents
│
├── 12. Human-in-the-Loop
│
├── 13. Multi-Agent Failure Handling
│
├── 14. Multi-Agent Memory
│
├── 15. Multi-Agent Production Architecture
│
└── 16. Interview Patterns
```

We'll use **one evolving project** throughout the lesson.

---

# 8. Our main project

Let's build:

# 🧠 AI Software Development Team

User says:

> "Build a REST API for a student management system."

Instead of one agent doing everything:

```text
USER
 ↓
ONE AGENT
 ↓
everything
```

we'll create:

```text
                   SUPERVISOR
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      Research       Coding       Review
       Agent          Agent        Agent
          │            │            │
          └────────────┼────────────┘
                       ↓
                     FINAL
```

Later we'll add:

```text
Testing Agent
Documentation Agent
Security Agent
```

---

# 9. Worker Agent

A **worker agent** is a specialized agent that performs a specific responsibility delegated by another component.

Example:

```text
Research Agent
```

might receive:

```text
"Find information about JWT authentication."
```

and return:

```text
"JWT uses three components:
header, payload, signature..."
```

It doesn't need to manage the whole project.

---

# 10. Supervisor Agent

The supervisor coordinates workers.

Conceptually:

```text
                 SUPERVISOR
                     │
              Understand task
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Research    Coding     Review
          │          │          │
          └──────────┼──────────┘
                     ↓
                 Final answer
```

The supervisor's job is **coordination**, not necessarily doing all the work itself.

---

# 11. Agent Routing

The supervisor needs to answer:

> "Which worker should handle this?"

For example:

```text
User request
      │
      ▼
 Supervisor
      │
      ├── research?
      │       ↓
      │    Research Agent
      │
      ├── coding?
      │       ↓
      │    Coding Agent
      │
      └── review?
              ↓
          Review Agent
```

This is **agent routing**.

---

# 12. Routing can be deterministic

Suppose:

```python
def route(task):

    if "research" in task:
        return "research"

    if "code" in task:
        return "coding"

    return "review"
```

This is deterministic.

You don't necessarily need an LLM.

This is an important engineering principle:

> **Use deterministic routing when the routing rules are known and reliable.**

---

# 13. Routing can also be LLM-based

Suppose the user says:

> "Investigate how authentication should work and then implement it."

It's not as simple as keyword matching.

The supervisor LLM can decide:

```text
First → Research Agent

Then → Coding Agent
```

This is agentic routing.

---

# 14. Our first multi-agent architecture

Let's build a simple version:

```text
USER
 ↓
SUPERVISOR
 ↓
 ┌───────────────┐
 │               │
Research       Coding
Agent           Agent
 │               │
 └───────┬───────┘
         ↓
       FINAL
```

---

# 15. State

Let's define shared state:

```python
from typing import TypedDict


class TeamState(TypedDict):

    task: str

    research_result: str

    code_result: str

    final_answer: str
```

State:

```text
task
research_result
code_result
final_answer
```

---

# 16. Research Worker

```python
def research_agent(state: TeamState):

    print("🔎 Research Agent working...")

    result = (
        "JWT authentication uses a signed token "
        "containing header, payload and signature."
    )

    return {
        "research_result": result
    }
```

This is our first specialized worker.

---

# 17. Coding Worker

```python
def coding_agent(state: TeamState):

    print("💻 Coding Agent working...")

    code = """
@app.post("/login")
def login():
    return {"token": "example"}
"""

    return {
        "code_result": code
    }
```

---

# 18. Supervisor

For our first implementation, keep the supervisor deterministic.

```python
def supervisor(state: TeamState):

    task = state["task"].lower()

    if "research" in task:
        return {
            "next": "research"
        }

    if "code" in task:
        return {
            "next": "coding"
        }

    return {
        "next": "research"
    }
```

But there's a problem.

Our state doesn't currently have:

```python
next
```

So let's add it.

```python
class TeamState(TypedDict):

    task: str

    next: str

    research_result: str

    code_result: str

    final_answer: str
```

---

# 19. Router

Now:

```python
def route_from_supervisor(state: TeamState):

    return state["next"]
```

Then:

```python
builder.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    {
        "research": "research",
        "coding": "coding"
    }
)
```

This gives us:

```text
                 SUPERVISOR
                 /         \
                /           \
               ↓             ↓
          RESEARCH         CODING
```

---

# 20. Add final node

```python
def final_node(state: TeamState):

    result = (
        f"Research:\n{state['research_result']}\n\n"
        f"Code:\n{state['code_result']}"
    )

    return {
        "final_answer": result
    }
```

Then:

```python
builder.add_edge(
    "research",
    "final"
)

builder.add_edge(
    "coding",
    "final"
)

builder.add_edge(
    "final",
    END
)
```

---

# 21. Complete basic graph

```python
from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


class TeamState(TypedDict):

    task: str

    next: str

    research_result: str

    code_result: str

    final_answer: str


# ==========================================
# SUPERVISOR
# ==========================================

def supervisor(state: TeamState):

    task = state["task"].lower()

    if "research" in task:
        return {
            "next": "research"
        }

    if "code" in task:
        return {
            "next": "coding"
        }

    return {
        "next": "research"
    }


# ==========================================
# RESEARCH AGENT
# ==========================================

def research_agent(state: TeamState):

    print("🔎 Research Agent")

    return {
        "research_result": (
            "JWT consists of header, payload, signature."
        )
    }


# ==========================================
# CODING AGENT
# ==========================================

def coding_agent(state: TeamState):

    print("💻 Coding Agent")

    return {
        "code_result": """
@app.post("/login")
def login():
    return {"token": "example"}
"""
    }


# ==========================================
# ROUTER
# ==========================================

def route(state: TeamState):

    return state["next"]


# ==========================================
# FINAL
# ==========================================

def final_node(state: TeamState):

    return {
        "final_answer": (
            f"Research:\n{state['research_result']}\n\n"
            f"Code:\n{state['code_result']}"
        )
    }


# ==========================================
# GRAPH
# ==========================================

builder = StateGraph(TeamState)

builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "research",
    research_agent
)

builder.add_node(
    "coding",
    coding_agent
)

builder.add_node(
    "final",
    final_node
)


builder.add_edge(
    START,
    "supervisor"
)


builder.add_conditional_edges(
    "supervisor",
    route,
    {
        "research": "research",
        "coding": "coding"
    }
)


builder.add_edge(
    "research",
    "final"
)

builder.add_edge(
    "coding",
    "final"
)

builder.add_edge(
    "final",
    END
)


graph = builder.compile()
```

---

# 22. Run it

```python
result = graph.invoke(
    {
        "task": "research JWT authentication",
        "next": "",
        "research_result": "",
        "code_result": "",
        "final_answer": ""
    }
)

print(result)
```

Flow:

```text
START
 ↓
SUPERVISOR
 ↓
RESEARCH
 ↓
FINAL
 ↓
END
```

If:

```python
task = "write code for JWT authentication"
```

then:

```text
START
 ↓
SUPERVISOR
 ↓
CODING
 ↓
FINAL
 ↓
END
```

This is your first multi-agent routing system.

---

# 23. But this isn't yet a true LLM supervisor

Exactly.

We've created the architecture first.

Now we can replace:

```python
if "research" in task:
```

with an LLM decision.

This is an important learning technique:

> **First understand orchestration deterministically. Then introduce LLM reasoning.**

Otherwise beginners often don't know whether a bug came from:

```text
LLM
or
Graph
or
Router
or
State
```

---

# 24. LLM Supervisor

We can ask Gemini to return structured routing information.

For example:

```python
from pydantic import BaseModel
from typing import Literal


class RouteDecision(BaseModel):

    next_agent: Literal[
        "research",
        "coding",
        "review"
    ]

    reason: str
```

Then use Gemini structured output.

Conceptually:

```python
router_model = model.with_structured_output(
    RouteDecision
)
```

Prompt:

```python
def supervisor(state):

    prompt = f"""
    You are a supervisor.

    Decide which specialist should handle
    the following task.

    Task:
    {state["task"]}

    Available specialists:

    research:
    Research and gather technical information.

    coding:
    Write implementation code.

    review:
    Review existing work.

    Return the appropriate specialist.
    """

    decision = router_model.invoke(prompt)

    return {
        "next": decision.next_agent
    }
```

Now:

```text
User
 ↓
Supervisor LLM
 ↓
structured decision
 ↓
worker
```

This is much more powerful.

---

# 25. Why structured output?

Without structured output:

```text
"Sure! I think the research agent would be appropriate..."
```

You then need to parse text.

Bad.

With structured output:

```json
{
  "next_agent": "research",
  "reason": "The task requires..."
}
```

Your graph gets predictable data.

This is exactly where your previous **Structured Output** learning becomes useful.

---

# 26. Agent delegation

Now let's introduce another term.

### Routing

Supervisor decides:

```text
"Research agent should handle this."
```

### Delegation

Supervisor actually **hands a task to the worker**.

For example:

```text
Supervisor:

"Research the security implications of JWT
authentication and return your findings."

        ↓

Research Agent
```

The worker gets:

```text
task
```

and executes it.

So:

```text
Routing
=
Who should work?

Delegation
=
What work should they perform?
```

That's a very useful interview distinction.

---

# 27. Worker communication

Suppose:

```text
Research Agent
```

finishes:

```text
JWT uses signed tokens...
```

The Coding Agent needs this information.

There are several ways to communicate.

---

# 28. Pattern 1 — Shared State

This is the easiest.

```text
Research Agent
      │
      ▼
research_result
      │
      ▼
Shared State
      │
      ▼
Coding Agent
```

Example:

```python
state["research_result"]
```

Coding agent can read it:

```python
def coding_agent(state):

    research = state["research_result"]

    ...
```

This is **shared-state communication**.

---

# 29. Pattern 2 — Message Passing

Instead of exposing all state, agents can communicate through messages.

Conceptually:

```text
Research Agent
     │
     │ message
     ▼
Coding Agent
```

Example:

```text
{
    "from": "research",
    "to": "coding",
    "content": "Use JWT with RS256..."
}
```

This is closer to actor/message-oriented systems.

---

# 30. Pattern 3 — Shared Store

Suppose multiple agents need access to durable knowledge:

```text
Research Agent
      │
      ▼
   Store/DB
      ▲
      │
Coding Agent
```

This is useful when:

* information is large
* multiple agents need it
* information should persist
* agents shouldn't pass everything through graph state

LangGraph distinguishes thread-scoped checkpoint state from longer-lived stores; stores are intended for application-defined data that can persist across threads. ([LangChain AI][2])

---

# 31. Don't put everything into shared state

Suppose Research produces:

```text
500-page document
```

Don't blindly put:

```python
state["research_result"] = entire_500_page_document
```

and send that to every agent.

Problems:

```text
Huge context
    ↓
Higher token cost
    ↓
Slower inference
    ↓
More noise
```

Instead:

```text
Research
 ↓
Store documents
 ↓
Return summary/references
 ↓
Coding Agent retrieves what it needs
```

This is where your RAG knowledge becomes important.

---

# 32. Sequential Multi-Agent System

Now:

```text
Research
   ↓
Coding
   ↓
Review
```

Example:

```text
USER
 ↓
Supervisor
 ↓
Research Agent
 ↓
Coding Agent
 ↓
Review Agent
 ↓
Final
```

This is a **sequential multi-agent workflow**.

Use this when later work depends on earlier work.

For example:

```text
Research
must happen before
Coding
```

and:

```text
Coding
must happen before
Review
```

---

# 33. Parallel Agents

Now imagine:

> "Research the topic from technical, business, and security perspectives."

These tasks don't depend on each other.

Instead of:

```text
Technical
 ↓
Business
 ↓
Security
```

we can do:

```text
             SUPERVISOR
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
    Technical  Business  Security
       Agent     Agent     Agent
        │         │         │
        └─────────┼─────────┘
                  ↓
               SYNTHESIS
```

That's parallel agent execution.

---

# 34. Why parallelism?

Sequential:

```text
Technical = 5 sec
Business  = 4 sec
Security  = 6 sec

Total ≈ 15 sec
```

Parallel:

```text
Technical = 5 sec
Business  = 4 sec
Security  = 6 sec

Total ≈ max(5,4,6)
      ≈ 6 sec
```

Ignoring orchestration/network overhead.

This is one of the biggest benefits of parallel agents.

---

# 35. But parallelism has a requirement

The tasks should ideally be independent.

Good:

```text
Technical research
Business research
Security research
```

Bad:

```text
Research
 ↓
Analyze research
```

because Analyze depends on Research.

That should be sequential.

---

# 36. Think in dependencies

This is exactly like a DAG.

Suppose:

```text
A = Research
B = Coding
C = Security review
D = Final
```

Dependencies:

```text
A → B
B → C
C → D
```

That's sequential.

But:

```text
A → D
B → D
C → D
```

means:

```text
A
B  → D
C
```

and A/B/C can potentially execute concurrently.

This is essentially workflow scheduling.

---

# 37. LangGraph fan-out/fan-in

This is where LangGraph becomes powerful.

Conceptually:

```text
             START
                │
                ▼
           Supervisor
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      A         B        C
       │        │        │
       └────────┼────────┘
                ↓
             Synthesis
                ↓
               END
```

This is called:

```text
fan-out
```

followed by:

```text
fan-in
```

The work fans out to multiple workers and then comes back together.

---

# 38. Parallel agents example

Imagine:

```python
def technical_agent(state):
    return {
        "technical": "Technical findings..."
    }


def business_agent(state):
    return {
        "business": "Business findings..."
    }


def security_agent(state):
    return {
        "security": "Security findings..."
    }
```

Then:

```python
builder.add_edge(
    "supervisor",
    "technical"
)

builder.add_edge(
    "supervisor",
    "business"
)

builder.add_edge(
    "supervisor",
    "security"
)
```

And all converge:

```python
builder.add_edge(
    "technical",
    "synthesis"
)

builder.add_edge(
    "business",
    "synthesis"
)

builder.add_edge(
    "security",
    "synthesis"
)
```

Conceptually:

```text
                 Supervisor
              /      |      \
             ↓       ↓       ↓
        Technical Business Security
             \       |       /
              \      |      /
                 Synthesis
```

---

# 39. Important: parallel doesn't mean "three agents talking randomly"

This is a common beginner misconception.

Parallel agents are usually better understood as:

```text
Supervisor
    ↓
Independent tasks
    ↓
Workers execute
    ↓
Aggregator/Synthesizer
```

Not:

```text
Agent A:
"Hey B, what do you think?"

Agent B:
"Ask C."

Agent C:
"Ask A."

💀
```

That can become uncontrolled.

---

# 40. Hierarchical Multi-Agent Systems

Now we're going one level deeper.

Suppose you have:

```text
                 CEO AGENT
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
     Engineering             Business
     Supervisor              Supervisor
          │                     │
      ┌───┼───┐             ┌───┼───┐
      ↓   ↓   ↓             ↓   ↓   ↓
    Code Test DevOps       Sales Market Finance
```

This is a **hierarchical multi-agent architecture**.

---

# 41. Why hierarchy?

Without hierarchy:

```text
                Supervisor
                    │
     ┌──────────────┼──────────────┐
     ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
    20 workers
```

The supervisor has to understand every worker.

With hierarchy:

```text
                 SUPERVISOR
                     │
             Engineering
                Supervisor
              /     |     \
            Code   Test   DevOps
```

The top supervisor only needs to understand:

```text
Engineering
Business
Research
```

The Engineering supervisor handles:

```text
Code
Test
DevOps
```

This reduces complexity.

---

# 42. Hierarchical state

You can think:

```text
Top-level state
       │
       ├── Engineering workflow
       │       │
       │       ├── code state
       │       ├── test state
       │       └── devops state
       │
       └── Research workflow
               │
               ├── search state
               └── analysis state
```

This is exactly where the **subgraphs from Project 10** become useful.

A hierarchical agent can be constructed from nested graphs/subgraphs.

---

# 43. Multi-Agent + Subgraphs

This is the architecture I want you to visualize:

```text
                         MAIN GRAPH
                             │
                        SUPERVISOR
                             │
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
     RESEARCH AGENT     CODING AGENT      REVIEW AGENT
       SUBGRAPH           SUBGRAPH          SUBGRAPH
          │                  │                  │
      ┌───┴───┐          ┌───┴───┐        ┌────┴────┐
      ↓       ↓          ↓       ↓        ↓         ↓
    Search   RAG       Plan     Code    Analyze   Validate
```

Now you're using everything you've learned.

---

# 44. Human-in-the-loop in Multi-Agent

This is another important pattern.

Suppose:

```text
Supervisor
   ↓
Coding Agent
   ↓
Generated code
   ↓
Human approval
   ↓
Deployment Agent
```

The human is a safety boundary.

Or:

```text
Supervisor
   ↓
Research
   ↓
Analysis
   ↓
Human Review
   ↓
Writer
```

LangGraph's interrupt mechanism supports pausing execution for external input, persisting the graph state while waiting, and resuming with `Command`. ([LangChain AI][3])

---

# 45. A more realistic multi-agent system

Let's combine everything:

```text
                          USER
                            │
                            ▼
                       SUPERVISOR
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
          RESEARCH        CODING        REVIEW
           AGENT           AGENT         AGENT
              │             │             │
              │             │             │
              └─────────────┼─────────────┘
                            ↓
                        SYNTHESIS
                            │
                            ▼
                     HUMAN REVIEW
                            │
                    ┌───────┴───────┐
                    ↓               ↓
                 APPROVE          REJECT
                    ↓               ↓
                  FINAL          REWORK
```

This is a real agentic workflow.

---

# 46. Agent communication architecture

There are three major patterns you should remember.

### Shared state

```text
Agent A
   ↓
Shared State
   ↓
Agent B
```

Good for tightly coupled workflow steps.

---

### Message passing

```text
Agent A
   ↓
Message
   ↓
Agent B
```

Good for explicit communication.

---

### Shared store

```text
Agent A
   ↓
Database / Store
   ↑
Agent B
```

Good for larger/durable information.

---

# 47. Shared state vs shared memory

Don't confuse them.

### Shared graph state

```text
Current workflow
```

Example:

```python
state["research_result"]
```

### Long-term memory/store

```text
Persistent information
across threads/workflows
```

For example:

```text
User preference
Company information
Known facts
Historical knowledge
```

LangGraph's persistence docs distinguish thread-scoped checkpoint state from longer-lived store data. ([LangChain AI][2])

---

# 48. Multi-Agent memory

Imagine:

```text
Research Agent
```

learns:

```text
"The company uses PostgreSQL."
```

Should the Coding Agent automatically see it?

Not necessarily.

You decide the communication mechanism.

Possible:

```text
Research
 ↓
Shared State
 ↓
Coding
```

or:

```text
Research
 ↓
Store
 ↓
Coding retrieves
```

or:

```text
Research
 ↓
Message
 ↓
Coding
```

Architecture should be intentional.

---

# 49. Agent-to-agent delegation

Imagine supervisor says:

```text
"Research JWT security."
```

Research Agent gets:

```text
task = "Research JWT security"
```

and returns:

```text
result = "..."
```

Then supervisor decides:

```text
"Now ask Coding Agent to implement secure JWT authentication."
```

This is:

```text
Supervisor
   │
   │ delegate
   ▼
Research
   │
   │ result
   ▼
Supervisor
   │
   │ delegate
   ▼
Coding
```

This is the classic supervisor pattern.

---

# 50. But there is another architecture: handoffs

Instead of always returning to the supervisor:

```text
Supervisor
 ↓
Research
 ↓
Supervisor
 ↓
Coding
 ↓
Supervisor
```

you can have:

```text
Supervisor
 ↓
Research
 ↓
Coding
 ↓
Review
```

The workers themselves determine who should handle the next step.

This is commonly called a **handoff** style.

Conceptually:

```text
Agent A
   │
   │ "This task belongs to B"
   ▼
Agent B
```

So:

### Supervisor pattern

```text
Supervisor
 ↓
Worker
 ↓
Supervisor
 ↓
Worker
```

### Handoff pattern

```text
Agent A
 ↓
Agent B
 ↓
Agent C
```

---

# 51. Supervisor vs Handoff

| Supervisor                   | Handoff                             |
| ---------------------------- | ----------------------------------- |
| Central coordinator          | Decentralized transition            |
| Supervisor controls routing  | Current agent can transfer control  |
| Easier centralized oversight | More flexible conversations         |
| Good for team workflows      | Good for conversational specialists |
| Can become bottleneck        | Can become harder to reason about   |

Neither is universally better.

Choose based on workflow.

---

# 52. Agent communication can become expensive

Suppose:

```text
Agent A
```

produces:

```text
20,000 tokens
```

and sends everything to:

```text
Agent B
```

Then:

```text
Agent B
```

has to process 20k tokens.

Now:

```text
A → B → C → D
```

could repeatedly pass huge contexts.

A better architecture may be:

```text
A
 ↓
summarize
 ↓
small structured result
 ↓
B
```

For example:

```json
{
  "key_findings": [
    "...",
    "...",
    "..."
  ],
  "sources": ["...", "..."],
  "confidence": 0.88
}
```

This is one reason structured outputs are so valuable in multi-agent systems.

---

# 53. Multi-Agent failure modes

This is very important for interviews.

Multi-agent systems introduce new failure modes.

### Failure 1 — Wrong routing

```text
Coding task
 ↓
Research Agent
```

---

### Failure 2 — Agent loop

```text
A → B → A → B → A → B
```

Forever.

---

### Failure 3 — Context explosion

```text
A → huge output
 ↓
B → huge output
 ↓
C → huge output
```

---

### Failure 4 — Conflicting agents

```text
Agent A:
Use MongoDB.

Agent B:
Use PostgreSQL.

Agent C:
Use Redis.
```

Who decides?

You need an authority/aggregation mechanism.

---

### Failure 5 — Duplicate work

```text
Research A
Research B
```

both independently research the same thing.

---

### Failure 6 — Cascading failure

```text
Research fails
 ↓
Coding receives bad information
 ↓
Review rejects
 ↓
Supervisor retries
 ↓
...
```

A multi-agent system can amplify errors.

---

# 54. How do we control these?

Use:

```text
Maximum iterations
Maximum agent calls
Timeouts
Retry policies
Structured outputs
Validation
State constraints
Human approval
Observability
```

And especially:

```text
Clear agent contracts
```

---

# 55. Agent contract

Every worker should ideally have:

```text
Purpose
Inputs
Outputs
Allowed tools
Constraints
Failure behavior
```

For example:

```text
CODING AGENT

Purpose:
Implement backend code.

Input:
Technical requirements.

Output:
Code + explanation + tests.

Tools:
File system
Code execution

Cannot:
Deploy production code.

Failure:
Return structured error.
```

This is exactly how you prevent a multi-agent system from becoming chaotic.

---

# 56. Agent boundaries should be capability boundaries

Bad:

```text
Agent 1
Agent 2
Agent 3
```

with no reason.

Good:

```text
Research Agent
    ↓
has research tools

Coding Agent
    ↓
has coding tools

Deployment Agent
    ↓
has deployment tools
    ↓
HITL approval required
```

This gives you **least privilege**.

For example, the Research Agent shouldn't have:

```text
delete_database()
deploy_production()
send_payment()
```

This becomes a security architecture decision.

---

# 57. Multi-Agent security

Imagine:

```text
Supervisor
   ↓
Coding Agent
   ↓
Deployment Agent
```

If Coding Agent can directly call:

```text
production_deploy()
```

you've created a dangerous architecture.

Better:

```text
Coding
 ↓
Review
 ↓
Human Approval
 ↓
Deployment Agent
 ↓
Production
```

This combines:

```text
Multi-agent
+
HITL
+
Least privilege
```

---

# 58. Parallel vs sequential decision

Here's the rule I want you to memorize.

### Sequential

Use when:

```text
B depends on A
```

Example:

```text
Research
 ↓
Code
 ↓
Review
```

### Parallel

Use when:

```text
A, B, C are independent
```

Example:

```text
Technical research
Business research
Security research
```

then:

```text
A
B → Synthesis
C
```

---

# 59. Hierarchical vs flat

### Flat

```text
Supervisor
 ├── A
 ├── B
 ├── C
 ├── D
 ├── E
 ├── F
 └── G
```

### Hierarchical

```text
                 Supervisor
                /          \
         Engineering      Research
             /   \          /   \
           Code  Test     Search Analyze
```

Hierarchy becomes useful when the number of responsibilities grows.

---

# 60. One of the biggest interview questions

> **"Why not just use one powerful LLM?"**

Answer:

A single powerful LLM can often handle many tasks, but multi-agent architecture can provide:

* specialization
* tool isolation
* context isolation
* clearer responsibilities
* independent testing
* parallel execution
* separate prompts/models
* capability boundaries
* easier organizational ownership

But multi-agent also introduces:

* latency
* token costs
* orchestration complexity
* communication overhead
* more failure modes
* debugging difficulty

Therefore:

> **Use multi-agent architecture when decomposition provides a concrete engineering or reasoning benefit, not simply because multiple agents sound more advanced.**

That is a very strong interview answer.

---

# 61. Another interview question

> "When would you choose a multi-agent system over an agent with multiple tools?"

Answer:

If one agent can reliably select and use the tools while maintaining manageable context and reasoning complexity, a single agent is usually simpler.

I'd consider multiple agents when tasks require substantially different:

* expertise
* tools
* prompts
* context
* permissions
* execution strategies
* parallelization

---

# 62. Another important question

> "What is a supervisor agent?"

A supervisor is an agent responsible for coordinating specialized workers by determining what work should be performed, which worker should perform it, and how results should be combined or what should happen next.

---

# 63. What is a worker?

A worker is a specialized agent responsible for executing a delegated task.

```text
Supervisor
    ↓
Worker
    ↓
Result
```

---

# 64. What is agent delegation?

Delegation means a coordinating agent assigns a specific task to another agent.

```text
Supervisor
    ↓
"Research JWT security."
    ↓
Research Agent
```

---

# 65. What is agent communication?

The mechanisms by which agents exchange information.

Common patterns:

```text
Shared state
Message passing
Shared store
Tool-mediated communication
```

---

# 66. What is a hierarchical agent?

A multi-level organization where higher-level agents delegate to lower-level supervisors/workers.

```text
Top Supervisor
      ↓
Domain Supervisor
      ↓
Specialist Worker
```

---

# 67. What is fan-out/fan-in?

### Fan-out

One task splits into multiple independent tasks.

```text
       Supervisor
       /   |   \
      A    B    C
```

### Fan-in

Those results converge.

```text
A
 \
B → Synthesis
 /
C
```

Together:

```text
Supervisor
    ↓
 fan-out
 /  |  \
A   B   C
 \  |  /
  fan-in
    ↓
Synthesis
```

---

# 68. Your Level 26 architecture

At the end of this level, you should be able to understand this:

```text
                              USER
                                │
                                ▼
                         TOP SUPERVISOR
                                │
                   ┌────────────┼────────────┐
                   ↓            ↓            ↓
              RESEARCH       CODING       REVIEW
              SUPERVISOR    SUPERVISOR     AGENT
                   │            │
              ┌────┼────┐   ┌───┼────┐
              ↓    ↓    ↓   ↓   ↓    ↓
            Search RAG Web Code Test Security
              │    │    │   │   │    │
              └────┴────┴───┴───┴────┘
                         │
                         ▼
                      SYNTHESIS
                         │
                         ▼
                   HUMAN REVIEW
                    /         \
                   ↓           ↓
                APPROVE      REWORK
                   │
                   ▼
                 FINAL
```

That's a serious multi-agent architecture.

---

# 69. How this connects everything you've learned

This is the really satisfying part.

### LangChain

```text
Models
Prompts
Tools
Structured output
```

### LangGraph

```text
State
Nodes
Edges
Routing
Persistence
Interrupts
Streaming
Retries
Subgraphs
```

### RAG

```text
Retrieval
Embeddings
Vector DB
Reranking
Grounding
```

### Multi-Agent

```text
Supervisor
Workers
Delegation
Communication
Parallelism
Hierarchy
```

Together:

```text
                 AGENTIC AI SYSTEM
                        │
        ┌───────────────┼────────────────┐
        ↓               ↓                ↓
      LLMs            Tools             RAG
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                    LANGGRAPH
                        │
             ┌──────────┼──────────┐
             ↓          ↓          ↓
         Supervisor   Workers   Subgraphs
             │          │          │
             └──────────┼──────────┘
                        ↓
                  Persistence
                        ↓
                  Human Review
                        ↓
                    Streaming
                        ↓
                   Production
```

---

# 70. What you should build to actually master Level 26

Don't just read this.

Build these **5 mini-projects** in order.

### Multi-Agent Project 1

**Supervisor + 3 Workers**

```text
Supervisor
 / | \
Research Code Review
```

Learn:

```text
Routing
Delegation
Shared state
```

---

### Multi-Agent Project 2

**Sequential Team**

```text
Research
 ↓
Writer
 ↓
Reviewer
```

Learn:

```text
Agent communication
Sequential execution
Feedback loops
```

---

### Multi-Agent Project 3

**Parallel Research Team**

```text
         Supervisor
        /    |    \
   Technical Business Security
        \     |     /
           Synthesis
```

Learn:

```text
Fan-out
Fan-in
Parallel execution
Aggregation
```

---

### Multi-Agent Project 4

**Hierarchical Coding Team**

```text
             CTO Agent
                 ↓
        Engineering Manager
          /       |       \
       Coder    Tester    Security
```

Learn:

```text
Hierarchical agents
Nested subgraphs
Delegation
Agent boundaries
```

---

### Multi-Agent Project 5

🏆 **Production Multi-Agent System**

Combine:

```text
Supervisor
+
Specialists
+
RAG
+
Tools
+
Memory
+
Parallelism
+
HITL
+
Streaming
+
Retries
+
Persistence
+
Subgraphs
```

That will be your Level 26 capstone before moving deeper into production agent architecture.

---

# 🧠 The 10 things you absolutely cannot miss

If you're preparing for interviews and real projects, make sure you can explain these without notes:

```text
1. Single-agent vs multi-agent

2. When multi-agent is actually justified

3. Supervisor-worker architecture

4. Routing vs delegation

5. Shared state vs message passing vs store

6. Sequential vs parallel agents

7. Fan-out / fan-in

8. Hierarchical agents

9. Supervisor vs handoff architecture

10. Multi-agent failure, security and cost tradeoffs
```

And one final principle:

> **Multi-agent systems are not about creating many AIs. They're about decomposing a complex decision/workflow into specialized capabilities with explicit coordination.**

That mental model will carry you much further than memorizing LangGraph APIs.

### Your roadmap now

```text
LEVEL 26 — MULTI-AGENT SYSTEMS
│
├── Fundamentals              ← YOU ARE HERE
├── Supervisor
├── Workers
├── Routing
├── Delegation
├── Communication
├── Shared State
├── Sequential
├── Parallel
├── Hierarchical
├── HITL
├── Failure handling
├── Memory
└── Production patterns
```

The **next thing I'd do is not jump to another theory level**. Build **Multi-Agent Project 1: Supervisor + Research/Coding/Review workers** with Gemini and LangGraph, then progressively turn that same project into sequential, parallel, and hierarchical versions. That will make these concepts stick instead of becoming another list of terminology.

[1]: https://langchain-ai.github.io/langgraph/reference/?utm_source=chatgpt.com "langgraph | LangChain Reference"
[2]: https://langchain-ai.github.io/langgraphjs/how-tos/cross-thread-persistence-functional/?utm_source=chatgpt.com "Persistence - Docs by LangChain"
[3]: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/?featured_on=talkpython&utm_source=chatgpt.com "Interrupts - Docs by LangChain"
