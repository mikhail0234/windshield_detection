import cv2

import numpy as np
from help import draw_lines, draw_lines_inf, lines_mask


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap, line_type = 0):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                            min_line_len, max_line_gap)
    # print("Hough lines: ", lines)
    line_img = np.zeros(img.shape, dtype=np.uint8)
    return lines

def my_hough(img, line_type = 1):
    # Hough lines
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 30  # minimum number of votes (intersections in Hough grid cell)
    min_line_len = 35  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments
    lines_image = hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap, line_type)
    return lines_image

def my_hough_mask(img):
    lines = my_hough(img)
    #print ('ne mask ',len(lines))
    return lines_mask(lines)