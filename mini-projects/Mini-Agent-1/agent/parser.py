def get_tool_calls(response):
    tool_calls = []

    for candidate in response.candidates or []:
        for part in (candidate.content.parts if candidate.content else []) or []:

            if part.function_call:
                function_call = part.function_call

                tool_calls.append(
                    {
                        "name": function_call.name,
                        "arguments": dict(function_call.args),
                    }
                )

    return tool_calls
