"""
Visualize traffic signal simulation results.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from simulation.models import Direction
from simulation.controllers import FixedTimerController, AdaptiveCountController
from simulation.simulator import TrafficSimulator
from simulation.models import ArrivalProcess


def plot_queue_lengths(simulators: dict, duration: int = 600):
    """
    Plot queue lengths over time for both controllers.
    
    Args:
        simulators: Dictionary with 'fixed' and 'adaptive' simulators
        duration: Time window to plot (seconds)
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    for idx, (controller_name, simulator) in enumerate(simulators.items()):
        ax = axes[idx]
        metrics = simulator.get_metrics()
        
        # Extract queue history (limit to duration)
        n_steps = min(duration, len(metrics.queue_history))
        time_steps = np.arange(n_steps)
        
        # Plot each direction
        for direction in Direction:
            queue_data = [metrics.queue_history[i][direction] for i in range(n_steps)]
            ax.plot(time_steps, queue_data, label=direction.value, linewidth=1.5)
        
        ax.set_xlabel('Time (seconds)', fontsize=11)
        ax.set_ylabel('Queue Length (vehicles)', fontsize=11)
        ax.set_title(f'{controller_name.capitalize()} Controller - Queue Lengths Over Time', 
                    fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/queue_lengths.png', dpi=150, bbox_inches='tight')
    print("Saved: results/queue_lengths.png")
    plt.close()


def plot_phase_timeline(simulators: dict, duration: int = 300):
    """
    Plot signal phase timeline showing green/yellow/red periods.
    
    Args:
        simulators: Dictionary with 'fixed' and 'adaptive' simulators
        duration: Time window to plot (seconds)
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 6))
    
    colors = {'G': 'green', 'Y': 'yellow', 'R': 'red'}
    
    for idx, (controller_name, simulator) in enumerate(simulators.items()):
        ax = axes[idx]
        metrics = simulator.get_metrics()
        
        # Extract phase history (limit to duration)
        phase_history = [p for p in metrics.phase_history if p[0] <= duration]
        
        # Plot NS phase
        ns_times = []
        ns_colors = []
        for time, phase, state in phase_history:
            if phase == 'NS':
                ns_times.append(time)
                ns_colors.append(colors[state])
            else:
                ns_times.append(time)
                ns_colors.append('red')
        
        # Plot EW phase
        ew_times = []
        ew_colors = []
        for time, phase, state in phase_history:
            if phase == 'EW':
                ew_times.append(time)
                ew_colors.append(colors[state])
            else:
                ew_times.append(time)
                ew_colors.append('red')
        
        # Create scatter plots
        ax.scatter(ns_times, [1]*len(ns_times), c=ns_colors, s=10, marker='s', label='NS Phase')
        ax.scatter(ew_times, [0]*len(ew_times), c=ew_colors, s=10, marker='s', label='EW Phase')
        
        ax.set_xlabel('Time (seconds)', fontsize=11)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['EW', 'NS'])
        ax.set_title(f'{controller_name.capitalize()} Controller - Signal Phase Timeline', 
                    fontsize=12, fontweight='bold')
        ax.set_xlim(0, duration)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add legend for colors
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', label='Green'),
            Patch(facecolor='yellow', label='Yellow'),
            Patch(facecolor='red', label='Red')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('results/phase_timeline.png', dpi=150, bbox_inches='tight')
    print("Saved: results/phase_timeline.png")
    plt.close()


def plot_comparison_bars(df: pd.DataFrame):
    """
    Plot bar chart comparing key metrics between controllers.
    
    Args:
        df: DataFrame with experiment results
    """
    grouped = df.groupby('controller').mean()
    
    metrics = [
        ('avg_wait_time', 'Avg Wait Time (s)', False),
        ('p95_wait_time', '95th %ile Wait (s)', False),
        ('max_queue_total', 'Max Queue Length', False),
        ('throughput', 'Throughput (veh/s)', True),
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    
    for idx, (metric, label, higher_better) in enumerate(metrics):
        ax = axes[idx]
        
        fixed_val = grouped.loc['fixed', metric]
        adaptive_val = grouped.loc['adaptive', metric]
        
        bars = ax.bar(['Fixed Timer', 'Adaptive'], 
                     [fixed_val, adaptive_val],
                     color=['#FF6B6B', '#4ECDC4'],
                     edgecolor='black',
                     linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontweight='bold')
        
        # Calculate improvement
        if higher_better:
            improvement = ((adaptive_val - fixed_val) / fixed_val) * 100
        else:
            improvement = ((fixed_val - adaptive_val) / fixed_val) * 100
        
        ax.set_ylabel(label, fontsize=11)
        ax.set_title(f'{label}\n(Improvement: {improvement:+.1f}%)', 
                    fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Fixed Timer vs Adaptive Controller Comparison', 
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('results/comparison_bars.png', dpi=150, bbox_inches='tight')
    print("Saved: results/comparison_bars.png")
    plt.close()


def plot_wait_time_distribution(simulators: dict):
    """
    Plot wait time distributions for both controllers.
    
    Args:
        simulators: Dictionary with 'fixed' and 'adaptive' simulators
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for controller_name, simulator in simulators.items():
        metrics = simulator.get_metrics()
        wait_times = metrics.wait_times
        
        # Plot histogram
        ax.hist(wait_times, bins=50, alpha=0.6, label=controller_name.capitalize(),
               edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Wait Time (seconds)', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title('Wait Time Distribution Comparison', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/wait_time_distribution.png', dpi=150, bbox_inches='tight')
    print("Saved: results/wait_time_distribution.png")
    plt.close()


def recreate_simulators():
    """Recreate simulators from first seed for visualization."""
    arrival_rates = {
        Direction.NORTH: 0.4,
        Direction.SOUTH: 0.3,
        Direction.EAST: 0.2,
        Direction.WEST: 0.15,
    }
    
    simulators = {}
    
    # Fixed controller
    controller_fixed = FixedTimerController(green_time=20.0, yellow_time=3.0)
    arrival_process_fixed = ArrivalProcess(arrival_rates, seed=0)
    sim_fixed = TrafficSimulator(controller_fixed, arrival_process_fixed, saturation_flow=1.0, dt=1.0)
    sim_fixed.run(1800.0)
    simulators['fixed'] = sim_fixed
    
    # Adaptive controller
    controller_adaptive = AdaptiveCountController(
        min_green=5.0, max_green=30.0, yellow_time=3.0,
        extension_threshold=2, max_wait_time=90.0, max_skips=3
    )
    arrival_process_adaptive = ArrivalProcess(arrival_rates, seed=0)
    sim_adaptive = TrafficSimulator(controller_adaptive, arrival_process_adaptive, saturation_flow=1.0, dt=1.0)
    sim_adaptive.run(1800.0)
    simulators['adaptive'] = sim_adaptive
    
    return simulators


def main():
    """Main plotting function."""
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70 + "\n")
    
    # Load results
    try:
        df = pd.read_csv('results/experiment_results.csv')
    except FileNotFoundError:
        print("Error: results/experiment_results.csv not found.")
        print("Please run 'python run_experiments.py' first.")
        return
    
    # Recreate simulators for visualization
    print("Recreating simulations for visualization...")
    simulators = recreate_simulators()
    print("Done.\n")
    
    # Generate plots
    print("Generating plots...")
    plot_comparison_bars(df)
    plot_queue_lengths(simulators, duration=600)
    plot_phase_timeline(simulators, duration=300)
    plot_wait_time_distribution(simulators)
    
    print("\n" + "="*70)
    print("All visualizations saved to results/ directory!")
    print("="*70)


if __name__ == "__main__":
    import os
    os.makedirs('results', exist_ok=True)
    main()
