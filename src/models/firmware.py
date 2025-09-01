"""
Enums and constants related to ion firmware in the resin simulation.
"""
from enum import Enum, auto


class IonFirmware(Enum):
    """
    Represents different ion types that can be used in the resin simulation.
    """
    H_PLUS = "H+"
    NA_PLUS = "Na+"
    K_PLUS = "K+"
    CA_2PLUS = "Ca2+"
    MG_2PLUS = "Mg2+"
    FE_3PLUS = "Fe3+"
    AL_3PLUS = "Al3+"
    CU_2PLUS = "Cu2+"
    ZN_2PLUS = "Zn2+"
    MIXED = "mixed"

    @classmethod
    def from_string(cls, value: str) -> 'IonFirmware':
        """Create an IonFirmware from a string representation."""
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"No IonFirmware with value {value}")


# Mobility constants for different ions (in relative units)
ION_MOBILITY = {
    IonFirmware.H_PLUS: 36.23e-8,
    IonFirmware.NA_PLUS: 5.19e-8,
    IonFirmware.K_PLUS: 7.62e-8,
    IonFirmware.CA_2PLUS: 6.17e-8,
    IonFirmware.MG_2PLUS: 5.46e-8,
    IonFirmware.FE_3PLUS: 4.50e-8,
    IonFirmware.AL_3PLUS: 4.20e-8,
    IonFirmware.CU_2PLUS: 5.60e-8,
    IonFirmware.ZN_2PLUS: 5.50e-8,
}
