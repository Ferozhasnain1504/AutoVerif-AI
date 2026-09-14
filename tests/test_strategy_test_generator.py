from agent.strategy_test_generator import StrategyTestGenerator
from agent.test_strategies import TestStrategy


def main():

    print("\n========================================")
    print("     STRATEGY TEST GENERATOR TEST")
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

    strategies = [
        TestStrategy.BOUNDARY,
        TestStrategy.NORMAL,
        TestStrategy.EXHAUSTIVE,
    ]

    generator = StrategyTestGenerator()

    test_cases = generator.generate(
        rtl_info,
        strategies
    )

    print(f"\nTotal unique test cases: {len(test_cases)}")

    print("\nFirst 5 cases:")

    for case in test_cases[:5]:
        print(case)

    print("\nLast 5 cases:")

    for case in test_cases[-5:]:
        print(case)

    if len(test_cases) != 256:
        print("\nSTRATEGY TEST GENERATOR: FAIL")
        return

    unique_cases = {
        (case["a"], case["b"])
        for case in test_cases
    }

    if len(unique_cases) != 256:
        print("\nSTRATEGY TEST GENERATOR: FAIL")
        return

    print("\nSTRATEGY TEST GENERATOR: PASS")


if __name__ == "__main__":
    main()