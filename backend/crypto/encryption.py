import base64
import json
import os
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


KEY_SIZE = 32
NONCE_SIZE = 12


def generate_key() -> bytes:
    """Generate a 256-bit AES key."""
    return AESGCM.generate_key(bit_length=256)


def encode_key(key: bytes) -> str:
    """Convert a key to a safe text representation."""
    return base64.urlsafe_b64encode(key).decode("utf-8")


def decode_key(encoded_key: str) -> bytes:
    """Convert a text key back into bytes."""
    return base64.urlsafe_b64decode(encoded_key.encode("utf-8"))


def encrypt_event(
    event: dict[str, Any],
    key: bytes,
    associated_data: str = "SYLTHEN-LAB",
) -> dict[str, str]:
    """Encrypt a telemetry event using AES-256-GCM."""

    aes = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)

    plaintext = json.dumps(
        event,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    ciphertext = aes.encrypt(
        nonce,
        plaintext,
        associated_data.encode("utf-8"),
    )

    return {
        "algorithm": "AES-256-GCM",
        "nonce": base64.urlsafe_b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.urlsafe_b64encode(ciphertext).decode("utf-8"),
        "aad": associated_data,
    }


def decrypt_event(
    encrypted_event: dict[str, str],
    key: bytes,
) -> dict[str, Any]:
    """Decrypt and authenticate a SYLTHEN telemetry event."""

    aes = AESGCM(key)

    nonce = base64.urlsafe_b64decode(
        encrypted_event["nonce"].encode("utf-8")
    )

    ciphertext = base64.urlsafe_b64decode(
        encrypted_event["ciphertext"].encode("utf-8")
    )

    aad = encrypted_event["aad"].encode("utf-8")

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        aad,
    )

    return json.loads(plaintext.decode("utf-8"))