from cmath import exp
from functools import partial
from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)

# for Thumbnail
# config.background_color = WHITE
# / for Thumbnail
class intro(Scene2D):
    def construct(self):
        start = MathTex(
            "(",
            "e",
            "^",
            "{",
            "1",
            "+",
            "2\\pi i",
            "}",
            ")",
            "^",
            "{",
            "1",
            "+",
            "2\\pi i",
            "}",
            # for Thumbnail
            color=BLACK,
            # / for Thumbnail
        ).scale(1.5)
        s0 = start[1]
        s1 = start[2:8]
        s2 = VGroup(start[0], start[8])
        s3 = start[9:]
        self.play(FadeIn(s0))
        self.play(LaggedStart(*[FadeIn(item) for item in s1], lag_ratio=0.1))
        self.play(FadeIn(s2))
        self.playw(LaggedStart(*[FadeIn(item) for item in s3], lag_ratio=0.1))
        # for Thumbnail
        # return
        # / for Thumbnail
        self.playw(start.animate.scale(0.7))

        eq1 = MathTex("=", "e", "=", "2.71828...").set_color_by_gradient(
            GREEN_A, GREEN_C
        )
        eq2 = MathTex("=", "0.000000000000000019...").set_color_by_gradient(
            RED_A, RED_C
        )
        eqs = (
            VGroup(eq1, eq2)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.75)
            .next_to(start, RIGHT, buff=0.5)
        )
        self.play(FadeIn(eq1[0]))
        self.playwl(FadeIn(eq1[1]), FadeIn(eq1[2]), lag_ratio=0.5, wait=0.1)
        self.playw(FadeIn(eq1[3:]))
        self.playwl(
            FadeIn(eq2[0]),
            AnimationGroup(*[FadeIn(item) for item in eq2[1:]], lag_ratio=0.1),
            AnimationGroup(
                self.cf.animate.shift(RIGHT), start.animate.set_color(GREY_B)
            ),
            lag_ratio=0.5,
        )

        start_p = BrokenLine(
            start.get_center(),
            start.get_center() + UP * 1.5 + RIGHT * 0.2,
            ORIGIN + UP * 2.5 + RIGHT,
            smooth=True,
        )
        eq11, eq21 = eq1[1:], eq2[1:]
        neq = MathTex("\\neq", color=GREY_B).set_opacity(0)
        self.playwl(
            MoveAlongPath(start, start_p),
            FadeOut(eq1[0], eq2[0]),
            VGroup(eq11, neq, eq21).animate.arrange(RIGHT, buff=0.5).shift(RIGHT),
            lag_ratio=0.5,
            run_time=2,
            wait=0.1,
        )
        self.playw(neq.animate.set_opacity(1))
        eq22 = VGroup(
            MathTex("=", color=GREY_A).next_to(eq21, LEFT).set_opacity(0), eq21
        )
        eq12 = eq11[1:]
        s0 = start.copy()
        s1 = start
        self.play(
            VGroup(s0, eq12)
            .animate.arrange(DOWN, buff=4, aligned_edge=LEFT)
            .shift(LEFT * 2 + UP * 0.5),
            FadeOut(eq11[0], neq),
            VGroup(s1, eq22)
            .animate.arrange(DOWN, buff=4, aligned_edge=LEFT)
            .shift(RIGHT * 4 + UP * 0.5),
        )
        sol1 = DashedVMobject(
            Rectangle(height=3.5, width=3.5, stroke_width=2, color=GREY_B)
            .move_to(VGroup(s0, eq12))
            .align_to(VGroup(s0, eq12), LEFT),
            num_dashes=60,
        )
        sol2 = DashedVMobject(
            Rectangle(height=3.5, width=4.5, stroke_width=2, color=GREY_B)
            .move_to(VGroup(s1, eq22))
            .align_to(VGroup(s1, eq22), LEFT),
            num_dashes=60,
        )

        self.playw(eq22[0].animate.set_opacity(1), FadeIn(sol1, sol2))


