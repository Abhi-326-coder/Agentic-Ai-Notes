from tools.executor import execute_tool
from tools.formatters import get_llm_tools


class ToolManager:

    def get_definitions(self):
        return get_llm_tools()

    def execute(
        self,
        name: str,
        arguments: dict
    ):
        return execute_tool(
            name,
            arguments
        )