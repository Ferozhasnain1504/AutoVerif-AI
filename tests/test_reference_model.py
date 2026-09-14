from agent.reference_model import ReferenceModel


def main():

    print("\n========================================")
    print("       REFERENCE MODEL TEST")
    print("========================================")

    model = ReferenceModel("adder")

    test_cases = [
        {"a": 0, "b": 0, "expected": 0},
        {"a": 1, "b": 2, "expected": 3},
        {"a": 5, "b": 7, "expected": 12},
        {"a": 15, "b": 15, "expected": 30},
    ]

    for test in test_cases:

        result = model.compute({
            "a": test["a"],
            "b": test["b"],
        })

        print(
            f"a={test['a']}, "
            f"b={test['b']}, "
            f"expected={test['expected']}, "
            f"actual={result}"
        )

        if result != test["expected"]:
            print("REFERENCE MODEL TEST: FAIL")
            return

    print("\nREFERENCE MODEL TEST: PASS")

    behavior = model.get_expected_behavior()

    print("\nExpected behavior:")
    print(behavior)


if __name__ == "__main__":
    main()