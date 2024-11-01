from manim import *
from manimdef import DefaultManimClass
from numpy import arctan2 as atan
from numpy.linalg import norm
import numpy as np


class Intro(DefaultManimClass):
    def construct(self):
        r_true = 1.15872847301
        self.cf.scale(0.35)
        nump = NumberPlane()
        c0 = (1, 0)
        self.cf.move_to(nump.c2p(*c0))
        circle = Circle(color=YELLOW, stroke_width=1).move_to(nump.c2p(*c0))
        x0 = (0.8, 0.3)
        gline = Line(nump.c2p(0, 0), nump.c2p(*x0), stroke_width=1, color=GREY_A)
        gcircle = Circle(radius=r_true, stroke_width=1).move_to(nump.c2p(0, 0))
        garc = (
            Intersection(circle, gcircle, stroke_width=1)
            .set_color(TEAL)
            .set_fill(BLUE, opacity=0.1)
        )
        rest = Difference(circle, gcircle, stroke_width=1).set_color(YELLOW)
        goat = ImageMobject("goat.jpg").scale(0.04).move_to(nump.c2p(*x0))
        gd = Dot(color=PURPLE_C, radius=DEFAULT_DOT_RADIUS * 0.5).move_to(goat)
        getr = lambda: norm(nump.p2c(gd.get_center()))
        getxr = lambda: (getr() / 2, 0)

        def get_rbuff(g=0.08):
            v = nump.p2c(gd.get_center())[:2]
            r = np.array([-v[1], v[0], 0])

            return r / norm(r[:2]) * g

        r = (
            MathTex("r =", f"{getr():.2f}", font_size=10)
            .move_to(nump.c2p(*getxr()))
            .set_opacity(0)
        )
        r.rotate_about_origin(atan(*x0[::-1])).shift(get_rbuff())

        self.playw(FadeIn(circle))
        self.playw(FadeIn(gline, goat), r.animate.set_opacity(1))
        self.playw(FadeTransform(goat, gd))
        gline.add_updater(
            lambda x: x.become(
                Line(nump.c2p(0, 0), gd.get_center(), stroke_width=1, color=GREY_A)
            )
        )
        r.add_updater(
            lambda x: x.become(
                MathTex("r =", f"{getr():.2f}", font_size=10)
                .move_to(nump.c2p(*getxr()))
                .rotate_about_origin(atan(*nump.p2c(gd.get_center())[::-1]))
                .shift(get_rbuff())
            )
        )
        x1 = (0.5, -0.1)
        self.playw(gd.animate.move_to(nump.c2p(*x1)))
        x2 = (0.45, -0.75)
        self.playw(gd.animate.move_to(nump.c2p(*x2)))
        x3 = (1.1, 0)
        self.play(gd.animate.move_to(nump.c2p(*x3)), run_time=1.5)
        x4 = (0.7, 0.7)
        self.play(gd.animate.move_to(nump.c2p(*x4)), run_time=1.5)

        r.suspend_updating()
        gline.suspend_updating()
        cc = Dot(nump.c2p(*c0), radius=DEFAULT_DOT_RADIUS * 0.5, color=YELLOW)
        cr = DashedLine(cc.get_center(), nump.c2p(c0[0] + 1, c0[1]), stroke_width=1)
        r1 = MathTex("1", font_size=14).move_to(cr.get_center()).shift(UP * 0.08)
        self.playw(FadeOut(r, gline, gd), FadeIn(cc, cr, r1))
        gc = Dot(radius=DEFAULT_DOT_RADIUS * 0.5, color=BLUE)
        gr = DashedLine(
            gc.get_center(), nump.c2p(r_true, 0), stroke_width=1, color=TEAL
        ).rotate_about_origin(0.3)
        rr = (
            MathTex("r", font_size=14)
            .rotate_about_origin(0.3)
            .move_to(gr.get_center())
            .shift(UP * 0.05 + LEFT * 0.01)
        )

        self.playw(FadeIn(garc, gc, gr))
        self.playw(FadeIn(rr))

        garcc = garc.copy()
        garc.set_fill(BLUE, opacity=0)
        self.play(
            garcc.animate.shift(DOWN * 2.5 + LEFT * 0.7),
            rest.animate.shift(DOWN * 2.5 + RIGHT * 0.7).set_fill(YELLOW, opacity=0.1),
            self.cf.animate.scale(2.5).shift(DOWN * 2.0),
        )
        equal = Text("=", font="Consolas", font_size=36).move_to(VGroup(rest, garcc))
        self.playw(FadeIn(equal))

        self.play(
            VGroup(rr, gr).animate.rotate(-0.3).scale(2.5).next_to(equal, UP),
            VGroup(garcc, equal, rest).animate.shift(RIGHT * 4),
            run_time=1,
        )


