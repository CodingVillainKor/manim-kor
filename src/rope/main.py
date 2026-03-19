from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class sinusoidal(Scene2D):
    def construct(self):
        wv = Tensor(12, shape="circle", arrange=RIGHT, buff=0.3)
        pv = Tensor(12, shape="square", arrange=RIGHT, buff=0.3)
        VGroup(wv, pv).arrange(UP, buff=1)
        wt = Text("Words", font="Noto Sans KR").scale(0.5).next_to(wv, LEFT)
        pt = Text("Positions", font="Noto Sans KR").scale(0.5).next_to(pv, LEFT)
        ps = VGroup(
            *[
                Text("+", font="Noto Sans KR").scale(0.5).next_to(wv[i], UP, buff=0.4)
                for i in range(12)
            ]
        )

        self.playw(FadeIn(wv, pv))
        self.play(FadeIn(wt), run_time=0.5)
        self.play(FadeIn(pt), run_time=0.5)
        self.playw(FadeIn(ps))

        qt = MathTex("W_q").scale(0.6).set_z_index(1)
        qb = (
            Rectangle(width=4, height=qt.height + 0.4, color=GREY_B)
            .move_to(qt)
            .set_fill(BLACK, opacity=0.7)
        ).set_z_index(0.5)
        q = VGroup(qt, qb)
        kt = MathTex("W_k").scale(0.6).set_z_index(1)
        kb = (
            Rectangle(width=4, height=kt.height + 0.4, color=GREY_B)
            .move_to(kt)
            .set_fill(BLACK, opacity=0.7)
        ).set_z_index(0.5)
        k = VGroup(kt, kb)

        VGroup(q, k).arrange(RIGHT, buff=0.5).next_to(pv, UP, buff=1.0)
        self.playw(FadeIn(q, k))

        pwv = VGroup(
            RoundedRectangle(
                corner_radius=0.1,
                width=pv[0].width,
                height=pv[0].height,
                stroke_width=2,
                color=GREY_B,
            )
            .move_to(pv[i])
            .set_fill(random_color(), opacity=1)
            for i in range(12)
        )
        pwt = (
            Words("Words with Position", font="Noto Sans KR")
            .scale(0.4)
            .next_to(pwv, LEFT, buff=0.4)
        )
        self.playwl(
            AnimationGroup(
                FadeOut(ps, target_position=pv),
                FadeOut(wv, target_position=pv),
                FadeOut(wt, target_position=pt),
            ),
            AnimationGroup(Transformr(pv, pwv), FadeOut(pt), FadeIn(pwt)),
            lag_ratio=0.3,
            wait=0,
        )

        pwvq = pwv.copy()
        pwvk = pwv.copy()
        pwvq.generate_target().scale(0.5).arrange(RIGHT, buff=0.1)
        pwvk.generate_target().scale(0.5).arrange(RIGHT, buff=0.1)
        pwvq.target.next_to(q, DOWN, buff=0.5)
        pwvk.target.next_to(k, DOWN, buff=0.5)
        self.play(
            MoveToTarget(pwvq),
            MoveToTarget(pwvk),
        )
        pwvq.generate_target().next_to(q, UP, buff=0.5)
        pwvk.generate_target().next_to(k, UP, buff=0.5)
        for i in range(12):
            pwvq.target[i].set_fill(random_color(), opacity=1)
            pwvk.target[i].set_fill(random_color(), opacity=1)
        self.playw(
            MoveToTarget(pwvq),
            MoveToTarget(pwvk),
            self.cf.animate.shift(UP * 3),
            FadeOut(pwt, pwv),
        )
        pwvq.generate_target()
        pwvk.generate_target().move_to(ORIGIN).align_to(pwvk, UP)

        dummy = pwvq[0].copy().next_to(pwvk.target, LEFT)
        pwvq.target.arrange(UP, buff=0.1).next_to(dummy, UP, buff=0.1)
        self.playw(
            MoveToTarget(pwvq),
            MoveToTarget(pwvk),
            FadeOut(q, k),
            self.cf.animate.shift(UP * 1.5),
        )
        self.playw(VGroup(pwvq, pwvk).animate.set_color(PURE_RED))

        def get_pet(i):
            color1 = BLUE_C
            color2 = GREEN_C
            return (
                MathTex(r"\mathrm{PE}_{%d}" % i)
                .scale(0.6)
                .set_z_index(1)
                .set_color(interpolate_color(color1, color2, i / num_pe))
            )

        self.play(
            FadeOut(pwvq, shift=LEFT),
            FadeOut(pwvk, shift=DOWN),
        )
        dummy.shift(LEFT * 3 + DOWN)
        num_pe = 12
        petk = (
            VGroup(get_pet(i).set_z_index(1) for i in range(num_pe))
            .arrange(RIGHT, buff=0.4)
            .next_to(dummy, RIGHT, buff=0.5)
        )
        petq = (
            VGroup(get_pet(i).set_z_index(1) for i in range(num_pe))
            .arrange(UP, buff=0.5)
            .next_to(dummy, UP, buff=0.5)
        )
        self.playw(
            FadeIn(petq, shift=RIGHT),
            FadeIn(petk, shift=UP),
        )

        pe_prods = VGroup(
            *[
                VGroup(
                    *[
                        MathTex(
                            r"\mathrm{PE}_{%d}" % i, r"\cdot", r"\mathrm{PE}_{%d}" % j
                        )
                        .scale(0.3)
                        .move_to([petk[j].get_x(), petq[i].get_y(), 0])
                        for j in range(num_pe)
                    ]
                )
                for i in range(num_pe)
            ]
        )
        anims = []
        for i in range(num_pe):
            for j in range(num_pe):
                anims.append(
                    Transformr(
                        VGroup(
                            petq[i].copy().set_z_index(1), petk[j].copy().set_z_index(1)
                        ),
                        pe_prods[i][j],
                    )
                )
        self.playw(*anims)
        pe_prods.generate_target().set_opacity(0.2)

        pe_prods.target[3][5].set_opacity(1)
        pe_prods.target[7][9].set_opacity(1)
        pep35 = pe_prods[3][5]
        pep79 = pe_prods[7][9]

        self.play(VGroup(petk, petq).animate.set_opacity(0.2), MoveToTarget(pe_prods))
        self.playw(
            VGroup(pep35, pep79)
            .animate.arrange(RIGHT, buff=0.5)
            .scale(3)
            .move_to(self.cf)
        )

        sig35 = (
            RaeTex(
                r"\displaystyle \sum_{i=0}^{\mathrm{dim}/2} \frac{ \cos( 3 - 5 ) }{10000^{2i}}",
                items=[r"\cos( 3 - 5 )"],
            )
            .scale(0.6)
            .next_to(pep35, DOWN)
        )
        sig35[r"\cos( 3 - 5 )"].set_color(GREEN)
        sig79 = (
            RaeTex(
                r"\displaystyle \sum_{i=0}^{\mathrm{dim}/2} \frac{ \cos( 7 - 9 ) }{10000^{2i}}",
                items=[r"\cos( 7 - 9 )"],
            )
            .scale(0.6)
            .next_to(pep79, DOWN)
        )
        sig79[r"\cos( 7 - 9 )"].set_color(GREEN)
        self.playw(FadeIn(sig35, sig79, shift=DOWN * 0.5))

        eq = Text("=").scale(0.6).move_to(self.cf)
        self.playw(FadeIn(eq))

        self.wait(2)

        self.playwl(
            Flash(sig35[r"\cos( 3 - 5 ))"].get_corner(UL)),
            Flash(sig79[r"\cos( 7 - 9 ))"].get_corner(UL)),
            lag_ratio=0.3,
        )

        wpe35 = (
            RaeTex(
                r"( \mathrm{seq}_3 + \mathrm{PE}_3 ) \cdot ( \mathrm{seq}_5 + \mathrm{PE}_5 )",
                items=[
                    r"\mathrm{PE}_3",
                    r"\cdot",
                    r"\mathrm{PE}_5",
                    r"( \mathrm{seq}_3 +",
                    r"( \mathrm{seq}_5 +",
                    ")",
                ],
            )
            .scale(0.75)
            .move_to(pep35)
            .align_to(pep35, RIGHT)
        )
        wpe79 = (
            RaeTex(
                r"( \mathrm{seq}_7 + \mathrm{PE}_7 ) \cdot ( \mathrm{seq}_9 + \mathrm{PE}_9 )",
                items=[
                    r"\mathrm{PE}_7",
                    r"\cdot",
                    r"\mathrm{PE}_9",
                    r"( \mathrm{seq}_7 +",
                    r"( \mathrm{seq}_9 +",
                    ")",
                ],
            )
            .scale(0.75)
            .move_to(pep79)
            .align_to(pep79, LEFT)
        )
        self.playwl(
            AnimationGroup(
                Transformr(pep35[0], wpe35[r"\mathrm{PE}_3"]),
                Transformr(pep35[1], wpe35[r"\cdot"]),
                Transformr(pep35[2], wpe35[r"\mathrm{PE}_5"]),
                Transformr(pep79[0], wpe79[r"\mathrm{PE}_7"]),
                Transformr(pep79[1], wpe79[r"\cdot"]),
                Transformr(pep79[2], wpe79[r"\mathrm{PE}_9"]),
            ),
            FadeOut(eq, sig35, sig79),
            AnimationGroup(
                FadeIn(
                    wpe35[r"( \mathrm{seq}_3 +"],
                    wpe35[r"( \mathrm{seq}_5 +"],
                    wpe35[r")"],
                    wpe79[r"( \mathrm{seq}_7 +"],
                    wpe79[r"( \mathrm{seq}_9 +"],
                    wpe79[r")"],
                )
            ),
            lag_ratio=0.5,
        )

        self.playw(VGroup(wpe35, wpe79).animate.set_color(PURE_RED))


