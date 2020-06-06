from enum import Enum
import time


class RunStates(Enum):
    RunInProgress = 1
    WaitingAtVictoryScreen = 2
    WaitingAtTreasureBox = 3


def IsActionDelayElapsed(delayInSeconds):
    if IsActionDelayElapsed.actionDelayStartTime is None:
        IsActionDelayElapsed.actionDelayStartTime = time.time()
        return False

    if (time.time() - IsActionDelayElapsed.actionDelayStartTime) >= delayInSeconds:
        IsActionDelayElapsed.actionDelayStartTime = None
        return True

    return False


IsActionDelayElapsed.actionDelayStartTime = None
