from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    age: int
    result: str


def check_age(state: State):
    return {}


def adult_node(state: State):

    return {
        "result": "You are an adult."
    }


def minor_node(state: State):

    return {
        "result": "You are a minor."
    }


def decide(state: State):

    if state["age"] >= 18:
        return "adult"

    return "minor"


graph = StateGraph(State)

graph.add_node("check_age", check_age)
graph.add_node("adult", adult_node)
graph.add_node("minor", minor_node)

graph.add_edge(START, "check_age")

graph.add_conditional_edges(
    "check_age",
    decide,
    {
        "adult": "adult",
        "minor": "minor"
    }
)

graph.add_edge("adult", END)
graph.add_edge("minor", END)

app = graph.compile()

result = app.invoke({
    "age": 10,
    "result": ""
})

print(result)