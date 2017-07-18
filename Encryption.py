from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
import base64

'''
RSA protocol
'''
def gen_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    return private_key


def save_key(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key

   
def encrypt_rsa(text, key):
    private_key = load_key(key)
    public_key = private_key.public_key()
    return public_key.encrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )


def decrypt_rsa(text, key):
    private_key = load_key(key)
    return private_key.decrypt(
        text,
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
if __name__ == "__main__":
    pk = gen_key()
    filename = 'privkey.pem'
    save_key(pk, filename)
    e_data = encrypt_rsa("rsa_text", filename)
    print "encrypt_rsa data: " + e_data
    d_data = decrypt_rsa(e_data,filename)
    print "decrypt_rsa data: " + d_data
