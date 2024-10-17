from manim import *
from manimdef import DefaultManimClass


class WhatIsEquation(DefaultManimClass):
    def construct(self):
        eq = MathTex("f(x)", "=", "0").set_color_by_gradient(BLUE, TEAL)
        self.playw(FadeIn(eq))
        double_x = MathTex("2x", "=", "0").set_color_by_gradient(BLUE, TEAL)
        self.playw(TransformMatchingTex(eq, double_x))
        plus_five = MathTex("x", "+ 5", "=", "0").set_color_by_gradient(BLUE, TEAL)
        self.playw(TransformMatchingTex(double_x, plus_five))
        self.wait(3)
        self.playw_return(plus_five[0][0].animate.shift(LEFT * 0.3).scale(2))
        self.playw(
            TransformMatchingTex(
                plus_five, double_x, replace_mobject_with_target_in_scene=True
            )
        )
        self.playw(double_x[0][0].animate.set_opacity(0))
        self.playw(
            TransformMatchingTex(
                double_x, plus_five, replace_mobject_with_target_in_scene=True
            )
        )

        eq_sol_xplusfive = MathTex("x", "=", "-5").set_color_by_gradient(BLUE, TEAL)
        self.playw(
            TransformMatchingTex(plus_five, eq_sol_xplusfive, key_map={"0": "-5"})
        )
        self.playw_return(eq_sol_xplusfive[0].animate.scale(2))


class WhatIsDE(DefaultManimClass):
    def construct(self):
        eq = MathTex("g(", "f'(x)", ")|", "=", "0")
        eq[2][1].set_color(BLACK)
        self.playw(Write(eq), run_time=1)
        unknown = (
            Text("Unknown", font="Noto Sans KR", font_size=36)
            .set_color_by_gradient(RED_E, PURE_RED)
            .next_to(eq[1], UP)
        )
        self.playw(
            FadeIn(unknown, shift=UP * 0.5),
            eq[1].animate.set_color_by_gradient(RED_E, PURE_RED),
        )
        self.wait(2)

        self.camera.frame.save_state()
        fx = MathTex("f(x)")
        fpx = MathTex("f'(x)")
        VGroup(fx, fpx).arrange(
            RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 4
        ).shift(DOWN * 2)
        self.playw(
            self.camera.frame.animate.shift(DOWN * 2),
            VGroup(eq, unknown).animate.set_opacity(0.3),
            FadeIn(fx),
        )
        self.playw(FadeIn(fpx))

        self.playw(FadeOut(fx, fpx), Restore(self.camera.frame))

        self.playw(eq.animate.set_opacity(1), unknown.animate.set_opacity(0))
        self.playw_return(
            eq[:3].animate.scale(1.5).shift(LEFT * 0.3),
            eq[-1].animate.scale(1.5).shift(RIGHT * 0.1),
            run_time=1.8,
        )

        VGroup(fx, fpx).next_to(eq, UP, buff=1)
        self.playw(FadeIn(fx))
        self.playw(FadeIn(fpx))
        eq_5 = MathTex("|", "f'(x)", "+5", "=", "0")
        eq_5[0].set_opacity(0)
        self.playw(TransformMatchingTex(eq, eq_5, key_map={")-": "+5", "g(": "|"}))


class SolvingDE(DefaultManimClass):
    def construct(self):
        eq5 = MathTex("f'(x)", "+5", "=", "0")
        self.playw(FadeIn(eq5))
        int_eq5 = MathTex(
            r"\int", "(", "f'(x)", "+5", ")", "dx", "=", r"\int", "0", "dx"
        )
        self.playw(TransformMatchingTex(eq5, int_eq5))
        after_int = MathTex("f(x)", "+", "5x", "+", "A", "=", "B")
        self.playw(TransformMatchingTex(int_eq5, after_int))
        self.playw(
            LaggedStart(
                after_int[4].animate.set_color(TEAL),
                after_int[6].animate.set_color(TEAL),
                lag_ratio=0.6,
            )
        )
        self.wait(3)
        final_sol = MathTex("f(x)", "=", "-", "5x", "+", "C").set_color_by_gradient(
            BLUE, TEAL
        )
        
        self.playw(TransformMatchingTex(after_int, final_sol))
        eq5.next_to(final_sol, UP, DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5)
        after_int.move_to(eq5)
        self.wait()
        self.playw(FadeIn(eq5, shift=DOWN * 0.5))
        self.playw(TransformMatchingTex(eq5, after_int))
        self.playw(TransformMatchingTex(after_int, eq5))

        self.playw(final_sol.animate.set_color_by_gradient(RED_E, PURE_RED))
        self.playw_return(final_sol[0].animate.scale(1.5))
        self.playw_return(final_sol[3].animate.scale(1.5))
        self.playw_return(final_sol[5].animate.scale(1.5))
        self.wait(2)
        self.playw(final_sol.animate.set_color_by_gradient(BLUE, TEAL))
