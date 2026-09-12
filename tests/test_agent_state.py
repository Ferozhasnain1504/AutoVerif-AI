from agent.state import AgentState


def main():

    print("\n========================================")
    print("        AGENT STATE TEST")
    print("========================================")

    state = AgentState(
        rtl_file="rtl/adder_faulty.v",
        current_rtl="rtl/adder_faulty.v",
        max_attempts=3
    )

    print("\nInitial status:")
    print(state.status)

    state.attempt = 1

    state.record_event(
        "RTL_ANALYZED",
        {
            "module": "adder_faulty"
        }
    )

    state.record_event(
        "TESTBENCH_GENERATED"
    )

    state.simulation_result = {
        "status": "FAIL",
        "passed_tests": 0,
        "failed_tests": 256
    }

    state.status = "FAILURE_DETECTED"

    state.record_event(
        "SIMULATION_FAILED",
        {
            "failed_tests": 256
        }
    )

    print("\nCurrent status:")
    print(state.status)

    print("\nHistory:")

    for event in state.history:

        print(
            f"- {event['event']}"
        )

    print("\nDictionary conversion:")

    state_dict = state.to_dict()

    print(
        "RTL:",
        state_dict["rtl_file"]
    )

    print(
        "Attempt:",
        state_dict["attempt"]
    )

    print(
        "History events:",
        len(state_dict["history"])
    )

    print("\n========================================")

    if (
        state.status == "FAILURE_DETECTED"
        and len(state.history) == 3
        and state.simulation_result["failed_tests"] == 256
    ):

        print("AGENT STATE TEST: PASS")

    else:

        print("AGENT STATE TEST: FAIL")


if __name__ == "__main__":
    main()