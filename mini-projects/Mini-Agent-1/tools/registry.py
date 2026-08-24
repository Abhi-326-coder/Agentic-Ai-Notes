from tools.calculator import calculator
from tools.time_tool import get_current_time

from models.schemas import ToolDefinition


TOOLS = {
    "calculator": calculator,
    "time": get_current_time,
}


TOOL_SCHEMAS = {
    "calculator": ToolDefinition(
        name="calculator",
        description="Perform basic mathematical calculations.",
        argument_schema={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression such as '25 * 4'.",
                }
            },
            "required": ["expression"],
        },
    ),

    "time": ToolDefinition(
        name="time",
        description="Get the current local date and time.",
        argument_schema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
}