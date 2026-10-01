from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("Project Analyzer")

WORKSPACE = Path("./workspace")


@mcp.tool()
def list_files() -> list[str]:
    """List project files."""

    return [
        str(path.relative_to(WORKSPACE))
        for path in WORKSPACE.rglob("*")
        if path.is_file()
    ]
