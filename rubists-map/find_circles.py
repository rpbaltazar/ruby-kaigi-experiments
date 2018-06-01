# import the necessary packages
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
count = 0
for c in cnts:
  # compute the center of the contour
  perimeter = cv2.arcLength(c, True)
  approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

  M = cv2.moments(approx)

  if int(M["m00"]) == 0:
    continue

  # 4 edges is a rectangle, so ignore
  if len(approx) == 4:
    continue

  if M["m00"] < 30:
    continue

  cX = int(M["m10"] / M["m00"])
  cY = int(M["m01"] / M["m00"])

  # draw the contour and center of the shape on the image
  cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
  cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

  # Hacky fix for big junction of spots
  if M["m00"] > 300:
    count += 2
  else:
    count += 1

# show the image
  cv2.imshow("Image", image)
  cv2.waitKey(0)

print(count)
