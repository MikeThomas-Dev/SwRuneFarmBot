from enum import Enum
import re as regex
from SwRuneFarmerProject.Stat import Stat


class Rune:
    titleFormatRegex = regex.compile(r"^([A-Za-z]+\s){2,3}\(\d\)$")

    def __init__(self, title, mainStat, subStats):
        self.inputTitle = title
        self.inputMainStat = mainStat
        self.inputSubStats = subStats
        self.__processTitle(title)

    def __processTitle(self, title):
        self.isTitleValid = True if Rune.titleFormatRegex.fullmatch(title) else self.isTitleValid = False
        if not self.isTitleValid:
            self.type = None
            self.position = None
            return

        splitTitle = title.split()
        splitTitleLen = len(splitTitle)
        if splitTitleLen == 2:
            self.type = Rune.Type[splitTitle[0]]
            self.position = Rune.Slot[splitTitle[1]]
        elif splitTitleLen == 3:
            self.type = Rune.Type[splitTitle[1]]
            self.position = Rune.Slot[splitTitle[2]]

    def __processMainStat(self, mainStat):
        mainStat = Stat(mainStat)

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
