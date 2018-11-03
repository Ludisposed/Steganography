import os
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding


class EncryptError(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return "Error during encrypt/decrypt: {}".format(self.error_msg)

'''
    Ecryption as by Cryptography.RSA module
'''
def generate_rsa_keys(private_key_filepath, public_key_filepath):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_key_filepath, 'wb+') as private_pem_out:
        private_pem_out.write(private_key_pem)

    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_key_filepath, 'wb+') as public_pem_out:
        public_pem_out.write(public_key_pem)


def load_private_key(filepath):
    if not os.path.exists(filepath):
        raise EncryptError("file {} not exist".format(filepath))
    with open(filepath, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = serialization.load_pem_private_key(pemlines, None, default_backend())
    return private_key

def load_public_key(filepath):
    if not os.path.exists(filepath):
        raise EncryptError("file {} not exist".format(filepath))
    with open(filepath, 'rb') as pem_in:
        pemlines = pem_in.read()
    public_key = serialization.load_pem_public_key(pemlines, default_backend())
    return public_key
   
def encrypt_rsa(plaintext, public_key_filepath):
    if not isinstance(plaintext, bytes):
        plaintext = plaintext.encode("utf-8")
    if not os.path.exists(public_key_filepath):
        raise EncryptError("file {} not exist".format(public_key_filepath))
    public_key = load_public_key(public_key_filepath)
    cipher_data = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return base64.b64encode(cipher_data)


def decrypt_rsa(ciphertext, private_key_filepath):
    if not isinstance(ciphertext, bytes):
        ciphertext = ciphertext.encode("utf-8")
    unbased_data = base64.b64decode(ciphertext)
    if not os.path.exists(private_key_filepath):
        raise EncryptError("file {} not exist".format(private_key_filepath))
    private_key = load_private_key(private_key_filepath)
    return private_key.decrypt(
        unbased_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )


'''
   Encryption methods as by Cryptography.fernet module
'''
def get_key(password):
    if not isinstance(password, bytes):
        password = password.encode("utf-8")
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt_fernet(password, plaintext):
    if not isinstance(plaintext, bytes):
        plaintext = plaintext.encode("utf-8")
    f = Fernet(get_key(password))
    return f.encrypt(plaintext)

def decrypt_fernet(password, ciphertext):
    if not isinstance(ciphertext, bytes):
        ciphertext = ciphertext.encode("utf-8")
    f = Fernet(get_key(password))
    return f.decrypt(ciphertext)



    

