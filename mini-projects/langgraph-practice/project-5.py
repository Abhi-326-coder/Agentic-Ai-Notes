from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
    MessagesState
)

from langgraph.checkpoint.memory import (
    InMemorySaver
)


# ==========================================
# ENV
# ==========================================

load_dotenv()


# ==========================================
# MODEL
# ==========================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# ==========================================
# NODE
# ==========================================

def chatbot(state: MessagesState):

    response = model.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# ==========================================
# GRAPH
# ==========================================

graph = StateGraph(
    MessagesState
)

graph.add_node(
    "chatbot",
    chatbot
)

graph.add_edge(
    START,
    "chatbot"
)

graph.add_edge(
    "chatbot",
    END
)


# ==========================================
# CHECKPOINTER
# ==========================================

checkpointer = InMemorySaver()


# ==========================================
# COMPILE
# ==========================================

app = graph.compile(
    checkpointer=checkpointer
)


# ==========================================
# THREAD
# ==========================================

config = {
    "configurable": {
        "thread_id": "student-123"
    }
}


# ==========================================
# FIRST MESSAGE
# ==========================================

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My name is arush."
            }
        ]
    },
    config
)

print("\nAI:")
print(
    result["messages"][-1].content
)


# ==========================================
# SECOND MESSAGE
# ==========================================

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is my name?"
            }
        ]
    },
    config
)

print("\nAI:")
print(
    result["messages"][-1].content
)

snapshot = app.get_state(config)

print(snapshot.values)
# config2 = {
#     "configurable":{
#         "thread_id":"student-456"
#     }
# }

# result = app.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "What is my name?"
#             }
#         ]
#     },
#     config2
# )
# print("config2 response : \n")
# print(
#     result["messages"][-1].content
# )