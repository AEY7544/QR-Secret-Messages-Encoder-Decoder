import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode('utf-8')).digest()


def encrypt_message(message: str, password: str) -> bytes:
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    payload = cipher.nonce + tag + ciphertext
    encoded_payload = base64.b64encode(payload)
    return encoded_payload


def decrypt_message(encoded_payload: bytes, password: str) -> str:
    try:
        payload = base64.b64decode(encoded_payload)
        nonce = payload[:16]
        tag = payload[16:32]
        ciphertext = payload[32:]
        key = derive_key(password)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')
    except (ValueError, KeyError, IndexError) as e:
        raise ValueError("Decryption failed. Wrong password or corrupted data.") from e
