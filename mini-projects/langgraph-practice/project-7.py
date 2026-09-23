from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


class AgentState(TypedDict):
    question:str
    answer:str

def llm_node(state: AgentState):

    response = model.invoke(
        state["question"]
    )

    return {
        "answer": response.content
    }

builder = StateGraph(AgentState)

builder.add_node(
    "llm",
    llm_node
)

builder.add_edge(
    START,
    "llm"
)

builder.add_edge(
    "llm",
    END
)

graph = builder.compile()

for chunk in graph.stream(
    {
        "question": "Explain distributed systems",
        "answer": ""
    }
):
    print(chunk)
