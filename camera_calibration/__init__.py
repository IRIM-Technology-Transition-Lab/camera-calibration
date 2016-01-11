from os import walk
import os
import numpy as np
import cv2
from colorama import init, Fore, Back, Style

#Based on example at: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


def calibrate(dir, rows, cols, win, save, outdir, space, visualize):
    #Figure out where the images are and get all filenames for that directory
    targetDir = os.getcwd()+dir+"\\"
    outdir = os.getcwd() + outdir
    print "Searching for images in: " + targetDir +"\n"
    # (_, _, filenames) = walk(targetDir).next()
    filenames = os.listdir(targetDir)

    init()

    print Fore.WHITE + Style.DIM + Back.MAGENTA + "Welcome"

    if rows==cols:
        print Style.DIM + Back.RED + "It is best to use an asymetric grid, rows and cols should be different"
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
        print Style.DIM + Back.MAGENTA + "Saving output to: "+outdir
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
            print Style.DIM + Back.CYAN + "searching image: "+file
            if visualize:
                cv2.imshow('Raw Image',img)
                cv2.waitKey(100)

            #Find chessboard corners. 9: cv2.CALIB_CB_FAST_CHECK + cv2.CV_CALIB_CB_ADAPTIVE_THRESH
            ret, corners = cv2.findChessboardCorners(img, (rows,cols),9)

            #If we found chessboard corners lets work on them
            if ret:
                print Style.DIM + Back.GREEN + "\tfound corners"
                objpoints.append(objp)

                #get subpixel accuracy corners
                corners2 = cv2.cornerSubPix(img,corners,(win,win),(-1,-1),criteria)
                imgpoints.append(corners2)
                print Style.DIM + Back.GREEN + "\t\tfound subpixel corners"
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
                print Style.DIM + Back.RED + "\tcould not find corners"
            print "\n"

    cv2.destroyAllWindows()
    if numFound >= 10:
        print Style.DIM + Back.GREEN + "Found " + str(numFound) + " calibratable images."
    else:
        print Style.DIM + Back.RED + "Found " + str(numFound) + " calibratable images."





    print(Style.RESET_ALL)

    # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
