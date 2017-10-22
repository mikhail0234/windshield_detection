import math
import cv2 as cv
from drawline import *
from math import hypot

def grayscale(img):
    """
    Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    you should call plt.imshow(gray, cmap='gray')

    :param img:
    :return:
    """

    gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray



def canny(img, low_threshold, high_threshold):
    """
    Applies the Canny transform
    :param img:
    :param low_threshold:
    :param high_threshold:
    :return:
    """
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """
    Applies a Gaussian Noise kernel
    :param img:
    :param kernel_size:
    :return:
    """
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    '''
     Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.

    image :param img:
    area :param vertices:
    corrected image with certain mask :return:
    '''
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def distance(p1, p2):
    '''
    point1 :param p1:
    point2 :param p2:
    calculate distance between two points :return:
    '''
    return hypot(p1[0] - p2[0], p1[1] - p2[1])

def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    #print('draw len=',len(lines))
    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
                cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    return img


def lines_mask(lines, y_min =50, y_max=110, length=55):

    '''
    :param lines:
    :param y_min:
    :param y_max:
    :param length:
    :return:
    '''
    new_lines = []
    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            pointDistance = distance((x1, y1), (x2, y2))


            if (x2 - x1 != 0):
                b = float((x2 * y1 - x1 * y2) / (x2 - x1))
                k = (y2 - y1) / (x2 - x1)
            else:
                b = 0
                k = 0

            alpha = math.atan(k)
            if ((y_min<y1<y_max  or 50<y2<y_max+20) and pointDistance < length and math.fabs(alpha) < 0.15) :
                pass
                #print(lines[x])
            else:
                new_lines.append([x1, y1, x2, y2, k, b, alpha])
    #print('new lengtht:', len(new_lines))
    return new_lines



def draw_lines_inf(img, lines, color=[255, 0, 0], thickness=2, R = 125):

    i = 0
    for x1, y1, x2, y2, k, b, alpha in lines:

        cos = np.cos(alpha)
        sin = np.sin(alpha)

        x1 = int(x1 + (-cos) * R)
        y1 = int(y1 + (-sin) * R)


        x2 = int(x2 + (cos) * R)
        y2 = int(y2 + (sin) * R)

        cv2.line(img, (x1, y1), (x2, y2), color, thickness)

        i = i + 1

    return img

def resizeLines(lines, R = 125):
    i = 0
    for x1, y1, x2, y2, k, b, alpha in lines:
        cos = np.cos(alpha)
        sin = np.sin(alpha)

        lines[i][0] = int(x1 + (-cos) * R)
        lines[i][1] = int(y1 + (-sin) * R)

        lines[i][2] = int(x2 + (cos) * R)
        lines[i][3] = int(y2 + (sin) * R)
        i = i + 1

    return lines




def lines_analizator(img, lines):
    linesH = []
    linesL = []
    linesR = []
    for x1, y1, x2, y2, k, b, alpha in lines:
        if (math.fabs(alpha) < 0.15):
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            linesH.append([x1, y1, x2, y2, k, b, alpha])
        elif (-1.2 > alpha > -1.73): #and (x2 <= img.shape[1]/2 or x1 <= img.shape[1]/2) ):
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            linesL.append([x1, y1, x2, y2, k, b, alpha])
        elif (1.05 < alpha < 1.45): # and (x1 >= img.shape[1]/2 or x2 >= img.shape[1]/2)):
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0) ,2)
            linesR.append([x1, y1, x2, y2, k, b, alpha])
    #cv2.line(img, (int(img.shape[1]/2), 0), (int(img.shape[1]/2), 288), (0, 255, 0), 2)

    return linesH, linesL, linesR


