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
        dit = Text("DiT 2", font_size=64).set_color_by_gradient(GREEN_A, GREEN_C)
        self.playw(FadeIn(dit[:-1]))
        self.playw(FadeIn(dit[-1]), run_time=0.3)

        te = (
            Text("Time embedding", font_size=36)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(dit, UP, buff=0.4)
            .align_to(dit[2], RIGHT)
            .shift(LEFT * 0.5)
        )
        co = (
            Text("Conditioning", font_size=36)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(dit, UP, buff=0.4)
            .align_to(dit[2], LEFT)
            .shift(RIGHT * 0.5)
        )
        self.playw(*[FadeIn(t, scale=0.5, target_position=dit) for t in [te, co]])

        dit_full = Text("Diffusion Transformer", font_size=64).set_color_by_gradient(
            GREEN_A, GREEN_C
        )
        self.playw(
            LaggedStart(
                FadeOut(dit[-1]),
                Transform(
                    dit[:2], dit_full[:2], replace_mobject_with_target_in_scene=True
                ),
                FadeIn(dit_full[2:8]),
                Transform(
                    dit[2],
                    dit_full[8],
                    replace_mobject_with_target_in_scene=True,
                ),
                FadeIn(dit_full[9:]),
                lag_ratio=0.4,
            ),
            wait=5,
        )
        dit[:-1].arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        self.play(
            LaggedStart(
                FadeOut(dit_full[2:8], dit_full[9:]),
                AnimationGroup(
                    Transform(
                        dit_full[:2], dit[:2], replace_mobject_with_target_in_scene=True
                    ),
                    Transform(
                        dit_full[8],
                        dit[2],
                        replace_mobject_with_target_in_scene=True,
                    ),
                ),
                FadeOut(te, co),
                lag_ratio=0.4,
            )
        )
        dit = dit[:-1].set_z_index(1)
        dit_box = (
            SurroundingRect(stroke_width=2)
            .surround(dit, buff_h=1, buff_w=3)
            .set_fill(color=BLACK, opacity=0.9)
            .set_z_index(0.5)
        )
        self.play(Create(dit_box))

        dit_in = Tensor(7, shape="square", arrange=RIGHT, buff=0.2).next_to(
            dit_box, DOWN, buff=0.5
        )
        dit_out = Tensor(7, shape="square", arrange=RIGHT, buff=0.2).next_to(
            dit_box, UP, buff=0.5
        )
        self.playw(FadeIn(dit_in), wait=0.2)
        self.playw(
            Transform(dit_in, dit_out, replace_mobject_with_target_in_scene=True)
        )


