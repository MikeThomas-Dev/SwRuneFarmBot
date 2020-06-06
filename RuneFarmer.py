import cv2
import random
from SwRuneFarmerProject.TensorflowWrapper import PerformObjectDetection, DetectionClasses, \
    IsDetectionResultConsistent, ReduceDetectionResultsToThreshold
from SwRuneFarmerProject.WindowsUiUtility import GetWindowHandleByWindowTitle, GetScreenShotFromWindow, \
    SetCursorPosition, DoLeftClick
from SwRuneFarmerProject.TesseractUtility import GetRuneTitle, GetRuneMainStat, GetRuneSubStats
from SwRuneFarmerProject.FarmingStateMachine import RunStates, IsActionDelayElapsed

detectionScoreThreshold = 0.7
snippetSizePercentOffset = 0.004
borderColor = [0, 0, 0]

bluestacksHwnd = GetWindowHandleByWindowTitle("BlueStacks")

currentRunState = RunStates.RunInProgress

while True:
    screenshot = GetScreenShotFromWindow(bluestacksHwnd)

    boxes, scores, classes, num = PerformObjectDetection(screenshot)
    classesToConsider, boxesToConsider = ReduceDetectionResultsToThreshold(boxes, scores, classes,
                                                                           detectionScoreThreshold)

    if not IsDetectionResultConsistent(classesToConsider):
        continue

    imageHeight, imageWidth, colorChannel = screenshot.shape

    print("\nConsistent detection result")

    if currentRunState == RunStates.RunInProgress:
        victoryLabelIndex = [i for i in range(len(classesToConsider)) if classesToConsider[i]
                             == DetectionClasses.VictoryLabel.value]

        if not IsActionDelayElapsed(3):
            print("\nAction delay NOT elapsed")
            continue

        # [ymin, xmin, ymax, xmax] boxes coordinate format
        yMinAbsolute = int(boxesToConsider[victoryLabelIndex[0]][0] * imageHeight)
        yMaxAbsolute = int(boxesToConsider[victoryLabelIndex[0]][2] * imageHeight)
        xMaxAbsolute = int(boxesToConsider[victoryLabelIndex[0]][3] * imageWidth)
        xMinAbsolute = int(boxesToConsider[victoryLabelIndex[0]][1] * imageWidth)

        randomYPosInRange = random.randint(yMinAbsolute, yMaxAbsolute)
        randomXPosInRange = random.randint(xMinAbsolute, xMaxAbsolute)

        SetCursorPosition(randomXPosInRange, randomYPosInRange)
        DoLeftClick()
        print("\nVictory screen click performed!")

        currentRunState = RunStates.WaitingAtTreasureBox
    elif currentRunState == RunStates.WaitingAtTreasureBox:
        treasureBoxIndex = [i for i in range(len(classesToConsider)) if classesToConsider[i]
                            == DetectionClasses.TreasureBox.value]

        if not IsActionDelayElapsed(3):
            print("\nAction delay NOT elapsed")
            continue

        # [ymin, xmin, ymax, xmax] boxes coordinate format
        yMinAbsolute = int(boxesToConsider[treasureBoxIndex[0]][0] * imageHeight)
        yMaxAbsolute = int(boxesToConsider[treasureBoxIndex[0]][2] * imageHeight)
        xMaxAbsolute = int(boxesToConsider[treasureBoxIndex[0]][3] * imageWidth)
        xMinAbsolute = int(boxesToConsider[treasureBoxIndex[0]][1] * imageWidth)

        randomYPosInRange = random.randint(yMinAbsolute, yMaxAbsolute)
        randomXPosInRange = random.randint(xMinAbsolute, xMaxAbsolute)

        SetCursorPosition(randomXPosInRange, randomYPosInRange)
        DoLeftClick()
        print("\nTreasure box click performed!")
    else:
        continue

    print("\nNew Item analysis:")
    for i in range(classesToConsider.size):
        if (classesToConsider[i] == DetectionClasses.Title.value
                or classesToConsider[i] == DetectionClasses.MainStat.value
                or classesToConsider[i] == DetectionClasses.SubStats.value):
            imageHeightOffset = int(imageHeight * snippetSizePercentOffset)
            imageWidthOffset = int(imageWidth * snippetSizePercentOffset)

            # [ymin, xmin, ymax, xmax] boxes coordinate format
            yMinAbsolute = int(boxesToConsider[i][0] * imageHeight - imageHeightOffset)
            yMaxAbsolute = int(boxesToConsider[i][2] * imageHeight + imageHeightOffset)
            xMaxAbsolute = int(boxesToConsider[i][3] * imageWidth + imageWidthOffset)
            xMinAbsolute = int(boxesToConsider[i][1] * imageWidth - imageWidthOffset)
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

            if classesToConsider[i] == DetectionClasses.Title.value:
                runeTitle = GetRuneTitle(snippet, False, True)
            elif classesToConsider[i] == DetectionClasses.MainStat.value:
                runeMainStat = GetRuneMainStat(snippet, False, True)
            elif classesToConsider[i] == DetectionClasses.SubStats.value:
                runeSubStats = GetRuneSubStats(snippet, False, True)

    isDetectionResultConsistent = False
    currentRunState = RunStates.RunInProgress
