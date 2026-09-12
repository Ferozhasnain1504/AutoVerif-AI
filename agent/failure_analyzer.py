class FailureAnalyzer:

    def analyze(self, simulation_result):

        status = simulation_result["status"]

        if status == "PASS":
            return {
                "has_failure": False,
                "status": status,
                "summary": "Verification passed successfully.",
                "failure_output": "",
                "errors": [],
            }

        failure_output = simulation_result.get(
            "output",
            ""
        )

        errors = simulation_result.get(
            "errors",
            []
        )

        if isinstance(errors, str):
            errors = [errors] if errors else []

        return {
            "has_failure": True,
            "status": status,
            "summary": self._create_summary(
                simulation_result
            ),
            "failure_output": failure_output,
            "errors": errors,
        }

    def _create_summary(self, simulation_result):

        status = simulation_result["status"]

        passed = simulation_result.get(
            "passed_tests",
            0
        )

        failed = simulation_result.get(
            "failed_tests",
            0
        )

        if status == "FAIL":

            return (
                f"Verification failed. "
                f"{failed} tests failed and "
                f"{passed} tests passed."
            )

        if status == "COMPILE_ERROR":

            return (
                "The generated testbench failed "
                "to compile."
            )

        if status == "SIMULATION_ERROR":

            return (
                "The simulation encountered "
                "an execution error."
            )

        if status == "TIMEOUT":

            return (
                "The simulation exceeded the "
                "allowed timeout."
            )

        return (
            f"Verification ended with status: {status}"
        )