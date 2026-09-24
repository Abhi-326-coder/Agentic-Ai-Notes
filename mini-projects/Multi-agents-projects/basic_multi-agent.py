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