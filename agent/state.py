from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentState:

    # --------------------------------------------------
    # Run information
    # --------------------------------------------------

    rtl_file: str = ""

    current_rtl: str = ""

    attempt: int = 0

    max_attempts: int = 3

    repair_attempts: int = 0

    # --------------------------------------------------
    # Verification information
    # --------------------------------------------------

    rtl_info: Optional[Dict[str, Any]] = None

    verification_plan: Optional[str] = None

    adaptation: Optional[str] = None

    # --------------------------------------------------
    # Latest simulation information
    # --------------------------------------------------

    simulation_result: Optional[Dict[str, Any]] = None

    failure_feedback: Optional[Dict[str, Any]] = None

    # --------------------------------------------------
    # Fault analysis
    # --------------------------------------------------

    localization: Optional[Dict[str, Any]] = None

    diagnosis: Optional[str] = None

    # --------------------------------------------------
    # Repair information
    # --------------------------------------------------

    patch: Optional[str] = None

    repaired_rtl: Optional[str] = None

    repair_validation: Optional[Dict[str, Any]] = None

    # --------------------------------------------------
    # Agent decision
    # --------------------------------------------------

    decision: Optional[str] = None

    # --------------------------------------------------
    # Final status
    # --------------------------------------------------

    status: str = "INITIALIZED"

    # --------------------------------------------------
    # Execution history
    # --------------------------------------------------

    history: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Record an event
    # --------------------------------------------------

    def record_event(
        self,
        event: str,
        details: Optional[Dict[str, Any]] = None
    ):

        self.history.append({
            "event": event,
            "attempt": self.attempt,
            "repair_attempts": self.repair_attempts,
            "details": details or {},
        })

    # --------------------------------------------------
    # Convert state to dictionary
    # --------------------------------------------------

    def to_dict(self):

        return {
            "rtl_file": self.rtl_file,
            "current_rtl": self.current_rtl,
            "attempt": self.attempt,
            "max_attempts": self.max_attempts,
            "repair_attempts": self.repair_attempts,
            "rtl_info": self.rtl_info,
            "verification_plan": self.verification_plan,
            "adaptation": self.adaptation,
            "simulation_result": self.simulation_result,
            "failure_feedback": self.failure_feedback,
            "localization": self.localization,
            "diagnosis": self.diagnosis,
            "patch": self.patch,
            "repaired_rtl": self.repaired_rtl,
            "repair_validation": self.repair_validation,
            "decision": self.decision,
            "status": self.status,
            "history": self.history,
        }