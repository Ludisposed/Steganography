import file_handler
import steganography
import numpy as np

text_ascii = lambda text: map(int, ''.join(map(lambda char: '{:08b}'.format(ord(char)), text)))
text = text_ascii("Some fucking text you know it") + [0] * 8
vid = file_handler.VideoHandler('video.mov')

INP = []
OUT = []

def encode_video(vid):
    global INP
    frames, fps = vid.load_video()
    new_frames = []
    for frame in frames:
        new_frame = steganography.hide_lsb(frame, None, text)
        new_frames.append(new_frame)
        INP.append(new_frame)

    return new_frames, fps

def decode_video(vid):
    global OUT
    frames, fps = vid.load_video()
    for frame in frames:
        OUT.append(frame)
        text = steganography.retrieve_lsb(frame, None)
        print(text)

frames, fps = encode_video(vid)
vid.save_video(frames, fps)

rev_vid = file_handler.VideoHandler('new_video.avi')
decode_video(rev_vid)

for a, b in zip(INP, OUT):
    print np.array_equal(a, b)
