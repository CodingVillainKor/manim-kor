from glm import pos
from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        pe_sin = RaeTex(
            r"PE_{(pos,\,i)}",
            r"=",
            r"\sin",
            r"\!\left(",
            r"\frac{pos}{i}",
            r"\right)",
            font_size=60,
        )
        pe_sin[2:].set_color(BLUE)

        self.addw(pe_sin, wait=1.5)
        ol = self.overlay
        pe_sin[2].set_z_index(ol.get_z_index() + 1)
        self.play(FadeIn(ol), run_time=0.5)
        self.playw(RWiggle(pe_sin[2]), run_time=3)


class whype(Scene2D):
    def construct(self):
        def tb(text, font_size=24):
            t = Text(text, font_size=font_size, font="Noto Sans KR", color=GREY_B)
            b = Square(
                side_length=0.6,
                color=GREY_B,
                fill_color=BLACK,
                fill_opacity=0.75,
                stroke_width=3,
            )
            return VGroup(b, t).arrange(IN)

        # === 1. Permutation: ABCD 스왑 ===
        a, b, c, d = [tb(ch, 24) for ch in "ABCD"]
        boxes = VGroup(a, b, c, d).arrange(RIGHT, buff=1)
        self.playw(FadeIn(boxes))

        a_pos, b_pos = a.get_center().copy(), b.get_center().copy()
        c_pos, d_pos = c.get_center().copy(), d.get_center().copy()
        self.playw(
            a.animate(path_arc=PI / 1.3).move_to(b_pos),
            b.animate(path_arc=PI / 1.3).move_to(a_pos),
            c.animate(path_arc=PI / 1.3).move_to(d_pos),
            d.animate(path_arc=PI / 1.3).move_to(c_pos),
        )

        # === 3. Attention: 두 입력 → 같은 출력 ===
        abcdc = boxes.copy()
        abcdc.generate_target().arrange(RIGHT, buff=0.5).shift(UP)
        abcd = VGroup(*[boxes[i] for i in [1, 0, 3, 2]])
        self.playw(
            MoveToTarget(abcdc),
            abcd.animate.arrange(RIGHT, buff=0.5).move_to(abcd).shift(DOWN),
        )

        attn1l = Text("Attention(", font_size=28, font=MONO_FONT, color=GREEN).next_to(
            abcdc, LEFT, buff=0.3
        )
        attn1r = Text(")", font_size=28, font=MONO_FONT, color=GREEN).next_to(
            abcdc, RIGHT, buff=0.3
        )
        attn2l = Text("Attention(", font_size=28, font=MONO_FONT, color=GREEN).next_to(
            abcd, LEFT, buff=0.3
        )
        attn2r = Text(")", font_size=28, font=MONO_FONT, color=GREEN).next_to(
            abcd, RIGHT, buff=0.3
        )
        self.playw(FadeIn(attn1l, attn1r, attn2l, attn2r))

        self.playw(Circumscribe(abcdc, fade_in=True, fade_out=True, color=YELLOW))
        self.playw(Circumscribe(abcd, fade_in=True, fade_out=True, color=YELLOW))

        # === 4. QK 내적: bipartite graph로 같은 쌍 시각화 ===
        self.play(FadeOut(attn1l, attn1r, attn2l, attn2r, abcdc, abcd))

        def texb(text):
            t = MathTex(text, font_size=40, color=GREY_A)
            b = Square(
                side_length=0.8,
                color=GREY_B,
                fill_color=BLACK,
                fill_opacity=0.75,
                stroke_width=3,
            )
            return VGroup(b, t)

        q_boxes = VGroup(*[texb(f"q_{c}") for c in "ABC"])
        k_boxes = VGroup(*[texb(f"k_{c}") for c in "ABC"])
        q_boxes.arrange(DOWN, buff=0.5).shift(LEFT * 2.5)
        k_boxes.arrange(DOWN, buff=0.5).shift(RIGHT * 2.5)

        q_label = Text("Q", font_size=28, color=BLUE).next_to(q_boxes, UP)
        k_label = Text("K", font_size=28, color=RED).next_to(k_boxes, UP)

        self.playw(FadeIn(q_boxes, k_boxes, q_label, k_label))

        # 모든 Q-K 쌍 연결 (9개 내적)
        pair_lines = VGroup(
            *[
                Line(q.get_right(), k.get_left(), stroke_width=1.5, color=GRAY_B)
                for q in q_boxes
                for k in k_boxes
            ]
        )
        self.playw(*[Create(line) for line in pair_lines])

        # Q 쪽 permute: qA ↔ qB 스왑
        qa_pos = q_boxes[0].copy().get_center()
        pair_lines_qa = VGroup(*[pair_lines[i] for i in [0, 1, 2]])
        qb_pos = q_boxes[1].copy().get_center()
        pair_lines_qb = VGroup(*[pair_lines[i] for i in [3, 4, 5]])
        # pair_lines_qa.add_updater(lambda m: m.put_start_and_end_on(q_boxes[0].get_right(), m.get_end()))
        fns_qa = []
        for item in pair_lines_qa:
            fn = lambda m: m.put_start_and_end_on(q_boxes[0].get_right(), m.get_end())
            item.add_updater(fn)
            fns_qa.append(fn)
        fns_qb = []
        for item in pair_lines_qb:
            fn = lambda m: m.put_start_and_end_on(q_boxes[1].get_right(), m.get_end())
            item.add_updater(fn)
            fns_qb.append(fn)
        self.playw(
            q_boxes[0].animate.move_to(qb_pos),
            q_boxes[1].animate.move_to(qa_pos),
        )

        # 연결선 업데이트 → 같은 9개 쌍이 유지됨

        # === 5. V 가중치 합: 교환법칙 시각화 ===
        v_boxes = VGroup(*[texb(f"v_{c}") for c in "ABC"])
        v_boxes.arrange(DOWN, buff=0.5).shift(RIGHT * 6)
        v_label = Text("V", font_size=28, color=ORANGE).next_to(v_boxes, UP)

        self.playw(FadeIn(v_boxes, v_label), self.cf.animate.shift(RIGHT * 2))

        for item, fn in zip(pair_lines_qa, fns_qa):
            item.remove_updater(fn)
        for item, fn in zip(pair_lines_qb, fns_qb):
            item.remove_updater(fn)

        o_boxes = VGroup(*[texb(f"o_{c}") for c in "BAC"])
        o_boxes.arrange(DOWN, buff=0.5).shift(RIGHT * 8)
        o_label = Text("Output", font_size=28, color=PURPLE).next_to(o_boxes, UP)
        anims = []
        temps = []
        for i in range(3):
            anims.append(
                [
                    Transform(pair_lines_qb[i], temp := v_boxes[i].copy()),
                    Indicate(v_boxes[i], scale_factor=1.0),
                ]
            )
            temps.append(temp)
        anims = SkewedAnimations(*anims)
        for anim in anims:
            self.play(*anim)
        self.remove(*temps)
        self.play(
            FadeIn(o_label),
            Transformr(v_boxes.copy(), o_boxes[0]),
            self.cf.animate.scale(1.2).shift(RIGHT),
        )
        ol = self.overlay
        q_boxes[1].set_z_index(ol.z_index + 1)
        o_boxes[0].set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))


