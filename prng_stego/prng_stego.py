from PIL import Image
import numpy as np
import sys
import os
import getopt
import Steganography
import Encryption
import argparse
from classes import ImageHandler
from classes import TextHandler


# Gets ascii representation from string to list of bits
text_ascii = lambda text: map(int, ''.join(map(lambda char: '{:08b}'.format(ord(char)), text)))

# Globals
ENDBIT = [0] * 8


'''
    Filehandling I/O stuff
'''

def check_space(text,data):
    if data.size < len(text):
        print '[*] Image not big enough'
        sys.exit(0)



def check_rsa_key(text, filename):
    succes = False
    while not succes:
        e_data = Encryption.encrypt_rsa(text, filename)
        new = ''.join(map(lambda char: '{:08b}'.format(ord(char)), e_data))
        succes = True
        for i in range(0, len(new), 8):
            if new[i:i+8] == '00000000':
                succes = False
    return map(int, new) + ENDBIT


'''
    Main methods and usage
'''
def encrypt(filename, text, password, magic, rsa):
    '''
    A method that hide text into image

    Args:
        filename (str) : The filename of the image
        text     (str) : Text or text file need to be hide in image
        password (str) : Used to encrypt text
        magic    (str) : Used to hide text in image

    Returns:
        A image named new + filename, which with encrypted text in it
    '''
    # Check for file!
    text = TextHandler(text).text

    # Optional encrypt
    if not password is None:
        print '[*] Encrypting text'
        text = Encryption.encrypt_text(password, text)

    if not rsa is None:
        print '[*] Encrypting text'
        if rsa == 'new':
            new_key = Encryption.gen_key()
            Encryption.save_key(new_key, 'private_key.pem')

            text = check_rsa_key(text, 'private_key.pem')
            # text = Encryption.encrypt_rsa(text, 'private_key.pem')                    
        else:
            text = check_rsa_key(text, rsa)
            # text = Encryption.encrypt_rsa(text, rsa)

    if rsa is None:        
        text = text_ascii(text) + ENDBIT    

    try:
        image = ImageHandler(filename)
       
        # Load Image
        d_old = image.load_image()
        
        # Check if image can contain the data
        check_space(text,d_old)
       
        # get new data and save to image
        d_new = Steganography.hide_lsb(d_old, magic, text)
        image.save_image(d_new, 'new_'+filename)
    except Exception, e:
        print str(e)


def decrypt(filename, password, magic, rsa):
    '''
    A method that decrypt text from image

    Args:
	filename (str) : The filename of the image
  	password (str) : Used to decrypt text
	magic    (str) : Used to retrieve text from image

    Returns:
	Text hided in image
    '''
    
    try:
        image = ImageHandler(filename)
        # Load image
        data = image.load_image()

        # Retrieve text
        text = Steganography.retrieve_lsb(data, magic)

        # Optional Decrypt
        if not password is None:
            print '[*] Decrypting text'
            text = Encryption.decrypt_text(password, text)
        if not rsa is None:
            print '[*] Decrypting text'
            text = Encryption.decrypt_rsa(text, rsa)
        
        print '[*] Retrieved text: \n%s' % text
    except Exception, e:
        print str(e)
    
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
    args = parser.parse_args()

    if args.encrypt ^ args.decrypt == False:
        parser.error('Incorrect encrypt/decrypt mode')
    else:
        if args.encrypt:
            if args.text == None:
                parser.error('Require text/text.path in encrypt mode')
    if args.password != None and args.rsa != None:
        parser.error('Specify Encryption/Decryption technique either RSA or Password')
    return args

if __name__ == "__main__":
    args = parse_options()
    if args.encrypt:
        encrypt(args.filename, args.text, args.password, args.magic, args.rsa)
    else:
        decrypt(args.filename, args.password, args.magic, args.rsa)
    