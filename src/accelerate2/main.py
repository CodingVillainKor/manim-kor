from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        text = Words("Gradient Accumulation", font_size=40).set_color_by_gradient(
            GREEN_A, GREEN_C
        )
        self.playwl(*[FadeIn(t) for t in text.words])

        self.playw(text.animate.set_color_by_gradient(RED_A, RED_C))

        self.wait()

        grads = (
            VGroup(
                *[
                    MathTex("\\nabla", "l", "_{" + str(i) + "}", font_size=36).next_to(
                        text, DOWN, buff=1
                    )
                    for i in range(4)
                ]
            )
            .arrange(RIGHT, buff=0.5)
            .next_to(text.words[0], DOWN, buff=0.75)
        )
        for g in grads:
            g[0].set_color(YELLOW_B)
        self.play(text.words[1].animate.set_opacity(0.4))
        self.playwl(*[FadeIn(g) for g in grads])

        self.play(
            text.words[0].animate.set_opacity(0.4), text.words[1].animate.set_opacity(1)
        )
        self.play(
            grads.animate.arrange(RIGHT, buff=0.15).next_to(
                text.words[1], DOWN, buff=0.75
            )
        )
        box = SurroundingRectangle(grads, buff=0.2, color=YELLOW_B, stroke_width=3)
        self.playw(FadeIn(box, scale=1.15))

        pre = VGroup(grads, text, box)
        minibatch = VGroup(
            *[
                Rectangle(
                    width=0.5,
                    height=0.5,
                    stroke_width=2,
                    fill_color=BLACK,
                    fill_opacity=1,
                    color=GREY_B,
                ).set_z_index(i + 1)
                for i in range(8)
            ]
        ).arrange(DR, buff=-0.4)
        self.playwl(
            AnimationGroup(pre.animate.shift(LEFT * 11), rate_func=rush_into),
            FadeIn(minibatch, shift=LEFT * 5, rate_func=rush_from),
            lag_ratio=0.7,
            wait=0.1,
        )
        bst = Words(
            "minibatch", font="Noto Sans KR", font_size=24, color=GREY_A
        ).next_to(minibatch, DOWN, buff=0.3)
        self.playw(FadeIn(bst))

        self.playw(VGroup(bst, minibatch).animate.shift(DOWN * 1.3))

        enterprise = RoundedRectangle(
            corner_radius=0.2, width=6, height=3.5, stroke_width=2, stroke_color=BLUE
        )
        individual = RoundedRectangle(
            corner_radius=0.2, width=3, height=2, stroke_width=2, stroke_color=ORANGE
        )
        VGroup(enterprise, individual).arrange(RIGHT, buff=1.5).shift(UP * 1.5)

        def get_gpu(scale=1):
            w = Text("GPU", font_size=24, font=MONO_FONT).set_z_index(1)
            gpu_box = SurroundingRectangle(
                w, buff=0.05, stroke_width=0, fill_color=BLACK, fill_opacity=0.7
            ).set_z_index(0.9)
            gpu = Rectangle(
                width=1.5 * scale, height=1 * scale, stroke_width=2
            ).set_z_index(0.8)
            VGroup(w, gpu_box).move_to(gpu.get_top())
            return VGroup(gpu, w, gpu_box)

        gpu_ent = VGroup(
            *[get_gpu(scale=1.2).move_to(enterprise.get_center()) for _ in range(4)]
        ).arrange_in_grid(2, 2, buff=0.2)
        gpu_ind = get_gpu().move_to(individual.get_center())
        self.playw(FadeIn(enterprise, individual, gpu_ent, gpu_ind))

        minibatch_ent = minibatch.copy()
        minibatch_ent = VGroup(
            minibatch_ent[:2],
            minibatch_ent[2:4],
            minibatch_ent[4:6],
            minibatch_ent[6:8],
        )
        minibatch_ent.generate_target()
        for i, m in enumerate(minibatch_ent.target):
            m.move_to(gpu_ent[i][0].get_center())
        minibatch_ind = minibatch.copy()
        minibatch_ind.generate_target()
        minibatch_ind.target.move_to(gpu_ind.get_center())

        self.play(MoveToTarget(minibatch_ent))
        self.playw(
            FadeOut(minibatch_ent),
            *[Indicate(gpu[0], scale_factor=0.9, color=BLUE) for gpu in gpu_ent],
            wait=0.5,
        )
        self.play(MoveToTarget(minibatch_ind))
        gi0 = gpu_ind[0]
        gi0.save_state()
        self.playw(
            minibatch_ind.animate.set_color(RED).set_fill(BLACK, opacity=1),
            gi0.animate.set_color(PURE_RED),
        )

        ga = (
            Words("Gradient Accumulation", font="Noto Sans KR", font_size=24)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(individual, DOWN, buff=0.5)
            .shift(RIGHT * 0.5)
        )
        self.playw(FadeIn(ga, shift=LEFT * 0.5))
        m_ind0 = minibatch_ind
        minibatch_ind = minibatch
        minibatch_ind = VGroup(
            minibatch_ind[:2],
            minibatch_ind[2:4],
            minibatch_ind[4:6],
            minibatch_ind[6:8],
        )
        self.play(FadeOut(m_ind0), Restore(gi0))
        for i, m in enumerate(minibatch_ind):
            m.generate_target()
            m.target.move_to(gpu_ind[0].get_center())
            self.play(MoveToTarget(m))
            self.play(
                FadeOut(m),
                Indicate(gpu_ind[0], scale_factor=0.9, color=ORANGE),
                *([FadeOut(bst)] if i == 3 else []),
                wait=0.3,
            )
        self.wait()

        ent_t = (
            Text("Enterprise", font="Noto Sans KR", font_size=24)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(enterprise, DOWN)
            .align_to(enterprise, LEFT)
        )
        ind_t = (
            Text("Individual", font="Noto Sans KR", font_size=24)
            .set_color_by_gradient(interpolate_color(ORANGE, WHITE, 0.5), ORANGE)
            .next_to(individual, DOWN)
            .align_to(individual, LEFT)
        )
        self.play(ga.animate.move_to(ORIGIN).shift(DOWN * 2))
        self.playw(FadeIn(ent_t, ind_t))

        self.playwl(
            FadeOut(ent_t, ind_t, enterprise, individual, gpu_ent, gpu_ind),
            ga.animate.move_to(ORIGIN),
            lag_ratio=0.4,
            wait=0,
        )
        self.playw(ga.animate.scale(1.2), run_time=3, rate_func=linear)


