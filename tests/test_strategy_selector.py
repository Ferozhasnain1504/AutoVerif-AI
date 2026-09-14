from agent.strategy_selector import StrategySelector
from agent.test_strategies import TestStrategy


def main():

    print("\n========================================")
    print("       STRATEGY SELECTOR TEST")
    print("========================================")

    selector = StrategySelector()

    adder_rtl = {
        "module": "adder",
        "inputs": [
            "a [3:0]",
            "b [3:0]"
        ],
        "outputs": [
            "sum [4:0]"
        ]
    }

    strategies = selector.select_strategies(adder_rtl)

    print("\nSelected strategies:")

    for strategy in strategies:
        print(f"- {strategy.value}")

    expected = [
        TestStrategy.BOUNDARY,
        TestStrategy.NORMAL,
        TestStrategy.EXHAUSTIVE,
    ]

    if strategies != expected:
        print("\nSTRATEGY SELECTOR TEST: FAIL")
        return

    print("\nSTRATEGY SELECTOR TEST: PASS")


if __name__ == "__main__":
    main()