from typing import TypedDict

class ProjectState(TypedDict, total=False):

    # Original user request
    task: str

    # Worker outputs
    research: str
    coding: str
    security: str

    # Review
    review: str
    decision: str

    # Revision control
    revision_count: int

    # Final result
    final_answer: str