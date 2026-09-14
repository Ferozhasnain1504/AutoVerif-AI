from agent.test_strategies import TestStrategy


class StrategySelector:

    def select_strategies(self, rtl_info):

        input_width = self._calculate_input_space(rtl_info)

        strategies = [
            TestStrategy.BOUNDARY,
            TestStrategy.NORMAL,
        ]

        # Exhaustive testing is practical for small input spaces.
        if input_width <= 10:
            strategies.append(TestStrategy.EXHAUSTIVE)

        return strategies

    def _calculate_input_space(self, rtl_info):

        total_bits = 0

        for input_signal in rtl_info.get("inputs", []):

            signal = input_signal.strip()

            if "[" not in signal or ":" not in signal:
                continue

            width_part = signal.split("[", 1)[1]
            width_part = width_part.split("]", 1)[0]

            msb, lsb = width_part.split(":")

            width = abs(int(msb) - int(lsb)) + 1

            total_bits += width

        return total_bits