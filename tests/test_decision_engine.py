from agent.decision_engine import DecisionEngine


def main():

    decision_engine = DecisionEngine()

    simulation_result = {
        "status": "TIMEOUT",
        "compile_success": True,
        "simulation_success": False,
        "passed_tests": 0,
        "failed_tests": 0,
        "output": "",
        "errors": "Simulation exceeded timeout limit.",
    }

    print("Sending simulation result to Decision Engine...")

    decision = decision_engine.decide(
        simulation_result
    )

    print("\n========== AGENT DECISION ==========")

    print(decision)


if __name__ == "__main__":
    main()