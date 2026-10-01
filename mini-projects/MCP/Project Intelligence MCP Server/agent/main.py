import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

async def main():

    # --------------------------------
    # 1. Create MCP Client
    # --------------------------------

    client = MultiServerMCPClient(
        {
            "project": {
                "command": "python",
                "args": [
                    "mcp_server/server.py"
                ],
                "transport": "stdio",
            }
        }
    )

    # --------------------------------
    # 2. Discover MCP tools
    # --------------------------------

    tools = await client.get_tools()
    resource = await client.get_resources()
    prompts = await client.get_prompt()

    print("\nDiscovered MCP tools:")

    for tool in tools:
        print("-", tool.name)

    # --------------------------------
    # 3. Create LLM
    # --------------------------------

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    # --------------------------------
    # 4. Bind MCP tools to model
    # --------------------------------

    model_with_tools = model.bind_tools(tools)

    # --------------------------------
    # 5. Model node
    # --------------------------------

    def call_model(state: MessagesState):

        response = model_with_tools.invoke(
            state["messages"]
        )

        return {
            "messages": [response]
        }

    # --------------------------------
    # 6. Build LangGraph
    # --------------------------------

    builder = StateGraph(MessagesState)

    builder.add_node(
        "agent",
        call_model
    )

    builder.add_node(
        "tools",
        ToolNode(tools)
    )

    builder.add_edge(
        START,
        "agent"
    )

    builder.add_conditional_edges(
        "agent",
        tools_condition
    )

    builder.add_edge(
        "tools",
        "agent"
    )

    graph = builder.compile()

    # --------------------------------
    # 7. Ask the agent
    # --------------------------------

    result = await graph.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "List the files in the project."
                }
            ]
        }
    )

    print("\nFINAL RESPONSE:\n")

    print(
        result["messages"][-1].content
    )


if __name__ == "__main__":
    asyncio.run(main())