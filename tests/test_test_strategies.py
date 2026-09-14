from agent.test_strategies import (
    TestStrategy,
    TestStrategyManager,
)


def main():

    print("\n========================================")
    print("       TEST STRATEGY TEST")
    print("========================================")

    manager = TestStrategyManager()

    strategies = manager.get_available_strategies()

    expected = [
        TestStrategy.BOUNDARY,
        TestStrategy.NORMAL,
        TestStrategy.EXHAUSTIVE,
    ]

    if strategies != expected:
        print("TEST STRATEGY TEST: FAIL")
        return

    print("\nAvailable strategies:")

    for strategy in strategies:

        description = manager.describe_strategy(strategy)

        print(f"\n{strategy.value.upper()}")
        print(description)

    print("\nTEST STRATEGY TEST: PASS")


if __name__ == "__main__":
    main()