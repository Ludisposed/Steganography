from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

'''
   Encryption methods as by Cryptography.fernet module
'''
def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())


def encrypt_text(password, token):
    f = Fernet(get_key(password))
    return f.encrypt(bytes(token))


def decrypt_text(password, token):
    f = Fernet(get_key(password))
    return f.decrypt(bytes(token))


'''
    Ecryption as by Cryptography.RSA module
'''
# RSA -- TODO
