from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='camera_calibration',
      version='0.2',
      description='A basic script to run camera calibration on images in a '
                  'folder.',
      long_description=readme(),
      url='https://github.com/IRIM-Technology-Transition-Lab/'
          'camera-calibration.git',
      author='Michael Sobrepera',
      author_email='mjsobrep@live.com',
      license='License :: OSI Approved :: MIT License',
      packages=['camera_calibration'],
      install_requires=[
          'argparse',
          'numpy',
          'cv2',
          'colorama'
      ],
      zip_safe=True,
      entry_points={
        'console_scripts': ['calibrate-camera=camera_calibration.cmd:main']
      })
