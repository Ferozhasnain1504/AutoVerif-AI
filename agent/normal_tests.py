class NormalTestGenerator:

    def generate(self, rtl_info):

        inputs = rtl_info.get("inputs", {})

        if isinstance(inputs, dict):
            input_names = list(inputs.keys())
            widths = list(inputs.values())

        elif isinstance(inputs, list):
            input_names = []
            widths = []

            for signal in inputs:

                signal = signal.strip()

                if "[" not in signal or ":" not in signal:
                    raise ValueError(
                        f"Unable to determine width for input: {signal}"
                    )

                width_part = signal.split("[", 1)[1]
                width_part = width_part.split("]", 1)[0]

                msb, lsb = width_part.split(":")

                parts = signal.split()

                if parts[0] == "input":
                    input_name = parts[-1]
                else:
                    input_name = parts[0]

                input_names.append(input_name)

                widths.append(
                    abs(int(msb) - int(lsb)) + 1
                )

        else:
            raise ValueError("Unsupported RTL input format.")

        if len(input_names) != 2:
            raise ValueError(
                "NormalTestGenerator currently supports "
                "exactly two inputs."
            )

        max_values = [
            (1 << width) - 1
            for width in widths
        ]

        input_a = input_names[0]
        input_b = input_names[1]

        test_cases = [
            {input_a: 1, input_b: 2},
            {input_a: 3, input_b: 4},
            {input_a: 5, input_b: 7},
            {input_a: 8, input_b: 6},
            {input_a: 10, input_b: 3},
            {input_a: 7, input_b: 9},
        ]

        for case in test_cases:

            if (
                case[input_a] > max_values[0]
                or case[input_b] > max_values[1]
            ):
                raise ValueError(
                    "Generated normal test case exceeds "
                    "input width."
                )

        return test_cases