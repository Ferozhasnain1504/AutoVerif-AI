import subprocess
from pathlib import Path


class SimulationRunner:

    def __init__(self, timeout=10):
        self.timeout = timeout

    def run(self, simulation_file):

        simulation_file = Path(simulation_file)

        command = [
            "vvp",
            str(simulation_file),
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timeout": False,
            }

        except subprocess.TimeoutExpired as error:

            return {
                "success": False,
                "return_code": None,
                "stdout": error.stdout or "",
                "stderr": "Simulation timed out.",
                "timeout": True,
            }