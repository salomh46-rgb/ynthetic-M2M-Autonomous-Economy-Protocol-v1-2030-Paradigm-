"""
Unit tests for cryptographic wallet, transaction signatures, and ledger invariants.
"""

import pytest
from m2m_engine.crypto_ledger.wallet import AgentWallet
from m2m_engine.crypto_ledger.transaction import Transaction
from m2m_engine.crypto_ledger.ledger import ImmutableLedger


def test_wallet_signature_verification():
    wallet = AgentWallet()
    message = b"Synthetic M2M settlement payload"

    signature = wallet.sign(message)
    assert AgentWallet.verify(wallet.public_key_hex, signature, message) is True

    # Tampered message must fail
    assert AgentWallet.verify(wallet.public_key_hex, signature, b"Tampered data") is False


def test_ledger_atomic_transfer():
    ledger = ImmutableLedger()
    alice_wallet = AgentWallet()
    bob_wallet = AgentWallet()

    ledger.mint_grant(alice_wallet.address, 100.0)

    tx = Transaction(
        sender_address=alice_wallet.address,
        recipient_address=bob_wallet.address,
        amount=40.0,
        fee=0.01,
        memo="Service payment",
    )
    tx.sign(alice_wallet)

    success = ledger.apply_transaction(tx, alice_wallet.public_key_hex)
    assert success is True

    assert ledger.get_balance(alice_wallet.address) == 59.99
    assert ledger.get_balance(bob_wallet.address) == 40.0
    assert ledger.get_balance(ledger.treasury_address) == 0.01


def test_ledger_insufficient_funds_rejection():
    ledger = ImmutableLedger()
    wallet = AgentWallet()
    ledger.mint_grant(wallet.address, 10.0)

    tx = Transaction(
        sender_address=wallet.address,
        recipient_address="synth_other",
        amount=50.0,
    )
    tx.sign(wallet)

    with pytest.raises(ValueError, match="Insufficient funds"):
        ledger.apply_transaction(tx, wallet.public_key_hex)
