import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

password = b"reportmanagement.online"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

def encrypt_message(body: dict) -> str:
    message = json.dumps(body).encode()
    encrypted_message = f.encrypt(message)
    return encrypted_message.decode()

def decrypt_message(token: str) -> dict:
    decrypted_message = f.decrypt(token.encode())
    return json.loads(decrypted_message.decode())
