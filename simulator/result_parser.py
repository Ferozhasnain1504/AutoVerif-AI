import re


class SimulationResultParser:

    def parse(self, compilation, simulation):

        compile_success = compilation.get(
            "success",
            False
        )

        simulation_success = simulation.get(
            "success",
            False
        )

        output = simulation.get(
            "stdout",
            ""
        )

        errors = simulation.get(
            "stderr",
            ""
        )

        # ---------------------------------------------------------
        # Compilation failure
        # ---------------------------------------------------------

        if not compile_success:

            return {
                "status": "COMPILE_ERROR",
                "compile_success": False,
                "simulation_success": False,
                "passed_tests": 0,
                "failed_tests": 0,
                "total_tests": 0,
                "output": output,
                "errors": errors,
            }

        # ---------------------------------------------------------
        # Simulation timeout
        # ---------------------------------------------------------

        if simulation.get("timeout", False):

            return {
                "status": "TIMEOUT",
                "compile_success": True,
                "simulation_success": False,
                "passed_tests": 0,
                "failed_tests": 0,
                "total_tests": 0,
                "output": output,
                "errors": errors,
            }

        # ---------------------------------------------------------
        # Simulation execution failure
        # ---------------------------------------------------------

        if not simulation_success:

            return {
                "status": "SIMULATION_ERROR",
                "compile_success": True,
                "simulation_success": False,
                "passed_tests": 0,
                "failed_tests": 0,
                "total_tests": 0,
                "output": output,
                "errors": errors,
            }

        # ---------------------------------------------------------
        # Missing output
        # ---------------------------------------------------------

        if not output:

            return {
                "status": "SIMULATION_ERROR",
                "compile_success": True,
                "simulation_success": True,
                "passed_tests": 0,
                "failed_tests": 0,
                "total_tests": 0,
                "output": output,
                "errors": errors,
            }

        # ---------------------------------------------------------
        # Parse total test count
        # ---------------------------------------------------------

        total_tests = 0

        total_patterns = [
            r"Total Tests Conducted\s*:\s*(\d+)",
            r"Total Tests Run\s*:\s*(\d+)",
            r"Total Test Cases Run\s*:\s*(\d+)",
            r"Total Tests Executed\s*:\s*(\d+)",
            r"Total Test Vectors Applied\s*:\s*(\d+)",
        ]

        for pattern in total_patterns:

            match = re.search(
                pattern,
                output,
                re.IGNORECASE
            )

            if match:
                total_tests = int(
                    match.group(1)
                )
                break

        # ---------------------------------------------------------
        # Parse passed count
        # ---------------------------------------------------------

        passed_tests = 0

        passed_patterns = [
            r"Total Passed\s*:\s*(\d+)",
            r"Total Tests Passed\s*:\s*(\d+)",
            r"Passed Test Cases\s*:\s*(\d+)",
        ]

        for pattern in passed_patterns:

            match = re.search(
                pattern,
                output,
                re.IGNORECASE
            )

            if match:
                passed_tests = int(
                    match.group(1)
                )
                break

        # ---------------------------------------------------------
        # Parse failed count
        # ---------------------------------------------------------

        failed_tests = 0

        failed_patterns = [
            r"Total Failed\s*:\s*(\d+)",
            r"Total Failures\s*:\s*(\d+)",
            r"Failed Test Cases\s*:\s*(\d+)",
            r"Total Errors Found\s*:\s*(\d+)",
        ]

        for pattern in failed_patterns:

            match = re.search(
                pattern,
                output,
                re.IGNORECASE
            )

            if match:
                failed_tests = int(
                    match.group(1)
                )
                break

        # ---------------------------------------------------------
        # Count individual PASS / FAIL test lines
        # ---------------------------------------------------------

        individual_passes = re.findall(
            r"^\s*PASS\s*:\s*Test\s+\d+",
            output,
            re.IGNORECASE | re.MULTILINE
        )

        individual_failures = re.findall(
            r"^\s*FAIL\s*:\s*Test\s+\d+",
            output,
            re.IGNORECASE | re.MULTILINE
        )

        # ---------------------------------------------------------
        # Derive total from individual results
        # ---------------------------------------------------------

        if total_tests == 0:

            total_tests = (
                len(individual_passes)
                + len(individual_failures)
            )

        # ---------------------------------------------------------
        # Derive passed count
        # ---------------------------------------------------------

        if passed_tests == 0 and individual_passes:

            passed_tests = len(
                individual_passes
            )

        # ---------------------------------------------------------
        # Derive failed count
        # ---------------------------------------------------------

        if failed_tests == 0 and individual_failures:

            failed_tests = len(
                individual_failures
            )

        # ---------------------------------------------------------
        # Derive passed tests from total - failures
        # ---------------------------------------------------------

        if (
            passed_tests == 0
            and total_tests > 0
        ):

            passed_tests = (
                total_tests
                - failed_tests
            )

        # ---------------------------------------------------------
        # Determine verification status
        # ---------------------------------------------------------

        upper_output = output.upper()

        pass_markers = [
            "OVERALL STATUS: PASSED",
            "OVERALL TEST RESULT: PASSED",
            "OVERALL TEST STATUS: PASSED",
            "RESULT: ALL TESTS PASSED SUCCESSFULLY",
        ]

        fail_markers = [
            "OVERALL STATUS: FAILED",
            "OVERALL TEST RESULT: FAILED",
            "OVERALL TEST STATUS: FAILED",
        ]

        explicit_pass = any(
            marker in upper_output
            for marker in pass_markers
        )

        explicit_fail = any(
            marker in upper_output
            for marker in fail_markers
        )

        if explicit_pass:

            status = "PASS"

        elif explicit_fail:

            status = "FAIL"

        elif (
            total_tests > 0
            and failed_tests == 0
            and passed_tests == total_tests
        ):

            status = "PASS"

        elif failed_tests > 0:

            status = "FAIL"

        else:

            status = "SIMULATION_ERROR"

        # ---------------------------------------------------------
        # Final structured result
        # ---------------------------------------------------------

        return {
            "status": status,
            "compile_success": True,
            "simulation_success": True,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "total_tests": total_tests,
            "output": output,
            "errors": errors,
        }