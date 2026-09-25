# PROJECT 5 — Production-Style Multi-Agent System

# We'll build:

# 🤖 AI Software Engineering Team

from typing import TypedDict
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import interrupt
from pydantic import BaseModel

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

class ProjectState(TypedDict):
    task: str

    research: str
    coding: str
    security: str

    review: str
    decision: str

    revision_count: int

    final_answer: str

@tool
def search_architecture_knowledge(query: str) -> str:
    """
    Search internal architecture knowledge.
    """

    knowledge = {
        "redis": "Redis is commonly used for caching, rate limiting and ephemeral data.",
        "postgres": "PostgreSQL is a relational database suitable for transactional workloads.",
        "kafka": "Kafka provides distributed event streaming.",
        "load balancer": "Load balancers distribute traffic across application instances.",
    }

    results = []

    for key, value in knowledge.items():
        if key in query.lower():
            results.append(value)

    return "\n".join(results) or "No relevant internal knowledge found."

research_model = model.bind_tools(
    [search_architecture_knowledge]
)

@tool
def analyze_code(code: str) -> str:
    """
    Perform basic code analysis.
    """

    issues = []

    if "password" in code.lower():
        issues.append("Possible hardcoded password.")

    if "print(" in code:
        issues.append("Debug print statement detected.")

    if not issues:
        return "No obvious issues detected."

    return "\n".join(issues)

coding_model = model.bind_tools(
    [analyze_code]
)

security_prompt = """
You are a security reviewer.

Analyze the proposed architecture for:

- authentication problems
- authorization problems
- exposed secrets
- insecure APIs
- database risks
- rate limiting
- injection risks
- excessive permissions

Do not modify anything.
Return concrete findings and mitigations.
"""

review_prompt = """
You are the final architecture reviewer.

Given:

RESEARCH:
{research}

CODING:
{coding}

SECURITY:
{security}

Review the team's work.

Identify:
1. Missing requirements
2. Technical contradictions
3. Security issues
4. Scalability issues
5. Improvements

Then decide:

APPROVE
or
REVISE
"""

class ReviewResult(BaseModel):
    decision: str
    feedback: str

review_model = model.with_structured_output(
    ReviewResult
)

def human_approval(state):

    decision = interrupt({
        "message": "Approve the final architecture?",
        "review": state["review"]
    })

    return {
        "final_answer": (
            state["research"]
            + "\n\n"
            + state["coding"]
            + "\n\n"
            + state["security"]
        )
    }

config = {
    "configurable": {
        "thread_id": "project-123"
    }
}