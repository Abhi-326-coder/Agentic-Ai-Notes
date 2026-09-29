from .graph import graph


def main():

    goal = input(
        "\nWhat should the Deep Agent do?\n> "
    )

    initial_state = {

        "goal": goal,

        "plan": [],

        "current_task": "",

        "completed_tasks": [],

        "failed_tasks": [],

        "observations": [],

        "retry_count": 0,

        "requires_approval": False,

        "approved": False,

        "final_result": ""
    }

    result = graph.invoke(initial_state)

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(
        result["final_result"]
    )


if __name__ == "__main__":
    main()