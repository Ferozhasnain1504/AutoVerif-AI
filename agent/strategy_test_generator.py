from agent.test_strategies import TestStrategy
from agent.boundary_tests import BoundaryTestGenerator
from agent.normal_tests import NormalTestGenerator
from agent.exhaustive_tests import ExhaustiveTestGenerator


class StrategyTestGenerator:

    def __init__(self):
        self.boundary_generator = BoundaryTestGenerator()
        self.normal_generator = NormalTestGenerator()
        self.exhaustive_generator = ExhaustiveTestGenerator()

    def generate(self, rtl_info, strategies):

        all_cases = []

        for strategy in strategies:

            if strategy == TestStrategy.BOUNDARY:
                cases = self.boundary_generator.generate(rtl_info)

            elif strategy == TestStrategy.NORMAL:
                cases = self.normal_generator.generate(rtl_info)

            elif strategy == TestStrategy.EXHAUSTIVE:
                cases = self.exhaustive_generator.generate(rtl_info)

            else:
                raise ValueError(
                    f"Unsupported test strategy: {strategy}"
                )

            all_cases.extend(cases)

        return self._remove_duplicates(all_cases)

    def _remove_duplicates(self, test_cases):

        unique_cases = []
        seen = set()

        for case in test_cases:

            key = tuple(sorted(case.items()))

            if key not in seen:
                seen.add(key)
                unique_cases.append(case)

        return unique_cases