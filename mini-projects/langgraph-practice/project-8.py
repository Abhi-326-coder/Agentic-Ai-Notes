import random

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


class ResearchState(TypedDict):

    question: str

    data: str

    answer: str

    error: str


# ==========================================
# ANALYZE
# ==========================================

def analyze(state: ResearchState):

    print("\n🔎 Analyzing request...")

    return {
        "error": ""
    }


# ==========================================
# PRIMARY API
# ==========================================

def primary_api(state: ResearchState):

    print("🌐 Calling primary API...")

    # Simulate failure

    if random.random() < 0.7:

        return {
            "error": "Primary API temporarily unavailable"
        }

    return {
        "data": "Fresh research data",
        "error": ""
    }


# ==========================================
# ROUTER
# ==========================================

def route_after_api(state: ResearchState):

    if state["error"]:

        return "fallback"

    return "success"


# ==========================================
# FALLBACK
# ==========================================

def fallback_api(state: ResearchState):

    print("\n⚠️ Using fallback source...")

    return {
        "data": "Cached research data",
        "error": ""
    }


# ==========================================
# GENERATE
# ==========================================

def generate_answer(state: ResearchState):

    print("\n🤖 Generating answer...")

    return {
        "answer": (
            f"Based on the available data: "
            f"{state['data']}"
        )
    }


# ==========================================
# GRAPH
# ==========================================

builder = StateGraph(ResearchState)

builder.add_node(
    "analyze",
    analyze
)

builder.add_node(
    "primary_api",
    primary_api
)

builder.add_node(
    "fallback",
    fallback_api
)

builder.add_node(
    "generate",
    generate_answer
)


builder.add_edge(
    START,
    "analyze"
)

builder.add_edge(
    "analyze",
    "primary_api"
)


builder.add_conditional_edges(
    "primary_api",
    route_after_api,
    {
        "success": "generate",
        "fallback": "fallback"
    }
)


builder.add_edge(
    "fallback",
    "generate"
)

builder.add_edge(
    "generate",
    END
)


graph = builder.compile()


# ==========================================
# RUN
# ==========================================

result = graph.invoke(
    {
        "question": "Research AI trends",
        "data": "",
        "answer": "",
        "error": ""
    }
)


print("\n==============================")
print("FINAL RESULT")
print("==============================")

print(result)