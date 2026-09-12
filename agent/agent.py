from pathlib import Path

from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.testbench_generator import TestbenchGenerator
from agent.decision_engine import DecisionEngine
from simulator.simulation_engine import SimulationEngine


class VerificationAgent:

    def __init__(self):

        self.analyzer = RTLAnalyzer()
        self.planner = VerificationPlanner()
        self.generator = TestbenchGenerator()
        self.simulator = SimulationEngine()
        self.decision_engine = DecisionEngine()

    def run(self, rtl_file):

        print("\n========================================")
        print("        AUTOVERIF-AI AGENT")
        print("========================================")

        # --------------------------------
        # STEP 1: OBSERVE RTL
        # --------------------------------

        print("\n[1/5] Analyzing RTL...")

        rtl_info = self.analyzer.analyze(
            rtl_file
        )

        print("RTL analysis completed.")

        # --------------------------------
        # STEP 2: DECIDE VERIFICATION PLAN
        # --------------------------------

        print("\n[2/5] Creating verification plan...")

        verification_plan = self.planner.analyze_rtl(
            rtl_info
        )

        print("Verification plan created.")

        # --------------------------------
        # STEP 3: ACT - GENERATE TESTBENCH
        # --------------------------------

        print("\n[3/5] Generating testbench...")

        testbench = self.generator.generate(
            rtl_info,
            verification_plan
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

        # --------------------------------
        # STEP 4: EVALUATE
        # --------------------------------

        print("\n[4/5] Running simulation...")

        simulation_result = self.simulator.execute(
            rtl_file,
            str(output_file)
        )

        print("Simulation completed.")

        print(
            "\nSimulation status:",
            simulation_result["status"]
        )

        # --------------------------------
        # STEP 5: DECIDE NEXT ACTION
        # --------------------------------

        print("\n[5/5] Agent deciding next action...")

        decision = self.decision_engine.decide(
            simulation_result
        )

        print("\n========== AGENT DECISION ==========")

        print(decision)

        return {
            "rtl": rtl_info,
            "verification_plan": verification_plan,
            "testbench": testbench,
            "simulation": simulation_result,
            "decision": decision,
        }