"""
Traffic signal simulation engine.
"""
from .models import (
    IntersectionState, ArrivalProcess, SimulationMetrics,
    Direction, SignalState, Vehicle
)
from .controllers import TrafficController
import copy


class TrafficSimulator:
    """Simulates traffic flow through a signalized intersection."""
    
    def __init__(self,
                 controller: TrafficController,
                 arrival_process: ArrivalProcess,
                 saturation_flow: float = 1.0,
                 dt: float = 1.0):
        """
        Initialize simulator.
        
        Args:
            controller: Traffic signal controller
            arrival_process: Vehicle arrival process
            saturation_flow: Vehicles that can depart per second during green (per direction)
            dt: Time step duration (seconds)
        """
        self.controller = controller
        self.arrival_process = arrival_process
        self.saturation_flow = saturation_flow
        self.dt = dt
        self.state = IntersectionState()
        self.metrics = SimulationMetrics()
        self.current_time = 0.0
    
    def reset(self):
        """Reset simulation to initial state."""
        self.state = IntersectionState()
        self.metrics = SimulationMetrics()
        self.current_time = 0.0
    
    def step(self):
        """Execute one simulation time step."""
        # 1. Generate new arrivals
        new_arrivals = self.arrival_process.generate_arrivals(self.current_time, self.dt)
        for vehicle in new_arrivals:
            self.state.queues[vehicle.direction].append(vehicle)
            self.metrics.total_vehicles_arrived += 1
        
        # 2. Update signal state using controller
        new_phase, new_signal_state = self.controller.decide_signal(
            self.state, self.current_time, self.dt
        )
        self.state.active_phase = new_phase
        self.state.signal_state = new_signal_state
        
        # 3. Process departures (only during green)
        if self.state.signal_state == SignalState.GREEN:
            green_directions = self.state.get_phase_directions(self.state.active_phase)
            for direction in green_directions:
                queue = self.state.queues[direction]
                if queue:
                    # Saturation flow: depart up to saturation_flow * dt vehicles
                    n_departures = min(len(queue), int(self.saturation_flow * self.dt))
                    for _ in range(n_departures):
                        vehicle = queue.pop(0)
                        vehicle.departure_time = self.current_time
                        self.metrics.record_departure(vehicle, self.current_time)
        
        # 4. Record metrics
        for direction in Direction:
            queue_len = self.state.get_queue_length(direction)
            self.metrics.max_queue_length[direction] = max(
                self.metrics.max_queue_length[direction],
                queue_len
            )
            self.metrics.max_consecutive_skips[direction] = max(
                self.metrics.max_consecutive_skips[direction],
                self.state.consecutive_skips[direction]
            )
        
        # Record queue snapshot
        queue_snapshot = {d: self.state.get_queue_length(d) for d in Direction}
        self.metrics.queue_history.append(queue_snapshot)
        
        # Record phase/state
        self.metrics.phase_history.append((
            self.current_time,
            self.state.active_phase.value,
            self.state.signal_state.value
        ))
        
        # 5. Advance time
        self.current_time += self.dt
    
    def run(self, duration: float):
        """
        Run simulation for specified duration.
        
        Args:
            duration: Simulation duration (seconds)
        """
        self.reset()
        n_steps = int(duration / self.dt)
        for _ in range(n_steps):
            self.step()
    
    def get_metrics(self) -> SimulationMetrics:
        """Get simulation metrics."""
        return self.metrics
    
    def print_summary(self):
        """Print simulation summary."""
        print(f"\n{'='*60}")
        print(f"Controller: {self.controller.get_name()}")
        print(f"{'='*60}")
        print(f"Simulation Duration: {self.current_time:.1f} seconds")
        print(f"Total Vehicles Arrived: {self.metrics.total_vehicles_arrived}")
        print(f"Total Vehicles Departed: {self.metrics.total_vehicles_departed}")
        print(f"Vehicles Still Waiting: {self.metrics.total_vehicles_arrived - self.metrics.total_vehicles_departed}")
        print(f"\nWait Time Statistics:")
        print(f"  Average Wait Time: {self.metrics.get_average_wait_time():.2f} seconds")
        print(f"  95th Percentile Wait: {self.metrics.get_percentile_wait_time(95):.2f} seconds")
        print(f"\nQueue Statistics:")
        print(f"  Max Queue Lengths:")
        for direction in Direction:
            print(f"    {direction.value}: {self.metrics.max_queue_length[direction]}")
        print(f"\nFairness Statistics:")
        print(f"  Max Consecutive Skips:")
        for direction in Direction:
            print(f"    {direction.value}: {self.metrics.max_consecutive_skips[direction]}")
        print(f"{'='*60}\n")
