import random
import numpy as np


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
    print('[*] Hiding message in image')

    if not magic is None:
        insert_fake_data(data)

        # We must alter the seed but for now lets make it simple
        random.seed(generate_seed(magic))

        for char, i in zip(text, random_ints(data.size)):
            data.flat[i] = (data.flat[i] & ~1) | char
    else:
        for i in range(len(text)):
            data.flat[i] = (data.flat[i] & ~1) | text[i]
    
    print('[*] Finished hiding the message')
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
    print('[*] Retrieving message from image')

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
                    print('[*] Finished retrieving')
                    return output
                output += chr(int(temp_char, 2))
                temp_char = ''
    print('[*] Retrieving the message has failed')
    return ''

def generate_seed(magic):
    seed = 1
    for char in magic:
        seed *= ord(char)
    print('[*] Your magic number is {}'.format(seed))
    return seed

def random_ints(size, start=0):
    random_numbers = list(range(start, size))
    random.shuffle(random_numbers)
    for random_num in random_numbers:
        yield random_num


def insert_fake_data(data):
    print('[*] Inserting fake data')
    for i in random_ints(data.size):
        data.flat[i] = (data.flat[i] & ~1) | random.randint(0,1)
    print('[*] Done inserting fake data')
