from model.model import model
from model.SupervisorDecision import SupervisorDecision

supervisor_model = model.with_structured_output(
    SupervisorDecision
)

def supervisor(state):

    result = supervisor_model.invoke(
        f"""
Determine which specialists are needed.

Task:
{state["task"]}

Return:
- needs_research
- needs_coding
- needs_security
"""
    )

    return {
        "needs_research":
            result.needs_research,

        "needs_coding":
            result.needs_coding,

        "needs_security":
            result.needs_security,
    }
