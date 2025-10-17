"""
Real-time animated visualization of traffic signal simulation.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.collections import PatchCollection
from .models import Direction, SignalState, SignalPhase
from .simulator import TrafficSimulator
import numpy as np


class TrafficAnimator:
    """Animates traffic signal simulation in real-time."""
    
    def __init__(self, simulator: TrafficSimulator, speed_multiplier: float = 1.0):
        """
        Initialize animator.
        
        Args:
            simulator: Traffic simulator instance
            speed_multiplier: Animation speed (1.0 = real-time, 2.0 = 2x speed)
        """
        self.simulator = simulator
        self.speed_multiplier = speed_multiplier
        self.fig = None
        self.ax = None
        self.anim = None
        
        # Visual parameters
        self.road_width = 0.3
        self.intersection_size = 1.0
        self.vehicle_size = 0.15
        self.signal_radius = 0.12
        self.max_vehicles_display = 12  # Max vehicles to show per direction
        
        # Enhanced color scheme
        self.colors = {
            'road': '#404040',
            'intersection': '#505050',
            'lane_marking': '#FFFFFF',
            'vehicle': '#FFD700',
            'vehicle_waiting': '#FFA500',  # Orange for waiting vehicles
            'vehicle_moving': '#90EE90',   # Light green for moving vehicles
            'green': '#00FF00',
            'yellow': '#FFFF00',
            'red': '#FF0000',
            'text': '#FFFFFF',
            'background': '#1a1a1a',
            'info_bg': '#2a2a2a',
            'highlight': '#00BFFF'
        }
        
    def setup_figure(self):
        """Setup the matplotlib figure and axes with enhanced layout."""
        self.fig, self.ax = plt.subplots(figsize=(14, 11), facecolor=self.colors['background'])
        self.ax.set_xlim(-3.5, 3.5)
        self.ax.set_ylim(-3.5, 3.5)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_facecolor(self.colors['background'])
        
        # Add enhanced title
        self.title = self.fig.suptitle(
            f'Traffic Signal Simulation - {self.simulator.controller.get_name()}',
            fontsize=18, color=self.colors['highlight'], fontweight='bold',
            y=0.98
        )
        
        # Add info text areas with backgrounds
        # Time and phase info (top-left)
        self.time_text = self.ax.text(
            -3.3, 3.2, '', fontsize=11, color=self.colors['text'],
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=self.colors['info_bg'], 
                     edgecolor=self.colors['highlight'], linewidth=2, alpha=0.9)
        )
        
        # Statistics (bottom-left)
        self.stats_text = self.ax.text(
            -3.3, -1.8, '', fontsize=10, color=self.colors['text'],
            verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=self.colors['info_bg'],
                     edgecolor=self.colors['highlight'], linewidth=2, alpha=0.9)
        )
        
        # Performance metrics (top-right)
        self.perf_text = self.ax.text(
            3.3, 3.2, '', fontsize=10, color=self.colors['text'],
            verticalalignment='top', horizontalalignment='right', family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=self.colors['info_bg'],
                     edgecolor=self.colors['highlight'], linewidth=2, alpha=0.9)
        )
        
        # Legend (bottom-right)
        self.legend_text = self.ax.text(
            3.3, -1.8, '', fontsize=9, color=self.colors['text'],
            verticalalignment='top', horizontalalignment='right', family='monospace',
            bbox=dict(boxstyle='round,pad=0.6', facecolor=self.colors['info_bg'],
                     edgecolor=self.colors['text'], linewidth=1, alpha=0.9)
        )
        self._setup_legend()
        
    def _setup_legend(self):
        """Setup static legend."""
        legend_info = (
            "LEGEND\n"
            "━━━━━━━━━━\n"
            "🟢 Green\n"
            "🟡 Yellow\n"
            "🔴 Red\n"
            "🚗 Vehicle\n"
        )
        self.legend_text.set_text(legend_info)
    
    def draw_intersection(self):
        """Draw the enhanced intersection layout."""
        half_size = self.intersection_size / 2
        
        # Draw roads with edge lines
        # North-South road
        ns_road = patches.Rectangle(
            (-self.road_width, -3.5), self.road_width * 2, 7,
            facecolor=self.colors['road'], edgecolor='#606060', linewidth=2
        )
        self.ax.add_patch(ns_road)
        
        # East-West road
        ew_road = patches.Rectangle(
            (-3.5, -self.road_width), 7, self.road_width * 2,
            facecolor=self.colors['road'], edgecolor='#606060', linewidth=2
        )
        self.ax.add_patch(ew_road)
        
        # Draw intersection center with gradient effect
        intersection = patches.Rectangle(
            (-half_size, -half_size), self.intersection_size, self.intersection_size,
            facecolor=self.colors['intersection'], edgecolor='#707070', linewidth=2
        )
        self.ax.add_patch(intersection)
        
        # Draw lane markings (dashed lines)
        self._draw_lane_markings()
        
        # Draw stop lines
        self._draw_stop_lines()
        
    def _draw_lane_markings(self):
        """Draw enhanced dashed lane markings."""
        dash_length = 0.15
        gap_length = 0.1
        
        # Vertical center line (North-South)
        y = -3.5
        while y < 3.5:
            if abs(y) > self.intersection_size / 2 + 0.1:
                self.ax.plot([0, 0], [y, y + dash_length], 
                           color=self.colors['lane_marking'], linewidth=2, alpha=0.7)
            y += dash_length + gap_length
        
        # Horizontal center line (East-West)
        x = -3.5
        while x < 3.5:
            if abs(x) > self.intersection_size / 2 + 0.1:
                self.ax.plot([x, x + dash_length], [0, 0],
                           color=self.colors['lane_marking'], linewidth=2, alpha=0.7)
            x += dash_length + gap_length
    
    def _draw_stop_lines(self):
        """Draw stop lines at intersection approaches."""
        stop_line_width = 3
        offset = self.intersection_size / 2 + 0.05
        
        # North approach
        self.ax.plot([-self.road_width, self.road_width], [offset, offset],
                    color=self.colors['lane_marking'], linewidth=stop_line_width, alpha=0.8)
        # South approach
        self.ax.plot([-self.road_width, self.road_width], [-offset, -offset],
                    color=self.colors['lane_marking'], linewidth=stop_line_width, alpha=0.8)
        # East approach
        self.ax.plot([offset, offset], [-self.road_width, self.road_width],
                    color=self.colors['lane_marking'], linewidth=stop_line_width, alpha=0.8)
        # West approach
        self.ax.plot([-offset, -offset], [-self.road_width, self.road_width],
                    color=self.colors['lane_marking'], linewidth=stop_line_width, alpha=0.8)
    
    def draw_traffic_signals(self, state):
        """Draw enhanced traffic signal lights with glow effect."""
        signal_positions = {
            Direction.NORTH: (0.4, 0.7),
            Direction.SOUTH: (-0.4, -0.7),
            Direction.EAST: (0.7, -0.4),
            Direction.WEST: (-0.7, 0.4)
        }
        
        # Clear previous signal patches
        for artist in self.ax.patches[:]:
            if hasattr(artist, '_signal_light'):
                artist.remove()
        
        # Determine which directions have green
        green_directions = []
        if state.signal_state == SignalState.GREEN:
            green_directions = state.get_phase_directions(state.active_phase)
        
        # Draw signal lights with glow effect
        for direction, (x, y) in signal_positions.items():
            if direction in green_directions:
                color = self.colors['green']
                glow_alpha = 0.3
            elif state.signal_state == SignalState.YELLOW and direction in state.get_phase_directions(state.active_phase):
                color = self.colors['yellow']
                glow_alpha = 0.3
            else:
                color = self.colors['red']
                glow_alpha = 0.2
            
            # Draw glow effect
            glow = patches.Circle(
                (x, y), self.signal_radius * 1.5,
                facecolor=color, edgecolor='none', alpha=glow_alpha
            )
            glow._signal_light = True
            self.ax.add_patch(glow)
            
            # Draw main signal
            circle = patches.Circle(
                (x, y), self.signal_radius, 
                facecolor=color, edgecolor='#000000', linewidth=2.5
            )
            circle._signal_light = True
            self.ax.add_patch(circle)
            
            # Add signal housing (black background)
            housing = patches.Rectangle(
                (x - self.signal_radius * 1.2, y - self.signal_radius * 1.2),
                self.signal_radius * 2.4, self.signal_radius * 2.4,
                facecolor='#1a1a1a', edgecolor='#333333', linewidth=1.5,
                zorder=-1
            )
            housing._signal_light = True
            self.ax.add_patch(housing)
    
    def draw_vehicles(self, state):
        """Draw enhanced vehicles with color coding."""
        # Clear previous vehicle patches
        for artist in self.ax.patches[:]:
            if hasattr(artist, '_vehicle'):
                artist.remove()
        
        # Vehicle positions for each direction
        vehicle_configs = {
            Direction.NORTH: {
                'start_x': -0.15,
                'start_y': 0.8,
                'dx': 0,
                'dy': 0.2,
                'width': self.vehicle_size,
                'height': self.vehicle_size * 1.5
            },
            Direction.SOUTH: {
                'start_x': 0.15,
                'start_y': -0.8,
                'dx': 0,
                'dy': -0.2,
                'width': self.vehicle_size,
                'height': self.vehicle_size * 1.5
            },
            Direction.EAST: {
                'start_x': 0.8,
                'start_y': 0.15,
                'dx': 0.2,
                'dy': 0,
                'width': self.vehicle_size * 1.5,
                'height': self.vehicle_size
            },
            Direction.WEST: {
                'start_x': -0.8,
                'start_y': -0.15,
                'dx': -0.2,
                'dy': 0,
                'width': self.vehicle_size * 1.5,
                'height': self.vehicle_size
            }
        }
        
        # Determine which directions have green
        green_directions = []
        if state.signal_state == SignalState.GREEN:
            green_directions = state.get_phase_directions(state.active_phase)
        
        # Draw vehicles for each direction
        for direction in Direction:
            queue = state.queues[direction]
            config = vehicle_configs[direction]
            
            # Draw up to max_vehicles_display (to avoid clutter)
            num_to_draw = min(len(queue), self.max_vehicles_display)
            for i in range(num_to_draw):
                x = config['start_x'] + i * config['dx']
                y = config['start_y'] + i * config['dy']
                
                # Color code: green for moving, orange for waiting
                if direction in green_directions and i < 3:
                    vehicle_color = self.colors['vehicle_moving']
                else:
                    vehicle_color = self.colors['vehicle_waiting']
                
                # Draw vehicle with rounded corners and shadow
                vehicle = patches.FancyBboxPatch(
                    (x - config['width']/2, y - config['height']/2),
                    config['width'], config['height'],
                    boxstyle="round,pad=0.01",
                    facecolor=vehicle_color,
                    edgecolor='#000000',
                    linewidth=1.5
                )
                vehicle._vehicle = True
                self.ax.add_patch(vehicle)
    
    def draw_queue_counts(self, state):
        """Draw enhanced queue count labels with color coding."""
        # Clear previous text
        for artist in self.ax.texts[:]:
            if hasattr(artist, '_queue_label'):
                artist.remove()
        
        label_positions = {
            Direction.NORTH: (-0.15, 2.8, 'N'),
            Direction.SOUTH: (0.15, -2.8, 'S'),
            Direction.EAST: (2.8, 0.15, 'E'),
            Direction.WEST: (-2.8, -0.15, 'W')
        }
        
        # Determine which directions have green
        green_directions = []
        if state.signal_state == SignalState.GREEN:
            green_directions = state.get_phase_directions(state.active_phase)
        
        for direction, (x, y, label) in label_positions.items():
            queue_len = state.get_queue_length(direction)
            
            # Color code based on signal state and queue length
            if direction in green_directions:
                bg_color = '#004400'  # Dark green
                edge_color = self.colors['green']
            elif queue_len > 8:
                bg_color = '#440000'  # Dark red for congestion
                edge_color = self.colors['red']
            elif queue_len > 4:
                bg_color = '#443300'  # Dark orange for moderate
                edge_color = self.colors['yellow']
            else:
                bg_color = '#333333'  # Default
                edge_color = '#666666'
            
            # Show overflow indicator
            display_text = f'{label}: {queue_len}'
            if queue_len > self.max_vehicles_display:
                display_text += f' (+{queue_len - self.max_vehicles_display})'
            
            text = self.ax.text(
                x, y, display_text,
                fontsize=13, color=self.colors['text'],
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.6', facecolor=bg_color, 
                         edgecolor=edge_color, linewidth=2.5, alpha=0.9),
                fontweight='bold'
            )
            text._queue_label = True
    
    def update_info_text(self):
        """Update information text displays with enhanced formatting."""
        state = self.simulator.state
        metrics = self.simulator.metrics
        
        # Time and phase info
        phase_symbol = '🟢' if state.signal_state == SignalState.GREEN else ('🟡' if state.signal_state == SignalState.YELLOW else '🔴')
        time_info = (
            f'⏱  TIME & PHASE\n'
            f'━━━━━━━━━━━━━━━\n'
            f'Time:  {self.simulator.current_time:6.1f}s\n'
            f'Phase: {state.active_phase.value} {phase_symbol}\n'
            f'State: {state.signal_state.value}\n'
            f'Timer: {state.phase_timer:6.1f}s'
        )
        self.time_text.set_text(time_info)
        
        # Statistics
        avg_wait = metrics.get_average_wait_time() if metrics.total_vehicles_departed > 0 else 0
        vehicles_waiting = metrics.total_vehicles_arrived - metrics.total_vehicles_departed
        stats_info = (
            f'📊 STATISTICS\n'
            f'━━━━━━━━━━━━━━━\n'
            f'Arrived:  {metrics.total_vehicles_arrived:4d}\n'
            f'Departed: {metrics.total_vehicles_departed:4d}\n'
            f'Waiting:  {vehicles_waiting:4d}\n'
            f'Avg Wait: {avg_wait:5.1f}s'
        )
        self.stats_text.set_text(stats_info)
        
        # Performance metrics
        total_queue = sum(state.get_queue_length(d) for d in Direction)
        max_queue = metrics.get_max_queue_length_total()
        throughput = metrics.total_vehicles_departed / self.simulator.current_time if self.simulator.current_time > 0 else 0
        perf_info = (
            f'⚡ PERFORMANCE\n'
            f'━━━━━━━━━━━━━━━\n'
            f'Total Queue: {total_queue:3d}\n'
            f'Max Queue:   {max_queue:3d}\n'
            f'Throughput:  {throughput:.2f}/s\n'
            f'Efficiency:  {self._calculate_efficiency():.1f}%'
        )
        self.perf_text.set_text(perf_info)
    
    def _calculate_efficiency(self):
        """Calculate traffic efficiency metric."""
        metrics = self.simulator.metrics
        if metrics.total_vehicles_arrived == 0:
            return 100.0
        
        # Efficiency based on throughput vs arrival rate
        departed_ratio = metrics.total_vehicles_departed / metrics.total_vehicles_arrived
        avg_wait = metrics.get_average_wait_time()
        
        # Penalize long wait times
        wait_penalty = max(0, 1 - (avg_wait / 100))  # 100s is considered very poor
        
        efficiency = departed_ratio * wait_penalty * 100
        return min(100, max(0, efficiency))
    
    def init_animation(self):
        """Initialize animation (called once)."""
        self.setup_figure()
        self.draw_intersection()
        return []
    
    def animate_frame(self, frame):
        """Update animation for each frame."""
        # Run simulation step
        self.simulator.step()
        
        # Update visualization
        state = self.simulator.state
        self.draw_traffic_signals(state)
        self.draw_vehicles(state)
        self.draw_queue_counts(state)
        self.update_info_text()
        
        return []
    
    def run(self, duration: float, save_path: str = None):
        """
        Run animated simulation.
        
        Args:
            duration: Simulation duration (seconds)
            save_path: Optional path to save animation as video/gif
        """
        self.simulator.reset()
        
        # Initialize figure first
        self.setup_figure()
        self.draw_intersection()
        
        # Calculate number of frames
        n_frames = int(duration / self.simulator.dt)
        
        # Create animation
        # Interval in milliseconds (adjusted by speed multiplier)
        interval = (self.simulator.dt * 1000) / self.speed_multiplier
        
        self.anim = animation.FuncAnimation(
            self.fig,
            self.animate_frame,
            init_func=lambda: [],
            frames=n_frames,
            interval=interval,
            blit=False,
            repeat=False
        )
        
        # Save or show
        if save_path:
            print(f"Saving animation to {save_path}...")
            if save_path.endswith('.gif'):
                self.anim.save(save_path, writer='pillow', fps=int(1000/interval))
            else:
                self.anim.save(save_path, writer='ffmpeg', fps=int(1000/interval))
            print("Animation saved!")
        else:
            plt.tight_layout()
            plt.show()
    
    def close(self):
        """Close the animation figure."""
        if self.fig:
            plt.close(self.fig)


def create_animation(simulator: TrafficSimulator, 
                     duration: float = 120.0,
                     speed_multiplier: float = 1.0,
                     save_path: str = None):
    """
    Convenience function to create and run animation.
    
    Args:
        simulator: Configured TrafficSimulator instance
        duration: Simulation duration (seconds)
        speed_multiplier: Animation speed multiplier
        save_path: Optional path to save animation
    """
    animator = TrafficAnimator(simulator, speed_multiplier)
    animator.run(duration, save_path)
    return animator
