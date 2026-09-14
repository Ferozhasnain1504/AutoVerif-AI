from pathlib import Path
import subprocess
import re

from agent.rtl_analyzer import RTLAnalyzer
from agent.reference_model import ReferenceModel
from agent.strategy_selector import StrategySelector
from agent.strategy_test_generator import StrategyTestGenerator
from agent.testbench_generator import TestbenchGenerator


def main():

    print("\n========================================")
    print("   STRATEGY SIMULATION INTEGRATION TEST")
    print("========================================")

    rtl_file = "rtl/adder_faulty.v"
    generated_tb = Path("testbench/generated_strategy_tb.v")
    build_dir = Path("simulator/build")
    output_file = build_dir / "strategy_integration.vvp"

    # 1. Analyze RTL
    analyzer = RTLAnalyzer()
    rtl_info = analyzer.analyze(rtl_file)

    # 2. Create independent reference model
    reference_model = ReferenceModel("adder")
    reference_behavior = reference_model.get_expected_behavior()

    # 3. Select verification strategies
    selector = StrategySelector()
    strategies = selector.select_strategies(rtl_info)

    print("\nSelected strategies:")

    for strategy in strategies:
        print(f"- {strategy.value}")

    # 4. Generate test cases
    strategy_generator = StrategyTestGenerator()

    test_cases = strategy_generator.generate(
        rtl_info,
        strategies
    )

    print(f"\nGenerated test cases: {len(test_cases)}")

    # 5. Generate AI testbench
    generator = TestbenchGenerator()

    verification_plan = """
    Verify the 4-bit unsigned adder using boundary,
    normal, and exhaustive input testing.

    The expected output is:

    sum = a + b

    The expected behavior must come from the independent
    reference model, not from the RTL implementation.

    The generated testbench must compare the DUT output
    against independently calculated expected values.
    """

    generated_testbench = generator.generate(
        rtl_info=rtl_info,
        verification_plan=verification_plan,
        reference_behavior=reference_behavior,
        strategies=strategies,
        test_cases=test_cases,
    )

    generated_tb.write_text(
        generated_testbench,
        encoding="utf-8"
    )

    print("\nTestbench generated.")

    # 6. Prepare simulation build directory
    build_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # 7. Compile generated testbench
    compile_command = [
        "iverilog",
        "-o",
        str(output_file),
        rtl_file,
        str(generated_tb),
    ]

    print("\nCompiling generated testbench...")

    compile_result = subprocess.run(
        compile_command,
        capture_output=True,
        text=True
    )

    if compile_result.returncode != 0:

        print("COMPILATION FAILED")
        print(compile_result.stderr)

        generated_tb.unlink(missing_ok=True)
        output_file.unlink(missing_ok=True)

        raise SystemExit(1)

    print("Compilation successful.")

    # 8. Run simulation
    print("\nRunning simulation...")

    simulation_result = subprocess.run(
        ["vvp", str(output_file)],
        capture_output=True,
        text=True
    )

    print(simulation_result.stdout)

    if simulation_result.returncode != 0:

        print("SIMULATION FAILED")

        if simulation_result.stderr:
            print(simulation_result.stderr)

        generated_tb.unlink(missing_ok=True)
        output_file.unlink(missing_ok=True)

        raise SystemExit(1)

    # 9. Validate simulation results
    output = simulation_result.stdout

    normalized_output = re.sub(
        r"\s+",
        " ",
        output.lower()
    )

    required_patterns = [
        r"total tests executed\s*:\s*256",
        r"total tests passed\s*:\s*0",
        r"total tests failed\s*:\s*256",
    ]

    for pattern in required_patterns:

        if not re.search(pattern, normalized_output):

            print(
                f"Missing expected simulation result: {pattern}"
            )

            generated_tb.unlink(missing_ok=True)
            output_file.unlink(missing_ok=True)

            raise SystemExit(1)

    # 10. Clean temporary simulation artifacts
    generated_tb.unlink(missing_ok=True)
    output_file.unlink(missing_ok=True)

    print("\nTemporary simulation artifacts cleaned.")

    # 11. Final result
    print("\nSTRATEGY SIMULATION INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()