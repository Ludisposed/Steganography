from helpers import encryption
from helpers import file_handler
from helpers import utility
from helpers import steganography 

import sys
import os

import numpy as np
from PIL import Image
import argparse

# Gets ascii representation from string to list of bits
text_ascii = lambda text: map(int, ''.join(map(lambda char: '{:08b}'.format(ord(char)), text)))

# Globals
ENDBIT = [0] * 8

def encrypt(filename, output_filename, text, password, magic, rsa):
    '''
    A method that hide text into image

    Args:
        filename (str) : The filename of the image
        text     (str) : Text or textfile to be hidden in the image
        password (str) : Password used to encrypt text
        magic    (str) : Magic Password used to use for pseudorandomness to hide text in the image
        rsa      (str) : RSA public key to encrypt the text

    Returns:
        A image named new + filename, which with encrypted text in it
    '''
    text = file_handler.TextHandler(text).text
    print '[*] Encrypting text'

    if not password is None:
        text = encryption.encrypt_text(password, text)

    if not rsa is None:
        text = encryption.check_rsa_key(text, rsa) + ENDBIT
    
    if rsa is None:
        text = text_ascii(text) + ENDBIT

    encrypt_file = {
        "image" : steganography.encrypt_image,
        "video" : steganography.encrypt_video,
        "audio" : steganography.encrypt_audio
    }
    file_type = utility.fileformat(filename)
    
    if file_type not in encrypt_file:
        print("[-] ERROR:Unknown file format")
        return
        
    encrypt_function = encrypt_file[file_type]
    encrypt_function(filename, output_filename, text, magic)
        
    

#TODO Specify outfilename
def decrypt(filename, output_filename, password, magic, rsa):
    '''
    A method that decrypt text from image

    Args:
	filename (str) : The filename of the image
  	password (str) : Used to decrypt text
        magic    (str) : Magic Password used to use for pseudorandomness to retrieve text in the image
        rsa      (str) : RSA private key to decrypt the text

    Returns:
	Text hided in image
    '''
    print '[*] Decrypting text'

    decrypt_file = {
        "image" : steganography.decrypt_image,
        "video" : steganography.decrypt_video,
        "audio" : steganography.decrypt_audio
    }
    file_type = utility.fileformat(filename)
    
    if file_type not in decrypt_file:
        print("[-] ERROR:Unknown file format")
        return
    decrypt_function = decrypt_file[file_type]
    text = decrypt_function(filename, magic)
    if not password is None:
        text = encryption.decrypt_text(password, text)
    if not rsa is None:
        text = encryption.decrypt_rsa(text, rsa)

    #print('[*] Retrieved text: \n%s' % text) 

    with open(output_filename, "wb+") as f:
        f.write('[*] Retrieved text: \n%s' % text)
    
def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <filename>',
                                     description='Steganography prng-Tool @Ludisposed & @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python prng_stego.py -e test.png -t howareyou
python prng_stego.py -e -r new test.png howareyou
python prng_stego.py -e -p password -m magic test.png -t howareyou
python prng_stego.py -e -p password -m magic test.png -t file_test.txt
python prng_stego.py --encrypt --password password --magic magic test.png -t "howareyou  some other text"

python prng_stego.py -d new_test.png
python prng_stego.py -d --rsa private.pem new_test.png
python prng_stego.py -d -p password -m magic new_test.png
python prng_stego.py --decrypt --password password --magic magic new_test.png

'''

                                        )
    parser.add_argument('-e','--encrypt', action="store_true", help='encrypt filename with text')
    parser.add_argument('-d','--decrypt', action="store_true", help='decrypt text from filename')
    parser.add_argument('-p','--password', type=str, help='encrypt/decrypt with password')
    parser.add_argument('-m','--magic', type=str, help='hide/retrieve with prng_magic')
    parser.add_argument('-r','--rsa', type=str, help='encrypt using RSA [filename of key]')
    parser.add_argument('filename', type=str, help='encrypt/decrypt message into this [image/audio/video]')
    parser.add_argument('-t','--text', type=str, help='[text/text_path] used to encrypt')
    parser.add_argument('-o','--output', type=str, help='specify outputfilename')
    args = parser.parse_args()

    if args.encrypt ^ args.decrypt == False:
        parser.error('Incorrect encrypt/decrypt mode')
    if args.encrypt and args.text is None:
        parser.error('Require text/text.path in encrypt mode')
    if not args.password is None and not args.rsa is None:
        parser.error('Specify Encryption/Decryption technique either RSA or Password')
    return args

if __name__ == "__main__":
    args = parse_options()
    if args.encrypt:
        encrypt(args.filename, args.output, args.text, args.password, args.magic, args.rsa)
    else:
        decrypt(args.filename, args.output, args.password, args.magic, args.rsa)
    
