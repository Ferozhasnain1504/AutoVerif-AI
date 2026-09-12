import subprocess
from pathlib import Path


class SimulationRunner:

    def run(self, simulation_file):

        simulation_file = Path(simulation_file)

        command = [
            "vvp",
            str(simulation_file),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }