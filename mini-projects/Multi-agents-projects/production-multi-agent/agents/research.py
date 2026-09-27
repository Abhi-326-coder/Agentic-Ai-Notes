from states.ProjectState import ProjectState
from model.model import model
from tools.research_tools import (
    research_tools,
    search_architecture_knowledge,
)

def research_agent(state: ProjectState):

    task = state["task"]

    research_model = model.bind_tools(
        [search_architecture_knowledge]
    )

    messages = [
        (
            "system",
            """
You are the Research Agent in a multi-agent
software engineering team.

Your responsibilities:

1. Analyze the user's technical requirement.
2. Identify relevant architecture concepts.
3. Use the architecture knowledge tool when useful.
4. Produce practical technical research.
5. Do not write the final answer for the user.

Focus on:
- architecture
- scalability
- databases
- caching
- queues
- APIs
- distributed systems
- reliability
"""
        ),
        (
            "human",
            task
        )
    ]

    response = research_model.invoke(messages)

    # --------------------------------------------------------
    # Tool execution
    # --------------------------------------------------------

    if response.tool_calls:

        tool_results = []

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_function = research_tools.get(
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

        research_context = "\n\n".join(
            tool_results
        )

        # ----------------------------------------------------
        # Second LLM call using tool results
        # ----------------------------------------------------

        final_response = model.invoke(
            [
                (
                    "system",
                    """
You are the Research Agent.

Using the retrieved internal knowledge,
produce a concise architecture research report.

Include:
- relevant technologies
- architectural decisions
- scalability considerations
- trade-offs
"""
                ),
                (
                    "human",
                    f"""
Original task:

{task}

Retrieved information:

{research_context}
"""
                )
            ]
        )

        result_text = final_response.content

    else:

        result_text = response.content

    return {
        "research": result_text
    }
