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

    # ----------------------------------------------
    # Verify agent state
    # ----------------------------------------------

    state = result.get("state")

    if not state:

        print("\nSTATE TEST: FAIL")
        print("Agent state was not returned.")

        return

    print("\n========================================")
    print("          AGENT EXECUTION HISTORY")
    print("========================================")

    history = state["history"]

    for event in history:

        print(
            f"- {event['event']}"
        )

    # ----------------------------------------------
    # Validate required events
    # ----------------------------------------------

    required_events = [
        "RTL_ANALYZED",
        "VERIFICATION_PLAN_CREATED",
        "TESTBENCH_GENERATED",
        "SIMULATION_COMPLETED",
        "VERIFICATION_SUCCESSFUL",
    ]

    missing_events = [
        event
        for event in required_events
        if event not in [
            item["event"]
            for item in history
        ]
    ]

    print("\n========================================")

    if (
        result["status"] == "SUCCESS"
        and len(missing_events) == 0
    ):

        print("FULL AGENT STATE TEST: PASS")

    else:

        print("FULL AGENT STATE TEST: FAIL")

        if missing_events:

            print(
                "Missing events:",
                missing_events
            )

    print("========================================")


if __name__ == "__main__":
    main()