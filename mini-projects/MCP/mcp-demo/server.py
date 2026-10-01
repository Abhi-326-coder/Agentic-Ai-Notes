from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"

@mcp.prompt()
def explain(topic: str) -> str:
    """Create an explanation prompt."""
    return f"""
Explain {topic} to a beginner.
Use simple examples.
"""


if __name__ == "__main__":
    mcp.run()