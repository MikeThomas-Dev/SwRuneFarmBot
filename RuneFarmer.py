import cv2
from SwRuneFarmerProject.TensorflowWrapper import PerformObjectDetection, DetectionClasses, \
    IsDetectionResultConsistent, ReduceDetectionResultsToThreshold
from SwRuneFarmerProject.WindowsUiUtility import GetWindowHandleByWindowTitle, GetScreenShotFromWindow
from SwRuneFarmerProject.TesseractUtility import GetRuneTitle, GetRuneMainStat, GetRuneSubStats
from SwRuneFarmerProject.FarmingStateMachine import RunStates, DoClickOnTargetClass, IsRuneReceived, \
    IsActionDelayElapsed, IsEnergyRechargeRequired

detectionScoreThreshold = 0.7
snippetSizePercentOffset = 0.004
borderColor = [0, 0, 0]

bluestacksHwnd = GetWindowHandleByWindowTitle("BlueStacks")

currentRunState = RunStates.RunInProgress

isRuneSold = None
print("Farming started")

while True:
    screenshot = GetScreenShotFromWindow(bluestacksHwnd)

    boxes, scores, classes, num = PerformObjectDetection(screenshot)
    classesToConsider, boxesToConsider = ReduceDetectionResultsToThreshold(boxes, scores, classes,
                                                                           detectionScoreThreshold)

    if not IsDetectionResultConsistent(classesToConsider):
        print("Detection result NOT consistent")
        continue

    print("Detection result consistent")

    imageHeight, imageWidth, colorChannel = screenshot.shape

    if currentRunState == RunStates.RunInProgress:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.VictoryLabel.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.WaitingAtTreasureBox
            print("State:", RunStates.WaitingAtTreasureBox.name)
        else:
            continue

    elif currentRunState == RunStates.WaitingAtTreasureBox:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.TreasureBox.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.AnalyseReceivedItemType
            print("State:", RunStates.AnalyseReceivedItemType.name)
        else:
            continue

    elif currentRunState == RunStates.AnalyseReceivedItemType:
        if not IsActionDelayElapsed(3):
            continue

        if IsRuneReceived(classesToConsider):
            currentRunState = RunStates.ProcessReceivedRune
            print("State:", RunStates.ProcessReceivedRune.name)
        else:
            currentRunState = RunStates.ProcessReceivedGeneralItem
            print("State:", RunStates.ProcessReceivedGeneralItem.name)

    elif currentRunState == RunStates.ProcessReceivedGeneralItem:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Ok.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryToRestartFarmRun
            print("State:", RunStates.TryToRestartFarmRun.name)
        else:
            continue

    elif currentRunState == RunStates.ProcessReceivedRune:
        if isRuneSold is None:
            isRuneSold = input("Should rune be sold? Enter Y or N \n")

        if isRuneSold == "Y":
            isClickPerformed = DoClickOnTargetClass(DetectionClasses.Sell.value, classesToConsider,
                                                    boxesToConsider, screenshot)

            if isClickPerformed:
                currentRunState = RunStates.SureToSellRune
                print("State:", RunStates.SureToSellRune.name)
                isRuneSold = None
            else:
                continue

        elif isRuneSold == "N":
            isRuneSold = None
        else:
            continue

    elif currentRunState == RunStates.SureToSellRune:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Yes.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryToRestartFarmRun
            print("State:", RunStates.TryToRestartFarmRun.name)
        else:
            continue

    elif currentRunState == RunStates.TryToRestartFarmRun:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.ReplayButton.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            if IsEnergyRechargeRequired(classesToConsider):
                currentRunState = RunStates.NotEnoughEnergyDialog
                print("State:", RunStates.NotEnoughEnergyDialog.name)
            else:
                currentRunState = RunStates.RunInProgress
                print("State:", RunStates.RunInProgress.name)

        else:
            continue

    elif currentRunState == RunStates.NotEnoughEnergyDialog:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Shop.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.EnergyReBuyShop
            print("State:", RunStates.EnergyReBuyShop.name)
        else:
            continue

    elif currentRunState == RunStates.EnergyReBuyShop:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.RechargeEnergyTile.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.PurchaseWithCrystals
            print("State:", RunStates.PurchaseWithCrystals.name)
        else:
            continue

    elif currentRunState == RunStates.PurchaseWithCrystals:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Yes.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.PurchaseSuccessful
            print("State:", RunStates.PurchaseSuccessful.name)
        else:
            continue
    elif currentRunState == RunStates.PurchaseSuccessful:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Ok.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.CloseShop
            print("State:", RunStates.CloseShop.name)
        else:
            continue

    elif currentRunState == RunStates.CloseShop:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Close.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryToRestartFarmRun
            print("State:", RunStates.TryToRestartFarmRun.name)
        else:
            continue

    else:
        continue

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

    isDetectionResultConsistent = False
