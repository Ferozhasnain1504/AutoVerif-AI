from agent.llm_client import LLMClient


class AdaptationEngine:

    def __init__(self):

        self.llm = LLMClient()

    def analyze_failure(
        self,
        rtl_info,
        verification_plan,
        failure_feedback
    ):

        prompt = f"""
You are an expert hardware verification engineer
working inside an autonomous verification system.

The verification system generated a testbench,
ran it against an RTL design, and encountered a problem.

Your task is to analyze the failure and recommend
how the verification strategy should adapt.

================ RTL INFORMATION ================

Module:
{rtl_info["module"]}

Inputs:
{rtl_info["inputs"]}

Outputs:
{rtl_info["outputs"]}

Assignments:
{rtl_info["assignments"]}

================ CURRENT PLAN ================

{verification_plan}

================ FAILURE FEEDBACK ================

Status:
{failure_feedback["status"]}

Summary:
{failure_feedback["summary"]}

Simulation Output:
{failure_feedback["failure_output"]}

Errors:
{failure_feedback["errors"]}

================ YOUR TASK ================

Determine:

1. What went wrong?
2. What is the likely cause?
3. What should be changed in the verification strategy?
4. What should the next testbench generation attempt focus on?

IMPORTANT:

- Do not generate Verilog code.
- Do not modify the RTL.
- Do not assume the RTL is necessarily wrong.
- Focus on improving the verification process.
- Be concise and technically precise.

Return exactly this format:

PROBLEM: <description>

LIKELY_CAUSE: <description>

ADAPTATION: <description>

NEXT_FOCUS: <description>

Return only these four sections.
"""

        return self.llm.generate(prompt)