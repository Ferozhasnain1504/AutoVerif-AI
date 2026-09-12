from pathlib import Path

from agent.rtl_analyzer import RTLAnalyzer
from agent.planner import VerificationPlanner
from agent.testbench_generator import TestbenchGenerator
from agent.decision_engine import DecisionEngine
from agent.failure_analyzer import FailureAnalyzer
from agent.adaptation_engine import AdaptationEngine
from agent.fault_localizer import FaultLocalizer
from agent.fault_diagnoser import FaultDiagnoser
from agent.patch_generator import PatchGenerator
from agent.patch_applier import PatchApplier

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

        self.fault_localizer = FaultLocalizer()
        self.fault_diagnoser = FaultDiagnoser()
        self.patch_generator = PatchGenerator()
        self.patch_applier = PatchApplier()

    def run(
        self,
        rtl_file,
        max_attempts=3
    ):

        print("\n========================================")
        print("        AUTOVERIF-AI AGENT")
        print("========================================")

        print("\n[1] Analyzing RTL...")

        rtl_info = self.analyzer.analyze(
            rtl_file
        )

        print("RTL analysis completed.")

        print("\n[2] Creating verification plan...")

        verification_plan = (
            self.planner.analyze_rtl(
                rtl_info
            )
        )

        print("Verification plan created.")

        adaptation = None

        current_rtl = Path(rtl_file)

        repair_attempt = 0

        for attempt in range(
            1,
            max_attempts + 1
        ):

            print("\n========================================")
            print(
                f"        VERIFICATION ATTEMPT {attempt}"
            )
            print("========================================")

            # -------------------------------------------------
            # TESTBENCH GENERATION
            # -------------------------------------------------

            print("\n[3] Generating testbench...")

            testbench = (
                self.generator.generate(
                    rtl_info,
                    verification_plan,
                    adaptation=adaptation
                )
            )

            testbench_file = Path(
                "testbench/generated_tb.v"
            )

            testbench_file.write_text(
                testbench,
                encoding="utf-8"
            )

            print(
                f"Testbench saved to: {testbench_file}"
            )

            # -------------------------------------------------
            # SIMULATION
            # -------------------------------------------------

            print("\n[4] Running simulation...")

            simulation_result = (
                self.simulator.execute(
                    str(current_rtl),
                    str(testbench_file)
                )
            )

            print(
                "\nSimulation status:",
                simulation_result["status"]
            )

            print(
                "Passed tests:",
                simulation_result[
                    "passed_tests"
                ]
            )

            print(
                "Failed tests:",
                simulation_result[
                    "failed_tests"
                ]
            )

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            if simulation_result["status"] == "PASS":

                print("\n========================================")
                print(
                    "       VERIFICATION SUCCESSFUL"
                )
                print("========================================")

                return {
                    "status": "SUCCESS",
                    "attempts": attempt,
                    "rtl": rtl_info,
                    "verification_plan":
                        verification_plan,
                    "simulation":
                        simulation_result,
                    "decision":
                        "PASS",
                    "repaired_rtl":
                        str(current_rtl),
                    "repair_attempts":
                        repair_attempt,
                }

            # -------------------------------------------------
            # FAILURE ANALYSIS
            # -------------------------------------------------

            failure_feedback = (
                self.failure_analyzer.analyze(
                    simulation_result
                )
            )

            print(
                "\n========== FAILURE ANALYSIS =========="
            )

            print(
                failure_feedback["summary"]
            )

            # -------------------------------------------------
            # AGENT DECISION
            # -------------------------------------------------

            print(
                "\n[5] Agent deciding next action..."
            )

            decision = (
                self.decision_engine.decide(
                    simulation_result
                )
            )

            print(
                "\n========== AGENT DECISION =========="
            )

            print(decision)

            # -------------------------------------------------
            # RTL SELF-HEALING
            # -------------------------------------------------

            if simulation_result["status"] == "FAIL":

                repair_attempt += 1

                print(
                    "\n========================================"
                )

                print(
                    "        RTL SELF-HEALING"
                )

                print(
                    "========================================"
                )

                # ---------------------------------------------
                # FAULT LOCALIZATION
                # ---------------------------------------------

                print(
                    "\n[6] Localizing RTL fault..."
                )

                localization = (
                    self.fault_localizer.localize(
                        rtl_info,
                        failure_feedback
                    )
                )

                print(
                    "\n========== FAULT LOCALIZATION =========="
                )

                print(
                    "Fault found:",
                    localization["fault_found"]
                )

                print(
                    "Signal:",
                    localization["signal"]
                )

                print(
                    "Expression:",
                    localization["expression"]
                )

                print(
                    "Pattern:",
                    localization["pattern"]
                )

                print(
                    "Confidence:",
                    localization["confidence"]
                )

                # ---------------------------------------------
                # AI DIAGNOSIS
                # ---------------------------------------------

                if localization["fault_found"]:

                    print(
                        "\n[7] Diagnosing RTL fault..."
                    )

                    diagnosis = (
                        self.fault_diagnoser.diagnose(
                            rtl_info,
                            localization
                        )
                    )

                    print(
                        "\n========== AI DIAGNOSIS =========="
                    )

                    print(diagnosis)

                    # -----------------------------------------
                    # PATCH GENERATION
                    # -----------------------------------------

                    print(
                        "\n[8] Generating RTL patch..."
                    )

                    patch = (
                        self.patch_generator.generate_patch(
                            rtl_info,
                            localization,
                            diagnosis
                        )
                    )

                    print(
                        "\n========== GENERATED PATCH =========="
                    )

                    print(patch)

                    # -----------------------------------------
                    # PATCH EXTRACTION
                    # -----------------------------------------

                    old_expression = (
                        localization["expression"]
                    )

                    new_expression = None

                    for line in patch.splitlines():

                        if line.startswith(
                            "NEW_EXPRESSION:"
                        ):

                            new_expression = (
                                line.split(
                                    ":",
                                    1
                                )[1]
                                .strip()
                            )

                            break

                    # -----------------------------------------
                    # APPLY PATCH
                    # -----------------------------------------

                    if new_expression:

                        repaired_rtl = Path(
                            "rtl/repaired"
                        ) / (
                            f"repair_{repair_attempt}.v"
                        )

                        print(
                            "\n[9] Applying RTL patch..."
                        )

                        patch_result = (
                            self.patch_applier.apply(
                                current_rtl,
                                old_expression,
                                new_expression,
                                repaired_rtl
                            )
                        )

                        print(
                            "\n========== PATCH RESULT =========="
                        )

                        print(
                            patch_result
                        )

                        # -------------------------------------
                        # VALIDATE REPAIR
                        # -------------------------------------

                        print(
                            "\n[10] Validating repaired RTL..."
                        )

                        repaired_simulation = (
                            self.simulator.execute(
                                str(repaired_rtl),
                                str(testbench_file)
                            )
                        )

                        print(
                            "\n========== REPAIR VALIDATION =========="
                        )

                        print(
                            "Status:",
                            repaired_simulation[
                                "status"
                            ]
                        )

                        print(
                            "Passed tests:",
                            repaired_simulation[
                                "passed_tests"
                            ]
                        )

                        print(
                            "Failed tests:",
                            repaired_simulation[
                                "failed_tests"
                            ]
                        )

                        # -------------------------------------
                        # ACCEPT REPAIR
                        # -------------------------------------

                        if (
                            repaired_simulation[
                                "status"
                            ] == "PASS"
                        ):

                            print(
                                "\n========================================"
                            )

                            print(
                                "       SELF-HEALING SUCCESSFUL"
                            )

                            print(
                                "========================================"
                            )

                            return {
                                "status":
                                    "SELF_HEALED",
                                "attempts":
                                    attempt,
                                "repair_attempts":
                                    repair_attempt,
                                "rtl":
                                    rtl_info,
                                "verification_plan":
                                    verification_plan,
                                "simulation":
                                    repaired_simulation,
                                "diagnosis":
                                    diagnosis,
                                "patch":
                                    patch,
                                "repaired_rtl":
                                    str(
                                        repaired_rtl
                                    ),
                            }

                        print(
                            "\nRepair validation failed."
                        )

                        current_rtl = repaired_rtl

            # -------------------------------------------------
            # ADAPT VERIFICATION STRATEGY
            # -------------------------------------------------

            if attempt < max_attempts:

                print(
                    "\n[11] Analyzing failure for "
                    "verification adaptation..."
                )

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

        print("\n========================================")
        print("       MAX ATTEMPTS REACHED")
        print("========================================")

        return {
            "status": "FAILED",
            "attempts": max_attempts,
            "rtl": rtl_info,
            "verification_plan":
                verification_plan,
        }