from enum import Enum


class TestStrategy(Enum):
    BOUNDARY = "boundary"
    NORMAL = "normal"
    EXHAUSTIVE = "exhaustive"


class TestStrategyManager:

    def get_available_strategies(self):
        return [
            TestStrategy.BOUNDARY,
            TestStrategy.NORMAL,
            TestStrategy.EXHAUSTIVE,
        ]

    def describe_strategy(self, strategy):

        descriptions = {
            TestStrategy.BOUNDARY:
                "Tests minimum, maximum, zero, and edge-case input values.",

            TestStrategy.NORMAL:
                "Tests representative functional input combinations.",

            TestStrategy.EXHAUSTIVE:
                "Tests every possible input combination when the input space is practical.",
        }

        return descriptions[strategy]