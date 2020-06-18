import pytest
from SwRuneFarmerProject.Rune import Rune


@pytest.fixture
def fix_SixStarRune():
    return {(Rune("Powerful Energy Rune (6)", "HP +11%", "ATK +20\nResistance +6%\nSPD +5"), True),
            (Rune("Energy Rune (5)", "HP +360", "SPD +4\nCRI Rate +5%\nCRI Dmg +5%"), True),
            (Rune("Vampire Rune (5)", "HP 100", "ATK +7\nHP +2%\nDEF +8\nAccuracy +4%"), False),
            (Rune("Durable Destroy Rune (5)", "HP +7", "ATK +7\nHP +2%\nDEF +8\nAccuracy +4%"), False),
            (Rune("_", "HP +360", "_"), True),
            (Rune("_", "HP+360", "_"), False),
            (Rune("_", "HP 360", "_"), False),
            (Rune("_", "HP +", "_"), False)}


@pytest.mark.parametrize("testee", fix_SixStarRune())
def test_IsSixStarRune(testee):
    assert testee[0]._Rune__isConfirmedSixStarRune() == testee[1]