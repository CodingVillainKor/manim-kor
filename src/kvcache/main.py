from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class autoregressive(Scene3D):
    def construct(self):
        model = (
            Rectangle(width=4.2, height=4.5, stroke_width=2, color=GREEN)
            .shift(UP * 0.5)
            .set_fill(BLACK, opacity=0.8)
            .set_z_index(1)
        )
        model_tag = (
            Text("GPT", font_size=24)
            .next_to(model, LEFT)
            .align_to(model, UP)
            .set_opacity(0.6)
        )
        tilt_degree = PI / 6
        VGroup(model, model_tag).rotate(tilt_degree, axis=UP)

        sentence_str = (
            "<SOS>  Some  call  me  nature,  others  call  me  mother  nature.  <EOS>"
        )
        sentence = Words(sentence_str, font_size=18).next_to(model, DOWN)
        sentence.save_state()
        for word in sentence.words:
            word.rotate(PI / 2)
        sentence.words[0].set_color(YELLOW)
        sentence.words[-1].set_color(YELLOW)
        sentence.words.arrange(RIGHT, aligned_edge=UP, buff=0.2).next_to(
            model, DOWN
        ).rotate(tilt_degree, axis=UP)
        self.playw(FadeIn(model, model_tag))

        output = (
            Tensor(len(sentence.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.75)
            .next_to(model, UP)
            .rotate(tilt_degree, axis=UP)
        )

        self.playw(FadeIn(sentence.words[0]))

        for i in range(len(sentence.words) - 1):
            model_in = sentence.words[: i + 1].copy()
            self.playw(model_in.animate.become(output[: i + 1].copy()))
            last = model_in[-1]
            future = sentence.words[i + 1]
            self.playw(
                last.animate.become(future.copy().move_to(last).align_to(last, DOWN))
            )
            model.set_z_index(-1)
            self.playw(
                Transform(
                    last,
                    future.copy(),
                    path_arc=-PI / 4,
                    replace_mobject_with_target_in_scene=True,
                ),
                FadeOut(model_in[:-1]),
            )
            model.set_z_index(1)


class attention(Scene3D):
    def construct(self):
        seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
        q_w = TexBox(
            "W",
            "_Q",
            tex_kwargs={"font_size": 36},
            box_kwargs={
                "stroke_width": 3,
                "stroke_color": GREY_B,
                "fill_opacity": 1,
                "fill_color": BLACK,
            },
        )
        k_w = TexBox(
            "W",
            "_K",
            tex_kwargs={"font_size": 36},
            box_kwargs={
                "stroke_width": 3,
                "stroke_color": GREY_B,
                "fill_opacity": 1,
                "fill_color": BLACK,
            },
        )
        v_w = TexBox(
            "W",
            "_V",
            tex_kwargs={"font_size": 36},
            box_kwargs={
                "stroke_width": 3,
                "stroke_color": GREY_B,
                "fill_opacity": 1,
                "fill_color": BLACK,
            },
        )
        VGroup(q_w.tex[-1], k_w.tex[-1], v_w.tex[-1]).set_color(YELLOW)
        q_w.set_z_index(1)
        k_w.set_z_index(1)
        v_w.set_z_index(1)
        VGroup(q_w, k_w, v_w).arrange(DOWN, buff=0.5)

        self.playwl(*[FadeIn(item) for item in [q_w, k_w, v_w]])
        seq.next_to(q_w, LEFT, buff=1)
        self.play(FadeIn(seq))
        q_seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1).next_to(
            q_w, RIGHT, buff=0.5
        )
        k_seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1).next_to(
            k_w, RIGHT, buff=0.5
        )
        v_seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1).next_to(
            v_w, RIGHT, buff=0.5
        )
        self.play(
            Transform(seq.copy(), q_seq, replace_mobject_with_target_in_scene=True)
        )
        self.play(seq.animate.next_to(k_w, LEFT, buff=1), run_time=0.5)
        self.play(
            Transform(seq.copy(), k_seq, replace_mobject_with_target_in_scene=True)
        )
        self.play(seq.animate.next_to(v_w, LEFT, buff=1), run_time=0.5)
        self.playw(
            Transform(seq.copy(), v_seq, replace_mobject_with_target_in_scene=True),
            FadeOut(seq),
        )

        ws = VGroup(q_w, k_w, v_w)
        ws.generate_target().shift(LEFT * 5 + UP * 2).set_opacity(0.4)

        tilt_angle = -PI / 3
        q_seq.generate_target().move_to(ORIGIN).shift(UP * 2)
        k_seq.generate_target().move_to(ORIGIN).rotate(tilt_angle, axis=UP).shift(LEFT)
        v_seq.generate_target().move_to(ORIGIN).rotate(tilt_angle, axis=UP).shift(
            DOWN + LEFT
        )
        self.playw(
            MoveToTarget(ws),
            MoveToTarget(q_seq),
            MoveToTarget(k_seq),
            MoveToTarget(v_seq),
        )
        k_softmax = (
            VGroup(
                *[
                    DecimalNumber(item, num_decimal_places=1)[1:]
                    for item in [0.7, 0.1, 0.2, 0.0, 0.0]
                ]
            )
            .arrange(RIGHT)
            .rotate(tilt_angle, axis=UP)
            .move_to(k_seq)
        )
        qs_ = VGroup(*[q_seq[0].copy() for _ in range(5)])
        qs_.generate_target()
        for i in range(len(qs_)):
            qs_.target[i].rotate(tilt_angle, axis=UP).move_to(k_seq[i])
        self.play(MoveToTarget(qs_))
        self.playw(FadeTransform(VGroup(k_seq, qs_), k_softmax))

        lines = VGroup(
            *[
                DashedLine(k_softmax[i].get_bottom(), v_seq[i].get_top(), color=GREY_C)
                for i in range(5)
            ]
        )
        self.cf.save_state()
        self.move_camera_horizontally(-tilt_angle / DEGREES, wait=0.1)
        self.playw(*[Create(line) for line in lines])
        self.play(FadeOut(lines))
        self.move_camera_horizontally(0)

        self.play(k_softmax.animate.move_to(v_seq))

        sigma = (
            MathTex("\\Sigma", font_size=84, color=YELLOW)
            .move_to(v_seq)
            .set_opacity(0.5)
        )
        out = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
        out[0].rotate(tilt_angle, axis=UP).move_to(v_seq[2])

        self.play(
            FadeOut(sigma, scale=1.5),
            FadeTransform(VGroup(v_seq, k_softmax), out[0]),
            rate_func=rush_from,
        )
        self.playw(out[0].animate.rotate(-tilt_angle, axis=UP))


