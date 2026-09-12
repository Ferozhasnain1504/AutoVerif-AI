from agent.llm_client import LLMClient


class FaultDiagnoser:

    def __init__(self):

        self.llm = LLMClient()

    def diagnose(
        self,
        rtl_info,
        localization
    ):

        prompt = f"""
You are an expert RTL design and hardware verification engineer.

A deterministic fault-localization system has identified
evidence of a possible RTL defect.

Your job is to analyze the evidence and produce a concise
technical diagnosis.

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

Fault found:
{localization["fault_found"]}

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

================ TASK ================

Determine:

1. What is likely wrong?
2. Which RTL expression is suspicious?
3. What behavior should the RTL produce?
4. What change would likely correct the defect?

IMPORTANT:

- Do not generate a complete RTL module.
- Do not modify the RTL.
- Do not invent signals that are not present.
- Use the deterministic evidence as the primary source.
- If the evidence is insufficient, explicitly say so.
- Do not blindly assume the RTL is wrong.
- Keep the diagnosis concise and technically precise.

Return exactly this format:

DIAGNOSIS: <technical explanation>

SUSPICIOUS_EXPRESSION: <expression>

EXPECTED_BEHAVIOR: <expected behavior>

RECOMMENDED_CHANGE: <recommended change>

CONFIDENCE: <HIGH, MEDIUM, or LOW>

Return only these five sections.
"""

        return self.llm.generate(prompt)