from pydantic import Field
from typing import Dict, Any, Optional
from openenv.core.env_server.types import Action, Observation

class AIOpsAction(Action):
    command: str = Field(
        ..., 
        description="The AIOps tool to execute (e.g., 'query_billing', 'refund', 'query_data', 'patch_data', 'analyze_fleet', 'terminate_node', 'resolve')"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Key-value parameters corresponding to the command"
    )

class AIOpsObservation(Observation):
    incident_id: Optional[str] = Field(None, description="Current priority incident ID")
    incident_severity: Optional[str] = Field(None, description="P1, P2, P3")
    incident_description: str = Field("", description="Details of the alert or ticket")
    telemetry_output: str = Field("", description="JSON output of the last command executed")
    system_health_score: float = Field(100.0, description="Overall health metric (100 is best)")
    budget_remaining: float = Field(10000.0, description="Available budget. Goes down based on cloud waste.")
