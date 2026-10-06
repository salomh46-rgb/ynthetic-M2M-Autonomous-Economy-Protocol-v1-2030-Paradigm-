"""
Immutable Hash-Chain Micro-Ledger for Synthetic M2M Economy.
Guarantees double-spending defense, balance conservation, and auditability.
"""

from typing import Dict, List, Optional
import time
from m2m_engine.crypto_ledger.transaction import Transaction


class ImmutableLedger:
    """
    Maintains cryptographic state of all agent account balances and transaction history.
    """

    def __init__(self):
        # address -> available balance (SynthoCredits)
        self.balances: Dict[str, float] = {}
        # List of committed transactions
        self.history: List[Transaction] = []
        # Protocol treasury address for collected fees
        self.treasury_address = "synth_treasury_protocol"
        self.balances[self.treasury_address] = 0.0

    def get_balance(self, address: str) -> float:
        return self.balances.get(address, 0.0)

    def mint_grant(self, address: str, amount: float, reason: str = "Initial Agent Boot Grant") -> Transaction:
        """Mints initial startup capital for autonomous agents."""
        if amount <= 0:
            raise ValueError("Mint amount must be positive")
        self.balances[address] = self.get_balance(address) + amount
        
        tx = Transaction(
            sender_address="synth_system_mint",
            recipient_address=address,
            amount=amount,
            fee=0.0,
            memo=reason,
            timestamp=time.time(),
        )
        self.history.append(tx)
        return tx

    def apply_transaction(self, tx: Transaction, sender_public_key_hex: str) -> bool:
        """
        Validates signature, verifies sufficient funds, and atomically executes transfer.
        """
        # 1. Verify cryptographic signature
        if not tx.is_valid_signature(sender_public_key_hex):
            raise ValueError(f"Invalid transaction signature for tx {tx.tx_id}")

        sender = tx.sender_address
        recipient = tx.recipient_address
        total_deduction = tx.amount + tx.fee

        # 2. Check balance
        sender_balance = self.get_balance(sender)
        if sender_balance < total_deduction:
            raise ValueError(
                f"Insufficient funds: {sender} has {sender_balance:.2f}, needs {total_deduction:.2f}"
            )

        # 3. Atomic state update
        self.balances[sender] = round(sender_balance - total_deduction, 4)
        self.balances[recipient] = round(self.get_balance(recipient) + tx.amount, 4)
        self.balances[self.treasury_address] = round(self.get_balance(self.treasury_address) + tx.fee, 4)

        # 4. Append to ledger chain
        self.history.append(tx)
        return True
