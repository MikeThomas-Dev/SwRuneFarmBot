from enum import Enum
import re as regex
from SwRuneFarmerProject.Stat import Stat, StatType


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
        if not self.__isConfirmedSixStarRune():
            print("Rune sold because it is not six star")
            return True

        if self.__isGradeLowerThanHero():
            print("Rune sold because grade is lower than hero")
            return True

        if self.__isConfirmedFlatValueOnPercentSlot:
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
            self.subStats.append(Stat(subStat))

    def __isConfirmedSixStarRune(self):
        if not self.mainStat.IsValid:
            return False

        if self.mainStat.Value == 7 and (self.mainStat.Type == StatType.Spd
                                         or self.mainStat.Type == StatType.CritRate):
            return True
        elif self.mainStat.Value == 11 and (self.mainStat.Type == StatType.Hp
                                            or self.mainStat.Type == StatType.Atk
                                            or self.mainStat.Type == StatType.Def
                                            or self.mainStat.Type == StatType.CritDmg):
            return True
        elif self.mainStat.Value == 12 and (self.mainStat.Type == StatType.Resistance
                                            or self.mainStat.Type == StatType.Accuracy):
            return True
        elif self.mainStat.Value == 22 and (self.mainStat.Type == StatType.FlatAtk
                                            or self.mainStat.Type == StatType.FlatDef):
            return True
        elif self.mainStat.Value == 360 and self.mainStat.Type == StatType.FlatHp:
            return True
        else:
            return False

    def __isGradeLowerThanHero(self):
        result = False if self.grade == Rune.Grade.Hero or self.grade == Rune.Grade.Legendary else True
        return result

    @property
    def __isConfirmedFlatValueOnPercentSlot(self):
        if not self.isTitleValid or not self.mainStat.IsValid:
            return False

        if self.mainStat.IsFlatValue \
                and self.mainStat.Type is not StatType.Spd \
                and (self.slot == self.Slot["TopRight"]
                     or self.slot == self.Slot["TopLeft"]
                     or self.slot == self.Slot["Bottom"]):
            return True
        else:
            return False

    @property
    def __areSubStatsValid(self):
        return all(subStat.IsValid for subStat in self.subStats)

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
