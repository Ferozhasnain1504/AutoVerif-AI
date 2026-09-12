from pathlib import Path


class PatchApplier:

    def apply(
        self,
        rtl_file,
        old_expression,
        new_expression,
        output_file
    ):

        rtl_file = Path(rtl_file)

        output_file = Path(output_file)

        if not rtl_file.exists():

            raise FileNotFoundError(
                f"RTL file not found: {rtl_file}"
            )

        code = rtl_file.read_text(
            encoding="utf-8"
        )

        # Make sure the expression actually exists.

        occurrences = code.count(
            old_expression
        )

        if occurrences == 0:

            raise ValueError(
                "Old expression was not found "
                "in the RTL."
            )

        if occurrences > 1:

            raise ValueError(
                "Old expression appears multiple "
                "times in the RTL. Patch rejected "
                "to avoid ambiguous modification."
            )

        # Apply exactly one replacement.

        repaired_code = code.replace(
            old_expression,
            new_expression,
            1
        )

        # Create output directory if needed.

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file.write_text(
            repaired_code,
            encoding="utf-8"
        )

        return {
            "success": True,
            "input_file": str(rtl_file),
            "output_file": str(output_file),
            "old_expression": old_expression,
            "new_expression": new_expression,
        }