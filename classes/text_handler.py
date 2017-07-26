import os
from file_handler import FileHandler

class TextHandler(FileHandler):
	def __init__ (self, filename):
		FileHandler.__init__(self, filename)
		self.text = filename
		self.trans_file_to_text()

	def trans_file_to_text(self):
	    textfile = os.path.join(self.path, self.filename)
	    if os.path.isfile(textfile) and os.path.exists(textfile):
	        with open(textfile, 'r') as f:
	            self.text = ''.join([i for i in f])