from agent.llm import ask_llm
from agent.parser import get_tool_calls
from google.genai import types
from tools.executor import execute_tool
from agent.logger import (
    log_action,
    log_final_answer,
    log_iteration,
    log_observation
)


def run_agent(state, tool):

    while state.iteration < state.max_iterations:

        state.iteration += 1

        log_iteration(state.iteration)
        
        response = ask_llm(
            state.contents,
            tool
        )

        tool_calls = get_tool_calls(response)
        
        state.tool_calls.extend(tool_calls)

        # No tool call means the model is finished.
        if not tool_calls:
            return response.text or "The model returned no text response."

        # Save Gemini's response containing the tool call.
        state.contents.append(
            response.candidates[0].content
        )

        tool_response_parts = []

        for tool_call in tool_calls:

            log_action(
            tool_call["name"],
            tool_call["arguments"]
            )

            try:

                result = execute_tool(
                    tool_call["name"],
                    tool_call["arguments"]
                )

            except Exception as error:

                result = f"Tool execution failed: {error}"
                
            state.observations.append(
                {
                    "tool": tool_call["name"],
                    "arguments": tool_call["arguments"],
                    "result": result,
                }
            )

            log_observation(result)

            function_response = types.Part.from_function_response(
                name=tool_call["name"],
                response={
                    "result": result
                },
            )

            state.contents.append(
                types.Content(
                    role="user",
                    parts=[function_response]
                )
            )

    raise RuntimeError(
        f"Agent stopped after reaching its {state.max_iterations}-iteration limit."
    )
