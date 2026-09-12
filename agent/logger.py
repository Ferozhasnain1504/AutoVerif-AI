import json
from datetime import datetime
from pathlib import Path


class ExecutionLogger:

    def __init__(
        self,
        log_file="reports/agent_runs.jsonl"
    ):

        self.log_file = Path(log_file)

        self.log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def log_event(
        self,
        event,
        attempt=0,
        repair_attempts=0,
        details=None
    ):

        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "attempt": attempt,
            "repair_attempts": repair_attempts,
            "details": details or {},
        }

        with self.log_file.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(record)
                + "\n"
            )

        return record

    def log_state(self, state):

        for event in state.history:

            self.log_event(
                event=event["event"],
                attempt=event.get(
                    "attempt",
                    0
                ),
                repair_attempts=event.get(
                    "repair_attempts",
                    0
                ),
                details=event.get(
                    "details",
                    {}
                )
            )