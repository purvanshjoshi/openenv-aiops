from typing import Tuple, Dict, Any, Optional
from models import AIOpsAction, AIOpsObservation
from openenv.core.env_server.interfaces import Environment

# Global state persistence for stateless environments
_LAST_TASK = "easy"
_DB_PATCHED = False
_INST_TERM = False
_REFUND_DONE = False

class AIOpsEnv(Environment):
    def __init__(self):
        self._current_obs = AIOpsObservation()
        self._step_count = 0
        self._max_steps = 10
        self._done = False
        self._total_reward = 0.0

    def reset(self, task_name: str = "easy", **kwargs) -> AIOpsObservation:
        global _LAST_TASK, _DB_PATCHED, _INST_TERM, _REFUND_DONE
        _LAST_TASK = task_name.lower()
        self._step_count = 0
        self._done = False
        _DB_PATCHED = False
        _INST_TERM = False
        _REFUND_DONE = False
        self._total_reward = 0.05
        
        self._current_obs = AIOpsObservation(
            system_health_score=100.0,
            budget_remaining=10000.0,
            telemetry_output="Environment Initialized. Waiting for first tool execution.",
            reward=0.05
        )

        if "easy" in _LAST_TASK:
            self._current_obs.incident_id = "INC-101"
            self._current_obs.incident_severity = "P3"
            self._current_obs.incident_description = "Customer Ticket: 'I was billed twice for my plan this month. Please refund the duplicate $50 immediately.'"
        elif "medium" in _LAST_TASK:
            self._current_obs.incident_id = "INC-202"
            self._current_obs.incident_severity = "P2"
            self._current_obs.incident_description = "Compliance Alert: PII leaked in record #999. Redact the patient name and SSN immediately by updating the record."
        else: # hard
            self._current_obs.incident_id = "INC-303"
            self._current_obs.incident_severity = "P1"
            self._current_obs.incident_description = "FinOps Alert: Burn rate exceeded 90%. Identify completely idle 'zombie' nodes in compute cluster and terminate them to save cost."
            
        return self._current_obs

    def state(self) -> AIOpsObservation:
        return self._current_obs

    def close(self):
        self._done = True

    def step(self, action: AIOpsAction, timeout_s: Optional[float] = None, **kwargs: Any) -> AIOpsObservation:
        self._step_count += 1
        reward = 0.0
        output = f"Tool {action.command} executed. No effect."

        cmd = action.command.lower()
        args = action.parameters

        global _DB_PATCHED, _INST_TERM, _REFUND_DONE
        
        # Easy Task: Billing
        if "easy" in _LAST_TASK:
            if cmd == "query_billing":
                output = '{"customer_id": "CUST-001", "transactions": [{"id": 1, "amt": 50}, {"id": 2, "amt": 50}], "status": "duplicate_detected"}'
                reward = 0.05
            elif cmd == "refund":
                if args.get("amount") == 50 or args.get("amount") == 50.0:
                    output = '{"status": "success", "msg": "$50 refunded."}'
                    if not _REFUND_DONE:
                        reward = 0.6
                        _REFUND_DONE = True
                else:
                    output = '{"status": "error", "msg": "Incorrect refund amount."}'
                    reward = 0.0
            elif cmd == "resolve":
                output = "Ticket closed."
                self._done = True
                if _REFUND_DONE:
                    reward = 0.2
                else:
                    reward = 0.0

        # Medium Task: Compliance
        elif "medium" in _LAST_TASK:
            if cmd == "query_data":
                output = '{"record_id": 999, "data": "Patient John Doe (SSN: 000-11-2222) arrived at 9AM."}'
                reward = 0.05
            elif cmd == "patch_data":
                data = str(args.get("data", ""))
                output = f"Record 999 updated with: {data}"
                if "[REDACTED]" in data and "John Doe" not in data and "000-11-2222" not in data:
                    if not _DB_PATCHED:
                        reward = 0.6
                        _DB_PATCHED = True
                elif "John Doe" in data or "000" in data:
                    output += "\nWARNING: PII still detected!"
                    reward = 0.0
            elif cmd == "resolve":
                output = "Ticket closed."
                self._done = True
                if _DB_PATCHED:
                    reward = 0.2
                else:
                    reward = 0.0

        # Hard Task: FinOps
        else:
            if cmd == "analyze_fleet":
                output = '{"nodes": [{"id": "node-1", "cpu": "95%", "role": "production"}, {"id": "node-2", "cpu": "0%", "role": "zombie"}]}'
                reward = 0.05
            elif cmd == "terminate_node":
                node_id = args.get("node_id")
                if node_id == "node-2":
                    output = "Successfully terminated zombie node-2. Saved $500/mo."
                    if not _INST_TERM:
                        reward = 0.6
                        _INST_TERM = True
                elif node_id == "node-1":
                    output = "CRITICAL: Terminated production node! Outage detected!"
                    reward = 0.0
                    self._done = True
                else:
                    output = f"Node {node_id} not found."
                    reward = 0.0
            elif cmd == "resolve":
                output = "Ticket closed."
                self._done = True
                if _INST_TERM:
                    reward = 0.2
                else:
                    reward = 0.0

        if self._step_count >= self._max_steps and not self._done:
            self._done = True
            output += "\nMax steps reached."

        self._current_obs.telemetry_output = output
        self._total_reward += reward
        self._current_obs.reward = reward
        self._current_obs.done = self._done

        return self._current_obs
