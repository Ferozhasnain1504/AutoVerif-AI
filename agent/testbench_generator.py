from agent.llm_client import LLMClient


class TestbenchGenerator:

    def __init__(self):
        self.llm = LLMClient()

    def generate(self, rtl_info, verification_plan):

        prompt = f"""
You are an expert Verilog verification engineer.

Generate a complete, synthesizable-compatible Verilog testbench
for the RTL module described below.

RTL information:

Module:
{rtl_info["module"]}

Inputs:
{rtl_info["inputs"]}

Outputs:
{rtl_info["outputs"]}

Assignments:
{rtl_info["assignments"]}

Verification strategy:

{verification_plan}

STRICT REQUIREMENTS:

1. Generate Verilog-2001 code only.
2. Do NOT use SystemVerilog.
3. Instantiate the DUT correctly.
4. Declare every required signal.
5. Test normal cases.
6. Test boundary cases.
7. Test important corner cases.
8. Calculate expected outputs correctly.
9. Compare actual outputs with expected outputs.
10. Print exactly "PASS:" when a test passes.
11. Print exactly "FAIL:" when a test fails.
12. Use $finish to terminate the simulation.
13. The testbench must compile with Icarus Verilog.
14. Do not use classes.
15. Do not use SystemVerilog types such as logic, bit, always_comb, always_ff, or string.
16. Avoid complex string parameters and string variables.
17. Do not use assertions.
18. Keep the testbench simple and portable.
19. Do not include markdown.
20. Do not include ```verilog or ``` around the code.
21. Return ONLY the Verilog source code.
"""

        return self.llm.generate(prompt)