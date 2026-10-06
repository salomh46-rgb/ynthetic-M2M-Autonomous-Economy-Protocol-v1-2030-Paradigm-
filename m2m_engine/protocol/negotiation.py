"""
Autonomous Auction and Price Negotiation Engine.
Selects the winning bid using utility-maximizing objective function.
"""

from typing import List, Optional, Tuple
from m2m_engine.protocol.rfp import RequestForProposal
from m2m_engine.protocol.bid import ServiceBid


class AutonomousAuction:
    """
    Evaluates competing provider bids for an RFP and determines the optimal winner.
    """

    @staticmethod
    def calculate_utility(bid: ServiceBid, rfp: RequestForProposal) -> float:
        """
        Utility scoring formula:
        Utility = (Reputation * 10) / (Price / MaxBudget) - (Latency / MaxLatency * 5)
        """
        if bid.price <= 0 or bid.price > rfp.max_budget:
            return -1.0  # Disqualified: exceeds budget or invalid price

        price_ratio = bid.price / max(0.01, rfp.max_budget)
        latency_ratio = bid.promised_latency_ms / max(1, rfp.max_latency_ms)

        # High reputation & low price maximizes utility; high latency penalizes
        utility = ((bid.reputation_score * 8.0) / (price_ratio + 0.2)) - (latency_ratio * 3.0)
        return round(utility, 3)

    @classmethod
    def select_winner(cls, rfp: RequestForProposal, bids: List[ServiceBid]) -> Optional[Tuple[ServiceBid, float]]:
        """
        Selects the winning bid with the highest positive utility score.
        """
        scored_bids = []
        for b in bids:
            if b.rfp_id != rfp.rfp_id:
                continue
            u = cls.calculate_utility(b, rfp)
            if u > 0:
                scored_bids.append((b, u))

        if not scored_bids:
            return None

        # Sort descending by utility
        scored_bids.sort(key=lambda item: item[1], reverse=True)
        return scored_bids[0]
