from agent.llm_client import LLMClient


class DecisionEngine:

    def __init__(self):

        self.llm = LLMClient()

    def decide(
        self,
        simulation_result
    ):

        prompt = f"""
You are an autonomous hardware verification
and RTL repair decision engine.

Analyze the simulation result below and decide
what the verification system should do next.

================ SIMULATION RESULT ================

Status:
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

================ AVAILABLE ACTIONS ================

Choose exactly ONE:

PASS
REPAIR_RTL
REGENERATE_TESTBENCH
INVESTIGATE_SIMULATION_ERROR
HANDLE_TIMEOUT

================ DECISION RULES ================

1. If status is PASS:
   choose PASS.

2. If status is FAIL and the simulation executed
   successfully:
   choose REPAIR_RTL.

3. If status is COMPILE_ERROR:
   choose REGENERATE_TESTBENCH.

4. If status is SIMULATION_ERROR:
   choose INVESTIGATE_SIMULATION_ERROR.

5. If status is TIMEOUT:
   choose HANDLE_TIMEOUT.

6. If status is COMPLETED:
   choose REGENERATE_TESTBENCH.

The system should prefer RTL repair when a valid
functional verification failure has been observed.

Return exactly:

ACTION: <one action>

REASON: <short explanation>

Do not return markdown.
"""

        return self.llm.generate(
            prompt
        )