class wope(Scene2D):
    def construct(self):
        words_list = ["어떻게", "고양이를", "좋아하는", "나를", "버려"]
        perms_idx = [3, 2, 1, 0, 4]
        words1 = Words(" ".join(words_list), font="Noto Sans KR", color=GREY_B).scale(
            0.7
        )
        words2 = Words(
            " ".join([words_list[i] for i in perms_idx]),
            font="Noto Sans KR",
            color=GREY_B,
        ).scale(0.7)

        VGroup(words1, words2).arrange(DOWN, buff=1)

        self.playwl(*[FadeIn(w) for w in words1.words], lag_ratio=0.4)
        self.playwl(*[FadeIn(w) for w in words2.words], lag_ratio=0.4)

        self.playwl(
            *[
                AnimationGroup(
                    Indicate(words1.words[i], scale_factor=1.1, color=YELLOW_B),
                    Indicate(
                        words2.words[perms_idx[i]], scale_factor=1.1, color=YELLOW_B
                    ),
                )
                for i in range(len(words1.words))
            ],
            lag_ratio=0.5,
        )

        lines = VGroup(
            *[
                DashedLine(
                    words1.words[i].get_bottom(),
                    words2.words[perms_idx[i]].get_top(),
                    color=YELLOW_A,
                    stroke_width=2,
                    dash_length=0.15,
                    dashed_ratio=0.8,
                )
                for i in range(len(words1.words))
            ]
        )
        self.playw(*[Create(line) for line in lines])

        self.play(FadeOut(lines))
        self.play(Flash(words1.get_corner(UL), color=RED))
        self.playw(Flash(words2.get_corner(UL), color=GREEN))

        self.play(VGroup(words1, words2).animate.shift(LEFT * 3))
        t1 = Tensor(len(words_list), shape="circle", arrange=RIGHT, buff=0.15).move_to(
            words1
        )
        t2 = (
            VGroup(*[t1[i].copy() for i in perms_idx])
            .arrange(RIGHT, buff=0.15)
            .move_to(words2)
        )
        self.playw(
            *[
                Transformr(VGroup(*words1.words[i]), t1[i])
                for i in range(len(words1.words))
            ],
            *[Transformr(words2.words[i], t2[i]) for i in range(len(words2.words))],
        )

        model = Rectangle(
            width=5, height=3, color=GREY_B, fill_color=BLACK, fill_opacity=0.75
        ).set_z_index(1)
        modelt = (
            Text("Transformer without PE", font="Noto Sans KR", color=BLUE)
            .scale(0.5)
            .next_to(model, DOWN)
        )

        model = VGroup(model, modelt).shift(RIGHT * 2)
        self.playw(FadeIn(model))
        self.play(VGroup(t1, t2).animate.move_to(model[0].get_center()))
        self.playw(self.cf.animate.move_to(model))

        lines = VGroup(
            *[
                DashedLine(
                    t1[i].get_bottom(),
                    t2[perms_idx[i]].get_top(),
                    color=YELLOW_A,
                    stroke_width=2,
                    dash_length=0.15,
                    dashed_ratio=0.8,
                )
                for i in range(len(t1))
            ]
        )
        self.playw(*[Create(line) for line in lines])


