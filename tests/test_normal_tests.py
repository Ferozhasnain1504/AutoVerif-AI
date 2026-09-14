from agent.normal_tests import NormalTestGenerator


def main():

    print("\n========================================")
    print("       NORMAL TEST GENERATOR")
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

    generator = NormalTestGenerator()

    test_cases = generator.generate(rtl_info)

    print("\nGenerated normal cases:")

    for case in test_cases:
        print(case)

    expected = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 7},
        {"a": 8, "b": 6},
        {"a": 10, "b": 3},
        {"a": 7, "b": 9},
    ]

    if test_cases != expected:
        print("\nNORMAL TEST GENERATOR: FAIL")
        return

    print("\nNORMAL TEST GENERATOR: PASS")


if __name__ == "__main__":
    main()