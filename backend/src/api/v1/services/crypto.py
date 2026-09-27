# stego/crypto.py
import base64
import hashlib
from cryptography.fernet import Fernet

def _derive_key(password: str, salt: bytes = b'fernet-salt-v1') -> bytes:
    """Деривация ключа Fernet из пароля."""
    digest = hashlib.sha256(salt + password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt(text: str, password: str) -> bytes:
    return Fernet(_derive_key(password)).encrypt(text.encode('utf-8'))

def decrypt(ciphertext: bytes, password: str) -> str:
    return Fernet(_derive_key(password)).decrypt(ciphertext).decode('utf-8')