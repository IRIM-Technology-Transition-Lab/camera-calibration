import argparse
from os import walk
import os
import numpy as np
import cv2
from colorama import init, Fore, Back, Style

# import pdb

#Based on example at: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


#Parse in arguments
parser = argparse.ArgumentParser(description='Calibrate Images', epilog="This software is designed to calibrate a camera based on images fed in from a folder. Images should be of a grid of white and black squares. It works best if there is a white border around the grid and if the number of columns and rows is different. This can work with any camera, just put the calibration images in a folder and run this script. For best results you need atleast calibratable images.")

parser.add_argument("--dir", metavar="directory", type = str , help='The directory of images to calibrate off of.', default = "")

parser.add_argument("-s","--spacing", type = float, help = "The grid spacing in mm." , required = True)

parser.add_argument("-c","--columns",type = int , help = "the number of inner corners horizontally", required = True)

parser.add_argument("-r","--rows",type = int , help = "the number of inner corners vertically", required = True)

parser.add_argument("-w","--window",type = int , help = "The size of the window to use for subpixel localization of the corners", default = 11)

parser.add_argument("--save", help = "Whether to save image output", action = 'store_true')

parser.add_argument("--outdir",type = str , help = "Where to save image output", default = "output")

parser.add_argument("-v", "--visualize", help = "Whether to show visualizations", action = 'store_true')

args = parser.parse_args()

#Figure out where the images are and get all filenames for that directory
targetDir = os.getcwd()+args.dir+"\\"
print "Searching for images in: " + targetDir +"\n"
# (_, _, filenames) = walk(targetDir).next()
filenames = os.listdir(targetDir)

rows = args.rows
cols = args.columns
win = args.window
save = args.save
outdir = os.getcwd() + args.outdir
space = args.spacing
visualize = args.visualize

print Fore.WHITE + Back.BLUE + "Welcome"

if rows==cols:
    print Back.RED + "It is best to use an asymetric grid, rows and cols should be different"
    print(Style.RESET_ALL)
    exit()

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((cols*rows,3), np.float32)
objp[:,:2] = np.mgrid[0:(rows*space):space,0:(cols*space):space].T.reshape(-1,2)

numFound = 0

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# termination criteria for the subpixel corner search algorithim
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

if visualize:
    cv2.namedWindow("Raw Image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Image with Corners", cv2.WINDOW_NORMAL)

if save:
    print Back.BLUE + "Saving output to: "+outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        print "\tMade a new output directory"
    print "\n"


for file in filenames:
    file = targetDir + file
    #Try to read in image as grayscale
    img = cv2.imread(file, 0 )

    #If the file isn't an image, move on
    if img is not None:
        print Back.GREEN + "read image: "+file
        if visualize:
            cv2.imshow('Raw Image',img)
            cv2.waitKey(100)

        #Find chessboard corners. 9: cv2.CALIB_CB_FAST_CHECK + cv2.CV_CALIB_CB_ADAPTIVE_THRESH
        ret, corners = cv2.findChessboardCorners(img, (rows,cols),9)

        #If we found chessboard corners lets work on them
        if ret:
            print Back.GREEN + "\tfound corners"
            objpoints.append(objp)

            #get subpixel accuracy corners
            corners2 = cv2.cornerSubPix(img,corners,(win,win),(-1,-1),criteria)
            imgpoints.append(corners2)
            print Back.GREEN + "\t\tfound subpixel corners"
            numFound = numFound + 1

            # Draw and display the corners
            colorimg = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            colorimg = cv2.drawChessboardCorners(colorimg, (cols,rows), corners2,ret)
            if visualize:
                cv2.imshow('Image with Corners',colorimg)
            if save:
                cv2.imwrite(outdir + "/grid" + str(numFound) + ".jpg", colorimg)
            cv2.waitKey(100)
        else:
            print Back.RED + "\tcould not find corners"
        print "\n"

cv2.destroyAllWindows()
if numFound >= 10:
    print Back.GREEN + "Found " + str(numFound) + " calibratable images."
else:
    print Back.RED + "Found " + str(numFound) + " calibratable images."

print(Style.RESET_ALL)
# pdb.set_trace()

# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
