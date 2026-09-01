def log_iteration(iteration: int):
    print(
        f"\n========== ITERATION {iteration} =========="
    )


def log_action(tool_name: str, arguments: dict):
    print("\n[ACTION]")
    print(f"Tool: {tool_name}")
    print(f"Arguments: {arguments}")


def log_observation(result, success: bool):
    print("\n[OBSERVATION]")

    if success:
        print(f"Success: {result}")
    else:
        print(f"Error: {result}")


def log_final_answer(answer: str):
    print("\n[FINAL ANSWER]")
    print(answer)