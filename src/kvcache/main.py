from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


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
        k_seq.generate_target().move_to(ORIGIN).rotate(tilt_angle, axis=UP).shift(
            RIGHT * 0.4
        )
        v_seq.generate_target().move_to(ORIGIN).rotate(tilt_angle, axis=UP).shift(
            DOWN + RIGHT * 0.4
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
                    for item in [0.1, 0.1, 0.2, 0.6, 0.0]
                ]
            )
            .arrange(RIGHT)
            .rotate(tilt_angle, axis=UP)
            .move_to(k_seq)
        )
        k_softmax[-1].set_opacity(0.2)
        qs_ = VGroup(*[q_seq[3].copy() for _ in range(5)])
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
                Indicate(
                    VGroup(q_seq[i], keys[i], values[i], srects[i]), scale_factor=1.1
                )
                for i in range(3)
            ],
            lag_ratio=0.5,
        )


class woKVcache(Scene3D):
    def construct(self):
        llm = TextBox(
            "LLM",
            text_kwargs={"font_size": 32},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.7,
                "stroke_width": 3,
                "color": GREY_B,
            },
        ).shift(UP * 1.3)
        llm.set_z_index(1)
        llm.box.stretch_to_fit_height(4).stretch_to_fit_width(6)
        llm.text.next_to(llm.box, LEFT, buff=0.1).align_to(llm.box, UP)
        self.addw(llm)
        sentence_str = "which is better, ChatGPT or Claude? <Response>"
        sentence = Words(sentence_str, font_size=24).next_to(llm, DOWN)
        sentence.save_state()
        for word in sentence.words:
            word.rotate(PI / 2)
        sentence.words[-1].set_color(YELLOW)
        sentence.words.arrange(RIGHT, aligned_edge=UP, buff=0.4).next_to(llm, DOWN)
        self.playw(FadeIn(sentence))

        model_in = (
            Tensor(len(sentence.words), shape="square", arrange=RIGHT, buff=0.25)
            .align_to(sentence, UP)
            .align_to(sentence, LEFT)
        )
        self.play(Transform(sentence.words, model_in))
        self.play(sentence.words.animate.shift(UP))
        llm.text.add_updater(
            lambda m: m.next_to(llm.box, LEFT, buff=0.1).align_to(llm.box, UP)
        )
        self.playw(
            llm.box.animate.scale(3.5).align_to(llm.box).shift(UP * 0.5).set_opacity(0)
        )
        llm.text.suspend_updating()
        self.remove(llm)

        lbrace = Brace(sentence.words, DOWN, buff=0.25)
        ltext = Text("L").next_to(lbrace, DOWN, buff=0.1)
        self.playw(FadeIn(lbrace, ltext))
        self.playw(FadeOut(lbrace, ltext))

        q_w = TexBox(
            "W",
            "_Q",
            tex_kwargs={"font_size": 48},
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
            tex_kwargs={"font_size": 48},
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
            tex_kwargs={"font_size": 48},
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
        VGroup(q_w, k_w, v_w).arrange(UP, buff=0.5)
        self.play(
            sentence.words.animate.arrange(RIGHT, buff=0.1).next_to(q_w, LEFT),
            run_time=0.5,
        )
        self.play(FadeIn(q_w, k_w, v_w))
        q_seq = Tensor(
            len(sentence.words), shape="square", arrange=RIGHT, buff=0.25
        ).next_to(q_w, RIGHT, buff=0.5)
        k_seq = Tensor(
            len(sentence.words), shape="square", arrange=RIGHT, buff=0.25
        ).next_to(k_w, RIGHT, buff=0.5)
        v_seq = Tensor(
            len(sentence.words), shape="square", arrange=RIGHT, buff=0.25
        ).next_to(v_w, RIGHT, buff=0.5)
        self.play(
            Transform(
                sentence.words.copy(), q_seq, replace_mobject_with_target_in_scene=True
            )
        )
        self.play(sentence.words.animate.next_to(k_w, LEFT), run_time=0.5)
        self.play(
            Transform(
                sentence.words.copy(), k_seq, replace_mobject_with_target_in_scene=True
            )
        )
        self.play(sentence.words.animate.next_to(v_w, LEFT), run_time=0.5)
        self.play(
            Transform(
                sentence.words.copy(), v_seq, replace_mobject_with_target_in_scene=True
            ),
            FadeOut(sentence.words),
        )
        self.playwl(
            FadeOut(q_w, k_w, v_w, shift=LEFT),
            VGroup(q_seq, k_seq, v_seq).animate.move_to(ORIGIN),
            lag_ratio=0.5,
        )
        tilt_angle = -PI / 2.9
        adaptive_angle = lambda i: tilt_angle * (
            1 + 0.4 * i / (len(sentence.words) - 2)
        )
        keys = VGroup(*[k_seq.copy() for i in range(len(sentence.words) - 1)]).arrange(
            RIGHT, buff=-2.4
        )
        keys = VGroup(k_seq, *keys)
        keys[0].set_z_index(1)
        for i, k in enumerate(keys[1:], 1):
            k.rotate(adaptive_angle(i - 1), axis=UP)

        values = VGroup(
            *[v_seq.copy() for _ in range(len(sentence.words) - 1)]
        ).arrange(RIGHT, buff=-2.4)
        values = VGroup(v_seq, *values)
        for i, v in enumerate(values[1:], 1):
            v.rotate(adaptive_angle(i - 1), axis=UP)
        self.play(
            keys[0].animate.rotate(tilt_angle, axis=UP).shift(LEFT * 5.7),
            values[0].animate.rotate(tilt_angle, axis=UP).shift(LEFT * 5.7),
        )
        keys[1:].next_to(keys[0], RIGHT, buff=-0.15)
        values[1:].next_to(values[0], RIGHT, buff=-0.15)
        self.playw(
            *[FadeIn(item, target_position=k_seq) for item in keys[1:]],
            *[FadeIn(item, target_position=v_seq) for item in values[1:]],
            q_seq.animate.arrange(RIGHT, buff=1.5).align_to(q_seq, DOWN),
        )

        keys.set_z_index(1)

        qs = VGroup(
            *[
                q_seq[i].copy()
                for i in range(len(sentence.words))
                for _ in range(len(keys[i]))
            ]
        )
        qs.generate_target()
        for i in range(len(sentence.words)):
            for j in range(len(keys[i])):
                qs.target[i * len(keys[i]) + j].rotate(
                    adaptive_angle(i), axis=UP
                ).move_to(keys[i][j])
        self.play(MoveToTarget(qs))

        softmaxes = VGroup()
        # softmax weight be Dot(), not DecimalNumber
        for i in range(len(sentence.words)):
            softmax_i = VGroup()
            for j in range(len(keys[i])):
                w = (
                    Dot(radius=0.1, color=random_bright_color())
                    .move_to(keys[i][j])
                    .scale(0.5)
                )
                w.set_opacity(1 if j <= i else 0.1)
                softmax_i.add(w)
            softmaxes.add(softmax_i)
        self.playw(FadeTransform(VGroup(keys, qs), softmaxes))
        values.save_state()
        q_seq.save_state()
        total_brace = Brace(
            VGroup(softmaxes[0][3], softmaxes[-1][3]), UP, color=RED, buff=0.2
        )
        total_text = Text("L", color=RED).next_to(total_brace, UP, buff=0.1)
        each_brace = VGroup(
            *[
                Brace(softmaxes[i], DOWN, color=GREEN, buff=0.1)
                for i in range(len(softmaxes))
            ]
        )
        each_text = VGroup(
            *[
                Text("L", color=GREEN, font_size=32).next_to(
                    each_brace[i], DOWN, buff=0.1
                )
                for i in range(len(each_brace))
            ]
        )
        self.playw(
            values.animate.shift(UP),
            q_seq.animate.shift(DOWN),
            FadeIn(total_brace, total_text),
            *[FadeIn(each_text[i]) for i in range(len(each_brace))],
        )

        self.playwl(
            FadeOut(total_brace, total_text, each_text),
            Restore(values),
            Restore(q_seq),
            lag_ratio=0.4,
        )
        softmaxes.set_z_index(1)
        self.play(
            *[softmaxes[i].animate.move_to(values[i]) for i in range(len(values))]
        )
        out = Tensor(len(sentence.words), shape="square", arrange=RIGHT)
        for i, o in enumerate(out):
            o.rotate(adaptive_angle(i), axis=UP).move_to(values[i])
        sigmas = VGroup(
            *[
                MathTex("\\Sigma", font_size=64, color=YELLOW)
                .move_to(values[i])
                .set_opacity(0.7)
                for i in range(len(values))
            ]
        )
        self.play(
            *[
                FadeTransform(VGroup(values[i], softmaxes[i]), out[i])
                for i in range(len(out))
            ],
            *[FadeOut(sigmas[i], scale=2) for i in range(len(sigmas))],
            rate_func=rush_from,
        )
        self.playw(
            *[
                out[i]
                .animate.rotate(-adaptive_angle(i), axis=UP)
                .align_to(q_seq[i], LEFT)
                for i in range(len(out))
            ]
        )

        attn = TextBox(
            "Self-Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.7,
                "stroke_width": 3,
                "color": GREY_B,
            },
        )
        attn.set_z_index(1)
        attn.box.stretch_to_fit_height(5).stretch_to_fit_width(14)
        attn.text.next_to(attn.box, LEFT, buff=0.1).align_to(attn.box, UP)
        self.playwl(self.cf.animate.shift(OUT * 7), FadeIn(attn), lag_ratio=0.7, wait=0)
        self.playw(out.animate.next_to(attn.box, UP, buff=1))

        self.playw(FadeOut(attn, q_seq))

        llm = TextBox(
            "LLM",
            text_kwargs={"font_size": 32},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.7,
                "stroke_width": 3,
                "color": GREY_B,
            },
        ).shift(UP * 3)
        llm.set_z_index(1)
        llm.box.stretch_to_fit_height(9).stretch_to_fit_width(13)
        llm.text.next_to(llm.box, LEFT, buff=0.1).align_to(llm.box, UP)
        self.play(FadeIn(llm))
        llm_ = TextBox(
            "LLM",
            text_kwargs={"font_size": 32},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.7,
                "stroke_width": 3,
                "color": GREY_B,
            },
        )
        llm_.set_z_index(1)
        llm_.box.stretch_to_fit_height(6).stretch_to_fit_width(13)
        llm_.text.next_to(llm_.box, LEFT, buff=0.1).align_to(llm_.box, UP)
        self.playw(llm.animate.become(llm_), out.animate.shift(DOWN * 4))
        self.playw(out.animate.next_to(llm.box, UP, buff=1))

        self.wait(3)

        response_str = "I prefer Claude because its writing is more natural."
        response = Words(response_str, font_size=32).next_to(llm, DOWN)
        response.save_state()
        # for word in response.words:
        #     word.rotate(PI / 2)
        response.words[0].move_to(out[-1]).align_to(out[-1], DOWN)

        self.playw(
            Transform(
                out[-1], response.words[0], replace_mobject_with_target_in_scene=True
            ),
            FadeOut(out[:-1]),
        )


