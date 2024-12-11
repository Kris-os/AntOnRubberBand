from dataclasses import dataclass
from typing import Any, Tuple
from manim import *
import numpy as np

from simulations.simulation_parameters import Simulation, SimulationParameters

params = SimulationParameters(
    ant_starting_position=0.0,
    rubber_band_starting_length=10.0,
    ant_walking_speed=1.0,
    rubber_band_stretch_rate=0.1
)
simulation_engine = Simulation(params)
simulation_engine2 = Simulation(params)

results: list[Tuple[float, float, float, float]] = []
results.append((params.ant_starting_position, params.rubber_band_starting_length, params.ant_starting_position, params.ant_starting_position))

def leos_solution(t: float):
    #c = (x0 + v / r )
    # return c e ^ (rt)  - v / r
    c = params.ant_starting_position + params.ant_walking_speed / params.rubber_band_stretch_rate
    
    return c * np.exp(params.rubber_band_stretch_rate * t) - params.ant_walking_speed / params.rubber_band_stretch_rate

for i in range(1, 10):
    simulation_engine.simulate_time_step_ant_then_stretch()
    simulation_engine2.simulate_time_step_stretch_then_ant()
    ant_position_result = simulation_engine.running_ant_position
    end_of_band_result = simulation_engine.running_rubber_band_length
    
    leos_result = leos_solution(i)
    
    results.append((ant_position_result, end_of_band_result, simulation_engine2.running_ant_position, leos_result)) 
    
max_y = max(max(t) for t in results) * 1.1

class AnimateAnt(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, len(results)-1, 10],
            y_range=[0, max_y, 10],
            axis_config={"color": BLUE},
        )
        
        self.play(Create(axes))
        time_label = axes.get_x_axis_label("Time").scale(0.6).next_to(axes.x_axis, DOWN)
        distance_label = axes.get_y_axis_label("Distance").scale(0.6).next_to(axes.y_axis, LEFT, buff = -0.3).rotate(PI / 2)
        self.play(FadeIn(time_label), FadeIn(distance_label))

        # Create the two line graphs (series)
        line1 = axes.plot_line_graph(
            x_values=np.arange(len(results)),
            y_values=[i[0] for i in results],
            line_color=RED,
            add_vertex_dots=False
        )

        line2 = axes.plot_line_graph(
            x_values=np.arange(len(results)),
            y_values=[i[1] for i in results],
            line_color=BLUE,
            add_vertex_dots=False
        )    
        
        line3 = axes.plot_line_graph(
            x_values=np.arange(len(results)),
            y_values=[i[2] for i in results],
            line_color=GREEN,
            add_vertex_dots=False
        )    
        
        line4 = axes.plot_line_graph(
            x_values=np.arange(len(results)),
            y_values=[i[3] for i in results],
            line_color=PURPLE,
            add_vertex_dots=False
        )    
        
        ant_label = Text("Ant (ant then stretch)", color=RED).scale(0.6).next_to(line1, UP, buff = -1)
        ant2_label = Text("Ant (stretch then ant)", color=GREEN).scale(0.6).next_to(line1, DOWN, buff = -0.5)
        rubber_band_label = Text("End of Rubber Band", color=BLUE).scale(0.6).next_to(line2, UP, buff = -1)
        leos_label = Text("LEO", color=PURPLE).scale(0.6).next_to(line3, UP, buff = -1)
        
        
        self.play(Create(line1, run_time = 2), Create(line2, run_time = 2), Create(line3, run_time = 2), Create(line4, run_time = 2))
        self.play(FadeIn(ant_label), FadeIn(rubber_band_label), FadeIn(ant2_label), FadeIn(leos_label))

        self.wait(2)
