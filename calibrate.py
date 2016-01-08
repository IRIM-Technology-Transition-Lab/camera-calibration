import argparse
from os import walk
import os
import numpy as np
import cv2

#Based on example at: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


#Parse in arguments
parser = argparse.ArgumentParser(description='Calibrate images.')

parser.add_argument("--dir", metavar="directory", type = str , help='The directory of images to calibrate off of.', default = "/")

parser.add_argument("-s","--spacing", type = float, help = "The grid spacing in mm." , required = True)

parser.add_argument("-c","--columns",type = int , help = "the number of inner corners horizontally", required = True)

parser.add_argument("-r","--rows",type = int , help = "the number of inner corners vertically", required = True)

parser.add_argument("-w","--window",type = int , help = "The size of the window to use for subpixel localization of the corners", default = 11)

args = parser.parse_args()

#Figure out where the images are and get all filenames for that directory
targetDir = os.getcwd()+args.dir
(_, _, filenames) = walk(targetDir).next()

rows = args.rows
cols = args.columns
win = args.window

if rows==cols:
    print "it is best to use an asymetric grid, rows and cols should be different"
    exit()

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((cols*rows,3), np.float32)
objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# termination criteria for the subpixel corner search algorithim
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cv2.namedWindow("Raw Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Image with Corners", cv2.WINDOW_NORMAL)

for file in filenames:
    #Try to read in image as grayscale
    img = cv2.imread(file, 0 )

    #If the file isn't an image, move on
    if img is not None:
        print "read image: "+file
        cv2.imshow('Raw Image',img)
        cv2.waitKey(100)

        #Find chessboard corners
        ret, corners = cv2.findChessboardCorners(img, (rows,cols),cv2.CALIB_CB_FAST_CHECK)

        #If we found chessboard corners lets work on them
        if ret:
            print "\tfound corners"
            objpoints.append(objp)

            #get subpixel accuracy corners
            corners2 = cv2.cornerSubPix(img,corners,(win,win),(-1,-1),criteria)
            imgpoints.append(corners2)
            print "\t\tfound subpixel corners"

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (cols,rows), corners2,ret)
            cv2.imshow('Image with Corners',img)
            cv2.waitKey(100)
        else:
            print "\tcould not find corners"

cv2.destroyAllWindows()
