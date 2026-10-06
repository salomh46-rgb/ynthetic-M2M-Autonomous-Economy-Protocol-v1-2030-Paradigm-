"""
Compute Provider Agent.
Autonomously sells GPU/CPU inference tokens on the decentralized M2M market.
Adjusts pricing dynamically based on capacity and market competition.
"""

import hashlib
import time
from typing import Optional
from m2m_engine.agents.base_agent import BaseEconomicAgent
from m2m_engine.crypto_ledger.ledger import ImmutableLedger
from m2m_engine.protocol.rfp import RequestForProposal
from m2m_engine.protocol.bid import ServiceBid


class ComputeProviderAgent(BaseEconomicAgent):
    """
    Sells machine computational cycles and inference bandwidth.
    """

    def __init__(
        self,
        name: str,
        ledger: ImmutableLedger,
        initial_balance: float = 50.0,
        base_unit_price: float = 10.0,
        latency_ms: int = 150,
    ):
        super().__init__(name, ledger, initial_balance)
        self.base_unit_price = base_unit_price
        self.latency_ms = latency_ms
        self.supported_services = {"inference_compute", "matrix_multiplication"}

    def evaluate_and_bid(self, rfp: RequestForProposal) -> Optional[ServiceBid]:
        """
        Evaluates incoming RFP. If solvent and service matches, constructs competitive bid.
        """
        if not self.is_solvent:
            return None  # Insolvent agents cannot bid

        if rfp.service_type not in self.supported_services:
            return None

        # Price matching: if client's budget is lower than base price, offer discount if profitable
        bid_price = min(self.base_unit_price, rfp.max_budget)
        if bid_price < self.base_unit_price * 0.70:
            return None  # Unprofitable, refuse to bid below operational cost

        return ServiceBid(
            rfp_id=rfp.rfp_id,
            bidder_address=self.address,
            bidder_name=self.name,
            price=round(bid_price, 2),
            promised_latency_ms=self.latency_ms,
            reputation_score=self.reputation,
        )

    def execute_task(self, task_description: str) -> str:
        """
        Executes computational workload and produces cryptographic Proof-of-Execution.
        """
        payload = f"COMPUTE_RESULT_{self.name}_{task_description}_{time.time()}"
        proof_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return f"proof_sha256:{proof_hash}"
