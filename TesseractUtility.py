import os
import cv2
import numpy as np
from PIL import Image
import pytesseract as tesseract

tesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

configTitleAndMainStat = '-l eng --oem 1 --psm 7'
configSubStats = '-l eng --oem 1 --psm 6'
kernel = np.ones((1, 1), np.uint8)


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def GetRuneTitle(titleSnippet, showTesseractInputImage=False, printOutputText=False):
    (thresh, snippet) = cv2.threshold(titleSnippet, 100, 255, cv2.THRESH_BINARY)
    snippet = adjust_gamma(snippet, gamma=0.70)
    snippet = cv2.erode(snippet, kernel, iterations=40)

    text = tesseract.image_to_string(snippet, config=configTitleAndMainStat)
    if printOutputText:
        print(text)
    if showTesseractInputImage:
        cv2.imshow("Title", snippet)
        cv2.waitKey(1)
    return text


def GetRuneMainStat(mainStatSnippet, showTesseractInputImage=False, printOutputText=False):
    snippetHeight, snippetWidth = mainStatSnippet.shape
    snippetAsImage = Image.fromarray(mainStatSnippet)
    resizedSnippetAsImage = snippetAsImage.resize((snippetWidth * 2, snippetHeight * 2))
    resizedSnippet = np.asarray(resizedSnippetAsImage)

    (thresh, resizedSnippet) = cv2.threshold(resizedSnippet, 150, 255, cv2.THRESH_BINARY)
    resizedSnippet = cv2.erode(resizedSnippet, kernel, iterations=10)

    text = tesseract.image_to_string(resizedSnippet, config=configTitleAndMainStat)
    if printOutputText:
        print(text)
    if showTesseractInputImage:
        cv2.imshow("Main stat", resizedSnippet)
        cv2.waitKey(1)
    return text


def GetRuneSubStats(subStatsSnippet, showTesseractInputImage=False, printOutputText=False):
    snippetHeight, snippetWidth = subStatsSnippet.shape
    snippetAsImage = Image.fromarray(subStatsSnippet)
    resizedSnippetAsImage = snippetAsImage.resize((snippetWidth * 3, snippetHeight * 3))
    resizedSnippet = np.asarray(resizedSnippetAsImage)

    (thresh, resizedSnippet) = cv2.threshold(resizedSnippet, 120, 255, cv2.THRESH_BINARY)
    resizedSnippet = cv2.erode(resizedSnippet, kernel, iterations=20)

    text = tesseract.image_to_string(resizedSnippet, config=configSubStats)
    text = os.linesep.join([line for line in text.splitlines() if line.strip()])
    if printOutputText:
        print(text)
    if showTesseractInputImage:
        cv2.imshow("Sub stats", resizedSnippet)
        cv2.waitKey(1)
    return text