class ropeintro(Scene3D):
    def construct(self):
        dummy = Tensor(1, shape="square").set_opacity(0).shift(DOWN * 2 + LEFT * 2.7)
        q = (
            VGroup(
                *[
                    RoundedRectangle(
                        corner_radius=0.05, width=0.3, height=0.3, stroke_width=2
                    ).set_fill(random_color(), opacity=1)
                    for _ in range(10)
                ]
            )
            .arrange(UP, buff=0.15)
            .next_to(dummy, UP, buff=0.5)
        )
        qt = Text("Query", font="Noto Sans KR").scale(0.4).next_to(q, LEFT, buff=0.3)
        k = (
            VGroup(
                *[
                    RoundedRectangle(
                        corner_radius=0.05, width=0.3, height=0.3, stroke_width=2
                    ).set_fill(random_color(), opacity=1)
                    for _ in range(10)
                ]
            )
            .arrange(RIGHT, buff=0.15)
            .next_to(dummy, RIGHT, buff=0.5)
        )
        kt = Text("Key", font="Noto Sans KR").scale(0.4).next_to(k, DOWN, buff=0.2)
        self.play(FadeIn(q), FadeIn(k))
        self.playw(FadeIn(qt), FadeIn(kt))

        anims = []
        theta = PI / 30
        for i in range(10):
            anims.append(Rotate(q[i], angle=theta * i))
            anims.append(Rotate(k[i], angle=-theta * i))
        self.playw(*anims, run_time=1.5)

        v = q[0].copy()
        self.add(v)
        self.play(FadeOut(q, k, qt, kt))
        self.playw(v.animate.move_to(ORIGIN))

        vv = (
            randn(16, 1, element_to_mobject_config={"num_decimal_places": 2})
            .scale(0.5)
            .shift(UP * 0.5)
        )
        self.playw(Transformr(v, vv))

        boxes = VGroup(
            *[
                DashedVMobject(
                    SurroundingRectangle(
                        vv[0][i : i + 2], buff=0.05, stroke_width=2, color=YELLOW
                    ),
                    num_dashes=40,
                    dashed_ratio=0.7,
                )
                for i in range(0, 16, 2)
            ]
        )
        self.playwl(*[FadeIn(box) for box in boxes], lag_ratio=0.1)

        self.playw_return(boxes.animate.set_stroke(opacity=0))

        self.wait()

        num_plane = 8
        items = VGroup(boxes, vv)
        items.generate_target().shift(LEFT * 5).rotate(PI / 4, axis=UP)
        planes = (
            VGroup(
                *[
                    RaenimPlane(
                        x_range=(-0.7, 0.7, 1), y_range=(-0.7, 0.7, 1)
                    ).set_color(GREY_C)
                    for i in range(num_plane)
                ]
            )
            .arrange(RIGHT, buff=0.5)
            .next_to(items.target, RIGHT, buff=1)
        )
        vals = [vv._val[i : i + 2] for i in range(0, 16, 2)]
        arrs = VGroup(
            *[
                Arrow(
                    planes[i].c2p(0, 0),
                    planes[i].c2p(val[0][0], val[1][0]),
                    buff=0,
                    color=YELLOW,
                    stroke_width=3,
                    tip_length=0.1,
                )
                for i, val in enumerate(vals[:num_plane])
            ]
        )
        self.playwl(MoveToTarget(items), FadeIn(planes), lag_ratio=0.5, wait=0)
        boxesc = boxes.copy()
        self.playw(Transformr(boxesc, arrs))

        def vals_plus_theta(t):
            wis = [t / (10000 ** (2 * i / 16)) for i in range(num_plane)]
            w_r = np.array(
                [
                    [
                        [np.cos(wis[i]), -np.sin(wis[i])],
                        [np.sin(wis[i]), np.cos(wis[i])],
                    ]
                    for i in range(num_plane)
                ]
            )
            shift_vals = [w_r[i] @ vals[i] for i in range(num_plane)]
            return shift_vals

        def vv_theta(integer=ValueTracker(0)):
            shift_vals = vals_plus_theta(integer.get_value())
            new_vv = (
                DecimalMatrix(
                    [val for pair in shift_vals for val in pair],
                    element_to_mobject_config={"num_decimal_places": 2},
                )
                .scale(0.5)
                .shift(UP * 0.5)
                .shift(LEFT * 5)
                .rotate(PI / 4, axis=UP)
            )
            integer.increment_value(1)
            return new_vv

        def arr_theta(integer=ValueTracker(0)):
            shift_vals = vals_plus_theta(integer.get_value())
            new_arrs = VGroup(
                *[
                    Arrow(
                        planes[i].c2p(0, 0),
                        planes[i].c2p(val[0][0], val[1][0]),
                        buff=0,
                        color=YELLOW,
                        stroke_width=3,
                        tip_length=0.1,
                    )
                    for i, val in enumerate(shift_vals[:num_plane])
                ]
            )
            integer.increment_value(1)
            return new_arrs

        vv.add_updater(vv_fn := lambda m, dt: m.become(vv_theta()))
        arrs.add_updater(arrs_fn := lambda m, dt: m.become(arr_theta()))
        self.playw(Dot().set_opacity(0).animate.shift(RIGHT), run_time=5)

        vels = VGroup(
            MathTex(f"\\theta_{{{i}}}(x)", "=", f"\\omega_{{{i}}}", r"x")
            .scale(0.6)
            .next_to(planes[i], DOWN if i % 2 == 0 else UP, buff=0.3)
            for i in range(num_plane)
        )
        for vel in vels:
            vel[2].set_color(PURE_MAGENTA)
        self.playwl(*[FadeIn(vel) for vel in vels], lag_ratio=0.4)

        def get_omegai(i):
            return (
                MathTex(
                    f"\\omega_{{{i}}} = ", r"1" if i == 0 else f"10000^{{-{2*i}/16}}"
                )
                .scale(0.5)
                .set_color(PURPLE_B)
            )

        omegais = VGroup(
            *[
                get_omegai(i).next_to(vels[i], DOWN if i % 2 == 0 else UP, buff=0.3)
                for i in range(num_plane)
            ]
        )
        self.play(FadeIn(omegais[0]))
        self.play(FadeIn(omegais[1]))
        self.playw(FadeIn(omegais[2]))
        self.playwl(*[FadeIn(item) for item in omegais[3:]], lag_ratio=0.3)


