"""A script to calibrate a camera based on stored images of a checkerboard.

Based on example at: http://opencv-python-tutroals.readthedocs.org/en/latest/
                     py_tutorials/py_calib3d/py_calibration/py_calibration.html

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
"""

import os
import numpy as np
import cv2
from colorama import init, Fore, Back, Style
import json
import datetime


def calibrate(directory, rows, cols, win, save, directory_out, space,
              visualize, circles):
    """Calibrate a camera based on the images in directory

    If save is set, then the resulting data (as txt and json files), along with
    undistorted versions of the input images will be saved to directory_out.
    The system only works in rows != cols. Most instructions will be printed to
    the terminal during execution.

    Args:
        directory (str): Where are the images stored
        rows (int): The number of internal corners in the vertical direction
        cols (int): The number of internal corners in the horizontal direction
        win (int): Half of the side length of the search window for subpixel
            accuracy corner detection. For example, if win=5, then a
            5*2+1 x 5*2+1 = 11 x 11 search window is used.
        save (bool): Whether to save output
        directory_out (str): Where to save output
        space (float): The spacing between squares on the grid.
        visualize (bool): Whether to visualize output as the script is running.
        circles (cir): Whether to use a circle calibration grid
    """
    # Based on example at:
    # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

    # Setup colored output
    init()

    if len(directory_out) and (directory_out[0] == '/' or directory_out[0] == '\\'):
        directory_out = directory_out[1:]
    if len(directory_out) and (directory_out[-1] == '/' or directory_out[-1] == '\\'):
        directory_out = directory_out[:-1]

    if len(directory) and (directory[0] == '/' or directory[0] == '\\'):
        directory = directory[1:]
    if len(directory) and (directory[-1] == '/' or directory[-1] == '\\'):
        directory = directory[:-1]

    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "\nWelcome\n"

    # Figure out where the images are and get all file_names for that directory
    target_directory = os.path.join(os.getcwd(), directory)
    directory_out = os.path.join(os.getcwd(), directory_out)
    print "Searching for images in: " + target_directory
    file_names = os.listdir(target_directory)
    print "Found Images:"
    for name in file_names:
        print "\t" + name

    if visualize:
        print ("\nYou have enabled visualizations.\n\tEach visualization will "
               "pause the software for 5 seconds.\n\tTo continue prior to the "
               "5 second time, press any key.")

    # Check grid symmetry
    if rows == cols:
        print (Style.BRIGHT + Back.RED + "It is best to use an asymmetric grid,"
                                         " rows and cols should be different")
        print(Style.RESET_ALL)
        exit()

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    object_point = np.zeros((cols * rows, 3), np.float32)
    object_point[:, :2] = np.mgrid[0:(rows * space):space, 0:(cols * space):space].T.reshape(-1, 2)

    number_found = 0  # How many good images are there?

    # Arrays to store object points and image points from all the images.
    object_points = []  # 3d point in real world space
    image_points = []  # 2d points in image plane.

    # termination criteria for the sub-pixel corner search algorithm
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
        print (Style.BRIGHT + Back.MAGENTA + "\nSaving output to: " +
               directory_out)
        if not os.path.exists(directory_out):
            os.makedirs(directory_out)
            print Style.BRIGHT + Back.GREEN + "\tMade a new output directory"
        print "\n"

    #########################################################################
    image_size = None
    for image_file in file_names:
        image_file = os.path.join(target_directory, image_file)

        # Try to read in image as gray scale
        img = cv2.imread(image_file, 0)

        # If the image_file isn't an image, move on
        if img is not None:
            print Style.BRIGHT + Back.CYAN + "searching image: " + image_file

            if visualize:
                cv2.imshow('Raw Image', img)
                cv2.waitKey(5000)

            if circles:
                # Find circle centers.
                re_projection_error, centers = cv2.findCirclesGrid(img, (rows, cols))
            else:
                # Find chessboard corners. 9: cv2.CALIB_CB_FAST_CHECK +
                # cv2.CV_CALIB_CB_ADAPTIVE_THRESH
                re_projection_error, corners = cv2.findChessboardCorners(
                    img, (rows, cols), 9)

            # If we found chessboard corners lets work on them
            if re_projection_error:
                print Style.BRIGHT + Back.GREEN + "\tfound corners or centers"
                object_points.append(object_point)

                # Since this is a good image, we will take its size as the
                # image size
                image_size = img.shape[::-1]

                # We found another good image
                number_found += 1

                if circles:

                    image_points.append(centers)

                    # Draw, display, and save the corners
                    color_image = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

                    new_color_image = cv2.drawChessboardCorners(color_image,
                                                                (cols, rows),
                                                                centers,
                                                                re_projection_error)
                    # OpenCV 2 vs 3
                    if new_color_image is not None:
                        color_image = new_color_image
                else:
                    # Get subpixel accuracy corners
                    corners2 = cv2.cornerSubPix(img, corners, (win, win), (-1, -1),
                                                criteria)

                    # Draw, display, and save the corners
                    color_image = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

                    # depending on the version of OpenCV, cv2.cornerSubPix may
                    # return none, in which case, it modified corners (how
                    # un-Pythonic)
                    if corners2 is None:
                        corners2 = corners

                    image_points.append(corners2)
                    print (Style.BRIGHT + Back.GREEN +
                           "\t\tfound sub-pixel corners")
                    new_color_image = cv2.drawChessboardCorners(color_image,
                                                                (cols, rows),
                                                                corners2,
                                                                re_projection_error)
                    # OpenCV 2 vs 3
                    if new_color_image is not None:
                        color_image = new_color_image

                if save:
                    cv2.imwrite(os.path.join(directory_out, "grid" +
                                             str(number_found) + ".jpg"),
                                color_image)
                if visualize:
                    cv2.imshow('Image with Centers or Corners', color_image)
                    cv2.waitKey(5000)
            else:
                print Style.BRIGHT + Back.RED + "\tcould not find corners or centers"
            print "\n"

    # Check how many good images we found
    if number_found >= 10:
        print (Style.BRIGHT + Back.GREEN + "Found " + str(number_found) +
               " calibratable images.")
    elif number_found == 0:
        print (Style.BRIGHT + Back.RED + "Found " + str(number_found) +
               " calibratable images. \nNow Exiting")
        print(Style.RESET_ALL)
        exit()
    else:
        print (Style.BRIGHT + Back.YELLOW + "Found " + str(number_found) +
               " calibratable images.")

    #######################################################################
    print Style.BRIGHT + Back.CYAN + "Beginning Calibration"

    # Execute calibration
    (re_projection_error, camera_matrix, distortion_coefficients,
     rotation_vectors, translation_vectors) = \
        cv2.calibrateCamera(object_points, image_points, image_size, None, None)

    # Get the crop and optimal matrix for the image
    w, h = image_size[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, distortion_coefficients, (w, h), 1, (w, h))

    # Go through all images and undistort them
    print Style.BRIGHT + Back.CYAN + "Beginning Undistort"
    i = 0
    for image_file in file_names:
        image_file = os.path.join(target_directory, image_file)

        # Try to read in image as gray scale
        img = cv2.imread(image_file, 0)

        # If the image_file isn't an image, move on
        if img is not None:
            print Style.BRIGHT + Back.CYAN + "undistorting image: " + image_file

            if visualize:
                cv2.imshow('Raw Image', img)
                cv2.waitKey(5000)

            # undistort
            dst = cv2.undistort(img, camera_matrix, distortion_coefficients,
                                None, new_camera_matrix)

            # crop the image
            x, y, w, h = roi
            dst = dst[y:y + h, x:x + w]
            if save:
                cv2.imwrite(os.path.join(directory_out, "undistort" + str(i) +
                                         ".jpg"), dst)
            if visualize:
                cv2.imshow('Undistorted Image', dst)
                cv2.waitKey(5000)

            i += 1

    #########################################################################
    print "\n"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Intrinsic Matrix:"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + str(camera_matrix)
    print "\n"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Distortion Matrix:"
    print (Fore.WHITE + Style.BRIGHT + Back.MAGENTA +
           str(distortion_coefficients))
    print "\n"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Optimal Camera Matrix:"
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + str(new_camera_matrix)
    print "\n"
    print (Fore.WHITE + Style.BRIGHT + Back.MAGENTA +
           "Optimal Camera Matrix Crop:")
    print Fore.WHITE + Style.BRIGHT + Back.MAGENTA + str(roi)

    # Calculate Re-projection Error
    tot_error = 0
    for i in xrange(len(object_points)):
        image_points_2, _ = cv2.projectPoints(
            object_points[i], rotation_vectors[i], translation_vectors[i],
            camera_matrix, distortion_coefficients)
        error = cv2.norm(image_points[i], image_points_2,
                         cv2.NORM_L2) / len(image_points_2)
        tot_error += error
    mean_error = tot_error / len(object_points)
    print "\n"
    print (Fore.WHITE + Style.BRIGHT + Back.MAGENTA + "Re-projection Error: " +
           str(mean_error))

    if save:
        with open(os.path.join(directory_out, 'result.txt'), 'w') as \
                result_text_file:
            result_text_file.write("Grid: Rows: {}, Cols: {}, Spacing: {}:\n"
                                   .format(rows, cols, space))
            result_text_file.write("Time: {}\n".format(datetime.datetime.now()))
            result_text_file.write("Intrinsic Matrix:\n")
            np.savetxt(result_text_file, camera_matrix, '%E')
            result_text_file.write("\n\n")
            result_text_file.write("Distortion Matrix:\n")
            np.savetxt(result_text_file, distortion_coefficients, '%E')
            result_text_file.write("\n\n")
            result_text_file.write("Optimal Camera Matrix:\n")
            np.savetxt(result_text_file, new_camera_matrix, '%E')
            result_text_file.write("\n\n")
            result_text_file.write("Optimal Camera Matrix Crop:\n")
            np.savetxt(result_text_file, roi, '%i')
            result_text_file.write("\n\n")
            result_text_file.write("Re-projection Error:  ")
            result_text_file.write(str(mean_error))

        json_dict = {"grid": {"rows": rows,
                              "cols": cols,
                              "spacing": space},
                     "time": str(datetime.datetime.now()),
                     "intrinsic": camera_matrix.tolist(),
                     "distortion": distortion_coefficients.tolist(),
                     "optimal": new_camera_matrix.tolist(),
                     "crop": roi,
                     "error": mean_error}
        with open(os.path.join(directory_out, 'result.json'), 'w') as \
                result_json_file:
            json.dump(json_dict, result_json_file, indent=4)

    print(Style.RESET_ALL)
    cv2.destroyAllWindows()
