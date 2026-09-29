from typing import TypedDict, List

class AgentState(TypedDict):

    # User's original objective
    goal: str

    # High-level plan
    plan: List[str]

    # Current task being executed
    current_task: str

    # Tasks already completed
    completed_tasks: List[str]

    # Tasks that failed
    failed_tasks: List[str]

    # Results produced by tools/agents
    observations: List[str]

    # Number of retry attempts
    retry_count: int

    # Whether human approval is required
    requires_approval: bool

    # Whether human approved the action
    approved: bool

    # Final response
    final_result: str