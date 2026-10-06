"""
Autonomous Sovereign Wallet for AI Agents.
Utilizes Ed25519 asymmetric cryptography for cryptographic identity and transaction signing.
No human intervention required.
"""

import hashlib
from typing import Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


class AgentWallet:
    """
    Sovereign cryptographic wallet owned and controlled exclusively by an AI Agent.
    """

    def __init__(self, private_key: Optional[ed25519.Ed25519PrivateKey] = None):
        self._private_key = private_key or ed25519.Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()
        
        # Public key bytes
        pub_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        # Address format: synth_<first 16 hex chars of sha256(pub_key)>
        self.address = "synth_" + hashlib.sha256(pub_bytes).hexdigest()[:20]

    @property
    def public_key_hex(self) -> str:
        return self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()

    def sign(self, message: bytes) -> bytes:
        """Signs a message or transaction payload using agent's private key."""
        return self._private_key.sign(message)

    @staticmethod
    def verify(public_key_hex: str, signature: bytes, message: bytes) -> bool:
        """Verifies an Ed25519 signature against the sender's public key."""
        try:
            pub_bytes = bytes.fromhex(public_key_hex)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            public_key.verify(signature, message)
            return True
        except Exception:
            return False
