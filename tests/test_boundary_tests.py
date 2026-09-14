from agent.boundary_tests import BoundaryTestGenerator


def main():

    print("\n========================================")
    print("       BOUNDARY TEST GENERATOR")
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

    generator = BoundaryTestGenerator()

    test_cases = generator.generate(rtl_info)

    print("\nGenerated boundary cases:")

    for case in test_cases:
        print(case)

    expected = [
        {"a": 0, "b": 0},
        {"a": 0, "b": 15},
        {"a": 15, "b": 0},
        {"a": 15, "b": 15},
    ]

    if test_cases != expected:
        print("\nBOUNDARY TEST GENERATOR: FAIL")
        return

    print("\nBOUNDARY TEST GENERATOR: PASS")


if __name__ == "__main__":
    main()