import cv2 as cv
import numpy as np
import change
import process
import time
import calculate
import test
t1=time.time()

img_patch= "img"
test_path = "test_set"
old= "test_set_o"

test.test('img/3.png',10,0)
#test.test_file(test_path,10)


cv.waitKey(0)
cv.destroyAllWindows()


t2=time.time()

print("time: " + str((t2-t1)))