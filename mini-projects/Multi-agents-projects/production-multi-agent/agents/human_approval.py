from states.ProjectState import ProjectState
from langgraph.types import (
    interrupt
)

def human_approval(state: ProjectState):

    review = state.get(
        "review",
        ""
    )

    decision = interrupt(
        {
            "type": "human_approval",
            "message":
                "The AI team has completed its review.",
            "review":
                review,
            "question":
                "Approve the final result?"
        }
    )

    # --------------------------------------------------------
    # Resume value comes from Command(resume=...)
    # --------------------------------------------------------

    if isinstance(decision, dict):

        approved = decision.get(
            "approved",
            False
        )

    else:

        approved = (
            str(decision).lower()
            == "approved"
        )

    if not approved:

        return {
            "final_answer":
                "Human rejected the result."
        }

    final_answer = f"""
==================================================
FINAL ARCHITECTURE REPORT
==================================================

USER REQUIREMENT
----------------
{state["task"]}


RESEARCH
--------
{state.get("research", "")}


IMPLEMENTATION
--------------
{state.get("coding", "")}


SECURITY
--------
{state.get("security", "")}


REVIEW
------
{state.get("review", "")}

==================================================
APPROVED BY HUMAN
==================================================
"""

    return {
        "final_answer": final_answer
    }

