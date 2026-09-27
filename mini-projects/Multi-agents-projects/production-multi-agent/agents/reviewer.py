from states.ProjectState import ProjectState
from model.model import model
from states.ReviewResult import ReviewResult

review_model = model.with_structured_output(
    ReviewResult
)

def reviewer(state: ProjectState):

    task = state["task"]

    research = state.get(
        "research",
        ""
    )

    coding = state.get(
        "coding",
        ""
    )

    security = state.get(
        "security",
        ""
    )

    revision_count = state.get(
        "revision_count",
        0
    )

    response = review_model.invoke(
        [
            (
                "system",
                """
You are the senior reviewer of a
multi-agent software engineering team.

Review the work from:

1. Technical correctness
2. Scalability
3. Security
4. Maintainability
5. Missing requirements
6. Contradictions

Approve only if the work is sufficiently
complete.

Otherwise request revision.

Maximum allowed revision attempts are 2.
"""
            ),
            (
                "human",
                f"""
USER TASK:

{task}


RESEARCH AGENT:

{research}


CODING AGENT:

{coding}


SECURITY AGENT:

{security}


CURRENT REVISION:

{revision_count}
"""
            )
        ]
    )

    decision = response.decision

    feedback = response.feedback

    # --------------------------------------------------------
    # Protect against infinite loops
    # --------------------------------------------------------

    if (
        decision == "REVISE"
        and revision_count >= 2
    ):
        decision = "APPROVE"

        feedback += (
            "\n\nMaximum revision count reached. "
            "Proceeding to human review."
        )

    new_revision_count = revision_count

    if decision == "REVISE":

        new_revision_count += 1

    return {
        "review": feedback,
        "decision": decision,
        "revision_count": new_revision_count,
    }
    
def route_after_review(
    state: ProjectState
):

    if state["decision"] == "REVISE":

        return "research"

    return "human_approval"
