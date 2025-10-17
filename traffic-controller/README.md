# AI-Based Traffic Signal Simulation

A Python-based simulation comparing traditional fixed-timer traffic signals with an intelligent adaptive controller that dynamically adjusts signal timings based on real-time vehicle counts.

## 🚦 Project Overview

Traditional traffic signals operate on fixed timers, which can cause:
- **Unnecessary delays** when one road remains red despite no vehicles
- **Congestion** when busy roads get insufficient green time
- **Unfair distribution** of green time across approaches

This project demonstrates how a simple AI-driven (rule-based) traffic signal system can:
- ✅ Dynamically adjust signal timings based on vehicle queue lengths
- ✅ Prevent starvation by ensuring fair time distribution
- ✅ Reduce average wait times and improve throughput
- ✅ Respond intelligently to varying traffic patterns

## 🏗️ Architecture

### Core Components

1. **Models** (`simulation/models.py`)
   - `IntersectionState`: Tracks queues, active phase, timers
   - `ArrivalProcess`: Generates vehicles using Poisson process
   - `SimulationMetrics`: Records performance data

2. **Controllers** (`simulation/controllers.py`)
   - `FixedTimerController`: Traditional fixed-timer (20s green, 3s yellow)
   - `AdaptiveCountController`: AI-based controller with:
     - Min/max green time constraints (5-30s)
     - Vehicle count-based decisions
     - Fairness rules (max wait time, consecutive skip limits)

3. **Simulator** (`simulation/simulator.py`)
   - Discrete-event simulation engine
   - 1-second time steps
   - Tracks arrivals, departures, queue lengths, wait times

### Traffic Model

- **Intersection**: 4 approaches (North, East, South, West)
- **Signal Phases**: 2-phase control (NS vs EW)
- **Arrivals**: Independent Poisson processes per direction
- **Saturation Flow**: 1 vehicle/second per green approach
- **Clearance**: 3-second yellow between phases

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd traffic-signal-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Simulation

1. **Run experiments** (compares both controllers across 5 random seeds):
   ```bash
   python run_experiments.py
   ```
   
   This will:
   - Simulate 30 minutes of traffic for each controller
   - Run 5 different random seeds for statistical validity
   - Save results to `results/experiment_results.csv`
   - Print detailed comparison metrics

2. **Generate visualizations:**
   ```bash
   python plot_results.py
   ```
   
   This creates:
   - `results/comparison_bars.png` - Key metrics comparison
   - `results/queue_lengths.png` - Queue evolution over time
   - `results/phase_timeline.png` - Signal phase patterns
   - `results/wait_time_distribution.png` - Wait time histograms

## 📊 Key Metrics

The simulation tracks and compares:

- **Average Wait Time**: Mean time vehicles spend waiting
- **95th Percentile Wait**: Worst-case wait time experience
- **Max Queue Length**: Peak congestion per direction
- **Throughput**: Vehicles processed per second
- **Fairness**: Max consecutive times a direction was skipped

## 🧠 Adaptive Controller Logic

The adaptive controller uses these decision rules:

1. **Minimum Green Time**: Ensures at least 5 seconds of green
2. **Maximum Green Time**: Caps green at 30 seconds to prevent starvation
3. **Extension Logic**: Extends green if:
   - Current queue still has vehicles
   - Opposing queue doesn't have significantly more vehicles
4. **Fairness Constraints**: Forces phase switch if opposing:
   - Has waited ≥ 90 seconds
   - Has been skipped ≥ 3 consecutive times

## 🎯 Expected Results

Typical improvements with adaptive controller:

- **20-30% reduction** in average wait time
- **15-25% reduction** in 95th percentile wait
- **Better fairness**: Lower consecutive skip counts
- **Higher throughput**: More efficient green time usage

## 📁 Project Structure

```
traffic-signal-ai/
├── simulation/
│   ├── __init__.py
│   ├── models.py          # Core data structures
│   ├── controllers.py     # Fixed & Adaptive controllers
│   └── simulator.py       # Simulation engine
├── results/               # Output directory (created on run)
│   ├── experiment_results.csv
│   ├── comparison_bars.png
│   ├── queue_lengths.png
│   ├── phase_timeline.png
│   └── wait_time_distribution.png
├── run_experiments.py     # Main experiment runner
├── plot_results.py        # Visualization script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Customization

### Modify Traffic Patterns

Edit arrival rates in `run_experiments.py`:

```python
arrival_rates = {
    Direction.NORTH: 0.4,  # vehicles/second
    Direction.SOUTH: 0.3,
    Direction.EAST: 0.2,
    Direction.WEST: 0.15,
}
```

### Tune Adaptive Controller

Adjust parameters in `run_experiments.py`:

```python
controller = AdaptiveCountController(
    min_green=5.0,           # Minimum green time
    max_green=30.0,          # Maximum green time
    yellow_time=3.0,         # Yellow clearance time
    extension_threshold=2,   # Queue difference threshold
    max_wait_time=90.0,      # Force switch after this wait
    max_skips=3              # Force switch after this many skips
)
```

### Change Simulation Duration

Modify in `run_experiments.py`:

```python
df, simulators = run_experiments(n_seeds=5, duration=1800.0)  # 1800s = 30 min
```

## 📚 Educational Value

This project demonstrates:

- **Discrete-event simulation** design patterns
- **Rule-based AI** for real-time decision making
- **Fairness constraints** in optimization problems
- **Statistical comparison** of algorithms
- **Data visualization** for performance analysis

Perfect for students learning:
- Python programming
- Algorithm design
- Traffic engineering concepts
- Simulation methodology
- Data analysis with pandas/matplotlib

## 🤝 Contributing

Ideas for extensions:

- [ ] Add more sophisticated AI (reinforcement learning)
- [ ] Implement multi-intersection networks
- [ ] Add pedestrian crossing phases
- [ ] Include turn lanes and movements
- [ ] Real-time visualization/animation
- [ ] Web-based interactive dashboard

## 📝 License

This project is open-source and available for educational purposes.

## 🙏 Acknowledgments

Inspired by real-world intelligent transportation systems and adaptive traffic signal control research.

---

**Author**: AI Traffic Signal Simulation Project  
**Version**: 1.0.0  
**Last Updated**: October 2025