class Isntiteasy(DefaultManimClass):
    def construct(self):
        r_true = 1.15872847301
        self.cf.scale(0.35)
        nump = NumberPlane()
        c0 = (1, 0)
        self.cf.move_to(nump.c2p(*c0))
        circle = Circle(color=YELLOW, stroke_width=1).move_to(nump.c2p(*c0))
        x0 = (0.8, 0.3)
        gline = Line(nump.c2p(0, 0), nump.c2p(*x0), stroke_width=1, color=GREY_A)
        gcircle = Circle(radius=r_true, stroke_width=1).move_to(nump.c2p(0, 0))
        garc = (
            Intersection(circle, gcircle, stroke_width=1)
            .set_color(TEAL)
            .set_fill(BLUE, opacity=0.1)
        )
        rest = Difference(circle, gcircle, stroke_width=1).set_color(YELLOW)
        goat = ImageMobject("goat.jpg").scale(0.04).move_to(nump.c2p(*x0))
        gd = Dot(color=PURPLE_C, radius=DEFAULT_DOT_RADIUS * 0.5).move_to(goat)
        getr = lambda: norm(nump.p2c(gd.get_center()))
        getxr = lambda: (getr() / 2, 0)

        circle_area = MathTex(
            "\\pi", "r", "^2", font_size=32, color=PURE_GREEN
        ).move_to(circle.get_center())
        circle_area1 = MathTex(
            "\\pi", "1", "^2", font_size=32, color=PURE_GREEN
        ).move_to(circle.get_center())

        self.playw(FadeIn(circle))
        self.playw(FadeIn(circle_area), circle.animate.set_fill(GREEN, 0.2))
        self.playw(TransformMatchingTex(circle_area, circle_area1))
        self.playw(
            circle_area1[0].animate.move_to(nump.c2p(*c0)),
            circle_area1[1:].animate.set_opacity(0),
        )
        self.play(
            FadeOut(circle_area1), circle.animate.set_fill(opacity=0), run_time=0.5
        )
        self.playw(FadeIn(garc))
        self.playw(
            self.cf.animate.move_to(garc),
            circle.animate.set_opacity(0.2).set_fill(opacity=0),
        )
        ct = np.array([0.6688411534746512, 0.94357502])
        tip_top = nump.c2p(*ct)
        tip_bot = nump.c2p(ct[0], -ct[1])
        sector1 = Union(
            Polygon(nump.c2p(0, 0), tip_top, tip_bot),
            Intersection(
                garc,
                Polygon(tip_top, tip_bot, nump.c2p(r_true, -1), nump.c2p(r_true, 1)),
            ),
            stroke_width=1,
            color=RED,
        )
        sector2 = Union(
            Polygon(nump.c2p(1, 0), tip_top, tip_bot),
            Intersection(
                garc, Polygon(tip_top, tip_bot, nump.c2p(0, -1), nump.c2p(0, 1))
            ),
            stroke_width=1,
            color=PURPLE,
        )
        quadrangle = Intersection(sector1, sector2, stroke_width=1, color=GREEN)
        self.playw(
            FadeIn(sector1, sector2, quadrangle),
            FadeOut(circle, garc),
        )
        self.playw(sector1.animate.next_to(sector2, LEFT))
        self.playw(quadrangle.animate.next_to(sector2, RIGHT))
        plus = (
            Text("+", font="Consolas", font_size=18)
            .move_to(VGroup(sector1, sector2))
            .shift(RIGHT * 0.08)
        )
        minus = Text("-", font="Consolas", font_size=18).move_to(
            VGroup(sector2, quadrangle)
        )
        self.playw(
            FadeIn(plus, scale=2),
            sector1.animate.set_fill(color=RED, opacity=0.2),
            sector2.animate.set_fill(color=PURPLE, opacity=0.2),
        )
        self.playw(
            FadeIn(minus, scale=2),
            quadrangle.animate.set_fill(color=GREEN, opacity=0.2),
        )
        equal_half = MathTex("=", r"{\pi \over 2}", font_size=36).next_to(quadrangle)
        self.playw(
            self.cf.animate.move_to(VGroup(sector1, equal_half))
            .shift(RIGHT * 0.3)
            .scale(1.4),
            FadeIn(equal_half),
        )

        r = (
            MathTex("r", font_size=24)
            .rotate(atan(*ct[::-1]), about_point=ORIGIN)
            .move_to(nump.c2p(*ct) / 2 + LEFT * 1.45 + UP * 0.15)
        )
        r1 = (
            MathTex("1", font_size=24)
            .rotate(atan(*((c0 - ct)[::-1])), about_point=ORIGIN)
            .move_to(nump.c2p(*ct) / 2 + nump.c2p(1, 0) / 2 + RIGHT * 0.13 + UP * 0.13)
        )
        self.playw(FadeIn(r, r1))


