from agent.llm_client import LLMClient


class VerificationPlanner:

    def __init__(self):
        self.llm = LLMClient()

    def analyze_rtl(self, rtl_info):

        prompt = f"""
You are a hardware verification engineer.

Analyze the following RTL module.

RTL module information:

Module:
{rtl_info["module"]}

Inputs:
{rtl_info["inputs"]}

Outputs:
{rtl_info["outputs"]}

Assignments:
{rtl_info["assignments"]}

Provide a concise analysis containing:

1. Purpose of the module
2. What each input does
3. What each output represents
4. How the output is calculated
5. Important verification scenarios
6. Boundary cases that should be tested

Do not generate Verilog code yet.
"""

        return self.llm.generate(prompt)