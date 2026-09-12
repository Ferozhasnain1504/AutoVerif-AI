from simulator.compiler import VerilogCompiler
from simulator.runner import SimulationRunner
from simulator.result_parser import SimulationResultParser


class SimulationEngine:

    def __init__(self):
        self.compiler = VerilogCompiler()
        self.runner = SimulationRunner()
        self.parser = SimulationResultParser()

    def execute(self, rtl_file, testbench_file):

        print("Step 1: Compiling Verilog...")

        compilation = self.compiler.compile(
            rtl_file,
            testbench_file,
        )

        print("Step 2: Running simulation...")

        if not compilation["success"]:
            return self.parser.parse(
                compilation,
                {
                    "success": False,
                    "stdout": "",
                    "stderr": "",
                },
            )

        simulation = self.runner.run(
            compilation["output_file"]
        )

        print("Step 3: Parsing result...")

        return self.parser.parse(
            compilation,
            simulation,
        )