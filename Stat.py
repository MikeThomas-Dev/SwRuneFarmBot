import re as regex
from enum import Enum


class Stat:
    statFormatRegex = regex.compile(r"^([A-Za-z]+\s){1,2}\+\d+%\?$")
    percentageStatRegex = regex.compile(r"%$")

    def __init__(self, stat):
        self.isValid = True if Stat.statFormatRegex.fullmatch(stat) else self.isValid = False
        if not self.isValid:
            return

        self.isValid = True
        self.__initializeIsFlatValue(stat)

    def __initializeIsFlatValue(self, stat):
        self.isFlatValue = False if Stat.percentageStatRegex.fullmatch(stat) else self.isFlatValue = True

    def __initializeType(self, stat):
        statType = stat.split('+').rstrip()

        if statType == "HP" and self.isFlatValue:
            self.Type = StatType.FlatHp


class StatType(Enum):
    FlatHp = 1
    Hp = 2
    FlatAtk = 3
    Atk = 4
    FlatDef = 5
    Def = 6
    Spd = 7
    CritRate = 8
    CritDmg = 9
    Resistance = 10
    Accuracy = 11
