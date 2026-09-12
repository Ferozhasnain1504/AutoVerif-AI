import subprocess
from pathlib import Path


class VerilogCompiler:

    def __init__(self, output_dir="simulator/build"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compile(self, rtl_file, testbench_file):

        rtl_file = Path(rtl_file)
        testbench_file = Path(testbench_file)

        output_file = self.output_dir / "simulation"

        command = [
            "iverilog",
            "-o",
            str(output_file),
            str(rtl_file),
            str(testbench_file),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "output_file": None,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        return {
            "success": True,
            "output_file": str(output_file),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }