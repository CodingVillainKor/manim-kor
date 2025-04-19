from manim import *
from math import log2

class Plotting(MovingCameraScene):
    def construct(self):
        axes = Axes(
            y_range = [0, 50, 10],
            x_range = [0, 50, 10],
            x_length = 10,
            y_length = 5
        )
        axes.add_coordinates()
        x_label = axes.get_x_axis_label("x").shift(DOWN*0.7)
        y_label = axes.get_y_axis_label("y")
        self.play(self.camera.frame.animate.move_to(axes).set(width=axes.width*2))
        self.play(LaggedStart(Write(axes), Write(x_label), Write(y_label), lag_ratio=0.5, run_time=2))
        self.wait()


        graph_logn = axes.plot(lambda x: log2(x),
                               color = GREEN,
                               x_range = [1, 50]
                               )
        log_text = Tex("$log_2(x)$", color=GREEN).move_to(axes.coords_to_point(52, log2(50)+2))
        graph_halfn = axes.plot(lambda x: (x+1)/2,
                               color = BLUE,
                               x_range = [1, 50]
                               )
        half_text = Tex("$(x+1)\\over{2}$", color=BLUE).move_to(axes.coords_to_point(52, 26))
        self.play(LaggedStart(Write(graph_logn), Write(log_text), lag_ratio=0.5, run_time=1.7))
        self.wait()
        self.play(LaggedStart(Write(graph_halfn), Write(half_text), lag_ratio=0.5, run_time=1.7))
        self.wait()