class eot(Scene2D):
    def construct(self):
        attn = TextBox(
            "Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln1 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ffn = TextBox(
            "FFN",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln2 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        for item in [attn, ln1, ffn, ln2]:
            item[1].stretch_to_fit_width(4.5)
            item[1].stretch_to_fit_height(1)
        module = VGroup(attn, ln1, ffn, ln2).arrange(UP, buff=0.2)
        module_box = SurroundingRect(color=YELLOW_B).surround(
            module, buff_h=0.25, buff_w=0.25
        )
        module.add(module_box)
        timg = (
            ImageMobject("tstructure.png")
            .scale(1.3)
            .next_to(self.cf, RIGHT)
            .shift(UP * 0.5)
        )
        self.playw(timg.animate.move_to(ORIGIN).shift(UP * 0.5))
        module.save_state()
        module.stretch_to_fit_height(2.3).shift(UP * 0.2).stretch_to_fit_width(
            1.5
        ).shift(LEFT * 0.95)
        self.play(FadeIn(module), FadeOut(timg))
        self.playw(Restore(module))

        self.playw(
            module_box.animate.stretch_to_fit_width(8.5).align_to(module_box, RIGHT),
            module[:-1].animate.scale(0.8),
        )

        te = TextBox(
            "Time Embedding",
            text_kwargs={"font_size": 28},
            box_kwargs={"buff": 0.3, "color": BLUE, "stroke_width": 2},
        ).next_to(ln1, LEFT, buff=0.4)
        co = TextBox(
            "Conditioning",
            text_kwargs={"font_size": 28},
            box_kwargs={"buff": 0.3, "color": BLUE, "stroke_width": 2},
        )
        co[1].stretch_to_fit_width(te[1].width)
        co.next_to(ln1, LEFT, buff=0.4).shift(UP*1.5)
        self.playw(FadeIn(te), FadeIn(co))
        return
        #

        ms = module[:-1]
        ms.generate_target().set_opacity(0.3)
        [ms.target[i][1].set_fill(opacity=0) for i in [0, 1, 2, 3]]
        co.generate_target().set_opacity(0.3)
        co.target[1].set_fill(opacity=0)

        self.play(
            MoveToTarget(ms),
            MoveToTarget(co),
        )
        ms.save_state()
        co.save_state()
        self.playw(
            ms.animate.set_opacity(0),
            co.animate.set_opacity(0),
            te.animate.move_to(ORIGIN).align_to(te, LEFT),
        )
        self.playw(Circumscribe(te[0][:4]))

        self.playw(self.cf.animate.scale(1.6).align_to(self.cf, UP))

        noise = denoised(0).scale(0.4).next_to(module_box, DOWN, buff=0.5)
        t0 = Text("t = 0", font=MONO_FONT, font_size=32).next_to(noise, LEFT)
        self.playw(FadeIn(noise, t0))
        cat = denoised(1).scale(0.4).next_to(module_box, DOWN, buff=0.5)
        t1 = Text("t = 1", font=MONO_FONT, font_size=32).next_to(cat, LEFT)
        self.playw(
            Transform(noise, cat, replace_mobject_with_target_in_scene=True),
            Transform(t0, t1, replace_mobject_with_target_in_scene=True),
        )
        t = ValueTracker(0.2)
        latent_t = (
            lambda: denoised(t.get_value())
            .scale(0.4)
            .next_to(module_box, DOWN, buff=0.5)
        )
        latent = latent_t()
        text_t = lambda: Text(
            f"t = {t.get_value():.2f}", font=MONO_FONT, font_size=32
        ).next_to(latent, LEFT)
        t2 = text_t()
        self.playw(
            Transform(cat, latent, replace_mobject_with_target_in_scene=True),
            Transform(t1, t2, replace_mobject_with_target_in_scene=True),
        )

        t2.add_updater(lambda m: m.become(text_t()))
        latent.add_updater(lambda m: m.become(latent_t()))
        self.playw(t.animate.set_value(0.7))
        t2.clear_updaters()
        latent.clear_updaters()

        self.play(Circumscribe(t2))
        te.save_state()
        t2.save_state()
        self.playw(
            t2.animate.set_opacity(0.2),
            te[0].animate.set_opacity(0.2),
            te[1].animate.set_opacity(0.2).set_fill(opacity=0),
        )
        module_box.set_fill(BLACK, opacity=0.4)
        latent.set_z_index(-0.1)
        self.playw(latent.animate.move_to(module_box))
        self.playw(Wiggle(latent))

        self.playw(Restore(te), Restore(t2))
        te[1].set_fill(BLACK, opacity=1)
        te.set_z_index(1)
        t2.set_z_index(0.5)
        self.play(t2.animate.next_to(te, DOWN))
        self.play(t2.animate.move_to(te))
        self.playw(Wiggle(te))


class conditioning(Scene2D):
    def construct(self):
        attn = TextBox(
            "Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln1 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ffn = TextBox(
            "FFN",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln2 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        for item in [attn, ln1, ffn, ln2]:
            item[1].stretch_to_fit_width(4.5)
            item[1].stretch_to_fit_height(1)
        module = VGroup(attn, ln1, ffn, ln2).arrange(UP, buff=0.2)
        module.scale(0.8)
        module_box = SurroundingRect(color=YELLOW_B).surround(
            module, buff_h=0.25, buff_w=0.25
        )
        module_box.stretch_to_fit_width(12.5)
        te = TextBox(
            "Time Embedding",
            text_kwargs={"font_size": 28},
            box_kwargs={"buff": 0.3, "color": BLUE, "stroke_width": 2},
        ).next_to(ln1, LEFT, buff=0.4)
        co = TextBox(
            "Conditioning",
            text_kwargs={"font_size": 28},
            box_kwargs={"buff": 0.3, "color": BLUE, "stroke_width": 2},
        )
        co[1].stretch_to_fit_width(te[1].width)
        co.next_to(ln1, RIGHT, buff=0.4)
        self.addw(module, module_box, te, co)
        for item in [attn, ln1, ffn, ln2]:
            item[0].set_opacity(0.3)
            item[1].set_opacity(0.3).set_fill(opacity=0.0)

        self.playw(
            te[0].animate.set_opacity(0.2),
            te[1].animate.set_opacity(0.2).set_fill(opacity=0),
        )
        self.playw(Indicate(co[0]))

        self.playw(self.cf.animate.scale(1.6).align_to(self.cf, UP))

        noise = denoised(0).scale(0.4).next_to(module_box, DOWN, buff=0.5)
        condition = Text("text", font=MONO_FONT, font_size=36).next_to(
            noise, RIGHT, buff=1
        )
        self.playw(FadeIn(noise, condition))
        self.playw(Circumscribe(condition))
        self.playw(
            condition.animate.become(
                Text('"Vegetarian cat"', font=MONO_FONT, font_size=36).next_to(
                    noise, RIGHT, buff=1
                )
            ),
            wait=4,
        )
        condition.set_z_index(-1)
        module_box.set_fill(BLACK, opacity=0.4).set_z_index(-0.5)
        co[1].set_fill(BLACK, opacity=0.8)
        self.playw(condition.animate.move_to(co).scale(0.7))


class conditioning1(Scene2D):
    def construct(self):
        attn = TextBox(
            "Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln1 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ffn = TextBox(
            "FFN",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln2 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        for item in [attn, ln1, ffn, ln2]:
            item[1].stretch_to_fit_width(4.5)
            item[1].stretch_to_fit_height(1)
        module = VGroup(attn, ln1, ffn, ln2).arrange(UP, buff=0.2)
        module.scale(0.65)
        module_box = SurroundingRect(color=YELLOW_B).surround(
            module, buff_h=0.25, buff_w=0.25
        )
        for item in [attn, ln1, ffn, ln2]:
            item[0].set_opacity(0.5)
            item[1].set_opacity(0.5).set_fill(opacity=0.0)
        module_box.stretch_to_fit_width(5.5)
        VGroup(module, module_box).shift(UP)
        self.playw(FadeIn(module), FadeIn(module_box))

        patches = denoised_patchfied(0.5, buff=0).next_to(module_box, DOWN, buff=0.5)
        out_patches = (
            denoised_patchfied(0)
            .arrange(RIGHT, buff=0.05)
            .next_to(module_box, UP, buff=0.5)
        )
        self.play(FadeIn(patches))
        self.play(
            patches.animate.arrange_in_grid(rows=5, cols=5, buff=0.05).next_to(
                module_box, DOWN, buff=0.5
            )
        )
        self.playw(patches.animate.arrange(RIGHT, buff=0.05).next_to(module_box, DOWN))

        text_in = Text('"Vegetarian cat"', font=MONO_FONT, font_size=18).next_to(
            patches, DR, buff=0.2
        )
        text0, text1 = text_in[:-4], text_in[-4:]
        self.playw(FadeIn(text_in))
        text_token = (
            Tensor(2, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.55)
            .next_to(patches, RIGHT, buff=0.2)
        )
        text_out = (
            Tensor(2, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.55)
            .next_to(out_patches, RIGHT, buff=0.2)
        )
        self.playw(
            Transform(text0, text_token[0], replace_mobject_with_target_in_scene=True),
            Transform(text1, text_token[1], replace_mobject_with_target_in_scene=True),
        )
        for item in [attn, ln1, ffn, ln2]:
            item[1].set_fill(BLACK, opacity=0.5)

        module_box.set_fill(BLACK, opacity=0.5).set_z_index(-0.5)
        model_in = Group(patches, text_token).set_z_index(-1.5)
        model_in.generate_target().stretch_to_fit_width(4.5).scale(0.6).move_to(attn)
        self.play(MoveToTarget(model_in))
        self.play(model_in.animate.move_to(ln2))
        model_out = Group(out_patches, text_out).set_z_index(-1.5)
        self.playw(
            Transform(model_in, model_out, replace_mobject_with_target_in_scene=True)
        )

        self.playw(Circumscribe(model_out[0]))
        self.playw(
            text_out.animate.rotate(PI / 3)
            .next_to(self.cf, RIGHT, buff=0.5)
            .shift(UP * 2)
        )


class conditioning2(Scene2D):
    def construct(self):
        attn = TextBox(
            "Attn",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln1 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ffn = TextBox(
            "FFN",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        ln2 = TextBox(
            "LayerNorm",
            text_kwargs={"font_size": 32},
            box_kwargs={"buff": 0.5, "color": WHITE, "stroke_width": 2},
        )
        for item in [attn, ln1, ffn, ln2]:
            item[1].stretch_to_fit_width(4.5)
            item[1].stretch_to_fit_height(1)
        module = VGroup(attn, ln1, ffn, ln2).arrange(UP, buff=0.2)
        module.scale(0.65)
        module_box = SurroundingRect(color=YELLOW_B).surround(
            module, buff_h=0.25, buff_w=0.25
        )
        for item in [attn, ln1, ffn, ln2]:
            item[0].set_opacity(0.5)
            item[1].set_opacity(0.5).set_fill(opacity=0.0)
        module_box.stretch_to_fit_width(5.5)
        VGroup(module, module_box).shift(UP)
        self.addw(module, module_box)

        patches = denoised_patchfied(0.5, buff=0.05).next_to(module_box, DOWN, buff=0.5)
        self.play(FadeIn(patches))
        self.playw(patches.animate.arrange(RIGHT, buff=0.05).next_to(module_box, DOWN))
        text_in = Text('"Vegetarian cat"', font=MONO_FONT, font_size=18).next_to(
            patches, UR, buff=0.2
        )
        self.play(FadeIn(text_in))
        text_token = (
            Tensor(2, shape="square", arrange=UP, buff=0.1)
            .scale(0.55)
            .next_to(patches, UR, buff=0.2)
            .shift(UP * 0.2)
        )
        self.playw(
            Transform(
                text_in[:-4],
                text_token[0],
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                text_in[-4:],
                text_token[1],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        kline, vline = DashedLine(
            text_token[0].get_left(),
            attn.get_right(),
            dash_length=0.1,
        ), DashedLine(
            text_token[1].get_left(),
            attn.get_right(),
            dash_length=0.1,
        )
        self.playw(Create(kline), Create(vline))
        qt = Text("query", font=MONO_FONT, font_size=18).next_to(
            patches, LEFT, buff=0.2
        )
        kvt = Text("key-value", font=MONO_FONT, font_size=18).next_to(
            text_token[1], UR, buff=0.1
        )
        self.playw(FadeIn(qt))
        self.playw(FadeIn(kvt))
        for item in [attn, ln1, ffn, ln2]:
            item[1].set_fill(BLACK, opacity=0.5)

        module_box.set_fill(BLACK, opacity=0.5).set_z_index(-0.5)
        patches.set_z_index(-1.5)
        text_token.set_z_index(-1.5)
        patches.generate_target().stretch_to_fit_width(4.5).scale(0.6).move_to(attn)
        text_token.generate_target().move_to(attn).scale(0.6)
        self.playw(
            MoveToTarget(patches),
            MoveToTarget(text_token),
            FadeOut(qt),
            FadeOut(kvt),
            FadeOut(kline),
            FadeOut(vline),
        )
        self.playw(patches.animate.move_to(ln2), FadeOut(text_token))
        out_patches = (
            denoised_patchfied(0)
            .arrange(RIGHT, buff=0.05)
            .next_to(module_box, UP, buff=0.5)
        )
        self.playw(
            Transform(patches, out_patches, replace_mobject_with_target_in_scene=True)
        )
