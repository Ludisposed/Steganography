from PIL import Image
import numpy as np
import sys
import os
import getopt
import base64
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

if __name__ == "__main__":
    '''
    What would we wanna do here?
    
    1. Try decryption from wordlist, imo this is the easiest one
    and possibly has the greatest effect only can be countered by using a RSA

    2. Look at difference in images try to derive the seed from that,
    and with seed recreate the password

    3. ???? Any more suggestions?
    '''

    print '[*] This is still a work in progress'
