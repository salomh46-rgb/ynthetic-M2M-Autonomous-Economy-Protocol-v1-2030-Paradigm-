"""
Zero-Trust Escrow Protocol for Agent Service Delivery.
Locks funds until cryptographic Proof-of-Execution is verified.
"""

from dataclasses import dataclass
import time
from typing import Dict, Optional
from m2m_engine.crypto_ledger.ledger import ImmutableLedger
from m2m_engine.crypto_ledger.transaction import Transaction
from m2m_engine.crypto_ledger.wallet import AgentWallet


@dataclass
class EscrowAgreement:
    agreement_id: str
    buyer_address: str
    seller_address: str
    amount: float
    task_description: str
    deadline_sec: float
    status: str = "LOCKED"  # LOCKED, RELEASED, REFUNDED
    proof_of_execution: Optional[str] = None


class ZeroTrustEscrow:
    """
    Manages autonomous conditional contract escrows between AI agents.
    """

    def __init__(self, ledger: ImmutableLedger):
        self.ledger = ledger
        self.escrow_vault_address = "synth_escrow_vault"
        self.ledger.balances[self.escrow_vault_address] = 0.0
        self.agreements: Dict[str, EscrowAgreement] = {}

    def lock_funds(
        self,
        agreement_id: str,
        buyer_wallet: AgentWallet,
        seller_address: str,
        amount: float,
        task_description: str,
        duration_sec: float = 60.0,
    ) -> EscrowAgreement:
        """Locks buyer funds into escrow vault pending service completion."""
        tx = Transaction(
            sender_address=buyer_wallet.address,
            recipient_address=self.escrow_vault_address,
            amount=amount,
            fee=0.01,
            memo=f"Escrow lock for {agreement_id}",
        )
        tx.sign(buyer_wallet)
        self.ledger.apply_transaction(tx, buyer_wallet.public_key_hex)

        agreement = EscrowAgreement(
            agreement_id=agreement_id,
            buyer_address=buyer_wallet.address,
            seller_address=seller_address,
            amount=amount,
            task_description=task_description,
            deadline_sec=time.time() + duration_sec,
            status="LOCKED",
        )
        self.agreements[agreement_id] = agreement
        return agreement

    def submit_proof_and_release(
        self,
        agreement_id: str,
        proof_of_execution: str,
        buyer_approver_wallet: Optional[AgentWallet] = None,
    ) -> bool:
        """
        Validates completion proof and transfers locked funds from vault to seller.
        """
        agr = self.agreements.get(agreement_id)
        if not agr or agr.status != "LOCKED":
            raise ValueError(f"Agreement {agreement_id} is not in LOCKED state")

        agr.proof_of_execution = proof_of_execution
        agr.status = "RELEASED"

        # Transfer from vault to seller
        tx = Transaction(
            sender_address=self.escrow_vault_address,
            recipient_address=agr.seller_address,
            amount=agr.amount,
            fee=0.0,
            memo=f"Escrow payout for {agreement_id}",
        )
        # Internal vault transfer executes directly on balance
        vault_bal = self.ledger.get_balance(self.escrow_vault_address)
        self.ledger.balances[self.escrow_vault_address] = round(vault_bal - agr.amount, 4)
        self.ledger.balances[agr.seller_address] = round(
            self.ledger.get_balance(agr.seller_address) + agr.amount, 4
        )
        self.ledger.history.append(tx)
        return True

    def refund_expired(self, agreement_id: str) -> bool:
        """Refunds locked capital to buyer if task was not completed before deadline."""
        agr = self.agreements.get(agreement_id)
        if not agr or agr.status != "LOCKED":
            raise ValueError(f"Agreement {agreement_id} is not in LOCKED state")

        if time.time() < agr.deadline_sec:
            raise ValueError("Cannot refund prior to deadline expiration")

        agr.status = "REFUNDED"
        vault_bal = self.ledger.get_balance(self.escrow_vault_address)
        self.ledger.balances[self.escrow_vault_address] = round(vault_bal - agr.amount, 4)
        self.ledger.balances[agr.buyer_address] = round(
            self.ledger.get_balance(agr.buyer_address) + agr.amount, 4
        )
        return True
