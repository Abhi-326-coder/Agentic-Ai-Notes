from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import(
    START, 
    END,
    StateGraph
)
from dotenv import load_dotenv

load_dotenv()

# model

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Engineering State

class EngineeringState(TypedDict):

    task: str

    backend_result: str
    frontend_result: str
    devops_result: str

    final_result: str
    
# Backend Agent

def backend_agent(state: EngineeringState):

    prompt = f"""
You are a Senior Backend Engineer.

Analyze this architecture requirement:

{state["task"]}

Focus on:

- API architecture
- backend services
- authentication
- databases
- caching
- scalability
- reliability
- async processing

Return a backend architecture proposal.
"""

    response = model.invoke(prompt)

    return {
        "backend_result": response.content
    }
    
# Frontend Agent

def frontend_agent(state: EngineeringState):

    prompt = f"""
You are a Senior Frontend Engineer.

Analyze:

{state["task"]}

Focus on:

- frontend architecture
- React/Next.js
- state management
- performance
- CDN
- caching
- API communication
- scalability

Return a frontend architecture proposal.
"""

    response = model.invoke(prompt)

    return {
        "frontend_result": response.content
    }

# Devops Agent

def devops_agent(state: EngineeringState):

    prompt = f"""
You are a Senior DevOps Engineer.

Analyze:

{state["task"]}

Focus on:

- Docker
- Kubernetes
- CI/CD
- load balancing
- autoscaling
- observability
- deployment
- fault tolerance

Return a DevOps architecture proposal.
"""

    response = model.invoke(prompt)

    return {
        "devops_result": response.content
    }
    
# Engineering Manager

def engineering_manager(state: EngineeringState):

    prompt = f"""
You are an Engineering Manager.

Your team contains:

1. Backend Engineer
2. Frontend Engineer
3. DevOps Engineer

Task:

{state["task"]}

For this architecture problem, coordinate
the engineering team.

The team should provide:

- backend architecture
- frontend architecture
- infrastructure architecture

Return a short coordination message.
"""

    response = model.invoke(prompt)

    return {}

# Engineering Graph

engineering_builder = StateGraph(
    EngineeringState
)

# Engineering Nodes

engineering_builder.add_node(
    "manager",
    engineering_manager
)

engineering_builder.add_node(
    "backend",
    backend_agent
)

engineering_builder.add_node(
    "frontend",
    frontend_agent
)

engineering_builder.add_node(
    "devops",
    devops_agent
)

# Engineering Edges

engineering_builder.add_edge(
    START,
    "manager"
)

engineering_builder.add_edge(
    "manager",
    "backend"
)

engineering_builder.add_edge(
    "manager",
    "frontend"
)

engineering_builder.add_edge(
    "manager",
    "devops"
)

# Engineering Synthesizer

def engineering_synthesizer(
    state: EngineeringState
):

    prompt = f"""
You are the Engineering Lead.

Combine these engineering analyses.

TASK:
{state["task"]}

BACKEND:
{state["backend_result"]}

FRONTEND:
{state["frontend_result"]}

DEVOPS:
{state["devops_result"]}

Create one coherent engineering architecture.
"""

    response = model.invoke(prompt)

    return {
        "final_result": response.content
    }

engineering_builder.add_node(
    "synthesizer",
    engineering_synthesizer
)

engineering_builder.add_edge(
    "backend",
    "synthesizer"
)

engineering_builder.add_edge(
    "frontend",
    "synthesizer"
)

engineering_builder.add_edge(
    "devops",
    "synthesizer"
)

engineering_builder.add_edge(
    "synthesizer",
    END
)

engineering_graph = engineering_builder.compile()

# Company state

class CompanyState(TypedDict):

    task: str

    engineering_result: str
    security_result: str
    data_result: str

    final_answer: str
    
# Run Engineering team : Acts as the Adapter

def run_engineering_team(
    state: CompanyState
):

    result = engineering_graph.invoke({

        "task": state["task"],

        "backend_result": "",

        "frontend_result": "",

        "devops_result": "",

        "final_result": ""
    })

    return {
        "engineering_result":
            result["final_result"]
    }
    
# Security State

class SecurityState(TypedDict):

    task: str

    app_security: str
    infra_security: str

    final_result: str
    
# App security Agent

def security_manager(state:SecurityState):
    prompt = f"""
You are an Security Manager.

Your team contains:

1. App Security Engineer
2. Infra Security Engineer

Task:

{state["task"]}

For this architecture problem, coordinate
the engineering team.

The team should provide:

- Backend Security architecture
- frontend Security architecture
- infrastructure Security architecture

Return a short coordination message.
    """
    response = model.invoke(prompt)
    
    return {}
    

def app_security_agent(state: SecurityState):

    prompt = f"""
You are an Application Security Engineer.

Analyze:

{state["task"]}

Focus on:

- authentication
- authorization
- API security
- input validation
- secrets
- data protection
"""

    response = model.invoke(prompt)

    return {
        "app_security": response.content
    }
    
# Infra Security Agent

def infra_security_agent(state: SecurityState):

    prompt = f"""
You are an Infrastructure Security Engineer.

Analyze:

{state["task"]}

Focus on:

- network isolation
- cloud security
- containers
- IAM
- secrets management
- monitoring
"""

    response = model.invoke(prompt)

    return {
        "infra_security": response.content
    }
    
security_builder = StateGraph(
    SecurityState
)

security_builder.add_edge(
    "security_manager",
    security_manager
)

security_builder.add_node(
    "app_security",
    app_security_agent
)

security_builder.add_node(
    "infra_security",
    infra_security_agent
)

security_builder.add_edge(
    START,
    "security_manager"
)

security_builder.add_edge(
    "security_manager",
    "app_security"
)
security_builder.add_edge(
    "security_manager",
    "infra_security"
)

# still need to add the synthsizer for security_builder graph 
# completely compile the security graph 
# then complete the company graph 

