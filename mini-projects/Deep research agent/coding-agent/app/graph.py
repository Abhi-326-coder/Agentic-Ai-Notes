from langgraph.graph import StateGraph, END

from .state import AgentState
from .planner import create_plan
from .executor import execute_task


def planner_node(state: AgentState):

    plan = create_plan(state["goal"])

    return {
        "plan": plan,
        "completed_tasks": [],
        "failed_tasks": [],
        "observations": [],
        "retry_count": 0,
        "approved": False,
        "requires_approval": False
    }

def executor_node(state):

    task = state["plan"][0]

    try:

        result = execute_task(
            task,
            state
        )

        if not result:
            raise ValueError(
                "Empty result"
            )

        observations = state["observations"]

        observations.append(
            result["result"]
        )

        return {
            "plan": state["plan"][1:],
            "completed_tasks":
                state["completed_tasks"] + [task],
            "observations":
                observations,
            "retry_count": 0
        }

    except Exception as error:

        return {
            "failed_tasks":
                state["failed_tasks"] + [task],

            "retry_count":
                state["retry_count"] + 1,

            "observations":
                state["observations"] + [
                    f"ERROR: {error}"
                ]
        }


def should_continue(state: AgentState):

    if not state["plan"]:
        return "finish"

    return "execute"


def final_node(state: AgentState):

    summary = "\n\n".join(
        state["observations"]
    )

    return {
        "final_result": summary
    }


builder = StateGraph(AgentState)


builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "executor",
    executor_node
)

builder.add_node(
    "final",
    final_node
)


builder.set_entry_point("planner")


builder.add_edge(
    "planner",
    "executor"
)


builder.add_conditional_edges(
    "executor",
    should_continue,
    {
        "execute": "executor",
        "finish": "final"
    }
)


builder.add_edge(
    "final",
    END
)


graph = builder.compile()
