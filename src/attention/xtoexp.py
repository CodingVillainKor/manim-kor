from manim import *
from math import e



class SceneInner(MovingCameraScene):
    def construct(self):
        self.sceneA()
        self.clear()

    def sceneA(self):
        axes = Axes(
            y_range = [-5, 15, 2],
            x_range = [-3, 3, 1]
        )
        self.playw(Write(axes))

        yxgraph = axes.plot(lambda x: x,
                            color = WHITE,)
        yexgraph = axes.plot(lambda x: e**x,
                            color = GOLD,)
        self.playw(Write(yxgraph))
        self.playw(Transform(yxgraph, yexgraph))

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])