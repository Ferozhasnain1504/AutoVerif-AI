from simulator.result_parser import SimulationResultParser


def main():

    parser = SimulationResultParser()

    compilation = {
        "success": True
    }

    simulation = {
        "success": True,
        "timeout": False,
        "stdout": """
==================================================
VERIFICATION SUMMARY
==================================================
Total Tests Conducted : 256
Total Passed          : 256
Total Failed          : 0
==================================================
OVERALL TEST STATUS: PASSED
==================================================
""",
        "stderr": ""
    }

    result = parser.parse(
        compilation,
        simulation
    )

    print("\n========================================")
    print("       RESULT PARSER TEST")
    print("========================================")

    print("Status:", result["status"])
    print("Passed:", result["passed_tests"])
    print("Failed:", result["failed_tests"])

    print("========================================")

    if (
        result["status"] == "PASS"
        and result["passed_tests"] == 256
        and result["failed_tests"] == 0
    ):

        print("PARSER TEST: PASS")

    else:

        print("PARSER TEST: FAIL")


if __name__ == "__main__":
    main()