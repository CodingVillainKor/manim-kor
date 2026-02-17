from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)

# ── 전체 씬 공유 ──
tilt_degree = 60
_UP = OUT * np.cos(tilt_degree * DEGREES) + UP * np.sin(tilt_degree * DEGREES)
rot = lambda m: m.rotate(tilt_degree * DEGREES, axis=RIGHT)

# ── Attention 레이아웃 공유 (introAttention, softmaxIssue, maxMdenomL, flashAttentionOverview) ──
seq_len = 6
attn_buff = 0.54


class introAttention(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(tilt_degree)
        qs, ks, vs = [Tensor(seq_len, shape="square") for _ in range(3)]
        os = Tensor(seq_len, shape="square")
        attn = VGroup(
            *[
                VGroup(*[Dot(color=random_color()) for _ in range(seq_len)]).arrange(
                    RIGHT, buff=attn_buff
                )
                for _ in range(seq_len)
            ]
        ).arrange(DOWN, buff=attn_buff)

        dummy = Tensor(1).shift(UL * 2)
        qs.arrange(DOWN, buff=0.3).next_to(dummy, DOWN, buff=0.5)
        ks.arrange(RIGHT, buff=0.3).next_to(dummy, RIGHT, buff=0.5)
        attn.next_to(qs, RIGHT, buff=0.65)
        attn_ = attn.copy()
        for i in range(seq_len):
            for j in range(seq_len):
                attn_[i][j].set_fill(random_color(), opacity=0.7)

        vs.arrange(RIGHT, buff=0.3).next_to(ks, _UP, buff=1).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )
        os.arrange(DOWN, buff=0.3).next_to(attn, RIGHT, buff=0.8)

        qt = (
            Text("Query", font="Noto Sans KR")
            .scale(0.4)
            .next_to(qs, DOWN, buff=0.2)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
        )
        kt = (
            Text("Key", font="Noto Sans KR")
            .scale(0.4)
            .next_to(ks, LEFT, buff=0.2)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
        )
        vt = (
            Text("Value", font="Noto Sans KR")
            .scale(0.4)
            .next_to(vs, LEFT, buff=0.2)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
        )
        ot = (
            Text("Output", font="Noto Sans KR")
            .scale(0.4)
            .next_to(os, DOWN, buff=0.2)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
        )

        q = VGroup(qs, qt)
        k = VGroup(ks, kt)
        v = VGroup(vs, vt)
        o = VGroup(os, ot)
        self.playwl(*[FadeIn(item) for item in [q, k, v]], lag_ratio=0.5)

        anims = []
        trt = lambda x, y: Transform(
            x.copy(), y, replace_mobject_with_target_in_scene=True
        )
        for i in range(seq_len):
            for j in range(seq_len):
                q_, k_ = qs[i], ks[j]
                anims.append(trt(VGroup(q_, k_), attn[i][j]))
        self.playw(*anims)

        ast = (
            Words("Attention Score", font="Noto Sans KR")
            .scale(0.5)
            .next_to(attn, DOWN, buff=0.2)
        )
        self.playwl(*[FadeIn(ast)], lag_ratio=0.5)

        def sm(target):
            sm_o = (
                Words("softmax(", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, LEFT, buff=0.1)
            )
            sm_c = (
                Words(")", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, RIGHT, buff=0.1)
            )
            return VGroup(sm_o, sm_c)

        sms = VGroup(*[sm(attn[i]) for i in range(seq_len)])
        self.play(q.animate.shift(LEFT * 1.5), FadeOut(k))
        self.playw(*[FadeIn(sms[i]) for i in range(seq_len)])
        self.playw(Transform(attn, attn_), FadeOut(sms))

        def sum_anim():
            sigma = MathTex(r"\sum").scale(1.8).move_to(vs)
            anim = FadeOut(sigma, scale=2.5, rate_func=rush_from)
            return anim

        total_anims = []
        for i in range(seq_len):
            anims = []
            ai = attn[i].copy()
            anims.append(
                AnimationGroup(
                    *[
                        ai[j]
                        .animate.move_to(vs[j])
                        .set_opacity(1)
                        .rotate(tilt_degree * DEGREES, axis=RIGHT)
                        for j in range(seq_len)
                    ],
                )
            )
            anims.append(
                AnimationGroup(
                    Transform(
                        VGroup(ai, vs.copy()),
                        os[i],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    sum_anim(),
                )
            )
            total_anims.append(anims)
        anims = SkewedAnimations(*total_anims)
        for anim in anims:
            self.play(anim, run_time=0.5)
        self.playw(FadeIn(ot))
        qkvo = Group(*self.mobjects)
        self.playw(qkvo.animate.shift(_UP))

        p1 = Text("QK Inner product", font="Noto Sans KR", color=BLUE).scale(0.5)
        p2 = Text("Softmax", font="Noto Sans KR", color=GREEN).scale(0.5)
        p3 = Text("Weighted sum: V", font="Noto Sans KR", color=YELLOW_B).scale(0.5)
        ps = (
            Joiner(p1, p2, p3, join=lambda: Text("→", color=GREY_B).scale(0.5))
            .arrange(RIGHT, buff=0.3)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .shift(DOWN * 3)
        )
        ol = self.overlay.scale(2).align_to(ot, DOWN)
        ps.set_z_index(ol.z_index + 1)
        self.playwl(FadeIn(ol), *[FadeIn(item) for item in ps], lag_ratio=0.4)

        self.play(Flash(p2.get_corner(UL), color=GREEN), run_time=0.7)
        self.playw(RWiggle(p2, amp=(0.1, 0.1, 0.1)), run_time=2)
        self.playw(FadeOut(qkvo))


class gpuStructure(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(tilt_degree)

        # ── GPU Memory Structure ──
        hbm_rect = RoundedRectangle(
            corner_radius=0.2,
            width=7,
            height=1.6,
            fill_color=BLUE_E,
            fill_opacity=0.15,
            stroke_color=BLUE_B,
            stroke_width=2,
        )
        sram_rect = RoundedRectangle(
            corner_radius=0.15,
            width=3,
            height=1.2,
            fill_color=GREEN_E,
            fill_opacity=0.15,
            stroke_color=GREEN,
            stroke_width=2,
        )
        VGroup(hbm_rect, sram_rect).arrange(_UP, buff=1.5).shift(_UP)

        hbm_title = rot(Text("HBM", font="Noto Sans KR", color=BLUE_B).scale(0.55))
        sram_title = rot(Text("SRAM", font="Noto Sans KR", color=GREEN).scale(0.55))
        hbm_title.next_to(hbm_rect, _UP, buff=0.1).align_to(hbm_rect, LEFT)
        sram_title.next_to(sram_rect, _UP, buff=0.1).align_to(sram_rect, LEFT)

        # "GPU에는 두 종류의 메모리가 있는데요 HBM과 SRAM입니다"
        self.play(FadeIn(hbm_rect), FadeIn(hbm_title))
        self.playw(FadeIn(sram_rect), FadeIn(sram_title))

        # "HBM은 용량이 큰 대신 읽는 속도가 상대적으로 느리구요"
        hbm_p1 = rot(Text("용량 큼", font="Noto Sans KR", color=BLUE).scale(0.4))
        hbm_p2 = rot(Text("속도 느림", font="Noto Sans KR", color=RED_B).scale(0.4))
        VGroup(hbm_p1, hbm_p2).arrange(RIGHT, buff=0.5).move_to(hbm_rect)
        self.playwl(FadeIn(hbm_p1), FadeIn(hbm_p2), lag_ratio=0.5)

        # "SRAM에서 계산이 이루어지는데 속도가 빠르지만 용량이 작습니다"
        sram_p2 = rot(Text("속도 빠름", font="Noto Sans KR", color=GREEN_B).scale(0.4))
        sram_p3 = rot(Text("용량 작음", font="Noto Sans KR", color=RED_B).scale(0.4))
        VGroup(sram_p2, sram_p3).arrange(RIGHT, buff=0.3).move_to(sram_rect)
        self.playwl(FadeIn(sram_p2), FadeIn(sram_p3), lag_ratio=0.5)

        hbm_props = VGroup(hbm_p1, hbm_p2)
        sram_props = VGroup(sram_p2, sram_p3)

        # "실제 계산이 이루어지는 곳은 SRAM이라서 HBM에 있는 데이터를 SRAM으로 가져와야하는데"
        transfer_path = DashedLine(
            hbm_rect.get_center() + _UP * 0.6,
            sram_rect.get_center() - _UP * 0.4,
            color=YELLOW_B,
            stroke_width=2,
            dash_length=0.15,
        )
        path_label = rot(
            Text("데이터 이동 필요", font="Noto Sans KR", color=YELLOW_B).scale(0.4)
        ).next_to(transfer_path, RIGHT, buff=0.2)
        self.playw(
            Create(transfer_path),
            FadeIn(path_label),
            FadeOut(hbm_p1, hbm_p2, sram_p2, sram_p3),
        )

        # "계산하는 시간보다 HBM을 읽는 시간이 길어서 시간 비효율이 발생합니다"
        data = (
            Tensor(4, shape="square", arrange=RIGHT)
            .scale(0.5)
            .move_to(hbm_rect.get_center())
        )
        self.play(FadeIn(data, scale=1.1), FadeOut(path_label), run_time=0.5)
        self.play(
            data.animate.move_to(sram_rect.get_center()), run_time=4.5, rate_func=linear
        )
        self.play(Rotating(data, angle=TAU * 8), rate_func=rush_from, run_time=0.7)
        self.playw(FadeOut(data), run_time=0.3)

        # "문제는 일반적인 attention 계산에서 이 이동이 너무 많다는 점입니다"
        # "아까 말한 attention 계산 과정 QK 행렬곱, softmax, V곱"
        st1 = rot(Text("QK 행렬곱", font="Noto Sans KR", color=BLUE).scale(0.5))
        st2 = rot(Text("softmax", font="Noto Sans KR", color=GREEN).scale(0.5))
        st3 = rot(Text("V곱", font="Noto Sans KR", color=YELLOW_B).scale(0.5))
        sa1 = rot(Text("→", color=GREY_B).scale(0.5))
        sa2 = rot(Text("→", color=GREY_B).scale(0.5))
        steps = VGroup(st1, sa1, st2, sa2, st3).arrange(RIGHT, buff=0.15)
        steps.next_to(hbm_rect, -_UP, buff=1)
        self.playwl(*[FadeIn(s) for s in steps], lag_ratio=0.15)

        # Place Q, K, V in HBM
        def dbox(label, color):
            r = RoundedRectangle(
                corner_radius=0.08,
                width=0.7,
                height=0.7,
                stroke_width=2,
                fill_color=color,
                fill_opacity=1,
                stroke_color=color,
            )
            t = rot(Text(label, font="Noto Sans KR", color=BLACK).scale(0.3))
            t.move_to(r)
            return VGroup(r, t)

        hc = hbm_rect.get_center()
        sc = sram_rect.get_center()
        q_d = dbox("Q", BLUE).move_to(hc + LEFT * 1.2)
        k_d = dbox("K", TEAL_B).move_to(hc)
        v_d = dbox("V", YELLOW_B).move_to(hc + RIGHT * 1.2)
        self.playwl(*[FadeIn(d) for d in [q_d, k_d, v_d]], lag_ratio=0.2)

        # Transfer helper: HBM → SRAM → HBM round trip
        def transfer(srcs, step_name, step_color, res_name, res_pos, step_mob):
            self.play(Indicate(step_mob, color=step_color), run_time=0.5)

            dir_t = (
                rot(
                    Words("HBM  →  SRAM", font="Noto Sans KR", color=step_color).scale(
                        0.5
                    )
                )
                .next_to(transfer_path, RIGHT, buff=1.5)
                .words
            )
            self.playw(
                VGroup(*srcs).animate.arrange(RIGHT, buff=0.1).move_to(sc),
                FadeIn(dir_t),
                run_time=3,
            )

            comp = rot(
                Text(step_name, font="Noto Sans KR", color=step_color).scale(0.3)
            ).move_to(sc)
            self.play(*[FadeOut(s) for s in srcs], FadeIn(comp), run_time=0.3)

            dir_t2 = (
                rot(
                    Words("HBM  ←  SRAM", font="Noto Sans KR", color=step_color).scale(
                        0.5
                    )
                )
                .next_to(transfer_path, RIGHT, buff=1.5)
                .words
            )

            res = dbox(res_name, step_color).move_to(sc)
            self.play(
                FadeOut(comp),
                FadeIn(res),
                Transform(dir_t, dir_t2),
                run_time=0.3,
            )

            self.playw(res.animate.move_to(res_pos), run_time=3)
            self.play(FadeOut(dir_t), run_time=0.2)
            return res

        # "QK 행렬곱 할 때 HBM → SRAM → HBM"
        s_d = transfer([q_d, k_d], "QK 행렬곱", BLUE, "S", hc + LEFT * 0.6, st1)

        # "softmax할 때 HBM → SRAM → HBM"
        p_d = transfer([s_d], "softmax", GREEN, "P", hc + LEFT * 0.6, st2)

        # "V곱 할 때 HBM → SRAM → HBM"
        o_d = transfer([p_d, v_d], "V곱", YELLOW_B, "O", hc, st3)


class flashAttnIntro(Scene3D):
    def construct(self):
        _IN = IN * np.cos(tilt_degree * DEGREES) + UP * np.sin(tilt_degree * DEGREES)
        self.tilt_camera_vertical(tilt_degree)

        # ── GPU Structure (continuing from gpuStructure) ──
        hbm_rect = RoundedRectangle(
            corner_radius=0.2,
            width=7,
            height=1.6,
            fill_color=BLUE_E,
            fill_opacity=0.15,
            stroke_color=BLUE_B,
            stroke_width=2,
        )
        sram_rect = RoundedRectangle(
            corner_radius=0.15,
            width=3,
            height=1.2,
            fill_color=GREEN_E,
            fill_opacity=0.15,
            stroke_color=GREEN,
            stroke_width=2,
        )
        VGroup(hbm_rect, sram_rect).arrange(_UP, buff=1.5).shift(_UP)

        hbm_title = rot(Text("HBM", font="Noto Sans KR", color=BLUE_B).scale(0.55))
        sram_title = rot(Text("SRAM", font="Noto Sans KR", color=GREEN).scale(0.55))
        hbm_title.next_to(hbm_rect, _UP, buff=0.1).align_to(hbm_rect, LEFT)
        sram_title.next_to(sram_rect, _UP, buff=0.1).align_to(sram_rect, LEFT)

        transfer_path = DashedLine(
            hbm_rect.get_center() + _UP * 0.6,
            sram_rect.get_center() - _UP * 0.4,
            color=YELLOW_B,
            stroke_width=2,
            dash_length=0.15,
        )

        hc = hbm_rect.get_center()
        sc = sram_rect.get_center()

        def dbox(label, color, w=0.7):
            r = RoundedRectangle(
                corner_radius=0.08,
                width=w,
                height=0.7,
                stroke_width=2,
                fill_color=color,
                fill_opacity=1,
                stroke_color=color,
            )
            t = rot(Text(label, font="Noto Sans KR", color=BLACK).scale(0.3))
            t.move_to(r)
            return VGroup(r, t)

        # Add GPU structure (assumed from previous scene)
        self.add(hbm_rect, hbm_title, sram_rect, sram_title, transfer_path)

        # ── 1. "이 때 Flash Attention의 핵심 아이디어는요" ──
        fa_title = rot(
            Words("Flash Attention", font="Noto Sans KR", color=YELLOW_B).scale(0.5)
        ).next_to(hbm_rect, -_UP, buff=1)
        self.playwl(*[FadeIn(item) for item in fa_title.words], lag_ratio=0.3)

        # ── 2. "이 왕복 횟수를 줄이는 겁니다" ──
        idea = rot(
            Text("왕복 횟수 ↓", font="Noto Sans KR", color=GREEN).scale(0.4)
        ).next_to(fa_title, RIGHT, buff=0.3)
        self.playw(FadeIn(idea, shift=RIGHT * 0.3))
        # ── 3. "어떻게 줄일까요?" ──
        self.wait()

        # ── 4. "SRAM에 왔을 때" ──
        self.playw(
            RWiggle(VGroup(sram_rect, sram_title), amp=(0.15, 0.15, 0.15)), run_time=2
        )

        # ── 5. "QK 행렬곱부터 V곱까지 다해버립니다" ──
        sram_flow = (
            VGroup(
                rot(Text("QK", color=BLUE).scale(0.4)),
                rot(Text("→ softmax", color=GREEN).scale(0.4)),
                rot(Text("→ V곱", color=YELLOW_B).scale(0.4)),
            )
            .arrange(RIGHT, buff=0.06)
            .move_to(sc)
        )
        self.cf.save_state()
        self.playwl(
            *[FadeIn(s) for s in sram_flow],
            self.cf.animate.shift(_IN * 4 + _UP * 2),
            lag_ratio=0.3,
        )

        # ── 6. "attention을 계산할 때는요" ──
        q_full = dbox("Q", BLUE, w=1.8).move_to(hc + LEFT * 2)
        k_full = dbox("K", TEAL_B, w=1.8).move_to(hc)
        v_full = dbox("V", YELLOW_B, w=1.8).move_to(hc + RIGHT * 2)
        self.playwl(
            Restore(self.cf),
            *[FadeIn(d) for d in [q_full, k_full, v_full]],
            lag_ratio=0.3,
        )

        # ── 7. "Query와 Key를 나눠서" ──
        n = 3
        q_blocks = VGroup(*[dbox(f"Q{chr(8321 + i)}", BLUE, w=0.55) for i in range(n)])
        k_blocks = VGroup(
            *[dbox(f"K{chr(8321 + i)}", TEAL_B, w=0.55) for i in range(n)]
        )
        v_blocks = VGroup(
            *[dbox(f"V{chr(8321 + i)}", YELLOW_B, w=0.55) for i in range(n)]
        )
        q_blocks.arrange(RIGHT, buff=0.06).move_to(q_full)
        k_blocks.arrange(RIGHT, buff=0.06).move_to(k_full)
        v_blocks.arrange(RIGHT, buff=0.06).move_to(v_full)
        self.playw(
            FadeOut(q_full),
            FadeIn(q_blocks),
            FadeOut(k_full),
            FadeIn(k_blocks),
            FadeOut(v_full),
            FadeIn(v_blocks),
            run_time=0.8,
        )

        # ── 8. "SRAM에 올릴 수 있는 크기로" ──
        self.wait()
        # ── 9. "쪼개서 가져옵니다" ──
        ol = self.overlay.shift(DOWN)
        q1 = q_blocks[0].copy().set_z_index(ol.z_index + 1)
        k1 = k_blocks[0].copy().set_z_index(ol.z_index + 1)
        transfer_path.set_z_index(ol.z_index + 1)
        VGroup(sram_rect, sram_title).set_z_index(ol.z_index)
        self.playw(
            FadeIn(ol),
            FadeOut(sram_flow),
            q1.animate.move_to(sc + LEFT * 0.5),
            k1.animate.move_to(sc + RIGHT * 0.5),
            run_time=0.8,
        )

        # ── 10. "그런데 여기서 중요한 건" ──
        # SKIP 1
        self.wait(1)

        # ── 11. "쪼갠 조각에서 QK 결과를 만들고 나서" ──
        qk_res = dbox("S", ORANGE).move_to(sc)
        self.play(FadeOut(q1), FadeOut(k1), run_time=0.3)
        self.playw(FadeIn(qk_res, scale=1.2))

        # ── 12. "그냥 attention은 HBM으로 보내는데요" ──
        normal_lbl = rot(
            Text("일반 Attention", font="Noto Sans KR", color=RED_B).scale(0.35)
        ).next_to(transfer_path, RIGHT, buff=1.5)
        arr = Arrow(
            qk_res.get_bottom(),
            qk_res.get_bottom() - _UP * 0.8,
            color=YELLOW_B,
            stroke_width=2,
            tip_length=0.2,
            buff=0,
        ).shift(RIGHT * 0.2)
        self.playw(FadeIn(normal_lbl), FadeIn(arr), run_time=0.3)

        # ── 13. "Flash attention같은 경우엔 HBM으로 안 보내고요" ──
        cross = rot(Text("✕", color=PURE_RED).scale(0.7)).move_to(arr)
        self.play(FadeIn(cross))
        self.playw(
            FadeOut(arr),
            FadeOut(cross),
            FadeOut(normal_lbl),
            run_time=1,
        )

        # ── 14. "바로 그 자리에서" ──
        self.playw(Indicate(qk_res, color=YELLOW), run_time=0.7, wait=0.3)

        # ── 15. "softmax도 하고 V 곱까지 해서" ──
        sm_res = dbox("P", GREEN).move_to(sc + LEFT * 0.4)
        self.playw(Transform(qk_res, sm_res), run_time=0.7)
        v_copy = v_blocks[0].copy()
        self.playw(v_copy.animate.move_to(sc + RIGHT * 0.4), run_time=0.5)

        # ── 16. "출력까지 만들어버립니다" ──
        output = dbox("O", PURPLE).move_to(sc)
        self.playw(
            FadeOut(qk_res),
            FadeOut(v_copy),
            FadeIn(output, scale=1.2),
            run_time=0.5,
        )
        return


class softmaxIssue(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(tilt_degree)

        # ── introAttention 배치 재현 ──
        qs, ks, vs = [Tensor(seq_len, shape="square") for _ in range(3)]
        attn = VGroup(
            *[
                VGroup(*[Dot(color=random_color()) for _ in range(seq_len)]).arrange(
                    RIGHT, buff=attn_buff
                )
                for _ in range(seq_len)
            ]
        ).arrange(DOWN, buff=attn_buff)

        dummy = Tensor(1).shift(UL * 2)
        qs.arrange(DOWN, buff=0.3).next_to(dummy, DOWN, buff=0.5)
        ks.arrange(RIGHT, buff=0.3).next_to(dummy, RIGHT, buff=0.5)
        attn.next_to(qs, RIGHT, buff=0.65)
        for i in range(seq_len):
            for j in range(seq_len):
                attn[i][j].set_fill(random_color(), opacity=0.7)
        vs.arrange(RIGHT, buff=0.3).next_to(ks, _UP, buff=1).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )

        qt = rot(Text("Query", font="Noto Sans KR").scale(0.4)).next_to(
            qs, DOWN, buff=0.2
        )
        kt = rot(Text("Key", font="Noto Sans KR").scale(0.4)).next_to(
            ks, LEFT, buff=0.2
        )
        vt = rot(Text("Value", font="Noto Sans KR").scale(0.4)).next_to(
            vs, LEFT, buff=0.2
        )

        q = VGroup(qs, qt)
        k = VGroup(ks, kt)
        v = VGroup(vs, vt)

        def sm(target):
            sm_o = (
                Words("softmax(", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, LEFT, buff=0.1)
            )
            sm_c = (
                Words(")", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, RIGHT, buff=0.1)
            )
            return VGroup(sm_o, sm_c)

        sms = VGroup(*[sm(attn[i]) for i in range(seq_len)])

        q.shift(LEFT * 1.5)
        # ── "그런데 여기서 문제가 하나 있는데요" ──
        self.playw(FadeIn(q, k, v, attn, sms))

        # ── "바로 softmax입니다" ──
        self.playw(sms.animate.set_color(RED))

        # ── "softmax는 쪼갠 조각만 가지고는 계산할 수가 없습니다" ──
        self.playw(
            qs[2:].animate.set_opacity(0),
            ks[2:].animate.set_opacity(0),
            vs[2:].animate.set_opacity(0),
            VGroup(*[sms[i] for i in range(2, seq_len)]).animate.set_opacity(0),
            attn[2:].animate.set_opacity(0),
            VGroup(
                *[attn[i][j] for i in range(2) for j in range(2, seq_len)]
            ).animate.set_opacity(0),
        )
        attn2_ = VGroup(*[attn[i][j] for i in range(2) for j in range(2, seq_len)])
        x_mark = rot(Text(X_STRING, color=PURE_RED).scale(0.7)).move_to(attn2_)
        self.playw(FadeIn(x_mark, scale=1.5))

        # ── "왜냐하면 softmax 공식을 보면은요" ──
        softmax_ex = (
            rot(
                RaeTex(
                    r"\text{softmax}(x_i) = {e^{x_i}",
                    r"\over",
                    r" \sum_{j=1}^{N} e^{x_j}}",
                    items=[
                        r"\text{softmax}(x_i)",
                        " = ",
                        denom := r"\sum_{j=1}^{N} e^{x_j}",
                    ],
                )
            )
            .scale(0.7)
            .shift(DOWN * 1.5)
        )
        softmax_ex[denom].set_color(RED)
        ol = self.overlay.scale(1.5)
        softmax_ex.set_z_index(ol.z_index + 1)
        self.playw(FadeIn(softmax_ex, scale=1.2), FadeIn(ol))

        # ── "분모에 전체 key sequence에 대한 attention score exp() 합이 필요하구요" ──
        attn_ = attn[0].copy().set_z_index(ol.z_index + 1).set_opacity(1)
        sms_ = sms[0].copy().set_z_index(ol.z_index + 1).set_opacity(1)
        self.play(FadeIn(attn_), FadeIn(sms_), FadeOut(x_mark))
        self.playw(RWiggle(attn_[2:], amp=(0.1, 0.1, 0.1)), run_time=2)

        # ── "아까 말한 수치 안정성 잡기술 때문에 최댓값을 뺀다고 했죠?" ──
        sm_formula = (
            rot(
                RaeTex(
                    r"\text{softmax}(x_i) = {e^{x_i - m}",
                    r"\over",
                    r" \sum_{j=1}^{N} e^{x_j - m}}",
                    items=[r"\text{softmax}(x_i)", " = ", r"- m}"],
                )
            )
            .scale(0.7)
            .move_to(softmax_ex)
            .set_z_index(ol.z_index + 1)
        )
        sm_formula[r"- m}"].set_color(PURE_GREEN)
        self.playw(
            Transformr(softmax_ex[0], sm_formula[0]),
            Transformr(softmax_ex[1], sm_formula[1]),
            Transformr(softmax_ex[2], sm_formula[2:4]),
            Transformr(softmax_ex[3], sm_formula[4]),
            Transformr(softmax_ex[5], sm_formula[5:]),
        )
        # ── "이 때 전체 key sequence에 대한 attention score의 최댓값도 필요합니다" ──
        self.cf.save_state()
        attn_2 = attn_.copy().set_z_index(ol.z_index + 1)
        meq = rot(
            RaeTex(
                r"m = \max(\quad , \quad , \quad , \quad , \quad , \quad )",
                items=[r"m ", r"=", r" \max("],
            )
            .scale(0.7)
            .set_z_index(ol.z_index + 1)
        ).next_to(sm_formula, RIGHT, buff=0.5)
        meq["m "].set_color(PURE_GREEN)
        self.playw(
            attn_2.animate.arrange(RIGHT, buff=0.34).next_to(
                meq[" \max("], RIGHT, buff=0.1
            ),
            FadeIn(meq),
            self.cf.animate.shift(RIGHT * 1.5),
        )
        # ── "그런데 지금은 key를 쪼개서 일부 조각만 SRAM에 있으니까요" ──
        sram_r = (
            Rectangle(
                width=4,
                height=1.5,
                color=GREEN,
                fill_opacity=0.1,
                stroke_width=2,
            )
            .next_to(attn_, _UP, buff=1.5)
            .shift(RIGHT * 4.5)
            .set_z_index(ol.z_index + 1)
        )
        sram_t = (
            rot(Text("SRAM", font="Noto Sans KR", color=GREEN).scale(0.4))
            .next_to(sram_r, UP, buff=0.3)
            .align_to(sram_r, LEFT)
            .set_z_index(sram_r.z_index + 1)
        )
        sram_s = attn_[:2].copy().set_z_index(sram_r.z_index + 1).set_opacity(1)
        self.playw(
            FadeIn(sram_r, scale=1.2),
            FadeIn(sram_t, scale=1.2),
            sram_s.animate.move_to(sram_r.get_center()),
        )

        # ── "전체 중의 최댓값도 모르고 전체 exp 합도 모릅니다" ──
        self.playw(
            meq.animate.set_color(PURE_RED),
            attn_2[2:].animate.set_color(PURE_RED).shift(_UP * 0.5),
        )
        self.playw(sm_formula[5:].animate.set_color(PURE_RED))
        # ── "이렇게 보면 softmax를 못 할 것 같죠?" ──
        self.playw(RWiggle(sm_formula, amp=(0.1, 0.1, 0.1)), run_time=3)

        # SKIP 1
        self.wait()

        # ── "하지만 이 둘은요 다행히 online으로 업데이트가 가능합니다" ──
        self.play(
            attn_2[2:].animate.shift(_UP * -0.5),
            self.cf.animate.restore().shift(OUT * 3 - _UP * 3),
        )
        self.playwl(
            *[
                AnimationGroup(*[Indicate(attn_[j]) for j in i])
                for i in [range(0, 2), range(0, 4), range(0, 6)]
            ],
            lag_ratio=1,
        )


class maxMdenomL(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(tilt_degree)

        # ── introAttention 배치 재현 ──
        qs, ks, vs = [Tensor(seq_len, shape="square") for _ in range(3)]
        attn = VGroup(
            *[
                VGroup(
                    *[Dot(color=random_bright_color()) for _ in range(seq_len)]
                ).arrange(RIGHT, buff=attn_buff)
                for _ in range(seq_len)
            ]
        ).arrange(DOWN, buff=attn_buff)

        dummy = Tensor(1).shift(UL * 2)
        qs.arrange(DOWN, buff=0.3).next_to(dummy, DOWN, buff=0.5)
        ks.arrange(RIGHT, buff=0.3).next_to(dummy, RIGHT, buff=0.5)
        attn.next_to(qs, RIGHT, buff=0.65)
        for i in range(seq_len):
            for j in range(seq_len):
                attn[i][j].set_fill(random_bright_color(), opacity=0.7)
        vs.arrange(RIGHT, buff=0.3).next_to(ks, _UP, buff=1).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )

        qt = rot(Text("Query", font="Noto Sans KR").scale(0.3)).next_to(
            qs, UP, buff=0.4
        )
        kt = rot(Text("Key", font="Noto Sans KR").scale(0.3)).next_to(
            ks, LEFT, buff=0.2
        )
        vt = rot(Text("Value", font="Noto Sans KR").scale(0.3)).next_to(
            vs, LEFT, buff=0.2
        )

        q = VGroup(qs, qt)
        k = VGroup(ks, kt)
        v = VGroup(vs, vt)

        def sm(target):
            sm_o = (
                Words("softmax(", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, LEFT, buff=0.1)
            )
            sm_c = (
                Words(")", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, RIGHT, buff=0.1)
            )
            return VGroup(sm_o, sm_c)

        sms = VGroup(*[sm(attn[i]) for i in range(seq_len)])

        def mx(target, buff=0.1):
            mx_l = (
                Words("max(", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, LEFT, buff=buff)
            )
            mx_r = (
                Words(")", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, RIGHT, buff=buff)
            )
            return VGroup(mx_l, mx_r)

        q.shift(LEFT * 1.5)

        # ══════════════════════════════════════
        # Section 1: m update
        # ══════════════════════════════════════

        # ── "첫 번째 조각에서 최댓값을 구합니다" ──
        self.cf.save_state()
        self.cf.move_to(IN * 5 + UP * 4 + LEFT * 0.7)
        q[0][1:].set_opacity(0.1)
        k[0][2:].set_opacity(0.1)
        v[0][2:].set_opacity(0.1)
        self.play(FadeIn(q, k, v, attn[0][:2]))
        mx0 = rot(mx(attn[0][:2])).scale(0.9).set_color(GREEN)
        meq = rot(RaeTex(r"m", "=", color=GREEN).scale(0.7)).next_to(
            mx0, LEFT, buff=0.2
        )
        self.play(FadeIn(mx0, meq))
        m = meq[0]

        # ── "그 다음 조각이 오면은요" ──
        self.playw(
            m.animate.next_to(attn[0][:2], -_UP, buff=0.3),
            FadeOut(mx0),
            FadeOut(meq[1]),
            k[0][:2].animate.set_opacity(0.1),
            k[0][2:4].animate.set_opacity(1),
            v[0][:2].animate.set_opacity(0.1),
            v[0][2:4].animate.set_opacity(1),
            attn[0][:2].animate.set_opacity(0.1),
            attn[0][2:4].animate.set_opacity(1),
        )

        # ── "이전 m이랑 새 조각의 m을 비교해서" ──
        m.generate_target().next_to(attn[0][2:4], LEFT, buff=0.15)
        mx1 = (
            rot(mx(VGroup(m.target, attn[0][2:4]), buff=0.2))
            .scale(0.9)
            .set_color(GREEN)
        )
        meq_ = rot(RaeTex(r"m_{\text{new}}", "=", color=GREEN).scale(0.7)).next_to(
            mx1, LEFT, buff=0.2
        )
        self.playw(MoveToTarget(m), FadeIn(mx1, meq_))
        m_ = m.copy().next_to(attn[0][4:6], LEFT, buff=0.15)
        # ── "더 큰 값으로 갱신하면 됩니다" ──
        meq_0 = meq_[0].copy()
        self.play(
            mx1.animate.shift(RIGHT * 1.4),
            attn[0][2:4].animate.set_opacity(0.1),
            attn[0][4:6].animate.set_opacity(1),
            FadeOut(m, shift=RIGHT * 1.3),
            Transform(meq_[0], m_, path_arc=150 * DEGREES),
            meq_[1].animate.shift(RIGHT * 1.3),
            k[0][2:4].animate.set_opacity(0.1),
            k[0][4:6].animate.set_opacity(1),
            v[0][2:4].animate.set_opacity(0.1),
            v[0][4:6].animate.set_opacity(1),
        )
        self.playw(FadeIn(meq_0.shift(RIGHT * 1.3)))

        # ══════════════════════════════════════
        # Section 2: l update
        # ══════════════════════════════════════

        # ── "분모의 전체 exp 합 l도 업데이트합니다" ──
        l_total = rot(
            RaeTex(
                r"\ell",
                "=",
                "e^{x_{0} - m }} + ",
                "e^{x_{1} - m }} + ",
                "e^{x_{2} - m }} + ",
                "e^{x_{3} - m }} + ",
                "e^{x_{4} - m }} + ",
                "e^{x_{5} - m }}",
                items=[" - m ", " + "],
            )
            .scale(0.5)
            .shift(-_UP * 0.7),
        )
        l_total_new = rot(
            RaeTex(
                r"\ell '",
                "=",
                r"e^{x_{0} - m _{:2} }} + ",
                r"e^{x_{1} - m _{:2} }} + ",
                r"e^{x_{2} - m _{:4} }} + ",
                r"e^{x_{3} - m _{:4} }} + ",
                r"e^{x_{4} - m _{:6} }} + ",
                r"e^{x_{5} - m _{:6} }}",
                items=[" - m ", " + "],
            )
            .scale(0.5)
            .move_to(l_total)
            .align_to(l_total, LEFT),
        )
        l_total_new2 = rot(
            RaeTex(
                r"\ell '",
                "=",
                r"e^{x_{0} - m _{:4} }} + ",
                r"e^{x_{1} - m _{:4} }} + ",
                r"e^{x_{2} - m _{:4} }} + ",
                r"e^{x_{3} - m _{:4} }} + ",
                r"e^{x_{4} - m _{:6}}} + ",
                r"e^{x_{5} - m _{:6}}}",
                items=[" - m ", " + "],
            )
            .scale(0.5)
            .move_to(l_total)
            .align_to(l_total, LEFT),
        )
        l_total_new3 = rot(
            RaeTex(
                r"\ell '",
                "=",
                r"e^{x_{0} - m _{:6} }} + ",
                r"e^{x_{1} - m _{:6} }} + ",
                r"e^{x_{2} - m _{:6} }} + ",
                r"e^{x_{3} - m _{:6} }} + ",
                r"e^{x_{4} - m _{:6} }} + ",
                r"e^{x_{5} - m _{:6} }}",
                items=[" - m ", " + "],
            )
            .scale(0.5)
            .move_to(l_total)
            .align_to(l_total, LEFT),
        )
        l_total_new[" - m "].set_color(PURE_RED)
        l_total_new2[" - m "].set_color(PURE_RED)
        l_total_new3[" - m "].set_color(PURE_RED)
        VGroup(
            l_total_new[4],
            l_total_new[8],
            l_total_new[12],
            l_total_new[16],
            l_total_new[20],
            l_total_new[24],
        ).set_color(PURE_RED)
        VGroup(
            l_total_new2[4],
            l_total_new2[8],
            l_total_new2[12],
            l_total_new2[16],
            l_total_new2[20],
            l_total_new2[24],
        ).set_color(PURE_RED)
        VGroup(
            l_total_new3[4],
            l_total_new3[8],
            l_total_new3[12],
            l_total_new3[16],
            l_total_new3[20],
            l_total_new3[24],
        ).set_color(PURE_RED)
        l_total_new[9:].set_opacity(0)
        self.playw(
            FadeIn(l_total),
            FadeOut(meq_0, meq_, mx1),
            self.cf.animate.shift(RIGHT * 0.5),
            k[0][4:6].animate.set_opacity(0.1),
            v[0][4:6].animate.set_opacity(0.1),
            attn[0][4:6].animate.set_opacity(0.1),
            k[0][:2].animate.set_opacity(1),
            v[0][:2].animate.set_opacity(1),
            attn[0][:2].animate.set_opacity(1),
        )
        self.playw(
            l_total[" - m "].animate.set_color(PURE_RED),
        )

        # ── "이전 분모 l에는 이전 최댓값이 묻어있고" ──
        mx_2 = rot(mx(attn[0][:2], buff=0.2).scale(0.9).set_color(GREEN))
        self.play(Transformr(l_total, l_total_new), FadeIn(mx_2))
        a1, a2 = Arrow(
            mx_2[0].get_bottom(),
            l_total[" - m "][0].get_top(),
            stroke_width=2,
            tip_length=0.15,
            color=RED,
        ), Arrow(
            mx_2[0].get_bottom(),
            l_total[" - m "][1].get_top(),
            stroke_width=2,
            tip_length=0.15,
            color=RED,
        )
        self.playw(FadeIn(a1), FadeIn(a2))

        # ── "새 조각의 부분 합에는 새 최댓값이 묻어있어서요" ──
        mx_3 = rot(mx(VGroup(mx_2, attn[0][2:4]), buff=0.2).scale(0.9).set_color(GREEN))
        self.play(
            FadeOut(a1),
            FadeOut(a2),
            FadeIn(mx_3),
            mx_2.animate.set_opacity(0.6),
            k[0][:2].animate.set_opacity(0.1),
            k[0][2:4].animate.set_opacity(1),
            v[0][:2].animate.set_opacity(0.1),
            v[0][2:4].animate.set_opacity(1),
            attn[0][:2].animate.set_opacity(0.1),
            attn[0][2:4].animate.set_opacity(1),
            l_total_new[9:17].animate.set_opacity(1),
        )
        a1, a2 = Arrow(
            mx_3[0].get_bottom(),
            l_total_new[" - m "][2].get_corner(UR),
            stroke_width=2,
            tip_length=0.15,
            color=RED,
        ), Arrow(
            mx_3[0].get_bottom(),
            l_total_new[" - m "][3].get_corner(UR),
            stroke_width=2,
            tip_length=0.15,
            color=RED,
        )
        self.playw(FadeIn(a1), FadeIn(a2))

        # ── "최댓값 차이를 보정해서" ──
        coeff1 = rot(MathTex(r"\times { e^{ - m_{:4} } \over e^{ - m_{:2} } }")).scale(
            0.6
        )

        def parenthesis(target, buff=0.1):
            p_o = (
                Words("(", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, LEFT, buff=buff)
            )
            p_c = (
                Words(")", font="Noto Sans KR")
                .scale(0.5)
                .next_to(target, RIGHT, buff=buff)
            )
            return VGroup(p_o, p_c)

        p1 = rot(parenthesis(l_total_new[2:9], buff=0.1))
        temp = l_total_new[9:17]
        self.playw(
            l_total_new[:2].animate.shift(LEFT * 0.2),
            temp.animate.shift(RIGHT * 0.2).set_opacity(0.3),
            FadeIn(p1),
            FadeIn(
                coeff1.rotate(-45 * DEGREES)
                .next_to(p1, -_UP, buff=-0.1)
                .shift(RIGHT * 1.4)
            ),
            FadeOut(a1, a2),
        )
        l_total_new2[17:].set_opacity(0)
        self.playw(FadeOut(p1, coeff1), Transformr(l_total_new, l_total_new2))

        # ── "이전 분모와 새 부분 합을 더합니다" ──
        coeff2 = rot(MathTex(r"\times { e^{ - m_{:6} } \over e^{ - m_{:4} } }")).scale(
            0.6
        )

        p2 = rot(parenthesis(l_total_new2[2:17], buff=0.1))
        temp2 = l_total_new2[17:]
        mx_4 = rot(
            mx(
                VGroup(mx_3, attn[0][4:6]),
                buff=0.4,
            )
            .scale(0.9)
            .set_color(GREEN)
        )
        self.playw(
            k[0][2:4].animate.set_opacity(0.1),
            v[0][2:4].animate.set_opacity(0.1),
            k[0][4:6].animate.set_opacity(1),
            v[0][4:6].animate.set_opacity(1),
            attn[0][2:4].animate.set_opacity(0.1),
            attn[0][4:6].animate.set_opacity(1),
            mx_3.animate.set_opacity(0.6),
            mx_2.animate.set_opacity(0.3),
            FadeIn(mx_4),
            q.animate.shift(LEFT * 0.8),
            temp2.animate.set_opacity(1),
        )
        self.play(
            l_total_new2[:2].animate.shift(LEFT * 0.2),
            temp2.animate.shift(RIGHT * 0.2).set_opacity(0.3),
            FadeIn(p2),
            FadeIn(
                coeff2.rotate(-45 * DEGREES)
                .next_to(p2, -_UP, buff=-0.1)
                .shift(RIGHT * 2.4)
            ),
        )
        l_total_new3[0][1].set_opacity(0)
        self.playw(FadeOut(p2, coeff2), Transformr(l_total_new2, l_total_new3))

        self.wait(3)


class flashAttentionOverview(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(tilt_degree)

        # ── introAttention 배치 재현 ──
        qs, ks, vs = [Tensor(seq_len, shape="square") for _ in range(3)]
        attn = VGroup(
            *[
                VGroup(
                    *[Dot(color=random_bright_color()) for _ in range(seq_len)]
                ).arrange(RIGHT, buff=attn_buff)
                for _ in range(seq_len)
            ]
        ).arrange(DOWN, buff=attn_buff)

        dummy = Tensor(1).shift(UL * 2)
        qs.arrange(DOWN, buff=0.3).next_to(dummy, DOWN, buff=0.5)
        ks.arrange(RIGHT, buff=0.3).next_to(dummy, RIGHT, buff=0.5)
        attn.next_to(qs, RIGHT, buff=0.65)
        for i in range(seq_len):
            for j in range(seq_len):
                attn[i][j].set_fill(random_bright_color(), opacity=0.7)
        vs.arrange(RIGHT, buff=0.3).next_to(ks, _UP, buff=1).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )

        qt = rot(Text("Query", font="Noto Sans KR").scale(0.3)).next_to(
            qs, UP, buff=0.4
        )
        kt = rot(Text("Key", font="Noto Sans KR").scale(0.3)).next_to(
            ks, LEFT, buff=0.2
        )
        vt = rot(Text("Value", font="Noto Sans KR").scale(0.3)).next_to(
            vs, LEFT, buff=0.2
        )

        q = VGroup(qs, qt)
        k = VGroup(ks, kt)
        v = VGroup(vs, vt)

        q.shift(LEFT * 1.5)
        VGroup(k, v).shift(_UP * 0.7)

        # ══════════════════════════════════════
        # Section: flash attention overview
        # ══════════════════════════════════════
        self.playw(FadeIn(q, k, v, attn))

        # ── Helpers ──
        chunk = 2
        n_blk = 3
        q_chunk = 1
        qn_blk = 6

        def dbox(label, color, w=0.7):
            r = RoundedRectangle(
                corner_radius=0.08,
                width=w,
                height=0.7,
                stroke_width=2,
                fill_color=color,
                fill_opacity=1,
                stroke_color=color,
            )
            t = rot(Text(label, font="Noto Sans KR", color=BLACK).scale(0.3))
            t.move_to(r)
            return VGroup(r, t)

        def attn_block(qi, kvj):
            return VGroup(
                *[
                    attn[qi * q_chunk + r][kvj * chunk + c]
                    for r in range(q_chunk)
                    for c in range(chunk)
                ]
            )

        def block_rect(target, color=YELLOW, buff=0.06):
            return SurroundingRectangle(
                target, color=color, buff=buff, stroke_width=2, corner_radius=0.05
            )

        # ── Setup: Output tensor + chunk groups ──
        os = Tensor(seq_len, shape="square")
        os.arrange(DOWN, buff=0.3).next_to(attn, RIGHT, buff=0.8)

        q_chunks = [qs[i * q_chunk] for i in range(qn_blk)]
        k_chunks = [VGroup(ks[i * chunk], ks[i * chunk + 1]) for i in range(n_blk)]
        v_chunks = [VGroup(vs[i * chunk], vs[i * chunk + 1]) for i in range(n_blk)]

        # ══════════════════════════════════════
        # Beat 1-2: "여기까지 이해했으면은요 / Flash Attention의 실제 방식은 이해하기 쉽습니다"
        # ══════════════════════════════════════
        self.wait(2)

        # ══════════════════════════════════════
        # Beat 3: "먼저 Query와 Key-Value를 SRAM에 올릴 수 있는 크기로 쪼갭니다"
        # ══════════════════════════════════════
        q_rects = VGroup(
            *[
                SurroundingRectangle(
                    q_chunks[i], color=BLUE, buff=0.1, stroke_width=1.5
                )
                for i in range(qn_blk)
            ]
        )
        k_rects = VGroup(
            *[
                SurroundingRectangle(
                    k_chunks[i], color=TEAL_B, buff=0.1, stroke_width=1.5
                )
                for i in range(n_blk)
            ]
        )
        v_rects = VGroup(
            *[
                SurroundingRectangle(
                    v_chunks[i], color=YELLOW_B, buff=0.15, stroke_width=1.5
                ).rotate(tilt_degree * DEGREES, axis=RIGHT)
                for i in range(n_blk)
            ]
        )
        q_labels = VGroup(
            *[
                rot(
                    Text(f"Q{chr(8321 + i)}", font="Noto Sans KR", color=BLUE).scale(
                        0.3
                    )
                ).next_to(q_rects[i], LEFT, buff=0.1)
                for i in range(qn_blk)
            ]
        )
        kv_labels = VGroup(
            *[
                rot(
                    Text(f"KV{chr(8321 + i)}", font="Noto Sans KR", color=TEAL_B).scale(
                        0.3
                    )
                ).next_to(k_rects[i], DOWN, buff=0.2)
                for i in range(n_blk)
            ]
        )

        self.playwl(
            *[FadeIn(r) for r in q_rects],
            *[FadeIn(r) for r in k_rects],
            *[FadeIn(r) for r in v_rects],
            FadeIn(q_labels),
            FadeIn(kv_labels),
            lag_ratio=0.1,
        )

        # ══════════════════════════════════════
        # Beat 4-5: "그리고 이중 반복을 돌리는데요 / 이 안에서 아까의 online 업데이트를 수행합니다"
        # ══════════════════════════════════════
        loop_outer = rot(
            Text("for Qᵢ :", font="Noto Sans KR", color=BLUE).scale(0.4)
        ).next_to(attn[0], LEFT)
        loop_inner = rot(
            Text("for KVⱼ :", font="Noto Sans KR", color=TEAL_B).scale(0.35)
        ).next_to(attn[0][:2], _UP, buff=0.2)

        self.playw(FadeIn(loop_outer))
        self.playw(FadeIn(loop_inner))
        self.playwl(
            *[
                AnimationGroup(
                    Indicate(k_rects[j], color=TEAL_B, scale_factor=1.15),
                    Indicate(v_rects[j], color=YELLOW_B, scale_factor=1.15),
                )
                for j in range(n_blk)
            ],
            lag_ratio=0.3,
        )

        # ══════════════════════════════════════
        # Beat 6-7: "내부 반복을 online으로 업데이트하면은요 / query 조각 하나가 완성됩니다"
        # ══════════════════════════════════════
        # Conceptual preview: quick flash through Q₁'s inner loop
        self.play(Indicate(q_rects[0], color=YELLOW, scale_factor=1.15), run_time=0.7)
        for j in range(n_blk):
            self.play(
                Indicate(attn_block(0, j), color=YELLOW, scale_factor=1.2),
                loop_inner.animate.next_to(attn[0][j * chunk: (j + 1) * chunk], _UP, buff=0.2),
                run_time=0.4,
            )
        # Brief flash showing "one chunk done"
        done_check = rot(Text(CHECK_STRING, color=GREEN).scale(0.5)).next_to(
            q_rects[0], RIGHT, buff=0.15
        )
        self.play(FadeIn(done_check, scale=1.5), run_time=0.4)
        self.playw(FadeOut(done_check), run_time=0.3)

        # ══════════════════════════════════════
        # Beat 8: "바깥 반복은 Query 조각을 순서대로 순회하고요"
        # ══════════════════════════════════════
        for i in range(qn_blk):
            self.play(
                Indicate(q_rects[i], color=YELLOW, scale_factor=1.15),
                loop_outer.animate.next_to(attn[i], LEFT, buff=0.2),
                run_time=0.5,
            )
        self.wait()

        # ══════════════════════════════════════
        # Beat 9: "안쪽 반복은 Key-Value 조각을 순서대로 순회합니다"
        # ══════════════════════════════════════
        for j in range(n_blk):
            self.play(
                Indicate(k_rects[j], color=YELLOW, scale_factor=1.15),
                Indicate(v_rects[j], color=YELLOW, scale_factor=1.15),
                loop_inner.animate.next_to(attn[0][j * chunk: (j + 1) * chunk], _UP, buff=0.2),
                run_time=1.2,
            )
        self.wait()

        # ══════════════════════════════════════
        # Beat 10-12: "안 쪽 반복을 보면 / 먼저 Query 조각 하나를 잡고요 / Key-Value 조각을 순회합니다"
        # ══════════════════════════════════════
        # Dim non-Q₁ elements
        self.play(
            *[q_chunks[i].animate.set_opacity(0.15) for i in range(1, qn_blk)],
            *[q_rects[i].animate.set_opacity(0.15).set_fill(opacity=0) for i in range(1, qn_blk)],
            *[q_labels[i].animate.set_opacity(0.15) for i in range(1, qn_blk)],
            q_rects[0].animate.set_color(YELLOW),
            *[attn[i].animate.set_opacity(0.15) for i in range(q_chunk, seq_len)],
            FadeOut(loop_outer, loop_inner),
        )

        # Iterate through KV chunks, highlighting attention blocks
        prev_br = None
        for j in range(n_blk):
            block = attn_block(0, j)
            br = block_rect(block)
            anims = [FadeIn(br), block.animate.set_opacity(1)]
            if prev_br:
                anims.append(FadeOut(prev_br))
            # Toggle KV chunk opacity
            for jj in range(n_blk):
                if jj == j:
                    anims.extend(
                        [
                            k_chunks[jj].animate.set_opacity(1),
                            v_chunks[jj].animate.set_opacity(1),
                        ]
                    )
                else:
                    anims.extend(
                        [
                            k_chunks[jj].animate.set_opacity(0.15),
                            v_chunks[jj].animate.set_opacity(0.15),
                        ]
                    )
            self.playw(*anims, run_time=0.7)
            prev_br = br
        self.play(FadeOut(prev_br), run_time=0.3)

        # ══════════════════════════════════════
        # Beat 13-15: "이 조각만으로는 전체 최댓값이나 / 전체 exp 합 / 아까 못 구한다고 했죠?"
        # ══════════════════════════════════════
        # Show only Q₁×KV₁ block
        br_01 = block_rect(attn_block(0, 0))
        self.play(
            FadeIn(br_01),
            k_chunks[0].animate.set_opacity(1),
            v_chunks[0].animate.set_opacity(1),
            *[k_chunks[i].animate.set_opacity(0.15) for i in range(1, n_blk)],
            *[v_chunks[i].animate.set_opacity(0.15) for i in range(1, n_blk)],
            *[attn_block(0, j).animate.set_opacity(0.15) for j in range(1, n_blk)],
        )

        # m and l labels with "?" marks
        m_label = dbox("m", GREEN, w=0.5).scale(0.8).next_to(attn[0], RIGHT, buff=0.5)
        l_label = dbox("l", ORANGE, w=0.5).scale(0.8).next_to(m_label, RIGHT, buff=0.3)
        q_mark_m = rot(Text("?", font="Noto Sans KR", color=RED).scale(0.5)).next_to(
            m_label, _UP, buff=0.15
        )
        q_mark_l = rot(Text("?", font="Noto Sans KR", color=RED).scale(0.5)).next_to(
            l_label, _UP, buff=0.15
        )

        self.playw(FadeIn(m_label), FadeIn(l_label))
        self.playw(FadeIn(q_mark_m, scale=1.5), FadeIn(q_mark_l, scale=1.5))

        # ══════════════════════════════════════
        # Beat 16-17: "아까의 online 업데이트로 / 조각마다 누적해서 m과 l과 O를 계산합니다"
        # ══════════════════════════════════════
        o_label = dbox("O", PURPLE, w=0.7).scale(0.8).next_to(l_label, RIGHT, buff=0.3)
        self.play(
            FadeOut(q_mark_m),
            FadeOut(q_mark_l),
            FadeOut(br_01),
            FadeIn(o_label),
        )

        # Full inner loop for Q₁: cycle through KV chunks with m, l, O pulse
        for j in range(n_blk):
            block = attn_block(0, j)
            br = block_rect(block)
            self.play(
                FadeIn(br),
                block.animate.set_opacity(1),
                k_chunks[j].animate.set_opacity(1),
                v_chunks[j].animate.set_opacity(1),
                *[
                    k_chunks[jj].animate.set_opacity(0.15)
                    for jj in range(n_blk)
                    if jj != j
                ],
                *[
                    v_chunks[jj].animate.set_opacity(0.15)
                    for jj in range(n_blk)
                    if jj != j
                ],
                run_time=0.5,
            )
            # Pulse m, l, O
            self.play(
                Indicate(m_label, color=GREEN, scale_factor=1.3),
                Indicate(l_label, color=ORANGE, scale_factor=1.3),
                Indicate(o_label, color=PURPLE, scale_factor=1.3),
                run_time=0.7,
            )
            self.play(FadeOut(br), run_time=0.2)

        # ══════════════════════════════════════
        # Beat 18-19: "이 때 안쪽 반복이 끝나면 / 이 O가 이번 Query 조각에 대한 attention 출력입니다"
        # ══════════════════════════════════════
        self.playwl(
            FadeOut(m_label, l_label),
            AnimationGroup(o_label[0].animate.rotate(tilt_degree*DEGREES, axis=RIGHT).next_to(attn[0], RIGHT, buff=0.5),
            o_label[1].animate.move_to(o_label[0].target)),
            lag_ratio=0.5
        )

        # ══════════════════════════════════════
        # Beat 20-22: "이걸 전체 query에 대해서 반복하면 / O가 완성됩니다"
        # ══════════════════════════════════════
        # Restore all opacities first
        self.play(
            *[q_chunks[i].animate.set_opacity(1) for i in range(qn_blk)],
            *[q_rects[i].animate.set_opacity(1).set_fill(opacity=0) for i in range(qn_blk)],
            *[q_labels[i].animate.set_opacity(1) for i in range(qn_blk)],
            q_rects[0].animate.set_color(BLUE),
            *[k_chunks[i].animate.set_opacity(1) for i in range(n_blk)],
            *[v_chunks[i].animate.set_opacity(1) for i in range(n_blk)],
            *[attn[i].animate.set_opacity(1) for i in range(seq_len)],
        )
        o_labels = [o_label]
        o_label[0].set_stroke(width=2, color=BLACK)
        for i in range(1, qn_blk):
            oi_label = o_label.copy().next_to(attn[i], RIGHT, buff=0.5)
            oi_label[0].set_stroke(width=2, color=BLACK).set_fill(color=random_color())
            oi_label[1].set_color(invert_color(oi_label[0].get_fill_color()))
            o_labels.append(oi_label)
        self.playw(FadeIn(VGroup(*o_labels[1:])))
        return


        # Abbreviated Q₂ and Q₃ inner loops
        for qi in range(1, n_blk):
            # Highlight current Q chunk
            self.play(
                *[
                    q_rects[i].animate.set_color(YELLOW if i == qi else BLUE)
                    for i in range(n_blk)
                ],
                *[
                    q_chunks[i].animate.set_opacity(1 if i == qi else 0.15)
                    for i in range(n_blk)
                ],
                *[
                    q_rects[i].animate.set_opacity(1 if i == qi else 0.15)
                    for i in range(n_blk)
                ],
                *[
                    q_labels[i].animate.set_opacity(1 if i == qi else 0.15)
                    for i in range(n_blk)
                ],
                *[
                    attn[r].animate.set_opacity(
                        1 if qi * chunk <= r < (qi + 1) * chunk else 0.15
                    )
                    for r in range(seq_len)
                ],
                run_time=0.5,
            )
            # Quick flash through KV blocks
            for j in range(n_blk):
                block = attn_block(qi, j)
                br = block_rect(block)
                self.play(
                    FadeIn(br),
                    block.animate.set_opacity(1),
                    run_time=0.3,
                )
                self.play(FadeOut(br), run_time=0.15)
            # Output chunk fills in
            oi_chunk = VGroup(*[os[qi * chunk + r] for r in range(chunk)])
            self.playw(FadeIn(oi_chunk, scale=1.2), run_time=0.5)

        # Restore everything and show final O
        self.play(
            *[q_chunks[i].animate.set_opacity(1) for i in range(qn_blk)],
            *[q_rects[i].animate.set_opacity(1) for i in range(qn_blk)],
            *[q_labels[i].animate.set_opacity(1) for i in range(qn_blk)],
            *[q_rects[i].animate.set_color(BLUE) for i in range(n_blk)],
            *[k_chunks[i].animate.set_opacity(1) for i in range(n_blk)],
            *[v_chunks[i].animate.set_opacity(1) for i in range(n_blk)],
            *[attn[i].animate.set_opacity(1) for i in range(seq_len)],
        )
        self.playw(Indicate(VGroup(os, ot), color=PURPLE, scale_factor=1.1))
