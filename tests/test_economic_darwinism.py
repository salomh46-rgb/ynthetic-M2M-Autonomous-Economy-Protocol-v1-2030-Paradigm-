"""
Tests for Economic Darwinism: Solvent agents flourish, insolvent agents exit.
"""

from m2m_engine.marketplace.exchange import M2MExchange
from m2m_engine.agents.compute_provider_agent import ComputeProviderAgent
from m2m_engine.agents.research_buyer_agent import ResearchBuyerAgent


def test_market_lifecycle_and_agent_survival():
    exchange = M2MExchange()

    # 1. Register agents
    buyer = ResearchBuyerAgent("AlphaBuyer", exchange.ledger, exchange.escrow, initial_balance=100.0)
    provider_efficient = ComputeProviderAgent("FastGPU_Node", exchange.ledger, initial_balance=20.0, base_unit_price=8.0, latency_ms=80)
    provider_expensive = ComputeProviderAgent("Overpriced_Node", exchange.ledger, initial_balance=20.0, base_unit_price=25.0, latency_ms=300)
    provider_broke = ComputeProviderAgent("Bankrupt_Node", exchange.ledger, initial_balance=0.0)

    exchange.register_agent(buyer)
    exchange.register_agent(provider_efficient)
    exchange.register_agent(provider_expensive)
    exchange.register_agent(provider_broke)

    # Insolvent agent cannot bid
    assert provider_broke.is_solvent is False

    # 2. Buyer issues RFP for 15 credits
    rfp = buyer.issue_rfp(service_type="inference_compute", max_budget=15.0)
    bids = exchange.broadcast_rfp(rfp)

    # Only provider_efficient bids; expensive refuses/exceeds budget, broke is disqualified
    assert len(bids) == 1
    assert bids[0].bidder_name == "FastGPU_Node"

    # 3. Contract & Escrow
    winner_bid = bids[0]
    agreement = buyer.contract_and_lock_escrow("agr_darwin_01", winner_bid, "Run 100k inference steps")
    assert agreement.status == "LOCKED"

    # 4. Provider executes and produces proof
    proof = provider_efficient.execute_task("Run 100k inference steps")
    buyer.verify_and_settle("agr_darwin_01", proof)
    provider_efficient.record_job_success(winner_bid.price)

    # 5. Financial verification
    assert provider_efficient.balance > 25.0  # Earned profit!
    assert provider_efficient.reputation > 1.0  # Reputation increased!
    assert exchange.ledger.get_balance(exchange.ledger.treasury_address) > 0.0  # Protocol earned fee
