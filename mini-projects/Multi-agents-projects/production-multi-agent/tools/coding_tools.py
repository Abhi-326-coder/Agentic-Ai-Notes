from langchain.tools import tool

@tool
def analyze_code(code: str) -> str:
    """
    Perform basic static analysis on supplied code.
    """

    issues = []

    code_lower = code.lower()

    if "password =" in code_lower:
        issues.append(
            "Possible hardcoded password detected."
        )

    if "api_key =" in code_lower:
        issues.append(
            "Possible hardcoded API key detected."
        )

    if "secret =" in code_lower:
        issues.append(
            "Possible hardcoded secret detected."
        )

    if "print(" in code_lower:
        issues.append(
            "Debug print statement detected."
        )

    if "eval(" in code_lower:
        issues.append(
            "eval() detected. This can introduce code execution risks."
        )

    if not issues:
        return "No obvious issues detected."

    return "\n".join(
        f"- {issue}"
        for issue in issues
    )

coding_tools = {
    "analyze_code":
        analyze_code
}