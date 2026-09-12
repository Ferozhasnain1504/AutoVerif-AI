from pathlib import Path

from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.testbench_generator import TestbenchGenerator
from simulator.simulation_engine import SimulationEngine


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

    print("\nStep 3: Generating testbench...")

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_info,
        verification_plan
    )

    print("\nStep 4: Saving generated testbench...")

    output_file = Path(
        "testbench/generated_tb.v"
    )

    output_file.write_text(
        testbench,
        encoding="utf-8"
    )

    print(
        f"Generated testbench saved to: {output_file}"
    )

    print("\nStep 5: Running AI-generated testbench...")

    engine = SimulationEngine()

    result = engine.execute(
        "rtl/adder.v",
        "testbench/generated_tb.v"
    )

    print("\n========== AI VERIFICATION RESULT ==========")

    print("Status:", result["status"])

    print(
        "Compile Success:",
        result["compile_success"]
    )

    print(
        "Simulation Success:",
        result["simulation_success"]
    )

    print(
        "Passed Tests:",
        result["passed_tests"]
    )

    print(
        "Failed Tests:",
        result["failed_tests"]
    )

    print("\nSimulation Output:")

    print(result["output"])

    if result["errors"]:

        print("\nErrors:")

        print(result["errors"])


if __name__ == "__main__":
    main()