class solution1(Scene2D):
    def construct(self):

        st = MathTex(
            *["(", "e", "^"],  # 0-2
            *["{", "1", "+", "2\\pi i", "}"],  # 3-7
            ")",  # 8
            "^",  # 9
            *["{", "1", "+", "2\\pi i", "}"],  # 10-14
        )
        end = MathTex(
            "=",
            "2.71828...",
        )
        se = VGroup(st, end).arrange(RIGHT)
        self.playwl(*[FadeIn(item) for item in [st, end[0], end[1]]], lag_ratio=0.3)

        step1 = MathTex(
            "=",  # 0
            *["(", "e", "^"],  # 1-3
            *["{", "1", "}"],  # 4-6
            "\\times",  # 7
            *["e", "^"],  # 8-9
            *["{", "2\\pi i", "}"],  # 10-12
            ")",  # 13
            "^",  # 14
            *["{", "1", "+", "2\\pi i", "}"],  # 15-19
        )

        def get_euler(x):
            item = MathTex(
                *["e", "^", "{", f"{x} i", "}"],  # 0~4
                "=",  # 5
                *["\\cos", "(", x, ")"],  # 6~9
                "+",  # 10
                *["i", "\\sin", "(", x, ")"],  # 11~14,
                font_size=36,
                color=GREY_A,
            )
            VGroup(item[3], item[8], item[14]).set_color(YELLOW_C)
            return item

        euler_theta = get_euler(r"\theta")
        euler_2pi = get_euler("2\\pi")

        step2 = MathTex(
            "=",  # 0
            *["(", "e"],  # 1-2
            "\\times",  # 3
            "1",  # 4
            ")",  # 5
            "^",  # 6
            *["{", "1", "+", "2\\pi i", "}"],  # 7-11
        )
        step3 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            *["{", "1", "+", "2\\pi i", "}"],  # 3-7
        )
        step4 = MathTex(
            "=",  # 0
            "e",  # 1
        )
        for item in [st, step1, step2, step3, step4, end]:
            item.generate_target()
        VGroup(
            *[item.target for item in [st, step1, step2, step3, step4, end]]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP * 0.5)
        euler_theta.next_to(step1.target, RIGHT, buff=1.0)
        euler_2pi.next_to(step1.target, RIGHT, buff=1.0)

        self.playw(MoveToTarget(st), MoveToTarget(end))
        step1.move_to(step1.target)
        t = partial(Transform, replace_mobject_with_target_in_scene=True)
        step1[2:12].set_color(GREEN_C)
        self.playw(
            FadeIn(step1[0]),
            t(st[:2].copy(), step1[1:3]),
            t(st[4].copy(), step1[5]),
            t(st[5].copy(), step1[7:9]),
            t(st[6].copy(), step1[11]),
            t(st[8:].copy(), step1[13:]),
            st[1:7].animate.set_color(GREEN_C),
        )
        self.playw(FadeOut(step1[5]))
        self.playw(FadeIn(euler_theta, scale=1.1))
        self.playw(t(euler_theta, euler_2pi))
        one = MathTex("1", font_size=36, color=GREY_A).move_to(euler_2pi[6:10])
        zeroi = MathTex("0 \\cdot i", font_size=36, color=GREY_A).move_to(
            euler_2pi[11:]
        )
        self.playw(t(euler_2pi[11:], zeroi))
        self.playw(Transform(euler_2pi[6:10], one))
        self.playw(FadeOut(zeroi, euler_2pi[10]))
        one = (
            MathTex("1", font_size=36, color=GREEN_C)
            .move_to(step1[8:13])
            .shift(DOWN * 0.07)
        )
        step2.move_to(step2.target)
        step2[2:5].set_color(GREEN_C)
        self.playw(
            FadeIn(step2[0]),
            t(step1[1:3].copy(), step2[1:3]),
            t(step1[7].copy(), step2[3]),
            t(step1[8:14].copy(), step2[4:6]),
            t(step1[14:].copy(), step2[6:]),
        )

        step3.move_to(step3.target)
        step3[1].set_color(GREEN_C)
        self.playw(
            FadeIn(step3[0]),
            t(step2[2].copy(), step3[1]),
            t(step2[7:].copy(), step3[3:]),
        )

        self.playw(
            Flash(st[1].get_corner(UL)),
            Indicate(st[1:7], color=YELLOW, scale_factor=1.02),
        )

        step4.move_to(step4.target)
        step4[1].set_color(GREEN_C)

        self.playw(
            FadeIn(step4[0]),
            t(step3[1].copy(), step4[1]),
        )

        return


