import re as regex
from enum import Enum


class Stat:
    statFormatRegex = regex.compile(r"^([A-Za-z]+\s){1,2}\+\d+%?$")
    percentageStatRegex = regex.compile(r".+%$")

    def __init__(self, stat):
        self.IsValid = True if Stat.statFormatRegex.fullmatch(stat) else False
        if not self.IsValid:
            self.Type = None
            self.IsFlatValue = None
            self.Type = None
            self.Value = None
            return

        self.IsValid = True
        self.__initializeIsFlatValue(stat)
        self.__initializeType(stat)
        self.__initializeValue(stat)

    def __initializeIsFlatValue(self, stat):
        self.IsFlatValue = False if Stat.percentageStatRegex.match(stat) else True

    def __initializeType(self, stat):
        typeAsString = stat.split('+', 1)[0].rstrip()

        if typeAsString == "HP" and self.IsFlatValue:
            self.Type = StatType.FlatHp
        elif typeAsString == "HP" and not self.IsFlatValue:
            self.Type = StatType.Hp
        elif typeAsString == "ATK" and self.IsFlatValue:
            self.Type = StatType.FlatAtk
        elif typeAsString == "ATK" and not self.IsFlatValue:
            self.Type = StatType.Atk
        elif typeAsString == "DEF" and self.IsFlatValue:
            self.Type = StatType.FlatDef
        elif typeAsString == "DEF" and not self.IsFlatValue:
            self.Type = StatType.Def
        elif typeAsString == "SPD":
            self.Type = StatType.Spd
        elif typeAsString == "CRI Rate":
            self.Type = StatType.CritRate
        elif typeAsString == "CRI Dmg":
            self.Type = StatType.CritDmg
        elif typeAsString == "Resistance":
            self.Type = StatType.Resistance
        elif typeAsString == "Accuracy":
            self.Type = StatType.Accuracy

    def __initializeValue(self, stat):
        if self.IsFlatValue:
            self.Value = int(stat.split('+', 1)[1])
        else:
            self.Value = int(stat[stat.find('+') + 1: stat.find('%')])


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
