from PIL import Image
from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


def denoised(x):
    cat = np.array(Image.open("cat.jpg").convert("RGB"))
    noise = np.random.randint(0, 256, cat.shape).astype(np.uint8)

    _denoised = x * cat.astype(np.float32) + (1 - x) * noise.astype(np.float32)
    _denoised = np.clip(_denoised, 0, 255).astype(np.uint8)
    return ImageMobject(_denoised)


def denoised_patchfied(x, num_patches_h=5, num_patches_w=5, buff=0.1):
    cat = np.array(Image.open("cat.jpg").convert("RGB"))
    noise = np.random.randint(0, 256, cat.shape).astype(np.uint8)

    _denoised = x * cat.astype(np.float32) + (1 - x) * noise.astype(np.float32)
    _denoised = np.clip(_denoised, 0, 255).astype(np.uint8)

    # Patchify the image
    patch_height = cat.shape[0] // num_patches_h
    patch_width = cat.shape[1] // num_patches_w
    patches_arrays = [
        _denoised[
            i * patch_height : (i + 1) * patch_height,
            j * patch_width : (j + 1) * patch_width,
        ]
        for i in range(num_patches_h)
        for j in range(num_patches_w)
    ]

    patches = [ImageMobject(patch).scale(0.2) for patch in patches_arrays]
    patch_group = Group(*patches).arrange_in_grid(
        rows=num_patches_h, cols=num_patches_w, buff=buff
    )
    return patch_group


