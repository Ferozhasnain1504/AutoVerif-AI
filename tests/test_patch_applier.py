from pathlib import Path

from agent.patch_applier import PatchApplier


def main():

    print("\n========================================")
    print("         RTL PATCH APPLIER TEST")
    print("========================================")

    input_file = Path(
        "rtl/adder_faulty.v"
    )

    output_file = Path(
        "rtl/repaired/adder_faulty_repaired.v"
    )

    old_expression = "a + b + 1"

    new_expression = "a + b"

    print("\n[1] Original RTL:")

    print(
        input_file.read_text(
            encoding="utf-8"
        )
    )

    print("\n[2] Applying patch...")

    applier = PatchApplier()

    result = applier.apply(
        input_file,
        old_expression,
        new_expression,
        output_file
    )

    print("\n========== PATCH RESULT ==========")

    print(
        "Success:",
        result["success"]
    )

    print(
        "Input:",
        result["input_file"]
    )

    print(
        "Output:",
        result["output_file"]
    )

    print(
        "Old expression:",
        result["old_expression"]
    )

    print(
        "New expression:",
        result["new_expression"]
    )

    print("\n[3] Repaired RTL:")

    print(
        output_file.read_text(
            encoding="utf-8"
        )
    )

    # Verify original RTL was not modified.

    original_code = input_file.read_text(
        encoding="utf-8"
    )

    repaired_code = output_file.read_text(
        encoding="utf-8"
    )

    print("\n[4] Safety checks...")

    if "a + b + 1" in original_code:

        print(
            "PASS: Original RTL remains unchanged."
        )

    else:

        print(
            "FAIL: Original RTL was modified."
        )

    if "a + b;" in repaired_code:

        print(
            "PASS: Repaired RTL contains the new expression."
        )

    else:

        print(
            "FAIL: Repaired RTL does not contain the new expression."
        )


if __name__ == "__main__":
    main()