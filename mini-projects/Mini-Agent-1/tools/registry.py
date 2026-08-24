from tools.calculator import calculator
from tools.time_tool import get_current_time
from tools.random_number import random_number

from models.schemas import ToolDefinition


TOOLS = {
    "calculator": calculator,
    "time": get_current_time,
    "random_number":random_number
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
    
    "random_number":ToolDefinition(
        name="random_number",
        description="Generates random number",
        argument_schema={
            "type":"object",
            "properties":{
                "minimum": {
                    "type": "int",
                    "description": "minimum integer value to get a random number",
                },
                "maximum": {
                    "type":"int",
                    "description":"Maximum integer value to get a random number"
                }
            }
        }
    )
}