class intro(Scene2D):
    def construct(self):
        ln1 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        attn = TextBox(
            "Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln2 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ffn = TextBox(
            "FFN",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        for item in [ln1, attn, ln2, ffn]:
            item[1].set_fill(BLACK, 0.7)
            item[1].stretch_to_fit_width(4.5)
            item[1].stretch_to_fit_height(1)

        module = (
            VGroup(ln1, attn, ln2, ffn)
            .arrange(UP, buff=0.2)
            .scale(0.75)
            .shift(UP * 0.7)
        )
        module_box = SurroundingRect(color=YELLOW_B).surround(
            module, buff_h=0.25, buff_w=0.25
        )
        module.add(module_box)

        self.addw(module)

        dit_in = denoised_patchfied(0.5).next_to(module, DOWN)
        self.play(FadeIn(dit_in))
        self.playw(dit_in.animate.arrange(RIGHT, buff=0.1).next_to(module, DOWN))
        dit_out = (
            denoised_patchfied(0.0)
            .arrange(RIGHT, buff=0.1)
            .next_to(module, UP, buff=0.5)
        )
        dit_arrow = Arrow(
            dit_in.get_top(),
            dit_out.get_bottom(),
            buff=0.1,
            color=GREY_B,
            tip_length=0.2,
        ).set_z_index(-0.1)
        self.playwl(GrowArrow(dit_arrow), FadeIn(dit_out), lag_ratio=0.7)

        te = TextBox(
            "Time Embedding",
            text_kwargs={"font_size": 20, "color": BLUE_B},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        co = TextBox(
            "Conditioning",
            text_kwargs={"font_size": 20, "color": BLUE_B},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        for item in [te, co]:
            item[1].set_fill(BLACK, 0.7)
            item[1].stretch_to_fit_width(2.6)
            item[1].stretch_to_fit_height(1)
        te.next_to(module[:-2], LEFT, buff=0.3)
        co.next_to(module[:-2], RIGHT, buff=0.3)
        self.play(module_box.animate.stretch_to_fit_width(module_box.width + 6))
        self.playwl(FadeIn(te), FadeIn(co), lag_ratio=0.5)
        self.playw(Circumscribe(co.text))


class layernorm(Scene3D):
    def construct(self):
        adaLN = Text("AdaLN", font_size=48).set_color_by_gradient(BLUE_A, BLUE_C)
        adaLN_full = Text(
            "Adaptive Layer Normalization", font_size=48
        ).set_color_by_gradient(BLUE_A, BLUE_C)

        self.playwl(*[FadeIn(item) for item in adaLN])
        self.playwl(
            Transform(
                adaLN[:3], adaLN_full[:3], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                adaLN[3], adaLN_full[8], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                adaLN[4], adaLN_full[13], replace_mobject_with_target_in_scene=True
            ),
            FadeIn(adaLN_full[3:8], adaLN_full[9:13], adaLN_full[14:]),
            lag_ratio=0.1,
        )
        self.playwl(
            FadeOut(adaLN_full[:8]),
            adaLN_full[8:].animate.move_to(ORIGIN),
            lag_ratio=0.5,
        )
        ln = adaLN_full[8:]
        ln.generate_target().shift(UP * 2.5)
        std = (
            Text("(Standardization)", font_size=36)
            .set_color_by_gradient(GREY_B, GREY_D)
            .next_to(ln.target[-13:], DOWN)
        )
        self.playwl(
            MoveToTarget(ln),
            FadeIn(std),
            lag_ratio=0.5,
        )

        norm_math = MathTex(
            r"{x -",
            r"\mu}",
            r"\over",
            r"{\sigma}",
            font_size=60,
        )
        norm_math[1].set_color(YELLOW)
        norm_math[3].set_color(GREEN_D)
        self.playw(FadeIn(norm_math))

        dit_in = (
            denoised_patchfied(0.5).arrange(RIGHT, buff=0.1).next_to(norm_math, DOWN)
        )
        self.playw(FadeIn(dit_in))

        tilt_theta = PI / 3
        xijs = (
            VGroup(
                *[
                    VGroup(
                        *[MathTex(f"x_{{{i}{j}}}", font_size=36) for j in range(1, 5)],
                        Text(".·", font_size=36, color=GREY_B),
                    )
                    .arrange(
                        IN * np.sin(tilt_theta)
                        + RIGHT * 0.0001
                        + UP * np.cos(tilt_theta),
                        buff=0.1,
                    )
                    .rotate(tilt_theta - i / 15, UP)
                    for i in range(1, 10)
                ],
                Text("...", font_size=36, color=GREY_B),
            )
            .arrange(RIGHT, buff=0.05)
            .next_to(dit_in, DOWN, buff=0.1)
        )
        self.playw(
            *[FadeTransform(dit_in[i], xijs[i]) for i in range(len(xijs) - 1)],
            FadeOut(dit_in[len(xijs) - 1 :], target_position=xijs[-1], scale=0.2),
            FadeIn(xijs[-1], target_position=dit_in[len(xijs) - 1]),
            self.cf.animate.shift(DOWN),
            ln.animate.set_opacity(0.3),
            std.animate.set_opacity(0.3),
        )

        mus = VGroup(
            *[
                MathTex(rf"\mu_{{{i}}}", color=YELLOW, font_size=36)
                .next_to(xijs[i], UP, buff=0.2)
                .shift(LEFT * 0.2)
                for i in range(len(xijs) - 1)
            ]
        )
        sigs = VGroup(
            *[
                MathTex(rf"\sigma_{{{i}}}", color=GREEN_D, font_size=36).next_to(
                    mus[i], RIGHT, buff=0.05
                )
                for i in range(len(xijs) - 1)
            ]
        )
        self.playwl(
            *[
                Transform(
                    xijs[i].copy(), mus[i], replace_mobject_with_target_in_scene=True
                )
                for i in range(len(xijs) - 1)
            ]
        )
        self.playwl(
            *[
                Transform(
                    xijs[i].copy(), sigs[i], replace_mobject_with_target_in_scene=True
                )
                for i in range(len(xijs) - 1)
            ]
        )

        zijs = (
            VGroup(
                *[
                    VGroup(
                        *[
                            MathTex(f"z_{{{i}{j}}}", font_size=36, color=TEAL_A)
                            for j in range(1, 5)
                        ],
                        Text(".·", font_size=36, color=GREY_B),
                    )
                    .arrange(
                        IN * np.sin(tilt_theta)
                        + RIGHT * 0.0001
                        + UP * np.cos(tilt_theta),
                        buff=0.1,
                    )
                    .rotate(tilt_theta - i / 15, UP)
                    for i in range(1, 10)
                ],
                Text("...", font_size=36, color=GREY_B),
            )
            .arrange(RIGHT, buff=0.2)
            .next_to(dit_in, DOWN, buff=0.1)
        )
        self.playwl(
            *[
                AnimationGroup(
                    Transform(
                        xijs[i], zijs[i], replace_mobject_with_target_in_scene=True
                    ),
                    FadeOut(mus[i], target_position=zijs[i], scale=0.6),
                    FadeOut(sigs[i], target_position=zijs[i], scale=0.6),
                )
                for i in range(len(xijs) - 1)
            ],
            Transform(xijs[-1], zijs[-1], replace_mobject_with_target_in_scene=True),
        )

        scale = MathTex(r"\cdot", r"\gamma", color=PURPLE_B, font_size=60).next_to(
            norm_math, RIGHT, buff=0.75
        )
        shift = MathTex(r"+", r"\beta", color=RED_B, font_size=60).next_to(
            scale, RIGHT, buff=0.75
        )
        self.playw(FadeIn(scale))
        self.playw(FadeIn(shift))
        scale_t = Text(
            "scale", font_size=36, color=PURPLE_B, font="Noto Serif"
        ).next_to(scale, UP, buff=0.2)
        shift_t = Text("shift", font_size=36, color=RED_B, font="Noto Serif").next_to(
            shift, UP, buff=0.2
        )
        self.playwl(FadeIn(scale_t), FadeIn(shift_t), lag_ratio=0.5)

        self.playw(Circumscribe(VGroup(scale, scale_t, shift, shift_t)))
        self.playw(Circumscribe(std), std.animate.set_opacity(1))
        self.playwl(
            Circumscribe(VGroup(scale, scale_t)),
            Circumscribe(VGroup(shift, shift_t)),
            lag_ratio=0.7,
        )

        self.playw(
            self.cf.animate.move_to(ORIGIN),
            FadeOut(std),
            ln.animate.set_opacity(1),
            FadeOut(zijs),
        )

        adaLN_fullc = (
            Text("Adaptive Layer Normalization", font_size=48)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .move_to(ln)
        )
        self.playwl(
            Transform(ln, adaLN_fullc[8:], replace_mobject_with_target_in_scene=True),
            FadeIn(adaLN_fullc[:8]),
            lag_ratio=0.5,
        )

        self.playwl(
            Circumscribe(VGroup(scale, scale_t)),
            Circumscribe(VGroup(shift, shift_t)),
            lag_ratio=0.3,
        )
        scale_c = MathTex(
            r"\cdot", r"\gamma", "_c", color=PURPLE_B, font_size=60
        ).next_to(norm_math, RIGHT, buff=0.75)
        shift_c = MathTex(r"+", r"\beta", "_c", color=RED_B, font_size=60).next_to(
            scale_c, RIGHT, buff=0.55
        )
        self.playw(
            TransformMatchingTex(scale, scale_c),
            TransformMatchingTex(
                shift,
                shift_c,
            ),
        )

        ln1 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 28},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln1[1].set_fill(BLACK, 0.7)
        ln1[1].stretch_to_fit_width(3.5)
        ln1[1].stretch_to_fit_height(1)
        ln1.next_to(norm_math, DOWN, buff=0.5)

        co = TextBox(
            "Conditioning",
            text_kwargs={"font_size": 28, "color": BLUE_B},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        co[1].set_fill(BLACK, 0.7)
        co[1].stretch_to_fit_width(3.5)
        co[1].stretch_to_fit_height(1)
        co.next_to(ln1, RIGHT, buff=0.3)
        adaln_box = SurroundingRect(color=YELLOW_A).surround(
            VGroup(ln1, co), buff_h=0.25, buff_w=0.25
        )
        adaln_t = (
            Text("adaLN", font_size=28, color=YELLOW_A)
            .next_to(adaln_box, LEFT, buff=0.2)
            .align_to(adaln_box, UP)
        )
        adaln_box.add(adaln_t)

        self.playw(
            FadeIn(ln1),
            FadeIn(co),
            FadeIn(adaln_box),
            FadeOut(adaLN_fullc),
            self.cf.animate.shift(DOWN * 2 + RIGHT),
        )
        xijs[0].next_to(ln1, DOWN, buff=0.5).set_z_index(-0.1)
        c = Tensor(1, shape="square").next_to(co, DOWN, buff=0.5).set_z_index(-0.1)
        self.playw(FadeIn(xijs[0]), FadeIn(c))
        zin = xijs[0].copy()
        cc = c.copy()
        self.add(zin, cc)
        self.play(
            xijs[0].animate.become(norm_math),
            c.animate.become(VGroup(scale_c, shift_c).copy()),
        )
        self.remove(xijs[0], c)
        self.wait()


class adaLNvsLN(Scene2D):
    def construct(self):
        line = DashedLine(
            self.cf.get_bottom(), self.cf.get_top(), color=GREY_C, stroke_width=3
        )
        self.addw(line)

        ln = TextBox(
            "LN",
            text_kwargs={"font_size": 24},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln[1].set_fill(BLACK, 0.7)
        ln[1].stretch_to_fit_width(4.5)
        ln[1].stretch_to_fit_height(2.5).align_to(ln[0], UL).shift(UL * 0.1)
        ln.move_to(self.cf.get_left() / 2 + ORIGIN / 2)

        adaLN = TextBox(
            "adaLN",
            text_kwargs={"font_size": 24},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        math_norm_ln = MathTex(
            r"{x -", r"\mu}", r"\over", r"{\sigma}", font_size=36
        ).set_z_index(0.2)
        math_norm_ln[1].set_color(YELLOW)
        math_norm_ln[3].set_color(GREEN_D)
        math_norm_ln.next_to(ln[1].get_bottom(), UP, buff=0.2)
        mnln_box = SurroundingRect(color=GREY_A, stroke_width=2).surround(
            math_norm_ln, buff_h=0.2, buff_w=0.2
        )
        mnln_box.set_z_index(0.1).set_fill(BLACK, 1)
        adaLN[1].set_fill(BLACK, 0.7)
        adaLN[1].stretch_to_fit_width(4.5)
        adaLN[1].stretch_to_fit_height(2.5).align_to(adaLN[0], UL).shift(UL * 0.1)
        adaLN.move_to(self.cf.get_right() / 2 + ORIGIN / 2)
        self.playw(FadeIn(ln, math_norm_ln, mnln_box), FadeIn(adaLN))

        beta_ln = (
            MathTex(r"\beta", color=RED_B, font_size=48)
            .align_to(ln[1], UR)
            .shift(DL * 0.2)
        )
        gamma_ln = MathTex(r"\gamma", color=PURPLE_B, font_size=48).next_to(
            beta_ln, DOWN, buff=0.2
        )
        self.playw(FadeIn(gamma_ln), FadeIn(beta_ln))

        omul = MathTex(r"\cdot", font_size=40, color=WHITE)
        omul_c = Circle(0.16).move_to(omul).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        omul = VGroup(omul, omul_c).set_z_index(0.1).next_to(math_norm_ln, UP, buff=0.4)
        omul[0].set_z_index(0.2)
        oplus = MathTex(r"+", font_size=40, color=WHITE)
        oplus_c = Circle(0.16).move_to(oplus).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        oplus = VGroup(oplus, oplus_c).set_z_index(0.1).next_to(omul, UP, buff=0.3)
        oplus[0].set_z_index(0.2)
        x = MathTex("x", font_size=48, color=WHITE).next_to(ln[1], DOWN, buff=0.3)
        self.playw(FadeIn(omul, oplus, x))
        arrow_ln = Arrow(
            x.get_top(),
            ln[1].get_top() + UP * 0.5,
            buff=0.05,
            color=GREY_B,
            tip_length=0.2,
            stroke_width=3,
        )
        gamma_line_ln = DashedLine(
            gamma_ln.get_left(),
            omul.get_right(),
            color=PURPLE_B,
            stroke_width=3,
        )
        beta_line_ln = DashedLine(
            beta_ln.get_left(),
            oplus.get_right(),
            color=RED_B,
            stroke_width=3,
        )
        self.playwl(
            Create(gamma_line_ln),
            Create(beta_line_ln),
            GrowArrow(arrow_ln),
            lag_ratio=0.5,
        )

        Wgb = (
            MathTex(r"W_{\gamma\beta}", font_size=36, color=YELLOW_A)
            .align_to(adaLN[1], DR)
            .shift(UL * 0.3)
        )
        Wgb_box = (
            SurroundingRect(color=YELLOW_A, stroke_width=2)
            .surround(Wgb, buff_h=0.2, buff_w=0.2)
            .set_z_index(0.1)
            .set_fill(BLACK, 1)
        )
        Wgb.set_z_index(0.2)
        math_norm_adaLN = MathTex(
            r"{x -", r"\mu}", r"\over", r"{\sigma}", font_size=36
        ).set_z_index(0.2)
        math_norm_adaLN[1].set_color(YELLOW)
        math_norm_adaLN[3].set_color(GREEN_D)
        math_norm_adaLN.next_to(adaLN[1].get_bottom(), UP, buff=0.2)
        mnada_box = SurroundingRect(color=GREY_A, stroke_width=2).surround(
            math_norm_adaLN, buff_h=0.2, buff_w=0.2
        )
        mnada_box.set_z_index(0.1).set_fill(BLACK, 1)
        self.playw(
            FadeIn(math_norm_adaLN, mnada_box, Wgb, Wgb_box),
        )
        x_adaLN = (
            MathTex("x", font_size=48, color=WHITE)
            .next_to(adaLN[1], DOWN, buff=0.3)
            .set_z_index(0.2)
        )
        c_adaLN = (
            MathTex("c", font_size=48, color=WHITE)
            .next_to(Wgb_box, DOWN, buff=0.5)
            .set_z_index(0.2)
        )
        self.playw(FadeIn(x_adaLN, c_adaLN))

        beta_adaln = (
            MathTex(r"\beta_c", font_size=48, color=RED_B)
            .next_to(Wgb_box, UP, buff=1.1)
            .set_z_index(0.2)
        )
        gamma_adaln = (
            MathTex(r"\gamma_c", font_size=48, color=PURPLE_B)
            .next_to(beta_adaln, DOWN, buff=0.2)
            .set_z_index(0.2)
        )

        c_arrow = Arrow(
            c_adaLN.get_top(),
            gamma_adaln.get_bottom(),
            buff=0.05,
            color=GREY_B,
            stroke_width=2,
            tip_length=0.2,
        )
        omul_adaln = MathTex(r"\cdot", font_size=40, color=WHITE)
        omul_adaln_c = (
            Circle(0.16).move_to(omul_adaln).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        )
        omul_adaln = VGroup(omul_adaln, omul_adaln_c).set_z_index(0.1)
        omul_adaln[0].set_z_index(0.2)
        omul_adaln.next_to(math_norm_adaLN, UP, buff=0.4)

        oplus_adaln = MathTex(r"+", font_size=40, color=WHITE).next_to(
            omul_adaln, UP, buff=0.3
        )
        oplus_adaln_c = (
            Circle(0.16).move_to(oplus_adaln).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        )
        oplus_adaln = VGroup(oplus_adaln, oplus_adaln_c).set_z_index(0.1)
        oplus_adaln[0].set_z_index(0.2)
        gamma_line_adaln = DashedLine(
            gamma_adaln.get_left(),
            omul_adaln.get_right(),
            color=PURPLE_B,
            stroke_width=3,
        )
        beta_line_adaln = DashedLine(
            beta_adaln.get_left(),
            oplus_adaln.get_right(),
            color=RED_B,
            stroke_width=3,
        )
        self.playwl(GrowArrow(c_arrow), FadeIn(gamma_adaln, beta_adaln), lag_ratio=0.5)
        x_arrow_adaln = Arrow(
            x_adaLN.get_top(),
            adaLN[1].get_top() + UP * 0.5,
            buff=0.05,
            color=GREY_B,
            tip_length=0.2,
            stroke_width=3,
        )
        self.playwl(
            FadeIn(omul_adaln, oplus_adaln),
            Create(gamma_line_adaln),
            Create(beta_line_adaln),
            GrowArrow(x_arrow_adaln),
            lag_ratio=0.5,
        )
        self.playw(Circumscribe(c_adaLN))


class singleLabel(Scene2D):
    def construct(self):
        adaln = TextBox(
            "adaLN",
            text_kwargs={"font_size": 24},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        adaln[1].set_fill(BLACK, 0.7)
        adaln[1].stretch_to_fit_width(4.5)
        adaln[1].stretch_to_fit_height(2.5).align_to(adaln[0], UL).shift(UL * 0.1)
        adaln.move_to(ORIGIN).shift(UP * 0.5)

        math_norm = MathTex(
            r"{x -", r"\mu}", r"\over", r"{\sigma}", font_size=36
        ).set_z_index(0.2)
        math_norm[1].set_color(YELLOW)
        math_norm[3].set_color(GREEN_D)
        math_norm.next_to(adaln[1].get_bottom(), UP, buff=0.2)
        mnada_box = SurroundingRect(color=GREY_A, stroke_width=2).surround(
            math_norm, buff_h=0.2, buff_w=0.2
        )
        mnada_box.set_z_index(0.1).set_fill(BLACK, 1)
        Wgb = (
            MathTex(r"W_{\gamma\beta}", font_size=36, color=YELLOW_A)
            .align_to(adaln[1], DR)
            .shift(UL * 0.3)
        )
        Wgb_box = (
            SurroundingRect(color=YELLOW_A, stroke_width=2)
            .surround(Wgb, buff_h=0.2, buff_w=0.2)
            .set_z_index(0.1)
            .set_fill(BLACK, 1)
        )
        Wgb.set_z_index(0.3)

        self.playw(FadeIn(adaln, math_norm, mnada_box, Wgb, Wgb_box))

        c_single = (
            Tensor(1, shape="square").next_to(Wgb_box, DOWN, buff=0.5).set_z_index(-0.1)
        )

        c_123 = (
            Tensor(3, shape="square", arrange=RIGHT)
            .next_to(Wgb_box, DOWN, buff=0.5)
            .set_z_index(0.15)
        )

        self.play(FadeIn(c_single))
        self.playw(c_single.animate.move_to(Wgb))
        self.remove(c_single)

        self.play(FadeIn(c_123))
        self.play(
            c_123.animate.scale(0.6).next_to(Wgb_box, DOWN, buff=0),
            rate_func=rush_into,
            run_time=0.5,
        )
        c_123.generate_target().rotate(PI / 3).next_to(self.cf, RIGHT, buff=2.5).shift(
            DOWN * 3
        )
        self.playw(MoveToTarget(c_123), rate_func=rush_from, run_time=2)

        c_single = (
            Tensor(1, shape="square").next_to(Wgb_box, DOWN, buff=0.5).set_z_index(-0.1)
        )
        label_c = Text('"0"', font_size=24, color=WHITE).move_to(c_single)
        self.playw(FadeIn(c_single))
        self.playw(
            Transform(c_single, label_c, replace_mobject_with_target_in_scene=True)
        )
        self.playw(label_c.animate.move_to(Wgb))

        c_123 = (
            Tensor(3, shape="square", arrange=RIGHT)
            .next_to(Wgb_box, DOWN, buff=0.5)
            .set_z_index(0.15)
        )
        label_123 = (
            ListText(
                '"cat"',
                '"eating"',
                '"vegetable"',
                font_size=24,
                color=WHITE,
                no_bracket=True,
            )
            .arrange(RIGHT, buff=0.3)
            .move_to(c_123)
        )

        self.play(FadeIn(c_123))
        self.playwl(
            *[
                Transform(
                    c_123[i], label_123[i], replace_mobject_with_target_in_scene=True
                )
                for i in range(len(label_123))
            ],
            lag_ratio=0.3,
            wait=0.2,
        )
        self.playw(label_123.copy().animate.scale(0.2).move_to(Wgb))
        self.playw(label_123.animate.set_color(PURE_RED))

        self.playw(FadeOut(label_123))
        xs = (
            denoised_patchfied(0.5, num_patches_h=3, num_patches_w=3, buff=0.1)
            .arrange(RIGHT, buff=0.1)[:4]
            .next_to(c_single, LEFT, buff=0.5)
        )
        self.playw(FadeIn(c_single, xs))

        gamma = MathTex(r"\gamma_c", font_size=36, color=PURPLE_B).next_to(
            xs, UP, buff=0.5
        )
        beta = MathTex(r"\beta_c", font_size=36, color=RED_B).next_to(
            gamma, DOWN, buff=0.2
        )
        gamma.move_to(Wgb)
        beta.move_to(Wgb)

        self.play(c_single.copy().animate.move_to(Wgb))
        self.play(
            gamma.animate.shift(UP),
            beta.animate.shift(UP * 1.6),
            xs.animate.scale(0.58).move_to(math_norm),
        )
        self.play(xs.animate.scale(1 / 0.58).next_to(math_norm, UP, buff=0.3))
        gammas = VGroup(*[gamma.copy() for _ in range(len(xs))])
        self.playwl(
            *[gammas[i].animate.move_to(xs[i]) for i in range(len(xs))], wait=0.1
        )
        self.playw(*[FadeOut(gammas[i], scale=1.5) for i in range(len(xs))])

        self.playw(FadeOut(gamma, beta))

        c_123 = (
            Tensor(3, shape="square", arrange=RIGHT)
            .next_to(Wgb_box, DOWN, buff=0.5)
            .set_z_index(0.15)
        )
        self.play(FadeIn(c_123), FadeOut(c_single), run_time=0.5)
        label_123 = (
            ListText(
                '"cat"',
                '"eating"',
                '"vegetable"',
                font_size=24,
                color=WHITE,
                no_bracket=True,
            )
            .arrange(RIGHT, buff=0.3)
            .move_to(c_123)
        )

        self.playwl(
            *[
                Transform(
                    c_123[i], label_123[i], replace_mobject_with_target_in_scene=True
                )
                for i in range(len(label_123))
            ],
            lag_ratio=0.3,
            wait=0.2,
        )
        label_123c = label_123.copy()
        self.play(label_123c.animate.scale(0.2).move_to(Wgb))

        gamma123 = (
            VGroup(
                *[
                    MathTex(rf"\gamma_{{c{{{i}}}}}", font_size=24, color=PURPLE_B)
                    for i in range(1, 4)
                ]
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(Wgb, UP, buff=0.6)
        )
        beta123 = (
            VGroup(
                *[
                    MathTex(rf"\beta_{{c{{{i}}}}}", font_size=24, color=RED_B)
                    for i in range(1, 4)
                ]
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(gamma123, UP, buff=0.4)
        )
        self.playw(
            *[
                Transform(
                    label_123c[i],
                    VGroup(gamma123[i], beta123[i]),
                    replace_mobject_with_target_in_scene=True,
                )
                for i in range(len(gamma123))
            ],
            self.cf.animate.scale(0.6).move_to(gamma123),
            label_123.animate.set_color(GREY_C),
        )
        self.playw(VGroup(gamma123, beta123).animate.set_color(PURE_RED))


class adaLNZero(Scene2D):
    def construct(self):
        adalnzt = Text("adaLN-Zero", font_size=48).set_color_by_gradient(BLUE_A, BLUE_C)
        adaln = adalnzt[:5]
        zt = adalnzt[5:].set_opacity(0)
        adaln.save_state()
        adaln.move_to(ORIGIN)
        self.playwl(*[FadeIn(item) for item in adaln])
        self.playwl(Restore(adaln), zt.animate.set_opacity(1), lag_ratio=0.5, wait=3)
        self.playw(zt.animate.set_color(PURE_RED))

        ln = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 24, "color": GREY_A},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln[1].set_fill(BLACK, 0.7)
        ln[1].stretch_to_fit_width(4.5)
        ln[1].stretch_to_fit_height(1)

        sa = TextBox(
            "Self-Attention",
            text_kwargs={"font_size": 24, "color": GREY_A},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        sa[1].set_fill(BLACK, 0.7)
        sa[1].stretch_to_fit_width(4.5)
        sa[1].stretch_to_fit_height(1)
        sa.next_to(ln, UP, buff=1.7)

        wagb = (
            MathTex(
                r"W_", r"{\alpha", r"\gamma", r"\beta}", font_size=48, color=YELLOW_A
            )
            .next_to(ln, RIGHT, buff=0.7)
            .set_z_index(1)
        )
        wagb[1].set_color(BLUE_B)
        wagb[2].set_color(PURPLE_B)
        wagb[3].set_color(RED_B)
        wagb_box = (
            SurroundingRect(color=YELLOW_A, stroke_width=2)
            .surround(wagb, buff_h=0.2, buff_w=0.2)
            .set_z_index(0.1)
            .set_fill(BLACK, 1)
        )

        box = SurroundingRect(color=YELLOW_A).surround(
            VGroup(ln, sa), buff_h=0.25, buff_w=0.25
        )
        _bc = box.copy()
        box.stretch_to_fit_height(5.2).stretch_to_fit_width(7).align_to(_bc, DL)
        self.playwl(
            adalnzt.animate.next_to(self.cf, LEFT),
            FadeIn(ln, wagb, wagb_box),
            lag_ratio=0.3,
            wait=0.1,
        )
        self.remove(adalnzt)
        self.playwl(
            self.cf.animate.shift(UP * 1.5).scale(1.1), FadeIn(sa, box), lag_ratio=0.3
        )
        gamma = (
            MathTex(r"\gamma", font_size=48, color=PURPLE_B)
            .next_to(wagb_box, UP, buff=0.5)
            .set_z_index(0.2)
        )
        beta = (
            MathTex(r"\beta", font_size=48, color=RED_B)
            .next_to(gamma, UP, buff=0.2)
            .set_z_index(0.2)
        )
        alpha = (
            MathTex(r"\alpha", font_size=48, color=BLUE_B)
            .next_to(beta, UP, buff=0.2)
            .set_z_index(0.2)
        )
        omul1 = MathTex(r"\cdot", font_size=40, color=WHITE).next_to(ln, UP, buff=0.4)
        omul1_c = Circle(0.16).move_to(omul1).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        omul1 = VGroup(omul1, omul1_c).set_z_index(0.1)
        omul1[0].set_z_index(0.2)
        oplus = MathTex(r"+", font_size=40, color=WHITE).next_to(omul1, UP, buff=0.3)
        oplus_c = Circle(0.16).move_to(oplus).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        oplus = VGroup(oplus, oplus_c).set_z_index(0.1)
        oplus[0].set_z_index(0.2)
        omul2 = MathTex(r"\cdot", font_size=40, color=WHITE).next_to(sa, UP, buff=0.5)
        omul2_c = Circle(0.16).move_to(omul2).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        omul2 = VGroup(omul2, omul2_c).set_z_index(0.1)
        omul2[0].set_z_index(0.2)
        gamma.align_to(omul1, UP)
        beta.align_to(oplus, UP)
        alpha.align_to(omul2, UP)

        x = MathTex("x", font_size=48, color=WHITE).next_to(ln, DOWN, buff=0.3)
        c = (
            Tensor(1, shape="square")
            .next_to(wagb_box, DOWN, buff=0.5)
            .set_z_index(-0.1)
        )
        arrow_ln = (
            Arrow(
                x.get_top(),
                omul2.get_top() + UP * 1.2,
                buff=0.05,
                color=GREY_B,
                tip_length=0.2,
                stroke_width=3,
            )
            .set_z_index(-0.5)
            .set_opacity(1)
        )
        self.play(FadeIn(c), run_time=0.5)
        self.play(c.animate.move_to(wagb))
        self.playwl(
            *[FadeIn(item, target_position=wagb) for item in [gamma, beta, alpha]],
            FadeIn(x),
            lag_ratio=0.3,
        )

        gamma_line = DashedLine(
            gamma.get_left(),
            omul1.get_right(),
            color=GREY_C,
            stroke_width=3,
        )
        beta_line = DashedLine(
            beta.get_left(),
            oplus.get_right(),
            color=GREY_C,
            stroke_width=3,
        )
        alpha_line = DashedLine(
            alpha.get_left() + LEFT * 0.05,
            omul2.get_right(),
            color=YELLOW,
            stroke_width=4,
            dash_length=0.2,
            dashed_ratio=0.7,
        )
        self.playwl(
            AnimationGroup(Create(gamma_line), Create(beta_line), Create(alpha_line)),
            FadeIn(omul1, oplus, omul2),
            lag_ratio=0.5,
            wait=0.1,
        )
        self.playw(GrowArrow(arrow_ln))

        res = BrokenLine(
            sa.get_bottom() + DOWN * 0.25,
            sa.get_bottom() + DOWN * 0.25 + LEFT * 2.5,
            sa.get_bottom() + DOWN * 0.25 + LEFT * 2.5 + UP * 2.2,
            sa.get_bottom() + DOWN * 0.25 + LEFT * 2.5 + UP * 2.2 + RIGHT * 2.35,
            stroke_width=2,
            tip_length=0.25,
            arrow=True,
            color=GREEN,
        )
        oplus_res = MathTex(r"+", font_size=40, color=WHITE).next_to(
            res[-1].get_end(), RIGHT, buff=0.0
        )
        oplus_res_c = (
            Circle(0.16).move_to(oplus_res).set_fill(BLACK, 1).set_stroke(GREY_A, 2)
        )
        oplus_res = VGroup(oplus_res, oplus_res_c).set_z_index(0.1)
        oplus_res[0].set_z_index(0.2)
        _bc = box.copy()
        box.generate_target().stretch_to_fit_width(7.4).align_to(_bc, DR)
        self.playwl(
            MoveToTarget(box),
            Succession(*[Create(line, rate_func=linear) for line in res], run_time=1),
            FadeIn(oplus_res),
            lag_ratio=0.5,
        )
        self.playw(Indicate(omul2))

        alpha_zero = MathTex("0", font_size=48, color=WHITE).move_to(alpha)
        self.playw(
            Transform(alpha, alpha_zero, replace_mobject_with_target_in_scene=True)
        )
        adalnzt.next_to(self.cf, LEFT).set_opacity(1).scale(0.7)
        adalnzt.save_state()
        self.play(adalnzt.animate.align_to(self.cf, LEFT).shift(RIGHT * 0.3))
        self.playw(Restore(adalnzt), wait=5)

        sa.generate_target().set_opacity(0.2)
        sa.target[1].set_fill(BLACK, 0.7)
        omul2.generate_target().set_opacity(0.2)
        omul2.target[1].set_fill(BLACK, 0.7)
        temp_line = Line(
            res[0].get_start(), oplus_res_c.get_bottom(), color=BLACK, stroke_width=6
        ).set_z_index(0.1)
        self.playw(MoveToTarget(sa), MoveToTarget(omul2), FadeIn(temp_line))

        skip_connection_line = BrokenLine(
            oplus_c.get_top(),
            res[0].get_start(),
            res[1].get_start(),
            res[2].get_start(),
            res[2].get_end(),
            color=PURE_GREEN,
        )
        self.playw(
            Succession(
                *[Create(line, rate_func=linear) for line in skip_connection_line],
                run_time=1.5,
            ),
        )
 