def searchPoints(img, linesH, linesL, linesR):
    bordersH = []
    for x1, y1, x2, y2, k, b, alpha in linesH:

        value = int(k * img.shape[1]/2 + b)
        for x12, y12, x22, y22, k2, b2, alpha in linesH:
            value2 = int(k2 * img.shape[1]/2 + b2)
            if (65 < math.fabs(value - value2) < 110 and (math.fabs(k - k2) < 0.06)):
                bordersH.append([k, b, value])


    bordersLR = []
    i = 0
    inf = 9999


    # поправить на непересекаемость циклов
    for x1, y1, x2, y2, k, b, alpha in linesL:
        i = i + 1
        for x12, y12, x22, y22, k2, b2, alpha2 in linesR:
            if (0.01 < math.fabs(alpha + alpha2) < 0.34 and 120<x12-x1<250 and 120<x22-x2<280 ):
                #if (math.isnan(k * 0 + b) != True and math.isnan(k * 384 + b) != True and math.isnan(
                                #k2 * 0 + b2) != True and math.isnan(k2 * 384 + b2) != True):
                #cv2.line(img,(x1, y1),(x2, y2),(255,0,0) ,2)
                #cv2.line(img, (x12, y12), (x22, y22), (255, 0, 0), 2)
                    # cv2.line(img,(0,int(k2 * 0 + b2)),(384, int(k2 * 384 + b2)),(255,255,0) ,2)

                #print('k = ',k)
                if(-inf <k<inf):
                    value = (80 - b) / k
                else:
                    value = (80 - b)
                value2 = (80 - b2) / k2
                bordersLR.append([k, b, value])
                bordersLR.append([k2, b2, value2])

    #print('Left/Right borders len = ', len(bordersLR))
    #print('Horizontal borders len =',len(bordersH))
    top = 0
    down = 288
    if len(bordersH) > 1:
        for k, b, value in bordersH:
            if (value < 80 and value > top):
                top = value
                topk = k
                topb = b
            if (value > 80 and value < down):
                down = value
                downk = k
                downb = b
        #value11 = int(topk * 0 + topb)
        #value12 = int(topk * 384 + topb)
        #value21 = int(downk * 0 + downb)
        #value22 = int(downk * 384 + downb)

        #cv2.line(img, (0, value11), (384, value12), (255, 0, 255), 2)
        #cv2.line(img, (0, value21), (384, value22), (255, 0, 255), 2)
    else:
        print("Error with amount of top/down elements")




    if len(bordersLR) > 1 and len(bordersH) > 1:
        left = -100
        right = 400
        for k, b, value in bordersLR:
            #print('value = ',value)
            if (value <= img.shape[1]/2 and value >= left):
                left = value
                leftk = k
                leftb = b

            if (value > img.shape[1]/2 and value < right):
                right = value
                rightk = k
                rightb = b

        #print('left = ', left)
        #print('right = ', right)

        if(left != -100 and right != 400 and top !=0 and down != 288):
            value11 = int(leftb)
            value12 = int(leftk * 384 + leftb)
            value21 = int(rightb)
            value22 = int(rightk * 384 + rightb)

            #cv2.line(img, (0, value11), (384, value12), (255, 0, 255), 2)
            #cv2.line(img, (0, value21), (384, value22), (255, 0, 255), 2)

            pts = []
            pts.append(intersection(leftk, leftb, topk, topb))
            pts.append(intersection(rightk, rightb, topk, topb))
            pts.append(intersection(rightk, rightb, downk, downb))
            pts.append(intersection(leftk, leftb, downk, downb))
        else:
            return img


            #print(rect)


            #cv2.line(img, (x1, y1), (x1+2, y1), (255, 0, 0), 5)
            #cv2.line(img, (x2, y2), (x2 + 2, y2), (255, 0, 0), 5)
            #cv2.line(img, (x3, y3), (x3 + 2, y3), (255, 0, 0), 5)
            #cv2.line(img, (x4, y4), (x4 + 2, y4), (255, 0, 0), 5)

        #return img
        return four_point_transform(img, pts)


    else:
        return img
        print("Error with amount of left/right borders")

    #return bordersH, bordersL, bordersR


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    #print(tl, tr, br, bl)

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    #cv2.line(warped, (0, 3), (384, 5), (255, 0, 255), 1)
    #cv2.line(warped, (0, 37), (384, 35), (255, 0, 255), 1)

    #cv2.line(warped, (20, warped.shape[0]//2-20 ), (288, warped.shape[0]//+20), (255, 0, 255), 1)

    #cv2.line(warped, (int(warped.shape[1]/2), 0), (int(warped.shape[1]/2), 288),(255, 0, 0), 2)

    # return the warped image
    return warped


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    rect[0] = pts[0]
    rect[2] = pts[2]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[1]
    rect[3] = pts[3]

    # return the ordered coordinates
    return rect


def intersection(k1, b1, k2, b2):
    x = int(round((b2-b1)/(k1-k2)))
    y = int(round(k1*x+b1))

    return [x,y]
