"""
Core simulation logic for the resin application.
"""
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from ..models import ComputationalState, IonFirmware
from .semantics import get_ion_semantics

# Base resin properties
BASE_RESIN_PROPS = {
    'base_conductivity': 0.01,
    'polymer_type': 'styrene-divinylbenzene',
    'crosslinking_density': 0.08,
    'water_content': 0.53,
    'total_capacity': 1.8,
    'dynamic_capacity': 526,
    'granule_size_min': 0.315,
    'granule_size_max': 1.25,
    'effective_size': 0.45,
    'uniformity_coefficient': 1.7,
    'osmotic_stability': 0.945,
    'max_temperature': 120,
    'pH_range': (0, 14),
    'volume_change_H_Na': 0.085,
    'base_structural_role': 0.6
}

def apply_firmware(resin_state: Optional[ComputationalState], ion: IonFirmware, 
                  resin_props: Dict[str, Any]) -> ComputationalState:
    """
    Apply ion firmware to the current resin state.
    
    Args:
        resin_state: Current state of the resin (None for initial state)
        ion: The ion firmware to apply
        resin_props: Resin properties dictionary
        
    Returns:
        New ComputationalState after applying the ion
    """
    if ion == IonFirmware.MIXED:
        raise ValueError("Для mixed состояния требуется состав")
    
    # Get the semantic function for this ion
    semantic_func = get_ion_semantics(ion)
    if not semantic_func:
        raise ValueError(f"No semantic function defined for ion: {ion}")
    
    # Apply the semantic function to get the new state
    return semantic_func(resin_props)

def generate_single_ion_states(resin_props: Dict[str, Any]) -> Dict[IonFirmware, ComputationalState]:
    """
    Generate states for all single ions.
    
    Args:
        resin_props: Resin properties dictionary
        
    Returns:
        Dictionary mapping each ion to its ComputationalState
    """
    states = {}
    errors = []
    
    for ion in IonFirmware:
        if ion == IonFirmware.MIXED:
            continue
            
        try:
            state = apply_firmware(None, ion, resin_props)
            states[ion] = state
        except Exception as e:
            error_msg = f"Error generating state for {ion}: {str(e)}"
            errors.append(error_msg)
            print(error_msg)  # Log to console
    
    if errors and not states:
        # If all ions failed, raise an exception with all error messages
        raise RuntimeError("\n".join(["Failed to generate any ion states:"] + errors))
    elif errors:
        # If some ions failed, log the errors but continue with the successful ones
        print("\n".join(["Some ion states could not be generated:"] + errors))
    
    return states

def run_program(program: List[IonFirmware], initial_resin_props: Dict[str, Any]) -> ComputationalState:
    """
    Run a sequence of ion applications on the resin.
    
    Args:
        program: List of IonFirmware to apply in sequence
        initial_resin_props: Initial resin properties
        
    Returns:
        Final ComputationalState after running the program
    """
    current_resin_props = initial_resin_props.copy()
    current_state = None

    for ion in program:
        new_state = apply_firmware(current_state, ion, current_resin_props)
        current_state = new_state

    return current_state

def simulate_osmotic_degradation(initial_state: ComputationalState, cycles: int, 
                                resin_grade: str = 'высший') -> ComputationalState:
    """
    Simulate the degradation of resin properties over multiple cycles.
    
    Args:
        initial_state: Initial state of the resin
        cycles: Number of degradation cycles to simulate
        resin_grade: Quality grade of the resin
        
    Returns:
        Degraded ComputationalState
    """
    stability_map = {'высший': 0.995, 'первый': 0.985, 'базовый': 0.975}
    retention_per_cycle = stability_map.get(resin_grade, 0.98)
    
    degraded_state = initial_state
    for _ in range(cycles):
        degraded_state = ComputationalState(
            conductivity=degraded_state.conductivity * retention_per_cycle,
            catalytic_activity=degraded_state.catalytic_activity * retention_per_cycle,
            structural_role=degraded_state.structural_role * retention_per_cycle,
            thermal_power=degraded_state.thermal_power,
            tribological_performance=degraded_state.tribological_performance * retention_per_cycle,
            optical_quality=degraded_state.optical_quality * retention_per_cycle
        )
    return degraded_state

def mixed_ion_state(ion1: IonFirmware, ion2: IonFirmware, 
                   fraction1: float, resin_props: Dict[str, Any]) -> ComputationalState:
    """
    Create a mixed ion state by combining two ion states.
    
    Args:
        ion1: First ion type
        ion2: Second ion type
        fraction1: Fraction of ion1 in the mixture (0-1)
        resin_props: Resin properties
        
    Returns:
        Mixed ComputationalState
    """
    state1 = apply_firmware(None, ion1, resin_props)
    state2 = apply_firmware(None, ion2, resin_props)
    
    mixed_conductivity = state1.conductivity * fraction1 + state2.conductivity * (1 - fraction1)
    mixed_catalytic = state1.catalytic_activity * fraction1 + state2.catalytic_activity * (1 - fraction1)
    mixed_tribo = state1.tribological_performance * fraction1 + state2.tribological_performance * (1 - fraction1)
    mixed_optical = state1.optical_quality * fraction1 + state2.optical_quality * (1 - fraction1)
    
    if ion1 != ion2:
        vol_change_H_Na = resin_props.get('volume_change_H_Na', 0.085)
        if {ion1, ion2} == {IonFirmware.H_PLUS, IonFirmware.NA_PLUS}:
            base_role = resin_props.get('base_structural_role', 0.6)
            role_H = base_role * (1 + vol_change_H_Na / 2)
            role_Na = base_role * (1 - vol_change_H_Na / 2)
            mixed_structural_role = role_H * fraction1 + role_Na * (1 - fraction1)
        else:
            mixed_structural_role = state1.structural_role * fraction1 + state2.structural_role * (1 - fraction1)
    else:
        mixed_structural_role = state1.structural_role
        
    return ComputationalState(
        conductivity=mixed_conductivity,
        catalytic_activity=mixed_catalytic,
        structural_role=mixed_structural_role,
        thermal_power=state1.thermal_power * fraction1 + state2.thermal_power * (1 - fraction1),
        tribological_performance=mixed_tribo,
        optical_quality=mixed_optical
    )
