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
    
    #The magic
    if not magic is None:
        key = Fernet.generate_key()
        text = encrypt_text(magic, text)
        
    try:
        # Change format to png
        filename = change_image_form(filename)
        
        # Load Image
        d_old = load_image( filename )        
        encrypt_lsb(d_old, magic, text)
        
        save_image(d_old, 'new_'+filename)
        
    except Exception,e:
        print str(e)
    
def decrypt(filename, magic):
    try:
        # Load image
        d = load_image( filename )
        
        text = decrypt_lsb(d, magic)
        print decrypt_text(magic, text)

    except Exception,e:
        print str(e)

def text_ascii(text):
    return map(lambda x: '{:07b}'.format(ord(x)),text)
def ascii_text(a):
    return chr(int(a, 2))

def encrypt_lsb(d, m, t):
    t = [int(x) for x in ''.join(text_ascii(t))] + [0]*7 # endbit
    
    # We must alter the seed but for now lets make it simple
    # this requeris the use of paswords though
    
    seed = 1
    for i in m:
        seed *= ord(i)
    random.seed(seed)
    
    r = random.sample(range(1, d.size), len(t))
    d_lin = d.view()  # construct a view
    d_lin.shape = -1  # turn the view into a 1d array
    for i in range(len(r)):
        d_lin[r[i]-1] = (d_lin[r[i]-1] & ~1) | t[i]

def decrypt_lsb(d, m):
    
    seed = 1
    for i in m:
        seed *= ord(i)
    random.seed(seed)
    
    r = random.sample(range(1, d.size), d.size-1)
    d_lin = d.view()  # construct a view
    d_lin.shape = -1  # turn the view into a 1d array

    l = ''
    out = ''
    
    for i in range(len(r)):
        l += str(d_lin[r[i]-1] & 1)
        if len(l) == 7:
             if int(l) > 0:
                 out += ascii_text(l)
                 l = ''
             else:
                 return out

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

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hedm:",["help", "encrypt", "decrypt", "magic="])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    magic = None
    step = ""
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

    if magic is None:
        print 'Only possible with password'
        sys.exit(0)
    
    if not to_encrypt:
        filename    = args[0]
        decrypt(filename, magic)
    else:
        filename    = args[0]
        text        = args[1]
        encrypt(filename, text, magic)   