class howpe(Scene3D):
    def construct(self):
        words_list = ["어떻게", "고양이를", "좋아하는", "나를", "버려"]
        words = Words(" ".join(words_list), font="Noto Sans KR", color=GREY_B).scale(
            0.7
        )

        w_seq = Tensor(
            len(words_list), shape="circle", arrange=RIGHT, buff=0.8
        ).move_to(words)
        self.addw(words)
        self.play(
            *[Transform(words.words[i], w_seq[i]) for i in range(len(words.words))]
        )

        pe = Tensor(len(words_list), shape="square", arrange=RIGHT).move_to(words)
        for i, item in enumerate(pe):
            item.next_to(words.words[i], UP, buff=0.75)
        pluses = VGroup(
            *[MathTex("+", font_size=24).next_to(item, DOWN, buff=0.3) for item in pe]
        )
        self.play(FadeIn(pe, shift=UP * 0.5))

        pe_t = (
            Words("Positional Encoding", font="Noto Sans KR", color=BLUE)
            .scale(0.5)
            .next_to(pe, UP)
        )
        pe_b = DashedVMobject(
            SurroundingRectangle(pe, color=BLUE, buff=0.1, stroke_width=2),
            num_dashes=60,
            dashed_ratio=0.6,
        )
        self.playw(FadeIn(pe_t, pe_b))

        iths = VGroup()
        for i in range(len(pe)):
            ith = (
                Text(f"[{i}]th", color=GREY_A, font="Noto Sans KR")
                .scale(0.35)
                .next_to(pe[i], UP, buff=0.15)
            )
            iths.add(ith)
        self.playwl(
            FadeOut(pe_t, pe_b),
            *[FadeIn(ith, shift=UP * 0.3) for ith in iths],
            lag_ratio=0.5,
        )
        self.playw(FadeIn(pluses))

        nnembed = (
            Text("nn.Embedding()", font=MONO_FONT, color=GREEN)
            .scale(0.4)
            .next_to(pe, UL)
        )
        self.playw(FadeIn(nnembed))

        entries = VGroup(
            *[
                VGroup(w, p, plus, ith)
                for w, p, plus, ith in zip(words.words, pe, pluses, iths)
            ]
        )
        self.move_camera_horizontally(
            45,
            added_anims=[
                entries.animate.arrange(RIGHT, buff=2.3).shift(RIGHT),
                nnembed.animate.rotate(-45 * DEGREES, axis=UP),
            ],
        )

        embeds = VGroup(*[nnembed.copy() for _ in range(len(words_list))])
        for i in range(len(pe)):
            em = embeds[i]
            em.generate_target().scale(0.8)
            em.target[:-1].rotate(45 * DEGREES, axis=UP).next_to(
                iths[i], LEFT, buff=0.1
            )
            em.target[-1].rotate(45 * DEGREES, axis=UP).next_to(
                iths[i], RIGHT, buff=0.1
            )
        self.playw(*[MoveToTarget(em) for em in embeds])

        anims = []
        temps = []
        for i in range(len(pe)):
            emi = VGroup(embeds[i], iths[i])
            anim = Transformr(emi.copy(), (tmp := pe[i].copy()))
            anims.append(anim)
            temps.append(tmp)
        self.playw(*anims)
        self.remove(*temps)

        lpe = (
            Words("Learnable Positional Encoding", font="Noto Sans KR", color=GREEN_C)
            .rotate(-45 * DEGREES, axis=UP)
            .scale(0.5)
            .next_to(nnembed, UP)
        )
        ol = self.overlay.scale(2)
        lpe.set_z_index(ol.z_index + 1)
        self.playwl(FadeIn(ol), *[FadeIn(w) for w in lpe.words], lag_ratio=0.5)

        self.play(FadeOut(lpe, ol, *embeds, nnembed))
        self.playw(entries.animate.arrange(RIGHT, buff=0.8).shift(LEFT * 4))

        more_items = 16
        w_seq_more = Tensor(
            more_items, shape="circle", arrange=RIGHT, buff=0.8
        ).next_to(words, RIGHT, buff=0.8)
        pe_more = Tensor(more_items, shape="square", arrange=RIGHT, buff=0.8).next_to(
            pe, RIGHT, buff=0.8
        )
        pluses_more = VGroup(
            *[
                MathTex("+", font_size=24).next_to(item, DOWN, buff=0.3)
                for item in pe_more
            ]
        )
        iths_more = VGroup()

        def idx_fn(i):
            if i < 6:
                return f"[{i + len(pe)}]th"
            elif i < 10:
                return "..."
            else:
                return f"[{i + 512 - more_items}]th"

        for i in range(more_items):
            ith = (
                Text(idx_fn(i), color=GREY_A, font="Noto Sans KR")
                .scale(0.35)
                .next_to(pe_more[i], UP, buff=0.15)
            )
            iths_more.add(ith)
        entries_more = VGroup(
            *[
                VGroup(w, p, plus, ith)
                for w, p, plus, ith in zip(
                    w_seq_more,
                    pe_more,
                    pluses_more,
                    iths_more,
                )
            ]
        )  # .arrange(RIGHT, buff=0.8).next_to(entries, RIGHT, buff=0.8)
        self.play(FadeIn(entries_more))
        self.playw(self.cf.animate.shift(19 * RIGHT + IN * 2), run_time=3)

        self.playw(
            Circumscribe(entries_more[-1], fade_in=True, fade_out=True, color=YELLOW)
        )

        w_seq_513 = Tensor(1, shape="circle", arrange=RIGHT).next_to(
            w_seq_more[-1], RIGHT, buff=0.8
        )
        pe_513 = Tensor(1, shape="square", arrange=RIGHT).next_to(
            pe_more[-1], RIGHT, buff=0.8
        )
        plus_513 = MathTex("+", font_size=24).next_to(pe_513, DOWN, buff=0.3)
        ith_513 = (
            Text("[512]th", color=GREY_A, font="Noto Sans KR")
            .scale(0.35)
            .next_to(pe_513, UP, buff=0.15)
        )
        entry_513 = VGroup(w_seq_513, pe_513, plus_513, ith_513)
        self.playw(FadeIn(w_seq_513))

        self.play(FadeIn(pe_513, plus_513, ith_513))
        problem = VGroup(pe_513, plus_513, ith_513)
        self.playw(problem.animate.set_color(PURE_RED))

        self.playw(RWiggle(problem), run_time=3)


