import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


# ==========================================
# 1. ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# 2. STATE
# ==========================================

class AgentState(TypedDict):
    # Each node returns only its new message(s); this reducer preserves the
    # user prompt, tool call, and tool result for the next LLM invocation.
    messages: Annotated[list, add_messages]


# ==========================================
# 3. TOOL
# ==========================================

@tool
def calculator(
    a: float,
    b: float,
    operation: str
) -> float:
    """
    Perform basic arithmetic.
    """

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":

        if b == 0:
            raise ValueError(
                "Cannot divide by zero"
            )

        return a / b

    else:
        raise ValueError(
            "Unknown operation"
        )


# ==========================================
# 4. MODEL
# ==========================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# Tell Gemini about the tool
model_with_tools = model.bind_tools(
    [calculator]
)


# ==========================================
# 5. LLM NODE
# ==========================================

def llm_node(state: AgentState):

    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ==========================================
# 6. TOOL NODE
# ==========================================
# toolnode executes the actual tool function
tool_node = ToolNode(
    [calculator]
)


# ==========================================
# 7. ROUTER
# ==========================================

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


# ==========================================
# 8. GRAPH
# ==========================================

graph = StateGraph(AgentState)


graph.add_node(
    "llm",
    llm_node
)

graph.add_node(
    "tools",
    tool_node
)


# START → LLM

graph.add_edge(
    START,
    "llm"
)


# LLM → TOOL or END

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)


# TOOL → LLM

graph.add_edge(
    "tools",
    "llm"
)


# ==========================================
# 9. COMPILE
# ==========================================

app = graph.compile()


# ==========================================
# 10. RUN
# ==========================================

result = app.invoke({
    "messages": [
        HumanMessage(
            content="What is 25 multiplied by 48?"
        )
    ]
})
# print(result)


# ==========================================
# 11. PRINT
# ==========================================

for message in result["messages"]:
    # print(message)
    print("\n--------------------")

    print(
        type(message).__name__
    )

    print(
        message.content
    )

    if hasattr(message, "tool_calls"):

        if message.tool_calls:
            print(
                "TOOL CALL:",
                message.tool_calls
            )
