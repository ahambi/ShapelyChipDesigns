
from distutils.core import setup

setup(name='ShapelyChipDesigns',
      version='0.0',
      description='Chip design package based on the Shapely module', 
      author='hambi',
      author_email='annahambi@gmail.com',
      py_modules=['src'],
      packages=['src'], 
      package_data={'': ['src/convert.rb']}
      #data_files=[('', ['ShapelyChipDesigns/convert.rb'])]
      )