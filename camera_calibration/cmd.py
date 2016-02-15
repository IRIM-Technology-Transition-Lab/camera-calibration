"""Commandline entry point to camera calibration script.

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

import camera_calibration
import argparse


def main():
    # Parse in arguments
    parser = argparse.ArgumentParser(
        description='Calibrate Images',
        epilog="This software is designed to calibrate a camera based on images"
               " fed in from a folder. Images should be of a grid of white and"
               " black squares. It works best if there is a white border around"
               " the grid and if the number of columns and rows is different. "
               "This can work with any camera, just put the calibration images"
               " in a folder and run this script. For best results you need"
               " at least calibratable images.")

    parser.add_argument("--dir", metavar="directory", type=str,
                        help='The directory of images to calibrate off of.',
                        default="\\")

    parser.add_argument("-s", "--spacing", type=float,
                        help="The grid spacing in mm.", required=True)

    parser.add_argument("-c", "--columns", type=int,
                        help="the number of inner corners horizontally",
                        required=True)

    parser.add_argument("-r", "--rows", type=int,
                        help="the number of inner corners vertically",
                        required=True)

    parser.add_argument("-w", "--window", type=int,
                        help="The size of the window to use for sub-pixel "
                             "localization of the corners", default=11)

    parser.add_argument("--save", help="Whether to save image output",
                        action='store_true')

    parser.add_argument("--outdir", type=str, help="Where to save image output",
                        default="output")

    parser.add_argument("-v", "--visualize",
                        help="Whether to show visualizations",
                        action='store_true')

    args = parser.parse_args()

    camera_calibration.calibrate(
        rows=args.rows,
        cols=args.columns,
        win=args.window,
        save=args.save,
        directory_out=args.outdir,
        space=args.spacing,
        visualize=args.visualize,
        directory=args.dir)