class whatisga(Scene2D):
    def construct(self):
        non_ga = Rectangle(
            width=5, height=3, stroke_width=2, stroke_color=GREY_A
        ).set_z_index(10)
        nga_m1 = Rectangle(
            width=4,
            height=1.1,
            stroke_width=2,
            stroke_color=GREY_B,
            fill_color=BLACK,
            fill_opacity=0.8,
        ).set_z_index(20)
        nga_m2 = Rectangle(
            width=4,
            height=1.1,
            stroke_width=2,
            stroke_color=GREY_B,
            fill_color=BLACK,
            fill_opacity=0.8,
        ).set_z_index(20)
        ms_nga = (
            VGroup(nga_m1, nga_m2).arrange(DOWN, buff=0.3).move_to(non_ga.get_center())
        )
        ga = Rectangle(
            width=5, height=3, stroke_width=2, stroke_color=BLUE_A
        ).set_z_index(1)
        ga_m1 = Rectangle(
            width=4,
            height=1.1,
            stroke_width=2,
            stroke_color=BLUE_B,
            fill_color=BLACK,
            fill_opacity=0.8,
        ).set_z_index(20)
        ga_m2 = Rectangle(
            width=4,
            height=1.1,
            stroke_width=2,
            stroke_color=BLUE_B,
            fill_color=BLACK,
            fill_opacity=0.8,
        ).set_z_index(20)
        ms_ga = VGroup(ga_m1, ga_m2).arrange(DOWN, buff=0.3).move_to(ga.get_center())
        nga = VGroup(non_ga, ms_nga)
        ga = VGroup(ga, ms_ga)
        VGroup(nga, ga).arrange(RIGHT, buff=1.5).shift(UP * 0.5)
        nga_t = (
            Text("Without GA", font="Noto Sans KR", font_size=18)
            .set_color_by_gradient(GREY_A, GREY_C)
            .next_to(nga, DOWN, buff=0.1)
            .align_to(nga, LEFT)
        )
        ga_t = (
            Text("With GA", font="Noto Sans KR", font_size=18)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(ga, DOWN, buff=0.1)
            .align_to(ga, LEFT)
        )
        self.addw(nga, ga, nga_t, ga_t)

        mb_nga = (
            VGroup(
                *[
                    Rectangle(
                        width=0.5,
                        height=0.5,
                        stroke_width=2,
                        fill_color=BLACK,
                        fill_opacity=1,
                        color=GREY_B,
                    ).set_z_index(i + 1)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.4)
            .next_to(nga, DOWN, buff=0.5)
        )
        mb_ga = (
            VGroup(
                *[
                    Rectangle(
                        width=0.5,
                        height=0.5,
                        stroke_width=2,
                        fill_color=BLACK,
                        fill_opacity=1,
                        color=BLUE_B,
                    ).set_z_index(i + 1)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.4)
            .next_to(ga, DOWN, buff=0.5)
        )
        mb_ga = VGroup(mb_ga[:2], mb_ga[2:4])
        nga_out = MathTex(
            *["\\nabla", "L"],  # 0-1
            "=",  # 2
            "\\nabla",  # 3
            "(",  # 4
            "{",  # 5
            *["l_1", "+", "l_2", "+", "l_3", "+", "l_4"],  # 6-12
            "\\over",  # 13
            "4",  # 14
            "}",  # 15
            ")",  # 16
            font_size=36,
            color=GREY_B,
        ).next_to(nga, UP, buff=0.5)
        self.play(FadeIn(mb_nga, shift=UP * 0.5))
        self.playw(
            *[
                Transform(
                    mb_nga[i], nga_out[j], replace_mobject_with_target_in_scene=True
                )
                for i, j in zip(range(4), [6, 8, 10, 12])
            ],
            FadeIn(
                nga_out[:6] + nga_out[13:] + nga_out[7] + nga_out[9] + nga_out[11],
                shift=UP * 2,
            ),
        )

        ga_out = MathTex(
            *["\\nabla", "L"],  # 0-1
            "=",  # 2
            "{",  # 3
            *["{", "\\nabla", "l_1", "\\over", "4", "}"],  # 4-9
            "+",  # 10
            *["{", "\\nabla", "l_2", "\\over", "4", "}"],  # 11-16
            "+",  # 17
            *["{", "\\nabla", "l_3", "\\over", "4", "}"],  # 18-23
            "+",  # 24
            *["{", "\\nabla", "l_4", "\\over", "4", "}"],  # 25-30
            "}",  # 33
            font_size=36,
            color=BLUE_B,
        ).next_to(ga, UP, buff=0.5)
        self.play(FadeIn(mb_ga, shift=UP * 0.5))
        self.playw(
            *[
                Transform(
                    mb_ga[i][j], ga_out[k], replace_mobject_with_target_in_scene=True
                )
                for i, j, k in zip(
                    [0, 0, 1, 1],
                    [0, 1, 0, 1],
                    [6, 13, 20, 27],
                )
            ],
            FadeIn(
                ga_out[:6] + ga_out[28:] + ga_out[7:13] + ga_out[14:20] + ga_out[21:27],
                shift=UP * 2,
            ),
        )

        self.playwl(
            FadeOut(ga_t, nga_t, ga, nga),
            VGroup(nga_out, ga_out).animate.arrange(DOWN, buff=1.5),
            lag_ratio=0.5,
            wait=0,
        )
        vs = Text("vs", font="Noto Sans KR", font_size=24, color=GREY_B)
        self.playw(FadeIn(vs, scale=1.5))
        ls_idx_nga = [6, 8, 10, 12]
        ls_idx_ga = [6, 13, 20, 27]
        nga_out.generate_target().set_opacity(0.3)
        ga_out.generate_target().set_opacity(0.3)
        for i in ls_idx_nga:
            nga_out.target[i].set_opacity(1)
        for i in ls_idx_ga:
            ga_out.target[i].set_opacity(1)
        self.play(
            MoveToTarget(nga_out), MoveToTarget(ga_out), vs.animate.set_opacity(0.5)
        )
        self.playw(nga_out[3:].animate.set_opacity(1))
        self.playw(ga_out[3:].animate.set_opacity(1))

        self.playw(Indicate(nga_out[6:15], color=YELLOW_C, scale_factor=1.1))
        self.playw(
            *[
                Indicate(ga_out[i - 1 : i + 1], color=YELLOW_C, scale_factor=1.1)
                for i in ls_idx_ga
            ]
        )


class compare(Scene2D):
    def construct(self):
        nga_model = (
            Rectangle(
                width=4,
                height=3,
                stroke_width=2,
                stroke_color=GREY_A,
                fill_color=BLACK,
                fill_opacity=0.6,
            )
            .set_z_index(10)
            .shift(LEFT * 4)
        )
        ga_model = (
            Rectangle(
                width=4,
                height=3,
                stroke_width=2,
                stroke_color=BLUE_A,
                fill_color=BLACK,
                fill_opacity=0.6,
            )
            .set_z_index(10)
            .shift(RIGHT * 4)
        )
        nga_m1 = Rectangle(
            width=3,
            height=1,
            stroke_width=2,
            stroke_color=GREY_B,
            fill_color=BLACK,
            fill_opacity=0.6,
        ).set_z_index(20)
        nga_m2 = Rectangle(
            width=3,
            height=1,
            stroke_width=2,
            stroke_color=GREY_B,
            fill_color=BLACK,
            fill_opacity=0.6,
        ).set_z_index(20)
        ga_m1 = Rectangle(
            width=3,
            height=1,
            stroke_width=2,
            stroke_color=BLUE_B,
            fill_color=BLACK,
            fill_opacity=0.6,
        ).set_z_index(20)
        ga_m2 = Rectangle(
            width=3,
            height=1,
            stroke_width=2,
            stroke_color=BLUE_B,
            fill_color=BLACK,
            fill_opacity=0.6,
        ).set_z_index(20)
        ms_nga = (
            VGroup(nga_m1, nga_m2)
            .arrange(DOWN, buff=0.3)
            .move_to(nga_model.get_center())
        )
        ms_ga = (
            VGroup(ga_m1, ga_m2).arrange(DOWN, buff=0.3).move_to(ga_model.get_center())
        )
        nga = VGroup(nga_model, ms_nga)
        ga = VGroup(ga_model, ms_ga)
        VGroup(nga, ga).arrange(RIGHT, buff=2.5).shift(UP * 0.5)
        nga_t = (
            Text("Without GA", font="Noto Sans KR", font_size=18)
            .set_color_by_gradient(GREY_A, GREY_C)
            .next_to(nga, LEFT, buff=0.1)
            .align_to(nga, DOWN)
        )
        ga_t = (
            Text("With GA", font="Noto Sans KR", font_size=18)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(ga, LEFT, buff=0.1)
            .align_to(ga, DOWN)
        )
        self.addw(nga, ga, nga_t, ga_t)

        mb_nga = (
            VGroup(
                *[
                    Rectangle(
                        width=0.5,
                        height=0.5,
                        stroke_width=2,
                        fill_color=BLACK,
                        fill_opacity=1,
                        color=GREY_B,
                    ).set_z_index(i + 1)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.4)
            .next_to(nga, DOWN, buff=0.5)
        )
        mb_ga = (
            VGroup(
                *[
                    Rectangle(
                        width=0.5,
                        height=0.5,
                        stroke_width=2,
                        fill_color=BLACK,
                        fill_opacity=1,
                        color=GREY_B,
                    ).set_z_index(i + 1)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.4)
            .next_to(ga, DOWN, buff=0.5)
        )
        mb_ga = VGroup(mb_ga[:2], mb_ga[2:4])
        self.play(FadeIn(mb_nga, shift=UP * 0.5))
        self.playw(mb_nga.animate.arrange(RIGHT).next_to(nga_model, DOWN, buff=0.5))

        nga_out = MathTex(
            *["\\nabla", "L"],  # 0-1
            "=",  # 2
            "\\nabla",  # 3
            "(",  # 4
            "{",  # 5
            *["l_1", "+", "l_2", "+", "l_3", "+", "l_4"],  # 6-12
            "\\over",  # 13
            "4",  # 14
            "}",  # 15
            ")",  # 16
            font_size=36,
            color=GREY_B,
        ).next_to(nga, UP, buff=0.5)
        self.playw(
            *[
                Transform(
                    mb_nga[i], nga_out[j], replace_mobject_with_target_in_scene=True
                )
                for i, j in zip(range(4), [6, 8, 10, 12])
            ],
            FadeIn(
                nga_out[7],
                nga_out[9],
                nga_out[11],
                nga_out[13:15],
                shift=UP * 2,
            ),
        )
        self.playw(FadeIn(nga_out[:6], nga_out[16]))

        self.play(
            VGroup(nga_t, nga_out, nga).animate.set_opacity(0.3),
            Indicate(ga_t, color=BLUE_C, scale_factor=1.1),
        )
        self.playw(FadeIn(mb_ga, shift=UP * 0.5))
        self.playw(
            mb_ga.animate.arrange(RIGHT, buff=0.5).next_to(ga_model, DOWN, buff=0.5)
        )

        ga_out = MathTex(
            *["\\nabla", "L"],  # 0-1
            "=",  # 2
            "{",  # 3
            *["{", "\\nabla", "l_1", "\\over", "4", "}"],  # 4-9
            "+",  # 10
            *["{", "\\nabla", "l_2", "\\over", "4", "}"],  # 11-16
            "+",  # 17
            *["{", "\\nabla", "l_3", "\\over", "4", "}"],  # 18-23
            "+",  # 24
            *["{", "\\nabla", "l_4", "\\over", "4", "}"],  # 25-30
            "}",  # 33
            font_size=36,
            color=BLUE_B,
        ).next_to(ga, UP, buff=0.5)
        self.playw(
            *[
                Transform(
                    mb_ga[i][j], ga_out[k], replace_mobject_with_target_in_scene=True
                )
                for i, j, k in zip(
                    [0, 0],
                    [0, 1],
                    [6, 13],
                )
            ],
            FadeIn(
                ga_out[7:9],
                ga_out[14:16],
                ga_out[10],
                shift=UP * 2,
            ),
        )
        self.playw(FadeIn(ga_out[5], ga_out[12]))

        self.playw(
            *[
                Transform(
                    mb_ga[1][j], ga_out[k], replace_mobject_with_target_in_scene=True
                )
                for j, k in zip([0, 1], [20, 27])
            ],
            FadeIn(
                ga_out[21:24],
                ga_out[28:30],
                ga_out[17],
                ga_out[24],
                shift=UP * 2,
            ),
        )
        self.playw(FadeIn(ga_out[19], ga_out[26]))
        self.playw(FadeIn(ga_out[:3]))

        self.playw(
            VGroup(ga, ga_t).animate.set_opacity(0.3), nga_out.animate.set_opacity(1)
        )
        self.play(self.cf.animate.shift(UP * 1.5))
        self.playw(Indicate(VGroup(nga_out, ga_out), color=YELLOW_C, scale_factor=1.1))


class batchnorm(Scene2D):
    def construct(self):
        model = (
            Rectangle(
                width=6,
                height=4,
                stroke_width=2,
                stroke_color=BLUE_A,
                stroke_opacity=0.7,
                fill_color=BLACK,
                fill_opacity=0.6,
            )
            .set_z_index(10)
            .shift(ORIGIN)
        )
        m1 = Rectangle(
            width=5,
            height=0.9,
            stroke_width=2,
            stroke_color=BLUE_B,
            stroke_opacity=0.7,
            fill_color=BLACK,
            fill_opacity=0.6,
        ).set_z_index(20)
        m2 = Rectangle(
            width=5,
            height=1.5,
            stroke_width=2,
            stroke_color=BLUE_B,
            stroke_opacity=0.7,
            fill_color=BLACK,
            fill_opacity=0.6,
        ).set_z_index(20)
        bn_t = (
            Text("BatchNorm", color=GREY_C, font="Noto Sans KR", font_size=18)
            .set_z_index(25)
            .next_to(m2, UP, buff=-0.25)
            .align_to(m2, RIGHT)
        )
        m2 = VGroup(m2, bn_t)
        ms = VGroup(m1, m2).arrange(DOWN, buff=0.5).move_to(model.get_center())
        model = VGroup(model, ms, bn_t).shift(UP * 0.5)
        mb = (
            VGroup(
                *[
                    Rectangle(
                        width=0.5,
                        height=0.5,
                        stroke_width=2,
                        fill_color=BLACK,
                        fill_opacity=1,
                        color=BLUE_B,
                    ).set_z_index(i + 1)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.4)
            .next_to(model, DOWN, buff=0.5)
            .shift(LEFT * 0.5)
            .set_z_index(30)
        )
        self.play(FadeIn(model), FadeIn(mb, shift=UP * 0.5))
        self.play(mb.animate.arrange(RIGHT).next_to(model, DOWN, buff=0.5))
        self.playw(mb.animate.move_to(m2).shift(LEFT * 0.5))

        box = DashedVMobject(
            SurroundingRectangle(mb, buff=0.1, stroke_width=2, stroke_color=YELLOW_B),
            num_dashes=50,
        ).set_z_index(30)
        mu, sig = MathTex("\\mu", font_size=28).set_color(YELLOW_B), MathTex(
            "\\sigma", font_size=28
        ).set_color(YELLOW_B)
        stat = (
            VGroup(mu, sig)
            .arrange(RIGHT, buff=0.1)
            .next_to(box, RIGHT, buff=0.05)
            .align_to(box, UP)
        ).set_z_index(30)
        self.playw(Create(box))
        self.playw(FadeIn(stat, shift=RIGHT * 0.3))

        self.play(FadeOut(box, stat, mb, shift=UP))

        mb_ga = (
            VGroup(
                *[
                    Rectangle(
                        width=0.5,
                        height=0.5,
                        stroke_width=2,
                        fill_color=BLACK,
                        fill_opacity=1,
                        color=BLUE_B,
                    ).set_z_index(i + 1)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.4)
            .next_to(model, DOWN, buff=0.5)
            .shift(LEFT * 0.5)
            .set_z_index(30)
        )
        self.play(FadeIn(mb_ga, shift=UP * 0.5))
        self.play(mb_ga.animate.arrange(RIGHT, buff=0.5).next_to(model, DOWN, buff=0.5))
        ga_in = mb_ga[:2]
        self.playw(ga_in.animate.move_to(m2).shift(LEFT * 0.5))
        box_ga = DashedVMobject(
            SurroundingRectangle(ga_in, buff=0.1, stroke_width=2, stroke_color=YELLOW_B),
            num_dashes=50,
        ).set_z_index(30)
        stat_ga = (
            VGroup(mu.copy(), sig.copy())
            .arrange(RIGHT, buff=0.1)
            .next_to(box_ga, RIGHT, buff=0.05)
            .align_to(box_ga, UP)
        ).set_z_index(30)
        self.playw(Create(box_ga), FadeIn(stat_ga, shift=RIGHT * 0.3))