from agent.agent import Agent


def main():

    agent = Agent()

    answer = agent.run(
        "What is 25 multiplied by 4?"
    )

    print("\nFINAL ANSWER")
    print(answer)


if __name__ == "__main__":
    main()