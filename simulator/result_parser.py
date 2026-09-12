class SimulationResultParser:

    def parse(self, compilation_result, simulation_result):

        # --------------------------------
        # Compilation failed
        # --------------------------------
        if not compilation_result["success"]:

            return {
                "status": "COMPILE_ERROR",
                "compile_success": False,
                "simulation_success": False,
                "output": "",
                "errors": compilation_result["stderr"],
                "warnings": [],
                "passed_tests": 0,
                "failed_tests": 0,
            }

        # --------------------------------
        # Simulation timeout
        # --------------------------------
        if simulation_result.get("timeout"):

            return {
                "status": "TIMEOUT",
                "compile_success": True,
                "simulation_success": False,
                "output": simulation_result["stdout"],
                "errors": "Simulation exceeded timeout limit.",
                "warnings": [],
                "passed_tests": 0,
                "failed_tests": 0,
            }

        # --------------------------------
        # Simulation runtime error
        # --------------------------------
        if not simulation_result["success"]:

            return {
                "status": "SIMULATION_ERROR",
                "compile_success": True,
                "simulation_success": False,
                "output": simulation_result["stdout"],
                "errors": simulation_result["stderr"],
                "warnings": [],
                "passed_tests": 0,
                "failed_tests": 0,
            }

        # --------------------------------
        # Successful simulation
        # --------------------------------

        output = simulation_result["stdout"]

        passed_tests = output.count("PASS:")
        failed_tests = output.count("FAIL:")

        if failed_tests > 0:
            status = "FAIL"

        elif passed_tests > 0:
            status = "PASS"

        else:
            status = "COMPLETED"

        return {
            "status": status,
            "compile_success": True,
            "simulation_success": True,
            "output": output,
            "errors": [],
            "warnings": [],
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
        }