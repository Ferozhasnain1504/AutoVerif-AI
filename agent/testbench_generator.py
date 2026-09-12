from agent.llm_client import LLMClient


class TestbenchGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate(self, rtl_info, verification_plan):

        prompt = f"""
You are an expert Verilog verification engineer.

Your task is to generate ONLY a testbench for an EXISTING RTL module.

IMPORTANT:

The RTL module already exists.

You must NOT recreate, redefine, or copy the RTL module.

The testbench must instantiate the existing DUT.

EXISTING RTL MODULE:

Module name:
{rtl_info["module"]}

Inputs:
{rtl_info["inputs"]}

Outputs:
{rtl_info["outputs"]}

Assignments:
{rtl_info["assignments"]}

VERIFICATION PLAN:

{verification_plan}

STRICT REQUIREMENTS:

1. Generate Verilog-2001 only.
2. Generate ONLY the testbench.
3. Do NOT generate the RTL module.
4. Do NOT declare a module named "{rtl_info["module"]}".
5. The DUT module "{rtl_info["module"]}" already exists in a separate RTL file.
6. Create exactly ONE testbench module.
7. The testbench module name must be "{rtl_info["module"]}_tb".
8. Instantiate the existing DUT inside the testbench.
9. Use the exact DUT port names provided above.
10. Declare all required testbench signals.
11. Test normal cases.
12. Test boundary cases.
13. Test important corner cases.
14. Calculate expected outputs correctly.
15. Compare actual outputs with expected outputs.
16. Print exactly "PASS:" when a test passes.
17. Print exactly "FAIL:" when a test fails.
18. Use $finish to terminate the simulation.
19. The testbench must compile with Icarus Verilog.
20. Do not use SystemVerilog.
21. Do not use classes.
22. Do not use logic.
23. Do not use bit.
24. Do not use always_comb.
25. Do not use always_ff.
26. Do not use string variables.
27. Do not use assertions.
28. Do not include the RTL implementation.
29. Do not include another copy of the DUT.
30. Do not include markdown.
31. Do not include ```verilog.
32. Return ONLY the Verilog testbench source code.

The final output must contain exactly one module declaration:

module {rtl_info["module"]}_tb

and it must instantiate:

{rtl_info["module"]}

Return ONLY Verilog code.
"""

        return self.llm.generate(prompt)