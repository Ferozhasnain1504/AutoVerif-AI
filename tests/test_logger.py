import json
from pathlib import Path

from agent.logger import ExecutionLogger


def main():

    print("\n========================================")
    print("        EXECUTION LOGGER TEST")
    print("========================================")

    log_file = Path(
        "reports/test_agent_runs.jsonl"
    )

    # Remove old test log if it exists.
    if log_file.exists():

        log_file.unlink()

    logger = ExecutionLogger(
        str(log_file)
    )

    first_event = logger.log_event(
        event="RTL_ANALYZED",
        attempt=0,
        repair_attempts=0,
        details={
            "module": "adder_faulty"
        }
    )

    second_event = logger.log_event(
        event="SIMULATION_COMPLETED",
        attempt=1,
        repair_attempts=0,
        details={
            "status": "PASS",
            "passed_tests": 256,
            "failed_tests": 0
        }
    )

    print("\nLogged events:")

    print(
        first_event["event"]
    )

    print(
        second_event["event"]
    )

    # ----------------------------------------------
    # Verify file
    # ----------------------------------------------

    if not log_file.exists():

        print("\nLOGGER TEST: FAIL")
        print("Log file was not created.")

        return

    lines = log_file.read_text(
        encoding="utf-8"
    ).strip().splitlines()

    print(
        "\nLog entries:",
        len(lines)
    )

    valid_records = []

    for line in lines:

        record = json.loads(line)

        valid_records.append(record)

        print(
            f"- {record['event']}"
        )

    print("\n========================================")

    if (
        len(valid_records) == 2
        and valid_records[0]["event"]
            == "RTL_ANALYZED"
        and valid_records[1]["event"]
            == "SIMULATION_COMPLETED"
        and valid_records[1]["details"]["status"]
            == "PASS"
    ):

        print("EXECUTION LOGGER TEST: PASS")

    else:

        print("EXECUTION LOGGER TEST: FAIL")

    print("========================================")


if __name__ == "__main__":
    main()