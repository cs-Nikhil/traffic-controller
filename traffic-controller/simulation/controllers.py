"""
Traffic signal controllers: Fixed-timer and Adaptive AI-based.
"""
from abc import ABC, abstractmethod
from .models import IntersectionState, SignalPhase, SignalState, Direction
from typing import Tuple


class TrafficController(ABC):
    """Base class for traffic signal controllers."""
    
    @abstractmethod
    def decide_signal(self, state: IntersectionState, current_time: float, dt: float) -> Tuple[SignalPhase, SignalState]:
        """
        Decide the signal phase and state for the next time step.
        
        Args:
            state: Current intersection state
            current_time: Current simulation time
            dt: Time step duration
            
        Returns:
            Tuple of (phase, signal_state)
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return controller name."""
        pass


class FixedTimerController(TrafficController):
    """Traditional fixed-timer traffic signal controller."""
    
    def __init__(self, green_time: float = 20.0, yellow_time: float = 3.0):
        """
        Initialize fixed-timer controller.
        
        Args:
            green_time: Duration of green light (seconds)
            yellow_time: Duration of yellow light (seconds)
        """
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.cycle_time = 2 * (green_time + yellow_time)
    
    def decide_signal(self, state: IntersectionState, current_time: float, dt: float) -> Tuple[SignalPhase, SignalState]:
        """Fixed-timer decision logic."""
        state.phase_timer += dt
        
        if state.signal_state == SignalState.GREEN:
            if state.phase_timer >= self.green_time:
                # Switch to yellow
                state.phase_timer = 0.0
                return state.active_phase, SignalState.YELLOW
            else:
                return state.active_phase, SignalState.GREEN
        
        elif state.signal_state == SignalState.YELLOW:
            if state.phase_timer >= self.yellow_time:
                # Switch to next phase (green)
                state.phase_timer = 0.0
                next_phase = state.get_opposing_phase(state.active_phase)
                return next_phase, SignalState.GREEN
            else:
                return state.active_phase, SignalState.YELLOW
        
        return state.active_phase, state.signal_state
    
    def get_name(self) -> str:
        return f"FixedTimer(G={self.green_time}s)"


class AdaptiveCountController(TrafficController):
    """AI-based adaptive controller using vehicle counts."""
    
    def __init__(self, 
                 min_green: float = 5.0,
                 max_green: float = 30.0,
                 yellow_time: float = 3.0,
                 extension_threshold: int = 2,
                 max_wait_time: float = 90.0,
                 max_skips: int = 3):
        """
        Initialize adaptive controller.
        
        Args:
            min_green: Minimum green time (seconds)
            max_green: Maximum green time (seconds)
            yellow_time: Duration of yellow light (seconds)
            extension_threshold: Extend green if queue >= this threshold
            max_wait_time: Force phase change if opposing waited this long (seconds)
            max_skips: Force phase change if opposing skipped this many times
        """
        self.min_green = min_green
        self.max_green = max_green
        self.yellow_time = yellow_time
        self.extension_threshold = extension_threshold
        self.max_wait_time = max_wait_time
        self.max_skips = max_skips
    
    def decide_signal(self, state: IntersectionState, current_time: float, dt: float) -> Tuple[SignalPhase, SignalState]:
        """Adaptive decision logic based on vehicle counts and fairness."""
        state.phase_timer += dt
        
        # Update time since green for all directions
        for direction in Direction:
            if direction in state.get_phase_directions(state.active_phase) and state.signal_state == SignalState.GREEN:
                state.time_since_green[direction] = 0.0
            else:
                state.time_since_green[direction] += dt
        
        if state.signal_state == SignalState.GREEN:
            # Check if we should extend or terminate green
            current_queue = state.get_phase_queue_length(state.active_phase)
            opposing_phase = state.get_opposing_phase(state.active_phase)
            opposing_queue = state.get_phase_queue_length(opposing_phase)
            
            # Check fairness constraints
            opposing_dirs = state.get_phase_directions(opposing_phase)
            max_opposing_wait = max(state.time_since_green[d] for d in opposing_dirs)
            max_opposing_skips = max(state.consecutive_skips[d] for d in opposing_dirs)
            
            # Force switch if fairness violated
            force_switch = (max_opposing_wait >= self.max_wait_time or 
                          max_opposing_skips >= self.max_skips)
            
            # Decide whether to switch
            should_switch = False
            
            if force_switch and state.phase_timer >= self.min_green:
                should_switch = True
            elif state.phase_timer >= self.max_green:
                should_switch = True
            elif state.phase_timer >= self.min_green:
                # Switch if current queue is empty or opposing has more vehicles
                if current_queue == 0 or (opposing_queue > current_queue + self.extension_threshold):
                    should_switch = True
            
            if should_switch:
                # Switch to yellow
                state.phase_timer = 0.0
                # Update consecutive skips
                for direction in state.get_phase_directions(state.active_phase):
                    state.consecutive_skips[direction] = 0
                for direction in opposing_dirs:
                    state.consecutive_skips[direction] += 1
                return state.active_phase, SignalState.YELLOW
            else:
                return state.active_phase, SignalState.GREEN
        
        elif state.signal_state == SignalState.YELLOW:
            if state.phase_timer >= self.yellow_time:
                # Switch to next phase (green)
                state.phase_timer = 0.0
                next_phase = state.get_opposing_phase(state.active_phase)
                # Reset consecutive skips for new green phase
                for direction in state.get_phase_directions(next_phase):
                    state.consecutive_skips[direction] = 0
                return next_phase, SignalState.GREEN
            else:
                return state.active_phase, SignalState.YELLOW
        
        return state.active_phase, state.signal_state
    
    def get_name(self) -> str:
        return f"AdaptiveCount(min={self.min_green}s,max={self.max_green}s)"