class GetAngle(DefaultManimClass):
    def construct(self):
        r_true = 1.15872847301
        self.cf.scale(0.35)
        nump = NumberPlane()
        c0 = (1, 0)
        self.cf.move_to(nump.c2p(*c0))
        circle = (
            Circle(color=YELLOW, stroke_width=1)
            .move_to(nump.c2p(*c0))
            .set_opacity(0.2)
            .set_fill(opacity=0.0)
        )
        x0 = (0.8, 0.3)
        gline = Line(nump.c2p(0, 0), nump.c2p(*x0), stroke_width=1, color=GREY_A)
        gcircle = Circle(radius=r_true, stroke_width=1).move_to(nump.c2p(0, 0))
        garc = (
            Intersection(circle, gcircle, stroke_width=1)
            .set_color(TEAL)
            .set_fill(BLUE, opacity=0.1)
        )
        rest = Difference(circle, gcircle, stroke_width=1).set_color(YELLOW)
        goat = ImageMobject("goat.jpg").scale(0.04).move_to(nump.c2p(*x0))
        gd = Dot(color=PURPLE_C, radius=DEFAULT_DOT_RADIUS * 0.5).move_to(goat)
        getr = lambda: norm(nump.p2c(gd.get_center()))
        getxr = lambda: (getr() / 2, 0)

        ct = np.array([0.6688411534746512, 0.94357502])
        tip_top = nump.c2p(*ct)
        tip_bot = nump.c2p(ct[0], -ct[1])
        sector1 = Union(
            Polygon(nump.c2p(0, 0), tip_top, tip_bot),
            Intersection(
                garc,
                Polygon(tip_top, tip_bot, nump.c2p(r_true, -1), nump.c2p(r_true, 1)),
            ),
            stroke_width=1,
            color=RED,
        )
        sector2 = Union(
            Polygon(nump.c2p(1, 0), tip_top, tip_bot),
            Intersection(
                garc, Polygon(tip_top, tip_bot, nump.c2p(0, -1), nump.c2p(0, 1))
            ),
            stroke_width=1,
            color=PURPLE,
        )
        quadrangle = Intersection(sector1, sector2, stroke_width=1, color=GREEN)

        self.playw(FadeIn(circle, sector1, sector2))
        line1u = Line(nump.c2p(0, 0), tip_top)
        line1d = Line(nump.c2p(0, 0), tip_bot)
        line2u = Line(nump.c2p(1, 0), tip_top)
        line2d = Line(nump.c2p(1, 0), tip_bot)
        angle1 = Angle(
            line1u,
            line1d,
            other_angle=True,
            radius=0.2,
            stroke_width=2.5,
            color=PURE_RED,
        )
        angle2 = Angle(line2u, line2d, radius=0.2, stroke_width=2.5, color="#FF00FF")
        r = (
            MathTex("r", font_size=24)
            .rotate(atan(*ct[::-1]), about_point=ORIGIN)
            .move_to(line1u)
            .shift(RIGHT * 0.1, DOWN * 0.1)
        )
        self.playw(FadeIn(angle1))
        self.playw(FadeIn(angle2))
        self.playw(FadeIn(r))
        theta = MathTex("\\theta", font_size=24).next_to(angle1, buff=0.05)
        self.playw(FadeIn(theta))
        self.playw(Wiggle(r, scale_value=1.6))
        circle.save_state(), sector2.save_state(), angle2.save_state(), sector1.save_state()
        sector_area = MathTex(
            r"{1 \over 2}", "r", "^2", r"\theta", font_size=24
        ).move_to(nump.c2p(tip_top[0], 0))

        self.playw(
            FadeIn(sector_area[0], sector_area[2]),
            Transform(r, sector_area[1], replace_mobject_with_target_in_scene=True),
            Transform(
                theta, sector_area[-1], replace_mobject_with_target_in_scene=True
            ),
            sector1.animate.set_fill(RED, opacity=0.2),
            VGroup(circle, sector2, angle2).animate.set_opacity(0),
        )
        self.playw(
            *[Restore(item) for item in [circle, sector2, angle2, sector1]],
            FadeOut(angle1, sector_area),
        )
        self.playw_return(
            angle2.animate.become(
                Angle(line2u, line2d, radius=0.4, stroke_width=2.5, color="#FF00FF")
            ),
            sector1.animate.set_opacity(0),
            run_time=1.5,
        )

        symline = Line(nump.c2p(-0.5, 0), nump.c2p(2.5, 0), stroke_width=1)
        hline = Line(nump.c2p(0, 0), nump.c2p(1, 0), stroke_width=1)
        self.playw(FadeIn(symline), FadeOut(angle2))
        self.playw(FadeOut(symline), FadeIn(hline))
        self.playw(FadeIn(angle1))
        angle1u = Angle(hline, line1u, radius=0.3, stroke_width=2.5, color=RED_C)
        hthetau = (
            MathTex(r"{\theta \over 2}", font_size=12, color=RED_C)
            .rotate(atan(*ct[::-1]) / 3, about_point=ORIGIN)
            .next_to(angle1u, buff=0.02)
            .shift(UP * 0.05)
        )
        angle1d = Angle(line1d, hline, radius=0.3, stroke_width=2.5, color=YELLOW)
        hthetad = (
            MathTex(r"{\theta \over 2}", font_size=12, color=YELLOW)
            .rotate(-atan(*ct[::-1]) / 3, about_point=ORIGIN)
            .next_to(angle1d, buff=0.02)
            .shift(DOWN * 0.05)
        )
        self.playw(FadeIn(angle1u, angle1d, hthetau, hthetad), FadeOut(angle1))

        triu = Polygon(
            nump.c2p(0, 0), tip_top, nump.c2p(1, 0), stroke_width=1.5, color=WHITE
        )
        sector1.save_state(), sector2.save_state(), hline.save_state(), angle1u.save_state(), angle1d.save_state(), hthetau.save_state(), hthetad.save_state()
        self.playw(
            FadeIn(triu),
            VGroup(hline, angle1d, hthetad).animate.set_opacity(0),
            sector1.animate.set_opacity(0.3).set_fill(opacity=0),
            sector2.animate.set_opacity(0.3).set_fill(opacity=0),
        )
        rm = (
            MathTex("1", font_size=18)
            .move_to(nump.c2p(r_true / 2, 0))
            .shift(DOWN * 0.085)
        )
        rh = (
            MathTex("1", font_size=18)
            .move_to(nump.c2p(ct[0] / 2 + 1 / 2, ct[1] / 2))
            .shift(RIGHT * 0.07, UP * 0.06)
        )
        self.playw(FadeIn(rm, rh))
        angleu = Angle(
            line1u, line2u, radius=0.3, stroke_width=2.5, quadrant=(-1, -1), color=RED
        )
        angled = Angle(
            line2d, line1d, radius=0.3, stroke_width=2.5, quadrant=(-1, -1), color=RED
        )
        hthetauu = MathTex(r"{\theta \over 2}", font_size=12, color=RED_C).next_to(
            angleu, DOWN, buff=0.05
        )
        hthetadd = MathTex(r"{\theta \over 2}", font_size=12, color=RED_C).next_to(
            angled, UP, buff=0.05
        )
        self.playw(FadeIn(angleu, hthetauu))
        theta.next_to(angle1, buff=0.05).set_opacity(0.3)
        angle1.set_opacity(0.3).set_fill(opacity=0)
        angled.set_opacity(0.3)
        hthetadd.set_opacity(0.3)
        self.playw(
            FadeOut(rm, rh, hthetau, triu, angle1u),
            VGroup(angleu, hthetauu).animate.set_opacity(0.3),
            *[Restore(item) for item in [sector1, sector2]],
            FadeIn(angle2, angle1, hthetadd, angled, theta),
        )
        angle2_tex = MathTex(
            "2\\pi", "-", "2\\theta", color="#FF00FF", font_size=12
        ).next_to(angle2, LEFT, buff=0.05)
        angle2_tex.save_state()
        angle2_tex.next_to(circle, DOWN, buff=0.4).scale(2)
        a360 = MathTex("360^\\circ", font_size=24).move_to(angle2_tex[0])
        self.cf.save_state()
        self.playw(
            LaggedStart(
                self.cf.animate.scale(1.4).align_to(self.cf, UP),
                FadeIn(a360),
                lag_ratio=0.3,
            )
        )
        self.playw(
            Transform(a360, angle2_tex[0], replace_mobject_with_target_in_scene=True)
        )
        self.playw(
            Transform(
                VGroup(theta, hthetauu, hthetadd, angle1, angleu, angled),
                angle2_tex[2],
                replace_mobject_with_target_in_scene=True,
            ),
            FadeIn(angle2_tex[1]),
        )
        self.playw(Restore(angle2_tex), Restore(self.cf))

        self.play(FadeOut(angle2_tex, angle2), run_time=0.5)
        self.playw_return(sector2.animate.scale(1.2).set_fill(PURPLE, opacity=0.2))
        self.playw_return(quadrangle.animate.scale(1.2).set_fill(GREEN, opacity=0.2))


