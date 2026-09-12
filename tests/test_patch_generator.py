from agent.rtl_analyzer import RTLAnalyzer
from agent.failure_analyzer import FailureAnalyzer
from agent.fault_localizer import FaultLocalizer
from agent.fault_diagnoser import FaultDiagnoser
from agent.patch_generator import PatchGenerator


def main():

    print("\n========================================")
    print("        RTL PATCH GENERATOR TEST")
    print("========================================")

    # 1. Analyze RTL

    print("\n[1] Analyzing RTL...")

    analyzer = RTLAnalyzer()

    rtl_info = analyzer.analyze(
        "rtl/adder_faulty.v"
    )

    print("RTL analysis complete.")

    # 2. Create controlled failure

    print("\n[2] Creating controlled failure...")

    failed_simulation = {

        "status": "FAIL",

        "compile_success": True,

        "simulation_success": True,

        "passed_tests": 0,

        "failed_tests": 1,

        "output": (
            "FAIL: sum expected=8 actual=9\n"
        ),

        "errors": [],

    }

    # 3. Analyze failure

    print("\n[3] Analyzing failure...")

    failure_analyzer = FailureAnalyzer()

    failure_feedback = (
        failure_analyzer.analyze(
            failed_simulation
        )
    )

    print("Failure analysis complete.")

    # 4. Localize fault

    print("\n[4] Localizing fault...")

    localizer = FaultLocalizer()

    localization = localizer.localize(
        rtl_info,
        failure_feedback
    )

    print("Fault localization complete.")

    # 5. Diagnose fault

    print("\n[5] Diagnosing fault with Gemini...")

    diagnoser = FaultDiagnoser()

    diagnosis = diagnoser.diagnose(
        rtl_info,
        localization
    )

    print("AI diagnosis complete.")

    # 6. Generate patch

    print("\n[6] Generating RTL patch...")

    patch_generator = PatchGenerator()

    patch = patch_generator.generate_patch(
        rtl_info,
        localization,
        diagnosis
    )

    print("\n========== PROPOSED RTL PATCH ==========")

    print(patch)


if __name__ == "__main__":
    main()