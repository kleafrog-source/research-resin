"""
Core functionality for the Resin Simulation application.
"""

from .simulation import (
    apply_firmware,
    generate_single_ion_states,
    run_program,
    simulate_osmotic_degradation,
    mixed_ion_state
)

__all__ = [
    'apply_firmware',
    'generate_single_ion_states',
    'run_program',
    'simulate_osmotic_degradation',
    'mixed_ion_state'
]
