from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class introAttention(Scene3D):
    def construct(self):
        tilt_degree = 60
        _UP = OUT * np.cos(tilt_degree * DEGREES) + UP * np.sin(tilt_degree * DEGREES)
        self.tilt_camera_vertical(tilt_degree)
        seq_len = 6
        qs, ks, vs = [Tensor(seq_len, shape="square") for _ in range(3)]
        os = Tensor(seq_len, shape="square")
        attn_buff = 0.54
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
            .shift(DOWN*3)
        )
        ol = self.overlay.scale(2).align_to(ot, DOWN)
        ps.set_z_index(ol.z_index + 1)
        self.playwl(FadeIn(ol), *[FadeIn(item) for item in ps], lag_ratio=0.4)

        self.play(Flash(p2.get_corner(UL), color=GREEN), run_time=0.7)
        self.playw(RWiggle(p2, amp=(0.1, 0.1, 0.1)), run_time=2)
        self.playw(FadeOut(qkvo))

