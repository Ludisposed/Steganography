import Image
import numpy as np
import sys
import os
import getopt

# Set location of directory we are working in to load files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def encrypt(filename, text, magic):
    # Load image in rgb-array
    # Least Significant Bit
    # Encrypt with 'Password:magic', and 'text'
    print 'I am here'
    try:
        d = load_image( filename )
        print d
    except Exception,e:
        print str(e)
    
def decrypt(filename, text, magic):
    # Load image in rgb-array
    # Least Significant Bit
    # Decrypt with 'Password:magic', and 'text'
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
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
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
    print "stego.py -e test.jpeg howareyou --magic password"
    print "stego.py -d test.jpeg"
    print "stego.py -d test.jpeg -m password"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hed:m",["help", "encrypt", "decrypt", "magic"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

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

        # Faulty but busy now
        text = ''
        if not to_encrypt:
            filename    = sys.argv[3]
        else:
            filename    = sys.argv[3]
            text        = sys.argv[4]

        print to_encrypt, filename, text

    
