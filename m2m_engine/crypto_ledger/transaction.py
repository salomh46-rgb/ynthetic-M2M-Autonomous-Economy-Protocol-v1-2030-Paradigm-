"""
Micro-transaction data structure for Machine-to-Machine settlements.
Supports cryptographic verification and fee accounting.
"""

from dataclasses import dataclass
import hashlib
import json
import time
from typing import Optional
from m2m_engine.crypto_ledger.wallet import AgentWallet


@dataclass
class Transaction:
    sender_address: str
    recipient_address: str
    amount: float
    fee: float = 0.01  # Network protocol maintenance fee
    memo: str = ""
    timestamp: float = 0.0
    signature_hex: Optional[str] = None
    tx_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if not self.tx_id:
            self.tx_id = self.compute_hash()

    def get_signable_bytes(self) -> bytes:
        payload = {
            "sender": self.sender_address,
            "recipient": self.recipient_address,
            "amount": self.amount,
            "fee": self.fee,
            "memo": self.memo,
            "timestamp": self.timestamp,
        }
        return json.dumps(payload, sort_keys=True).encode("utf-8")

    def compute_hash(self) -> str:
        return hashlib.sha256(self.get_signable_bytes()).hexdigest()

    def sign(self, wallet: AgentWallet) -> None:
        if wallet.address != self.sender_address:
            raise ValueError("Wallet address does not match transaction sender")
        sig = wallet.sign(self.get_signable_bytes())
        self.signature_hex = sig.hex()

    def is_valid_signature(self, sender_public_key_hex: str) -> bool:
        if not self.signature_hex:
            return False
        sig_bytes = bytes.fromhex(self.signature_hex)
        return AgentWallet.verify(sender_public_key_hex, sig_bytes, self.get_signable_bytes())
