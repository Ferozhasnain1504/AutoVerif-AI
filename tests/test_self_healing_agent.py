from agent.agent import VerificationAgent


def main():

    print("\n========================================")
    print("      FULL SELF-HEALING AGENT TEST")
    print("========================================")

    agent = VerificationAgent()

    result = agent.run(
        "rtl/adder_faulty.v",
        max_attempts=1
    )

    print("\n========================================")
    print("          FINAL RESULT")
    print("========================================")

    print(
        "Status:",
        result["status"]
    )

    print(
        "Attempts:",
        result["attempts"]
    )

    print(
        "Repair attempts:",
        result.get(
            "repair_attempts",
            0
        )
    )

    print(
        "Repaired RTL:",
        result.get(
            "repaired_rtl",
            "None"
        )
    )

    print("\n========================================")


if __name__ == "__main__":
    main()