from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message:str

def hello_node(state:State):
    
    return{
        "message" : state["message"] + " hello from LangGraph"
    }

graph = StateGraph(State)

graph.add_node("hello", hello_node)

graph.add_edge(START, "hello")
# START -> hello 

graph.add_edge("hello", END)
# hello -> END

# graph : START -> hello -> END

app = graph.compile()

result = app.invoke({
    "message":"Hi"
})

print(result)