import os

class FileHandler(object):
    def __init__(self, filename):
	self.path, self.filename = self.file_path_composition(filename)
		
    def file_path_composition(self,filename):
	if os.path.isfile(filename):
	    return os.path.split(filename)
	return ("",filename)
