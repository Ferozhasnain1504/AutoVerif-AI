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
from agent.state import AgentState

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
        state = AgentState(
            rtl_file=str(rtl_file),
            current_rtl=str(rtl_file),
            max_attempts=max_attempts
        )

        print("\n========================================")
        print("        AUTOVERIF-AI AGENT")
        print("========================================")

        print("\n[1] Analyzing RTL...")

        rtl_info = self.analyzer.analyze(
            rtl_file
        )

        state.rtl_info = rtl_info

        state.record_event(
            "RTL_ANALYZED",
            {
                "module": rtl_info["module"]
            }
        )

        print("RTL analysis completed.")

        print("\n[2] Creating verification plan...")

        verification_plan = (
            self.planner.analyze_rtl(
                rtl_info
            )
        )

        state.verification_plan = verification_plan

        state.record_event(
            "VERIFICATION_PLAN_CREATED"
        )

        print("Verification plan created.")

        adaptation = None

        current_rtl = Path(rtl_file)

        state.current_rtl = str(
            current_rtl
        )

        for attempt in range(
            1,
            max_attempts + 1
        ):
            state.attempt = attempt

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

            state.record_event(
                "TESTBENCH_GENERATED",
                {
                    "file": str(testbench_file)
                }
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

            state.simulation_result = simulation_result

            state.record_event(
                "SIMULATION_COMPLETED",
                {
                    "status": simulation_result["status"]
                }
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

                state.status = "SUCCESS"

                state.record_event(
                    "VERIFICATION_SUCCESSFUL"
                )

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
                        state.repair_attempts,
                    "state": state.to_dict(),
                }

            # -------------------------------------------------
            # FAILURE ANALYSIS
            # -------------------------------------------------

            failure_feedback = (
                self.failure_analyzer.analyze(
                    simulation_result
                )
            )

            state.failure_feedback = failure_feedback

            state.status = "FAILURE_DETECTED"

            state.record_event(
                "FAILURE_DETECTED",
                {
                    "status": simulation_result["status"],
                    "failed_tests": simulation_result[
                        "failed_tests"
                    ]
                }
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

            state.decision = decision

            state.record_event(
                "AGENT_DECISION_MADE"
            )

            print(
                "\n========== AGENT DECISION =========="
            )

            print(decision)

            # -------------------------------------------------
            # RTL SELF-HEALING
            # -------------------------------------------------

            if simulation_result["status"] == "FAIL":

                state.repair_attempts += 1

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

                state.localization = localization

                state.record_event(
                    "FAULT_LOCALIZED",
                    {
                        "signal": localization["signal"],
                        "pattern": localization["pattern"],
                        "confidence": localization["confidence"]
                    }
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

                    state.diagnosis = diagnosis

                    state.record_event(
                        "FAULT_DIAGNOSED"
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

                    state.patch = patch

                    state.record_event(
                        "PATCH_GENERATED"
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
                            f"repair_{state.repair_attempts}.v"
                        )

                        state.repaired_rtl = str(
                            repaired_rtl
                        )

                        state.record_event(
                            "PATCH_APPLIED",
                            {
                                "file": str(repaired_rtl)
                            }
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

                        state.repair_validation = (
                            repaired_simulation
                        )

                        state.record_event(
                            "REPAIR_VALIDATED",
                            {
                                "status": repaired_simulation[
                                    "status"
                                ]
                            }
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

                            state.status = "SELF_HEALED"

                            state.record_event(
                                "SELF_HEALING_SUCCESSFUL"
                            )

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
                                    state.repair_attempts,
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
                                "state": state.to_dict(),
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