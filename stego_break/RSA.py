from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Working RSA encryption you can run for yourself
MESSAGE = 'Ligula Venenatis Etiam Fermentum'

# Create private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Create public key
public_key = private_key.public_key()

# Encrypt
ciphertext = public_key.encrypt(
    MESSAGE,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)

# Encrypted text
print(ciphertext)

# Decrypt
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)

# Decrypted text
print plaintext

# Make human readable key
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
pem_data = pem.splitlines()
print pem_data


# How to Save//Load???
