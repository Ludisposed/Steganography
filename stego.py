from PIL import Image
from passlib.hash import pbkdf2_sha256
import numpy as np
import sys
import os
import getopt

# Set location of directory we are working in to load files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def encrypt(filename, text, magic):
    if not magic is None:
        hash = pbkdf2_sha256.encrypt(magic, rounds=10000, salt_size=16)
        if pbkdf2_sha256.verify(magic, hash):
            print 'The hash is correctly set\n'
    
    # Load image in rgb-array
    # Least Significant Bit
    # Encrypt with 'Password:magic', and 'text'
    try:
        d = load_image( filename )
        print d
    except Exception,e:
        print str(e)
    
def decrypt(filename, magic):
    # Load image in rgb-array
    # Least Significant Bit
    # Decrypt with 'Password:magic'
    try:
        d = load_image( filename )
        print d
    except Exception,e:
        print str(e)

def load_image( filename ) :
    img = Image.open( os.path.join(__location__, filename) )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "RGB" )
    img.save( outfilename )
    
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
    print "stego.py -e test.jpeg howareyou"
    print "stego.py -e --magic password test.jpeg howareyou "
    print "stego.py -d test.jpeg"
    print "stego.py -d -m password test.jpeg"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hedm:",["help", "encrypt", "decrypt", "magic="])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    magic = None
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

    if not to_encrypt:
        filename    = args[0]
        decrypt(filename, magic)
    else:
        filename    = args[0]
        text        = args[1]
        encrypt(filename, text, magic)   