class queryParallel(Scene3D):
    def construct(self):
        q_seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1).shift(UP * 2)
        k_seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
        v_seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)

        tilt_angle = -PI / 3
        k_seq.rotate(tilt_angle, axis=UP).shift(LEFT)
        v_seq.rotate(tilt_angle, axis=UP).shift(DOWN + LEFT)

        self.addw(q_seq, k_seq, v_seq)

        keys = (
            VGroup(*[k_seq.copy() for _ in range(4)])
            .arrange(RIGHT, buff=1)
            .shift(RIGHT * 1.2)
        )
        keys = VGroup(k_seq, *keys)
        values = (
            VGroup(*[v_seq.copy() for _ in range(4)])
            .arrange(RIGHT, buff=1)
            .shift(RIGHT * 1.2 + DOWN)
        )
        values = VGroup(v_seq, *values)

        self.play(
            keys[0].animate.shift(LEFT * 3),
            values[0].animate.shift(LEFT * 3),
            q_seq[0].animate.shift(LEFT * 3),
        )
        self.playw(
            *[FadeIn(item, target_position=k_seq) for item in keys[1:]],
            *[FadeIn(item, target_position=v_seq) for item in values[1:]],
            q_seq[1:]
            .animate.arrange(RIGHT, buff=1.8)
            .next_to(q_seq[0], RIGHT, buff=1.5),
            run_time=1.5,
        )

        srects = VGroup(
            *[
                DashedVMobject(
                    SurroundingRect(stroke_width=2, color=GREY_C).surround(
                        VGroup(q_seq[i], values[i]), buff_w=0.1 + i * 0.2, buff_h=0.5
                    ),
                    num_dashes=30,
                    dashed_ratio=0.7,
                )
                for i in range(5)
            ]
        )
        self.playw(FadeIn(srects))

        self.wait(5)

        idx = 2
        q, k, v = q_seq[idx], keys[idx], values[idx]
        self.playw(
            FadeOut(
                VGroup(
                    *[item for item in q_seq if item != q],
                    *[item for item in keys if item != k],
                    *[item for item in values if item != v],
                    *[item for item in srects if item != srects[idx]],
                )
            )
        )

        self.playw(*[FadeIn(item) for item in q_seq if item != q], run_time=0.5)
        self.playw(Circumscribe(q_seq))
        self.playw(*[FadeOut(item) for item in q_seq if item != q], run_time=0.5)

        softmax_tex = MathTex(
            r"\mathrm{exp}(<q_i, k_i>)",
            r"\over",
            r"\sum_{i=0}^n",
            r"\mathrm{exp}(<q_i, k_i>)",
            font_size=32,
        ).next_to(k, RIGHT, buff=0.5)

        weighted_sum_tex = MathTex(
            r"\sum_{i=0}^n",
            r"w_i \cdot",
            r"v_i",
            font_size=32,
        ).next_to(v, RIGHT, buff=0.5)
        self.playw(FadeIn(softmax_tex))
        self.playw(FadeIn(weighted_sum_tex))
        self.playw(softmax_tex[2].animate.set_color(RED_D))
        self.playw(weighted_sum_tex[0].animate.set_color(RED_D))

        self.playw(
            *[FadeIn(item) for item in q_seq[:2]],
            *[FadeIn(item) for item in keys[:2]],
            *[FadeIn(item) for item in values[:2]],
            *[FadeIn(item) for item in srects[:2]],
        )

        self.playwl(
            *[
                Indicate(VGroup(q_seq[i], keys[i], values[i], srects[i]), scale_factor=1.1)
                for i in range(3)
            ], lag_ratio=0.5
        )
