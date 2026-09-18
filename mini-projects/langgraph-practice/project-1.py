import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

load_dotenv()

# -------------------------
# 1. STATE & PROMPT
# -------------------------

class AgentState(TypedDict):
    question: str
    answer: str
    topic: str

# Defined explicitly as system and user messages for cleaner LLM execution
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI tutor specializing in {topic}."),
    ("user", "Question: {question}\n\nExplain the answer for a beginner.")
])

# -------------------------
# 2. LLM
# -------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# -------------------------
# 3. NODE
# -------------------------

def llm_node(state: AgentState):
    question = state["question"]
    topic = state["topic"]
    
    # CORRECTED: Use .invoke() to format the prompt template
    formatted_prompt = prompt.invoke({
        "topic": topic,
        "question": question
    })
    
    print(">> Getting response from LLM...")
    response = model.invoke(formatted_prompt)

    # Returns the state update
    return {
        "answer": response.content
    }
    
def review_code(state:AgentState):
    
    answer = state["answer"]
    
    return {
        "answer":answer + "\n\nReviewed by the AI workflow"
    }

# -------------------------
# 4. GRAPH
# -------------------------

graph = StateGraph(AgentState)

# Add node
graph.add_node("llm", llm_node)
graph.add_node("review",review_code)

# Add edges
graph.add_edge(START, "llm")
graph.add_edge("llm", "review")
graph.add_edge("review",END)

# -------------------------
# 5. COMPILE
# -------------------------

app = graph.compile()

# -------------------------
# 6. RUN
# -------------------------

result = app.invoke({
    "question": "Explain RAG in simple terms.",
    "topic": "RAG",
    "answer": ""
})

print(result["answer"])
