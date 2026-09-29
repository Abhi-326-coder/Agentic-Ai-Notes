from langchain_google_genai import ChatGoogleGenerativeAI
from .config import gemini_api_key

GEMINI_API_KEY = gemini_api_key()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=GEMINI_API_KEY,
)


def research_agent(task: str, context: str):

    prompt = f"""
You are a Research Agent.

Task:
{task}

Context:
{context}

Analyze the information carefully.

Return:
- Findings
- Important issues
- Recommendations
"""

    response = llm.invoke(prompt)

    return response.content


def coding_agent(task: str, context: str):

    prompt = f"""
You are a Coding Agent.

Task:
{task}

Context:
{context}

Analyze the code and determine what should be changed.

Do not invent files.

Return:
- Problem
- Proposed solution
- Exact changes required
"""

    response = llm.invoke(prompt)

    return response.content


def testing_agent(task: str, context: str):

    prompt = f"""
You are a Testing Agent.

Task:
{task}

Context:
{context}

Analyze the testing situation.

Return:
- Tests that should be executed
- Expected behavior
- Possible failures
"""

    response = llm.invoke(prompt)

    return response.content
