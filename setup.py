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
    init_py = get_file(os.path.dirname(__file__), 'stegoprng', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


setup(
	name='stegoprng',                      
	version=get_version(),
    author="Ludisposed&Qin",
    description="Steganography prng-Tool",
    url="https://github.com/Ludisposed/Steganography",             
	packages=find_packages(),
	install_requires=['Pillow', 'cryptography', 'numpy'],
    license="MIT license",         
  )
