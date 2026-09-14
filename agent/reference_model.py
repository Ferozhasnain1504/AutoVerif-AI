class ReferenceModel:

    def __init__(self, module_type="adder"):
        self.module_type = module_type

    def compute(self, inputs):
        if self.module_type == "adder":
            a = inputs["a"]
            b = inputs["b"]

            return a + b

        raise ValueError(
            f"Unsupported module type: {self.module_type}"
        )

    def get_expected_behavior(self):
        if self.module_type == "adder":
            return {
                "description": "5-bit unsigned addition",
                "expression": "a + b",
                "inputs": ["a", "b"],
                "output": "sum",
            }

        raise ValueError(
            f"Unsupported module type: {self.module_type}"
        )