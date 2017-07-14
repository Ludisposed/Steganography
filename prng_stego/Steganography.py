import random
import numpy as np


ascii_text = lambda byte_char: chr(int(byte_char, 2))


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

    output = temp_char = ''
    if not magic is None:
        random.seed(generate_seed(magic))

        # TODO: Make function for this
        for i in random_ints(data.size):
            temp_char += str(data.flat[i] & 1)
            if len(temp_char) == 7:
                if int(temp_char) == 0:
                    print '[*] Finished retrieving'
                    return output
                output += ascii_text(temp_char)
                temp_char = ''
    else:
        # TODO: Make function for this
        for i in range(data.size):
            temp_char += str(data.flat[i] & 1)
            if len(temp_char) == 7:
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
