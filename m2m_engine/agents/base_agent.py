"""
Base Economic Agent class.
Every agent is a financially autonomous entity with its own cryptographic identity,
operating budget, and economic survival imperative.
"""

from typing import Optional
from m2m_engine.crypto_ledger.wallet import AgentWallet
from m2m_engine.crypto_ledger.ledger import ImmutableLedger


class BaseEconomicAgent:
    """
    Autonomous Economic Agent with cryptographic sovereignty and budget constraints.
    """

    def __init__(self, name: str, ledger: ImmutableLedger, initial_balance: float = 100.0):
        self.name = name
        self.ledger = ledger
        self.wallet = AgentWallet()
        self.reputation: float = 1.0
        self.total_earned: float = 0.0
        self.total_spent: float = 0.0
        self.completed_jobs: int = 0
        self.failed_jobs: int = 0

        # Boot capital grant
        if initial_balance > 0:
            self.ledger.mint_grant(self.wallet.address, initial_balance, f"Boot capital for {name}")

    @property
    def address(self) -> str:
        return self.wallet.address

    @property
    def balance(self) -> float:
        return self.ledger.get_balance(self.address)

    @property
    def is_solvent(self) -> bool:
        """Agent must maintain positive balance to pay for hosting and operations."""
        return self.balance > 0.05

    def record_job_success(self, payout: float) -> None:
        self.completed_jobs += 1
        self.total_earned += payout
        # Boost reputation asymptotically up to 5.0
        self.reputation = min(5.0, round(self.reputation + 0.15, 2))

    def record_job_failure(self) -> None:
        self.failed_jobs += 1
        # Severe penalty for task breach
        self.reputation = max(0.2, round(self.reputation - 0.50, 2))
