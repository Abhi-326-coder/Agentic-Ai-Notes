def execute_with_retry(
    tool_function,
    arguments,
    max_retries=2
):

    last_error = None

    for attempt in range(max_retries + 1):

        try:
            return tool_function(
                **arguments
            )

        except Exception as error:

            last_error = error

            print(
                f"\nTool attempt {attempt + 1} failed:"
                f" {error}"
            )

    raise last_error