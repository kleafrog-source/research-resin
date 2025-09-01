"""
Semantic functions for different ion types in the resin simulation.
"""
from typing import Dict, Any
from ..models import ComputationalState, IonFirmware

def _base_ion_effect(resin_props: Dict[str, Any], 
                   conductivity_scale: float,
                   catalytic_activity: float,
                   structural_role: float,
                   thermal_power: float,
                   tribological_performance: float,
                   optical_quality: float) -> ComputationalState:
    """Base function for ion effects with configurable parameters."""
    base_conductivity = resin_props.get('base_conductivity', 1.0)
    return ComputationalState(
        conductivity=base_conductivity * conductivity_scale,
        catalytic_activity=catalytic_activity,
        structural_role=structural_role,
        thermal_power=thermal_power,
        tribological_performance=tribological_performance,
        optical_quality=optical_quality
    )

def semantics_H_plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for H+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=3.623,
        catalytic_activity=0.10,
        structural_role=0.5,
        thermal_power=-1090,
        tribological_performance=0.05,
        optical_quality=0.7
    )

def semantics_Na_plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Na+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.8,
        catalytic_activity=0.15,
        structural_role=0.6,
        thermal_power=-405,
        tribological_performance=0.03,
        optical_quality=0.9
    )

def semantics_K_plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for K+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.9,
        catalytic_activity=0.18,
        structural_role=0.55,
        thermal_power=-321,
        tribological_performance=0.04,
        optical_quality=0.85
    )

def semantics_Ca_2plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Ca2+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.7,
        catalytic_activity=0.25,
        structural_role=0.7,
        thermal_power=-1590,
        tribological_performance=0.08,
        optical_quality=0.6
    )

def semantics_Mg_2plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Mg2+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.65,
        catalytic_activity=0.22,
        structural_role=0.75,
        thermal_power=-1920,
        tribological_performance=0.09,
        optical_quality=0.65
    )

def semantics_Fe_3plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Fe3+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.5,
        catalytic_activity=0.90,
        structural_role=0.7,
        thermal_power=-4300,
        tribological_performance=0.15,
        optical_quality=0.4
    )

def semantics_Al_3plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Al3+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.45,
        catalytic_activity=0.85,
        structural_role=0.72,
        thermal_power=-4660,
        tribological_performance=0.16,
        optical_quality=0.35
    )

def semantics_Cu_2plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Cu2+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.75,
        catalytic_activity=0.60,
        structural_role=0.65,
        thermal_power=-2100,
        tribological_performance=0.07,
        optical_quality=0.5
    )

def semantics_Zn_2plus(resin_props: Dict[str, Any]) -> ComputationalState:
    """Semantic function for Zn2+ ion."""
    return _base_ion_effect(
        resin_props=resin_props,
        conductivity_scale=0.7,
        catalytic_activity=0.55,
        structural_role=0.68,
        thermal_power=-2040,
        tribological_performance=0.08,
        optical_quality=0.55
    )

# Map ion types to their semantic functions
ION_SEMANTICS = {
    IonFirmware.H_PLUS: semantics_H_plus,
    IonFirmware.NA_PLUS: semantics_Na_plus,
    IonFirmware.K_PLUS: semantics_K_plus,
    IonFirmware.CA_2PLUS: semantics_Ca_2plus,
    IonFirmware.MG_2PLUS: semantics_Mg_2plus,
    IonFirmware.FE_3PLUS: semantics_Fe_3plus,
    IonFirmware.AL_3PLUS: semantics_Al_3plus,
    IonFirmware.CU_2PLUS: semantics_Cu_2plus,
    IonFirmware.ZN_2PLUS: semantics_Zn_2plus,
}

def get_ion_semantics(ion: IonFirmware):
    """Get the semantic function for a given ion."""
    return ION_SEMANTICS.get(ion)
