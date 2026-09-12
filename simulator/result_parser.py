import re


class SimulationResultParser:

    def parse(
        self,
        compilation,
        simulation
    ):

        compile_success = compilation.get(
            "success",
            False
        )

        simulation_success = simulation.get(
            "success",
            False
        )

        stdout = simulation.get(
            "stdout",
            ""
        )

        stderr = simulation.get(
            "stderr",
            ""
        )

        output = stdout

        if stderr:
            output += "\n" + stderr

        # --------------------------------------------------
        # Compilation failure
        # --------------------------------------------------

        if not compile_success:

            return {
                "status": "COMPILE_ERROR",
                "compile_success": False,
                "simulation_success": False,
                "passed_tests": 0,
                "failed_tests": 0,
                "output": output,
                "errors": [stderr] if stderr else [
                    "Compilation failed."
                ],
            }

        # --------------------------------------------------
        # Simulation timeout
        # --------------------------------------------------

        if simulation.get("timeout", False):

            return {
                "status": "TIMEOUT",
                "compile_success": True,
                "simulation_success": False,
                "passed_tests": 0,
                "failed_tests": 0,
                "output": output,
                "errors": [
                    "Simulation timed out."
                ],
            }

        # --------------------------------------------------
        # Simulation execution failure
        # --------------------------------------------------

        if not simulation_success:

            return {
                "status": "SIMULATION_ERROR",
                "compile_success": True,
                "simulation_success": False,
                "passed_tests": 0,
                "failed_tests": 0,
                "output": output,
                "errors": [stderr] if stderr else [
                    "Simulation execution failed."
                ],
            }

        # --------------------------------------------------
        # Extract total test count
        #
        # Supports multiple LLM-generated formats:
        #
        # Total Test Cases Run : 256
        # Total Tests Executed : 256
        # Total Tests Conducted : 256
        # Total Test Vectors Applied : 256
        # --------------------------------------------------

        total_patterns = [

            r"Total\s+Test\s+Cases\s+Run\s*:\s*(\d+)",

            r"Total\s+Tests\s+Executed\s*:\s*(\d+)",

            r"Total\s+Tests\s+Conducted\s*:\s*(\d+)",

            r"Total\s+Test\s+Vectors\s+Applied\s*:\s*(\d+)",

        ]

        total_tests = 0

        for pattern in total_patterns:

            match = re.search(
                pattern,
                stdout,
                re.IGNORECASE
            )

            if match:

                total_tests = int(
                    match.group(1)
                )

                break

        # --------------------------------------------------
        # Extract passed test count
        #
        # Supports:
        #
        # Total Passed : 256
        # Passed Test Cases : 256
        # --------------------------------------------------

        passed_patterns = [

            r"Total\s+Passed\s*:\s*(\d+)",

            r"Passed\s+Test\s+Cases\s*:\s*(\d+)",

        ]

        passed_tests = 0

        for pattern in passed_patterns:

            match = re.search(
                pattern,
                stdout,
                re.IGNORECASE
            )

            if match:

                passed_tests = int(
                    match.group(1)
                )

                break

        # --------------------------------------------------
        # Extract failed test count
        #
        # Supports:
        #
        # Total Failures : 256
        # Total Errors Found : 256
        # Total Failed : 256
        # Failed Test Cases : 256
        # --------------------------------------------------

        failure_patterns = [

            r"Total\s+Failures\s*:\s*(\d+)",

            r"Total\s+Errors\s+Found\s*:\s*(\d+)",

            r"Total\s+Failed\s*:\s*(\d+)",

            r"Failed\s+Test\s+Cases\s*:\s*(\d+)",

        ]

        failed_tests = 0

        for pattern in failure_patterns:

            match = re.search(
                pattern,
                stdout,
                re.IGNORECASE
            )

            if match:

                failed_tests = int(
                    match.group(1)
                )

                break

        # --------------------------------------------------
        # If passed count wasn't explicitly reported,
        # calculate it from total - failed.
        # --------------------------------------------------

        if passed_tests == 0 and total_tests > 0:

            passed_tests = max(
                total_tests - failed_tests,
                0
            )

        # --------------------------------------------------
        # Detect explicit final verification status
        #
        # Supports:
        #
        # OVERALL STATUS: PASSED
        # OVERALL TEST RESULT: PASSED
        # OVERALL TEST STATUS: PASSED
        # --------------------------------------------------

        status_patterns = [

            r"OVERALL\s+STATUS\s*:\s*(PASSED|FAILED)",

            r"OVERALL\s+TEST\s+RESULT\s*:\s*(PASSED|FAILED)",

            r"OVERALL\s+TEST\s+STATUS\s*:\s*(PASSED|FAILED)",

        ]

        final_status = None

        for pattern in status_patterns:

            match = re.search(
                pattern,
                stdout,
                re.IGNORECASE
            )

            if match:

                final_status = (
                    match.group(1).upper()
                )

                break

        # --------------------------------------------------
        # Handle:
        #
        # RESULT: ALL TESTS PASSED SUCCESSFULLY
        # --------------------------------------------------

        if final_status is None:

            success_match = re.search(
                r"RESULT\s*:\s*ALL\s+TESTS\s+PASSED\s+SUCCESSFULLY",
                stdout,
                re.IGNORECASE
            )

            if success_match:

                final_status = "PASSED"

        # --------------------------------------------------
        # Explicit PASS
        # --------------------------------------------------

        if final_status == "PASSED":

            return {
                "status": "PASS",
                "compile_success": True,
                "simulation_success": True,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "output": stdout,
                "errors": [],
            }

        # --------------------------------------------------
        # Explicit FAIL
        # --------------------------------------------------

        if final_status == "FAILED":

            return {
                "status": "FAIL",
                "compile_success": True,
                "simulation_success": True,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "output": stdout,
                "errors": [],
            }

        # --------------------------------------------------
        # Statistical fallback
        #
        # If the simulation reports a total number of tests,
        # the statistics themselves are enough to determine
        # PASS or FAIL.
        # --------------------------------------------------

        if total_tests > 0:

            if failed_tests == 0:

                return {
                    "status": "PASS",
                    "compile_success": True,
                    "simulation_success": True,
                    "passed_tests": passed_tests,
                    "failed_tests": 0,
                    "output": stdout,
                    "errors": [],
                }

            return {
                "status": "FAIL",
                "compile_success": True,
                "simulation_success": True,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "output": stdout,
                "errors": [],
            }

        # --------------------------------------------------
        # Fallback for simple PASS / FAIL output
        # --------------------------------------------------

        fail_count = len(
            re.findall(
                r"^\s*FAIL\b",
                stdout,
                re.MULTILINE
            )
        )

        pass_count = len(
            re.findall(
                r"^\s*PASS\b",
                stdout,
                re.MULTILINE
            )
        )

        if fail_count > 0:

            return {
                "status": "FAIL",
                "compile_success": True,
                "simulation_success": True,
                "passed_tests": pass_count,
                "failed_tests": fail_count,
                "output": stdout,
                "errors": [],
            }

        if pass_count > 0:

            return {
                "status": "PASS",
                "compile_success": True,
                "simulation_success": True,
                "passed_tests": pass_count,
                "failed_tests": 0,
                "output": stdout,
                "errors": [],
            }

        # --------------------------------------------------
        # Unknown verification result
        # --------------------------------------------------

        return {
            "status": "COMPLETED",
            "compile_success": True,
            "simulation_success": True,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "output": stdout,
            "errors": [
                "Simulation completed but no "
                "verification result marker was found."
            ],
        }