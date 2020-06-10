import cv2
from SwRuneFarmerProject.Rune import Rune
from SwRuneFarmerProject.TensorflowWrapper import BoxCoordinateFormat, DetectionClasses
from SwRuneFarmerProject.TesseractUtility import GetRuneTitle, GetRuneMainStat, GetRuneSubStats

snippetSizePercentOffset = 0.004
borderColor = [0, 0, 0]


def CreateRune(screenshot, detectedClasses, detectedBoxes):
    imageHeight, imageWidth, colorChannel = screenshot.shape
    imageHeightOffset = int(imageHeight * snippetSizePercentOffset)
    imageWidthOffset = int(imageWidth * snippetSizePercentOffset)

    titleSnippet = getScreenShotSnippetByClass(DetectionClasses.Title.value, screenshot, detectedClasses, detectedBoxes,
                                               imageHeight, imageWidth, imageHeightOffset, imageWidthOffset)
    titleAsString = GetRuneTitle(titleSnippet, False, True)

    mainStatSnippet = getScreenShotSnippetByClass(DetectionClasses.MainStat.value, screenshot, detectedClasses,
                                                  detectedBoxes, imageHeight, imageWidth, imageHeightOffset,
                                                  imageWidthOffset)
    mainStatAsString = GetRuneMainStat(mainStatSnippet, False, True)

    subStatsSnippet = getScreenShotSnippetByClass(DetectionClasses.SubStats.value, screenshot, detectedClasses,
                                                  detectedBoxes, imageHeight, imageWidth, imageHeightOffset,
                                                  imageWidthOffset)
    subStatsAsString = GetRuneSubStats(subStatsSnippet, False, True)

    rune = Rune(titleAsString, mainStatAsString, subStatsAsString)
    return rune


def getScreenShotSnippetByClass(searchedClass, screenshot, detectedClasses, detectedBoxes, imageHeight, imageWidth,
                                imageHeightOffset, imageWidthOffset):
    classIndexCollection = [i for i in range(len(detectedClasses)) if detectedClasses[i] == searchedClass]
    # first result is used in the case of multiple matching detections as it is the one with the highest detection score
    classIndex = classIndexCollection[0]

    yMinAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.YMinCoordinate.value] * imageHeight)
    yMaxAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.YMaxCoordinate.value] * imageHeight)
    xMinAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.XMinCoordinate.value] * imageWidth)
    xMaxAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.XMaxCoordinate.value] * imageWidth)
    snippet = screenshot[yMinAbsolute:yMaxAbsolute, xMinAbsolute:xMaxAbsolute, :]
    snippet = cv2.cvtColor(snippet, cv2.COLOR_RGB2GRAY)

    # space added by imageOffset should always be black to ensure no noise is
    # added to the real string
    snippet = cv2.copyMakeBorder(snippet,
                                 imageHeightOffset,
                                 imageHeightOffset,
                                 imageWidthOffset,
                                 imageWidthOffset,
                                 cv2.BORDER_CONSTANT, value=borderColor)

    return snippet

    #    for i in range(classesToConsider.size):
    #        if (classesToConsider[i] == DetectionClasses.Title.value
    #                or classesToConsider[i] == DetectionClasses.MainStat.value
    #                or classesToConsider[i] == DetectionClasses.SubStats.value):
    #            imageHeightOffset = int(imageHeight * snippetSizePercentOffset)
    #            imageWidthOffset = int(imageWidth * snippetSizePercentOffset)

    # [ymin, xmin, ymax, xmax] boxes coordinate format
    #            yMinAbsolute = int(boxesToConsider[i][0] * imageHeight - imageHeightOffset)
    #            yMaxAbsolute = int(boxesToConsider[i][2] * imageHeight + imageHeightOffset)
    #            xMaxAbsolute = int(boxesToConsider[i][3] * imageWidth + imageWidthOffset)
    #            xMinAbsolute = int(boxesToConsider[i][1] * imageWidth - imageWidthOffset)
    #            snippet = screenshot[yMinAbsolute:yMaxAbsolute, xMinAbsolute:xMaxAbsolute, :]
    #            snippet = cv2.cvtColor(snippet, cv2.COLOR_RGB2GRAY)
    # space added by imageOffset should always be black to ensure no noise is
    # added to the real string
    #            snippet = cv2.copyMakeBorder(snippet,
    #                                         imageHeightOffset,
    #                                         imageHeightOffset,
    #                                         imageWidthOffset,
    #                                         imageWidthOffset,
    #                                         cv2.BORDER_CONSTANT, value=borderColor)

    #            if classesToConsider[i] == DetectionClasses.Title.value:
    #                runeTitle = GetRuneTitle(snippet, False, True)
    #            elif classesToConsider[i] == DetectionClasses.MainStat.value:
    #                runeMainStat = GetRuneMainStat(snippet, False, True)
    #            elif classesToConsider[i] == DetectionClasses.SubStats.value:
    #                runeSubStats = GetRuneSubStats(snippet, False, True)
