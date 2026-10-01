from pathlib import Path
from mcp.server import MCPServer


mcp = MCPServer("Project Intelligence")


WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"

def safe_path(relative_path: str) -> Path:
    """
    Resolve a path while preventing path traversal outside workspace.
    """

    target = (WORKSPACE / relative_path).resolve()
    workspace = WORKSPACE.resolve()

    if target != workspace and workspace not in target.parents:
        raise ValueError("Access outside workspace is not allowed")

    return target


@mcp.tool()
def list_files() -> list[str]:
    """List all files inside the project workspace."""

    return [
        str(path.relative_to(WORKSPACE))
        for path in WORKSPACE.rglob("*")
        if path.is_file()
    ]


@mcp.tool()
def read_file(path: str) -> str:
    """Read a text file from the project workspace."""

    target = safe_path(path)

    if not target.exists():
        raise ValueError(f"File does not exist: {path}")

    if not target.is_file():
        raise ValueError(f"Not a file: {path}")

    return target.read_text(encoding="utf-8")


@mcp.tool()
def search_code(query: str) -> list[str]:
    """Search for a text string inside project files."""

    results = []

    for path in WORKSPACE.rglob("*"):

        if not path.is_file():
            continue

        try:
            content = path.read_text(encoding="utf-8")

            if query.lower() in content.lower():
                results.append(str(path.relative_to(WORKSPACE)))

        except UnicodeDecodeError:
            continue

    return results


@mcp.resource("project://README")
def project_readme() -> str:
    """Return the project's README."""

    return read_file("README.md")


@mcp.prompt()
def review_project() -> str:
    """Generate a project review prompt."""

    return """
Review the project using the available project tools.

Analyze:

1. Architecture
2. Code quality
3. Security
4. Error handling
5. Performance
6. Testing

Provide concrete recommendations.
"""


if __name__ == "__main__":
    mcp.run()