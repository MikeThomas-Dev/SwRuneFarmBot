from SwRuneFarmerProject.Stat import Stat, StatType


class SubStat(Stat):
    def __init__(self, stat):
        super().__init__(stat)
        if not self.IsValid:
            self.IsSubStatValueTooLowForSixStar = None
            return

        self.__initializeIsStatValueTooLowForSixStar()

    def __initializeIsStatValueTooLowForSixStar(self):
        if self.Type == StatType.FlatHp and self.Value < 135:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.Hp and self.Value < 5:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.FlatAtk and self.Value < 10:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.Atk and self.Value < 5:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.FlatDef and self.Value < 10:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.Def and self.Value < 5:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.Spd and self.Value < 4:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.CritRate and self.Value < 4:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.CritDmg and self.Value < 4:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.Resistance and self.Value < 4:
            self.IsSubStatValueTooLowForSixStar = True
        elif self.Type == StatType.Accuracy and self.Value < 4:
            self.IsSubStatValueTooLowForSixStar = True
        else:
            self.IsSubStatValueTooLowForSixStar = False
