"""
Demo script for animated traffic signal simulation.
Shows real-time visualization of both Fixed-Timer and Adaptive AI controllers.
"""
from simulation.models import Direction, ArrivalProcess
from simulation.controllers import FixedTimerController, AdaptiveCountController
from simulation.simulator import TrafficSimulator
from simulation.animation import create_animation
import sys
import time


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print("   ENHANCED TRAFFIC SIGNAL SIMULATION - ANIMATED DEMO")
    print("="*70)
    print("\nThis demo shows real-time animation of traffic signal simulation.")
    print("Compare Fixed-Timer vs Adaptive AI controllers with various scenarios.\n")


def get_traffic_scenario():
    """Let user select a predefined traffic scenario."""
    print("\n" + "-"*70)
    print("SELECT TRAFFIC SCENARIO:")
    print("-"*70)
    print("  1. Balanced Traffic (all directions equal)")
    print("  2. Rush Hour North (heavy northbound traffic)")
    print("  3. Asymmetric (varying loads)")
    print("  4. Light Traffic (low volume)")
    print("  5. Custom (enter your own rates)")
    
    scenario_choice = input("\nEnter scenario (1-5) [default: 3]: ").strip() or "3"
    
    scenarios = {
        "1": {
            "name": "Balanced Traffic",
            "rates": {Direction.NORTH: 0.3, Direction.SOUTH: 0.3, 
                     Direction.EAST: 0.3, Direction.WEST: 0.3}
        },
        "2": {
            "name": "Rush Hour North",
            "rates": {Direction.NORTH: 0.6, Direction.SOUTH: 0.2, 
                     Direction.EAST: 0.15, Direction.WEST: 0.15}
        },
        "3": {
            "name": "Asymmetric Traffic",
            "rates": {Direction.NORTH: 0.4, Direction.SOUTH: 0.3, 
                     Direction.EAST: 0.2, Direction.WEST: 0.15}
        },
        "4": {
            "name": "Light Traffic",
            "rates": {Direction.NORTH: 0.1, Direction.SOUTH: 0.1, 
                     Direction.EAST: 0.1, Direction.WEST: 0.1}
        }
    }
    
    if scenario_choice == "5":
        print("\nEnter arrival rates (vehicles/second):")
        rates = {}
        for direction in Direction:
            rate_input = input(f"  {direction.value}: ").strip()
            rates[direction] = float(rate_input) if rate_input else 0.3
        return "Custom Scenario", rates
    
    scenario = scenarios.get(scenario_choice, scenarios["3"])
    return scenario["name"], scenario["rates"]


def get_controller_choice():
    """Get user's controller selection."""
    print("\n" + "-"*70)
    print("SELECT CONTROLLER:")
    print("-"*70)
    print("  1. Fixed-Timer Controller (traditional)")
    print("  2. Adaptive AI Controller (intelligent)")
    print("  3. Side-by-Side Comparison (both sequential)")
    
    choice = input("\nEnter choice (1/2/3) [default: 3]: ").strip() or "3"
    return choice


def get_simulation_parameters():
    """Get simulation parameters from user."""
    print("\n" + "-"*70)
    print("SIMULATION PARAMETERS:")
    print("-"*70)
    
    duration_input = input("  Simulation duration in seconds [default: 120]: ").strip()
    duration = float(duration_input) if duration_input else 120.0
    
    speed_input = input("  Animation speed multiplier (1.0=real-time, 2.0=2x) [default: 1.5]: ").strip()
    speed = float(speed_input) if speed_input else 1.5
    
    save_choice = input("  Save animation as GIF? (y/n) [default: n]: ").strip().lower()
    save_animation = save_choice == 'y'
    
    return duration, speed, save_animation


def print_scenario_info(scenario_name, arrival_rates, duration, speed):
    """Print scenario information."""
    print(f"\n{'='*70}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*70}")
    print("Arrival Rates (vehicles/second):")
    for direction, rate in arrival_rates.items():
        bar = "█" * int(rate * 20)
        print(f"  {direction.value:5s}: {rate:4.2f} {bar}")
    print(f"\nDuration: {duration}s | Speed: {speed}x")
    print(f"{'='*70}\n")


