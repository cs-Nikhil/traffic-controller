"""
Core data structures for traffic signal simulation.
"""
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum
import numpy as np


class Direction(Enum):
    """Four approaches to the intersection."""
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


class SignalPhase(Enum):
    """Two-phase signal control."""
    NS = "NS"  # North-South green
    EW = "EW"  # East-West green


class SignalState(Enum):
    """Signal light states."""
    GREEN = "G"
    YELLOW = "Y"
    RED = "R"


@dataclass
class Vehicle:
    """Represents a single vehicle."""
    arrival_time: float
    direction: Direction
    departure_time: float = None


@dataclass
class IntersectionState:
    """Current state of the intersection."""
    queues: Dict[Direction, List[Vehicle]] = field(default_factory=lambda: {
        Direction.NORTH: [],
        Direction.EAST: [],
        Direction.SOUTH: [],
        Direction.WEST: []
    })
    active_phase: SignalPhase = SignalPhase.NS
    signal_state: SignalState = SignalState.GREEN
    phase_timer: float = 0.0  # Time in current state
    time_since_green: Dict[Direction, float] = field(default_factory=lambda: {
        Direction.NORTH: 0.0,
        Direction.EAST: 0.0,
        Direction.SOUTH: 0.0,
        Direction.WEST: 0.0
    })
    consecutive_skips: Dict[Direction, int] = field(default_factory=lambda: {
        Direction.NORTH: 0,
        Direction.EAST: 0,
        Direction.SOUTH: 0,
        Direction.WEST: 0
    })
    
    def get_queue_length(self, direction: Direction) -> int:
        """Get number of vehicles waiting in a direction."""
        return len(self.queues[direction])
    
    def get_phase_queue_length(self, phase: SignalPhase) -> int:
        """Get total vehicles waiting for a phase."""
        if phase == SignalPhase.NS:
            return self.get_queue_length(Direction.NORTH) + self.get_queue_length(Direction.SOUTH)
        else:
            return self.get_queue_length(Direction.EAST) + self.get_queue_length(Direction.WEST)
    
    def get_phase_directions(self, phase: SignalPhase) -> List[Direction]:
        """Get directions served by a phase."""
        if phase == SignalPhase.NS:
            return [Direction.NORTH, Direction.SOUTH]
        else:
            return [Direction.EAST, Direction.WEST]
    
    def get_opposing_phase(self, phase: SignalPhase) -> SignalPhase:
        """Get the opposing phase."""
        return SignalPhase.EW if phase == SignalPhase.NS else SignalPhase.NS


class ArrivalProcess:
    """Generates vehicle arrivals using Poisson process."""
    
    def __init__(self, arrival_rates: Dict[Direction, float], seed: int = None):
        """
        Initialize arrival process.
        
        Args:
            arrival_rates: Dictionary mapping Direction to arrival rate (vehicles/second)
            seed: Random seed for reproducibility
        """
        self.arrival_rates = arrival_rates
        self.rng = np.random.RandomState(seed)
    
    def generate_arrivals(self, current_time: float, dt: float) -> List[Vehicle]:
        """
        Generate vehicle arrivals for time step.
        
        Args:
            current_time: Current simulation time
            dt: Time step duration
            
        Returns:
            List of new vehicles
        """
        arrivals = []
        for direction, rate in self.arrival_rates.items():
            # Poisson: number of arrivals in dt
            n_arrivals = self.rng.poisson(rate * dt)
            for _ in range(n_arrivals):
                arrivals.append(Vehicle(
                    arrival_time=current_time,
                    direction=direction
                ))
        return arrivals


@dataclass
class SimulationMetrics:
    """Tracks performance metrics during simulation."""
    total_vehicles_arrived: int = 0
    total_vehicles_departed: int = 0
    total_wait_time: float = 0.0
    max_queue_length: Dict[Direction, int] = field(default_factory=lambda: {
        Direction.NORTH: 0,
        Direction.EAST: 0,
        Direction.SOUTH: 0,
        Direction.WEST: 0
    })
    wait_times: List[float] = field(default_factory=list)
    queue_history: List[Dict[Direction, int]] = field(default_factory=list)
    phase_history: List[tuple] = field(default_factory=list)  # (time, phase, state)
    max_consecutive_skips: Dict[Direction, int] = field(default_factory=lambda: {
        Direction.NORTH: 0,
        Direction.EAST: 0,
        Direction.SOUTH: 0,
        Direction.WEST: 0
    })
    
    def record_departure(self, vehicle: Vehicle, departure_time: float):
        """Record a vehicle departure."""
        wait_time = departure_time - vehicle.arrival_time
        self.total_vehicles_departed += 1
        self.total_wait_time += wait_time
        self.wait_times.append(wait_time)
    
    def get_average_wait_time(self) -> float:
        """Calculate average wait time."""
        if self.total_vehicles_departed == 0:
            return 0.0
        return self.total_wait_time / self.total_vehicles_departed
    
    def get_percentile_wait_time(self, percentile: float) -> float:
        """Calculate percentile wait time."""
        if not self.wait_times:
            return 0.0
        return np.percentile(self.wait_times, percentile)
    
    def get_max_queue_length_total(self) -> int:
        """Get maximum queue length across all directions."""
        return max(self.max_queue_length.values())
