from states.ProjectState import ProjectState
from model.model import model
from tools.coding_tools import analyze_code, coding_tools

def coding_agent(state: ProjectState):

    task = state["task"]

    coding_model = model.bind_tools(
        [analyze_code]
    )

    response = coding_model.invoke(
        [
            (
                "system",
                """
You are the Coding Agent.

Your job is to reason about the implementation
of the requested software system.

You may use the code-analysis tool when
code is supplied.

Focus on:

- API design
- backend structure
- data models
- implementation strategy
- error handling
- scalability
- maintainability

Do not deploy anything.
Do not execute arbitrary system commands.
"""
            ),
            (
                "human",
                task
            )
        ]
    )

    # --------------------------------------------------------
    # Execute tools
    # --------------------------------------------------------

    if response.tool_calls:

        tool_results = []

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_function = coding_tools.get(
                tool_name
            )

            if not tool_function:
                continue

            result = tool_function.invoke(
                tool_args
            )

            tool_results.append(
                f"Tool: {tool_name}\n"
                f"Result:\n{result}"
            )

        tool_context = "\n\n".join(
            tool_results
        )

        final_response = model.invoke(
            [
                (
                    "system",
                    """
You are the Coding Agent.

Produce a concise implementation plan
using the supplied tool results.

Include:
- components
- APIs
- data models
- important implementation details
- failure handling
"""
                ),
                (
                    "human",
                    f"""
Task:

{task}

Tool results:

{tool_context}
"""
                )
            ]
        )

        result_text = final_response.content

    else:

        result_text = response.content

    return {
        "coding": result_text
    }