def run_simulation(controller, arrival_rates, duration, speed, save_path, controller_name):
    """Run a single simulation with given parameters."""
    print(f"\n{'─'*70}")
    print(f"▶ Running: {controller_name}")
    print(f"{'─'*70}")
    
    start_time = time.time()
    
    arrival_process = ArrivalProcess(arrival_rates, seed=42)
    simulator = TrafficSimulator(
        controller=controller,
        arrival_process=arrival_process,
        saturation_flow=1.0,
        dt=1.0
    )
    
    animator = create_animation(simulator, duration, speed, save_path)
    
    elapsed = time.time() - start_time
    
    # Print detailed summary
    print(f"\n{'─'*70}")
    print(f"✓ {controller_name} - RESULTS")
    print(f"{'─'*70}")
    simulator.print_summary()
    print(f"\nExecution Time: {elapsed:.1f}s")
    print(f"{'─'*70}")
    
    animator.close()
    return simulator.metrics


def print_comparison(metrics_fixed, metrics_adaptive):
    """Print comparison between two controllers."""
    print(f"\n{'='*70}")
    print("📊 PERFORMANCE COMPARISON")
    print(f"{'='*70}")
    
    avg_wait_fixed = metrics_fixed.get_average_wait_time()
    avg_wait_adaptive = metrics_adaptive.get_average_wait_time()
    improvement = ((avg_wait_fixed - avg_wait_adaptive) / avg_wait_fixed * 100) if avg_wait_fixed > 0 else 0
    
    print(f"\nAverage Wait Time:")
    print(f"  Fixed-Timer:  {avg_wait_fixed:6.2f}s")
    print(f"  Adaptive AI:  {avg_wait_adaptive:6.2f}s")
    print(f"  Improvement:  {improvement:6.1f}% {'✓' if improvement > 0 else '✗'}")
    
    print(f"\nTotal Vehicles Departed:")
    print(f"  Fixed-Timer:  {metrics_fixed.total_vehicles_departed}")
    print(f"  Adaptive AI:  {metrics_adaptive.total_vehicles_departed}")
    
    print(f"\nMax Queue Length:")
    max_fixed = metrics_fixed.get_max_queue_length_total()
    max_adaptive = metrics_adaptive.get_max_queue_length_total()
    print(f"  Fixed-Timer:  {max_fixed}")
    print(f"  Adaptive AI:  {max_adaptive}")
    
    print(f"\n95th Percentile Wait Time:")
    p95_fixed = metrics_fixed.get_percentile_wait_time(95)
    p95_adaptive = metrics_adaptive.get_percentile_wait_time(95)
    print(f"  Fixed-Timer:  {p95_fixed:6.2f}s")
    print(f"  Adaptive AI:  {p95_adaptive:6.2f}s")
    
    print(f"\n{'='*70}")
    if improvement > 10:
        print("🎯 Adaptive AI shows SIGNIFICANT improvement!")
    elif improvement > 0:
        print("✓ Adaptive AI shows modest improvement.")
    else:
        print("⚠ Fixed-Timer performed similarly or better.")
    print(f"{'='*70}\n")


def main():
    """Run enhanced animated traffic signal simulation demo."""
    print_banner()
    
    # Get user inputs
    scenario_name, arrival_rates = get_traffic_scenario()
    choice = get_controller_choice()
    duration, speed, save_animation = get_simulation_parameters()
    
    # Display scenario info
    print_scenario_info(scenario_name, arrival_rates, duration, speed)
    
    # Run simulations based on choice
    metrics_fixed = None
    metrics_adaptive = None
    
    if choice in ['1', '3']:
        controller = FixedTimerController(green_time=20.0, yellow_time=3.0)
        save_path = "fixed_timer_animation.gif" if save_animation else None
        metrics_fixed = run_simulation(
            controller, arrival_rates, duration, speed, save_path,
            "Fixed-Timer Controller"
        )
    
    if choice in ['2', '3']:
        controller = AdaptiveCountController(
            min_green=5.0,
            max_green=30.0,
            yellow_time=3.0,
            extension_threshold=2,
            max_wait_time=90.0,
            max_skips=3
        )
        save_path = "adaptive_animation.gif" if save_animation else None
        metrics_adaptive = run_simulation(
            controller, arrival_rates, duration, speed, save_path,
            "Adaptive AI Controller"
        )
    
    # Show comparison if both were run
    if choice == '3' and metrics_fixed and metrics_adaptive:
        print_comparison(metrics_fixed, metrics_adaptive)
    
    # Final message
    print("\n" + "="*70)
    print("✓ SIMULATION COMPLETE!")
    if save_animation:
        print("\n📁 Animation(s) saved as GIF file(s) in the current directory.")
    print("\n💡 Tip: Try different scenarios to see how controllers adapt!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Animation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
