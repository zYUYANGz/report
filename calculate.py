import itertools

import cv2 as cv
import numpy as np
import change
import process


# 把img画到target上
def add(target, img):
    m = process.get_contours(img)
    cv.drawContours(target, [m], -1, (0, 0, 0), -1)
    return target


# 批量画到target上
def add_list(target, list):
    for x in list:
        add(target, x)
    return target


# 画到空白上
def add_blank(img):
    blank = change.input('0.png', 400, 300)
    add(blank, img)
    return blank


# 批量画到空白上
def add_blank_list(list):
    blank = change.input('0.png', 400, 300)
    add_list(blank, list)
    return blank


def similarity(img1, img2):
    cnt1 = process.get_contours(img1)
    cnt2 = process.get_contours(img2)

    return cv.matchShapes(cnt1, cnt2, 3, 0.0)


def combination(img, img2):
    list1 = []
    f = 0
    # print(process.get_contours_list(img, list1))
    if (process.get_contours_list(img, list1)) > 1:

        for x in list1:

            if (similarity(x, img2)) > 0.09:
                f = f + 1

    if f > 0:
        return False

    return True


def merge(merge1, zoom):
    i = len(merge1)
    result = []
    combol1 = []
    combol2 = []

    while i > 0:
        for x in itertools.combinations(merge1, i):
            combol1.clear()
            combol2.clear()
            for y in x:
                combol1.append(y[0] + 1)
                combol2.append(y[2])

            img = process.draw_cont(combol2)
            img_zoomed = change.zooming(img)
            # print(combol1)

            for n, z in enumerate(zoom):

                s = similarity(img_zoomed, z)
                # cv.imshow(str(combol1) + str(n), img_zoomed)
                # .imshow("z" + str(combol1) + str(n), z)
                # print(s)

                if s < 0.09:
                    # print(s)
                    if combination(img_zoomed, z):
                        # print(s)
                        # cv.imshow(str(combol1) + str(n), img_zoomed)
                        # cv.imshow("z" + str(combol1) + str(n), z)
                        cv.waitKey(0)
                        cv.destroyAllWindows()
                        # lista=[combol1,[n+1]]
                        for a in combol1:
                            lista = [[a], [n + 1]]
                            result.append(lista)
                        # print(lista)

        i = i - 1
    # print("m1", result)
    for m in result:
        for n in result:

            if (m is not n and m[1] == n[1]):
                tm = m[0] + n[0]
                m[0] = tm
                result.remove(n)

    # print("m2", result)
    return result


def split(split, zoom):
    # split是二维列表每个子列表包含[序号，img，zoom后的img的列表,cont]
    list = []
    split_list = []
    com = []
    for x in split:

        # 使用zoom后的img与zoom列表进行对比，若相同则将符合的zoom中的序号放入zoom_list
        # 然后将split的序号和zoomlist组合后添加到list中
        # x[2]即是zoom后产出的的列表
        # process.show_list(x[2],"x[2]")
        # process.show_list(zoom,"zoom!")

        zoom_list = []
        for y in x[2]:

            for i, z in enumerate(zoom):
                # 显示对比中的两个img
                # cv.imshow(str(i),y)
                # cv.imshow(str(i)+"_zoomed",z)
                # cv.waitKey(0)
                # cv.destroyAllWindows()

                if similarity(y, z) < 0.1:
                    # 显示相似度
                    # print(similarity(y,z))
                    zoom_list.append(i + 1)
                    # 加入的img的id
                    # print(zoom_list)
        if zoom_list:
            split_list.extend([[x[0] + 1], zoom_list])
        for c in x[3]:
            # print(x[0])
            tem = [x[0] + 1, c]
            com.append(tem)

    list.append(split_list)
    num_piece = 0
    for l in list:
        if l != []:
            num_piece = num_piece + len(l[1])

    if len(list) < len(split) or num_piece < (2 * len(split)):
        # print(com[0][0])
        list.extend(complicated(com, zoom))
        # list=list+complicated(com,zoom)
    # print("s", list)

    return list


def complicated(com, zoom):
    i = len(com)
    combol1 = []
    combol2 = []
    result = []

    while i > 0:
        for x in itertools.combinations(com, i):
            combol1.clear()
            combol2.clear()
            for y in x:
                # print(y[0])
                combol1.append(y[0])

                combol2.append(y[1])
            # print(combol1)
            ID = sorted(list(set(combol1)))

            img = process.draw_cont(combol2)
            img_zoomed = change.zooming(img)

            for n, z in enumerate(zoom):

                s = similarity(img_zoomed, z)
                # print(ID)
                # cv.imshow(str(combol1), img_zoomed)
                # cv.imshow(str(combol1) + "zoom", z)
                if (s) < 0.1:
                    if combination(img_zoomed, z):
                        # print(ID)
                        # print(s)
                        # cv.imshow(str(combol1), img_zoomed)
                        # cv.imshow(str(combol1) + "zoom", z)
                        result.append([ID, [n + 1]])
                        # for l in ID:

                        # result.append([[l], [n + 1]])

        i = i - 1
        cv.waitKey(0)
        cv.destroyAllWindows()
    # print("c",result)
    return result


