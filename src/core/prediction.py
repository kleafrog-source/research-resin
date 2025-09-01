"""
Machine learning models for predicting resin properties based on ion characteristics.
"""
from typing import Dict, List, Optional, Any
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from ..models import IonFirmware, ComputationalState

class PropertyPredictor:
    """
    A class for predicting resin properties using machine learning models.
    
    This class trains and uses machine learning models to predict various
    properties of resin based on ion characteristics.
    """
    
    def __init__(self):
        """Initialize the predictor with empty models and feature importances."""
        self.models: Dict[str, Any] = {}
        self.feature_importances: Dict[str, np.ndarray] = {}
        self._initialize_ion_properties()
    
    def _initialize_ion_properties(self):
        """Initialize the ion properties database."""
        self.ion_properties = {
            IonFirmware.H_PLUS: {
                'name': 'H+',
                'charge': 1,
                'radius': 0.28,  # in nm
                'hydration_energy': 1090,  # kJ/mol
                'electronegativity': 2.2,
                'hydration_number': 4
            },
            IonFirmware.NA_PLUS: {
                'name': 'Na+',
                'charge': 1,
                'radius': 0.36,
                'hydration_energy': 405,
                'electronegativity': 0.93,
                'hydration_number': 6
            },
            IonFirmware.K_PLUS: {
                'name': 'K+',
                'charge': 1,
                'radius': 0.48,
                'hydration_energy': 295,
                'electronegativity': 0.82,
                'hydration_number': 6
            },
            IonFirmware.CA_2PLUS: {
                'name': 'Ca2+',
                'charge': 2,
                'radius': 0.46,
                'hydration_energy': 1577,
                'electronegativity': 1.0,
                'hydration_number': 6
            },
            IonFirmware.MG_2PLUS: {
                'name': 'Mg2+',
                'charge': 2,
                'radius': 0.36,
                'hydration_energy': 1830,
                'electronegativity': 1.31,
                'hydration_number': 6
            },
            IonFirmware.FE_3PLUS: {
                'name': 'Fe3+',
                'charge': 3,
                'radius': 0.39,
                'hydration_energy': 4294,
                'electronegativity': 1.83,
                'hydration_number': 6
            },
            IonFirmware.AL_3PLUS: {
                'name': 'Al3+',
                'charge': 3,
                'radius': 0.34,
                'hydration_energy': 4530,
                'electronegativity': 1.61,
                'hydration_number': 6
            },
            IonFirmware.CU_2PLUS: {
                'name': 'Cu2+',
                'charge': 2,
                'radius': 0.44,
                'hydration_energy': 2100,
                'electronegativity': 1.9,
                'hydration_number': 6
            },
            IonFirmware.ZN_2PLUS: {
                'name': 'Zn2+',
                'charge': 2,
                'radius': 0.44,
                'hydration_energy': 2020,
                'electronegativity': 1.65,
                'hydration_number': 6
            }
        }
    
    def train_models(self, ion_states: Dict[IonFirmware, ComputationalState]):
        """
        Train machine learning models for each property.
        
        Args:
            ion_states: Dictionary mapping ions to their ComputationalState
        """
        # Prepare training data
        X = []  # Features: [charge, radius, hydration_energy, electronegativity, hydration_number]
        y = {prop: [] for prop in [
            'conductivity', 'catalytic_activity', 'swelling_ratio',
            'mechanical_strength', 'ion_diffusion_rate', 'selectivity_coefficient',
            'chemical_stability', 'optical_quality', 'surface_area'
        ]}
        
        # Collect data for training
        for ion, state in ion_states.items():
            if ion in self.ion_properties:
                props = self.ion_properties[ion]
                X.append([
                    props['charge'],
                    props['radius'],
                    props['hydration_energy'],
                    props['electronegativity'],
                    props['hydration_number']
                ])
                
                for prop in y.keys():
                    y[prop].append(getattr(state, prop))
        
        X = np.array(X)
        
        # Train a model for each property
        for prop, values in y.items():
            if len(values) < 3:  # Need at least 3 samples for meaningful training
                continue
                
            y_arr = np.array(values)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_arr, test_size=0.2, random_state=42
            )
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Store model and feature importances
            self.models[prop] = model
            self.feature_importances[prop] = model.feature_importances_
    
    def predict_for_new_ion(self, charge: float, radius: float, hydration_energy: float,
                          electronegativity: float, hydration_number: int) -> Dict[str, float]:
        """
        Predict properties for a new ion.
        
        Args:
            charge: Ion charge
            radius: Ion radius (nm)
            hydration_energy: Hydration energy (kJ/mol)
            electronegativity: Pauling electronegativity
            hydration_number: Number of water molecules in hydration shell
            
        Returns:
            Dictionary of predicted properties
        """
        X_new = np.array([[
            charge,
            radius,
            hydration_energy,
            electronegativity,
            hydration_number
        ]])
        
        predictions = {}
        for prop, model in self.models.items():
            predictions[prop] = float(model.predict(X_new)[0])
            
        return predictions
    
    def get_feature_importances(self, property_name: str) -> Dict[str, float]:
        """
        Get feature importances for a specific property.
        
        Args:
            property_name: Name of the property
            
        Returns:
            Dictionary mapping feature names to their importance scores
        """
        if property_name not in self.models:
            return {}
            
        feature_names = [
            'charge', 'radius', 'hydration_energy',
            'electronegativity', 'hydration_number'
        ]
        
        return {
            name: float(imp)
            for name, imp in zip(
                feature_names,
                self.feature_importances[property_name]
            )
        }
