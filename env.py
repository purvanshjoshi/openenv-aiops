from typing import Tuple, Dict, Any, Optional
from models import AIOpsAction, AIOpsObservation
from openenv.core.env_server.interfaces import Environment

class AIOpsEnv(Environment):
    def __init__(self):
        self._current_obs = AIOpsObservation()
        self._task_name = "easy"
        self._step_count = 0
        self._max_steps = 10
        self._done = False
        
        # State tracking for graders
        self._db_patched = False
        self._instance_terminated = False
        self._refund_issued = False
        self._total_reward = 0.0

    def reset(self, task_name: str = "easy", **kwargs) -> AIOpsObservation:
        self._task_name = task_name.lower()
        self._step_count = 0
        self._done = False
        self._db_patched = False
        self._instance_terminated = False
        self._refund_issued = False
        self._total_reward = 0.05
        
        self._current_obs = AIOpsObservation(
            system_health_score=100.0,
            budget_remaining=10000.0,
            telemetry_output="Environment Initialized. Waiting for first tool execution.",
            reward=0.05
        )

        if "easy" in self._task_name:
            self._current_obs.incident_id = "INC-101"
            self._current_obs.incident_severity = "P3"
            self._current_obs.incident_description = "Customer Ticket: 'I was billed twice for my plan this month. Please refund the duplicate $50 immediately.'"
        elif "medium" in self._task_name:
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

        # Easy Task: Billing
        if "easy" in self._task_name:
            if cmd == "query_billing":
                output = '{"customer_id": "CUST-001", "transactions": [{"id": 1, "amt": 50}, {"id": 2, "amt": 50}], "status": "duplicate_detected"}'
                reward = 0.05
            elif cmd == "refund":
                if args.get("amount") == 50 or args.get("amount") == 50.0:
                    output = '{"status": "success", "msg": "$50 refunded."}'
                    if not self._refund_issued:
                        reward = 0.6
                        self._refund_issued = True
                else:
                    output = '{"status": "error", "msg": "Incorrect refund amount."}'
                    reward = 0.0
            elif cmd == "resolve":
                output = "Ticket closed."
                self._done = True
                if self._refund_issued:
                    reward = 0.2
                else:
                    reward = 0.0

        # Medium Task: Compliance
        elif "medium" in self._task_name:
            if cmd == "query_data":
                output = '{"record_id": 999, "data": "Patient John Doe (SSN: 000-11-2222) arrived at 9AM."}'
                reward = 0.05
            elif cmd == "patch_data":
                data = str(args.get("data", ""))
                output = f"Record 999 updated with: {data}"
                if "[REDACTED]" in data and "John Doe" not in data and "000-11-2222" not in data:
                    if not self._db_patched:
                        reward = 0.6
                        self._db_patched = True
                elif "John Doe" in data or "000" in data:
                    output += "\nWARNING: PII still detected!"
                    reward = 0.0
            elif cmd == "resolve":
                output = "Ticket closed."
                self._done = True
                if self._db_patched:
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
                    if not self._instance_terminated:
                        reward = 0.6
                        self._instance_terminated = True
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
                if self._instance_terminated:
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
