import random
import base64
import numpy as np
from helpers import file_handler 

ascii_text = lambda byte_char: chr(int(byte_char, 2))

def encrypt_image(filename, output_filename, text, magic):
    image = file_handler.ImageHandler(filename)
    d_old = image.load_image()
    d_new = hide_lsb(d_old, magic, text)
    image.save_image(d_new, output_filename)

def encrypt_video(filename, output_filename, text, magic):
    video = file_handler.VideoHandler(filename)
    frames, fps, aud = video.load_video()
    new_frame = hide_lsb(frames[0], magic, text)
    new_frames = [new_frame] + frames[1:]
    video.save_video(frames, fps, aud, output_filename)

def encrypt_audio(filename, output_filename, text, magic):
    pass

def decrypt_image(filename, magic):
    image = file_handler.ImageHandler(filename)
    data = image.load_image()
    text = retrieve_lsb(data, magic)
    return text

def decrypt_video(filename, magic,):
    video = file_handler.VideoHandler(filename)
    frames, fps, _ = video.load_video()
    text = retrieve_lsb(frames[0], magic)
    return text

def decrypt_audio(filename, magic):
    pass

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

    if not magic is None:
        insert_fake_data(data)

        # We must alter the seed but for now lets make it simple
        random.seed(generate_seed(magic))

        for char, i in zip(text, random_ints(data.size)):
            data.flat[i] = (data.flat[i] & ~1) | char
    else:
        for i in range(len(text)):
            data.flat[i] = (data.flat[i] & ~1) | text[i]
    
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

    retrieve_range = range(data.size)
    if not magic is None:
        random.seed(generate_seed(magic))
        retrieve_range = random_ints(data.size)

    return retrieve(data, retrieve_range)

def retrieve(data, retrieve_range):
    output = temp_char = ''
    for i in retrieve_range:
            temp_char += str(data.flat[i] & 1)
            if len(temp_char) == 8:
                if int(temp_char) == 0:
                    print '[*] Finished retrieving'
                    return output
                output += ascii_text(temp_char)
                temp_char = ''
    print '[*] Retrieving the message has failed'
    return ''

def generate_seed(magic):
    seed = 1
    for char in magic:
        seed *= ord(char)
    print '[*] Your magic number is %d' % seed
    return seed


def random_ints(size, start=0):
    random_numbers = range(start, size)
    random.shuffle(random_numbers)
    for random_num in random_numbers:
        yield random_num


def insert_fake_data(data):
    print '[*] Inserting fake data'
    for i in random_ints(data.size):
        data.flat[i] = (data.flat[i] & ~1) | random.randint(0,1)
    print '[*] Done inserting fake data'
