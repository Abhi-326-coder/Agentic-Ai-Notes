from langchain_google_genai import ChatGoogleGenerativeAI
from .config import gemini_api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=gemini_api_key(),
)


def create_plan(goal: str):

    prompt = f"""
You are the planning component of a Deep Agent.

User goal:

{goal}

Break the goal into 3-6 concrete executable tasks.

Rules:

1. Tasks must be specific.
2. Tasks should have logical ordering.
3. Avoid unnecessary tasks.
4. Return only a numbered list.

Example:

1. Inspect project files
2. Analyze source code
3. Identify bugs
4. Implement fixes
5. Run tests
6. Prepare final report
"""

    response = llm.invoke(prompt)

    lines = response.content.split("\n")

    plan = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove simple numbering
        line = line.lstrip("0123456789.- ")

        if line:
            plan.append(line)

    return plan
