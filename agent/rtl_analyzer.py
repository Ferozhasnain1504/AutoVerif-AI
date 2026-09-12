import re
from pathlib import Path


class RTLAnalyzer:

    def analyze(self, rtl_file):

        rtl_file = Path(rtl_file)

        if not rtl_file.exists():
            raise FileNotFoundError(
                f"RTL file not found: {rtl_file}"
            )

        code = rtl_file.read_text()

        module_name = self._extract_module_name(code)

        inputs = self._extract_ports(code, "input")

        outputs = self._extract_ports(code, "output")

        return {
            "module": module_name,
            "inputs": inputs,
            "outputs": outputs,
        }

    def _extract_module_name(self, code):

        match = re.search(
            r"\bmodule\s+(\w+)",
            code
        )

        if not match:
            raise ValueError(
                "Could not find module name."
            )

        return match.group(1)

    def _extract_ports(self, code, port_type):

        pattern = rf"{port_type}\s+\[(\d+):(\d+)\]\s+(\w+)"

        matches = re.findall(pattern, code)

        ports = {}

        for msb, lsb, name in matches:

            width = abs(
                int(msb) - int(lsb)
            ) + 1

            ports[name] = width

        return ports