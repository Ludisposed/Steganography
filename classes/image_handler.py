from file_handler import FileHandler
from PIL import Image
import numpy as np
import sys
import os
class ImageHandler(FileHandler):
	"""docstring for Image"""
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


	
	