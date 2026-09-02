from agent.memory import ConversationMemory
from tools.registry import TOOL_SCHEMAS


def test_memory_clear_removes_saved_contents():
    memory = ConversationMemory()
    memory.add("saved message")

    memory.clear()

    assert memory.get_contents() == []


def test_registered_tools_have_cli_display_details():
    displayed_tools = [
        f"- {tool.name}: {tool.description}"
        for tool in TOOL_SCHEMAS.values()
    ]

    assert displayed_tools == [
        "- calculator: Perform basic mathematical calculations.",
        "- time: Get the current local date and time.",
        "- random_number: Generate a random integer within an inclusive range.",
    ]
