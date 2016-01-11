camera_calibration
=====================
This library takes in images of a grid in a folder and generates camera calibration data based on the images.

Some tips:
 * Use an asymetric grid (different number of rows and cols). Don't worry if you already have a grid that is symetric, just cover a row or colomn with white paper or tape.
 * Use a grid with a white border around it.
 * Take more images than you think you will need. Often, some images fail.


To Install:
-----------
 #. Clone the repository or download the zip
 #. run: ``python setup.py install

That's it!!

At a later time, I would like to open source this and put it on PyPi

To use within another python script:
--------------------------------------
The calibration routine can be run from within another script like this::

    import camera_calibration as cc

    cc.calibrate(dir, rows, cols, win, save, outdir, space, visualize)

============= ========= ========================================================
Arg           Type      Use
============= ========= ========================================================
``dir``       ``str``   The directory where the image sources are
``rows``      ``int``   The number of internal corners on the grid vertically
``cols``      ``int``   The number of internal corners on the grid horizontally
``win``       ``int``   The window across which to look for subpixel corners
``save``      ``bool``  Whether or not to save output
``outdir``    ``str``   Where to save output
``space``     ``float`` The grid spacing in mm
``visualize`` ``bool``  Whether or not to visualize output while running
============= ========= ========================================================

To use as a standalone command line utility:
-----------------------------------------------
This system can also be used from the commandline. Once the system is installed, so long as python is on your path, it can be run very simply. For more information, run ``calibrate-camera -h`` from the commandline/terminal
