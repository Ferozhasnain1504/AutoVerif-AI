import re


class FaultLocalizer:

    def localize(
        self,
        rtl_info,
        failure_feedback
    ):

        if not failure_feedback["has_failure"]:

            return {
                "fault_found": False,
                "signal": None,
                "expression": None,
                "expected": None,
                "actual": None,
                "difference": None,
                "pattern": "NONE",
                "finding": "No failure detected.",
                "reason": "No verification failure detected.",
                "confidence": "NONE",
            }

        failure_output = (
            failure_feedback["failure_output"]
        )

        assignments = rtl_info.get(
            "assignments",
            []
        )

        mismatch = self._extract_mismatch(
            failure_output
        )

        for assignment in assignments:

            target = assignment["target"]

            expression = assignment["expression"]

            if self._signal_appears_in_failure(
                target,
                failure_output
            ):

                expression_analysis = (
                    self._analyze_expression(
                        expression,
                        mismatch
                    )
                )

                reason = (
                    f"Signal '{target}' is associated "
                    "with the observed verification failure."
                )

                if mismatch:

                    expected = mismatch["expected"]

                    actual = mismatch["actual"]

                    difference = mismatch["difference"]

                    reason = (
                        f"Signal '{target}' produced "
                        f"{actual} while {expected} "
                        f"was expected. "
                        f"The observed difference is "
                        f"{difference}. "
                        f"{expression_analysis['finding']}"
                    )

                return {
                    "fault_found": True,

                    "signal": target,

                    "expression": expression,

                    "expected": (
                        mismatch["expected"]
                        if mismatch
                        else None
                    ),

                    "actual": (
                        mismatch["actual"]
                        if mismatch
                        else None
                    ),

                    "difference": (
                        mismatch["difference"]
                        if mismatch
                        else None
                    ),

                    "pattern": expression_analysis[
                        "pattern"
                    ],

                    "finding": expression_analysis[
                        "finding"
                    ],

                    "reason": reason,

                    "confidence": "HIGH",
                }

        return {
            "fault_found": True,

            "signal": None,

            "expression": None,

            "expected": (
                mismatch["expected"]
                if mismatch
                else None
            ),

            "actual": (
                mismatch["actual"]
                if mismatch
                else None
            ),

            "difference": (
                mismatch["difference"]
                if mismatch
                else None
            ),

            "pattern": "UNKNOWN",

            "finding": (
                "No matching RTL assignment "
                "was identified."
            ),

            "reason": (
                "A verification failure was detected, "
                "but no directly matching RTL assignment "
                "could be identified."
            ),

            "confidence": "LOW",
        }

    def _extract_mismatch(
        self,
        failure_output
    ):

        pattern = (
            r"expected\s*=\s*(\d+)"
            r"\s+actual\s*=\s*(\d+)"
        )

        match = re.search(
            pattern,
            failure_output,
            re.IGNORECASE
        )

        if not match:
            return None

        expected = int(
            match.group(1)
        )

        actual = int(
            match.group(2)
        )

        return {
            "expected": expected,
            "actual": actual,
            "difference": actual - expected,
        }

    def _analyze_expression(
        self,
        expression,
        mismatch
    ):

        if not mismatch:

            return {
                "pattern": "UNKNOWN",
                "finding": (
                    "No numerical mismatch available."
                )
            }

        difference = mismatch["difference"]

        # Detect unnecessary positive constant

        positive_constant = re.search(
            r"\+\s*(\d+)\s*$",
            expression
        )

        if positive_constant:

            constant = int(
                positive_constant.group(1)
            )

            if constant == difference:

                return {
                    "pattern": "EXTRA_POSITIVE_CONSTANT",

                    "finding": (
                        f"Expression contains an extra "
                        f"+{constant}, matching the "
                        f"observed output difference of "
                        f"+{difference}."
                    )
                }

        # Detect unnecessary negative constant

        negative_constant = re.search(
            r"-\s*(\d+)\s*$",
            expression
        )

        if negative_constant:

            constant = int(
                negative_constant.group(1)
            )

            if -constant == difference:

                return {
                    "pattern": "EXTRA_NEGATIVE_CONSTANT",

                    "finding": (
                        f"Expression contains an extra "
                        f"-{constant}, matching the "
                        f"observed output difference of "
                        f"{difference}."
                    )
                }

        return {
            "pattern": "NO_SIMPLE_PATTERN",

            "finding": (
                "No simple constant-offset pattern "
                "was detected."
            )
        }

    def _signal_appears_in_failure(
        self,
        signal,
        failure_output
    ):

        pattern = rf"\b{re.escape(signal)}\b"

        return bool(
            re.search(
                pattern,
                failure_output
            )
        )