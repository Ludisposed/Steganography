import os.path
import re

from setuptools import setup, find_packages

def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass
def get_version():
    init_py = get_file(os.path.dirname(__file__), 'prng_stego', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version

def install():
	setup(
		name='prng_stego',                      
		version=get_version(),                    
		packages = find_packages(exclude=['tester','tester_mac']),
		scripts=['prng_stego'],
		install_requires=['Pillow','cryptography','numpy'],             
      )
