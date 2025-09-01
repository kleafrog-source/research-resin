"""
Recommendation system for suggesting optimal ion forms based on application requirements.
"""
from typing import Dict, List, Optional, Tuple, Any, Literal
from dataclasses import dataclass
from ..models import ComputationalState, IonFirmware

ApplicationType = Literal['catalysis', 'conductivity', 'mechanical', 'optical', 'stability', 'custom']

@dataclass
class RecommendationResult:
    """Container for recommendation results."""
    ion: IonFirmware
    score: float
    state: ComputationalState
    matched_requirements: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ion': self.ion.value,
            'score': self.score,
            'state': self.state.to_dict(),
            'matched_requirements': self.matched_requirements
        }

class IonRecommendationSystem:
    """System for recommending optimal ion forms based on application requirements."""
    
    def __init__(self, ion_states: Dict[IonFirmware, ComputationalState]):
        self.ion_states = ion_states
        self.application_requirements = {
            'catalysis': {
                'catalytic_activity': (0.7, 1.0),
                'chemical_stability': (0.8, 1.0),
                'surface_area': (1.0, 2.0)
            },
            'conductivity': {
                'conductivity': (0.1, 1.0),
                'ion_diffusion_rate': (1.5, 3.0),
                'swelling_ratio': (0.9, 1.1)
            },
            'mechanical': {
                'mechanical_strength': (1.2, 2.0),
                'swelling_ratio': (0.8, 1.2),
                'chemical_stability': (0.7, 1.0)
            },
            'optical': {
                'optical_quality': (0.8, 1.0),
                'surface_area': (1.0, 1.5),
                'chemical_stability': (0.9, 1.0)
            },
            'stability': {
                'chemical_stability': (0.9, 1.0),
                'mechanical_strength': (1.0, 2.0),
                'thermal_power': (-500, 500)
            }
        }
    
    def recommend_for_application(
        self,
        application_type: ApplicationType,
        custom_requirements: Optional[Dict[str, Tuple[float, float]]] = None,
        min_score: float = 0.7
    ) -> List[RecommendationResult]:
        requirements = (self.application_requirements.get(application_type, {}) 
                      if application_type != 'custom' else custom_requirements or {})
        
        recommendations = []
        for ion, state in self.ion_states.items():
            score, matched = self._evaluate_ion(state, requirements)
            if score >= min_score:
                recommendations.append(RecommendationResult(
                    ion=ion, score=score, state=state, matched_requirements=matched
                ))
        
        return sorted(recommendations, key=lambda x: x.score, reverse=True)
    
    def _evaluate_ion(
        self,
        state: ComputationalState,
        requirements: Dict[str, Tuple[float, float]]
    ) -> Tuple[float, List[str]]:
        if not requirements:
            return 0.0, []
            
        matched = [
            prop for prop, (min_val, max_val) in requirements.items()
            if hasattr(state, prop) and min_val <= getattr(state, prop) <= max_val
        ]
        
        return len(matched) / len(requirements), matched
    
    def get_optimal_ion(
        self,
        application_type: ApplicationType,
        custom_requirements: Optional[Dict[str, Tuple[float, float]]] = None,
        min_score: float = 0.7
    ) -> Optional[RecommendationResult]:
        recommendations = self.recommend_for_application(
            application_type, custom_requirements, min_score
        )
        return recommendations[0] if recommendations else None
