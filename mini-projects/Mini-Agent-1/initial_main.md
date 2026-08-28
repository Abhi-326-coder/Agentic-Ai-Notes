from google.genai import types

from agent.loop import run_agent
from agent.state import AgentState
from tools.formatters import get_llm_tools


def main():

    tools = get_llm_tools()
    
    print("WELCOM TO MINI-AGENT")

    user_message = input("Enter the prompt and see the magic \n")

    state = AgentState()

    state.contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_message
                )
            ],
        )
    )

    final_answer = run_agent(
        state,
        tools
    )

    print("\nFINAL ANSWER")
    print(final_answer)


if __name__ == "__main__":
    main()