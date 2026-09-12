from simulator.simulation_engine import SimulationEngine


def main():

    engine = SimulationEngine()

    result = engine.execute(
        "rtl/adder.v",
        "testbench/adder_tb.v",
    )

    print("\n========== RESULT ==========")

    print("Status:", result["status"])

    if "output" in result:
        print("\nSimulation Output:")
        print(result["output"])

    if "stderr" in result:
        print("\nErrors:")
        print(result["stderr"])


if __name__ == "__main__":
    main()