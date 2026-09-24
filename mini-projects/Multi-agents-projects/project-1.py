# Supervisor + Worker Agents


from typing import TypedDict, Literal
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

load_dotenv()

# -----------------------------
# MODEL
# -----------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# -----------------------------
# STATE
# -----------------------------

class TeamState(TypedDict):
    task: str
    next_agent: str

    research_result: str
    coding_result: str
    writing_result: str

    final_answer: str


# -----------------------------
# ROUTING SCHEMA
# -----------------------------

class RouteDecision(BaseModel):

    next_agent: Literal[
        "research",
        "coding",
        "writer"
    ]

    reason: str


router_model = model.with_structured_output(RouteDecision)


# -----------------------------
# SUPERVISOR
# -----------------------------

def supervisor(state: TeamState):

    task = state["task"]

    prompt = f"""
You are the Supervisor of an AI software team.

Workers:

research:
Researches technical concepts.

coding:
Solves programming and implementation tasks.

writer:
Creates clear technical explanations.

User task:
{task}

Choose the single most appropriate worker.
"""

    decision = router_model.invoke(prompt)

    print("\n===== SUPERVISOR =====")
    print("Selected:", decision.next_agent)
    print("Reason:", decision.reason)

    return {
        "next_agent": decision.next_agent
    }


# -----------------------------
# RESEARCH AGENT
# -----------------------------

def research_agent(state: TeamState):

    task = state["task"]

    prompt = f"""
You are the Research Agent.

Research the following task:

{task}

Provide important technical concepts,
how they work, and important considerations.

Do not produce the final answer.
"""

    response = model.invoke(prompt)

    return {
        "research_result": response.content
    }


# -----------------------------
# CODING AGENT
# -----------------------------

def coding_agent(state: TeamState):

    task = state["task"]

    prompt = f"""
You are the Coding Agent.

Solve the programming portion of:

{task}

Provide correct implementation,
explanation and edge cases.
"""

    response = model.invoke(prompt)

    return {
        "coding_result": response.content
    }


# -----------------------------
# WRITER AGENT
# -----------------------------

def writer_agent(state: TeamState):

    task = state["task"]

    prompt = f"""
You are the Technical Writer Agent.

Explain this task clearly:

{task}

Make the explanation educational
and technically accurate.
"""

    response = model.invoke(prompt)

    return {
        "writing_result": response.content
    }


# -----------------------------
# ROUTER
# -----------------------------

def route(state: TeamState):

    return state["next_agent"]


# -----------------------------
# FINAL AGENT
# -----------------------------

def final_node(state: TeamState):

    prompt = f"""
Create the final answer for the user.

User task:
{state["task"]}

Research result:
{state["research_result"]}

Coding result:
{state["coding_result"]}

Writing result:
{state["writing_result"]}

Combine the useful information into
a clear final response.
"""

    response = model.invoke(prompt)

    return {
        "final_answer": response.content
    }


# -----------------------------
# GRAPH
# -----------------------------

builder = StateGraph(TeamState)

builder.add_node("supervisor", supervisor)
builder.add_node("research", research_agent)
builder.add_node("coding", coding_agent)
builder.add_node("writer", writer_agent)
builder.add_node("final", final_node)

builder.add_edge(
    START,
    "supervisor"
)

builder.add_conditional_edges(
    "supervisor",
    route,
    {
        "research": "research",
        "coding": "coding",
        "writer": "writer"
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
    "writer",
    "final"
)

builder.add_edge(
    "final",
    END
)


graph = builder.compile()


# -----------------------------
# RUN
# -----------------------------

result = graph.invoke({
    "task": "Explain JWT authentication",
    "next_agent": "",
    "research_result": "",
    "coding_result": "",
    "writing_result": "",
    "final_answer": ""
})


print("\n\n===== FINAL ANSWER =====")
print(result["final_answer"])