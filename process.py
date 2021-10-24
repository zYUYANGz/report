import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import change


def binarization(img):
    # blur the image (to reduce false-positive detections) and then
    #  perform edge detection
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    blurred = cv.GaussianBlur(gray, (3, 3), 1)
    # Image binarization using the Otsu algorithm for local thresholding
    dst = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 21, 3)
    # int blockSize(101) is related to the size of the image
    # return gray
    return dst
#使用局部阈值的大津算法进行图像二值化
#这个参数和图片大小有关 https://www.cnblogs.com/pacino12134/p/11429379.html

def get_edge(img):
    bin = binarization(img)
    # cv.imshow("bin",bin)
    edged = cv.Canny(bin, 50, 300)
    return edged


# 获取img的每一个部分的轮廓返回部分数量，并将每个部分保存到list1中，将轮廓保存到list2中
#Get the outline of each part of img to return the number of parts
# and save each part to list1 and the outline to list2
def get_contours_list(img, list1=[], list2=[]):
    edged = get_edge(img)
    cnts, x = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)
    total = 0
    # loop over the contours one by one
    for c in cnts:
        # if the contour area is small, then the area is likely noise, so
        # we should ignore the contour
        if cv.contourArea(c) < 25:
            continue

        # otherwise, draw the contour on the image and increment the total
        # number of shapes found

        list1.append(fill_cont(c))
        # list2 return contours
        list2.append(c)

        total += 1
    return total


# 返回contours的边缘
def get_contours(img):
    edged = get_edge(img)
    cnts, x = cv.findContours(edged.copy(), cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)
    return cnts[0]


def fill_cont(cont):
    img = change.input('0.png')
    cv.drawContours(img, [cont], -1, (0, 0, 0), -1)
    return img


def show_list(list, name):
    for i, x in enumerate(list):
        plt.subplot(1, len(list), i + 1)
        plt.title(name + str(i + 1))
        plt.imshow(x)
    plt.show()


def show_list_other(list, name):
    for i, x in enumerate(list):
        plt.subplot(1, len(list), i + 1)
        plt.title(name + str(i + 1))
        plt.imshow(x[1])
    plt.show()


def draw_cont(list):
    blank = change.input("0.png")
    for x in list:
        cv.drawContours(blank, [x], -1, (0, 0, 0), -1)
    return blank
