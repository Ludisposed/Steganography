from PIL import Image
import numpy as np
import sys
import os
import getopt
import Steganography
import Encryption


# Set location of directory we are working in to load/save files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


'''
    Filehandling I/O stuff
'''
def load_image(filename):
    img = Image.open(os.path.join(__location__, filename))
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_image(npdata, outfilename): 
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "RGB")
    img.save(os.path.join(__location__, outfilename))


def change_image_form(filename):
    f = filename.split('.')
    if f[-1] not in ['bmp', 'BMP', 'PNG', 'png']:
        img = Image.open(os.path.join(__location__, filename))
        img.load()
        filename = ''.join(f[:-1]) + '.png'
        img.save(os.path.join(__location__, filename))
    return filename


def check_image_space(text,data):
    if data.size < len(text):
        print '[*] Image not big enough'
        sys.exit(0)


def trans_file_to_text(text):
    if os.path.isfile(text):
        with open(text, 'r') as f:
            text = ''.join([i for i in f])
    return text


'''
    Main methods and usage
'''
text_ascii = lambda text: map(int, ''.join(map(lambda char: '{:07b}'.format(ord(char)), text)))

# Nessecary?
endbit = [0] * 7


def encrypt(filename, text, password, magic):
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
    text = trans_file_to_text(text)

    # Optional encrypt
    if not password is None:
        print '[*] Encrypting text'
        text = Encryption.encrypt_text(password, text)

    text = text_ascii(text) + endbit

    try:
        # Change format to png
        filename = change_image_form(filename)
       
        # Load Image
        d_old = load_image(filename)
        
        # Check if image can contain the data
        check_image_space(text,d_old)
       
        # get new data and save to image
        d_new = Steganography.hide_lsb(d_old, magic, text)
        save_image(d_new, 'new_'+filename)
    except Exception, e:
        print str(e)


def decrypt(filename, password, magic):
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
        # Load image
        data = load_image(filename)

        # Retrieve text
        text = Steganography.retrieve_lsb(data, magic)

        # Optional Decrypt
        if not password is None:
            print '[*] Decrypting text'
            text = Encryption.decrypt_text(password, text)
        
        print '[*] Retrieved text: \n%s' % text
    except Exception, e:
        print str(e)


def usage():
    print "Steganography prng-Tool @Ludisposed & @Qin"
    print ""
    print "Usage: prng_stego.py -e -p password -m magic filename text "
    print "-e --encrypt              - encrypt filename with text"
    print "-d --decrypt              - decrypt filename"
    print ''
    print 'Optionals'
    print "-p --password             - encrypt/decrypt with password"
    print "-m --magic                - hide/retrieve   with prng_magic"
    print ""
    print ""
    print "Examples: "
    print "prng_stego.py -e -p password -m magic test.png howareyou"
    print 'python prng_stego.py -e -p password -m magic test.png tester.sh'
    print 'python prng_stego.py -e -p password -m magic test.png file_test.txt'
    print 'prng_stego.py --encrypt --password password --magic magic test.png "howareyou  some other text"'
    print "prng_stego.py -e test.png howareyou"
    print ''
    print "prng_stego.py -d -p password -m magic new_test.png"
    print "prng_stego.py -d new_test.png"
    print "prng_stego.py --decrypt --password password --magic magic new_test.png"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hedm:p:", ["help", "encrypt", "decrypt", "magic=", "password="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    
    magic = to_encrypt = password = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-e", "--encrypt"):
            to_encrypt = True
        elif o in ("-d", "--decrypt"):
            to_encrypt = False
        elif o in ("-m", "--magic"):
            magic = a
        elif o in ("-p", "--password"):
            password = a
        else:
            assert False, "Unhandled Option"

    if to_encrypt is None:
        usage()

    if not to_encrypt:
        filename = args[0]
        decrypt(filename, password, magic)
    else:
        filename = args[0]
        text = args[1]
        encrypt(filename, text, password, magic)
