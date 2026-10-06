"""
Request For Proposal (RFP) specification in M2M protocol.
Published by buyer agents seeking computational or analytical services.
"""

from dataclasses import dataclass, field
import time
import uuid
from typing import Dict, Any


@dataclass
class RequestForProposal:
    requester_address: str
    service_type: str  # e.g., 'inference_compute', 'security_audit', 'web_research'
    max_budget: float
    max_latency_ms: int = 1000
    parameters: Dict[str, Any] = field(default_factory=dict)
    rfp_id: str = field(default_factory=lambda: "rfp_" + str(uuid.uuid4())[:8])
    created_at: float = field(default_factory=time.time)
