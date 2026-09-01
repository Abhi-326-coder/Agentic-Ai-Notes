
from agent.parser import get_tool_calls
from google.genai import types
from agent.logger import (
    log_action,
    log_final_answer,
    log_iteration,
    log_observation
)
from tools.manager import ToolManager


def run_agent(
    state,
    tools,
    llm,
    tool_manager
):

    while state.iteration < state.max_iterations:

        state.iteration += 1

        log_iteration(state.iteration)
        
        response = llm.generate(
            state.contents,
            tools
        )

        tool_calls = get_tool_calls(response)
        
        state.tool_calls.extend(tool_calls)

        # No tool call means the model is finished.
        if not tool_calls:
            if response.text:
                if response.candidates and response.candidates[0].content:
                    state.contents.append(response.candidates[0].content)
                return response.text

            if state.observations:
                state.contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=(
                                    "Using the tool result above, provide the final "
                                    "answer as plain text."
                                )
                            )
                        ],
                    )
                )
                continue

            if response.candidates and response.candidates[0].content:
                state.contents.append(response.candidates[0].content)
            return "The model returned no text response."

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

                result = tool_manager.execute(
                    tool_call["name"],
                    tool_call["arguments"]
                )

                success = True

            except Exception as error:

                result = f"Tool execution failed: {error}"

                success = False
                
            state.observations.append(
                {
                    "tool": tool_call["name"],
                    "arguments": tool_call["arguments"],
                    "result": result,
                    "success": success,
                }
            )

            log_observation(result, success)

            function_response = types.Part.from_function_response(
                name=tool_call["name"],
                response={
                    "result": result
                },
            )

            state.contents.append(
                types.Content(
                    role="tool",
                    parts=[function_response]
                )
            )

    raise RuntimeError(
        f"Agent stopped after reaching its {state.max_iterations}-iteration limit."
    )
