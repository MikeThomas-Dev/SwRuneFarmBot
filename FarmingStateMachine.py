from enum import Enum
import time
import random
from SwRuneFarmerProject.WindowsUiUtility import SetCursorPosition, DoLeftClick
from SwRuneFarmerProject.TensorflowWrapper import DetectionClasses, TryGetClassIndexByClass, \
    GetAbsoluteBoxCoordinatesByClassIndex


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


def IsActionDelayElapsed(delayInSeconds):
    if IsActionDelayElapsed.actionDelayStartTime is None:
        IsActionDelayElapsed.actionDelayStartTime = time.time()
        return False

    if (time.time() - IsActionDelayElapsed.actionDelayStartTime) >= delayInSeconds:
        IsActionDelayElapsed.actionDelayStartTime = None
        return True

    return False


IsActionDelayElapsed.actionDelayStartTime = None


def DoClickOnTargetClass(classToClick, detectedClasses, detectedBoxes, screenshot):
    if not IsActionDelayElapsed(3):
        return False

    isClassIndexExistent, classIndex = TryGetClassIndexByClass(classToClick, detectedClasses)

    if not isClassIndexExistent:
        return False

    imageHeight, imageWidth, colorChannel = screenshot.shape

    yMinAbsolute, yMaxAbsolute, xMinAbsolute, xMaxAbsolute =\
        GetAbsoluteBoxCoordinatesByClassIndex(classIndex, detectedBoxes, imageHeight, imageWidth)

    randomYCoordinateInBox = random.randint(yMinAbsolute, yMaxAbsolute)
    randomXCoordinateInBox = random.randint(xMinAbsolute, xMaxAbsolute)

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
