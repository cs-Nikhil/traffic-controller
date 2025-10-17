"""
Run traffic signal simulation experiments comparing Fixed-Timer vs Adaptive controllers.
"""
import numpy as np
import pandas as pd
from simulation.models import Direction, ArrivalProcess
from simulation.controllers import FixedTimerController, AdaptiveCountController
from simulation.simulator import TrafficSimulator


def run_single_experiment(controller_name: str, 
                         arrival_rates: dict,
                         seed: int,
                         duration: float = 1800.0):
    """
    Run a single simulation experiment.
    
    Args:
        controller_name: "fixed" or "adaptive"
        arrival_rates: Dictionary of arrival rates per direction
        seed: Random seed
        duration: Simulation duration in seconds (default 30 minutes)
        
    Returns:
        Dictionary of results
    """
    # Create controller
    if controller_name == "fixed":
        controller = FixedTimerController(green_time=20.0, yellow_time=3.0)
    else:
        controller = AdaptiveCountController(
            min_green=5.0,
            max_green=30.0,
            yellow_time=3.0,
            extension_threshold=2,
            max_wait_time=90.0,
            max_skips=3
        )
    
    # Create arrival process
    arrival_process = ArrivalProcess(arrival_rates, seed=seed)
    
    # Create and run simulator
    simulator = TrafficSimulator(
        controller=controller,
        arrival_process=arrival_process,
        saturation_flow=1.0,
        dt=1.0
    )
    
    simulator.run(duration)
    metrics = simulator.get_metrics()
    
    # Compile results
    results = {
        'controller': controller_name,
        'seed': seed,
        'total_arrived': metrics.total_vehicles_arrived,
        'total_departed': metrics.total_vehicles_departed,
        'avg_wait_time': metrics.get_average_wait_time(),
        'p95_wait_time': metrics.get_percentile_wait_time(95),
        'max_queue_total': metrics.get_max_queue_length_total(),
        'throughput': metrics.total_vehicles_departed / duration,
    }
    
    # Add per-direction metrics
    for direction in Direction:
        results[f'max_queue_{direction.value}'] = metrics.max_queue_length[direction]
        results[f'max_skips_{direction.value}'] = metrics.max_consecutive_skips[direction]
    
    return results, simulator


def run_experiments(n_seeds: int = 5, duration: float = 1800.0):
    """
    Run multiple experiments with different seeds and controllers.
    
    Args:
        n_seeds: Number of random seeds to test
        duration: Simulation duration in seconds
        
    Returns:
        DataFrame of results
    """
    # Define traffic scenario: NS is busier than EW
    arrival_rates = {
        Direction.NORTH: 0.4,  # 0.4 vehicles/second
        Direction.SOUTH: 0.3,  # 0.3 vehicles/second
        Direction.EAST: 0.2,   # 0.2 vehicles/second
        Direction.WEST: 0.15,  # 0.15 vehicles/second
    }
    
    print("="*70)
    print("TRAFFIC SIGNAL SIMULATION EXPERIMENTS")
    print("="*70)
    print(f"\nArrival Rates (vehicles/second):")
    for direction, rate in arrival_rates.items():
        print(f"  {direction.value}: {rate}")
    print(f"\nSimulation Duration: {duration/60:.1f} minutes")
    print(f"Number of Seeds: {n_seeds}")
    print(f"\nRunning experiments...\n")
    
    all_results = []
    all_simulators = {}
    
    for seed in range(n_seeds):
        print(f"Seed {seed+1}/{n_seeds}:")
        
        # Run fixed-timer
        print(f"  Running Fixed-Timer controller...")
        results_fixed, sim_fixed = run_single_experiment(
            "fixed", arrival_rates, seed, duration
        )
        all_results.append(results_fixed)
        if seed == 0:  # Save first run for visualization
            all_simulators['fixed'] = sim_fixed
        
        # Run adaptive
        print(f"  Running Adaptive controller...")
        results_adaptive, sim_adaptive = run_single_experiment(
            "adaptive", arrival_rates, seed, duration
        )
        all_results.append(results_adaptive)
        if seed == 0:  # Save first run for visualization
            all_simulators['adaptive'] = sim_adaptive
        
        print()
    
    # Create DataFrame
    df = pd.DataFrame(all_results)
    
    return df, all_simulators


def print_comparison(df: pd.DataFrame):
    """Print comparison summary between controllers."""
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    # Group by controller
    grouped = df.groupby('controller')
    
    metrics = [
        ('avg_wait_time', 'Average Wait Time (s)'),
        ('p95_wait_time', '95th Percentile Wait (s)'),
        ('max_queue_total', 'Max Queue Length'),
        ('throughput', 'Throughput (veh/s)'),
    ]
    
    print("\nPerformance Metrics (mean ± std):")
    print("-" * 70)
    
    for metric, label in metrics:
        print(f"\n{label}:")
        for controller in ['fixed', 'adaptive']:
            data = grouped.get_group(controller)[metric]
            mean = data.mean()
            std = data.std()
            print(f"  {controller:10s}: {mean:8.2f} ± {std:6.2f}")
        
        # Calculate improvement
        fixed_mean = grouped.get_group('fixed')[metric].mean()
        adaptive_mean = grouped.get_group('adaptive')[metric].mean()
        
        if metric == 'throughput':
            improvement = ((adaptive_mean - fixed_mean) / fixed_mean) * 100
            print(f"  {'Improvement':10s}: {improvement:+7.2f}%")
        else:
            improvement = ((fixed_mean - adaptive_mean) / fixed_mean) * 100
            print(f"  {'Improvement':10s}: {improvement:+7.2f}%")
    
    print("\n" + "="*70)
    
    # Fairness comparison
    print("\nFairness Metrics (Max Consecutive Skips):")
    print("-" * 70)
    for direction in ['N', 'E', 'S', 'W']:
        metric = f'max_skips_{direction}'
        print(f"\nDirection {direction}:")
        for controller in ['fixed', 'adaptive']:
            data = grouped.get_group(controller)[metric]
            mean = data.mean()
            print(f"  {controller:10s}: {mean:6.2f}")
    
    print("\n" + "="*70)


def main():
    """Main experiment runner."""
    # Run experiments
    df, simulators = run_experiments(n_seeds=5, duration=1800.0)
    
    # Save results
    df.to_csv('results/experiment_results.csv', index=False)
    print("\nResults saved to: results/experiment_results.csv")
    
    # Print comparison
    print_comparison(df)
    
    # Print individual summaries for first seed
    print("\n" + "="*70)
    print("DETAILED SUMMARY (Seed 0)")
    print("="*70)
    simulators['fixed'].print_summary()
    simulators['adaptive'].print_summary()
    
    print("\nExperiments complete! Run 'python plot_results.py' to visualize.")


if __name__ == "__main__":
    import os
    os.makedirs('results', exist_ok=True)
    main()
