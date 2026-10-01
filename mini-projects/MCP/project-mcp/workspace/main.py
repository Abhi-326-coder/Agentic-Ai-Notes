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


@mcp.tool()
def read_file(path: str) -> str:
    """Read a project file."""

    file_path = WORKSPACE / path

    if not file_path.exists():
        raise ValueError("File does not exist")

    return file_path.read_text(
        encoding="utf-8"
    )


@mcp.tool()
def search_code(query: str) -> list[str]:
    """Search for a string in project files."""

    results = []

    for path in WORKSPACE.rglob("*"):

        if not path.is_file():
            continue

        try:
            content = path.read_text(
                encoding="utf-8"
            )

            if query.lower() in content.lower():

                results.append(
                    str(path.relative_to(WORKSPACE))
                )

        except UnicodeDecodeError:
            continue

    return results


@mcp.resource("project://README")
def project_readme() -> str:
    """Project README."""

    path = WORKSPACE / "README.md"

    return path.read_text(
        encoding="utf-8"
    )


@mcp.prompt()
def review_project() -> str:

    return """
Review this project.

Focus on:

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