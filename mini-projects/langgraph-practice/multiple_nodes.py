from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name: str
    message: str
    
def greeting(state: State):
    return {
        "message":f"Hello {state['name']}"
    }

def answer(state: State):

    return {
        "message": state["message"] + ", welcome to LangGraph!"
    }
    
graph = StateGraph(State)

graph.add_node("greeting", greeting)
graph.add_node("answer",answer)

graph.add_edge(START, "greeting")
graph.add_edge("greeting","answer")
graph.add_edge("answer", END)

app = graph.compile()

result = app.invoke({
    "name":"Abhishek",
    "message":""
})

print(result)