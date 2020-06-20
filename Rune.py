from enum import Enum
import re as regex
from SwRuneFarmerProject.Stat import Stat, StatType
from SwRuneFarmerProject.SubStat import SubStat


class Rune:
    titleFormatRegex = regex.compile(r"^([A-Za-z]+\s){2,3}\(\d\)$")

    def __init__(self, title, mainStat, subStats):
        self.inputTitle = title
        self.inputMainStat = mainStat
        self.inputSubStats = subStats
        self.__processTitle(title)
        self.__processMainStat(mainStat)
        self.__processSubStats(subStats)

    @property
    def ShouldRuneBeSold(self):
        if self.__isSixStarRune() == self.EvaluationResult.Negative:
            print("Rune sold because it is not six star")
            return True

        if self.__isGradeLowerThanHero() == self.EvaluationResult.Positive:
            print("Rune sold because grade is lower than hero")
            return True

        if self.__isFlatValueOnPercentSlot() == self.EvaluationResult.Positive:
            print("Rune sold because it has flat value on percentage slot")
            return True

        return False

    def __processTitle(self, title):
        self.isTitleValid = True if Rune.titleFormatRegex.fullmatch(title) else False
        if not self.isTitleValid:
            self.type = None
            self.slot = None
            return

        splitTitle = title.split()
        splitTitleLen = len(splitTitle)
        if splitTitleLen == 3:
            self.type = Rune.Type[splitTitle[0]]
            self.slot = Rune.Slot[splitTitle[2]]
        elif splitTitleLen == 4:
            self.type = Rune.Type[splitTitle[1]]
            self.slot = Rune.Slot[splitTitle[3]]

    def __processMainStat(self, mainStat):
        self.mainStat = Stat(mainStat)

    def __processSubStats(self, subStats):
        self.subStats = []
        splitSubStats = subStats.splitlines()
        self.grade = self.Grade(len(splitSubStats))

        for subStat in splitSubStats:
            self.subStats.append(SubStat(subStat))

    def __isSixStarRune(self):
        if self.mainStat.IsValid:
            if self.mainStat.Value == 7 and (self.mainStat.Type == StatType.Spd
                                             or self.mainStat.Type == StatType.CritRate):
                return self.EvaluationResult.Positive
            elif self.mainStat.Value == 11 and (self.mainStat.Type == StatType.Hp
                                                or self.mainStat.Type == StatType.Atk
                                                or self.mainStat.Type == StatType.Def
                                                or self.mainStat.Type == StatType.CritDmg):
                return self.EvaluationResult.Positive
            elif self.mainStat.Value == 12 and (self.mainStat.Type == StatType.Resistance
                                                or self.mainStat.Type == StatType.Accuracy):
                return self.EvaluationResult.Positive
            elif self.mainStat.Value == 22 and (self.mainStat.Type == StatType.FlatAtk
                                                or self.mainStat.Type == StatType.FlatDef):
                return self.EvaluationResult.Positive
            elif self.mainStat.Value == 360 and self.mainStat.Type == StatType.FlatHp:
                return self.EvaluationResult.Positive
            else:
                return self.EvaluationResult.Negative
        elif any(subStat.IsValid and subStat.IsSubStatValueTooLowForSixStar for subStat in self.subStats):
            return self.EvaluationResult.Negative
        else:
            return self.EvaluationResult.Invalid

    def __isGradeLowerThanHero(self):
        result = self.EvaluationResult.Negative if self.grade == Rune.Grade.Hero or self.grade == Rune.Grade.Legendary \
            else self.EvaluationResult.Positive
        return result

    def __isFlatValueOnPercentSlot(self):
        if not self.isTitleValid or not self.mainStat.IsValid:
            return self.EvaluationResult.Invalid

        if self.mainStat.IsFlatValue \
                and self.mainStat.Type is not StatType.Spd \
                and (self.slot == self.Slot["TopRight"]
                     or self.slot == self.Slot["TopLeft"]
                     or self.slot == self.Slot["Bottom"]):
            return self.EvaluationResult.Positive
        else:
            return self.EvaluationResult.Negative

    Type = Enum(
        value='Type',
        names=[
            ('Energy', 1),
            ('Fatal', 2),
            ('Blade', 3),
            ('Swift', 4),
            ('Focus', 5),
            ('Guard', 6),
            ('Endure', 7),
            ('Shield', 8),
            ('Revenge', 9),
            ('Will', 10),
            ('Nemesis', 11),
            ('Vampire', 12),
            ('Destroy', 13),
            ('Despair', 14),
            ('Violent', 15),
            ('Rage', 16),
            ('Fight', 17),
            ('Determination', 18),
            ('Enhance', 19),
            ('Accuracy', 20),
            ('Tolerance', 21),
        ]
    )

    Slot = Enum(
        value='Slot',
        names=[
            ('Top', 1),
            ('(1)', 1),
            ('TopRight', 2),
            ('(2)', 2),
            ('BottomRight', 3),
            ('(3)', 3),
            ('Bottom', 4),
            ('(4)', 4),
            ('BottomLeft', 5),
            ('(5)', 5),
            ('TopLeft', 6),
            ('(6)', 6),
        ]
    )

    class Grade(Enum):
        Normal = 0
        Magic = 1
        Rare = 2
        Hero = 3
        Legendary = 4

    class EvaluationResult(Enum):
        Positive = 0
        Negative = 1
        Invalid = 2
