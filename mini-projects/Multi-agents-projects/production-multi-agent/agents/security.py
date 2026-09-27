from states.ProjectState import ProjectState
from model.model import model


def security_agent(state: ProjectState):

    task = state["task"]

    response = model.invoke(
        [
            (
                "system",
                """
You are the Security Agent.

Analyze the proposed software requirement
from a security perspective.

Check:

- authentication
- authorization
- API security
- secrets
- injection
- rate limiting
- data protection
- least privilege
- abuse prevention
- infrastructure security

Do NOT modify anything.

Return concrete risks and mitigations.
"""
            ),
            (
                "human",
                task
            )
        ]
    )

    return {
        "security": response.content
    }
