from enum import Enum
import time
import random
from SwRuneFarmerProject.WindowsUiUtility import SetCursorPosition, DoLeftClick
from SwRuneFarmerProject.TensorflowWrapper import DetectionClasses, TryGetClassIndexByClass, \
    GetAbsoluteBoxCoordinatesByClassIndex

INACCURARY_OFFSET = 0.03


class RunStates(Enum):
    RunInProgress = 1
    WaitingAtVictoryScreen = 2
    WaitingAtTreasureBox = 3
    AnalyseReceivedItemType = 4
    ProcessReceivedRune = 5
    ProcessReceivedGeneralItem = 6
    SureToSellRune = 7
    TryRestartFarmRun = 8
    CheckForRequiredEnergyRecharge = 9
    NotEnoughEnergyDialog = 10
    EnergyReBuyShop = 11
    PurchaseWithCrystals = 12
    PurchaseSuccessful = 13
    CloseShop = 14


def IsActionDelayElapsed(delayInSeconds=3):
    if IsActionDelayElapsed.actionDelayStartTime is None:
        IsActionDelayElapsed.actionDelayStartTime = time.time()
        return False

    if (time.time() - IsActionDelayElapsed.actionDelayStartTime) >= delayInSeconds:
        IsActionDelayElapsed.actionDelayStartTime = None
        return True

    return False


IsActionDelayElapsed.actionDelayStartTime = None


def DoClickOnTargetClass(classToClick, detectedClasses, detectedBoxes, screenshot):
    if not IsActionDelayElapsed():
        print("Click action delay not elapsed!")
        return False

    isClassIndexExistent, classIndex = TryGetClassIndexByClass(classToClick, detectedClasses)

    if not isClassIndexExistent:
        print("Target class for click action not found - resetting click action")
        return False

    imageHeight, imageWidth, colorChannel = screenshot.shape

    yMinAbsolute, yMaxAbsolute, xMinAbsolute, xMaxAbsolute = \
        GetAbsoluteBoxCoordinatesByClassIndex(classIndex, detectedBoxes, imageHeight, imageWidth)

    offsetYMinAbsolute, offsetYMaxAbsolute, offsetXMinAbsolute, offsetXMaxAbsolute = \
        AddInaccuracyMarginToCoordinates(yMinAbsolute, yMaxAbsolute, xMinAbsolute, xMaxAbsolute)

    randomYCoordinateInBox = random.randint(offsetYMinAbsolute, offsetYMaxAbsolute)
    randomXCoordinateInBox = random.randint(offsetXMinAbsolute, offsetXMaxAbsolute)

    SetCursorPosition(randomXCoordinateInBox, randomYCoordinateInBox)
    DoLeftClick()
    return True


def IsRuneReceived(detectedClasses):
    # classes are ordered by their detection score -> first item in loop decides which item type was received
    for detectedClass in detectedClasses:
        if detectedClass == DetectionClasses.GeneralItem.value:
            return False
        elif detectedClass == DetectionClasses.Title.value \
                or detectedClass == DetectionClasses.MainStat.value \
                or detectedClass == DetectionClasses.SubStats.value:
            return True


def IsEnergyRechargeRequired(detectedClasses):
    if DetectionClasses.NotEnoughEnergyDialog.value in detectedClasses:
        return True
    else:
        return False


def AddInaccuracyMarginToCoordinates(yMinAbsolute, yMaxAbsolute, xMinAbsolute, xMaxAbsolute):
    deltaY = yMaxAbsolute - yMinAbsolute
    deltaX = xMaxAbsolute - xMinAbsolute

    yOffset = deltaY * INACCURARY_OFFSET
    xOffset = deltaX * INACCURARY_OFFSET

    offsetYMinAbsolute = int(yMinAbsolute + yOffset)
    offsetYMaxAbsolute = int(yMaxAbsolute - yOffset)
    offsetXMinAbsolute = int(xMinAbsolute + xOffset)
    offsetXMaxAbsolute = int(xMaxAbsolute - xOffset)
    return offsetYMinAbsolute, offsetYMaxAbsolute, offsetXMinAbsolute, offsetXMaxAbsolute
