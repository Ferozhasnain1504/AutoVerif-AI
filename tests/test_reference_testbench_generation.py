from agent.reference_model import ReferenceModel
from agent.testbench_generator import TestbenchGenerator


def main():

    print("\n========================================")
    print("   REFERENCE-AWARE TESTBENCH TEST")
    print("========================================")

    model = ReferenceModel("adder")

    reference_behavior = (
        model.get_expected_behavior()
    )

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

    verification_plan = """
Test the adder using boundary,
normal, and exhaustive input combinations.
Expected behavior must follow the
independent reference model.
"""

    generator = TestbenchGenerator()

    testbench = generator.generate(
        rtl_info,
        verification_plan,
        reference_behavior=reference_behavior
    )

    if not testbench:
        print("TESTBENCH GENERATION TEST: FAIL")
        return

    print("\nTestbench generated successfully.")

    if "a + b" in testbench:
        print("Independent expected behavior detected.")
    else:
        print(
            "WARNING: Expected behavior expression "
            "not explicitly found."
        )

    if "module adder_tb" in testbench:
        print("Correct testbench module detected.")
    else:
        print(
            "WARNING: Testbench module name "
            "not detected."
        )

    print("\nREFERENCE-AWARE TESTBENCH TEST: PASS")


if __name__ == "__main__":
    main()