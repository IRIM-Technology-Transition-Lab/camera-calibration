camera_calibration
==================
This library takes in images of a chessboard or grid of circles in a folder and
generates camera calibration data based on the images.

Some tips:
 * Use an asymmetric grid (different number of rows and cols). Don't worry
   if you already have a grid that is symmetric, just cover a row or column with
   white paper or tape.
 * Use a grid with a white border around it.
 * Take more images than you think you will need. Often, some images fail.


To Install:
-----------
Using PIP (recommended):
........................
``pip install camera_calibration``

Using SetupTools:
.................
 #. Clone the repository or download the zip
 #. run: ``python setup.py install``

    **A Note on virtualenv**: When using a virtual env, one must copy their cv2.so
    (linux) or cv2.pyd (windows) file into the virtual environment at
    Lib/site-packages

To use within another python script:
------------------------------------
The calibration routine can be run from within another script like this::

   import camera_calibration as cc``
   cc.calibrate(dir, rows, cols, win, save, outdir, space, visualize)

============= ========= ========================================================
Arg           Type      Use
============= ========= ========================================================
``dir``       ``str``   The directory where the image sources are
``rows``      ``int``   The number of internal corners on the grid vertically
``cols``      ``int``   The number of internal corners on the grid horizontally
``win``       ``int``   The window across which to look for sub-pixel corners
``save``      ``bool``  Whether or not to save output
``outdir``    ``str``   Where to save output
``space``     ``float`` The grid spacing in mm
``visualize`` ``bool``  Whether or not to visualize output while running
``circles``   ``bool``  Whether to use a circle grid
============= ========= ========================================================

To use as a standalone command line utility:
--------------------------------------------
This system can also be used from the commandline. Once the system is installed,
so long as python is on your path, it can be run very simply. For more
information, run ``calibrate-camera -h`` from the commandline/terminal

Thanks:
-------
This is heavily based on `This Tutorial <http://opencv-python-tutroals.readthedocs.org/
en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html#goal>`_.

Contributors:
-------------
- Michael Sobrepera
- Toni Cvitanic

License:
--------
The MIT License (MIT)

Copyright (c) 2016 GTRC.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
