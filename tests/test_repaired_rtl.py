from simulator.simulation_engine import SimulationEngine


def main():

    print("\n========================================")
    print("       REPAIRED RTL VALIDATION")
    print("========================================")

    rtl_file = (
        "rtl/repaired/adder_faulty_repaired.v"
    )

    testbench_file = (
        "testbench/failing_tb.v"
    )

    print("\n[1] Repaired RTL:")
    print(rtl_file)

    print("\n[2] Testbench:")
    print(testbench_file)

    print("\n[3] Running simulation...")

    simulator = SimulationEngine()

    result = simulator.execute(
        rtl_file,
        testbench_file
    )

    print("\n========== VALIDATION RESULT ==========")

    print(
        "Status:",
        result["status"]
    )

    print(
        "Compilation successful:",
        result["compile_success"]
    )

    print(
        "Simulation successful:",
        result["simulation_success"]
    )

    print(
        "Passed tests:",
        result["passed_tests"]
    )

    print(
        "Failed tests:",
        result["failed_tests"]
    )

    print(
        "\nSimulation output:"
    )

    print(
        result["output"]
    )

    print("\n========================================")

    if result["status"] == "PASS":

        print(
            "       SELF-HEALING VALIDATED"
        )

        print(
            "========================================"
        )

    else:

        print(
            "       REPAIR VALIDATION FAILED"
        )

        print(
            "========================================"
        )


if __name__ == "__main__":
    main()