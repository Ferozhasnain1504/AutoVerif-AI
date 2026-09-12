from agent.llm_client import LLMClient


class DecisionEngine:

    def __init__(self):

        self.llm = LLMClient()

    def decide(self, simulation_result):

        prompt = f"""
You are an autonomous hardware verification agent.

Analyze the simulation result below and decide what the
verification system should do next.

Simulation status:
{simulation_result["status"]}

Compilation successful:
{simulation_result["compile_success"]}

Simulation successful:
{simulation_result["simulation_success"]}

Passed tests:
{simulation_result["passed_tests"]}

Failed tests:
{simulation_result["failed_tests"]}

Simulation output:
{simulation_result["output"]}

Errors:
{simulation_result["errors"]}

Choose exactly ONE action from:

PASS
REGENERATE_TESTBENCH
INVESTIGATE_SIMULATION_ERROR
HANDLE_TIMEOUT

Rules:

- If status is PASS, choose PASS.
- If status is FAIL, choose REGENERATE_TESTBENCH.
- If status is COMPILE_ERROR, choose REGENERATE_TESTBENCH.
- If status is SIMULATION_ERROR, choose INVESTIGATE_SIMULATION_ERROR.
- If status is TIMEOUT, choose HANDLE_TIMEOUT.

Return your response in exactly this format:

ACTION: <one action>

REASON: <short explanation>

Do not return markdown.
"""

        response = self.llm.generate(prompt)

        return response