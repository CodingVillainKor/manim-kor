from manim import *
from manimdef import DefaultManimClass
import numpy as np


class WhatisVectorField(DefaultManimClass):
    def construct(self):
        def vf_fn(pos):
            x, y, _ = pos
            return np.sin(y / 2) * RIGHT + np.cos(x / 2) * UP

        x_range = [-7, 7, 1]
        y_range = [-4, 4, 1]
        avf = (
            ArrowVectorField(
                vf_fn, x_range=x_range, y_range=y_range, length_func=lambda x: x / 2
            )
            .set_opacity(0.7)
            .scale(0.7)
        )

        nump = NumberPlane().scale(0.7)
        dots = VGroup()
        for i in range(y_range[0], y_range[1], y_range[2]):
            dot_row = VGroup()
            for j in range(x_range[0], x_range[1], x_range[2]):
                dot_row.add(
                    Dot(nump.c2p(j, i), radius=DEFAULT_SMALL_DOT_RADIUS, color=BLUE)
                )
            dots.add(dot_row)
        self.playw(FadeIn(dots))
        self.playw(LaggedStart(*[FadeIn(avf[i]) for i in range(len(avf))]))


class VectorFieldPhysics(DefaultManimClass):
    def construct(self):
        def vf_fn(pos):
            x, y, _ = pos
            if x**2 + y**2 <= 4:
                return [0, 0, 0]
            center_x, center_y = 0, 0
            direction = np.array([center_x - x, center_y - y])
            return direction / np.linalg.norm(direction) / (x**2 + y**2) ** 0.15

        x_range = [-7, 7, 1]
        y_range = [-4, 4, 1]
        avf = (
            ArrowVectorField(
                vf_fn,
                x_range=x_range,
                y_range=y_range,
                length_func=lambda x: x / 2,
                vector_config={"stroke_width": 1},
            )
            .set_opacity(0.5)
            .scale(0.7)
        )

        nump = NumberPlane().scale(0.7)
        c = Circle(radius=1.5, color=GREEN, stroke_width=1).scale(0.7)
        self.cf.scale(0.7)
        self.cf.save_state()
        self.cf.move_to(nump.c2p(3, 2)).scale(0.15)
        me = Dot(nump.c2p(3, 2), color=BLUE)
        self.playw(FadeIn(me))
        self.playw(FadeIn(avf, c))
        self.playw(me.animate.move_to(nump.c2p(3, 2) / 1.05))
        self.playw(Restore(self.cf))

        self.wait(2)

        self.playw_return(*[item.animate.scale(1.5) for item in avf])
        eq = MathTex(
            r"\mathbf{E}(",
            "x",  # 1
            ", ",
            "y",  # 3
            ") = k {(-",
            "x",  # 5
            ", -",
            "y",  # 7
            r")",  # 8
            r"\over "  # 9
            r"\sqrt{",  # 10
            "x",  # 11
            "^2",  # 12
            "+",  # 13
            "y",  # 14
            "^2",  # 15
            r"}",  # 16
            r"}",  # 17
            font_size=24,
        )  # x: 1, 5, 11 / y: 3, 7, 13
        VGroup(eq[1], eq[5], eq[11]).set_color(YELLOW)
        VGroup(eq[3], eq[7], eq[14]).set_color(TEAL)
        self.playw(FadeOut(c), FadeIn(eq))

        x_range = [-7, 8, 1]
        y_range = [-4, 5, 1]
        coords = VGroup()
        for y in range(*y_range):
            for x in range(*x_range):
                if x**2 + y**2 > 4:
                    coords.add(
                        MathTex(f"[{x}, {y}]", font_size=16, color=GREEN).move_to(
                            nump.c2p(x, y)
                        )
                    )

        self.playw(FadeOut(avf, me), FadeIn(coords))
        self.play(*[item.animate.move_to(ORIGIN).set_opacity(0.0) for item in coords])
        avf.save_state()
        [item.move_to(ORIGIN).set_opacity(0) for item in avf]
        self.playw(Restore(avf))

        self.playw_return(*[item.animate.scale(1.5) for item in avf])