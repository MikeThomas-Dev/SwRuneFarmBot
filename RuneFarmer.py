from SwRuneFarmerProject.TensorflowWrapper import PerformObjectDetection, DetectionClasses, \
    IsDetectionResultConsistent, ReduceDetectionResultsToThreshold
from SwRuneFarmerProject.WindowsUiUtility import GetWindowHandleByWindowTitle, GetScreenShotFromWindow
from SwRuneFarmerProject.FarmingStateMachine import RunStates, DoClickOnTargetClass, IsRuneReceived, \
    IsActionDelayElapsed, IsEnergyRechargeRequired
from SwRuneFarmerProject.RuneFactory import CreateRune

detectionScoreThreshold = 0.7

bluestacksHwnd = GetWindowHandleByWindowTitle("BlueStacks")

currentRunState = RunStates.RunInProgress

print("Farming started")

while True:
    screenshot = GetScreenShotFromWindow(bluestacksHwnd)

    boxes, scores, classes, num = PerformObjectDetection(screenshot)
    classesToConsider, boxesToConsider = ReduceDetectionResultsToThreshold(boxes, scores, classes,
                                                                           detectionScoreThreshold)

    if not IsDetectionResultConsistent(classesToConsider):
        print("Detection result NOT consistent")
        continue

    imageHeight, imageWidth, colorChannel = screenshot.shape

    if currentRunState == RunStates.RunInProgress:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.VictoryLabel, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.WaitingAtTreasureBox
            print("State:", RunStates.WaitingAtTreasureBox.name)
        else:
            continue

    elif currentRunState == RunStates.WaitingAtTreasureBox:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.TreasureBox, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.AnalyseReceivedItemType
            print("State:", RunStates.AnalyseReceivedItemType.name)
        else:
            continue

    elif currentRunState == RunStates.AnalyseReceivedItemType:
        if not IsActionDelayElapsed():
            continue

        if IsRuneReceived(classesToConsider):
            currentRunState = RunStates.ProcessReceivedRune
            print("State:", RunStates.ProcessReceivedRune.name)
        else:
            currentRunState = RunStates.ProcessReceivedGeneralItem
            print("State:", RunStates.ProcessReceivedGeneralItem.name)

    elif currentRunState == RunStates.ProcessReceivedGeneralItem:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Ok, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryRestartFarmRun
            print("State:", RunStates.TryRestartFarmRun.name)
        else:
            continue

    elif currentRunState == RunStates.ProcessReceivedRune:
        rune = CreateRune(screenshot, classesToConsider, boxesToConsider)

        if rune.ShouldRuneBeSold:
            isClickPerformed = DoClickOnTargetClass(DetectionClasses.Sell, classesToConsider, boxesToConsider,
                                                    screenshot)

            if isClickPerformed:
                currentRunState = RunStates.SureToSellRune
                print("State:", RunStates.SureToSellRune.name)
            else:
                continue
        else:
            isClickPerformed = DoClickOnTargetClass(DetectionClasses.Ok, classesToConsider, boxesToConsider,
                                                    screenshot)

            if isClickPerformed:
                print("Rune has been taken")
                currentRunState = RunStates.TryRestartFarmRun
                print("State:", RunStates.TryRestartFarmRun.name)
            else:
                continue

    elif currentRunState == RunStates.SureToSellRune:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Yes, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryRestartFarmRun
            print("State:", RunStates.TryRestartFarmRun.name)
        else:
            continue

    elif currentRunState == RunStates.TryRestartFarmRun:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.ReplayButton, classesToConsider, boxesToConsider,
                                                screenshot)

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
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Shop, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.EnergyReBuyShop
            print("State:", RunStates.EnergyReBuyShop.name)
        else:
            continue

    elif currentRunState == RunStates.EnergyReBuyShop:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.RechargeEnergyTile, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.PurchaseWithCrystals
            print("State:", RunStates.PurchaseWithCrystals.name)
        else:
            continue

    elif currentRunState == RunStates.PurchaseWithCrystals:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Yes, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.PurchaseSuccessful
            print("State:", RunStates.PurchaseSuccessful.name)
        else:
            continue
    elif currentRunState == RunStates.PurchaseSuccessful:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Ok, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.CloseShop
            print("State:", RunStates.CloseShop.name)
        else:
            continue

    elif currentRunState == RunStates.CloseShop:
        isClickPerformed = DoClickOnTargetClass(DetectionClasses.Close, classesToConsider, boxesToConsider,
                                                screenshot)

        if isClickPerformed:
            currentRunState = RunStates.TryRestartFarmRun
            print("State:", RunStates.TryRestartFarmRun.name)
        else:
            continue

    else:
        continue

    isDetectionResultConsistent = False
