from agent.llm import ask_llm
from agent.parser import get_tool_calls
from google.genai import types
from tools.executor import execute_tool


def run_agent(state, tool):

    while state.iteration < state.max_iterations:

        state.iteration += 1

        print(f"\n--- ITERATION {state.iteration} ---")

        response = ask_llm(
            state.contents,
            tool
        )

        tool_calls = get_tool_calls(response)

        # No tool call means the model is finished.
        if not tool_calls:
            return response.text or "The model returned no text response."

        # Save Gemini's response containing the tool call.
        state.contents.append(
            response.candidates[0].content
        )

        tool_response_parts = []

        for tool_call in tool_calls:

            print("\nACTION")
            print(
                tool_call["name"],
                tool_call["arguments"]
            )

            try:
                result = execute_tool(
                    tool_call["name"],
                    tool_call["arguments"]
                )
                function_response = {"output": result}
            except Exception as error:
                result = f"Tool error: {error}"
                function_response = {"error": str(error)}

            print("\nOBSERVATION")
            print(result)

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=tool_call["name"],
                    response=function_response,
                )
            )

        state.contents.append(
            types.Content(role="tool", parts=tool_response_parts)
        )

    raise RuntimeError(
        f"Agent stopped after reaching its {state.max_iterations}-iteration limit."
    )
