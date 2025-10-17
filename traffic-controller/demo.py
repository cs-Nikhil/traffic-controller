"""
Quick demo script to see the simulation in action.
Runs a short 5-minute simulation with both controllers.
"""
from simulation.models import Direction, ArrivalProcess
from simulation.controllers import FixedTimerController, AdaptiveCountController
from simulation.simulator import TrafficSimulator


def run_demo():
    """Run a quick demo comparing both controllers."""
    print("\n" + "="*70)
    print("TRAFFIC SIGNAL SIMULATION - QUICK DEMO")
    print("="*70)
    print("\nThis demo runs a 5-minute simulation with both controllers.")
    print("For full experiments and visualizations, run: python run_experiments.py\n")
    
    # Define traffic scenario
    arrival_rates = {
        Direction.NORTH: 0.4,   # Busy direction
        Direction.SOUTH: 0.3,   # Moderate
        Direction.EAST: 0.2,    # Light
        Direction.WEST: 0.15,   # Light
    }
    
    print("Traffic Arrival Rates (vehicles/second):")
    for direction, rate in arrival_rates.items():
        print(f"  {direction.value}: {rate}")
    
    duration = 300.0  # 5 minutes
    print(f"\nSimulation Duration: {duration/60:.1f} minutes\n")
    
    # Run Fixed-Timer Controller
    print("-" * 70)
    print("Running Fixed-Timer Controller...")
    print("-" * 70)
    
    controller_fixed = FixedTimerController(green_time=20.0, yellow_time=3.0)
    arrival_process_fixed = ArrivalProcess(arrival_rates, seed=42)
    sim_fixed = TrafficSimulator(
        controller=controller_fixed,
        arrival_process=arrival_process_fixed,
        saturation_flow=1.0,
        dt=1.0
    )
    sim_fixed.run(duration)
    sim_fixed.print_summary()
    
    # Run Adaptive Controller
    print("-" * 70)
    print("Running Adaptive Controller...")
    print("-" * 70)
    
    controller_adaptive = AdaptiveCountController(
        min_green=5.0,
        max_green=30.0,
        yellow_time=3.0,
        extension_threshold=2,
        max_wait_time=90.0,
        max_skips=3
    )
    arrival_process_adaptive = ArrivalProcess(arrival_rates, seed=42)
    sim_adaptive = TrafficSimulator(
        controller=controller_adaptive,
        arrival_process=arrival_process_adaptive,
        saturation_flow=1.0,
        dt=1.0
    )
    sim_adaptive.run(duration)
    sim_adaptive.print_summary()
    
    # Quick comparison
    print("\n" + "="*70)
    print("QUICK COMPARISON")
    print("="*70)
    
    fixed_metrics = sim_fixed.get_metrics()
    adaptive_metrics = sim_adaptive.get_metrics()
    
    fixed_avg_wait = fixed_metrics.get_average_wait_time()
    adaptive_avg_wait = adaptive_metrics.get_average_wait_time()
    wait_improvement = ((fixed_avg_wait - adaptive_avg_wait) / fixed_avg_wait) * 100
    
    fixed_p95 = fixed_metrics.get_percentile_wait_time(95)
    adaptive_p95 = adaptive_metrics.get_percentile_wait_time(95)
    p95_improvement = ((fixed_p95 - adaptive_p95) / fixed_p95) * 100
    
    fixed_throughput = fixed_metrics.total_vehicles_departed / duration
    adaptive_throughput = adaptive_metrics.total_vehicles_departed / duration
    throughput_improvement = ((adaptive_throughput - fixed_throughput) / fixed_throughput) * 100
    
    print(f"\nAverage Wait Time:")
    print(f"  Fixed:    {fixed_avg_wait:.2f}s")
    print(f"  Adaptive: {adaptive_avg_wait:.2f}s")
    print(f"  Improvement: {wait_improvement:+.1f}%")
    
    print(f"\n95th Percentile Wait:")
    print(f"  Fixed:    {fixed_p95:.2f}s")
    print(f"  Adaptive: {adaptive_p95:.2f}s")
    print(f"  Improvement: {p95_improvement:+.1f}%")
    
    print(f"\nThroughput (vehicles/second):")
    print(f"  Fixed:    {fixed_throughput:.3f}")
    print(f"  Adaptive: {adaptive_throughput:.3f}")
    print(f"  Improvement: {throughput_improvement:+.1f}%")
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("\nFor comprehensive analysis:")
    print("  1. Run: python run_experiments.py")
    print("  2. Then: python plot_results.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_demo()
