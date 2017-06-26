from PIL import Image
import numpy as np
import sys
import os
import getopt
import base64
import re
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
    
    key = Fernet.generate_key()
    t = [int(x) for x in ''.join(text_ascii(encrypt_text(magic, text)))] + [0]*7
        
    try:
        # Change format to png
        filename = change_image_form(filename)
        
        # Load Image
        d_old = load_image( filename )        
        d_old = encrypt_lsb(d_old, magic, t)      
        save_image(d_old, 'new_'+filename)
        
    except Exception,e:
        print str(e)
    
def decrypt(filename, magic):
    try:
        # Load image
        d = load_image( filename )
        
        text = decrypt_lsb(d, magic)
        print magic, text
        print decrypt_text(magic, text)

    except Exception,e:
        print str(e)

def text_ascii(text):
    return map(lambda x: '{:07b}'.format(ord(x)),text)
def ascii_text(a):
    return chr(int(a, 2))

def encrypt_lsb(d, m, t):
    print '[*] Starting Encryption'
    print t
    # We must alter the seed but for now lets make it simple
    # this requeris the use of paswords though
    
    seed = 1
    for i in m:
        seed *= ord(i)
    random.seed(seed)
    print seed
    
    r = random.sample(range(1, d.size), len(t))
    for i in range(len(r)):
        
        d.flat[r[i]-1] = (d.flat[r[i]-1] & ~1) | t[i]
        
        if d.flat[r[i]-1] & 1 != t[i]:
            print 'at %d lsb = %d' % (r[i]-1, d.flat[r[i]-1] & 1)
            print 'bit from text = %d' % t[i]


    # Proof the old array is altered with correct value
    seed = 1
    for i in m:
        seed *= ord(i)
    random.seed(seed)
    print seed

    # Works for:
    r = random.sample(range(1, d.size), len(t))

    # Does not work for
    r2 = random.sample(range(1, d.size), d.size-1)
    
    out2 = v = ''
    for i in range(len(r)):
        if r[i]-1 != r2[i]-1:
            print 'at %d: r=%d and r2=%d' % (i, r[i]-1, r2[i]-1)
        
        if d.flat[r[i]-1] & 1 != t[i]:
            print 'at %d lsb = %d' % (r[i]-1, d.flat[r[i]-1] & 1)
            print 'bit from text = %d' % t[i]
        v += str(d.flat[r[i]-1] & 1)        
        if len(v) == 7:
            if int(v) > 0:
                 out2 += ascii_text(v)
                 v = ''
            else:
                 print decrypt_text(m, out2)


    print '[*] Finished Encryption'
    return d
    
def decrypt_lsb(d, m):
    print '[*] Starting Decryption'
    seed = 1
    for i in m:
        seed *= ord(i)
    random.seed(seed)
    print seed
    
    r = random.sample(range(1, d.size), d.size-1)
    out2 = v = ''
    for i in range(len(r)):

        v += str(d.flat[r[i]-1] & 1)
        # print d_lin[r[i]-1] & 1
        
        if len(v) == 7:
            if int(v) > 0:
                 out2 += ascii_text(v)
                 v = ''
            else:
                 print '[*] Finished Decryption'
                 return out2

def load_image( filename ) :
    img = Image.open( os.path.join(__location__, filename) )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "RGB" )
    img.save(os.path.join(__location__, outfilename))

def change_image_form(filename):
    f = filename.split('.')
    if not (f[-1] == 'bmp' or f[-1] == 'BMP' or f[-1] == 'PNG' or f[-1] == 'png'):
        img = Image.open( os.path.join(__location__, filename) )
        img.load()
        filename = ''.join(f[:-1]) + '.png'
        img.save(os.path.join(__location__, filename))
    return filename

def usage():
    print "Steganography prng-Tool @Ludisposed & @Qin"
    print ""
    print "Usage: stego.py -e -m magic filename text "
    print "-e --encrypt              - encrypt filename with text"
    print "-d --decrypt              - decrypt filename"
    print "-m --magic                - encrypt/decrypt with password"
    print ""
    print ""
    print "Examples: "
    print "stego.py -e -m pass test.png howareyou"
    print 'stego.py --encrypt --magic password test.png "howareyou  some other text"'
    print "stego.py -d -m password test.png"
    print "stego.py --decrypt --magic password test.png"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hedm:",["help", "encrypt", "decrypt", "magic="])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    magic = to_encrypt = None
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-e","--encrypt"):
            to_encrypt = True
        elif o in ("-d","--decrypt"):
            to_encrypt = False
        elif o in ("-m", "--magic"):
            magic = a
        else:
            assert False,"Unhandled Option"

    if magic is None or to_encrypt is None:
        usage()
    
    if not to_encrypt:
        filename    = args[0]
        decrypt(filename, magic)
    else:
        filename    = args[0]
        text        = args[1]
        encrypt(filename, text, magic)   
