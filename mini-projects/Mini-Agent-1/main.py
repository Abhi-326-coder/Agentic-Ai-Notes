from agent.agent import Agent
from agent.cli import print_banner, print_help
from tools.registry import TOOL_SCHEMAS


def main():

    print_banner()

    agent = Agent()

    print("Type /help to see available commands.\n")

    while True:

        try:
            user_input = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # -----------------------------
        # EXIT
        # -----------------------------

        if user_input == "/exit":
            print("Goodbye!")
            break

        # -----------------------------
        # HELP
        # -----------------------------

        if user_input == "/help":
            print_help()
            continue

        # -----------------------------
        # CLEAR MEMORY
        # -----------------------------

        if user_input == "/clear":
            agent.memory.clear()
            print("Conversation memory cleared.")
            continue

        # -----------------------------
        # SHOW STATE
        # -----------------------------

        if user_input == "/state":

            state = agent.get_state()

            if state is None:
                print("No agent execution yet.")
                continue

            print("\nCurrent State:")
            print("Iterations:", state.iteration)
            print("Tool calls:", state.tool_calls)
            print("Observations:", state.observations)
            print("Final answer:", state.final_answer)

            continue

        # -----------------------------
        # SHOW TOOLS
        # -----------------------------

        if user_input == "/tools":

            print("\nAvailable tools:")

            for tool in TOOL_SCHEMAS.values():
                print(
                    f"- {tool.name}: "
                    f"{tool.description}"
                )

            continue

        # -----------------------------
        # RUN AGENT
        # -----------------------------

        try:

            result = agent.run(
                user_input
            )

            print("\nAgent:")
            print(result.final_answer)
            print()

        except Exception as error:

            print(
                f"\nAgent error: {error}\n"
            )


if __name__ == "__main__":
    main()
