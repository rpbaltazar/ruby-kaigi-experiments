# import the necessary packages
import cv2

class ShapeDetector:
  def __init__(self):
    pass

  def detect(self, c):
    # initialize the shape name and approximate the contour
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    M = cv2.moments(approx)

    if int(M["m00"]) == 0:
      shape = "unidentified"

    elif len(approx) == 3:
      shape = "triangle"

    elif len(approx) == 4:
      shape = "rectangle"

    else:
      shape = "circle"

    return [shape, M]

  def findCenter(self, M):
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return [cX, cY]
