import os
from PIL import Image
import cv2
import numpy as np
import sys
import skvideo.io

class FileHandler(object):
    def __init__(self, filename):
	self.path, self.filename = self.file_path_composition(filename)
		
    def file_path_composition(self, filename):
	if os.path.isfile(filename):
	    return os.path.split(filename)
	return ("" ,filename)

class TextHandler(FileHandler):
    def __init__ (self, filename):
	FileHandler.__init__(self, filename)
	self.text = filename
	self.trans_file_to_text()

    def trans_file_to_text(self):
	textfile = os.path.join(self.path, self.filename)
	if os.path.isfile(textfile) and os.path.exists(textfile):
	    with open(textfile, 'r') as f:
                self.text = f.read()

class ImageHandler(FileHandler):
    def __init__(self, filename):
	FileHandler.__init__(self,filename)
        
        # Change format to png
	self.change_image_form()

    def load_image(self):
	img = Image.open(os.path.join(self.path, self.filename))
	img.load()
	data = np.asarray(img, dtype="int32")
	return data

    def save_image(self, npdata, outfilename): 
	img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "RGB")
	img.save(os.path.join(self.path, outfilename))

    def change_image_form(self):
	f = self.filename.split('.')
	if f[-1].lower() not in ['bmp', 'png']:
	    img = Image.open(os.path.join(self.path, self.filename))
	    img.load()
	    self.filename = ''.join(f[:-1]) + '.png'
	    img.save(os.path.join(self.path, self.filename))
class VideoHandler(FileHandler):
    def __init__(self, filename):
        FileHandler.__init__(self, filename)

    def load_video(self):
        file_path = os.path.join(self.path, self.filename)

        vid = skvideo.io.FFmpegReader(file_path)
        data = skvideo.io.ffprobe(file_path)['video']
        rate = data['@r_frame_rate']
        return vid, rate

    def save_video(self, frames, rate, new_filename='new_video.avi'):
        writer = skvideo.io.FFmpegWriter(os.path.join(self.path, new_filename),
                                         inputdict={
                                                    '-r': rate,
                                         }, 
                                         outputdict={
                                                    '-vcodec': 'libx264', 
                                                    '-b': '300000000',
                                                    '-r': rate,
                                         })
        for frame in frames:
            writer.writeFrame(frame.astype(np.uint8))
        writer.close()
