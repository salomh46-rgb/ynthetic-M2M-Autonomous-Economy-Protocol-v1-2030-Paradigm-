"""
Unit tests for zero-trust conditional escrow settlements.
"""

from m2m_engine.crypto_ledger.wallet import AgentWallet
from m2m_engine.crypto_ledger.ledger import ImmutableLedger
from m2m_engine.crypto_ledger.escrow import ZeroTrustEscrow


def test_escrow_lock_and_release():
    ledger = ImmutableLedger()
    escrow = ZeroTrustEscrow(ledger)

    buyer = AgentWallet()
    seller = AgentWallet()

    ledger.mint_grant(buyer.address, 100.0)

    # 1. Lock 30 tokens in escrow
    agreement = escrow.lock_funds(
        agreement_id="agr_001",
        buyer_wallet=buyer,
        seller_address=seller.address,
        amount=30.0,
        task_description="Train sub-agent model",
    )
    assert agreement.status == "LOCKED"
    assert ledger.get_balance(buyer.address) == 69.99  # 30 + 0.01 fee
    assert ledger.get_balance(seller.address) == 0.0

    # 2. Seller completes task and submits proof
    escrow.submit_proof_and_release("agr_001", "proof_sha256:abcdef123456")

    assert agreement.status == "RELEASED"
    assert ledger.get_balance(seller.address) == 30.0
    assert ledger.get_balance(escrow.escrow_vault_address) == 0.0
