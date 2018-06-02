# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from worldmapper.continentdetector import ContinentDetector
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
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if imutils.is_cv2() else cnts[1]

sd = ShapeDetector()
cd = ContinentDetector()

for rect in cd.continents.values():
  cv2.rectangle(image, rect.topleft, rect.bottomright, (0, 255, 0), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)

# loop over the contours
count = 0
countriesCount = {}
for c in cnts:
  shape, M = sd.detect(c)
  if (shape != "circle" or int(M["m00"]) < 10):
    continue

  cX, cY = sd.findCenter(M)

  # draw the contour and center of the shape on the image
  cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
  cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

  # Hacky fix for big junction of spots
  increment = 1
  if M["m00"] > 300:
    increment = int(M["m00"] / 200)

  coords = { 'x': cX, 'y': cY }
  continent = cd.detect(coords)

  if continent == "invalid":
    print("Not found")
    print(coords)
  else:
    countriesCount.setdefault(continent, 0)
    countriesCount[continent] += increment

  count += increment

# show the image
cv2.imshow("Image", image)
cv2.waitKey(0)

print(count)
print(countriesCount)
