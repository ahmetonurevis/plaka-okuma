import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('D:\\python\\plaka_okuma\\plaka.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
filtered = cv2.bilateralFilter(gray, 6, 250, 250)
edged = cv2.Canny(filtered, 30, 200)

contours = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(contours)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
screen = None

for c in cnts:
    epsilon = 0.018 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    if len(approx) == 4:
        screen = approx
        break

mask = np.zeros(gray.shape, np.uint8)
new_img = cv2.drawContours(mask, [screen], 0, (255, 255, 255), -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
print(np.where(mask == 255))
cv2.imshow("mask", cropped)

text = pytesseract.image_to_string(cropped, lang='eng')
print("plaka: ", text)

cv2.waitKey(0)
cv2.destroyAllWindows()
