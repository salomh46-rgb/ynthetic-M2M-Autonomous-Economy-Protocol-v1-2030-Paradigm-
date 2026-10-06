"""
Research Buyer Agent.
Purchases distributed compute and analysis on behalf of high-level goals.
Conducts autonomous auctions, manages escrow funding, and evaluates results.
"""

from typing import List, Optional, Tuple
from m2m_engine.agents.base_agent import BaseEconomicAgent
from m2m_engine.crypto_ledger.ledger import ImmutableLedger
from m2m_engine.crypto_ledger.escrow import ZeroTrustEscrow, EscrowAgreement
from m2m_engine.protocol.rfp import RequestForProposal
from m2m_engine.protocol.bid import ServiceBid
from m2m_engine.protocol.negotiation import AutonomousAuction


class ResearchBuyerAgent(BaseEconomicAgent):
    """
    Autonomous purchasing agent procuring machine compute via smart contracts.
    """

    def __init__(self, name: str, ledger: ImmutableLedger, escrow: ZeroTrustEscrow, initial_balance: float = 200.0):
        super().__init__(name, ledger, initial_balance)
        self.escrow = escrow

    def issue_rfp(self, service_type: str, max_budget: float, max_latency_ms: int = 500) -> RequestForProposal:
        """Publishes an autonomous Request For Proposal to the agent marketplace."""
        if self.balance < max_budget:
            raise ValueError(f"Insufficient funds ({self.balance:.2f}) to post RFP for {max_budget:.2f}")

        return RequestForProposal(
            requester_address=self.address,
            service_type=service_type,
            max_budget=max_budget,
            max_latency_ms=max_latency_ms,
        )

    def evaluate_auction(
        self,
        rfp: RequestForProposal,
        bids: List[ServiceBid],
    ) -> Optional[Tuple[ServiceBid, float]]:
        """Selects winning provider using auction utility engine."""
        return AutonomousAuction.select_winner(rfp, bids)

    def contract_and_lock_escrow(
        self,
        agreement_id: str,
        winning_bid: ServiceBid,
        task_desc: str,
    ) -> EscrowAgreement:
        """Locks agreed payment into zero-trust escrow vault."""
        agreement = self.escrow.lock_funds(
            agreement_id=agreement_id,
            buyer_wallet=self.wallet,
            seller_address=winning_bid.bidder_address,
            amount=winning_bid.price,
            task_description=task_desc,
        )
        self.total_spent += winning_bid.price
        return agreement

    def verify_and_settle(self, agreement_id: str, proof_of_execution: str) -> bool:
        """Validates execution and authorizes release of escrow funds to provider."""
        if not proof_of_execution.startswith("proof_"):
            raise ValueError("Invalid proof format")
        return self.escrow.submit_proof_and_release(agreement_id, proof_of_execution)
