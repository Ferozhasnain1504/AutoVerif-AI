from agent.rtl_analyzer import RTLAnalyzer
from agent.failure_analyzer import FailureAnalyzer
from agent.fault_localizer import FaultLocalizer


def main():

    print("\n========================================")
    print("       FAULT LOCALIZATION TEST")
    print("========================================")

    # 1. Analyze RTL

    print("\n[1] Analyzing RTL...")

    analyzer = RTLAnalyzer()

    rtl_info = analyzer.analyze(
        "rtl/adder_faulty.v"
    )

    print("RTL analysis complete.")

    print("\nRTL assignments:")

    for assignment in rtl_info["assignments"]:

        print(
            f"  {assignment['target']} = "
            f"{assignment['expression']}"
        )

    # 2. Create controlled failure

    print("\n[2] Creating failure feedback...")

    failed_simulation = {

        "status": "FAIL",

        "compile_success": True,

        "simulation_success": True,

        "passed_tests": 0,

        "failed_tests": 1,

        "output": (
            "FAIL: sum expected=8 actual=9\n"
        ),

        "errors": [],

    }

    # 3. Analyze failure

    failure_analyzer = FailureAnalyzer()

    failure_feedback = (
        failure_analyzer.analyze(
            failed_simulation
        )
    )

    print("\nFailure feedback:")

    print(
        failure_feedback["summary"]
    )

    # 4. Localize fault

    print("\n[3] Localizing RTL fault...")

    localizer = FaultLocalizer()

    localization = localizer.localize(
        rtl_info,
        failure_feedback
    )

    # 5. Display result

    print("\n========== FAULT LOCALIZATION ==========")

    print(
        "Fault found:",
        localization["fault_found"]
    )

    print(
        "Signal:",
        localization["signal"]
    )

    print(
        "Expression:",
        localization["expression"]
    )

    print(
        "Expected:",
        localization["expected"]
    )

    print(
        "Actual:",
        localization["actual"]
    )

    print(
        "Difference:",
        localization["difference"]
    )

    print(
        "Pattern:",
        localization["pattern"]
    )

    print(
        "Finding:",
        localization["finding"]
    )

    print(
        "Reason:",
        localization["reason"]
    )

    print(
        "Confidence:",
        localization["confidence"]
    )


if __name__ == "__main__":
    main()