from langgraph.graph import (
    StateGraph, 
    START,
    END
)
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from states.ProjectState import (
    ProjectState
)

from agents.coding import (
    coding_agent
)

from agents.research import research_agent
from agents.reviewer import (
    reviewer,
    route_after_review
)
from agents.human_approval import human_approval
from agents.security import security_agent
from agents.supervisor import supervisor


workflow = StateGraph(
    ProjectState
)


# ------------------------------------------------------------
# Nodes
# ------------------------------------------------------------

workflow.add_node(
    "supervisor",
    lambda state: {}
)

workflow.add_node(
    "research",
    research_agent
)

workflow.add_node(
    "coding",
    coding_agent
)

workflow.add_node(
    "security",
    security_agent
)

workflow.add_node(
    "reviewer",
    reviewer
)

workflow.add_node(
    "human_approval",
    human_approval
)


# ============================================================
# EDGES
# ============================================================

workflow.add_edge(
    START,
    "supervisor"
)


# ------------------------------------------------------------
# Supervisor → all workers
#
# Multiple outgoing edges create parallel branches.
# ------------------------------------------------------------

workflow.add_edge(
    "supervisor",
    "research"
)

workflow.add_edge(
    "supervisor",
    "coding"
)

workflow.add_edge(
    "supervisor",
    "security"
)


# ------------------------------------------------------------
# Workers → Reviewer
#
# Reviewer runs after the parallel worker branches finish.
# ------------------------------------------------------------

workflow.add_edge(
    "research",
    "reviewer"
)

workflow.add_edge(
    "coding",
    "reviewer"
)

workflow.add_edge(
    "security",
    "reviewer"
)


# ------------------------------------------------------------
# Reviewer routing
# ------------------------------------------------------------

workflow.add_conditional_edges(
    "reviewer",
    route_after_review,
    {
        "research": "research",
        "human_approval": "human_approval",
    }
)


workflow.add_edge(
    "human_approval",
    END
)


# ============================================================
# CHECKPOINTER
# ============================================================

checkpointer = InMemorySaver()


# ============================================================
# COMPILE
# ============================================================

graph = workflow.compile(
    checkpointer=checkpointer
)


# ============================================================
# RUN
# ============================================================

def approve_workflow():

    config = {
        "configurable": {
            "thread_id": "ecommerce-project-001"
        }
    }

    response = graph.invoke(
        Command(
            resume={
                "approved": True
            }
        ),
        config
    )

    print("\n")
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(
        response.get(
            "final_answer",
            "No final answer."
        )
    )

def run():

    task = """
Design a highly scalable e-commerce platform
that can support millions of users.

Requirements:

- user authentication
- product catalog
- shopping cart
- orders
- payments
- Redis caching
- PostgreSQL
- asynchronous processing
- high availability
- monitoring
- rate limiting

Explain the architecture and implementation strategy.
"""

    config = {
        "configurable": {
            "thread_id": "ecommerce-project-001"
        }
    }

    initial_state = {
        "task": task,
        "revision_count": 0,
    }

    print("\n")
    print("=" * 70)
    print("STARTING MULTI-AGENT SYSTEM")
    print("=" * 70)

    # --------------------------------------------------------
    # STREAM GRAPH UPDATES
    # --------------------------------------------------------

    for event in graph.stream(
        initial_state,
        config,
        stream_mode="updates",
    ):

        print("\n")
        print("EVENT:")
        print(event)

        # ----------------------------------------------------
        # If execution paused for HITL,
        # stream will stop here.
        # ----------------------------------------------------

        snapshot = graph.get_state(config)

        if snapshot.next:

            print("\n")
            print("=" * 70)
            print("WORKFLOW PAUSED")
            print("=" * 70)

            print(
                "Next node:",
                snapshot.next
            )

            print(
                "\nHuman approval required."
            )

            break


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run()
    approve_workflow()