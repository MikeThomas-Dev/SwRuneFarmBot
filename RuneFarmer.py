from SwRuneFarmerProject.TensorflowWrapper import PerformObjectDetection, DetectionClasses, \
    IsDetectionResultConsistent, ReduceDetectionResultsToThreshold
from SwRuneFarmerProject.WindowsUiUtility import GetWindowHandleByWindowTitle, GetScreenShotFromWindow
from SwRuneFarmerProject.FarmingStateMachine import RunStates, DoClickOnTargetClass, IsRuneReceived, \
    IsActionDelayElapsed, IsEnergyRechargeRequired
from SwRuneFarmerProject.RuneFactory import CreateRune

detectionScoreThreshold = 0.7

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
            currentRunState = RunStates.TryRestartFarmRun
            print("State:", RunStates.TryRestartFarmRun.name)
        else:
            continue

    elif currentRunState == RunStates.ProcessReceivedRune:
        rune = CreateRune(screenshot, classesToConsider, boxesToConsider)

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
            currentRunState = RunStates.TryRestartFarmRun
            print("State:", RunStates.TryRestartFarmRun.name)
        else:
            continue

    elif currentRunState == RunStates.TryRestartFarmRun:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.ReplayButton.value, classesToConsider,
                                                boxesToConsider, screenshot)

        if isClickPerformed:
            currentRunState = RunStates.CheckForRequiredEnergyRecharge
            print("State:", RunStates.CheckForRequiredEnergyRecharge.name)
        else:
            continue

    elif currentRunState == RunStates.CheckForRequiredEnergyRecharge:
        if IsEnergyRechargeRequired(classesToConsider):
            currentRunState = RunStates.NotEnoughEnergyDialog
        else:
            currentRunState = RunStates.RunInProgress

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
            currentRunState = RunStates.TryRestartFarmRun
            print("State:", RunStates.TryRestartFarmRun.name)
        else:
            continue

    else:
        continue

    isDetectionResultConsistent = False
