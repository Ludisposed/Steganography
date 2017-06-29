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
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())


def encrypt_text(password, token):
    f = Fernet(get_key(password))
    return f.encrypt(bytes(token))


def decrypt_text(password, token):
    f = Fernet(get_key(password))
    return f.decrypt(bytes(token))


def encrypt(filename, text, magic):
    # check whether the text is a file name
    if len(text.split('.')[1:]):
        text = read_files(os.path.join(__location__, text))
    t = [int(x) for x in ''.join(text_ascii(encrypt_text(magic, text)))] + [0]*7 # endbit
    try:
        # Change format to png
        filename = change_image_form(filename)

        # Load Image
        d_old = load_image(filename)

        # Check if image can contain the data
        if d_old.size < len(t):
            print '[*] Image not big enough'
            sys.exit(0)

        # get new data and save to image
        d_new = encrypt_lsb(d_old, magic, t)
        save_image(d_new, 'new_'+filename)
    except Exception, e:
        print str(e)


def decrypt(filename, magic):
    try:
        # Load image
        data = load_image(filename)

        # Retrieve text
        text = decrypt_lsb(data, magic)
        print '[*] Retrieved text: \n%s' % decrypt_text(magic, text)
    except Exception, e:
        print str(e)


def text_ascii(text):
    return map(lambda x: '{:07b}'.format(ord(x)), text)


def ascii_text(a):
    return chr(int(a, 2))


def next_random(r, d):
    r2 = random.randint(0, d.size-1)
    while r2 in r:
        r2 = random.randint(0, d.size-1)
    return r2


def generate_seed(m):
    seed = 1
    for i in m:
        seed *= ord(i)
    print '[*] Your magic number is %d' % seed
    return seed


def encrypt_lsb(data, magic, text):
    print '[*] Starting Encryption'

    # We must alter the seed but for now lets make it simple
    random.seed(generate_seed(magic))

    random_list = []
    for i in range(len(t)):
        next_random_number = next_random(random_list, data)
        random_list.append(next_random_number)
        data.flat[next_random_number] = (data.flat[next_random_number] & ~1) | text[i]

    print '[*] Finished Encryption'
    return data


def decrypt_lsb(data, magic):
    print '[*] Starting Decryption'
    random.seed(generate_seed(magic))

    random_list = []
    output = temp_char = ''

    for i in range(data.size):
        next_random_number = next_random(r, data)
        random_list.append(next_random_number)
        temp_char += str(data.flat[next_random_number] & 1)
        if len(temp_char) == 7:
            if int(temp_char) > 0:
                output += ascii_text(temp_char)
                temp_char = ''
            else:
                print '[*] Finished Decryption'
                return output


def load_image(filename):
    img = Image.open(os.path.join(__location__, filename))
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_image(npdata, outfilename) :
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "RGB")
    img.save(os.path.join(__location__, outfilename))


def change_image_form(filename):
    f = filename.split('.')
    if not (f[-1] == 'bmp' or f[-1] == 'BMP' or f[-1] == 'PNG' or f[-1] == 'png'):
        img = Image.open(os.path.join(__location__, filename))
        img.load()
        filename = ''.join(f[:-1]) + '.png'
        img.save(os.path.join(__location__, filename))
    return filename


def read_files(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return ''.join([i for i in f])
    return filename.replace(__location__, '')


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
