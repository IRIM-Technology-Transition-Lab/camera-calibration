from setuptools import setup

setup(name='camera_calibration',
      version='0.1',
      description='A basic script to run camera calibration on images in a folder.',
      url='',
      author='Michael Sobrepera',
      author_email='mjsobrep@live.com',
      license='TBD',
      packages=['camera_calibration'],
      install_requires=[
          'argparse',
          'numpy',
          'cv2',
          'colorama'
      ],
      zip_safe=True)
