from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        right = r"\frac{e^{x_i}}{`\sum_{j}` e^{x_j}`}"
        softmax_formula = RaeTex(r"\text{softmax}(x_i) =" + f"`{right}", color=GREY_A)
        self.addw(softmax_formula)
        self.wait()

        self.playw(softmax_formula[1:].animate.set_color(RED))
        self.wait()
        self.play(softmax_formula[0].animate.shift(LEFT), run_time=0.5)
        self.playw(RWiggle(softmax_formula[1:]), run_time=3)

        right_after = r"{e^{x_i `- C`} `\over` \sum_{j}` e^{x_j `- C`}}"
        softmax_formula_after = RaeTex(
            r"\text{softmax}(x_i) =`" + f"{right_after}", color=GREY_A
        ).align_to(softmax_formula, RIGHT)
        softmax_formula_after[1:].set_color(GREEN_B)
        softmax_formula_after["- C"].set_color(PURE_GREEN)
        trt = lambda x, y: Transform(x, y, replace_mobject_with_target_in_scene=True)
        self.playw(
            trt(softmax_formula[0], softmax_formula_after[0]),
            trt(softmax_formula[2], softmax_formula_after[5]),
            trt(softmax_formula[3], softmax_formula_after[6:]),
            trt(softmax_formula[1], softmax_formula_after[1:5]),
        )

        s1 = softmax_formula_after[0]
        s2 = softmax_formula_after[1:]
        self.play(FadeOut(s1, shift=LEFT), s2.animate.move_to(ORIGIN))
        self.playw(RWiggle(softmax_formula_after["- C"]), run_time=3)


class softmax_intro(Scene3D):
    def construct(self):
        sf = RaeTex(
            r"\text{softmax}(x_i) `= `{`e^{x_i}` \over \sum_{j} e^{x_j}}", color=GREY_A
        )
        sf[2:].set_color(YELLOW_B)
        self.playwl(
            *[FadeIn(item) for item in [sf[i] for i in [0, 1, 2, 4, 3]]],
            lag_ratio=0.3,
            wait=0,
        )
        self.playw(AnchorToPoint(sf, ORIGIN, sf[2:]))
        sf.generate_target()
        sf.target.set_opacity(0.3)
        sf.target[r"e^{x_i}"].set_opacity(1).set_color(RED)
        self.playw(MoveToTarget(sf))

        nump = (
            NumberPlane(
                x_range=[-1, 10],
                y_range=[-0.5, 7],
                x_length=11,
                y_length=6,
                background_line_style={"stroke_opacity": 0.0},
            )
            .next_to(sf[r"e^{x_i}"], RIGHT, buff=1)
            .shift(UP * 1)
        )
        nump.x_axis.set_opacity(0.5)
        nump.y_axis.set_opacity(0.5)
        p = nump.plot(lambda x: 2.71828**x, x_range=[-1, 3], color=RED)
        self.play(FadeIn(nump))
        self.playw(Create(p))

        v = ValueTracker(0)
        get_dot = lambda: Dot(color=YELLOW).move_to(
            nump.c2p(v.get_value(), 2.71828 ** (v.get_value()))
        )
        dot = get_dot()

        def get_fx():
            r = (
                RaeTex(r"e^{`" + f"{v.get_value():.2f}" + "`}")
                .set_color(RED)
                .move_to(sf[r"e^{x_i}"])
                .align_to(sf[r"e^{x_i}"], LEFT)
            )
            r[1].set_color(YELLOW)
            return r

        fx = get_fx()

        def get_val():
            r = MathTex(
                r"e^{x_i} =", f"{2.71828 ** v.get_value():.5f}", font_size=36
            ).shift(UP * 1.5)
            r[-1].set_color(YELLOW)
            return r

        val = get_val()

        self.play(FadeIn(dot), FadeIn(fx), FadeOut(sf[r"e^{x_i}"]), FadeIn(val))
        dot_fn = lambda d: d.move_to(
            nump.c2p(v.get_value(), 2.71828 ** (v.get_value()))
        )
        dot.add_updater(dot_fn)
        fx.add_updater(
            lambda m: m.become(
                RaeTex(r"e^{`" + f"{v.get_value():.2f}" + "`}")
                .set_color(RED)
                .move_to(sf[r"e^{x_i}"])
                .align_to(sf[r"e^{x_i}"], LEFT)
                .set_color_by_tex(f"{v.get_value():.2f}", YELLOW)
            )
        )
        val.add_updater(lambda m: m.become(get_val()))
        self.playw(v.animate.set_value(1))
        dot.remove_updater(dot_fn)
        dot_fn = lambda d: d.move_to(
            nump.c2p(v.get_value(), min(2.71828 ** (v.get_value()), 9))
        )
        dot.add_updater(dot_fn)
        self.playw(v.animate.set_value(10))
        self.playw(FadeOut(nump, p))


