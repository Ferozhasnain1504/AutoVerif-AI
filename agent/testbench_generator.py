from agent.llm_client import LLMClient


class TestbenchGenerator:

    def __init__(self):

        self.llm = LLMClient()

    def generate(
        self,
        rtl_info,
        verification_plan,
        adaptation=None
    ):

        prompt = f"""
You are an expert Verilog verification engineer.

Your task is to generate ONLY a testbench for an EXISTING RTL module.

The RTL module already exists.
You must NOT recreate, redefine, or copy the RTL module.

The testbench must instantiate the existing DUT.

================ RTL INFORMATION ================

Module:
{rtl_info["module"]}

Inputs:
{rtl_info["inputs"]}

Outputs:
{rtl_info["outputs"]}

Assignments:
{rtl_info["assignments"]}

================ VERIFICATION PLAN ================

{verification_plan}

================ PREVIOUS ADAPTATION ================

{adaptation if adaptation else "No previous failure. This is the first verification attempt."}

================ CRITICAL VERIFICATION RULES ================

The testbench must independently determine the EXPECTED behavior
of the DUT.

NEVER derive the expected value by copying the RTL implementation.

For example, if the RTL contains:

assign sum = a + b + 1;

and the intended behavior is addition:

expected_sum = a + b;

NOT:

expected_sum = a + b + 1;

The testbench must detect implementation bugs.

The expected-value calculation must represent the INTENDED
functional behavior, not the CURRENT RTL implementation.

The testbench must contain real functional comparisons.

Do not create a testbench that merely checks whether the
DUT produces some value.

Each test case must compare:

EXPECTED VALUE
against
ACTUAL DUT OUTPUT

and report PASS or FAIL accordingly.

================ TESTING REQUIREMENTS ================

1. Generate Verilog-2001 only.
2. Generate ONLY the testbench.
3. Do NOT generate the RTL module.
4. Do NOT declare a module named "{rtl_info["module"]}".
5. The existing DUT module is named "{rtl_info["module"]}".
6. Create exactly ONE testbench module.
7. The testbench module name must be "{rtl_info["module"]}_tb".
8. Instantiate the existing DUT.
9. Declare appropriate reg inputs.
10. Declare appropriate wire outputs.
11. Generate meaningful functional test cases.
12. Include boundary cases.
13. Include representative normal cases.
14. Include exhaustive testing when practical.
15. Calculate expected outputs independently.
16. Compare expected outputs with actual DUT outputs.
17. Increment a failure counter whenever a mismatch occurs.
18. Print clear PASS and FAIL messages.
19. Print a final verification summary.
20. Call $finish.
21. The testbench must compile with Icarus Verilog.
22. If a previous adaptation recommendation is provided,
    incorporate relevant recommendations.
23. Do not blindly trust the RTL implementation.
24. Do not use the RTL assignment itself as the expected-value model.
25. The testbench must be capable of detecting an incorrect
    constant, incorrect operator, missing operation, or similar
    functional defect.
26. Do not generate self-fulfilling tests.
27. The expected model must be independent from the DUT.
28. Do not include another copy of the DUT.
29. Do not include markdown.
30. Do not include ```verilog.
31. Return ONLY the Verilog testbench source code.

================ FINAL VALIDATION REQUIREMENT ================

Before returning the testbench, mentally verify:

"If the RTL contains a deliberate +1 bug in an otherwise
normal addition module, will this testbench detect it?"

If the answer is NO, revise the testbench.

Return ONLY Verilog code.
"""

        return self.llm.generate(prompt)