from pathlib import Path

from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.testbench_generator import TestbenchGenerator


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

    adaptation = """
PROBLEM: Previous verification showed incorrect
output values for some addition cases.

LIKELY_CAUSE: The previous testbench may not have
allowed sufficient time for combinational output
settling.

ADAPTATION: Add an explicit delay after driving
the input signals before checking the output.

NEXT_FOCUS: Verify boundary values and all
4-bit input combinations with proper settling time.
"""

    print("\nStep 3: Generating adapted testbench...")

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_info,
        verification_plan,
        adaptation=adaptation
    )

    output_file = Path(
        "testbench/adapted_tb.v"
    )

    output_file.write_text(
        testbench,
        encoding="utf-8"
    )

    print(
        f"Adapted testbench saved to: {output_file}"
    )

    print("\n========== GENERATED TESTBENCH ==========")

    print(testbench)


if __name__ == "__main__":
    main()