class BuildEquation(DefaultManimClass):
    def construct(self):
        r_true = 1.15872847301
        self.cf.scale(0.35)
        nump = NumberPlane()
        c0 = (1, 0)
        self.cf.move_to(nump.c2p(*c0))
        circle = (
            Circle(color=YELLOW, stroke_width=1)
            .move_to(nump.c2p(*c0))
            .set_opacity(0.2)
            .set_fill(opacity=0.0)
        )
        x0 = (0.8, 0.3)
        gline = Line(nump.c2p(0, 0), nump.c2p(*x0), stroke_width=1, color=GREY_A)
        gcircle = Circle(radius=r_true, stroke_width=1).move_to(nump.c2p(0, 0))
        garc = (
            Intersection(circle, gcircle, stroke_width=1)
            .set_color(TEAL)
            .set_fill(BLUE, opacity=0.1)
        )
        rest = Difference(circle, gcircle, stroke_width=1).set_color(YELLOW)
        goat = ImageMobject("goat.jpg").scale(0.04).move_to(nump.c2p(*x0))
        gd = Dot(color=PURPLE_C, radius=DEFAULT_DOT_RADIUS * 0.5).move_to(goat)
        getr = lambda: norm(nump.p2c(gd.get_center()))
        getxr = lambda: (getr() / 2, 0)

        ct = np.array([0.6688411534746512, 0.94357502])
        tip_top = nump.c2p(*ct)
        tip_bot = nump.c2p(ct[0], -ct[1])
        sector1 = Union(
            Polygon(nump.c2p(0, 0), tip_top, tip_bot),
            Intersection(
                garc,
                Polygon(tip_top, tip_bot, nump.c2p(r_true, -1), nump.c2p(r_true, 1)),
            ),
            stroke_width=1,
            color=RED,
        )
        sector2 = Union(
            Polygon(nump.c2p(1, 0), tip_top, tip_bot),
            Intersection(
                garc, Polygon(tip_top, tip_bot, nump.c2p(0, -1), nump.c2p(0, 1))
            ),
            stroke_width=1,
            color=PURPLE,
        )
        quadrangle = Intersection(sector1, sector2, stroke_width=1, color=GREEN)

        self.add(circle, sector1, sector2)
        self.wait()
        sector2_area0 = MathTex(
            r"{1", r"\over", r"2}", "r", "^2", r"\theta", font_size=24
        ).next_to(circle, DOWN)
        sector2_area = MathTex(
            r"{1",
            r"\over",
            r"2}",
            "1",
            "^2",
            r"(2\pi - 2\theta)",
            font_size=24,
            color=PURPLE,
        ).next_to(circle, DOWN)
        sector2_area1 = MathTex(r"\pi - \theta", font_size=24, color=PURPLE).next_to(
            circle, DOWN
        )
        self.playw(
            LaggedStart(
                self.cf.animate.scale(1.4).align_to(self.cf, UP),
                AnimationGroup(
                    FadeIn(sector2_area0),
                    sector2.animate.set_fill(PURPLE, opacity=0.2),
                    sector1.animate.set_opacity(0.2).set_fill(opacity=0),
                ),
                lag_ratio=0.3,
            )
        )
        self.playw(
            TransformMatchingTex(
                sector2_area0,
                sector2_area,
                key_map={"r": "1", r"\theta": r"(2\pi - 2\theta)"},
            )
        )
        self.play(sector2_area[3:5].animate.set_opacity(0), run_time=0.5)
        self.play(
            VGroup(
                sector2_area[2], sector2_area[5][1], sector2_area[5][4]
            ).animate.set_color(PURE_RED)
        )
        self.playw(Transform(sector2_area, sector2_area1))
        self.playw(
            VGroup(sector2, sector2_area)
            .animate.arrange(DOWN)
            .next_to(circle, LEFT, buff=0.5)
            .align_to(circle, UP),
            FadeIn(quadrangle),
        )
        hline = Line(nump.c2p(0, 0), nump.c2p(1, 0), stroke_width=1)
        r1u = (
            MathTex("1", font_size=24)
            .rotate(atan(*((c0 - ct)[::-1])), about_point=ORIGIN)
            .move_to(nump.c2p(*ct) / 2 + nump.c2p(1, 0) / 2 + RIGHT * 0.13 + UP * 0.13)
        )
        r1d = MathTex("1", font_size=24).next_to(hline, DOWN, buff=0.05)
        line2u = Line(nump.c2p(1, 0), tip_top)
        angle2h = Angle(
            line2u,
            hline,
            radius=0.2,
            stroke_width=2.5,
            quadrant=(1, -1),
            color="#FF55FF",
        )
        hthetah = (
            MathTex("\\pi", "-", "\\theta", font_size=16)
            .next_to(angle2h, LEFT, buff=0.05)
            .shift(UP * 0.05)
        )
        self.playw(FadeIn(hline, r1u, r1d, angle2h, hthetah))
        triu = Polygon(
            nump.c2p(0, 0), tip_top, nump.c2p(1, 0), stroke_width=1.5, color=WHITE
        ).set_fill(opacity=0.2)
        tri_area0 = MathTex(
            r"{1",
            r"\over",
            r"2}",
            "a",
            "b",
            r"\operatorname{sin}",
            "\\theta",
            font_size=24,
        ).next_to(circle, DOWN)
        tri_area = MathTex(
            r"{1",
            r"\over",
            r"2}",
            "a",
            "b",
            r"\operatorname{sin}",
            r"(\pi-\theta)",
            font_size=24,
        ).next_to(circle, DOWN)
        tri_area[-1].align_to(tri_area0[-1], LEFT)
        self.playw(FadeIn(tri_area0, triu))

        self.play(
            tri_area0[3:5].animate.set_opacity(0),
            r1u.animate.rotate(-atan(*((c0 - ct)[::-1]))).move_to(tri_area0[4]),
            r1d.animate.move_to(tri_area0[3]).align_to(tri_area0[-2], DOWN),
            Transform(
                tri_area0[-1], tri_area[-1], replace_mobject_with_target_in_scene=True
            ),
        )
        self.playw(FadeOut(r1u, r1d))
        double = MathTex("2", " \\times ", font_size=24, color=GREEN).next_to(
            tri_area0, LEFT
        )
        self.playw(
            quadrangle.animate.set_fill(color=GREEN, opacity=0.2),
            FadeOut(hline, triu, angle2h, hthetah),
            FadeIn(double),
            tri_area[-1].animate.set_color(GREEN),
            tri_area0.animate.set_color(GREEN),
        )
        tri_areaf = MathTex(
            r"\operatorname{sin}", r"(\pi-\theta)", font_size=24, color=GREEN
        ).next_to(circle, DOWN)
        sintheta = MathTex(
            r"\operatorname{sin}", r"\theta", font_size=24, color=GREEN
        ).next_to(circle, DOWN)
        self.playw(FadeTransform(VGroup(double, tri_area0, tri_area[-1]), tri_areaf))
        self.playw(
            TransformMatchingTex(
                tri_areaf, sintheta, key_map={r"(\pi-\theta)": r"\theta"}
            )
        )
        self.playw(
            VGroup(quadrangle, sintheta)
            .animate.arrange(DOWN)
            .next_to(circle)
            .align_to(circle, UP)
        )
        s1_area = MathTex(
            r"{1 \over 2}", "r^2", r"\theta", font_size=24, color=RED
        ).next_to(sector1, DOWN)
        self.play(
            sector1.animate.set_opacity(1).set_fill(RED, opacity=0.2), FadeIn(s1_area)
        )
        self.playw(
            FadeOut(circle),
            sector1.animate.move_to(circle),
            s1_area.animate.next_to(circle, DOWN, buff=0.1),
        )
        plus = (
            Text("+", font="Consolas", font_size=18)
            .move_to(VGroup(sector1, sector2))
            .shift(RIGHT * 0.08)
        )
        minus = Text("-", font="Consolas", font_size=18).move_to(
            VGroup(sector1, quadrangle)
        )
        self.play(FadeIn(plus), run_time=0.5)
        self.playw_return(sector2.animate.scale(1.2))
        self.play(FadeIn(minus), run_time=0.5)
        self.playw_return(quadrangle.animate.scale(1.2))
        self.playw(
            sector2_area.animate.move_to(sector2),
            s1_area.animate.move_to(sector1),
            sintheta.animate.move_to(quadrangle),
            VGroup(sector1, sector2, quadrangle).animate.set_opacity(0),
        )
        self.play(
            VGroup(sector2_area, plus, s1_area, minus, sintheta).animate.arrange(RIGHT),
            self.cf.animate.move_to(ORIGIN),
        )
        equalh = MathTex("=", r"{1 \over 2}", r"\pi", font_size=24).next_to(sintheta)
        self.playw(FadeIn(equalh))