class autoregressive(Scene3D):
    def construct(self):
        model = (
            Rectangle(width=8.2, height=4.5, stroke_width=2, color=GREEN)
            .shift(UP * 0.5)
            .set_fill(BLACK, opacity=0.8)
            .set_z_index(1)
        )
        model_tag = (
            Text("LLM", font_size=24)
            .next_to(model, LEFT)
            .align_to(model, UP)
            .set_opacity(0.6)
        )
        tilt_degree = PI / 6
        VGroup(model, model_tag).rotate(tilt_degree, axis=UP)

        sentence_str = "which is better, ChatGPT or Claude? <Response> I prefer Claude because its writing is more natural."
        sentence = Words(sentence_str, font_size=18).next_to(model, DOWN)
        sentence.save_state()
        for word in sentence.words:
            word.rotate(PI / 2)
        sentence.words[6].set_color(YELLOW)
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
            self.play(model_in.animate.become(output[: i + 1].copy()))
            last = model_in[-1]
            future = sentence.words[i + 1]
            self.play(
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


class kvCache(Scene3D):
    def construct(self):
        model = (
            Rectangle(width=8.2, height=3.5, stroke_width=2, color=GREEN)
            .shift(UP)
            .set_fill(BLACK, opacity=0.8)
            .set_z_index(1)
        )
        model_tag = (
            Text("LLM", font_size=24)
            .next_to(model, LEFT)
            .align_to(model, UP)
            .set_opacity(0.6)
        )
        tilt_degree = PI / 6
        VGroup(model, model_tag).rotate(tilt_degree, axis=UP)
        sentence_str = "What is piui ? <Response>"
        sentence = Words(sentence_str, font_size=20)
        sentence.save_state()
        for word in sentence.words:
            word.rotate(PI / 2)
        sentence.words[-1].set_color(YELLOW)
        sentence.words.arrange(RIGHT, aligned_edge=UP, buff=0.4).next_to(
            model, DOWN
        ).shift(LEFT * 2.2).rotate(tilt_degree, axis=UP)
        self.addw(model, model_tag, sentence)
        model_in = Tensor(
            len(sentence.words), shape="square", arrange=RIGHT, buff=0.25
        ).rotate(tilt_degree, axis=UP)
        for i, t in enumerate(model_in):
            t.move_to(sentence.words[i]).align_to(sentence.words[i], UP)
        self.play(Transform(sentence.words, model_in))
        self.play(sentence.words.animate.shift(UP))
        self.playw(
            sentence.words.animate.rotate(-tilt_degree, axis=UP),
            model.animate.set_opacity(0).rotate(-tilt_degree, axis=UP).scale(3),
            model_tag.animate.shift(LEFT * 8 + OUT * 4),
        )
        q_w = TexBox(
            "W",
            "_Q",
            tex_kwargs={"font_size": 48},
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
            tex_kwargs={"font_size": 48},
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
            tex_kwargs={"font_size": 48},
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
        VGroup(q_w, k_w, v_w).arrange(UP, buff=0.5).shift(LEFT * 2)
        # seq = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
        # seq.next_to(q_w, LEFT, buff=1)
        self.playwl(
            sentence.words.animate.next_to(q_w, LEFT, buff=1),
            FadeIn(q_w, k_w, v_w),
            lag_ratio=0.5,
        )
        seq = sentence.words

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
        kvcache = TextBox(
            "KV Cache",
            text_kwargs={"font_size": 20, "color": GREEN},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.5,
                "stroke_width": 3,
                "color": GREY_C,
            },
        )
        kvcache.set_z_index(1)
        kvcache.box.stretch_to_fit_height(3).stretch_to_fit_width(4).shift(
            RIGHT * 4.5 + DOWN
        )
        kvcache.text.next_to(kvcache.box, UP, buff=0.1).align_to(kvcache.box, LEFT)
        ws = VGroup(q_w, k_w, v_w)
        ws.generate_target().shift(LEFT * 7 + UP * 2).set_opacity(0.4)
        self.playw(FadeIn(kvcache, shift=LEFT * 3), run_time=1)
        k_cached = k_seq.copy()
        v_cached = v_seq.copy()
        self.playw(
            VGroup(k_cached, v_cached)
            .animate.arrange(UP, buff=0.7)
            .move_to(kvcache.box)
        )
        q_seq.generate_target().move_to(ORIGIN).shift(DOWN)
        k_seq.generate_target().move_to(ORIGIN).rotate(-PI / 3, axis=UP).shift(
            UP + RIGHT * 0.4
        )
        v_seq.generate_target().move_to(ORIGIN).rotate(-PI / 3, axis=UP).shift(
            UP * 2 + RIGHT * 0.4
        )
        cached = VGroup(kvcache, k_cached, v_cached)
        adaptive_angle = lambda i: -PI / 3.5 * (1 + 0.3 * i / (len(sentence.words) - 2))
        keys = VGroup(k_seq, *[k_seq.copy() for _ in range(len(sentence.words) - 1)])
        keys.generate_target()
        keys.target.arrange(RIGHT, buff=-0.15).shift(UP)
        for i, k in enumerate(keys.target):
            k.rotate(adaptive_angle(i), axis=UP)
        values = VGroup(v_seq, *[v_seq.copy() for _ in range(len(sentence.words) - 1)])
        values.generate_target()
        values.target.arrange(RIGHT, buff=-0.15).shift(UP * 2)
        for i, v in enumerate(values.target):
            v.rotate(adaptive_angle(i), axis=UP)
        self.playw(
            MoveToTarget(ws),
            MoveToTarget(keys),
            MoveToTarget(values),
            q_seq.animate.arrange(RIGHT, buff=2).align_to(q_seq, DOWN),
            cached.animate.rotate(-PI / 2.1, axis=UP).shift(RIGHT * 1.6),
        )

        qs = VGroup(
            *[
                q_seq[i].copy()
                for i in range(len(sentence.words))
                for _ in range(len(keys[i]))
            ]
        )
        qs.generate_target()
        for i in range(len(sentence.words)):
            for j in range(len(keys[i])):
                qs.target[i * len(keys[i]) + j].rotate(
                    adaptive_angle(i), axis=UP
                ).move_to(keys[i][j])
        keys.set_z_index(1)
        self.play(MoveToTarget(qs))
        softmaxes = VGroup()
        # softmax weight be Dot(), not DecimalNumber
        for i in range(len(sentence.words)):
            softmax_i = VGroup()
            for j in range(len(keys[i])):
                w = (
                    Dot(radius=0.1, color=random_bright_color())
                    .move_to(keys[i][j])
                    .scale(0.5)
                )
                w.set_opacity(1 if j <= i else 0.1)
                softmax_i.add(w)
            softmaxes.add(softmax_i)
        self.playw(FadeTransform(VGroup(keys, qs), softmaxes))
        softmaxes.set_z_index(1)
        self.play(
            *[softmaxes[i].animate.move_to(values[i]) for i in range(len(values))]
        )
        out = Tensor(len(sentence.words), shape="square", arrange=RIGHT)
        for i, o in enumerate(out):
            o.rotate(adaptive_angle(i), axis=UP).move_to(values[i])
        sigmas = VGroup(
            *[
                MathTex("\\Sigma", font_size=64, color=YELLOW)
                .move_to(values[i])
                .set_opacity(0.7)
                for i in range(len(values))
            ]
        )
        self.play(
            *[
                FadeTransform(VGroup(values[i], softmaxes[i]), out[i])
                for i in range(len(out))
            ],
            *[FadeOut(sigmas[i], scale=2) for i in range(len(sigmas))],
            rate_func=rush_from,
        )
        self.playw(
            *[
                out[i]
                .animate.rotate(-adaptive_angle(i), axis=UP)
                .align_to(q_seq[i], LEFT)
                for i in range(len(out))
            ]
        )
        sa = TextBox(
            "Self-Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.5,
                "stroke_width": 3,
                "color": GREY_B,
            },
        ).shift(UP)
        sa.set_z_index(2)
        sa.box.stretch_to_fit_height(10).stretch_to_fit_width(17).align_to(
            kvcache, RIGHT
        ).shift(RIGHT)
        sa.text.next_to(sa.box, LEFT, buff=0.1).align_to(sa.box, UP)
        self.play(FadeIn(sa))
        self.cf.save_state()
        self.play(
            self.cf.animate.shift(OUT * 12 + LEFT * 2),
            sa.box.animate.set_fill(opacity=0.3),
        )
        llm = TextBox(
            "LLM",
            text_kwargs={"font_size": 32},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.7,
                "stroke_width": 3,
                "color": GREY_B,
            },
        ).shift(UP * 2)
        self.remove(model_tag)
        llm.set_z_index(3)
        llm.box.stretch_to_fit_height(12).stretch_to_fit_width(20).move_to(sa)
        llm.text.next_to(llm.box, LEFT, buff=0.1).align_to(llm.box, UP)
        self.playw(
            FadeIn(llm),
            self.cf.animate.shift(OUT * 12),
            out.animate.next_to(llm.box, UP, buff=0.75).align_to(out, RIGHT),
            FadeOut(q_seq),
        )
        self.playw(FadeOut(out[:-1]), Indicate(out[-1]))
        self.playw(cached.animate.shift(RIGHT * 4).rotate(PI / 2.1, axis=UP))

        self.cf.save_state()
        self.playw(self.cf.animate.move_to(cached))

        self.playwl(*[Indicate(item) for item in [k_cached, v_cached]], lag_ratio=0.5)

        self.playw(Restore(self.cf))
        next_sample = (
            out[-1].copy().next_to(llm, DOWN, buff=0.75).align_to(out[-1], LEFT)
        )
        out[-1].set_z_index(5)
        self.playw(
            Transform(
                out[-1],
                next_sample,
                path_arc=-PI / 2.5,
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(next_sample.animate.shift(UP * 3), FadeOut(llm))
        self.play(FadeOut(sa))
        self.playw(
            self.cf.animate.shift(IN * 14 + LEFT * 2),
            cached.animate.shift(LEFT * 7 + UP * 4),
            next_sample.animate.shift(LEFT * 12.5 + UP),
            VGroup(q_w, k_w, v_w).animate.set_opacity(1).shift(RIGHT * 3 + DOWN * 2),
        )
        ns = next_sample
        qs = ns.copy().set_fill(random_color(), opacity=1).next_to(q_w, RIGHT, buff=1)
        ks = ns.copy().set_fill(random_color(), opacity=1).next_to(k_w, RIGHT, buff=1)
        vs = ns.copy().set_fill(random_color(), opacity=1).next_to(v_w, RIGHT, buff=1)
        self.play(ns.animate.next_to(q_w, LEFT, buff=1), run_time=0.5)
        self.play(Transform(ns.copy(), qs, replace_mobject_with_target_in_scene=True))
        self.play(ns.animate.next_to(k_w, LEFT, buff=1), run_time=0.5)
        self.play(Transform(ns.copy(), ks, replace_mobject_with_target_in_scene=True))
        self.play(ns.animate.next_to(v_w, LEFT, buff=1), run_time=0.5)
        self.playw(Transform(ns, vs, replace_mobject_with_target_in_scene=True))

        self.playw(ws.animate.set_opacity(0.4).shift(LEFT * 7 + UP * 2), run_time=0.5)
        kv_cached = VGroup(k_cached, v_cached).copy()
        self.add(kv_cached)
        self.play(
            VGroup(k_cached, v_cached)
            .animate.next_to(VGroup(ks, vs), LEFT, buff=0.1)
            .align_to(v_cached, UP),
            rate_func=rush_into,
        )
        self.playw(
            k_cached.animate.next_to(ks, LEFT, buff=0.1),
            v_cached.animate.next_to(vs, LEFT, buff=0.1),
            rate_func=rush_from,
            run_time=0.7,
        )
        ksc = ks.copy()
        vsc = vs.copy()
        self.playw(
            ksc.animate.next_to(kv_cached[0], RIGHT, buff=0.1),
            vsc.animate.next_to(kv_cached[1], RIGHT, buff=0.1),
        )

        keys = VGroup(*k_cached, ks)
        values = VGroup(*v_cached, vs)
        self.play(
            keys.animate.rotate(-PI / 3, axis=UP).shift(RIGHT * 0.7),
            values.animate.rotate(-PI / 3, axis=UP).shift(RIGHT * 0.7),
        )

        qs_ = VGroup(*[qs.copy() for _ in range(len(keys))])
        qs_.generate_target()
        for i in range(len(keys)):
            qs_.target[i].rotate(-PI / 3, axis=UP).move_to(keys[i])
        self.play(MoveToTarget(qs_))
        softmaxes = VGroup()
        # softmax weight be Dot(), not DecimalNumber
        for i in range(len(keys)):
            w = Dot(radius=0.1, color=random_bright_color()).move_to(keys[i]).scale(0.5)
            softmaxes.add(w)
        self.playw(FadeTransform(VGroup(keys, qs_), softmaxes))
        softmaxes.set_z_index(1)
        self.play(softmaxes.animate.move_to(values))
        out = (
            Tensor(1, shape="square", arrange=RIGHT)
            .rotate(-PI / 3, axis=UP)
            .move_to(values[-1])
        )
        sigma = (
            MathTex("\\Sigma", font_size=64, color=YELLOW)
            .move_to(values)
            .set_opacity(0.7)
        )
        self.play(
            FadeTransform(VGroup(values, softmaxes), out),
            FadeOut(sigma, scale=2),
            rate_func=rush_from,
        )
        self.playw(out.animate.rotate(PI / 3, axis=UP))
        self.wait()
        sa.shift(LEFT * 3).scale(1.2)
        llm.shift(LEFT * 3).scale(1.2)
        self.playwl(FadeIn(sa), self.cf.animate.shift(OUT * 10), lag_ratio=0.7, wait=0)
        self.playwl(FadeIn(llm), self.cf.animate.shift(OUT * 12), lag_ratio=0.7, wait=0)
        self.playw(out.animate.next_to(llm.box, UP, buff=0.75).align_to(out, RIGHT))


class forTN(Scene3D):
    def construct(self):
        kvcache = TextBox(
            "KV Cache",
            text_kwargs={"font_size": 20, "color": GREEN},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.5,
                "stroke_width": 3,
                "color": GREY_C,
            },
        )
        kvcache.set_z_index(1)
        kvcache.box.stretch_to_fit_height(3).stretch_to_fit_width(4).shift(
            LEFT * 3.5 + UP * 1.5
        )
        kvcache.text.next_to(kvcache.box, UP, buff=0.1).align_to(kvcache.box, LEFT)

        adaptive_angle = lambda i: -PI / 2.3 * (0.85 + 0.2 * i / 4)
        key = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
        keys = (
            VGroup(*[key.copy().rotate(adaptive_angle(i), axis=UP) for i in range(4)])
            .arrange(RIGHT, buff=0.8)
            .shift(RIGHT * 2)
        )

        value = Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
        values = (
            VGroup(*[value.copy().rotate(adaptive_angle(i), axis=UP) for i in range(4)])
            .arrange(RIGHT, buff=0.8)
            .shift(RIGHT * 2 + UP)
        )

        q_seq = Tensor(4, shape="square", arrange=RIGHT, buff=0.1)
        for i, q in enumerate(q_seq):
            q.next_to(keys[i], DOWN, buff=1.5)

        self.addw(kvcache, keys, values, q_seq)