class sinusoidalpe(Scene2D):
    def construct(self):
        pe_sin = RaeTex(
            r"PE_{( pos ,\, 2i )}",
            r"=",
            r"\sin",
            r"\!\left(",
            r"\frac{ pos }{10000^{\frac{2i}{d_{model}}}}",
            r"\right)",
            items=[" pos ", r",\,", "2i ", ")}", r"\sin"],
        ).scale(0.7)
        pe_sin[2:].set_color(BLUE)
        pe_cos = RaeTex(
            r"PE_{( pos ,\, 2i+1 )}",
            r"=",
            r"\cos",
            r"\!\left(",
            r"\frac{ pos }{10000^{\frac{2i}{d_{model}}}}",
            r"\right)",
            items=[" pos ", r",\,", " 2i+1 ", ")}", r"\cos"],
        ).scale(0.7)
        pe_cos[2:].set_color(BLUE)
        pe = VGroup(pe_sin, pe_cos).arrange(DOWN, buff=1, aligned_edge=RIGHT)
        self.addw(pe, wait=1.5)

        sit = (
            Words("Sinusoidal Positional Encoding", color=BLUE).scale(0.7).shift(UP * 3)
        )
        self.playwl(*[FadeIn(item) for item in sit.words], lag_ratio=0.5)

        nnembed = (
            Text("nn.Embedding(pos)", font=MONO_FONT, color=GREEN)
            .scale(0.4)
            .next_to(self.cf, RIGHT, buff=0.1)
        )
        nnembed.save_state()
        self.play(
            nnembed.animate.to_edge(RIGHT, buff=0.1), run_time=2, rate_func=linear
        )
        self.playw(Restore(nnembed), run_time=2, rate_func=linear)

        self.playw(
            *[Indicate(item) for item in pe_sin[" pos "]],
            *[Indicate(item) for item in pe_cos[" pos "]],
        )

        fx = MathTex("f(x)")
        pe.generate_target()
        pe.target.arrange(DOWN, buff=0.4, aligned_edge=RIGHT)
        fb = Brace(pe.target, LEFT, color=GREY_B).scale(0.7)
        self.playw(
            MoveToTarget(pe),
            FadeIn(fb),
            FadeIn(fx.next_to(fb, LEFT, buff=0.3)),
        )

        num_seq = 12
        iths = VGroup()

        def ith_string(i):
            if i < 4:
                return f"[{i}]th"
            elif i < 9:
                return "..."
            else:
                return f"[{512 + i - num_seq}]th"

        for i in range(num_seq):
            iths.add(Text(ith_string(i), color=GREY_A, font="Noto Sans KR").scale(0.35))
        iths.arrange(RIGHT, buff=0.5).align_to(fx, LEFT).shift(DOWN * 2)
        self.playwl(*[FadeIn(ith) for ith in iths], lag_ratio=0.3)

        def fi_string(i):
            if i < 4:
                return f"f({i})"
            elif i < 9:
                return "f(...)"
            else:
                return f"f({512 + i - num_seq})"

        skew_anims = []
        vectors = VGroup()
        fis = VGroup()
        for i in range(num_seq):
            if i % 2 == 0:
                item = pe_sin[" pos "][1]
                f = VGroup(pe_sin.copy(), iths[i])
            else:
                item = pe_cos[" pos "][1]
                f = VGroup(pe_cos.copy(), iths[i])

            fi = MathTex(fi_string(i), font_size=24).move_to(iths[i])
            fis.add(fi)
            v = Tensor(1, shape="square").scale(0.7).next_to(fi, DOWN, buff=0.1)
            vectors.add(v)

            skew_anims.append(
                [
                    AnimationGroup(
                        item.animate.set_opacity(0), iths[i].animate.move_to(item)
                    ),
                    Transformr(f, fi),
                    FadeIn(v),
                ]
            )
        skew_anims = SkewedAnimations(*skew_anims)
        for anim in skew_anims:
            self.play(*anim, run_time=0.5)
        self.wait()

        self.play(VGroup(fx, pe, fb, iths, fis, vectors).animate.shift(UP))

        w_seq = VGroup(
            *[
                Tensor(1, shape="circle").scale(0.7).next_to(vectors[i], DOWN, buff=0.4)
                for i in range(num_seq)
            ]
        )
        pluses = VGroup(
            *[
                MathTex("+", font_size=24).next_to(vectors[i], DOWN, buff=0.15)
                for i in range(num_seq)
            ]
        )
        self.remove(nnembed)
        self.playwl(FadeIn(pluses), FadeIn(w_seq), lag_ratio=0.5)

        more_items = 4
        vectors_more = (
            Tensor(more_items, shape="square", arrange=RIGHT, buff=0.8)
            .scale(0.7)
            .next_to(vectors, RIGHT, buff=0.8)
        )
        w_seq_more = VGroup(
            *[
                Tensor(1, shape="circle")
                .scale(0.7)
                .next_to(vectors_more[i], DOWN, buff=0.4)
                for i in range(more_items)
            ]
        )
        pluses_more = VGroup(
            *[
                MathTex("+", font_size=24).next_to(item, DOWN, buff=0.15)
                for item in vectors_more
            ]
        )
        iths_more = VGroup()
        for i in range(more_items):
            ith = (
                Text(f"[{512 + i}]th", color=GREY_A, font="Noto Sans KR")
                .scale(0.35)
                .next_to(vectors_more[i], UP, buff=0.15)
            )
            iths_more.add(ith)
        entries_more = (
            VGroup(
                *[
                    VGroup(w, p, v, ith)
                    for w, p, v, ith in zip(
                        w_seq_more,
                        vectors_more,
                        pluses_more,
                        iths_more,
                    )
                ]
            )
            .arrange(RIGHT, buff=0.8)
            .next_to(vectors, RIGHT, buff=0.8)
            .align_to(iths, UP)
        )
        self.playwl(FadeIn(entries_more))

        skew_anims_more = []
        fs_more = VGroup()
        for i in range(more_items):
            if i % 2 == 0:
                item = pe_cos[" pos "][1]
                f = VGroup(pe_cos.copy(), iths_more[i])
            else:
                item = pe_sin[" pos "][1]
                f = VGroup(pe_sin.copy(), iths_more[i])
            fs_more.add(f)
            fi = MathTex(fi_string(num_seq + i), font_size=24).move_to(iths_more[i])
            skew_anims_more.append(
                [
                    AnimationGroup(iths_more[i].animate.move_to(item)),
                    Transform(f, fi),
                ]
            )

        skew_anims_more = SkewedAnimations(*skew_anims_more)
        self.cf.save_state()
        for i, anim in enumerate(skew_anims_more):
            self.playw(*anim, wait=0.2)
        self.playw(self.cf.animate.shift(RIGHT * 9))

        extrap_t = (
            Text("Extrapolation", color=YELLOW).scale(0.5).next_to(fi, UP, buff=0.75)
        )
        self.playw(FadeIn(extrap_t, shift=UP * 0.3))

        self.wait()
        pe_sin[" pos "][1].set_opacity(1)
        pe_cos[" pos "][1].set_opacity(1)
        # VGroup(fx, fb, pe).shift(DOWN)

        self.playw(
            Restore(self.cf),
            FadeOut(entries_more, iths_more, fs_more, fis, vectors, pluses, w_seq),
            run_time=2,
        )
        pe.save_state()
        self.playw(pe.animate.set_color(RED))

        ol = self.overlay
        pe_sin[r"\sin"].set_z_index(ol.z_index + 1)
        pe_cos[r"\cos"].set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))

        self.playw(FadeOut(ol))
        pe_sin[r"\sin"].set_z_index(ol.z_index - 1)
        pe_cos[r"\cos"].set_z_index(ol.z_index - 1)
        pe_sin[" pos "].set_z_index(ol.z_index + 1)
        pe_cos[" pos "].set_z_index(ol.z_index + 1)
        pe_sin[-2].set_z_index(ol.z_index + 1)
        pe_cos[-2].set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))

        self.playw(FadeOut(ol), Restore(pe))


