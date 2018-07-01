import unittest
import stego
import os

_cwd = os.getcwd()
ENCRYPT_IMAGE = os.path.join(_cwd, 'tests/test.png')
DECRYPT_IMAGE = os.path.join(_cwd, 'tests/new_test.png')
TEST_FILE = os.path.join(_cwd, 'tests/file_test.txt')
PRIVATE_KEY = os.path.join(_cwd, 'tests/private_key.pem')
PUBLIC_KEY = os.path.join(_cwd, 'tests/public_key.pem')

class StegoTests(unittest.TestCase):
    def test_magic(self):
        print("Test magic password.")
        stego.encrypt(ENCRYPT_IMAGE, TEST_FILE, "password", "magic", None)
        print("")
        stego.decrypt(DECRYPT_IMAGE, "password", "magic", None)

    def test_rsa(self):
        print("\nTest RSA.")
        stego.encrypt(ENCRYPT_IMAGE, TEST_FILE, None, None, PUBLIC_KEY)
        print("")
        stego.decrypt(DECRYPT_IMAGE, None, None, PRIVATE_KEY)

if __name__ == "__main__":
    unittest.main()