class softmaxC(Scene3D):
    def construct(self):
        sf = RaeTex(
            r"\text{softmax}(x_i) `= `{`e^{x_i}` \over` \sum_{j}` e^{`x_j`}}",
            color=GREY_A,
        ).shift(UP * 1.5)
        sf[2:].set_color(YELLOW_B)

        o = (
            Tensor(6)
            .arrange(RIGHT, buff=1)
            .rotate(-PI / 3, axis=RIGHT)
            .shift(DOWN * 1.5)
        )
        oi = VGroup(
            *[
                MathTex(f"x_{i}", font_size=36).set_color(TEAL_A).next_to(o[i], UP)
                for i in range(len(o))
            ]
        )
        ov = VGroup(
            *[
                DecimalNumber(random() * 10 - 5, font_size=36, color=GREY_B)
                .rotate(-PI / 3, axis=RIGHT)
                .next_to(o[i], DOWN)
                for i in range(len(o))
            ]
        )
        os = VGroup(*[VGroup(o[i], oi[i], ov[i]) for i in range(len(o))])
        o_max = max(os, key=lambda x: x[-1].get_value())
        self.addw(sf, o, oi, ov)
        self.playwl(*[Indicate(item, scale_factor=1.1) for item in o], lag_ratio=0.1)
        self.play(Circumscribe(o_max))
        ct = Text("C", font=MONO_FONT, font_size=24, color=GREEN).next_to(
            o_max, UP, buff=0.3
        )
        self.playw(FadeIn(ct, shift=UP * 0.5))

        get_ec = lambda: MathTex("\\times", r"e^{-C}", font_size=36, color=GREEN)
        ecs = VGroup(get_ec(), get_ec())
        ecs.arrange(DOWN, buff=0.5).next_to(sf, RIGHT, buff=0.4)
        ecs[1].shift(UP * 0.2)
        self.playw(FadeIn(ecs))

        self.playw(RWiggle(ecs, amp=(0.1, 0.1, 0.1)), run_time=3)

        sfa = RaeTex(
            r"\text{softmax}(x_i) `= `{`e^{`x_i `- C`} `\over` \sum_{j}` e^{`x_j `- C`}}",
            color=GREY_A,
        ).shift(UP * 1.5)
        sfa[2:].set_color(YELLOW_B)
        sfa["- C"].set_color(PURE_GREEN)
        trt = lambda x, y: Transform(x, y, replace_mobject_with_target_in_scene=True)
        self.playw(
            trt(sf[0], sfa[0]),
            trt(sf[1], sfa[1]),
            trt(sf[2], sfa[2]),
            trt(sf[3], sfa[3:6]),
            trt(sf[4], sfa[7]),
            trt(sf[5], sfa[8]),
            trt(sf[6], sfa[9]),
            trt(sf[7], sfa[10]),
            trt(sf[8], sfa[11:]),
            FadeOut(ecs, shift=LEFT * 0.5),
        )
        exponent = VGroup(sfa[4:6], sfa[-3:-1])
        self.playw(Circumscribe(VGroup(o_max, ct)))
        self.playw(exponent.animate.shift(RIGHT))
        get_lt0 = lambda: MathTex(r"\le 0", font_size=36, color=YELLOW_B)
        lt0n, lt0d = get_lt0(), get_lt0()
        lt0n.next_to(exponent[0], RIGHT, buff=0.3)
        lt0d.next_to(exponent[1], RIGHT, buff=0.3)
        self.playw(FadeIn(lt0n, shift=RIGHT), FadeIn(lt0d, shift=RIGHT))
        self.playw(FadeOut(lt0n, lt0d), exponent.animate.shift(LEFT))

        exps = VGroup(sfa[3:6], sfa[-4:-1])
        self.playw(RWiggle(exps, amp=(0.1, 0.1, 0.1)), run_time=4)

        self.wait(2)

        self.playw(Circumscribe(sfa[5]), Circumscribe(sfa[-2]))


