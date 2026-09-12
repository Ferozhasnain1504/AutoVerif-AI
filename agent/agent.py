from pathlib import Path

from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.testbench_generator import TestbenchGenerator
from agent.decision_engine import DecisionEngine
from agent.failure_analyzer import FailureAnalyzer
from agent.adaptation_engine import AdaptationEngine
from simulator.simulation_engine import SimulationEngine


class VerificationAgent:

    def __init__(self):

        self.analyzer = RTLAnalyzer()
        self.planner = VerificationPlanner()
        self.generator = TestbenchGenerator()
        self.simulator = SimulationEngine()
        self.decision_engine = DecisionEngine()
        self.failure_analyzer = FailureAnalyzer()
        self.adaptation_engine = AdaptationEngine()

    def run(self, rtl_file, max_attempts=3):

        print("\n========================================")
        print("        AUTOVERIF-AI AGENT")
        print("========================================")

        # OBSERVE
        print("\n[1] Analyzing RTL...")

        rtl_info = self.analyzer.analyze(
            rtl_file
        )

        print("RTL analysis completed.")

        # PLAN
        print("\n[2] Creating verification plan...")

        verification_plan = self.planner.analyze_rtl(
            rtl_info
        )

        print("Verification plan created.")

        # ADAPTATION MEMORY
        adaptation = None

        # AGENT LOOP
        for attempt in range(1, max_attempts + 1):

            print("\n========================================")
            print(
                f"        VERIFICATION ATTEMPT {attempt}"
            )
            print("========================================")

            # ACT
            print("\n[3] Generating testbench...")

            testbench = self.generator.generate(
                rtl_info,
                verification_plan,
                adaptation=adaptation
            )

            output_file = Path(
                "testbench/generated_tb.v"
            )

            output_file.write_text(
                testbench,
                encoding="utf-8"
            )

            print(
                f"Testbench saved to: {output_file}"
            )

            # EVALUATE
            print("\n[4] Running simulation...")

            simulation_result = self.simulator.execute(
                rtl_file,
                str(output_file)
            )

            print("\nSimulation status:",
                  simulation_result["status"])

            print(
                "Passed tests:",
                simulation_result["passed_tests"]
            )

            print(
                "Failed tests:",
                simulation_result["failed_tests"]
            )

            # OBSERVE FAILURE
            failure_feedback = (
                self.failure_analyzer.analyze(
                    simulation_result
                )
            )

            print("\n========== FAILURE ANALYSIS ==========")

            print(
                failure_feedback["summary"]
            )

            # DECIDE
            print("\n[5] Agent deciding next action...")

            decision = self.decision_engine.decide(
                simulation_result
            )

            print("\n========== AGENT DECISION ==========")

            print(decision)

            # SUCCESS
            if simulation_result["status"] == "PASS":

                print("\n========================================")
                print("       VERIFICATION SUCCESSFUL")
                print("========================================")

                return {
                    "status": "SUCCESS",
                    "attempts": attempt,
                    "rtl": rtl_info,
                    "verification_plan": verification_plan,
                    "simulation": simulation_result,
                    "decision": decision,
                    "adaptation": adaptation,
                }

            # LAST ATTEMPT
            if attempt == max_attempts:

                print("\n========================================")
                print("       MAX ATTEMPTS REACHED")
                print("========================================")

                return {
                    "status": "FAILED",
                    "attempts": attempt,
                    "rtl": rtl_info,
                    "verification_plan": verification_plan,
                    "simulation": simulation_result,
                    "decision": decision,
                    "adaptation": adaptation,
                }

            # ADAPT
            print("\n[6] Analyzing failure for adaptation...")

            adaptation = (
                self.adaptation_engine.analyze_failure(
                    rtl_info,
                    verification_plan,
                    failure_feedback
                )
            )

            print(
                "\n========== ADAPTATION =========="
            )

            print(adaptation)

            print(
                "\n[7] Agent will regenerate "
                "the testbench using this adaptation..."
            )

        return None