class ThetaByR(DefaultManimClass):
    def construct(self):
        s1_area = MathTex(r"{1 \over 2}", "r^2", r"\theta", font_size=24, color=RED)
        plus = Text("+", font="Consolas", font_size=18)
        s2_area = MathTex(
            r"\pi",
            "-",
            r"\theta",
            font_size=24,
            color=PURPLE,
        )
        minus = Text("-", font="Consolas", font_size=18)
        sintheta = MathTex(r"\operatorname{sin}", r"\theta", font_size=24, color=GREEN)
        VGroup(s2_area, plus, s1_area, minus, sintheta).arrange(RIGHT)
        equalh = MathTex("=", r"{1 \over 2}", r"\pi", font_size=24).next_to(sintheta)
        self.cf.scale(0.35 * 1.4)
        self.add(VGroup(s2_area, plus, s1_area, minus, sintheta, equalh))
        self.wait()
        self.playw_return(
            *[
                item.animate.scale(1.5)
                for item in [s1_area[-1], s2_area[-1], sintheta[-1]]
            ],
            *[
                item.animate.set_opacity(0.3)
                for item in [
                    s1_area[:-1],
                    s2_area[:-1],
                    sintheta[:-1],
                    plus,
                    minus,
                    equalh,
                ]
            ],
            run_time=2,
        )

        r_true = 1.15872847301
        nump = NumberPlane()
        c0 = (1, 0)
        circle = (
            Circle(color=YELLOW, stroke_width=1)
            .move_to(nump.c2p(*c0))
            .set_opacity(0.2)
            .set_fill(opacity=0.0)
        )
        x0 = (0.8, 0.3)
        gline = Line(nump.c2p(0, 0), nump.c2p(*x0), stroke_width=1, color=GREY_A)
        gcircle = Circle(radius=r_true, stroke_width=1).move_to(nump.c2p(0, 0))
        garc = (
            Intersection(circle, gcircle, stroke_width=1)
            .set_color(TEAL)
            .set_fill(BLUE, opacity=0.1)
        )
        rest = Difference(circle, gcircle, stroke_width=1).set_color(YELLOW)
        goat = ImageMobject("goat.jpg").scale(0.04).move_to(nump.c2p(*x0))
        gd = Dot(color=PURPLE_C, radius=DEFAULT_DOT_RADIUS * 0.5).move_to(goat)
        getr = lambda: norm(nump.p2c(gd.get_center()))
        getxr = lambda: (getr() / 2, 0)

        ct = np.array([0.6688411534746512, 0.94357502])
        tip_top = nump.c2p(*ct)
        tip_bot = nump.c2p(ct[0], -ct[1])
        sector1 = Union(
            Polygon(nump.c2p(0, 0), tip_top, tip_bot),
            Intersection(
                garc,
                Polygon(tip_top, tip_bot, nump.c2p(r_true, -1), nump.c2p(r_true, 1)),
            ),
            stroke_width=1,
            color=RED,
        )
        sector2 = Union(
            Polygon(nump.c2p(1, 0), tip_top, tip_bot),
            Intersection(
                garc, Polygon(tip_top, tip_bot, nump.c2p(0, -1), nump.c2p(0, 1))
            ),
            stroke_width=1,
            color=PURPLE,
        )
        quadrangle = Intersection(sector1, sector2, stroke_width=1, color=GREEN)
        hline = Line(nump.c2p(0, 0), nump.c2p(1, 0), stroke_width=1)
        self.playw(Wiggle(sintheta, scale_value=1.5))
        self.play(
            FadeOut(s2_area, plus, s1_area, minus, sintheta, equalh),
        )
        self.cf.move_to(nump.c2p(*c0)).scale(0.8)
        self.playw(FadeIn(circle, quadrangle, hline, sector1, sector2))
        r1u = (
            MathTex("1", font_size=18)
            .rotate(atan(*((c0 - ct)[::-1])), about_point=ORIGIN)
            .move_to(nump.c2p(*ct) / 2 + nump.c2p(1, 0) / 2 + RIGHT * 0.08 + UP * 0.08)
        )
        r1d = MathTex("1", font_size=18).next_to(hline, DOWN, buff=0.05)
        self.playw(FadeIn(r1u, r1d))

        aoverb = ct[0] / ct[1]
        bovera = ct[1] / ct[0]
        fx = -aoverb / (-aoverb - bovera)
        fy = -aoverb * (fx - 1)
        fop = nump.c2p(fx, fy)
        fop_line = Line(fop, nump.c2p(1, 0), stroke_width=1)
        self.playw(Create(fop_line), self.cf.animate.move_to(fop_line).scale(0.7))
        line1u = Line(nump.c2p(0, 0), tip_top, stroke_width=1)
        rangle = RightAngle(
            line1u, fop_line, quadrant=(-1, 1), length=0.1, stroke_width=1
        )
        angle1u = Angle(hline, line1u, radius=0.2, stroke_width=1.5, color=RED_C)
        hthetau = (
            MathTex(r"{\theta \over 2}", font_size=10, color=RED_C)
            .rotate(atan(*ct[::-1]) / 3, about_point=ORIGIN)
            .next_to(angle1u, buff=0.01)
            .shift(UP * 0.04)
        )
        self.playw(FadeIn(rangle, angle1u, hthetau))
        self.playw(Wiggle(r1d, scale_value=1.6))
        sinhalf0 = MathTex(
            r"\operatorname{sin}",
            r"{\theta \over 2}",
            "=",
            r"{",
            r"\sqrt{1- {r^2 \over 4} }",
            r"\over",
            r"1}",
            font_size=12,
        ).next_to(circle, LEFT)
        sinhalf = MathTex(
            r"\operatorname{sin}",
            r"{\theta \over 2}",
            "=",
            r"\sqrt{ 1- {r^2 \over 4}}",
            font_size=12,
        ).next_to(circle, LEFT)
        coshalf = (
            MathTex(
                r"\operatorname{cos}",
                r"{\theta \over 2}",
                "=",
                r"{r \over 2}",
                font_size=12,
            )
            .next_to(circle, LEFT)
            .shift(UP * 0.5)
            .align_to(sinhalf0, LEFT)
        )
        coshalf0 = (
            MathTex(
                r"\operatorname{cos}",
                r"{\theta \over 2}",
                "=",
                r"{",
                r"{r \over 2}",
                r"\over",
                r"1}",
                font_size=12,
            )
            .next_to(circle, LEFT)
            .shift(UP * 0.5)
            .align_to(sinhalf0, LEFT)
        )
        self.playw(FadeIn(coshalf0[:3]))
        line1uh = Line(nump.c2p(0, 0), fop, stroke_width=1, color=RED)
        rhalf = (
            MathTex(r"{r", r"\over", "2}", font_size=14, color=RED)
            .move_to(line1uh)
            .shift(LEFT * 0.1 + UP * 0.1)
            .set_opacity(0)
        )
        self.playw_return(
            line1uh.animate.shift(LEFT * 0.5 + UP * 0.7),
            rhalf.animate.shift(LEFT * 0.5 + UP * 0.7).set_opacity(1),
            run_time=1.5,
        )
        self.playw(FadeIn(coshalf0[3:]))
        self.playw(
            Transform(
                coshalf0[:3], coshalf[:3], replace_mobject_with_target_in_scene=True
            ),
            FadeTransform(coshalf0[4], coshalf[3]),
            FadeOut(coshalf0[3], coshalf0[5:]),
        )
        self.playw(FadeIn(sinhalf0))
        self.playw(
            Transform(
                sinhalf0[:3], sinhalf[:3], replace_mobject_with_target_in_scene=True
            ),
            FadeTransform(sinhalf0[4], sinhalf[3]),
            FadeOut(sinhalf0[3], sinhalf0[3:]),
        )

        eq1 = MathTex(
            r"\operatorname{sin}",
            r" 2\theta ",
            "=",
            "2",
            r"\operatorname{sin}",
            r"\theta",
            r"\operatorname{cos}",
            r"\theta ",
            font_size=12,
        ).next_to(coshalf, buff=0.75)
        eq2 = MathTex(
            r"\operatorname{sin}",
            r" \theta ",
            "=",
            "2",
            r"\operatorname{sin}",
            r"{\theta \over 2}",
            r"\operatorname{cos}",
            r"{\theta \over 2} ",
            font_size=12,
        ).next_to(eq1, DOWN)
        eq1.move_to(eq2)
        self.playw(
            FadeOut(
                circle,
                sector1,
                sector2,
                r1u,
                r1d,
                fop_line,
                angle1u,
                hthetau,
                hline,
                rangle,
                quadrangle,
                line1uh,
            ),
            FadeIn(eq1),
            self.cf.animate.move_to(eq2),
        )
        self.playw(
            *[
                Transform(eq1[i], eq2[i], replace_mobject_with_target_in_scene=True)
                for i in range(len(eq1))
            ]
        )
        cosh = coshalf[-1].copy()
        sinh = sinhalf[-1].copy()
        cosh.generate_target().move_to(eq2[4])
        sinh.generate_target().move_to(eq2[-2]).align_to(eq2[-2], LEFT)
        self.playw(
            eq2[-4:].animate.set_opacity(0), MoveToTarget(cosh), MoveToTarget(sinh)
        )

        sinthetaf = (
            MathTex("{r", r"\sqrt{4-r^2}", r"\over", r"2", font_size=14, color=YELLOW)
            .move_to(eq2[3:])
            .align_to(eq2[3:], LEFT)
        )
        self.playw(FadeTransform(VGroup(eq2[3:], cosh, sinh), sinthetaf))


