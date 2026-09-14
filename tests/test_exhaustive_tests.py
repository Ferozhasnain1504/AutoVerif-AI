from agent.exhaustive_tests import ExhaustiveTestGenerator


def main():

    print("\n========================================")
    print("       EXHAUSTIVE TEST GENERATOR")
    print("========================================")

    rtl_info = {
        "module": "adder",
        "inputs": [
            "a [3:0]",
            "b [3:0]"
        ],
        "outputs": [
            "sum [4:0]"
        ]
    }

    generator = ExhaustiveTestGenerator()

    test_cases = generator.generate(rtl_info)

    print(f"\nTotal test cases generated: {len(test_cases)}")

    print("\nFirst 5 cases:")

    for case in test_cases[:5]:
        print(case)

    print("\nLast 5 cases:")

    for case in test_cases[-5:]:
        print(case)

    if len(test_cases) != 256:
        print("\nEXHAUSTIVE TEST GENERATOR: FAIL")
        return

    if test_cases[0] != {"a": 0, "b": 0}:
        print("\nEXHAUSTIVE TEST GENERATOR: FAIL")
        return

    if test_cases[-1] != {"a": 15, "b": 15}:
        print("\nEXHAUSTIVE TEST GENERATOR: FAIL")
        return

    unique_cases = {
        (case["a"], case["b"])
        for case in test_cases
    }

    if len(unique_cases) != 256:
        print("\nEXHAUSTIVE TEST GENERATOR: FAIL")
        return

    print("\nEXHAUSTIVE TEST GENERATOR: PASS")


if __name__ == "__main__":
    main()