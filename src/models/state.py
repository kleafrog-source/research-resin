"""
Data classes for representing the resin properties and the computational state of the resin simulation.
"""
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

@dataclass
class Resin:
    """
    Represents the physical and chemical properties of a specific ion-exchange resin.
    """
    name: str
    manufacturer: str
    type: str
    structure: str
    functional_group: str
    ionic_form: str
    anion_exchange_capacity_min_meq_ml: Optional[float] = None
    anion_exchange_capacity_max_meq_ml: Optional[float] = None
    specific_volume_g_ml: Optional[str] = None
    water_retention_capacity_percent: Optional[str] = None
    mean_diameter_um: Optional[float] = None
    uniformity_coefficient: Optional[float] = None
    max_temp_c: Optional[int] = None
    mercury_capacity_g_dm3: Optional[float] = None

    @classmethod
    def load_from_json(cls, filepath: str) -> List['Resin']:
        """Loads a list of resins from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return [cls(**resin_data) for resin_data in data]

@dataclass
class ComputationalState:
    """
    Represents the calculated state of the resin with various physical and chemical properties.
    
    Attributes:
        conductivity: Electrical conductivity (σ)
        catalytic_activity: Catalytic activity (κ)
        structural_role: Structural role parameter (ρ)
        thermal_power: Thermal power (ΔT)
        tribological_performance: Friction coefficient (μ_eff)
        optical_quality: Optical quality (Q_optical)
        swelling_ratio: Degree of swelling (volume ratio)
        mechanical_strength: Mechanical strength (relative units)
        ion_diffusion_rate: Ion diffusion rate
        selectivity_coefficient: Selectivity coefficient
        chemical_stability: Chemical stability (0-1)
        surface_area: Specific surface area
    """
    # Existing properties
    conductivity: float               # σ
    catalytic_activity: float         # κ
    structural_role: float            # ρ
    thermal_power: float = 0.0        # ΔT
    tribological_performance: float = 0.0  # μ_eff (friction coefficient)
    optical_quality: float = 0.0      # Q_optical (reflection quality)
    
    # Properties from previous model
    swelling_ratio: float = 1.0          # Degree of swelling (volume ratio)
    mechanical_strength: float = 1.0     # Mechanical strength (relative units)
    ion_diffusion_rate: float = 1.0      # Ion diffusion rate
    selectivity_coefficient: float = 1.0 # Selectivity coefficient
    chemical_stability: float = 1.0      # Chemical stability (0-1)
    surface_area: float = 1.0            # Specific surface area

    def to_dict(self) -> Dict[str, Any]:
        """Convert the state to a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComputationalState':
        """Create a ComputationalState from a dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
