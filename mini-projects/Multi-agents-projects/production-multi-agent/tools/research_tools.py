from langchain.tools import tool

@tool
def search_architecture_knowledge(query: str) -> str:
    """
    Search a small internal architecture knowledge base.

    This simulates a RAG retrieval system.
    """

    knowledge_base = {

        "redis": """
Redis is commonly used for caching, distributed locks,
rate limiting, sessions and ephemeral data.
        """,

        "postgres": """
PostgreSQL is a relational database suitable for
transactional workloads, strong consistency and complex queries.
        """,

        "mongodb": """
MongoDB is a document database useful for flexible
document-oriented data models.
        """,

        "kafka": """
Apache Kafka is a distributed event streaming platform
used for high-throughput asynchronous communication.
        """,

        "load balancer": """
A load balancer distributes incoming traffic across
multiple application instances.
        """,

        "cdn": """
A CDN caches content geographically closer to users,
reducing latency and origin-server load.
        """,

        "microservices": """
Microservices split an application into independently
deployable services communicating through APIs or events.
        """,

        "docker": """
Docker packages applications and their dependencies
into portable containers.
        """,

        "kubernetes": """
Kubernetes orchestrates containerized workloads,
handling scheduling, scaling and service management.
        """,

        "rate limiting": """
Rate limiting restricts request frequency to protect
services from abuse and overload.
        """,
    }

    query_lower = query.lower()

    results = []

    for keyword, information in knowledge_base.items():

        if keyword in query_lower:

            results.append(
                f"[{keyword.upper()}]\n{information.strip()}"
            )

    if not results:

        return "No matching internal architecture knowledge found."

    return "\n\n".join(results)

research_tools = {
    "search_architecture_knowledge":
        search_architecture_knowledge
}