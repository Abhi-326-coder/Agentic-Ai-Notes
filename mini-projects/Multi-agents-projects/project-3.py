from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


# =====================================
# MODEL
# =====================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# =====================================
# STATE
# =====================================

class ResearchState(TypedDict):

    question: str

    technical_analysis: str
    business_analysis: str
    security_analysis: str

    final_answer: str


# =====================================
# SUPERVISOR
# =====================================

def supervisor(state: ResearchState):

    print("\n===== SUPERVISOR =====")
    print("Starting parallel research team...")

    return {}


# =====================================
# TECHNICAL AGENT
# =====================================

def technical_agent(state: ResearchState):

    print("\n[Technical Agent] Starting...")

    question = state["question"]

    prompt = f"""
You are a Senior Software Architect.

Analyze:

{question}

Focus on:

- scalability
- performance
- architecture
- bottlenecks
- data flow
- reliability
- technology tradeoffs

Return a technical analysis.
"""

    response = model.invoke(prompt)

    print("[Technical Agent] Finished.")

    return {
        "technical_analysis": response.content
    }


# =====================================
# BUSINESS AGENT
# =====================================

def business_agent(state: ResearchState):

    print("\n[Business Agent] Starting...")

    question = state["question"]

    prompt = f"""
You are a Technology Business Analyst.

Analyze:

{question}

Focus on:

- operational complexity
- development complexity
- infrastructure cost considerations
- maintenance
- team complexity
- technology tradeoffs

Return a business/operational analysis.
"""

    response = model.invoke(prompt)

    print("[Business Agent] Finished.")

    return {
        "business_analysis": response.content
    }


# =====================================
# SECURITY AGENT
# =====================================

def security_agent(state: ResearchState):

    print("\n[Security Agent] Starting...")

    question = state["question"]

    prompt = f"""
You are a Senior Application Security Engineer.

Analyze:

{question}

Focus on:

- authentication
- authorization
- data protection
- secrets
- attack surface
- network security
- common security risks
- secure configuration

Return a security analysis.
"""

    response = model.invoke(prompt)

    print("[Security Agent] Finished.")

    return {
        "security_analysis": response.content
    }


# =====================================
# SYNTHESIZER
# =====================================

def synthesizer(state: ResearchState):

    print("\n===== SYNTHESIZER =====")

    prompt = f"""
You are the Lead Architect.

Synthesize these independent analyses.

QUESTION:
{state["question"]}

TECHNICAL:
{state["technical_analysis"]}

BUSINESS:
{state["business_analysis"]}

SECURITY:
{state["security_analysis"]}

Create a balanced technical assessment.

Include:

1. Architecture
2. Performance
3. Business/operational considerations
4. Security
5. Tradeoffs
6. Appropriate use cases
7. Situations where it may not be appropriate

Identify disagreements or uncertainty.
Do not blindly trust individual agents.
"""

    response = model.invoke(prompt)

    return {
        "final_answer": response.content
    }


# =====================================
# BUILD GRAPH
# =====================================

builder = StateGraph(ResearchState)


builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "technical",
    technical_agent
)

builder.add_node(
    "business",
    business_agent
)

builder.add_node(
    "security",
    security_agent
)

builder.add_node(
    "synthesizer",
    synthesizer
)


# =====================================
# FAN-OUT
# =====================================

builder.add_edge(
    START,
    "supervisor"
)

builder.add_edge(
    "supervisor",
    "technical"
)

builder.add_edge(
    "supervisor",
    "business"
)

builder.add_edge(
    "supervisor",
    "security"
)


# =====================================
# FAN-IN
# =====================================

builder.add_edge(
    "technical",
    "synthesizer"
)

builder.add_edge(
    "business",
    "synthesizer"
)

builder.add_edge(
    "security",
    "synthesizer"
)

builder.add_edge(
    "synthesizer",
    END
)


# =====================================
# COMPILE
# =====================================

graph = builder.compile()


# =====================================
# RUN
# =====================================

result = graph.invoke({

    "question":
        "Is PostgreSQL + Redis + Kafka suitable "
        "for a scalable social media backend?",

    "technical_analysis": "",

    "business_analysis": "",

    "security_analysis": "",

    "final_answer": ""
})


# =====================================
# OUTPUT
# =====================================

print("\n\n================================")
print("FINAL ARCHITECTURE ANALYSIS")
print("================================\n")

print(result["final_answer"])