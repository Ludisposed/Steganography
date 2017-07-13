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

# Set location of directory we are working in to load/save files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_key(password):
    '''
    A method to create the key for encryption

    Args:
        password (str): The password to use for encryption

    Returns:
        The digested pasword
    '''
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())


def encrypt_text(password, token):
    '''
    A method to encrypt the text

    Args:
        password (str): The password to use for encryption
        token    (str): The text that will be encrypted

    Returns:
        The encrypted text
    '''
    f = Fernet(get_key(password))
    return f.encrypt(bytes(token))


def decrypt_text(password, token):
    '''
    A method to decrypt the text

    Args:
        password (str): The password to use for decryption
        token    (str): The text that will be decrypted

    Returns:
        The decrypted text
    '''
    f = Fernet(get_key(password))
    return f.decrypt(bytes(token))


'''
Still methods that are bad
'''
def check_image_space(data):
    if data.size < len(t):
        print '[*] Image not big enough'
        sys.exit(0)


def trans_file_to_text(text):
    if os.path.isfile(text):
        with open(text, 'r') as f:
            text = ''.join([i for i in f])
    return text


def encode_text(text):
    text = trans_file_to_text(text)
    return [int(x) for x in ''.join(text_ascii(encrypt_text(magic, text)))] + [0]*7  # endbit



def encrypt(filename, text, magic):
    # We need to break it down!
    t = encode_text(text)
    print '[*] Encrypting text'
    try:
        # Change format to png
        filename = change_image_form(filename)

        # Load Image
        d_old = load_image(filename)

        # Check if image can contain the data
        check_image_space(d_old)

        # get new data and save to image
        d_new = hide_lsb(d_old, magic, t)
        save_image(d_new, 'new_'+filename)
    except Exception, e:
        print str(e)


def decrypt(filename, magic):
    try:
        # Load image
        data = load_image(filename)

        # Retrieve text
        text = retrieve_lsb(data, magic)
        print '[*] Decrypting text'
        print '[*] Retrieved text: \n%s' % decrypt_text(magic, text)
    except Exception, e:
        print str(e)

# This method needs reworking!!!!
# Unsure how to fix the seed issues
def generate_seed(magic):
    seed = 1
    for char in magic:
        seed *= ord(char)
    print '[*] Your magic number is %d' % seed
    return seed
'''
End of methods that need to be reworked
'''


def text_ascii(text):
    '''
    A method to convert the text to a bitlist

    Args:
        text     (str): The text to be converted to ascii values

    Returns:
        A byterepresentation of the text as a list
    '''
    return map(lambda char: '{:07b}'.format(ord(char)), text)


def ascii_text(byte_char):
    '''
    A method to convert the byte to a character value

    Args:
        byte_char  (list): The byte to be converted to a char

    Returns:
        The character
    '''
    return chr(int(byte_char, 2))


def random_ints(start=0, size):
    '''
    A generator used to prive the pseudo random generated numbers

    Args:
        start    (int): Left bound of the random numbers
        size     (int): Right bound of random numbers

    Returns:
        A random number
    '''
    random_numbers = range(start, size)
    random.shuffle(random_numbers)
    for random_num in random_numbers:
        yield random_num


def insert_fake_data(data):
    '''
    A method used to fill the least significant bits of the picture with fake data

    Args:
        data     (list): The list representation of the image

    Returns:
        The list representation of the image with random lsb's
    '''
    print '[*] Inserting fake data'
    for i in random_ints(data.size):
        data.flat[i] = (data.flat[i] & ~1) | random.randint(0,1)
    print '[*] Done inserting fake data'

def hide_lsb(data, magic, text):
    '''
    A method that hides the least significant bits of the picture with text

    Args:
        data     (list): The list representation of the image
        magic    (str) : The password
        text     (str) : Encrypted text to hide

    Returns:
        The list representation of the image with text hidden in random lsb's
    '''
    print '[*] Hiding message in image'

    insert_fake_data(data)

    # We must alter the seed but for now lets make it simple
    random.seed(generate_seed(magic))

    for char, i in zip(text, random_ints(data.size)):
        data.flat[i] = (data.flat[i] & ~1) | char
        
    print '[*] Finished hiding the message'
    return data


def retrieve_lsb(data, magic):
    '''
    A method that retrieves the least significant bits of the picture

    Args:
        data     (list): The list representation of the image
        magic    (str) : The password

    Returns:
        The list representation of the image with retrieved text from random lsb's
    '''
    print '[*] Retrieving message from image'
    random.seed(generate_seed(magic))

    output = temp_char = ''

    for i in random_ints(data.size):
        temp_char += str(data.flat[i] & 1)
        if len(temp_char) == 7:
            if int(temp_char) == 0:
                print '[*] Finished retrieving'
                return output
            output += ascii_text(temp_char)
            temp_char = ''
    print '[*] Retrieving the message has failed'
    return ''

def load_image(filename):
    '''
    A method that loads an image

    Args:
        filename    (str) : The filename

    Returns:
        The image as an numpy array
    '''
    img = Image.open(os.path.join(__location__, filename))
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_image(npdata, outfilename):
    '''
    A method that saves an image

    Args:
        filename    (str) : The filename
        npdata      (list): The numpy array representation of the image
    '''
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "RGB")
    img.save(os.path.join(__location__, outfilename))


def change_image_form(filename):
    '''
    A method that changes an image encoding

    Args:
        filename    (str) : The filename

    Returns:
        The image
    '''
    f = filename.split('.')
    if not (f[-1] == 'bmp' or f[-1] == 'BMP' or f[-1] == 'PNG' or f[-1] == 'png'):
        img = Image.open(os.path.join(__location__, filename))
        img.load()
        filename = ''.join(f[:-1]) + '.png'
        img.save(os.path.join(__location__, filename))
    return filename


def usage():
    print "Steganography prng-Tool @Ludisposed & @Qin"
    print ""
    print "Usage: prng_stego.py -e -m magic filename text "
    print "-e --encrypt              - encrypt filename with text"
    print "-d --decrypt              - decrypt filename"
    print "-m --magic                - encrypt/decrypt with password"
    print ""
    print ""
    print "Examples: "
    print "prng_stego.py -e -m pass test.png howareyou"
    print 'python prng_stego.py -e -m magic test.png tester.sh'
    print 'python prng_stego.py -e -m magic test.png file_test.txt'
    print 'prng_stego.py --encrypt --magic password test.png "howareyou  some other text"'
    print ''
    print "prng_stego.py -d -m password test.png"
    print "prng_stego.py --decrypt --magic password test.png"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hedm:", ["help", "encrypt", "decrypt", "magic="])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    magic = to_encrypt = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-e", "--encrypt"):
            to_encrypt = True
        elif o in ("-d", "--decrypt"):
            to_encrypt = False
        elif o in ("-m", "--magic"):
            magic = a
        else:
            assert False, "Unhandled Option"

    if magic is None or to_encrypt is None:
        usage()

    if not to_encrypt:
        filename = args[0]
        decrypt(filename, magic)
    else:
        filename = args[0]
        text = args[1]
        encrypt(filename, text, magic)
