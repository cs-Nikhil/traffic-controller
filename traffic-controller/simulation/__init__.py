"""
Traffic signal simulation package with AI-based adaptive control.
"""
from .models import (
    Direction, SignalPhase, SignalState, Vehicle,
    IntersectionState, ArrivalProcess, SimulationMetrics
)
from .controllers import TrafficController, FixedTimerController, AdaptiveCountController
from .simulator import TrafficSimulator
from .animation import TrafficAnimator, create_animation

__all__ = [
    'Direction', 'SignalPhase', 'SignalState', 'Vehicle',
    'IntersectionState', 'ArrivalProcess', 'SimulationMetrics',
    'TrafficController', 'FixedTimerController', 'AdaptiveCountController',
    'TrafficSimulator', 'TrafficAnimator', 'create_animation'
]
