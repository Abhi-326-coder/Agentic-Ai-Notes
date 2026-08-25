from google.genai import types

from tools.registry import TOOL_SCHEMAS


def get_llm_tools() -> types.Tool:
    """Build the Gemini tool declaration for the locally registered tools."""
    function_declarations = [
        types.FunctionDeclaration(
            name=schema.name,
            description=schema.description,
            parameters_json_schema=schema.argument_schema,
        )
        for schema in TOOL_SCHEMAS.values()
    ]

    return types.Tool(function_declarations=function_declarations)
