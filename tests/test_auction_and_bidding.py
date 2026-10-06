"""
Unit tests for autonomous auction and competitive bidding mechanics.
"""

from m2m_engine.protocol.rfp import RequestForProposal
from m2m_engine.protocol.bid import ServiceBid
from m2m_engine.protocol.negotiation import AutonomousAuction


def test_auction_selects_highest_utility_provider():
    rfp = RequestForProposal(
        requester_address="synth_buyer",
        service_type="inference_compute",
        max_budget=20.0,
        max_latency_ms=200,
    )

    # 3 competing providers
    bid_expensive = ServiceBid(rfp.rfp_id, "synth_node_1", "Node1", price=19.0, promised_latency_ms=100, reputation_score=1.5)
    bid_optimal = ServiceBid(rfp.rfp_id, "synth_node_2", "Node2", price=10.0, promised_latency_ms=120, reputation_score=2.0)
    bid_slow = ServiceBid(rfp.rfp_id, "synth_node_3", "Node3", price=8.0, promised_latency_ms=800, reputation_score=1.0)

    winner_tuple = AutonomousAuction.select_winner(rfp, [bid_expensive, bid_optimal, bid_slow])
    assert winner_tuple is not None
    winner_bid, utility = winner_tuple

    # Node2 has high reputation and reasonable price
    assert winner_bid.bidder_name == "Node2"
