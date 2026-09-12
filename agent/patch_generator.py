from agent.llm_client import LLMClient


class PatchGenerator:

    def __init__(self):

        self.llm = LLMClient()

    def generate_patch(
        self,
        rtl_info,
        localization,
        diagnosis
    ):

        prompt = f"""
You are an expert Verilog RTL repair engineer.

A verification system has detected a possible RTL defect.

Your task is to propose a MINIMAL source-code change
that could repair the defect.

================ RTL INFORMATION ================

Module:
{rtl_info["module"]}

Inputs:
{rtl_info["inputs"]}

Outputs:
{rtl_info["outputs"]}

Assignments:
{rtl_info["assignments"]}

================ FAULT LOCALIZATION ================

Signal:
{localization["signal"]}

Expression:
{localization["expression"]}

Expected:
{localization["expected"]}

Actual:
{localization["actual"]}

Difference:
{localization["difference"]}

Pattern:
{localization["pattern"]}

Finding:
{localization["finding"]}

Confidence:
{localization["confidence"]}

================ AI DIAGNOSIS ================

{diagnosis}

================ TASK ================

Generate a minimal RTL patch.

IMPORTANT RULES:

1. Modify only the suspicious expression.
2. Do not redesign the module.
3. Do not change module ports.
4. Do not add unrelated logic.
5. Do not generate a complete RTL module.
6. Do not use markdown.
7. Do not use code fences.
8. Return only the requested patch information.
9. The proposed replacement must be valid Verilog.
10. If the evidence is insufficient, say that a patch cannot
    be safely generated.

Return exactly this format:

TARGET_SIGNAL: <signal name>

OLD_EXPRESSION: <current expression>

NEW_EXPRESSION: <replacement expression>

PATCH_REASON: <short explanation>

CONFIDENCE: <HIGH, MEDIUM, or LOW>
"""

        return self.llm.generate(prompt)