import pytest
from SwRuneFarmerProject.Rune import Rune


@pytest.fixture
def fix_SixStarRune():
    return {(Rune("", "HP +11%", ""), True),
            (Rune("", "HP +360", ""), True),
            (Rune("", "HP 100", ""), False),
            (Rune("", "HP +7", ""), False),
            (Rune("", "HP+360", ""), False),
            (Rune("", "HP +", ""), False),
            (Rune("", "H +360", ""), False),
            (Rune("", "360", ""), False),
            (Rune("", "SPD +7", ""), True),
            (Rune("", "@foo1+", ""), False),
            (Rune("", "CRI Rate +/%", ""), False)}


@pytest.mark.parametrize("testee", fix_SixStarRune())
def test_IsSixStarRune(testee):
    assert testee[0]._Rune__isConfirmedSixStarRune() == testee[1]


@pytest.fixture
def fix_GradeLowerThanHero():
    return {(Rune("", "", "SPD +5\nATK +20\nResistance +6%"), False),
            (Rune("", "", "SPD +5\nATK +20"), True),
            (Rune("", "", "SPD +5\nATK +20\nResistance +6%\nATK +7%"), False),
            (Rune("", "", "SPD +5"), True),
            (Rune("", "", "\n\n\n"), False)}


@pytest.mark.parametrize("testee", fix_GradeLowerThanHero())
def test_IsGradeLowerThanHero(testee):
    assert testee[0]._Rune__isGradeLowerThanHero() == testee[1]