class clock(Scene2D):
    def construct(self):
        circle = Circle(
            radius=2, color=GREY_B, fill_color=BLACK, fill_opacity=0.75
        ).shift(UP * 0.5)

        self.playw(FadeIn(circle))
        ct = (
            Text("Clock", color=BLUE, font="Noto Serif KR")
            .scale(0.5)
            .next_to(circle, DOWN, buff=0.5)
        )
        self.playw(FadeIn(ct, shift=DOWN * 0.5))

        def get_digit(tv):
            total = int(tv)
            hh, mm, ss = total // 3600, (total % 3600) // 60, total % 60
            return Text(
                f"{hh%24:02d}:{mm:02d}:{ss:02d}", font=MONO_FONT, color=GREEN
            ).scale(0.6)

        t = ValueTracker(4 * 3600 + 14 * 60)  # 4:14:00
        digit = get_digit(t.get_value()).next_to(circle, RIGHT, buff=0.5).shift(UP)
        c_center = Dot(circle.get_center(), radius=0.05, color=GREY_C)

        self.playw(FadeIn(digit, shift=RIGHT * 0.5), FadeIn(c_center))

        def get_hour_handle(tv):
            angle = PI / 2 - (tv % 43200) / 43200 * 2 * PI
            length = 1.0
            center = circle.get_center()
            end = center + length * np.array([np.cos(angle), np.sin(angle), 0])
            return Line(center, end, stroke_width=6, color=GREY_B)

        def get_minute_handle(tv, opacity=1.0):
            angle = PI / 2 - (tv % 3600) / 3600 * 2 * PI
            length = 1.4
            center = circle.get_center()
            end = center + length * np.array([np.cos(angle), np.sin(angle), 0])
            return Line(center, end, stroke_width=4, color=GREEN_B).set_opacity(opacity)

        def get_second_handle(tv, opacity=1.0):
            angle = PI / 2 - (tv % 60) / 60 * 2 * PI
            length = 1.7
            center = circle.get_center()
            end = center + length * np.array([np.cos(angle), np.sin(angle), 0])
            return Line(center, end, stroke_width=2, color=RED_B).set_opacity(opacity)

        hour_handle = get_hour_handle(t.get_value())
        minute_handle = get_minute_handle(t.get_value())
        second_handle = get_second_handle(t.get_value())

        self.playw(FadeIn(hour_handle), FadeIn(minute_handle), FadeIn(second_handle))
        s_opacity = 1
        m_opacity = 1
        hour_handle.add_updater(lambda mob: mob.become(get_hour_handle(t.get_value())))
        minute_handle.add_updater(
            lambda mob: mob.become(get_minute_handle(t.get_value(), m_opacity))
        )
        second_handle.add_updater(
            lambda mob: mob.become(get_second_handle(t.get_value(), s_opacity))
        )
        digit.add_updater(
            lambda mob: mob.become(
                get_digit(t.get_value()).next_to(circle, RIGHT, buff=0.5).shift(UP)
            )
        )

        self.playw(
            t.animate.set_value(4 * 3600 + 15 * 60), run_time=2.5, rate_func=linear
        )
        self.playw(
            t.animate.set_value(7 * 3600 + 15 * 60 + 23), run_time=5.5, rate_func=linear
        )

        hour_handle.clear_updaters()
        minute_handle.clear_updaters()
        second_handle.clear_updaters()
        digit.clear_updaters()

        c = VGroup(c_center, hour_handle, minute_handle, second_handle)
        c.save_state()
        self.cf.save_state()
        opacity = 0.2
        self.playw(
            self.cf.animate.move_to(digit),
            c.animate.set_opacity(opacity),
            circle.animate.set_stroke(opacity=opacity),
            ct.animate.set_opacity(opacity),
        )

        vec = (
            Words("[7, 15, 23]", font=MONO_FONT, color=GREEN)
            .scale(0.6)
            .next_to(digit, DOWN, buff=0.5)
        )
        vs = vec.words[-1][:-1]
        vm = vec.words[1][:-1]
        vh = vec.words[0][1:-1]
        remain = VGroup(
            vec.words[0][0],
            vec.words[0][-1],
            vec.words[1][-1],
            vec.words[2][-1],
        ).set_opacity(0.5)

        self.playw(Transformr(digit[-2:].copy(), vs), FadeIn(remain))
        self.playw(Transformr(digit[3:-3].copy(), vm))
        self.playw(Transformr(digit[:2].copy(), vh))

        self.playw(Restore(c), Restore(self.cf))

        ol = self.overlay
        vs.set_z_index(ol.z_index + 1)
        vm.set_z_index(ol.z_index + 1)
        vh.set_z_index(ol.z_index + 1)
        self.play(FadeIn(ol))
        self.playw(RWiggle(vs), RWiggle(vm), RWiggle(vh), run_time=3)

        self.play(FadeOut(ol))
        self.playw(
            Circumscribe(VGroup(vs, vm, vh), fade_in=True, fade_out=True, color=YELLOW)
        )

        self.playw(Indicate(hour_handle), Indicate(vh))
        self.playw(Indicate(minute_handle), Indicate(vm))
        self.playw(Indicate(second_handle), Indicate(vs))


