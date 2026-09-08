from backend.crypto.encryption import (
    decrypt_event,
    encode_key,
    encrypt_event,
    generate_key,
)


def test_encryption_round_trip():
    key = generate_key()

    event = {
        "event_type": "key_event",
        "session_id": "lab-001",
        "key_category": "ALPHANUMERIC",
        "action": "DOWN",
        "dwell_ms": 84,
    }

    encrypted = encrypt_event(event, key)

    assert encrypted["algorithm"] == "AES-256-GCM"
    assert encrypted["ciphertext"] != str(event)

    decrypted = decrypt_event(encrypted, key)

    assert decrypted == event


def test_key_encoding_round_trip():
    key = generate_key()

    encoded = encode_key(key)

    from backend.crypto.encryption import decode_key

    assert decode_key(encoded) == key