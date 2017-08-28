from file_handler import FileHandler
import numpy as np
import soundfile as sf
import struct

class AudioHandler(FileHandler):
    """docstring for Audio"""
    def __init__(self, filename):
        FileHandler.__init__(self,filename)

    def load_audio(self):
        data, samplerate = sf.read(self.filename)
        for i in data:
            print [b for b in bytearray(struct.pack("f", i))]

    def save_audio(self):
        pass
