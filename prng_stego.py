from PIL import Image
import numpy as np
import sys
import os
import getopt
import Steganography
import Encryption


# Gets ascii representation from string to list of bits
text_ascii = lambda text: map(int, ''.join(map(lambda char: '{:08b}'.format(ord(char)), text)))

# Globals
ENDBIT = [0] * 8
PATH = ""


'''
    Filehandling I/O stuff
'''

def file_path_composition(filename):
    if os.path.isfile(filename):
        return os.path.split(filename)
    return ("",filename)


def load_image(filename):
    img = Image.open(os.path.join(PATH, filename))
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_image(npdata, outfilename): 
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "RGB")
    img.save(os.path.join(PATH, outfilename))


def change_image_form(filename):
    f = filename.split('.')
    if f[-1] not in ['bmp', 'BMP', 'PNG', 'png']:
        img = Image.open(os.path.join(PATH, filename))
        img.load()
        filename = ''.join(f[:-1]) + '.png'
        img.save(os.path.join(PATH, filename))
    return filename


def check_image_space(text,data):
    if data.size < len(text):
        print '[*] Image not big enough'
        sys.exit(0)


def trans_file_to_text(text):
    path,text = file_path_composition(text)
    filename = os.path.join(path, text)
    if os.path.isfile(filename) and os.path.exists(filename):
        with open(text, 'r') as f:
            text = ''.join([i for i in f])
    
    return text


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
    text = trans_file_to_text(text)

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
        # Load image
        data = load_image(filename)

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
    print "-r --rsa                  - encrypt using RSA [filename of key]"
    print ""
    print ""
    print "Examples: "
    print "prng_stego.py -e -p password -m magic test.png howareyou"
    print 'python prng_stego.py -e -p password -m magic test.png tester.sh'
    print 'python prng_stego.py -e -p password -m magic test.png file_test.txt'
    print 'prng_stego.py --encrypt --password password --magic magic test.png "howareyou  some other text"'
    print "prng_stego.py -e test.png howareyou"
    print "prng_stego.py -e -r new test.png howareyou"
    print ''
    print "prng_stego.py -e --rsa private.pem new_test.png"
    print "prng_stego.py -d -p password -m magic new_test.png"
    print "prng_stego.py -d new_test.png"
    print "prng_stego.py --decrypt --password password --magic magic new_test.png"
    sys.exit(0)

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hedm:p:r:", ["help", "encrypt", "decrypt", "magic=", "password=", "rsa="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    
    magic = to_encrypt = password = rsa = None
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
        elif o in ("-r", "--rsa"):
            rsa = a
        else:
            assert False, "Unhandled Option"

    if to_encrypt is None:
        usage()

    filename = args[0]
    PATH, filename = file_path_composition(filename)

    if rsa and password:
        print 'Specify Encryption technique either RSA or Password'
        sys.exit(1)

    if not to_encrypt:
        decrypt(filename, password, magic, rsa)
    else:
        text = args[1]
        encrypt(filename, text, password, magic, rsa)