class solution2(Scene2D):
    def construct(self):

        st = MathTex(
            *["(", "e", "^"],  # 0-2
            *["{", "1", "+", "2\\pi i", "}"],  # 3-7
            ")",  # 8
            "^",  # 9
            *["{", "1", "+", "2\\pi i", "}"],  # 10-14
        )
        end = MathTex(
            "=",
            "0.000000000000000019...",
        )
        se = VGroup(st, end).arrange(RIGHT)

        form = MathTex(
            *["(a^", "b", ")", "^c"],  # 0-3
            "=",  # 4
            *["a^", "{b", "\\times", "c}"],  # 5-8
            font_size=36,
            color=GREY_A,
        )
        step1 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            *["(", "1", "+", "2\\pi i", ")"],  # 4-8
            "\\times",  # 9
            *["(", "1", "+", "2\\pi i", ")"],  # 10-14
            "}",  # 15
        )
        step2 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            *["1", "+", "4\\pi i", "-", "4\\pi^2"],  # 4-8
            "}",  # 9
        )
        step3 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            *["1", "-", "4\\pi^2", "+", "4\\pi i"],  # 4-8
            "}",  # 9
        )

        # step4: 이 지수들을 실수와 허수,
        # 각각 곱으로 분리하면
        # exp( 1 - 4π² ) * exp(4πi) 이고요
        step4 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            *["1", "-", "4\\pi^2"],  # 4-6
            "}",  # 7
            "\\times",  # 8
            *["e", "^"],  # 9-10
            "{",  # 11
            "4\\pi i",  # 12
            "}",  # 13
        )

        def get_euler(x):
            item = MathTex(
                *["e", "^", "{", f"{x} i", "}"],  # 0~4
                "=",  # 5
                *["\\cos", "(", x, ")"],  # 6~9
                "+",  # 10
                *["i", "\\sin", "(", x, ")"],  # 11~14,
                font_size=36,
                color=GREY_A,
            )
            VGroup(item[3], item[8], item[14]).set_color(YELLOW_C)
            return item

        # 뒤를 오일러 공식,
        # cos4π + isin4π
        # 1 + 0 * i라서
        # 뒤에는 1이 되구요
        euler_4pi = get_euler("4\\pi")

        step5 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            *["1", "-", "4\\pi^2"],  # 4-6
            "}",  # 7
            "\\times",  # 8
            "1",  # 9
        )

        # 그러면 결과는 앞의 것만 남아서
        # exp(1 - 4π²)입니다
        step6 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            *["1", "-", "4\\pi^2"],  # 4-6
            "}",  # 7
        )

        # 1-4π²은 -38.5정도라서요
        step7 = MathTex(
            "=",  # 0
            *["e", "^"],  # 1-2
            "{",  # 3
            "-38.5...",  # 4
            "}",  # 5
        )

        for item in [st, step1, step2, step3, step4, step5, step6, step7, end]:
            item.generate_target()
        VGroup(
            *[
                item.target
                for item in [st, step1, step2, step3, step4, step5, step6, step7, end]
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8).shift(UP * 0.7)
        form.next_to(st.target, RIGHT, buff=1.2)
        form[1].set_color(GREEN_C)
        form[3].set_color(BLUE_C)
        form[6].set_color(GREEN_C)
        form[8].set_color(BLUE_C)
        st[3:8].set_color(GREEN_C)
        st[10:].set_color(BLUE_C)

        st.scale(0.8).move_to(st.target)
        end.scale(0.8).move_to(end.target)
        self.playw(FadeIn(se))

        self.playw(
            Flash(st[3:8].get_corner(UL)),
            Indicate(st[3:8], color=YELLOW, scale_factor=1.02),
            Indicate(st[10:], color=YELLOW, scale_factor=1.02),
        )

        self.playw(FadeIn(form, scale=1.1))

        step1.scale(0.8).move_to(step1.target)
        t = partial(Transform, replace_mobject_with_target_in_scene=True)
        step1[5:8].set_color(GREEN_C)
        step1[11:14].set_color(BLUE_C)
        self.playw(
            FadeIn(step1[0]),
            t(st[1].copy(), step1[1]),
            t(st[4:7].copy(), step1[5:8]),
            FadeIn(VGroup(step1[4], step1[8], step1[9], step1[10], step1[14])),
            t(st[11:14].copy(), step1[11:14]),
        )

        step2.scale(0.8).move_to(step2.target)
        gb = interpolate_color(GREEN_C, BLUE_C, 0.5)
        step2[4:9].set_color(gb)
        self.playw(
            FadeIn(step2[0]),
            FadeTransform(step1[1:3].copy(), step2[1:3]),
            FadeTransform(step1[3:].copy(), step2[3:]),
        )

        step3.scale(0.8).move_to(step3.target)
        step3[4:9].set_color(gb)
        self.play(
            FadeIn(step3[0]),
            t(step2[1:3].copy(), step3[1:3]),
            t(step2[4].copy(), step3[4]),
            t(step2[7:9].copy(), step3[5:7]),
        )
        self.playw(
            t(step2[5:7].copy(), step3[7:9]),
        )

        step4.scale(0.8).move_to(step4.target)
        step4[4:9].set_color(gb)
        step4[12].set_color(gb)

        self.playw(
            FadeIn(step4[0]),
            t(step3[1:7].copy(), step4[1:7]),
            t(step3[7].copy(), step4[8:10]),
            t(step3[8].copy(), step4[12]),
        )

        euler_4pi.scale(0.75).next_to(step4, RIGHT, buff=1.0)
        one = MathTex("1", font_size=36, color=GREY_A).move_to(euler_4pi[6:10])
        zeroi = MathTex("0 \\cdot i", font_size=36, color=GREY_A).move_to(
            euler_4pi[11:]
        )
        self.playw(FadeIn(euler_4pi, scale=1.1))
        self.play(t(euler_4pi[6:10], one))
        self.play(t(euler_4pi[11:], zeroi))
        self.playw(FadeOut(zeroi, euler_4pi[10]))

        step5.scale(0.8).move_to(step5.target)
        step5[4:9].set_color(gb)
        self.playw(
            FadeIn(step5[0]),
            t(step4[1:9].copy(), step5[1:9]),
            t(step4[9:].copy(), step5[9]),
        )

        step6.scale(0.8).move_to(step6.target)
        step6[4:7].set_color(gb)
        self.playw(
            FadeIn(step6[0]),
            t(step5[1:7].copy(), step6[1:7]),
        )

        step7.scale(0.8).move_to(step7.target)
        step7[4].set_color(gb)
        self.playw(
            FadeIn(step7[0]),
            t(step6[1:3].copy(), step7[1:3]),
            FadeTransform(step6[4:7].copy(), step7[4]),
        )


class power_complex(Scene2D):
    def construct(self):
        st = MathTex(
            *["a", "^", "x"],  # 0-2
            "=",  # 3
            *["e", "^", "{", "x", "\\ln", "a", "}"],  # 4-10
            color=GREY_A,
        )

        self.addw(st, wait=2)
        self.playw(
            st[8:10].animate.set_color(RED_C),
            Flash(st[8:10].get_corner(UL), color=RED_C, line_length=0.1),
        )


class power(Scene2D):
    def construct(self):
        cond1 = MathTex(
            *["a", "^", "x"],  # 0-2
            ",",  # 3
            *["\\quad", "x", "\\in", r"\mathbb{Z}"],  # 4-7
            color=GREY_A,
            font_size=40,
        )
        ax = cond1[:3]
        ax.save_state()
        ax.move_to(ORIGIN)
        self.playw(FadeIn(ax))
        self.play(Restore(ax))
        self.play(FadeIn(cond1[3:]))
        self.playw(cond1.animate.to_edge(UP, buff=1))

        eq1a = MathTex(
            "a^x",
            "=",
            "1",
            *["\\times", "a", "\\times", "a", "\\times", "...", "\\times", "a"],  # 3-10
            color=GREY_A,
        )
        eq1a[3:].set_color(BLUE_C)
        eq1b = MathTex(
            "a^x",
            "=",
            "1",
            *["\\div", "a", "\\div", "a", "\\div", "...", "\\div", "a"],  # 3-10
            "}",  # 11
            color=GREY_A,
        )
        eq1b[3:].set_color(BLUE_C)
        eq1s = VGroup(eq1a, eq1b).arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        br1a = Brace(eq1a[3:], DOWN, buff=0.2, color=GREY_B)
        eq1at = MathTex("x", color=BLUE_C).next_to(br1a, DOWN, buff=0.1)
        eq1ac = MathTex(">= 0", color=GREY_B, font_size=36).next_to(
            eq1at, RIGHT, buff=0.3
        )
        self.play(FadeIn(eq1a))
        self.playwl(FadeIn(br1a), FadeIn(eq1at), FadeIn(eq1ac), lag_ratio=0.5)

        br1b = Brace(eq1b[3:-1], DOWN, buff=0.2, color=GREY_B)
        eq1bt = MathTex("x", color=BLUE_C).next_to(br1b, DOWN, buff=0.1)
        eq1bc = MathTex("< 0", color=GREY_B, font_size=36).next_to(
            eq1bt, RIGHT, buff=0.3
        )
        self.play(FadeIn(eq1b))
        self.playwl(FadeIn(br1b), FadeIn(eq1bt), FadeIn(eq1bc), lag_ratio=0.5)

        ax1 = VGroup(eq1a, eq1b, br1a, eq1at, eq1ac, br1b, eq1bt, eq1bc)
        self.play(
            ax1.animate.shift(LEFT * 4.75).scale(0.75).set_opacity(0.5),
            cond1.animate.shift(LEFT * 4.75),
        )

        __l1 = DashedLine(
            self.cf.get_left() * (2 / 3) + self.cf.get_right() * (1 / 3) + UP * 5,
            self.cf.get_left() * (2 / 3) + self.cf.get_right() * (1 / 3) + DOWN * 5,
            color=GREY_D,
            stroke_width=2,
            dashed_ratio=0.5,
            dash_length=0.05,
        )
        __l2 = DashedLine(
            self.cf.get_left() * (1 / 3) + self.cf.get_right() * (2 / 3) + UP * 5,
            self.cf.get_left() * (1 / 3) + self.cf.get_right() * (2 / 3) + DOWN * 5,
            color=GREY_D,
            stroke_width=2,
            dashed_ratio=0.5,
            dash_length=0.05,
        )
        self.playw(FadeIn(__l1))

        #

        cond2 = MathTex(
            *["a", "^", "x"],  # 0-2
            ",",  # 3
            *["\\quad", "x", "\\in", r"\mathbb{C}"],  # 4-7
            ",",  # 8
            *["\\quad", "a", "\\neq", r"e"],  # 9-12
            color=GREY_A,
            font_size=40,
        ).to_edge(UP, buff=1)
        self.playw(FadeIn(cond2, scale=1.1))

        eq2 = MathTex(
            "a^x",  # 0
            "=",  # 1
            *["e", "^", "{", "x", "\\ln", "a", "}"],  # 2-8
            color=GREY_A,
        )
        self.playwl(
            *[FadeIn(item) for item in [eq2[0], eq2[1], eq2[2:]]], lag_ratio=0.3
        )
        self.playw(Indicate(eq2[2:6], color=PURE_RED, scale_factor=1.02))
        self.playw(eq2[6:8].animate.set_color(RED))

        #
        cond3 = (
            MathTex(
                *["a", "^", "x"],  # 0-2
                ",",  # 3
                *["\\quad", "x", "\\in", r"\mathbb{C}"],  # 4-7
                ",",  # 8
                *["\\quad", "a", "=", r"e"],  # 9-12
                color=GREY_A,
                font_size=40,
            )
            .to_edge(UP, buff=1)
            .shift(RIGHT * 4.75)
        )
        self.play(FadeIn(__l2))
        self.playw(FadeIn(cond3, scale=1.1))

        eq3 = MathTex(
            *["a^x", "=", r"e^x", "="],  # 0-3
            *[
                r"\sum_{n=0}",
                "^",
                r"{\infty}",
                "{",
                r"{x",
                "^n",
                r"}\over{n!}",
                "}",  # 5-12
            ],
            color=GREY_A,
            font_size=36,
        ).shift(RIGHT * 4.75)
        eq3[2:].set_color(GREEN_C)
        self.playw(FadeIn(eq3))
        self.playw(Indicate(eq3[9], color=YELLOW_C, scale_factor=1.2))

        self.play(
            Flash(cond1.get_corner(UL), color=YELLOW_C),
            Indicate(cond1, color=YELLOW_C, scale_factor=1.02),
        )
        self.playw_return(ax1.animate.set_opacity(1))

        eq32 = (
            MathTex(
                "=",  # 0
                "1 +",  # 1
                *["{x", "\\over", "1!}"],  # 2-4
                *[" + ", "{x", "\\times x", "\\over", "2!}"],  # 5-9
                *[" + ", "..."],
                color=GREY_A,
                font_size=36,
            )
            .next_to(eq3, DOWN, buff=0.5)
            .align_to(eq3, LEFT)
        )
        self.playw(FadeIn(eq32))

        eq22 = MathTex(
            "=",  # 0
            "1 + ",  # 1
            *["{x \\ln a", "\\over", "1!}"],  # 2-4
            *[" + ", "{(x \\ln a)", "\\times", "(x \\ln a)", "\\over", "2!}"],  # 5-9
            *[" + ", "..."],
            color=GREY_A,
            font_size=24,
        ).next_to(eq2, DOWN, buff=0.5)
        self.playw(FadeIn(eq22))

        #
        ax3 = VGroup(eq3, eq32)
        self.play(
            ax3.animate.shift(RIGHT * 5).scale(0.75),
            cond3.animate.shift(RIGHT * 5),
            __l2.animate.shift(RIGHT * 5),
            ax1.animate.shift(LEFT * 5).set_opacity(0.5),
            cond1.animate.shift(LEFT * 5),
            __l1.animate.shift(LEFT * 5),
        )
        self.playw(eq22.animate.scale(1.5).align_to(eq2[1], LEFT))
        lna = eq2[6:8]
        self.play(
            cond2.animate.shift(UP * 2),
            FadeOut(eq2[:6], shift=LEFT * 2),
            FadeOut(eq22, shift=DOWN * 2),
        )
        self.playw(lna.animate.move_to(ORIGIN).scale(1.8))
        lnac = lna.copy()

        lna1 = MathTex("=", "p", "+", "q", "i", font_size=36, color=GREY_A).next_to(
            lna, RIGHT
        )
        lna2 = (
            MathTex(
                "=",
                *["p", "+"],
                *["(", "q", "+", r"2 \pi", ")"],
                "i",
                font_size=36,
                color=GREY_A,
            )
            .next_to(lna1, DOWN, buff=0.5)
            .align_to(lna1, LEFT)
        )
        lna3 = (
            MathTex(
                "=",
                *["p", "+"],
                *["(", "q", "+", "...", ")"],
                "i",
                font_size=36,
                color=GREY_A,
            )
            .next_to(lna2, DOWN, buff=0.5)
            .align_to(lna1, LEFT)
        )
        self.play(FadeIn(lna1))
        self.play(FadeIn(lna2))
        self.playw(FadeIn(lna3))

        lns = VGroup(lna, lna1, lna2, lna3)
        lns.save_state()
        self.playw(lns.animate.shift(LEFT * 5.5).set_opacity(0.3))

        #

        log2_8 = MathTex(
            r"\log", "_", "2", "8", ":", "2", "^", "p", "=", "8", color=GREY_A
        )
        log2_8[2].set_color(GREEN_C)
        log2_8[3].set_color(BLUE_C)
        log2_8[5].set_color(GREEN_C)
        log2_8[9].set_color(BLUE_C)
        self.playw(FadeIn(log2_8[:5], scale=1.2))
        self.play(FadeIn(log2_8[5]))
        self.playw(FadeIn(log2_8[7:9]))
        self.playw(FadeIn(log2_8[9]))

        self.playw(Indicate(log2_8[:4]), Indicate(log2_8[7]))

        loga_b = MathTex(
            r"\log", "_", "a", "b", ":", "a", "^", "p", "=", "b", color=GREY_A
        )
        loga_b[2].set_color(GREEN_C)
        loga_b[3].set_color(BLUE_C)
        loga_b[5].set_color(GREEN_C)
        loga_b[9].set_color(BLUE_C)
        self.play(FadeOut(log2_8, shift=UP * 2), run_time=0.5)
        self.playw(FadeIn(loga_b[:5], scale=1.2))
        self.play(FadeIn(loga_b[5]))
        self.playw(FadeIn(loga_b[7:9]))
        self.playw(FadeIn(loga_b[9]))
        self.playw(Indicate(loga_b[:4]), Indicate(loga_b[7]))

        self.playw(FadeOut(loga_b, shift=UP * 2), Restore(lns))

        loge_a = MathTex(
            r"\log", "_", "e", "a", ":", "e", "^", "p", "=", "a", color=GREY_A
        )
        loge_a[2].set_color(GREEN_C)
        loge_a[3].set_color(BLUE_C)
        loge_a[5].set_color(GREEN_C)
        loge_a[9].set_color(BLUE_C)
        self.playw(FadeTransform(lna, loge_a[:5]), FadeOut(lns[1:], shift=RIGHT * 2))

        loge_3 = MathTex(
            r"\log", "_", "e", "3", ":", "e", "^", "p", "=", "3", color=GREY_A
        )
        loge_3[2].set_color(GREEN_C)
        loge_3[3].set_color(BLUE_C)
        loge_3[5].set_color(GREEN_C)
        loge_3[9].set_color(BLUE_C)
        self.playw(
            Transform(loge_a[:5], loge_3[:5], replace_mobject_with_target_in_scene=True)
        )
        self.playwl(
            FadeIn(loge_3[5]), FadeIn(loge_3[7:9]), FadeIn(loge_3[9]), lag_ratio=0.3
        )
        self.playw(Indicate(loge_3[:4]), Indicate(loge_3[7]))

        lna = lnac
        self.playw(FadeOut(loge_3, shift=UP * 2), FadeIn(lna, scale=1.2))

        ln3 = MathTex(
            r"\ln 3",
            color=GREY_A,
        ).move_to(lna)
        self.playw(FadeTransform(lna, ln3))


class multivalue(Scene2D):
    def construct(self):
        cp = (
            ComplexPlane(
                x_range=[-3.5, 3.5, 1],
                y_range=[-3.5, 3.5, 1],
                background_line_style={"stroke_color": GREY_D, "stroke_width": 1},
            )
            .scale(0.9)
            .shift(UP * 0.5 + LEFT)
            .add_coordinates()
        )
        cp.coordinate_labels.set_opacity(0.7)

        pm = lambda i: "+" if i >= 0 else "-"

        def get_exp(r, i):
            item = (
                MathTex(
                    "e",  # 0
                    "^",  # 1
                    *["{", pm(r), f"{r:.2f}", pm(i), f"{abs(i):.2f}i", "}"],  # 2-7
                    r"\\",  # 8
                    "=",  # 9
                    *[
                        pm(np.cos(i)),
                        f"{abs(np.exp(r)*np.cos(i)):.2f}",
                        pm(np.sin(i)),
                        f"{abs(np.exp(r)*np.sin(i)):.2f}i",
                    ],  # 10-13
                    font_size=36,
                    color=GREY_A,
                )
                .next_to(cp, RIGHT, buff=0.5)
                .shift(UP)
            )
            item[4].set_color(GREEN_C)
            item[6].set_color(YELLOW_C)
            item[11].set_color(GREEN_C)
            item[13].set_color(YELLOW_C)
            return item

        r = ValueTracker(1)
        i = ValueTracker(0.78)
        eq = get_exp(r.get_value(), i.get_value())

        get_point = lambda z: Dot(cp.n2p(z), color=BLUE_B, radius=0.06)
        p = get_point(np.exp(r.get_value() + i.get_value() * 1j))
        get_line = lambda: DashedLine(
            eq[9].get_left(), p.get_center(), buff=0.1, color=GREY_C, dashed_ratio=0.5
        )
        line = get_line()

        self.playw(FadeIn(cp, eq, p, line))

        eq.add_updater(lambda m: m.become(get_exp(r.get_value(), i.get_value())))
        p.add_updater(
            lambda m: m.move_to(cp.n2p(np.exp(r.get_value() + i.get_value() * 1j)))
        )
        line.add_updater(lambda m: m.become(get_line()))

        self.playw(r.animate.set_value(1.09861), i.animate.set_value(0))

        self.playw(i.animate.set_value(2 * 3.141592), run_time=2)
        self.playw(i.animate.set_value(4 * 3.141592))
        self.playw(i.animate.set_value(-2 * 3.141592), run_time=3)

        self.playw(r.animate.set_value(0), i.animate.set_value(0))
        self.playw(r.animate.set_value(0), i.animate.set_value(2 * 3.141592))
        self.playw(r.animate.set_value(0), i.animate.set_value(4 * 3.141592))
        self.playw(r.animate.set_value(0), i.animate.set_value(-2 * 3.141592))


class solution(Scene2D):
    def construct(self):
        start = MathTex(
            *["(", "e", "^"],  # 0-2
            *["{", "1", "+", "2\\pi i", "}"],  # 3-7
            ")",  # 8
            "^",  # 9
            *["{", "1", "+", "2\\pi i", "}"],  # 10-14
            color=GREY_A,
        )

        ax = MathTex(
            *["a", "^", "x"],  # 2
            "=",  # 3
            *["e", "^", "{", "x", "\\ln", "a", "}"],  # 4-10
            font_size=36,
            color=GREY_A,
        )

        lna = MathTex(
            "\\ln",
            "e",
            ":",
            font_size=36,
            color=GREY_A,
        )
        lna1 = MathTex("1", "+", "0", "i", font_size=36, color=GREY_A).next_to(
            lna, RIGHT
        )
        lna2 = (
            MathTex(
                *["1", "+"],
                *["(", "0", "+", "2\\pi", ")"],
                "i",
                font_size=36,
                color=GREY_A,
            )
            .next_to(lna1, DOWN, buff=0.3)
            .align_to(lna1, LEFT)
        )
        lna3 = (
            MathTex(
                *["1", "+"],
                *["(", "0", "+", "...", ")"],
                "i",
                font_size=36,
                color=GREY_A,
            )
            .next_to(lna2, DOWN, buff=0.3)
            .align_to(lna1, LEFT)
        )
        lnas = VGroup(lna, lna1, lna2, lna3)

        VGroup(
            start, VGroup(ax, lnas).arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        ).arrange(RIGHT, buff=2.0)

        self.playwl(
            *[
                FadeIn(item)
                for item in [
                    start[1],
                    start[3:8],
                    VGroup(start[0], start[8]),
                    start[9:],
                ]
            ],
            lag_ratio=0.3,
            wait=0.1,
        )
        self.playwl(
            *[
                FadeIn(item)
                for item in [
                    ax[:3],
                    ax[3],
                    ax[4:],
                ]
            ],
            lag_ratio=0.3,
            wait=0.1,
        )
        self.playwl(*[FadeIn(item) for item in lnas], lag_ratio=0.3)

        self.playw(
            Flash(start.get_corner(UL), color=YELLOW_C),
            Indicate(start, color=YELLOW_C, scale_factor=1.02),
        )
        self.play(
            Flash(ax.get_corner(UL), color=YELLOW_C), Indicate(ax, color=YELLOW_C)
        )
        self.playw(
            start[1:8].animate.set_color(GREEN_C),
            ax[0].animate.set_color(GREEN_C),
            start[10:].animate.set_color(BLUE_C),
            ax[2].animate.set_color(BLUE_C),
            lnas.animate.set_opacity(0.3),
        )
        self.playw_return(
            start[1:8].animate.shift(DOWN * 0.5), ax[0].animate.shift(DOWN * 0.5)
        )
        self.playw_return(
            start[10:].animate.shift(UP * 0.5), ax[2].animate.shift(UP * 0.5)
        )

        self.playw(
            Flash(ax[4].get_corner(UL), color=YELLOW_C),
            Indicate(ax[4:], color=YELLOW_C),
        )

        ax2 = (
            MathTex(
                *["a", "^", "x"],  # 0-2
                "=",  # 3
                *["e", "^", "{", "(1 + 2\\pi i)"],  # 4-7
                "\\ln",  # 8
                *["e", "^", "{1 + 2\\pi i}"],  # 9-11
                "}",  # 12
                color=GREY_A,
                font_size=36,
            )
            .move_to(ax)
            .align_to(ax, LEFT)
        )
        ax2[0].set_color(GREEN_C)
        ax2[2].set_color(BLUE_C)
        ax2[7].set_color(BLUE_C)
        ax2[9:12].set_color(GREEN_C)
        ft = FadeTransform
        t = partial(Transform, replace_mobject_with_target_in_scene=True)
        self.playw(
            t(ax[0:4], ax2[0:4]),
            ft(ax[4], ax2[4]),
            ft(ax[7], ax2[7]),
            t(ax[8], ax2[8]),
            ft(ax[9:], ax2[9:]),
        )
        self.playw(
            Flash(
                ax2[9:].get_corner(UL),
                color=YELLOW_C,
                line_length=0.1,
                line_stroke_width=2,
            ),
            Indicate(ax2[9:], color=YELLOW_C),
            wait=3,
        )
        self.playw(ax2[10:].animate.set_opacity(0))
        self.play(lna.animate.set_opacity(1))
        self.playw_return(lnas[1:].animate.set_opacity(1))
        self.playw(lna1.animate.set_color(RED_A).set_opacity(1))
        self.playw(lna2.animate.set_color(RED_B).set_opacity(1))
        self.playw(lna3.animate.set_color(RED_C).set_opacity(1))

        eq1 = MathTex(
            "=",  # 0
            "e = 2.71828...",  # 1
            font_size=36,
            color=GREY_A,
        ).next_to(ax2[:8], RIGHT)
        eq2 = (
            MathTex(
                "=",  # 0
                "e^{(1 + 2\\pi i)^2} =",
                "0.000000000000000019...",  # 1
                font_size=36,
                color=GREY_A,
            )
            .move_to(ax2[3:])
            .align_to(ax2[3:], LEFT)
        )
        eq2[-1].scale(0.75).shift(LEFT*0.3 + DOWN*0.03)

        self.playw(lnas[2:].animate.set_opacity(0.3))
        ax2.save_state()
        self.playw(ax2[8:10].animate.set_opacity(0), FadeIn(eq1, scale=1.1))

        self.playw(
            Restore(ax2),
            FadeOut(eq1),
            lna1.animate.set_opacity(0.3),
            lna2.animate.set_opacity(1),
        )
        self.playw(FadeOut(ax2[3:]), FadeIn(eq2[:-1]), FadeIn(eq2[-1], scale=1.1))
