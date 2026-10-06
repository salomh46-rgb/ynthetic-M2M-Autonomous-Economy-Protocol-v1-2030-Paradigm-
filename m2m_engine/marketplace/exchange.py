"""
M2M Decentralized Exchange & Market Clearinghouse.
Facilitates autonomous discovery, RFP broadcasting, and transactional volume tracking.
"""

from typing import Dict, List, Optional
from m2m_engine.agents.base_agent import BaseEconomicAgent
from m2m_engine.agents.compute_provider_agent import ComputeProviderAgent
from m2m_engine.crypto_ledger.ledger import ImmutableLedger
from m2m_engine.crypto_ledger.escrow import ZeroTrustEscrow
from m2m_engine.protocol.rfp import RequestForProposal
from m2m_engine.protocol.bid import ServiceBid


class M2MExchange:
    """
    Decentralized clearinghouse and order matching engine for AI agents.
    """

    def __init__(self):
        self.ledger = ImmutableLedger()
        self.escrow = ZeroTrustEscrow(self.ledger)
        self.registered_agents: Dict[str, BaseEconomicAgent] = {}
        self.total_volume = 0.0

    def register_agent(self, agent: BaseEconomicAgent) -> None:
        self.registered_agents[agent.address] = agent

    def broadcast_rfp(self, rfp: RequestForProposal) -> List[ServiceBid]:
        """
        Broadcasts buyer's RFP to all active provider agents on the network.
        Collects competing bids.
        """
        bids: List[ServiceBid] = []
        for agent in self.registered_agents.values():
            if isinstance(agent, ComputeProviderAgent) and agent.is_solvent:
                bid = agent.evaluate_and_bid(rfp)
                if bid:
                    bids.append(bid)
        return bids

    def get_market_statistics(self) -> dict:
        total_agent_capital = sum(a.balance for a in self.registered_agents.values())
        treasury_balance = self.ledger.get_balance(self.ledger.treasury_address)
        return {
            "registered_agents_count": len(self.registered_agents),
            "total_transactions_count": len(self.ledger.history),
            "treasury_collected_fees": treasury_balance,
            "circulating_capital": round(total_agent_capital, 2),
        }