def genDescription(img, kernel=10, method=0):
    # list1存img的每个部分
    split_list = []
    merge_list = []
    list1 = []
    # zoom_list存zoom的每个部分
    zoom_list = []

    # zoom img
    zoom = change.zooming(img, kernel)
    if method == 1:
        cv.imshow("detailed", img)
        cv.imshow("zoomed", zoom)

    # 返回img 中每个部分的img格式存在list中
    num_d = process.get_contours_list(img, list1)
    # 返回zoom 中每个部分的img格式存在zoom_list中
    num_z = process.get_contours_list(zoom, zoom_list)

    process.show_list(list1, "detailed_list")
    process.show_list(zoom_list, "zoomed_list")
    # 遍历list 判断每个部分再次zoom后是否会分裂，若分裂则存入split否则存入merge
    # (有问题如果一个图形即分裂又合并)目前只能吧所有的图形都丢进merge
    for i, x in enumerate(list1):
        # sp.clear()
        sp = []
        cont = []
        if process.get_contours_list(change.zooming(x, 10), sp, cont) > 1:
            t1 = [i, x, sp, cont]
            split_list.append(t1)

        # else:

        # print("cont:")
        # print(type(cont[0]))
        if cont:
            t2 = [i, x, cont[0]]
            merge_list.append(t2)
    # process.show_list_other(split_list,"split")
    # print("merge:" + str(len(merge_list)))
    # print("split:" + str(len(split_list)))
    x = merge(merge_list, zoom_list)
    y = split(split_list, zoom_list)
    result = x + y
    result = [i for i in result if i != []]
    tem_list = []
    for e in result:
        tem_list.append(e[0])
    # print("o",result)

    result = simplify(result, num_d)
    translator(result, num_d, num_z)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return result


def simplify(list, n):
    # print("list:")
    # print(list)
    newlist = []
    # for x in range(n):
    # newlist.append([[x + 1], []])
    for x in list:
        a = 0
        for y in newlist:

            if x[0] == y[0]:

                a = a + 1
                for i in x[1]:
                    if i not in y[1]:
                        y[1].append(i)
        if a == 0:
            newlist.append(x)

        for z in newlist:

            if x[1] == z[1]:
                n = 0
                for i in x[0]:
                    if i not in z[0]:
                        n = n + 1
                if n == 0:
                    if x != z:
                        # print("x",x)
                        # print("z",z)
                        if x in newlist:
                            # print(x)
                            newlist.remove(x)
    tem = []
    for a in range(len(newlist)):
        for b in range(len(newlist) - a):
            if a is not b:
                for a1 in newlist[a][0]:
                    # print("a",a1)
                    if a1 in newlist[b][0]:
                        if a1 != b + 1:
                            tem = [a1, b + 1]
                            # print("a1",newlist[a][1])
                            # print("b", newlist[b][1])
                            # print([[a1+1],tem])
                            # print(newlist[a])
                            # print(newlist[b])
                            newlist.append([[a1], tem])
                            del newlist[a]

    return newlist


def changing(list1, list2):
    result = []
    detailed = []
    zoomed = []
    detailed1 = []
    zoomed1 = []
    detailed2 = []
    zoomed2 = []
    for x in list1:
        detailed1.append(x[0])
        zoomed1.append(x[1])

    for y in list2:
        detailed2.append(y[0])
        zoomed2.append(y[1])

    detailed.append(Deduplication(detailed1))
    zoomed.append(Deduplication(zoomed1))
    detailed.append(Deduplication(detailed2))
    zoomed.append(Deduplication(zoomed2))
    result.append(detailed)
    result.append(zoomed)

    for i, a in enumerate(result):
        if a[0] == a[1]:
            min = []
            for b in a[0]:
                min.append([[b], [b]])

            result[i] = min

    return result


def Deduplication(list1):
    newlist1 = []
    newlist2 = []
    for x in list1:

        for y in x:
            if isinstance(y, list):
                for z in y:
                    newlist2.append(z)

                x = sorted(list(set(newlist2)))
        newlist2.clear()

        newlist1.extend(x)

    # return newlist1
    return sorted(list(set(newlist1)))


def changDescription(img1, img2):
    a = genDescription(img1)
    b = genDescription(img2)
    result = changing(a, b)
    return result


def translator(description, d, z):
    state = 0
    if description == []:
        print("there is nothing at detailed level ")
    else:

        if d > 1:
            print("there are {n} pieces in detailed level".format(n=d))
        else:
            print("there is {n} piece in detailed level".format(n=d))
        if z > 1:
            print("there are {n} pieces in zoomed level".format(n=z))
        else:
            print("there is {n} piece in zoomed level".format(n=z))

        for x in description:
            if len(x[0]) > 1 and len(x[1]) == 1:
                state = 1
            if len(x[0]) == 1 and len(x[1]) > 1:
                state = 2
            if len(x[0]) == 1 and x[1] == []:
                state = 3
            if x[0] == x[1]:
                state = 4
            if state == 1:
                print("pieces ", end='')
            for y in range(len(x[0])):
                if y == (len(x[0]) - 1):
                    if state == 1:
                        print("and {element} at detailed level ".format(element=x[0][y]), end='')
                    if state == 2 or state == 3 or state == 4:
                        print("piece {element} at detailed level ".format(element=x[0][y]), end='')
                else:
                    print("{element},".format(element=x[0][y]), end='')

            if state == 1:
                print("are separated by a narrow gap,they are close")
                print("because they merge to ", end='')
            if state == 2:
                print("is made up of two parts joined by narrow channel")
                print("because it split to ", end='')
            if state == 3:
                print("disappears at zoomed level")
                continue
            if state == 4:
                print("is no change")
                continue
            for z in range(len(x[1])):
                if z == (len(x[1]) - 1):
                    if state == 1:
                        print("{element} at zoomed level ".format(element=x[1][z]))
                    if state == 2:
                        print("and {element} at zoomed level ".format(element=x[1][z]))
                else:
                    print("{element},".format(element=x[1][z]), end='')
