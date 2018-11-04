# Steganography
Steganography is the art of hiding messages in (images, videos or even audio)

# Prerequisites
It uses the `PIL`, `numpy` and `cryptography` modules

run `pip install -r requirements-stego.txt` to download all the libraries

# How to use
run `python stego.py --help`

# Install from pip

`pip install stegoprng`

## Example

```python
from stegoprng import stego

encrypt_image_path = "test.png" #hide information to this image
decrypt_image_path = "new_test.png" #image generated after hide information
test_file_path = "test.txt" #information need to be hide
password = "password" #password to encrypt/decrypt informaton
magic = "magic" #hide/retrieve with prng_magic
public_key_path = "public.pem" #rsa public key
private_key_path = "private.pem" #rsa private key

#aes encrypt information
stego.encrypt(encrypt_image_path, test_file_path, password, magic, None)
secret = stego.decrypt(decrypt_image_path, password, magic, None)

#rsa encrypt information
stego.encrypt(encrypt_image_path, test_file_path, None, None, public_key_path)
secret = stego.decrypt(decrypt_image_path, None, None, private_key_path)
```



# Todo
- [ ] Code Refractor
- [ ] Write better tests
- [ ] Rework RSA
- [ ] Other formats Video/Audio
- [ ] Finish Packaging
