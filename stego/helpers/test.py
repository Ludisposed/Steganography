import file_handler
import steganography
import numpy as np

text_ascii = lambda text: map(int, ''.join(map(lambda char: '{:08b}'.format(ord(char)), text)))
text = text_ascii("Some fucking text you know it") + [0] * 8
vid = file_handler.VideoHandler('/root/Videos/video.webm')

INP = []
OUT = []

def encode_video(vid):
    global INP
    vid, rate = vid.load_video()
    frames = []
    for idx, frame in enumerate(vid.nextFrame()):
        new_frame = steganography.hide_lsb(frame, None, text)
        frames.append(new_frame)
        INP.append(new_frame)
    return frames, rate

def decode_video(vid):
    global OUT
    vid, rate = vid.load_video()
    for idx, frame in enumerate(vid.nextFrame()):
        OUT.append(frame)
        text = steganography.retrieve_lsb(frame, None)
        print(text)

frames, rate = encode_video(vid)
vid.save_video(frames, rate)

rev_vid = file_handler.VideoHandler('/root/Videos/new_video.avi')
decode_video(rev_vid)

for a, b in zip(INP, OUT):
    print np.array_equal(a, b)
