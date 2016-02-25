from os import walk
import os
import numpy as np
import cv2
from colorama import init, Fore, Back, Style

#Based on example at: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


def calibrate(dir, rows, cols, win, save, outdir, space, visualize, circles):
    # Setup colored output
    init()

    if len(outdir) and (outdir[0] == '/' or outdir[0] == '\\'):
        outdir = outdir[1:]
    if len(outdir) and (outdir[-1] == '/' or outdir[-1] == '\\'):
        outdir = outdir[:-1]

    if len(dir) and (dir[0] == '/' or dir[0] == '\\'):
        dir = dir[1:]
    if len(dir) and (dir[-1] == '/' or dir[-1] == '\\'):
        dir = dir[:-1]

    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "\nWelcome\n"

    #Figure out where the images are and get all filenames for that directory
    targetDir = os.getcwd() + "\\" + dir+"\\"
    outdir = os.getcwd() + "\\" + outdir
    print "Searching for images in: " + targetDir +"\n"
    filenames = os.listdir(targetDir)



    if visualize:
        print "\tYou have enabled viaualizations.\n\tEach visualization will pause the software for 5 seconds.\n\tTo continue prior to the 5 second time, press any key."

    # Check grid symetry
    if rows==cols:
        print Style.BRIGHT + Back.RED + "It is best to use an asymetric grid, rows and cols should be different"
        print(Style.RESET_ALL)
        exit()

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((cols*rows,3), np.float32)
    objp[:,:2] = np.mgrid[0:(rows*space):space,0:(cols*space):space].T.reshape(-1,2)

    numFound = 0 # How many good images are there?
    shape = 0 # Placeholder for the image shape

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    # termination criteria for the subpixel corner search algorithim
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Setup windows for visualization
    if visualize:
        cv2.namedWindow("Raw Image", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Undistorted Image", cv2.WINDOW_NORMAL)
        if circles:
            cv2.namedWindow("Image with Centers", cv2.WINDOW_NORMAL)
        else:
            cv2.namedWindow("Image with Corners", cv2.WINDOW_NORMAL)

    # Check if output directory exists, if not, make it.
    if save:
        print Style.BRIGHT + Back.MAGENTA + "Saving output to: "+outdir
        if not os.path.exists(outdir):
            os.makedirs(outdir)
            print Style.BRIGHT + Back.GREEN + "\tMade a new output directory"
        print "\n"

    #########################################################################
    for file in filenames:
        file = targetDir + file

        # Try to read in image as grayscale
        img = cv2.imread(file, 0 )

        # If the file isn't an image, move on
        if img is not None:
            print Style.BRIGHT + Back.CYAN + "searching image: "+file

            if visualize:
                cv2.imshow('Raw Image',img)
                cv2.waitKey(5000)

            if circles:
                # Find circle centers.
                ret, centers = cv2.findCirclesGrid(img, (rows,cols))
            else:
                # Find chessboard corners. 9: cv2.CALIB_CB_FAST_CHECK + cv2.CV_CALIB_CB_ADAPTIVE_THRESH
                ret, corners = cv2.findChessboardCorners(img, (rows,cols),9)



            # If we found chessboard corners lets work on them
            if ret:
                print Style.BRIGHT + Back.GREEN + "\tfound corners or centers"
                objpoints.append(objp)

                # Since this is a good image, we will take its size as the image size
                imsize = img.shape[::-1]

                # We found another good image
                numFound = numFound + 1

                if not circles:
                    # Get subpixel accuracy corners
                    corners2 = cv2.cornerSubPix(img,corners,(win,win),(-1,-1),criteria)
                    imgpoints.append(corners2)
                    print Style.BRIGHT + Back.GREEN + "\t\tfound subpixel corners"

                # Draw, display, and save the corners
                colorimg = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
                if circles:
                    colorimg = cv2.drawChessboardCorners(colorimg, (cols,rows), centers,ret)
                else:
                    colorimg = cv2.drawChessboardCorners(colorimg, (cols,rows), corners2,ret)
                if save:
                    cv2.imwrite(outdir + "/grid" + str(numFound) + ".jpg", colorimg)
                if visualize:
                    cv2.imshow('Image with Centers or Corners',colorimg)
                    cv2.waitKey(5000)
            else:
                print Style.BRIGHT + Back.RED + "\tcould not find corners or centers"
            print "\n"

    # Check how many good images we found
    if numFound >= 10:
        print Style.BRIGHT + Back.GREEN + "Found " + str(numFound) + " calibratable images."
    elif numFound == 0:
        print Style.BRIGHT + Back.RED + "Found " + str(numFound) + " calibratable images. \nNow Exiting"
        print(Style.RESET_ALL)
        exit()
    else:
        print Style.BRIGHT + Back.YELLOW + "Found " + str(numFound) + " calibratable images."

    #######################################################################
    print Style.BRIGHT + Back.CYAN + "Begining Calibration"

    # Execute calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, imsize,None,None)

    # Get the crop and optimal matrix for the image
    w,h = imsize[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))


    # Go through all images and undistort them
    print Style.BRIGHT + Back.CYAN + "Begining Undistort"
    i = 0
    for file in filenames:
        file = targetDir + file

        #Try to read in image as grayscale
        img = cv2.imread(file, 0 )

        #If the file isn't an image, move on
        if img is not None:
            print Style.BRIGHT + Back.CYAN + "undistorting image: "+file

            if visualize:
                cv2.imshow('Raw Image',img)
                cv2.waitKey(5000)

            # undistort
            dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

            # crop the image
            x,y,w,h = roi
            dst = dst[y:y+h, x:x+w]
            if save:
                cv2.imwrite(outdir + "/undistort" + str(i) + ".jpg", dst)
            if visualize:
                cv2.imshow('Undistorted Image',dst)
                cv2.waitKey(5000)

            i = i+1

    #########################################################################
    print "\n"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Intrinsic Matrix:"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + str(newcameramtx)
    print "\n"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Distortion Matrix:"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + str(dist)

    # Calculate Reprojection Error
    tot_error = 0
    for i in xrange(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        tot_error = tot_error + error
    mean_error = tot_error/len(objpoints)
    print "\n"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Reprojection Error: " + str(mean_error)

    if save:
        resulttxt = open(outdir + '\\result.txt', 'w')
        resulttxt.write("Intrinsic Matrix:\n")
        np.savetxt(resulttxt,newcameramtx,'%E')
        resulttxt.write("\n\n")
        resulttxt.write("Distortion Matrix:\n")
        np.savetxt(resulttxt,dist,'%E')
        resulttxt.write("\n\n")
        resulttxt.write("Reprojection Error:  ")
        resulttxt.write(str(mean_error))
        resulttxt.close()


    print(Style.RESET_ALL)
    cv2.destroyAllWindows()
