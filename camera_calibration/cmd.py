#!/usr/bin/env python

import camera_calibration
import argparse


def main():
    #Parse in arguments
    parser = argparse.ArgumentParser(description='Calibrate Images', epilog="This software is designed to calibrate a camera based on images fed in from a folder. Images should be of a grid of white and black squares. It works best if there is a white border around the grid and if the number of columns and rows is different. This can work with any camera, just put the calibration images in a folder and run this script. For best results you need atleast calibratable images.")

    parser.add_argument("--dir", metavar="directory", type = str , help='The directory of images to calibrate off of.', default = "\\")

    parser.add_argument("-s","--spacing", type = float, help = "The grid spacing in mm." , required = True)

    parser.add_argument("-c","--columns",type = int , help = "the number of inner corners horizontally", required = True)

    parser.add_argument("-r","--rows",type = int , help = "the number of inner corners vertically", required = True)

    parser.add_argument("-w","--window",type = int , help = "The size of the window to use for subpixel localization of the corners", default = 11)

    parser.add_argument("--save", help = "Whether to save image output", action = 'store_true')

    parser.add_argument("--outdir",type = str , help = "Where to save image output", default = "output")

    parser.add_argument("-v", "--visualize", help = "Whether to show visualizations", action = 'store_true')

    args = parser.parse_args()

    camera_calibration.calibrate(
    rows = args.rows,
    cols = args.columns,
    win = args.window,
    save = args.save,
    outdir = args.outdir,
    space = args.spacing,
    visualize = args.visualize,
    dir = args.dir)
