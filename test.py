import itertools
import os

import cv2 as cv
import numpy as np
# import imutils
import change
import process
import calculate


def test(name, kernel=10,mode=0):
    try:
        a = change.input(name)
    except cv.error:
        print("Incorrect input format or empty input!")
    else:
        print(calculate.genDescription(a, kernel,mode))


def test_file(filename, kernel=10,mode=0):
    files = os.listdir(filename)

    for x in files:
        print(x + ":")
        s = filename + '/' + x
        try:
            a = change.input(s)
        except cv.error:
            print("Incorrect input format or empty input!")
        else:
            print(calculate.genDescription(a, kernel,mode))