class sinusoidallikeclock(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(-18)

        def pe_fn(pos, i, d_model=16):
            if i % 2 == 0:
                return np.sin(pos / (10000 ** (i / d_model)))
            else:
                return np.cos(pos / (10000 ** ((i - 1) / d_model)))

        num_items = 16
        num_pos = 512
        pes = []
        for pos in range(num_pos):
            pe = [pe_fn(pos, i) for i in range(num_items)]
            pes.append(pe)

        d_model = num_items
        n_pairs = num_items // 2  # 8 pairs: (0,1),(2,3),...,(14,15)

        numps = (
            VGroup(
                *[
                    RaenimPlane(
                        x_range=(0, 200), y_range=(-1.3, 1.3), x_length=100
                    ).rotate(PI / 2, axis=UP)
                    for i in range(num_items)
                ]
            )
            .arrange(RIGHT, buff=0.8)
            .shift(IN * 28 + DOWN * 1.5)
        )

        plots = VGroup()
        for i, nump in enumerate(numps):
            nump: NumberPlane
            plot = nump.plot(
                lambda x: pe_fn(x, i, d_model), color=BLUE, stroke_width=1.5
            ).set_stroke(opacity=0.8)
            nump.x_axis.set_opacity(0.7)
            nump.y_axis.set_opacity(0)
            plots.add(plot)
        tags = VGroup()
        for i in range(num_items):
            tag = (
                Text(f"[{i}]", color=GREY_C, font="Noto Sans")
                .scale(0.3)
                .move_to(numps[i].c2p(-2, 0))
            )
            tags.add(tag)

        dots = VGroup()
        fns = []
        t = ValueTracker(0)
        for i in range(num_items):
            dot = Dot(color=RED).set_z_index(1)
            dot.move_to(numps[i].c2p(0, pe_fn(0, i, d_model)))
            fn = lambda m, i=i: m.move_to(
                numps[i].c2p(t.get_value(), pe_fn(t.get_value(), i, d_model))
            )
            dot.add_updater(fn)
            dots.add(dot)
            fns.append(fn)
        self.play(FadeIn(numps, tags, dots))

        trail_dots = VGroup()
        self.add(trail_dots)
        snap_interval = 10
        last_snap = [0.0]

        def leave_trail(mob, dt):
            current_t = t.get_value()
            if current_t - last_snap[0] >= snap_interval:
                last_snap[0] = current_t
                for dot in dots:
                    snapshot = (
                        dot.copy()
                        .set_color(BLUE_C)
                        .clear_updaters()
                        .set_opacity(1)
                        .scale(0.6)
                    )
                    trail_dots.add(snapshot)

        dots.add_updater(leave_trail)
        self.play(*[Create(plot) for plot in plots], run_time=2)
        self.playw(t.animate.set_value(180), run_time=4, rate_func=rush_into)
        dots.remove_updater(leave_trail)

        pos_t = (
            Text("Position (Time)", color=GREEN, font="Noto Sans")
            .scale(0.3)
            .next_to(numps, LEFT, buff=0.1)
            .align_to(numps, OUT)
        )
        pos_a = Arrow(
            pos_t.get_top(), pos_t.get_top() + IN * 10, color=GREEN, tip_length=0.2
        ).set_stroke(width=2)
        idx_t = (
            Text("Dimension (Index)", color=GREY_C, font="Noto Sans")
            .scale(0.3)
            .next_to(tags, LEFT, buff=0.3)
            .shift(OUT * 0.6 + RIGHT)
        )
        idx_a = Arrow(
            idx_t.get_right(),
            idx_t.get_right() + RIGHT * 5,
            color=GREY_C,
            tip_length=0.15,
        ).set_stroke(width=2)
        self.playwl(GrowArrow(idx_a), FadeIn(idx_t), lag_ratio=0.3)
        self.playwl(
            GrowArrow(pos_a),
            self.cf.animate.shift(OUT * 3 + UP * 1 + LEFT * 0.5),
            FadeIn(pos_t),
            lag_ratio=0.3,
        )

        self.playw(Indicate(plots[0], color=PURE_YELLOW, scale_factor=1))
        self.playw(Indicate(plots[-1], color=PURE_YELLOW, scale_factor=1))


class cosAminusB(Scene2D):
    def construct(self):
        eq = RaeTex(
            *[r"\cos", "\!\left(", r"A", r"-", r"B", r"\right)"],
            "=",
            *[r"\cos", "\!\left(", r"A", r"\right)"],
            *[r"\cos", "\!\left(", r"B", r"\right)"],
            r"+",
            *[r"\sin", "\!\left(", r"A", r"\right)"],
            *[r"\sin", "\!\left(", r"B", r"\right)"],
            items=[r"\sin", r"\cos", r"A", r"B", r"-", r"+", r"="],
        )

        self.playw(FadeIn(eq))
        self.playwl(
            *[
                Indicate(eq[i], color=YELLOW_C, scale_factor=1.1)
                for i in [
                    0,
                    slice(1, 6),
                    6,
                    slice(7, 11),
                    slice(11, 15),
                    15,
                    slice(16, 20),
                    slice(20, 24),
                ]
            ],
            lag_ratio=0.3,
        )

        self.play(FadeOut(eq))

        def get_pe_sin(position, i):
            return RaeTex(
                r"\sin\!\left(",
                f"\\frac{{{position}}}{{10000^ \\frac{{{i}}}{{d}}}}",
                r"\right)",
                items=[f"\\frac{{{position}}}{{10000^ \\frac{{{i}}}{{d}}}}"],
            ).scale(0.4)

        def get_pe_cos(position, i):
            return RaeTex(
                r"\cos\!\left(",
                f"\\frac{{{position}}}{{10000^ \\frac{{{i}}}{{d}}}}",
                r"\right)",
                items=[f"\\frac{{{position}}}{{10000^ \\frac{{{i}}}{{d}}}}"],
            ).scale(0.4)

        def get_pe_tex(position, i):
            if i % 2 == 0:
                return get_pe_sin(position, i)
            else:
                return get_pe_cos(position, i - 1)

        num_i = 8
        num_pos = 16
        pes = (
            VGroup(
                *[
                    VGroup(*[get_pe_tex(pos, i) for i in range(num_i)]).arrange(
                        DOWN, aligned_edge=LEFT
                    )
                    for pos in range(num_pos)
                ]
            )
            .arrange(RIGHT, buff=0.5)
            .shift(RIGHT * 7 + UP * 0.5)
            .set_opacity(0.4)
        )

        pe_ts = VGroup()
        for pos in range(num_pos):
            pe_t = (
                Text(f"pe({pos})", color=GREY_C, font="Noto Sans")
                .scale(0.3)
                .set_color(GREY_C)
                .next_to(pes[pos], DOWN, buff=0.1)
            )
            pe_ts.add(pe_t)

        pe4 = pes[4].set_opacity(1)
        pe6 = pes[6].set_opacity(1)
        pe1 = pes[1].set_opacity(1)
        pe3 = pes[3].set_opacity(1)
        pet4 = pe_ts[4]
        pet6 = pe_ts[6]
        pet1 = pe_ts[1]
        pet3 = pe_ts[3]

        self.playw(FadeIn(pes, pe_ts))

        get_cdot = lambda: MathTex(r"\cdot", font_size=24)
        ip1 = VGroup(pet1, pet3)
        ip1.generate_target().arrange(RIGHT).move_to(VGroup(pet1, pet3))
        prod1 = get_cdot().move_to(ip1.get_center())
        ip2 = VGroup(pet4, pet6)
        ip2.generate_target().arrange(RIGHT).move_to(VGroup(pet4, pet6))
        prod2 = get_cdot().move_to(ip2.get_center())

        cdots1 = VGroup(
            *[
                get_cdot().move_to(VGroup(pe1[i], pe3[i]).get_center())
                for i in range(num_i)
            ]
        ).set_opacity(0)
        ipe1 = VGroup(pe1, cdots1, pe3)
        cdots2 = VGroup(
            *[
                get_cdot().move_to(VGroup(pe4[i], pe6[i]).get_center())
                for i in range(num_i)
            ]
        ).set_opacity(0)
        ipe2 = VGroup(pe4, cdots2, pe6)
        ipe1.generate_target().arrange(RIGHT, buff=0.1).move_to(ipe1).set_opacity(1)
        ipe2.generate_target().arrange(RIGHT, buff=0.1).move_to(ipe2).set_opacity(1)

        ipe1t = VGroup(*[VGroup(*items) for items in zip(*ipe1)])
        ipe2t = VGroup(*[VGroup(*items) for items in zip(*ipe2)])

        self.play(
            *[FadeOut(pes[i]) for i in range(num_pos) if i not in [1, 3, 4, 6]],
            *[FadeOut(pe_ts[i]) for i in range(num_pos) if i not in [1, 3, 4, 6]],
            MoveToTarget(ip1),
            FadeIn(prod1),
            MoveToTarget(ip2),
            FadeIn(prod2),
            MoveToTarget(ipe1),
            MoveToTarget(ipe2),
        )

        get_plus = lambda: MathTex("+", font_size=24)

        ip1_pairs = VGroup(
            *[
                VGroup(ipe1t[i], get_plus().set_opacity(0), ipe1t[i + 1])
                for i in range(0, num_i, 2)
            ]
        )
        ip1_pairs.generate_target()
        for item in ip1_pairs.target:
            item.arrange(RIGHT, buff=0.1)
        ip1_pairs.target.arrange(DOWN, buff=0.2).set_opacity(1).next_to(
            ip1, UP, buff=0.5
        ).shift(LEFT * 0.7)

        ip2_pairs = VGroup(
            *[
                VGroup(ipe2t[i], get_plus().set_opacity(0), ipe2t[i + 1])
                for i in range(0, num_i, 2)
            ]
        )
        ip2_pairs.generate_target()
        for item in ip2_pairs.target:
            item.arrange(RIGHT, buff=0.1)
        ip2_pairs.target.arrange(DOWN, buff=0.2).set_opacity(1).next_to(
            ip2, UP, buff=0.5
        ).shift(RIGHT * 0.7)

        self.playw(
            MoveToTarget(ip1_pairs),
            MoveToTarget(ip2_pairs),
            ip1.animate.shift(LEFT * 0.5),
            prod1.animate.shift(LEFT * 0.5),
            ip2.animate.shift(RIGHT * 0.5),
            prod2.animate.shift(RIGHT * 0.5),
        )

        result1 = (
            VGroup(*[get_pe_cos("1 - 3", i) for i in range(0, num_i, 2)])
            .arrange(DOWN, buff=0.2)
            .move_to(ip1_pairs)
        )
        result2 = (
            VGroup(*[get_pe_cos("4 - 6", i) for i in range(0, num_i, 2)])
            .arrange(DOWN, buff=0.2)
            .move_to(ip2_pairs)
        )
        self.play(Transformr(ip1_pairs, result1), Transformr(ip2_pairs, result2))
        res1 = Joiner(*result1, join=lambda: get_plus().set_opacity(0))
        res2 = Joiner(*result2, join=lambda: get_plus().set_opacity(0))
        res1.generate_target().arrange(RIGHT, buff=0.1).move_to(result1).set_opacity(1)
        res2.generate_target().arrange(RIGHT, buff=0.1).move_to(result2).set_opacity(1)
        self.playw(MoveToTarget(res1), MoveToTarget(res2))

        equal = MathTex("=").move_to(VGroup(res1, res2).get_center())
        self.playw(FadeIn(equal))
