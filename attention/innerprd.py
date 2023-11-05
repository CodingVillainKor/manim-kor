from manim import *
from math import e


def rect(height=0.3, width=1.0, opacity=0.8, 
         stroke_width=DEFAULT_STROKE_WIDTH/2,
         color=[BLUE, YELLOW], stroke_color=WHITE,
         **kwargs):
    return Rectangle(
        height=height,
        width=width,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        **kwargs)

def texbox(*msg, tex_config=dict(), box_config=dict()):
    tex = Tex(*msg, **tex_config)
    box = rect(height=tex.height, width=tex.width, 
               stroke_color=GOLD, **box_config).surround(tex)
    return VGroup(box, tex)


class SceneInner(MovingCameraScene):
    def construct(self):
        self.sceneA()
        self.clear()
        self.sceneB()
        self.clear()

    def sceneA(self):
        r1 = rect(0.5, 0.5, color="#FF0000", stroke_color=WHITE)
        r2 = rect(0.5, 0.5, color="#00FF00", stroke_color=WHITE)
        vg1 = VGroup(r1, r2).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10).move_to(ORIGIN)
        self.playw(Write(vg1))
        

        r1.generate_target()
        r2.generate_target()
        r1.target.move_to(ORIGIN)
        r2.target.move_to(ORIGIN)

        self.play(MoveToTarget(r1), MoveToTarget(r2))
        self.playw(Transform(vg1, Text("-4.1")))

    def sceneB(self):
        r1 = rect(0.5, 0.5, color="#00FF55", stroke_color=WHITE)
        r2 = rect(0.5, 0.5, color="#00EE00", stroke_color=WHITE)
        vg1 = VGroup(r1, r2).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10).move_to(ORIGIN)
        self.playw(Write(vg1))
        

        r1.generate_target()
        r2.generate_target()
        r1.target.move_to(ORIGIN)
        r2.target.move_to(ORIGIN)

        self.play(MoveToTarget(r1), MoveToTarget(r2))
        self.playw(Transform(vg1, Text("9.7")))

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])