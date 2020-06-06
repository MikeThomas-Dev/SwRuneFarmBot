import cv2
from SwRuneFarmerProject.TensorflowWrapper import PerformObjectDetection, DetectionClasses, \
    IsDetectionResultConsistent, ReduceDetectionResultsToThreshold
from SwRuneFarmerProject.WindowsUiUtility import GetWindowHandleByWindowTitle, GetScreenShotFromWindow
from SwRuneFarmerProject.TesseractUtility import GetRuneTitle, GetRuneMainStat, GetRuneSubStats
from SwRuneFarmerProject.FarmingStateMachine import RunStates, DoClickOnTargetClass, IsRuneReceived, \
    IsActionDelayElapsed

detectionScoreThreshold = 0.7
snippetSizePercentOffset = 0.004
borderColor = [0, 0, 0]

bluestacksHwnd = GetWindowHandleByWindowTitle("BlueStacks")

currentRunState = RunStates.RunInProgress

isRuneSold = None

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
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.VictoryLabel.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.WaitingAtTreasureBox
        else:
            continue

    elif currentRunState == RunStates.WaitingAtTreasureBox:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.TreasureBox.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.AnalyseReceivedItemType
        else:
            continue

    elif currentRunState == RunStates.AnalyseReceivedItemType:
        if not IsActionDelayElapsed(3):
            print("\nAction delay NOT elapsed")
            continue

        if IsRuneReceived(classesToConsider):
            currentRunState = RunStates.ProcessReceivedRune
        else:
            currentRunState = RunStates.ProcessReceivedGeneralItem

    elif currentRunState == RunStates.ProcessReceivedGeneralItem:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Ok.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryToRestartFarmRun
        else:
            continue

    elif currentRunState == RunStates.ProcessReceivedRune:
        if isRuneSold is None:
            isRuneSold = input("Should rune be sold? Enter Y or N")

        if isRuneSold == "Y":
            isClickPerformed = DoClickOnTargetClass(DetectionClasses.Sell.value, classesToConsider,
                                                    boxesToConsider, screenshot)

            if isClickPerformed:
                currentRunState = RunStates.SureToSellRune
                isRuneSold = None
            else:
                continue

        elif isRuneSold == "N":
            print("Rune kept")
            isRuneSold = None
        else:
            continue

    elif currentRunState == RunStates.SureToSellRune:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Yes.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryToRestartFarmRun
        else:
            continue

    elif currentRunState == RunStates.TryToRestartFarmRun:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.ReplayButton.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.RunInProgress
        else:
            continue
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
