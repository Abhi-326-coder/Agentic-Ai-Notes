from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


# ==========================================
# STATE
# ==========================================

class DeploymentState(TypedDict):
    request: str
    version: str
    environment: str

    approved: bool
    deployment_status: str


# ==========================================
# NODE 1
# ==========================================

def prepare_deployment(state: DeploymentState):

    print("\nPreparing deployment...")

    return {
        "version": "2.4.0",
        "environment": "production"
    }


# ==========================================
# NODE 2
# ==========================================

def human_approval(state: DeploymentState):

    approval_request = {
        "message": "Production deployment requires approval.",
        "version": state["version"],
        "environment": state["environment"],
        "action": "deploy"
    }

    decision = interrupt(approval_request)

    return {
        "approved": decision
    }


# ==========================================
# NODE 3
# ==========================================

def deploy_application(state: DeploymentState):

    print("\n🚀 Deploying application...")

    return {
        "deployment_status": "DEPLOYED"
    }


# ==========================================
# ROUTER
# ==========================================

def route_after_approval(state: DeploymentState):

    if state["approved"]:
        return "deploy"

    return "end"


# ==========================================
# GRAPH
# ==========================================

builder = StateGraph(DeploymentState)


builder.add_node(
    "prepare",
    prepare_deployment
)

builder.add_node(
    "approval",
    human_approval
)

builder.add_node(
    "deploy",
    deploy_application
)


builder.add_edge(
    START,
    "prepare"
)

builder.add_edge(
    "prepare",
    "approval"
)

builder.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "deploy": "deploy",
        "end": END
    }
)

builder.add_edge(
    "deploy",
    END
)


# ==========================================
# CHECKPOINTER
# ==========================================

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# ==========================================
# THREAD
# ==========================================

config = {
    "configurable": {
        "thread_id": "deployment-001"
    }
}


# ==========================================
# INITIAL RUN
# ==========================================

result = graph.invoke(
    {
        "request": "Deploy version 2.4.0 to production",
        "version": "",
        "environment": "",
        "approved": False,
        "deployment_status": ""
    },
    config
)


print("\n================================")
print("GRAPH PAUSED")
print("================================")

print(result["__interrupt__"])


# ==========================================
# HUMAN APPROVES
# ==========================================

result = graph.invoke(
    Command(resume=True),
    config
)


print("\n================================")
print("FINAL RESULT")
print("================================")

print(result)