class PureThetaByR(DefaultManimClass):
    def construct(self):
        s1_area = MathTex(
            r"{1", r"\over", r"2}", "r^2", r"\theta", font_size=24, color=RED
        )
        plus = Text("+", font="Consolas", font_size=18)
        s2_area = MathTex(
            r"\pi",
            "-",
            r"\theta",
            font_size=24,
            color=PURPLE,
        )
        minus = Text("-", font="Consolas", font_size=18)
        sintheta = MathTex(r"\operatorname{sin}", r"\theta", font_size=24, color=GREEN)
        VGroup(s2_area, plus, s1_area, minus, sintheta).arrange(RIGHT)
        equalh = MathTex("=", r"{1 \over 2}", r"\pi", font_size=24).next_to(sintheta)
        self.cf.scale(0.35 * 1.4)
        self.add(VGroup(s2_area, plus, s1_area, minus, sintheta, equalh))
        self.wait()
        sinthetaf = MathTex(
            "{r", r"\sqrt{4-r^2}", r"\over", r"2", font_size=18, color=GREEN
        ).move_to(sintheta)
        self.playw(
            Transform(sintheta, sinthetaf, replace_mobject_with_target_in_scene=True)
        )

        self.playw_return(
            s1_area[-1].animate.scale(1.5),
            s2_area[-1].animate.scale(1.5),
            s1_area[:-1].animate.set_opacity(0.2),
            s2_area.animate.set_opacity(0.2),
            VGroup(plus, minus, equalh).animate.set_opacity(0.2),
        )
        arccosblahblah = MathTex(
            r"\theta = ", r"\operatorname{cos}^{-1}", "f(r)", font_size=24
        ).shift(UP)
        self.playw(
            FadeIn(arccosblahblah, shift=UP * 0.5),
            VGroup(
                s2_area, plus, s1_area, minus, sinthetaf, equalh
            ).animate.set_opacity(0.3),
        )
        self.playw(
            VGroup(
                s2_area, plus, s1_area, minus, sinthetaf, equalh
            ).animate.set_opacity(1),
            FadeOut(arccosblahblah),
        )

        s1_area_ = MathTex("r^2", r"{\theta", r"\over", r"2}", font_size=24, color=RED)
        self.playw(
            TransformMatchingTex(s1_area, s1_area_, key_map={r"\theta": r"{\theta"})
        )
        s1_area_arc = MathTex(
            "r^2",
            r"\operatorname{cos}^{-1}",
            r"{r",
            r"\over",
            r"2",
            r"}",
            font_size=24,
            color=RED,
        )
        self.playw(
            TransformMatchingTex(s1_area_, s1_area_arc),
            VGroup(s2_area, plus).animate.shift(LEFT * 0.2),
            VGroup(minus, sinthetaf, equalh).animate.shift(RIGHT*0.1)
        )
        s2_area_ = MathTex(
            r"\pi",
            "-",
            r"2\operatorname{cos}^{-1}",
            r"{r",
            r"\over",
            r"2",
            r"}",
            font_size=24,
            color=PURPLE,
        ).move_to(s2_area).align_to(s2_area, RIGHT)
        self.playw(TransformMatchingTex(s2_area, s2_area_))