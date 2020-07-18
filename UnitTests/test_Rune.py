import pytest
from SwRuneFarmerProject.Rune import Rune


@pytest.fixture
def fix_SixStarRune():
    return {(Rune("", "HP +11%", ""), Rune.EvaluationResult.Positive),
            (Rune("", "HP +360", ""), Rune.EvaluationResult.Positive),
            (Rune("", "HP 100", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "HP +7", ""), Rune.EvaluationResult.Negative),
            (Rune("", "HP+360", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "HP +", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "H +360", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "360", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "SPD +7", ""), Rune.EvaluationResult.Positive),
            (Rune("", "@foo1+", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "CRI Rate +/%", ""), Rune.EvaluationResult.Invalid),
            (Rune("", "", "SPD +3\nATK +20"), Rune.EvaluationResult.Negative),
            (Rune("", "", "SPD +4\nATK +10"), Rune.EvaluationResult.Invalid),
            (Rune("", "", "SPD +3\nATK +9"), Rune.EvaluationResult.Negative),
            (Rune("", "", "SPD +4\nATK +10\nResistance +"), Rune.EvaluationResult.Invalid),
            (Rune("", "", "foo\nfoo\nfoo"), Rune.EvaluationResult.Invalid),
            (Rune("", "", "SPD +3\nATK +10\nResistance +"), Rune.EvaluationResult.Negative)}


@pytest.mark.parametrize("testee", fix_SixStarRune())
def test_IsSixStarRune(testee):
    assert testee[0]._Rune__isSixStarRune() == testee[1]


@pytest.fixture
def fix_GradeLowerThanHero():
    return {(Rune("", "", "SPD +5\nATK +20\nResistance +6%"), Rune.EvaluationResult.Negative),
            (Rune("", "", "SPD +5\nATK +20"), Rune.EvaluationResult.Positive),
            (Rune("", "", "SPD +5\nATK +20\nResistance +6%\nATK +7%"), Rune.EvaluationResult.Negative),
            (Rune("", "", "SPD +5"), Rune.EvaluationResult.Positive),
            (Rune("", "", "\n\n\n"), Rune.EvaluationResult.Negative)}


@pytest.mark.parametrize("testee", fix_GradeLowerThanHero())
def test_IsGradeLowerThanHero(testee):
    assert testee[0]._Rune__isGradeLowerThanHero() == testee[1]


@pytest.fixture
def fix_IsConfirmedFlatValueOnPercentSlot():
    return {(Rune("Mortal Focus Rune (2)", "HP +11%", ""), Rune.EvaluationResult.Negative),
            (Rune("Focus Rune (4)", "DEF +11%", ""), Rune.EvaluationResult.Negative),
            (Rune("Strong Focus Rune (3)", "DEF +22", ""), Rune.EvaluationResult.Negative),
            (Rune("Tenacious Energy Rune (5)", "HP +360", ""), Rune.EvaluationResult.Negative),
            (Rune("Blade Rune (2)", "SPD +7", ""), Rune.EvaluationResult.Negative),
            (Rune("Enhance Rune (2)", "DEF +22", ""), Rune.EvaluationResult.Positive),
            (Rune("Intricate Blade Rune (4)", "DEF +22", ""), Rune.EvaluationResult.Positive),
            (Rune("Blade Rune (6)", "ATK +22", ""), Rune.EvaluationResult.Positive),
            (Rune("Blade Rune 6)", "ATK +22", ""), Rune.EvaluationResult.Invalid),
            (Rune("Blade Rune (6", "ATK +22", ""), Rune.EvaluationResult.Invalid),
            (Rune("Blade Rune (/)", "ATK +22", ""), Rune.EvaluationResult.Invalid),
            (Rune("Rune (6)", "ATK +22", ""), Rune.EvaluationResult.Invalid),
            (Rune("@ASjd765", "ATK +22", ""), Rune.EvaluationResult.Invalid),
            (Rune("Blade Rune (6)", "ATK +22@", ""), Rune.EvaluationResult.Invalid)}


@pytest.mark.parametrize("testee", fix_IsConfirmedFlatValueOnPercentSlot())
def test_IsConfirmedFlatValueOnPercentSlot(testee):
    assert testee[0]._Rune__isFlatValueOnPercentSlot() == testee[1]


@pytest.fixture
def fix_IsHeroRuneWithMoreThanTwoFlatSubStats():
    return {(Rune("", "", "CRI Rate +6%\nCRI Dmg +7%\nResistance +6%"), Rune.EvaluationResult.Negative),
            (Rune("", "", "CRI Rate +6%\nCRI Dmg +7%\nATK +20"), Rune.EvaluationResult.Negative),
            (Rune("", "", "SPD +5\nATK +20\nResistance +6%"), Rune.EvaluationResult.Negative),
            (Rune("", "", "DEF +20\nATK +20\nResistance +6%"), Rune.EvaluationResult.Positive),
            (Rune("", "", "DEF +20\nATK +20\nXYZ"), Rune.EvaluationResult.Positive),
            (Rune("", "", "DEF +20\nXYZ\nXYZ"), Rune.EvaluationResult.Negative)}


@pytest.mark.parametrize("testee", fix_IsHeroRuneWithMoreThanTwoFlatSubStats())
def test_IsHeroRuneWithMoreThanTwoFlatSubStats(testee):
    assert testee[0]._Rune__isHeroRuneWithMoreThanTwoFlatSubStats() == testee[1]


@pytest.fixture
def fix_IsHeroRuneWithSpdSubStat():
    return {(Rune("", "SPD +7", "CRI Rate +6%\nCRI Dmg +7%\nResistance +6%\nDEF +20"), Rune.EvaluationResult.Invalid),
            (Rune("", "ATK +22", "CRI Rate +6%\nCRI Dmg +7%\nResistance +6%\nSPD +5"), Rune.EvaluationResult.Invalid),
            (Rune("", "SPD +7", "CRI Rate +6%\nCRI Dmg +7%\nResistance +6%"), Rune.EvaluationResult.Invalid),
            (Rune("", "ATK +22", "CRI Rate +6%\nCRI Dmg +7%\nSPD +5"), Rune.EvaluationResult.Positive),
            (Rune("", "ATK +22", "XYZ\nCRI Dmg +7%\nSPD +5"), Rune.EvaluationResult.Positive),
            (Rune("", "ATK +22", "XYZ\nCRI Dmg +7%\nCRI Rate +6%"), Rune.EvaluationResult.Invalid),
            (Rune("", "SPD +7", "Resistance +6%\nCRI Dmg +7%\nCRI Rate +6%"), Rune.EvaluationResult.Invalid)}


@pytest.mark.parametrize("testee", fix_IsHeroRuneWithSpdSubStat())
def test_IsHeroRuneWithoutSpdSubStat(testee):
    assert testee[0]._Rune__isHeroRuneWithSpdSubStat() == testee[1]
