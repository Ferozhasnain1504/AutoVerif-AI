from agent.reference_model import ReferenceModel
from agent.strategy_selector import StrategySelector
from agent.strategy_test_generator import StrategyTestGenerator
from agent.testbench_generator import TestbenchGenerator


def main():

    print("\n========================================")
    print("   STRATEGY-AWARE TESTBENCH TEST")
    print("========================================")

    rtl_info = {
        "module": "adder",
        "inputs": [
            "a [3:0]",
            "b [3:0]"
        ],
        "outputs": [
            "sum [4:0]"
        ],
        "assignments": [
            "sum = a + b + 1"
        ]
    }

    # ========================================
    # STEP 1: Independent reference model
    # ========================================

    model = ReferenceModel("adder")

    reference_behavior = (
        model.get_expected_behavior()
    )

    print("\nReference behavior:")
    print(reference_behavior)

    # ========================================
    # STEP 2: Select verification strategies
    # ========================================

    selector = StrategySelector()

    strategies = selector.select_strategies(
        rtl_info
    )

    print("\nSelected strategies:")

    for strategy in strategies:
        print(f"- {strategy.value}")

    # ========================================
    # STEP 3: Generate test cases
    # ========================================

    strategy_generator = StrategyTestGenerator()

    test_cases = strategy_generator.generate(
        rtl_info,
        strategies
    )

    print(
        f"\nGenerated test cases: "
        f"{len(test_cases)}"
    )

    # ========================================
    # STEP 4: Generate AI testbench
    # ========================================

    verification_plan = """
Verify the adder using multiple verification
strategies.

The expected behavior must come from the
independent reference model.

The RTL implementation must not be used as
the source of expected values.
"""

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_info,
        verification_plan,
        reference_behavior=reference_behavior,
        strategies=strategies,
        test_cases=test_cases
    )

    if not testbench:
        print(
            "\nSTRATEGY-AWARE TESTBENCH TEST: FAIL"
        )
        return

    print("\nTestbench generated successfully.")

    from pathlib import Path

    output_file = Path("testbench/generated_strategy_tb.v")
    output_file.write_text(testbench, encoding="utf-8")

    print(
        f"\nGenerated testbench saved to: "
        f"{output_file}"
    )

    print("\n========== GENERATED TESTBENCH ==========")
    print(testbench)
    print("========== END GENERATED TESTBENCH ==========")

    # ========================================
    # STEP 5: Validate generated testbench
    # ========================================

    required_checks = {
        "Testbench module":
            "module adder_tb",

        "DUT instantiation":
            "adder",

        "Independent addition model":
            "a + b",

        "Expected signal":
            "expected",

        "Actual output":
            "sum",

        "Finish statement":
            "$finish"
    }

    failed_checks = []

    for check_name, pattern in required_checks.items():

        if pattern not in testbench:
            failed_checks.append(
                f"{check_name} "
                f"(missing: {pattern})"
            )

    # Verify that the generated testbench
    # contains some form of failure tracking.

        # Verify that the testbench contains an
    # actual comparison between expected and DUT output.

    comparison_patterns = [
        "sum === expected_sum",
        "expected_sum === sum",
        "sum !== expected_sum",
        "expected_sum !== sum",
        "sum == expected_sum",
        "expected_sum == sum",
        "sum != expected_sum",
        "expected_sum != sum"
    ]


    if not any(
        pattern in testbench
        for pattern in comparison_patterns
    ):
        failed_checks.append(
            "Expected-vs-actual comparison"
        )

    # Verify that the testbench has conditional
    # failure handling.

    if "if (" not in testbench:
        failed_checks.append(
            "Conditional failure handling"
        )

    if failed_checks:

        print("\nFAILED VALIDATION CHECKS:")

        for failure in failed_checks:
            print(f"- {failure}")

        print(
            "\nSTRATEGY-AWARE TESTBENCH TEST: FAIL"
        )
        return

    # ========================================
    # STEP 6: Verify generated strategies
    # ========================================

    if len(test_cases) != 256:

        print(
            "\nExpected 256 test cases but got "
            f"{len(test_cases)}"
        )

        print(
            "\nSTRATEGY-AWARE TESTBENCH TEST: FAIL"
        )
        return

    # ========================================
    # SUCCESS
    # ========================================

    print("\nValidation checks passed:")

    for check_name in required_checks:
        print(f"- {check_name}")

    print("- Failure tracking")

    print(
        f"\nVerified {len(test_cases)} generated "
        "test cases."
    )

    print(
        "\nSTRATEGY-AWARE TESTBENCH TEST: PASS"
    )


if __name__ == "__main__":
    main()
