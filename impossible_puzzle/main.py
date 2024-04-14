from manim import *
from manimdef import DefaultManimClass


def get_sum_split(sum_int):
    result = []
    for i in range(2, sum_int - 1):
        first, second = i, sum_int - i
        if first < second:
            result.append([first, second])
    return result


class Main(DefaultManimClass):
    def construct(self):
        self.sceneA()

    def sceneA(self):
        a = Text("a", font="Consolas", font_size=48, color=GREEN)
        b = Text("b", font="Consolas", font_size=48, color=BLUE)
        VGroup(a, b).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 12)
        a.align_to(b, DOWN)
        self.playw(LaggedStart(FadeIn(a), FadeIn(b), lag_ratio=0.5))
        a2 = MathTex(">= 2", font_size=36).next_to(a)
        b2 = MathTex(">= 2", font_size=36).next_to(b)
        self.playw(LaggedStart(FadeIn(a2), FadeIn(b2), lag_ratio=0.3))
        plus = Text("+", font="Consolas", font_size=28).set_opacity(0)
        self.play(FadeOut(a2, b2))
        self.playw(
            VGroup(a, plus, b).animate.arrange(RIGHT), plus.animate.set_opacity(1.0)
        )
        small100 = MathTex("<= 100", font_size=36).next_to(b)
        self.playw(FadeIn(small100))

        s, p = ImageMobject("seoksir.png").scale(0.2).shift(2 * LEFT), ImageMobject(
            "parksir.png"
        ).scale(0.2).shift(2 * RIGHT)
        s_info = MathTex("a", "+", "b", font_size=24).next_to(s, UP)
        p_info = MathTex("a", "\\times", "b", font_size=24).next_to(p, UP)

        self.playw(
            FadeOut(small100, plus), VGroup(a, b).animate.shift(UP * 3), FadeIn(s, p)
        )
        self.playw(FadeIn(s_info, shift=DOWN))
        self.playw(FadeIn(p_info, shift=DOWN))
        self.wait(5)
        self.camera.frame.save_state()
        self.playw(self.camera.frame.animate.move_to(s).scale(0.6))
        sum5 = Text("5", font="Consolas", font_size=24, color=YELLOW).move_to(s_info)
        s_info.save_state()
        s_info5 = Tex("2", "+", "3", font_size=24).next_to(s, UP)
        self.playw(Transform(s_info, sum5))
        self.playw(Transform(s_info, s_info5))
        self.playw(Restore(s_info), self.camera.frame.animate.move_to(p))

        p_info513 = MathTex(
            "5", "\\times", "13", font_size=24, color=PURE_GREEN
        ).move_to(p_info)
        p_info311 = MathTex("3", "\\times", "11", font_size=24, color=PURE_RED).move_to(
            p_info
        )
        p_info1117 = MathTex("11", "\\times", "17", font_size=24, color=YELLOW).move_to(
            p_info
        )
        result1117 = MathTex(
            "a=11", "\\quad", "b=17", font_size=24, color=YELLOW
        ).move_to(p_info)
        p_info.save_state()
        self.playw(Transform(p_info, p_info513))
        self.playw(Transform(p_info, p_info311))
        self.playw(Transform(p_info, p_info1117))
        self.playw(Transform(p_info, result1117))
        self.playw(self.camera.frame.animate.move_to(s).scale(1.1), Restore(p_info))

        num_s_int = 11
        num_s = Text(
            f"{num_s_int}", font="Consolas", font_size=32, color=YELLOW
        ).move_to(s_info)
        s_info.save_state()
        self.playw(Transform(s_info, num_s))
        candidates = (
            VGroup(
                *[
                    MathTex(f"a = {i}", "\\quad", f"b = {num_s_int-i}", font_size=24)
                    for i in range(2, num_s_int // 2 + 1)
                ]
            )
            .arrange(DOWN)
            .next_to(s, UP)
        )
        self.playw(
            s_info.animate.shift(LEFT).shift(LEFT),
            LaggedStart(
                *[FadeIn(candidates[i]) for i in range(len(candidates))], lag_ratio=0.2
            ),
            run_time=1.5,
        )
        self.playw(
            candidates[0][-1].animate.set_color(PURE_RED),
            candidates[1][-1].animate.set_color(PURE_RED),
            candidates[2][0].animate.set_color(PURE_RED),
            candidates[3][-1].animate.set_color(PURE_RED),
        )
        self.playw(FadeOut(candidates), Restore(s_info), Restore(self.camera.frame))

        exclam_p = Text("!", font_size=36, color=YELLOW).move_to(p_info)
        self.playw(FadeTransform(p_info, exclam_p))
        self.playw(FadeOut(exclam_p))
        self.playw(FadeOut(p))

        exclam_s = Text("!", font_size=36, color=YELLOW).move_to(s_info)
        self.playw(FadeTransform(s_info, exclam_s))
        self.playw(FadeOut(exclam_s))
        self.playw(FadeOut(s))
        self.playw(Restore(self.camera.frame))
        self.wait(3)

        self.playw(FadeIn(s, s_info))
        self.playw(FadeIn(p, p_info))
        self.wait(3)
        self.camera.frame.save_state()
        self.playw(self.camera.frame.animate.move_to(p).scale(0.6))
        p_answer = MathTex("52", font_size=32).move_to(p_info)
        self.play(p_info.animate.scale(1.5))
        self.playw(Transform(p_info, p_answer))
        p_can1 = MathTex("a=4", "\\quad", "b=13", font_size=24)
        p_can2 = MathTex("a=2", "\\quad", "b=26", font_size=24)
        p_can = VGroup(p_can1, p_can2).arrange(DOWN).next_to(p, UP)
        self.playw(FadeTransform(p_info, p_can))

        self.playw(Restore(self.camera.frame))
        self.wait()

        self.playw(
            self.camera.frame.animate.move_to(p).scale(0.6)
        )  # 어.. 이제 해골을 굴려봅니다
        self.playw(FadeOut(p_can2))
        sum17 = MathTex("a + b", "= 17", font_size=24, color=YELLOW).move_to(p_can1)
        self.playw(FadeTransform(p_can1, sum17))
        sp_candidate = (
            VGroup(
                *[
                    MathTex(f"a={i}", "\\quad", f"b={17-i}", font_size=18, color=BLUE)
                    for i in range(2, 17 // 2 + 1)
                ]
            )
            .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.5)
            .next_to(sum17)
            .shift(DOWN * 0.5)
        )
        self.playw(
            LaggedStart(
                *[
                    FadeIn(sp_candidate[i], target_position=sum17)
                    for i in range(len(sp_candidate))
                ],
                lag_ratio=0.2,
            ),
            run_time=2,
        )
        self.playw(
            LaggedStart(
                *[
                    sp_candidate[0][-1].animate.set_color(PURE_RED),
                    sp_candidate[1][-1].animate.set_color(PURE_RED),
                    sp_candidate[2][0].animate.set_color(PURE_RED),
                    sp_candidate[3][-1].animate.set_color(PURE_RED),
                    sp_candidate[4][0].animate.set_color(PURE_RED),
                    sp_candidate[5][-1].animate.set_color(PURE_RED),
                    sp_candidate[6][0].animate.set_color(PURE_RED),
                    sp_candidate[6][-1].animate.set_color(PURE_RED),
                ],
                lag_ratio=0.1,
            ),
            run_time=2.0,
        )  # 이거 전부 다 소수 쌍이 아니네?
        self.playw(FadeOut(sp_candidate, sum17), FadeIn(p_can2))
        sum28 = MathTex("a + b", "= 28", font_size=24, color=YELLOW).move_to(p_can2)
        self.playw(FadeTransform(p_can2, sum28))
        sp_candidate = (
            VGroup(
                *[
                    MathTex(f"a={i}", "\\quad", f"b={28-i}", font_size=18, color=BLUE)
                    for i in range(2, 28 // 2)
                ]
            )
            .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.5)
            .next_to(sum28)
            .shift(DOWN * 0.5)
        )
        for i in range(len(sp_candidate)):
            if not is_prime(i + 2):
                sp_candidate[i][0].set_color(PURE_RED)
            if not is_prime(28 - i - 2):
                sp_candidate[i][-1].set_color(PURE_RED)
        self.playw(
            LaggedStart(
                *[FadeIn(sp_candidate[i]) for i in range(len(sp_candidate))],
                lag_ratio=0.1,
            )
        )
        self.playw(
            sp_candidate[3].animate.shift(RIGHT).scale(1.5),
            sp_candidate[-3].animate.shift(RIGHT).scale(1.5),
        )
        self.playw(FadeOut(sp_candidate), sum28.animate.set_color(PURE_RED))
        self.playw(Restore(self.camera.frame), FadeIn(sum17))
        self.playw(FadeOut(sum28))

        self.playw(FadeOut(sum17, p))
        s.save_state()
        self.play(s.animate.scale(1.3))
        self.playw(Restore(s))

        s_17 = Text("17", font="Consolas", font_size=24, color=YELLOW).move_to(s_info)
        self.camera.frame.save_state()
        self.playw(
            Transform(s_info, s_17), self.camera.frame.animate.move_to(s).scale(0.6)
        )
        candidates = (
            VGroup(
                *[
                    MathTex(f"a = {i}", "\\quad", f"b = {17-i}", font_size=18)
                    for i in range(2, 17 // 2 + 1)
                ]
            )
            .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.5)
            .next_to(s_info, LEFT)
        )
        self.playw(
            LaggedStart(
                *[
                    FadeIn(candidates[i], target_position=s_info)
                    for i in range(len(candidates))
                ]
            )
        )
        self.playw(
            LaggedStart(
                candidates[0][-1].animate.set_colot(PURE_RED),
                candidates[1][-1].animate.set_colot(PURE_RED),
                candidates[2][0].animate.set_colot(PURE_RED),
                candidates[3][-1].animate.set_colot(PURE_RED),
                candidates[4][0].animate.set_colot(PURE_RED),
                candidates[5][-1].animate.set_colot(PURE_RED),
                candidates[6][-1].animate.set_colot(PURE_RED),
            )
        )
        p_candidates, p_answers = [], []
        for i in range(2, 9):
            a, b = i, 17 - i
            p_candidate = Text(
                f"{a} * {b}", font="Consolas", font_size=18, color=PURE_GREEN
            ).next_to(candidates[i - 2], LEFT)
            p_answer = Text(
                f"{a*b}", font="Consolas", font_size=18, color=PURE_GREEN
            ).move_to(p_candidate)
            if i == 8:
                p_answer.align_to(p_answers[-1], LEFT)
            p_candidate.save_state()
            p_candidates.append(p_candidate)
            p_answers.append(p_answer)
            self.playw(FadeIn(p_candidate, shift=LEFT))
            self.playw(Transform(p_candidate, p_answer))
            if i == 4:
                p_real = p_candidate
        p_candidates = VGroup(*p_candidates)
        p_real.save_state()
        self.playw(p_real.animate.set_color(PURE_BLUE))
        self.playw(Restore(p_real))

        self.play(p_candidates.animate.scale(1.5))
        self.playw(p_candidates.animate.scale(1 / 1.5))
        self.wait(5)
        self.playw(FadeOut(p_candidates[1:]), Restore(p_candidates[0]))
        self.playw(Transform(p_candidates[0], p_answers[0]))

        ps_candidates = (
            VGroup(
                *[
                    Text(f"{a}, {b}", font="Consolas", font_size=16, color=RED)
                    for a, b in zip([2, 3, 5], [15, 10, 6])
                ]
            )
            .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.5)
            .next_to(p_answers[0], LEFT)
        )
        ps_sums = VGroup(
            *[
                Text(f"{num}", font="Consolas", font_size=16, color=RED).move_to(
                    ps_candidates[i]
                )
                for i, num in enumerate([17, 13, 11])
            ]
        )
        self.playw(
            LaggedStart(
                *[FadeIn(ps, target_position=p_answers[0]) for ps in ps_candidates],
                lag_ratio=0.1,
            ),
        )
        self.playw(
            LaggedStart(
                *[Transform(ps, _sum) for ps, _sum in zip(ps_candidates, ps_sums)],
                lag_ratio=0.1,
            )
        )
        for i in range(len(ps_candidates)):
            ps_candidates[i].save_state()
        self.playw(ps_candidates[0].animate.set_color(PURE_RED))
        self.playw(
            ps_candidates[1].animate.set_color(PURE_GREEN), Restore(ps_candidates[0])
        )
        self.playw(
            ps_candidates[2].animate.set_color(PURE_RED), Restore(ps_candidates[1])
        )
        self.playw(Restore(ps_candidates[2]))
        self.playw(ps_candidates[1].animate.set_opacity(0))
        self.play(ps_candidates.animate.scale(1.5))
        self.playw(ps_candidates.animate.scale(1 / 1.5))
        self.play(p_candidates[0].animate.scale(1.5))
        self.playw(p_candidates[0].animate.scale(1 / 1.5))

        self.playw(FadeOut(ps_candidates, p_candidates[0]))
        self.playw(FadeIn(p_candidates[1]))
        ps_candidates = (
            VGroup(
                *[
                    Text(f"{a}, {b}", font="Consolas", font_size=16, color=RED)
                    for a, b in zip([2, 3, 6], [21, 14, 7])
                ]
            )
            .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.5)
            .next_to(p_answers[1], LEFT)
        )
        ps_sums = VGroup(
            *[
                Text(f"{num}", font="Consolas", font_size=16, color=RED).move_to(
                    ps_candidates[i]
                )
                for i, num in enumerate([23, 17, 13])
            ]
        )
        for i in range(len(ps_candidates)):
            ps_candidates[i].save_state()
        self.playw(ps_candidates[0].animate.set_color(PURE_RED))
        self.playw(
            ps_candidates[1].animate.set_color(PURE_RED), Restore(ps_candidates[0])
        )
        self.playw(
            ps_candidates[2].animate.set_color(PURE_GREEN), Restore(ps_candidates[1])
        )
        self.playw(Restore(ps_candidates[2]))
        self.playw(ps_candidates[2].animate.set_opacity(0))
        self.play(ps_candidates.animate.scale(1.5))
        self.playw(ps_candidates.animate.scale(1 / 1.5))
        self.play(p_candidates[1].animate.scale(1.5))
        self.playw(p_candidates[1].animate.scale(1 / 1.5))

        self.playw(FadeIn(p_candidates[2]))
        self.playw(FadeIn(p_candidates[3]))
        self.playw(FadeIn(p_candidates[4]))
        self.playw(FadeIn(p_candidates[5]))
        self.playw(FadeIn(p_candidates[6]))
        self.playw(FadeOut(p_candidates[:2], p_candidates[3:]))
        self.playw(FadeOut(s, p_candidates[2], s_info, ps_candidates, candidates))
        self.clear()
        self.playw(Restore(self.camera.frame))

        c = ImageMobject("choisir.png").scale(0.2).shift(4 * RIGHT)
        s_info = MathTex("a", "+", "b", font_size=24).next_to(s, UP)
        p_info = MathTex("a", "\\times", "b", font_size=24).next_to(p, UP)
        c_info = Text("?", font="Consolas", font_size=32, color=PURE_RED).next_to(c, UP)
        self.playw(FadeIn(s, s_info, p, p_info))
        self.playw(FadeIn(c, c_info))
        self.playw(FadeOut(p, p_info))
        self.playw(FadeOut(s, s_info))
        self.playw(FadeOut(c, c_info))
        self.playw(FadeIn(c, c_info))
        self.wait(2)


def is_prime(num):
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
