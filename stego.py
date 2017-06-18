from PIL import Image
import numpy as np
import sys
import os
import getopt
import base64
import re
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

def encrypt(filename, text, magic, step):
    
    #The magic
    if not magic is None:
        key = Fernet.generate_key()
        text = encrypt_text(magic, text)
        
    try:
        # Change format to png
        filename = change_image_form(filename)
        
        # Load Image
        d_old = load_image( filename )

        # Check if image can contain the data
        if ('0' <= step[0] <= '9' and len(d_old)*len(d_old[0])*3 < len(text) * int(step))\
        or ('a' <= step[0] <= 'z' and len(d_old)*len(d_old[0])*len(step) < len(text)): 
            print 'image not big enough'
            sys.exit(0)


        
        # get new data and save to image
        d_new = change_lsb(text_ascii(text), d_old, step)
        
        save_image(d_new, 'new_'+filename)
        
    except Exception,e:
        print str(e)
    
def decrypt(filename, magic, step):
    try:
        # Load image
        d = load_image( filename )

        # Retrieve text
        text = retrieve_lsb(d, step)

        # Added magic
        if not magic is None:
            text = decrypt_text(magic, text)
        print text
    except Exception,e:
        print str(e)

def text_ascii(text):
    return map(lambda x: '{:07b}'.format(ord(x)),text)
def ascii_text(a):
    return chr(int(a, 2))

def retrieve_lsb(d, step):    
    l = ''
    out = ''
    k_range,s = step_info(step)
    c = 1
    for _ in d:
        for i in _:             
            for k in k_range:
                if c == s:
                    l += str(i[k] & 1)
                    if len(l) == 7:
                        if int(l) > 0:
                            out += ascii_text(l)
                            l = ''
                        else:
                            return out
                    c = 1
                else:
                    c += 1
    return out

def change_lsb(t,d,step):
    t = [int(x) for x in ''.join(t)] + [0]*7 # endbit
    b = 0
    k_range,s = step_info(step)
    c = 1
    for _ in d:
        for i in _:              
            for k in k_range:
                if c == s:
                    i[k] = (i[k] & ~1) | t[b]
                    b += 1
                    if b == len(t):
                        return d
                    c = 1
                else:
                    c += 1
    return d


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
# TODO: bad function name
# return a list: 0 is the range of 'k', 1 is step in int
def step_info(step):
    if len(step) == 0:
        return [range(3),1]
    s = 1
    if '0' <= step[0] <= '9':
        k_range = range(3)
        s = int(step)
    else:
        k_range = []
        if 'r' in step:
            k_range += [0]
        if 'g' in step:
            k_range += [1]
        if 'b' in step:
            k_range += [2]
    return [k_range, s]

def usage():
    print "Steganography Tool @Ludisposed & @Qin"
    print ""
    print "Usage: stego.py -e -m magic filename text "
    print "-e --encrypt              - encrypt filename with text"
    print "-d --decrypt              - decrypt filename"
    print "-m --magic                - encrypt/decrypt with password"
    print ""
    print ""
    print "Examples: "
    print "stego.py -e test.png howareyou"
    print "stego.py -e -s 10 test.png howareyou"
    print "stego.py -e --magic password test.png howareyou "
    print "stego.py -e --magic password --rgb rg test.png howareyou"
    print "stego.py -d test.png"
    print "stego.py -d -s 10 test.png"
    print "stego.py -d -m password test.png"
    print "stego.py -d -m password --rgb rg test.png"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        # Adding optional -s [steps] -rgb [r or g or b]
        opts,args = getopt.getopt(sys.argv[1:],"heds:m:",["help", "encrypt", "decrypt", "rgb=", "step=", "magic="])
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
        elif o in ("-s","--step"):
            try:
                t = int(a)
                if t <= 0:
                    print "step is negtive, step will be default 1"
                    step = "1"
                else:
                    step = a
            except Exception:
                print "step is not an int, step will be default 1"
                step = "1"
        elif o in ("--rgb"):
            if len(a) > 0 and len(a) <= 3:
                m = re.search('(r?)(g?)(b?)',a)
                if m and len(m.group(0)) > 0:
                    step = m.group(0)
                    continue
            
            print "rgb value form is not right, rgb value will be default 'rgb'"
            step = 'rgb'

        else:
            assert False,"Unhandled Option"

    if not to_encrypt:
        filename    = args[0]
        decrypt(filename, magic, step)
    else:
        filename    = args[0]
        text        = args[1]
        encrypt(filename, text, magic, step)   
