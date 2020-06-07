from enum import Enum
import time
import random
from SwRuneFarmerProject.WindowsUiUtility import SetCursorPosition, DoLeftClick
from SwRuneFarmerProject.TensorflowWrapper import BoxCoordinateFormat, DetectionClasses


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
    classIndexCollection = [i for i in range(len(detectedClasses)) if detectedClasses[i] == classToClick]
    # first result is used in the case of multiple matching detections as it is the one with the highest detection score
    classIndex = classIndexCollection[0]

    if not IsActionDelayElapsed(3):
        return False

    imageHeight, imageWidth, colorChannel = screenshot.shape

    yMinAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.YMinCoordinate.value] * imageHeight)
    yMaxAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.YMaxCoordinate.value] * imageHeight)
    xMinAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.XMinCoordinate.value] * imageWidth)
    xMaxAbsolute = int(detectedBoxes[classIndex][BoxCoordinateFormat.XMaxCoordinate.value] * imageWidth)

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
