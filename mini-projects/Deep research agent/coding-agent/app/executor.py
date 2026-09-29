from .tools import (
    list_files,
    read_file,
    write_file,
    run_tests
)

from .agents import (
    research_agent,
    coding_agent,
    testing_agent
)


def execute_task(task: str, state):

    task_lower = task.lower()

    context = "\n".join(state["observations"])

    # File inspection
    if "inspect" in task_lower or "files" in task_lower:

        files = list_files()

        return {
            "type": "tool",
            "result": "\n".join(files)
        }

    # Testing
    if "test" in task_lower:

        result = run_tests()

        return {
            "type": "testing",
            "result": str(result)
        }

    # Coding
    if any(word in task_lower for word in [
        "fix",
        "implement",
        "modify",
        "code"
    ]):

        result = coding_agent(
            task,
            context
        )

        return {
            "type": "coding",
            "result": result
        }

    # Research / analysis
    result = research_agent(
        task,
        context
    )

    return {
        "type": "research",
        "result": result
    }