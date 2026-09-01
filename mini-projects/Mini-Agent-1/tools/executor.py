from tools.registry import TOOLS
from models.arguments import ARGUMENT_MODELS


def execute_tool(tool_name: str, arguments: dict):

    if tool_name not in TOOLS:
        raise ValueError(
            f"Unknown tool: '{tool_name}'"
        )

    if not isinstance(arguments, dict):
        raise TypeError(
            "Tool arguments must be a dictionary."
        )

    argument_model = ARGUMENT_MODELS.get(tool_name)

    if argument_model is None:
        raise ValueError(
            f"No argument schema found for '{tool_name}'"
        )

    validated_arguments = argument_model(
        **arguments
    )

    tool = TOOLS[tool_name]

    return tool(
        **validated_arguments.model_dump()
    )