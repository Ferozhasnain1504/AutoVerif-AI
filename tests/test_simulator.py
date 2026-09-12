from simulator.simulation_engine import SimulationEngine


def main():

    engine = SimulationEngine()

    result = engine.execute(
        "rtl/adder.v",
        "testbench/adder_tb.v",
    )

    print("\n========== RESULT ==========")

    print("Status:", result["status"])

    print("Compile Success:", result["compile_success"])

    print("Simulation Success:", result["simulation_success"])

    print("Passed Tests:", result["passed_tests"])

    print("Failed Tests:", result["failed_tests"])

    print("\nSimulation Output:")
    print(result["output"])

    if result["errors"]:
        print("\nErrors:")
        print(result["errors"])


if __name__ == "__main__":
    main()