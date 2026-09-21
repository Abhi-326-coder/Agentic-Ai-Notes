from typing import TypedDict

from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode


# ==========================================
# ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# STATE
# ==========================================

class AgentState(TypedDict):
    messages: list


# ==========================================
# TOOL 1
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

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":

        if b == 0:
            raise ValueError(
                "Cannot divide by zero"
            )

        return a / b

    raise ValueError(
        "Unknown operation"
    )


# ==========================================
# TOOL 2
# ==========================================

@tool
def convert_km_to_meters(
    km: float
) -> float:
    """
    Convert kilometers to meters.
    """

    return km * 1000


# ==========================================
# TOOL 3
# ==========================================

students = {
    "abhishek": {
        "semester": 3,
        "course": "Computer Science"
    },

    "rahul": {
        "semester": 5,
        "course": "Information Science"
    }
}


@tool
def get_student_info(
    name: str
) -> str:
    """
    Get information about a student.
    """

    student = students.get(
        name.lower()
    )

    if not student:
        return (
            f"No student found with name {name}"
        )

    return (
        f"Name: {name}\n"
        f"Semester: {student['semester']}\n"
        f"Course: {student['course']}"
    )


# ==========================================
# MODEL
# ==========================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


tools = [
    calculator,
    convert_km_to_meters,
    get_student_info
]


model_with_tools = model.bind_tools(
    tools
)


# ==========================================
# LLM NODE
# ==========================================

def llm_node(state: AgentState):

    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ==========================================
# TOOL NODE
# ==========================================

tool_node = ToolNode(tools)


# ==========================================
# ROUTER
# ==========================================

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


# ==========================================
# GRAPH
# ==========================================

graph = StateGraph(
    AgentState
)


graph.add_node(
    "llm",
    llm_node
)


graph.add_node(
    "tools",
    tool_node
)


graph.add_edge(
    START,
    "llm"
)


graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)


graph.add_edge(
    "tools",
    "llm"
)


# ==========================================
# COMPILE
# ==========================================

app = graph.compile()


# ==========================================
# RUN
# ==========================================

result = app.invoke({
    "messages": [
        HumanMessage(
            content="What is 25 multiplied by 48?"
        )
    ]
})


# ==========================================
# OUTPUT
# ==========================================

for message in result["messages"]:

    print("\n====================")

    print(
        type(message).__name__
    )

    print(
        message.content
    )

    if hasattr(
        message,
        "tool_calls"
    ):

        if message.tool_calls:

            print(
                "TOOL CALLS:"
            )

            print(
                message.tool_calls
            )