class comparison(Scene2D):
    def construct(self):
        nums1_list = [0, 1, 2]
        nums2_list = [10, 11, 12]

        nums1 = VGroup(
            *[
                DecimalNumber(num, num_decimal_places=0, font_size=48, color=GREY_B)
                for num in nums1_list
            ]
        ).arrange(RIGHT, buff=1)
        nums2 = VGroup(
            *[
                DecimalNumber(num, num_decimal_places=0, font_size=48, color=GREY_B)
                for num in nums2_list
            ]
        ).arrange(RIGHT, buff=2.0)

        VGroup(nums1, nums2).arrange(RIGHT, buff=3).shift(DOWN)
        self.addw(nums1, nums2)
        sums1_str = r"e^{0} + e^{1} + e^{2}"
        exps1 = (
            VGroup(
                *[
                    RaeTex(
                        "{" + f"e^`{{{num}}}`" + r"\over `" + sums1_str + r"}",
                        font_size=28,
                        color=GREEN_A,
                    )
                    for num in nums1_list
                ]
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(nums1, UP, buff=0.5)
        )
        sums2_str = r"e^{10} + e^{11} + e^{12}"
        exps2 = (
            VGroup(
                *[
                    RaeTex(
                        "{" + f"e^`{{{num}}}`" + r"\over `" + sums2_str + r"}",
                        font_size=28,
                        color=GREEN_A,
                    )
                    for num in nums2_list
                ]
            )
            .arrange(RIGHT, buff=0.8)
            .next_to(nums2, UP, buff=0.5)
        )
        self.playw(FadeIn(exps1, shift=UP), FadeIn(exps2, shift=UP))

        e101_open = RaeTex(r"e^{10} (", font_size=28, color=RED_B).next_to(
            exps2[0][3], LEFT, buff=0.05
        )
        e101_close = RaeTex(r")", font_size=28, color=RED_B).next_to(
            exps2[0][-1], RIGHT, buff=0.05
        )
        e102_open = RaeTex(r"e^{10} (", font_size=28, color=RED_B).next_to(
            exps2[1][3], LEFT, buff=0.05
        )
        e102_close = RaeTex(r")", font_size=28, color=RED_B).next_to(
            exps2[1][-1], RIGHT, buff=0.05
        )
        e103_open = RaeTex(r"e^{10} (", font_size=28, color=RED_B).next_to(
            exps2[2][3], LEFT, buff=0.05
        )
        e103_close = RaeTex(r")", font_size=28, color=RED_B).next_to(
            exps2[2][-1], RIGHT, buff=0.05
        )
        self.play(
            FadeIn(e101_open, e101_close),
            FadeOut(exps2[0][-1][-2], exps2[0][-1][-6], exps2[0][-1][-10]), 
            FadeIn(e102_open, e102_close),
            FadeOut(exps2[1][-1][-2], exps2[1][-1][-6], exps2[1][-1][-10]),
            FadeIn(e103_open, e103_close),
            FadeOut(exps2[2][-1][-2], exps2[2][-1][-6], exps2[2][-1][-10]),
        )

        self.playw(
            FadeOut(e101_open, e101_close, e102_open, e102_close, e103_open, e103_close),
            FadeOut(exps2[0][1][0], exps2[1][1][0], exps2[2][1][0])
        )
