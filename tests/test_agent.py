from agent.agent import VerificationAgent


def main():

    agent = VerificationAgent()

    result = agent.run(
        "rtl/adder.v"
    )

    print("\n========================================")
    print("        FINAL AGENT RESULT")
    print("========================================")

    print(
        "\nSimulation Status:",
        result["simulation"]["status"]
    )

    print(
        "Passed Tests:",
        result["simulation"]["passed_tests"]
    )

    print(
        "Failed Tests:",
        result["simulation"]["failed_tests"]
    )

    print("\nDecision:")

    print(
        result["decision"]
    )


if __name__ == "__main__":
    main()