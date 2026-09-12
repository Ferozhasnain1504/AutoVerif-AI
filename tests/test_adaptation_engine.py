from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.failure_analyzer import FailureAnalyzer
from agent.adaptation_engine import AdaptationEngine


def main():

    print("Step 1: Analyzing RTL...")

    analyzer = RTLAnalyzer()

    rtl_info = analyzer.analyze(
        "rtl/adder.v"
    )

    print("RTL analysis complete.")

    print("\nStep 2: Creating verification plan...")

    planner = VerificationPlanner()

    verification_plan = planner.analyze_rtl(
        rtl_info
    )

    print("Verification plan created.")

    print("\nStep 3: Creating simulated failure...")

    failed_simulation = {
        "status": "FAIL",
        "passed_tests": 8,
        "failed_tests": 2,
        "output": (
            "PASS: a=1 b=2 expected=3 actual=3\n"
            "FAIL: a=15 b=15 expected=30 actual=31\n"
            "FAIL: a=7 b=8 expected=15 actual=16\n"
        ),
        "errors": [],
    }

    failure_analyzer = FailureAnalyzer()

    failure_feedback = failure_analyzer.analyze(
        failed_simulation
    )

    print("\nFailure feedback:")

    print(failure_feedback)

    print("\nStep 4: Asking Gemini to analyze failure...")

    adaptation = AdaptationEngine()

    recommendation = adaptation.analyze_failure(
        rtl_info,
        verification_plan,
        failure_feedback
    )

    print("\n========== ADAPTATION RECOMMENDATION ==========")

    print(recommendation)


if __name__ == "__main__":
    main()