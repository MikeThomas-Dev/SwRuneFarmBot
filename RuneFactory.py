import cv2
from SwRuneFarmerProject.Rune import Rune
from SwRuneFarmerProject.TensorflowWrapper import DetectionClasses, GetClassIndexByClass, \
    GetAbsoluteBoxCoordinatesByClassIndex
from SwRuneFarmerProject.TesseractUtility import GetRuneTitle, GetRuneMainStat, GetRuneSubStats

snippetSizePercentOffset = 0.004
borderColor = [0, 0, 0]


def CreateRune(screenshot, detectedClasses, detectedBoxes):
    imageHeight, imageWidth, colorChannel = screenshot.shape
    imageHeightOffset = int(imageHeight * snippetSizePercentOffset)
    imageWidthOffset = int(imageWidth * snippetSizePercentOffset)

    titleSnippet = getScreenShotSnippetByClass(DetectionClasses.Title, screenshot, detectedClasses, detectedBoxes,
                                               imageHeight, imageWidth, imageHeightOffset, imageWidthOffset)
    titleAsString = GetRuneTitle(titleSnippet, False, True)

    mainStatSnippet = getScreenShotSnippetByClass(DetectionClasses.MainStat, screenshot, detectedClasses,
                                                  detectedBoxes, imageHeight, imageWidth, imageHeightOffset,
                                                  imageWidthOffset)
    mainStatAsString = GetRuneMainStat(mainStatSnippet, False, True)

    subStatsSnippet = getScreenShotSnippetByClass(DetectionClasses.SubStats, screenshot, detectedClasses,
                                                  detectedBoxes, imageHeight, imageWidth, imageHeightOffset,
                                                  imageWidthOffset)
    subStatsAsString = GetRuneSubStats(subStatsSnippet, False, True)

    rune = Rune(titleAsString, mainStatAsString, subStatsAsString)
    return rune


def getScreenShotSnippetByClass(searchedClass, screenshot, detectedClasses, detectedBoxes, imageHeight, imageWidth,
                                imageHeightOffset, imageWidthOffset):
    classIndex = GetClassIndexByClass(searchedClass, detectedClasses)

    yMinAbsolute, yMaxAbsolute, xMinAbsolute, xMaxAbsolute =\
        GetAbsoluteBoxCoordinatesByClassIndex(classIndex, detectedBoxes, imageHeight, imageWidth)

    snippet = screenshot[yMinAbsolute:yMaxAbsolute, xMinAbsolute:xMaxAbsolute, :]
    snippet = cv2.cvtColor(snippet, cv2.COLOR_RGB2GRAY)

    # space added by imageOffset should always be black to ensure no noise is added to the string in picture
    snippet = cv2.copyMakeBorder(snippet,
                                 imageHeightOffset,
                                 imageHeightOffset,
                                 imageWidthOffset,
                                 imageWidthOffset,
                                 cv2.BORDER_CONSTANT, value=borderColor)

    return snippet