class ropeimplementation(Scene3D):
    def construct(self):
        num_query = 9
        w_r = (
            MobjectMatrix(
                [
                    [MathTex(r"cos(m\theta_i)"), MathTex(r"-sin(m\theta_i)")],
                    [MathTex(r"sin(m\theta_i)"), MathTex(r"cos(m\theta_i)")],
                ],
                h_buff=2.7,
                v_buff=1.0,
            )
            .set_color(PURPLE_A)
            .scale(0.8)
            .set_z_index(3)
        )
        self.playw(FadeIn(w_r))

        query = (
            VGroup(
                *[
                    RoundedRectangle(
                        corner_radius=0.05, width=0.3, height=0.3, stroke_width=1.5
                    ).set_fill(random_color(), opacity=1)
                    for _ in range(num_query)
                ]
            )
            .arrange(RIGHT, buff=0.7)
            .scale(1.3)
            .shift(RIGHT * 0.5)
        )

        qt = (
            Text("Query", font="Noto Sans KR").scale(0.5).next_to(query, LEFT, buff=0.5)
        )
        self.play(w_r.animate.shift(UL * 2 + RIGHT * 0.9 + UP * 0.8).scale(0.5))
        self.playw(FadeIn(query), FadeIn(qt))

        qv = VGroup(
            *[
                randn(16, 1)
                .scale(0.5)
                .move_to(query[i].get_center())
                .set_z_index(0)
                .set_opacity(1 if i == num_query // 2 else 0.1)
                for i in range(num_query)
            ]
        )
        self.playw(Transformr(query, qv))
        wrc = w_r.copy().set_opacity(0)
        w_rs = (
            VGroup(*[(w_r.copy() if i != 0 else w_r) for i in range(8)])
            .arrange(DOWN, buff=0)
            .move_to(wrc)
            .align_to(wrc, UP)
        )
        boxes = VGroup(
            *[
                DashedVMobject(
                    SurroundingRectangle(
                        qv[num_query // 2][0][i : i + 2],
                        buff=0.05,
                        stroke_width=2,
                        color=YELLOW,
                    ),
                    num_dashes=40,
                    dashed_ratio=0.7,
                )
                for i in range(0, 16, 2)
            ]
        )
        self.playw(FadeIn(boxes))

        planes = (
            VGroup(
                *[
                    RaenimPlane(
                        x_range=(-1.0, 1.0, 1), y_range=(-1.0, 1.0, 1)
                    ).set_color(GREY_C)
                    for i in range(8)
                ]
            )
            .scale(0.7)
            .arrange(DOWN, buff=0)
            .next_to(qv[num_query // 2], RIGHT, buff=0.5)
        )
        vals = [qv[num_query // 2]._val[i : i + 2] for i in range(0, 16, 2)]
        arrs = VGroup(
            *[
                Arrow(
                    planes[i].c2p(0, 0),
                    planes[i].c2p(val[0][0], val[1][0]),
                    buff=0,
                    color=YELLOW,
                    stroke_width=3,
                    tip_length=0.1,
                )
                for i, val in enumerate(vals)
            ]
        )
        self.playw(FadeIn(planes, shift=RIGHT * 0.2), Transformr(boxes, arrs))
        self.playw(FadeIn(w_rs[1:]))

        def vals_plus_theta(t):
            wis = [t / (10000 ** (2 * i / 16)) for i in range(8)]
            w_r = np.array(
                [
                    [
                        [np.cos(wis[i]), -np.sin(wis[i])],
                        [np.sin(wis[i]), np.cos(wis[i])],
                    ]
                    for i in range(8)
                ]
            )
            shift_vals = [w_r[i] @ vals[i] for i in range(8)]
            return shift_vals

        def qv_theta(integer=ValueTracker(0)):
            shift_vals = vals_plus_theta(integer.get_value())
            new_qv = (
                DecimalMatrix(
                    [val for pair in shift_vals for val in pair],
                    element_to_mobject_config={"num_decimal_places": 2},
                )
                .scale(0.5)
                .move_to(qv[num_query // 2].get_center())
            )
            integer.increment_value(1)
            return new_qv

        def arr_theta(integer=ValueTracker(0)):
            shift_vals = vals_plus_theta(integer.get_value())
            new_arrs = VGroup(
                *[
                    Arrow(
                        planes[i].c2p(0, 0),
                        planes[i].c2p(val[0][0], val[1][0]),
                        buff=0,
                        color=YELLOW,
                        stroke_width=3,
                        tip_length=0.1,
                    )
                    for i, val in enumerate(shift_vals)
                ]
            )
            integer.increment_value(1)
            return new_arrs

        qv[num_query // 2].generate_target().become(qv_theta(ValueTracker(3)))
        arrs.generate_target().become(arr_theta(ValueTracker(3)))
        self.playw(MoveToTarget(qv[num_query // 2]), MoveToTarget(arrs))

        self.playwl(
            *[
                Circumscribe(
                    qv[num_query // 2][0][i : i + 2],
                    buff=0.05,
                    fade_in=True,
                    fade_out=True,
                    stroke_width=2,
                )
                for i in range(0, 16, 2)
            ],
            lag_ratio=0.1,
        )


class whyRoPEgood(Scene2D):
    def construct(self):
        rope_eq = (
            MathTex(
                r"q_m^\top k_n",  # 0
                r"=",  # 1
                r"(",  # 2
                r"R_{\Theta,m}^d",  # 3
                r"W_q",  # 4
                r"x_m",  # 5
                r")",  # 6
                r"^\top",  # 7
                r"(",  # 8
                r"R_{\Theta,n}^d",  # 9
                r"W_k",  # 10
                r"x_n",  # 11
                r")",  # 12
                r"=",  # 13
                r"x_m^\top",  # 14
                r"W_q^\top",  # 15
                r"R_{\Theta,n-m}^d",  # 16
                r"W_k",  # 17
                r"x_n",  # 18
            )
            .scale(0.8)
            .to_edge(UP, buff=0.5)
        )
        self.addw(rope_eq)
        o1 = lambda x: x.set_opacity(1)
        xm, xn = rope_eq[5], rope_eq[11]

        qx = VGroup(
            *[
                RoundedRectangle(
                    corner_radius=0.05, width=0.3, height=0.3, stroke_width=1.5
                ).set_fill(random_color(), opacity=1)
                for _ in range(10)
            ]
        ).arrange(RIGHT, buff=0.15)
        kx = VGroup(
            *[
                RoundedRectangle(
                    corner_radius=0.05, width=0.3, height=0.3, stroke_width=1.5
                ).set_fill(random_color(), opacity=1)
                for _ in range(10)
            ]
        ).arrange(RIGHT, buff=0.15)
        VGroup(qx, kx).arrange(RIGHT, buff=1).shift(DOWN * 2)

        self.play(FadeIn(qx, kx), rope_eq.animate.set_opacity(0.3))
        self.play(o1(xm.animate), o1(xn.animate))
        self.play(Indicate(xm), Indicate(qx))
        self.play(Indicate(xn), Indicate(kx))

        wqt = MathTex("W_q").scale(0.6).set_z_index(1).set_color(YELLOW_B)
        wqb = (
            Rectangle(width=4.8, height=wqt.height + 0.4, color=GREY_B)
            .move_to(wqt)
            .set_color(YELLOW_B)
            .set_fill(BLACK, opacity=0.7)
        ).set_z_index(0.5)
        wq = VGroup(wqt, wqb)
        wkt = MathTex("W_k").scale(0.6).set_z_index(1).set_color(YELLOW_B)
        wkb = (
            Rectangle(width=4.8, height=wkt.height + 0.4, color=GREY_B)
            .move_to(wkt)
            .set_color(YELLOW_B)
            .set_fill(BLACK, opacity=0.7)
        ).set_z_index(0.5)
        wk = VGroup(wkt, wkb)
        ws = VGroup(wq, wk).arrange(RIGHT, buff=0.5).shift(DOWN * 0.6)
        rope_wq, rope_wk = rope_eq[4], rope_eq[10]
        self.play(
            FadeIn(ws),
            o1(rope_wq.animate.set_color(YELLOW_B)),
            o1(rope_wk.animate.set_color(YELLOW_B)),
        )

        q, k = qx.copy().next_to(wq, UP, buff=0.5), kx.copy().next_to(wk, UP, buff=0.5)
        self.play(Transformr(qx, q), Transformr(kx, k))

        rm, rn = rope_eq[3], rope_eq[9]
        self.play(
            o1(rm.animate.set_color(PURPLE_A)), o1(rn.animate.set_color(PURPLE_A))
        )
        qarrs = VGroup(
            *[
                Arrow(
                    rm.get_bottom(),
                    q[i].get_top(),
                    buff=0.2,
                    color=PURPLE_A,
                    stroke_width=2,
                    tip_length=0.1,
                )
                for i in range(10)
            ]
        )
        karrs = VGroup(
            *[
                Arrow(
                    rn.get_bottom(),
                    k[i].get_top(),
                    buff=0.2,
                    color=PURPLE_A,
                    stroke_width=2,
                    tip_length=0.1,
                )
                for i in range(10)
            ]
        )
        self.play(
            *[GrowArrow(arr) for arr in qarrs], *[GrowArrow(arr) for arr in karrs]
        )

        theta = PI / 30
        anims = []
        for i in range(10):
            anims.append(Rotate(q[i], angle=theta * i))
            anims.append(Rotate(k[i], angle=-theta * i))
        self.play(*anims, FadeOut(qarrs, karrs), run_time=1.5)
        rope_eq.generate_target().shift(UP * 0.5)
        rope_eq.target[2].set_opacity(1)
        rope_eq.target[6:9].set_opacity(1)
        rope_eq.target[12].set_opacity(1)
        self.play(
            VGroup(wq, wk).animate.shift(DOWN * 2.3),
            q.animate.rotate(PI / 2).shift(RIGHT * 0.5 + UP * 0.2),
            k.animate.shift(LEFT * 2.2 + DOWN * 2.5),
            self.cf.animate.scale(1.2),
            MoveToTarget(rope_eq),
        )
        self.playwl(
            rope_eq[13].animate.set_opacity(1),
            rope_eq[14:19].animate.set_opacity(1),
            lag_ratio=0.5,
        )

        rnm = rope_eq[16]
        self.playw(
            o1(rnm.animate.set_color(PURPLE_A)),
            rope_eq[:16].animate.set_opacity(0.3),
            rope_eq[17:].animate.set_opacity(0.3),
        )

        self.playw(self.cf.animate.move_to(rnm).scale(0.7), FadeOut(q, k))

        self.playw(rope_eq.animate.shift(UP * 2))
        sentence = (
            Words(
                "어떻게 고양이를 좋아하는 나를 버려", font="Noto Sans KR", color=GREY_A
            )
            .scale(0.5)
            .next_to(rnm, DOWN, buff=2)
        )
        prev = (
            Words("이 문장은 앞 문장이다.", font="Noto Sans KR", color=GREY_D)
            .scale(0.5)
            .next_to(sentence, LEFT, buff=0.5)
        )
        self.playw(FadeIn(sentence))

        arcs = VGroup()
        for i in range(len(sentence.words)):
            for j in range(i + 1, len(sentence.words)):
                arc = ArcBetweenPoints(
                    sentence.words[i].get_top(),
                    sentence.words[j].get_top(),
                    angle=-PI / 2,
                    stroke_width=2,
                )
                arc.set_color(random_bright_color())
                arcs.add(arc)
        self.playw(*[Create(arc) for arc in arcs], run_time=2)
        
        self.playw(FadeIn(prev))
        self.playw(Flash(rnm.get_corner(UL)))

        self.playw(rope_eq[14:].animate.set_opacity(1))
        self.playw(ApplyWave(sentence))

