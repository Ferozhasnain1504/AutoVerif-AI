from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.testbench_generator import TestbenchGenerator
from agent.failure_analyzer import FailureAnalyzer
from agent.adaptation_engine import AdaptationEngine
from simulator.simulation_engine import SimulationEngine


def main():

    print("\n========================================")
    print("      ADAPTIVE LOOP TEST")
    print("========================================")

    # 1. Analyze RTL

    print("\n[1] Analyzing RTL...")

    analyzer = RTLAnalyzer()

    rtl_info = analyzer.analyze(
        "rtl/adder.v"
    )

    print("RTL analysis complete.")

    # 2. Create verification plan

    print("\n[2] Creating verification plan...")

    planner = VerificationPlanner()

    verification_plan = planner.analyze_rtl(
        rtl_info
    )

    print("Verification plan created.")

    # 3. Create controlled failure

    print("\n[3] Creating controlled failure...")

    failed_simulation = {

        "status": "FAIL",

        "compile_success": True,

        "simulation_success": True,

        "passed_tests": 1,

        "failed_tests": 1,

        "output": (
            "PASS: a=5 b=3 expected=8 actual=8\n"
            "FAIL: a=15 b=15 expected=31 actual=30\n"
        ),

        "errors": [],

    }

    # 4. Analyze failure

    print("\n[4] Analyzing failure...")

    failure_analyzer = FailureAnalyzer()

    failure_feedback = failure_analyzer.analyze(
        failed_simulation
    )

    print("\n========== FAILURE FEEDBACK ==========")

    print(failure_feedback)

    # 5. Generate adaptation

    print("\n[5] Generating adaptation...")

    adaptation_engine = AdaptationEngine()

    adaptation = adaptation_engine.analyze_failure(
        rtl_info,
        verification_plan,
        failure_feedback
    )

    print("\n========== ADAPTATION ==========")

    print(adaptation)

    # 6. Generate adapted testbench

    print("\n[6] Generating adapted testbench...")

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_info,
        verification_plan,
        adaptation=adaptation
    )

    print("\nAdapted testbench generated.")

    # 7. Save adapted testbench

    output_file = "testbench/adaptive_tb.v"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(testbench)

    print(
        f"Saved to: {output_file}"
    )

    # 8. Run real simulator

    print("\n[7] Running adapted testbench...")

    simulator = SimulationEngine()

    result = simulator.execute(
        "rtl/adder.v",
        output_file
    )

    # 9. Final result

    print("\n========================================")
    print("       ADAPTIVE LOOP RESULT")
    print("========================================")

    print(
        "\nStatus:",
        result["status"]
    )

    print(
        "Passed:",
        result["passed_tests"]
    )

    print(
        "Failed:",
        result["failed_tests"]
    )

    print("\nSimulation Output:")

    print(result["output"])


if __name__ == "__main__":
    main()