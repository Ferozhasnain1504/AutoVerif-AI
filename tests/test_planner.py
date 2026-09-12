from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner


def main():

    print("Step 1: Reading RTL...")

    analyzer = RTLAnalyzer()

    rtl_info = analyzer.analyze(
        "rtl/adder.v"
    )

    print("RTL successfully analyzed.")

    print("\nStep 2: Asking Gemini to analyze RTL...")

    planner = VerificationPlanner()

    analysis = planner.analyze_rtl(
        rtl_info
    )

    print("\n========== GEMINI RTL ANALYSIS ==========")

    print(analysis)


if __name__ == "__main__":
    main()