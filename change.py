import cv2 as cv
import numpy as np


def input(imgName, high=400, width=300):
    img = cv.imread(imgName)

    img = cv.resize(img, (high, width))
    return img


def erosion(img, ker):
    kernel = np.ones((ker, ker), np.uint8)
    er = cv.erode(img, kernel, iterations=1)
    return er


def dilation(img, ker):
    kernel = np.ones((ker, ker), np.uint8)
    di = cv.dilate(img, kernel, iterations=1)
    return di


def opening(img, ker):
    kernel = np.ones((ker, ker), np.uint8)
    op = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
    return op


def closing(img, ker):
    kernel = np.ones((ker, ker), np.uint8)
    cl = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
    return cl


def zooming(img, ker=10):
    cl = closing(img, ker)
    zo = opening(cl, ker)
    return zo


def zoomed_list(list1, n):
    list2 = []
    for x in list1:
        list2.append(zooming(x, n))
    return list2
# 把list1中的图像zoom to list2,kernel=n
