from agent.agent import Agent
from agent.memory import ConversationMemory
from google.genai import types
from tools.manager import ToolManager
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


def test_tool_manager_returns_a_valid_gemini_tool_declaration():
    tool = ToolManager().get_definitions()

    config = types.GenerateContentConfig(tools=[tool])

    assert config.tools[0].function_declarations[0].name == "calculator"


def test_agent_passes_its_tool_manager_to_agent_loop(monkeypatch):
    captured = {}

    def fake_run_agent(state, tools, llm, tool_manager):
        captured["tool_manager"] = tool_manager
        return "done"

    monkeypatch.setattr("agent.agent.run_agent", fake_run_agent)
    agent = Agent(llm=object())

    result = agent.run("Hello")

    assert result.final_answer == "done"
    assert captured["tool_manager"] is agent.tool_manager
