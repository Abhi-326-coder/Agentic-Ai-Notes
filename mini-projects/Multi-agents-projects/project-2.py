# Sequential Multi Agents

from typing import TypedDict, Literal
from dotenv import load_dotenv
from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

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

class ArticleState(TypedDict):

    topic: str

    research: str

    draft: str

    review: str

    review_status: str

    revision_count: int

    final_answer: str
    
class ReviewDecision(BaseModel):

    status: Literal[
        "approved",
        "needs_revision"
    ]

    feedback: str
    
review_model = model.with_structured_output(
    ReviewDecision
)


# =====================================
# RESEARCH AGENT
# =====================================

def research_agent(state: ArticleState):

    topic = state["topic"]

    prompt = f"""
You are a technical research agent.

Research the following topic:

{topic}

Target audience:
Backend developers.

Provide:

1. Definition
2. Core concepts
3. How it works
4. Architecture patterns
5. Common mistakes
6. Security considerations
7. Practical examples

Do not write the final article.
Return research notes only.
"""

    response = model.invoke(prompt)

    return {
        "research": response.content
    }


# =====================================
# WRITER AGENT
# =====================================

def writer_agent(state: ArticleState):

    topic = state["topic"]
    research = state["research"]

    prompt = f"""
You are a technical writer.

Write a technical article about:

{topic}

Use the following research:

{research}

Requirements:

- Explain concepts clearly.
- Use headings.
- Include examples.
- Do not invent information.
- Target backend developers.
- Make the article technically accurate.

Return only the draft article.
"""

    response = model.invoke(prompt)

    return {
        "draft": response.content,
        "revision_count" : state["revision_count"] + 1
    }


# =====================================
# REVIEWER AGENT
# =====================================

def reviewer_agent(state: ArticleState):

    draft = state["draft"]

    prompt = f"""
Review the following article.

DRAFT:
{draft}

Determine whether it is acceptable.

Return:

status:
approved
OR
needs_revision

feedback:
Explain your reasoning.
"""

    result = review_model.invoke(prompt)

    return {
        "review": result.feedback,
        "review_status": result.status
    }
    
# REVIEW ROUTER
    
def review_router(state: ArticleState):

    if state["review_status"] == "approved":
        return "final"

    if state["revision_count"] >= 3:
        return "final"

    return "writer"


# =====================================
# FINAL AGENT
# =====================================

def final_agent(state: ArticleState):

    topic = state["topic"]
    draft = state["draft"]
    review = state["review"]

    prompt = f"""
You are the final editor.

Topic:
{topic}

Draft:
{draft}

Review:
{review}

Create the final corrected article.

Apply valid reviewer feedback.

Do not blindly accept incorrect feedback.

Return only the final article.
"""

    response = model.invoke(prompt)

    return {
        "final_answer": response.content
    }


# =====================================
# GRAPH
# =====================================

builder = StateGraph(ArticleState)


builder.add_node(
    "research",
    research_agent
)

builder.add_node(
    "writer",
    writer_agent
)

builder.add_node(
    "reviewer",
    reviewer_agent
)

builder.add_node(
    "final",
    final_agent
)


# =====================================
# EDGES
# =====================================

builder.add_edge(
    START,
    "research"
)

builder.add_edge(
    "research",
    "writer"
)

builder.add_edge(
    "writer",
    "reviewer"
)

builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "final":"final",
        "writer":"writer"
    }
)

builder.add_edge(
    "reviewer",
    "final"
)

builder.add_edge(
    "final",
    END
)


# =====================================
# COMPILE
# =====================================

graph = builder.compile()


# =====================================
# EXECUTE
# =====================================

result = graph.invoke({

    "topic": "Redis caching",

    "research": "",

    "draft": "",

    "review": "",
    
    "review_status":"",
    
    "revision_count":0,

    "final_answer": ""
})


print("\n==============================")
print("FINAL ANSWER")
print("==============================\n")

print(result["final_answer"])