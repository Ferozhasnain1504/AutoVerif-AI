from agent.agent import VerificationAgent


def main():

    agent = VerificationAgent()

    result = agent.run(
        "rtl/adder.v",
        max_attempts=3
    )

    print("\n========================================")
    print("        FINAL AGENT RESULT")
    print("========================================")

    print(
        "\nOverall Status:",
        result["status"]
    )

    print(
        "Attempts:",
        result["attempts"]
    )

    print(
        "Simulation Status:",
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

    print("\nFinal Decision:")

    print(
        result["decision"]
    )


if __name__ == "__main__":
    main()