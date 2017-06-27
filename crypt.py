import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt(password, token):
    f = Fernet(get_key(password))
    return f.encrypt(bytes(token))

def decrypt(password, token):
    f = Fernet(get_key(password))
    return f.decrypt(bytes(token))

key = Fernet.generate_key()
m = raw_input("Magic: ")
t = raw_input("Text: ")

k = encrypt(m, t)
print 'encrypt :' + k
k = decrypt(m, k)
print 'decrypt :' + k
