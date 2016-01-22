from .HydrogenBond import HBondAcceptor, HBondDonor
from .Weight import Weight
from .WildmanCrippenLogP import WildmanCrippenLogP, WildmanCrippenMR

from ._base import Descriptor


class LipinskiLike(Descriptor):
    require_connected = False

    @classmethod
    def preset(cls):
        yield cls()

    def __str__(self):
        return self.__class__.__name__


class Lipinski(LipinskiLike):
    r"""Lipinski rule of 5 descriptor.

    LogP: WildmanCrippenLogP

    :rtype: bool
    """

    __slots__ = ()

    def dependencies(self):
        return dict(
            LogP=WildmanCrippenLogP(),
            MW=Weight(),
            HBDon=HBondDonor(),
            HBAcc=HBondAcceptor(),
        )

    def calculate(self, mol, LogP, MW, HBDon, HBAcc):
        return\
            HBDon <= 5 and\
            HBAcc <= 10 and\
            MW <= 500 and\
            LogP <= 5


class GhoseFilter(LipinskiLike):
    r"""Ghose filter descriptor.

    LogP, MR: WildmanCrippenLogP

    :rtype: bool
    """

    __slots__ = ()

    def dependencies(self):
        return dict(
            LogP=WildmanCrippenLogP(),
            MR=WildmanCrippenMR(),
            MW=Weight(),
        )

    def calculate(self, mol, MW, LogP, MR):
        return\
            (160 <= MW <= 480) and\
            (20 <= mol.GetNumAtoms() <= 70) and\
            (-0.4 <= LogP <= 5.6) and\
            (40 <= MR <= 130)
