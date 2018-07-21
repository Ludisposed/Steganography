__all__ = ['steganography',
           'file_handler', 
           'encryption']

import file_handler
import encryption
import steganography
import utility

def encrypt_image(filename, text, magic):
    image = file_handler.ImageHandler(filename)
    d_old = image.load_image()
    d_new = steganography.hide_lsb(d_old, magic, text)
    image.save_image(d_new, 'new_' + image.filename)

def encrypt_video(filename, text, magic):
    video = file_handler.VideoHandler(filename)
    frames, fps, aud = video.load_video()
    new_frame = steganography.hide_lsb(frames[0], magic, text)
    new_frames = [new_frame] + frames[1:]
    video.save_video(frames, fps, aud, 'new_' + video.filename)

def encrypt_audio(filename, text, magic):
    pass

def decrypt_image(filename, magic):
    image = file_handler.ImageHandler(filename)
    data = image.load_image()
    text = steganography.retrieve_lsb(data, magic)
    return text

def decrypt_video(filename, magic,):
    video = file_handler.VideoHandler(filename)
    frames, fps, _ = video.load_video()
    text = steganography.retrieve_lsb(frames[0], magic)
    return text

def decrypt_audio(filename, magic):
    pass