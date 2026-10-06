"""
Service Bid model submitted by provider agents in response to RFPs.
"""

from dataclasses import dataclass, field
import time
import uuid


@dataclass
class ServiceBid:
    rfp_id: str
    bidder_address: str
    bidder_name: str
    price: float
    promised_latency_ms: int
    reputation_score: float = 1.0  # [0.1 .. 5.0] historical quality rating
    bid_id: str = field(default_factory=lambda: "bid_" + str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)
