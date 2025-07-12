from manim import *
from raenim import *
from PIL import Image
from random import seed


seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        gm = Text(
            "Generative Model", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(GREEN_A, GREEN_D)
        gmbox = (
            SurroundingRect(stroke_width=3, color=GREY_B)
            .set_fill(BLACK, opacity=1)
            .surround(gm)
            .set_z_index(-0.5)
        )
        gm = VGroup(gm, gmbox).move_to(ORIGIN)
        gm_rect = RoundedRectangle(width=9, height=6).set_z_index(-1)
        gm.next_to(gm_rect, UP, buff=-0.3)

        self.playw(FadeIn(gm, gm_rect), run_time=0.4)

        diffusion = Text(
            "Diffusion", font_size=28, font="Noto Serif"
        ).set_color_by_gradient(BLUE_A, BLUE_D)
        diffusion_box = (
            SurroundingRect(stroke_width=3, color=GREY_B)
            .set_fill(BLACK, opacity=1)
            .surround(diffusion)
            .set_z_index(-0.5)
        )
        diffusion = VGroup(diffusion, diffusion_box).move_to(ORIGIN)
        diffusion_rect = RoundedRectangle(width=4, height=3).set_z_index(-1)
        diffusion.next_to(diffusion_rect, UP, buff=-0.3)
        VGroup(diffusion, diffusion_rect).shift(RIGHT * 1.5)
        self.play(
            FadeIn(diffusion, diffusion_rect),
            run_time=0.4,
        )
        self.playw(
            self.cf.animate.scale(0.6).move_to(diffusion_rect), FadeOut(gm_rect, gm)
        )

        dit = (
            Text("DiT", font_size=36, font="Noto Serif")
            .set_color_by_gradient(YELLOW_A, YELLOW)
            .move_to(diffusion_rect)
        )
        self.playw(
            FadeIn(dit, scale=0.7), VGroup(diffusion, diffusion_rect).animate.scale(3)
        )

        self.playw(dit.animate.scale(4 / 3), run_time=3)

        self.playw(dit.animate.shift(LEFT * 2))
        first = Text(
            "1. Basic Transformer", font_size=28, font="Noto Serif"
        ).set_color_by_gradient(GREY_A, GREY_B)
        second = Text(
            "2. How DiT works", font_size=28, font="Noto Serif"
        ).set_color_by_gradient(GREY_A, GREY_B)
        VGroup(first, second).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(
            dit, RIGHT, buff=1
        )
        self.playw(
            LaggedStart(*[FadeIn(item) for item in first], lag_ratio=0.2), run_time=1
        )
        self.playw(
            LaggedStart(*[FadeIn(item) for item in second], lag_ratio=0.2), run_time=1
        )


class firstPrelim(Scene2D):
    def construct(self):
        prelim1 = Text(
            "What is Diffusion?", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim2 = Text(
            "How Diffusion works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim3 = Text(
            "How Transformer works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)

        prelims = VGroup(prelim1, prelim2, prelim3).arrange(
            DOWN, buff=0.75, aligned_edge=LEFT
        )

        self.playw(
            LaggedStart(*[FadeIn(item) for item in prelims], lag_ratio=0.2), wait=2
        )

        self.play(FadeOut(prelim2, prelim3))
        self.playw(prelim1.animate.move_to(ORIGIN).scale(1.25))

        px = MathTex("p(x)", font_size=64).set_color_by_gradient(BLUE_A, BLUE_C)
        self.playw(
            Transform(prelim1[:4], px[0][0], replace_mobject_with_target_in_scene=True),
            Transform(
                prelim1[4:6], px[0][1], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                prelim1[6:-1], px[0][2], replace_mobject_with_target_in_scene=True
            ),
            Transform(prelim1[-1], px[0][3], replace_mobject_with_target_in_scene=True),
            wait=2,
        )

        self.play(Wiggle(px, scale_value=1.2))
        cat = ImageMobject("cat.jpg").scale(0.3).next_to(px, UR)
        self.playw(FadeIn(cat, scale=0.5, target_position=px))

        pz = MathTex("p(z)", "=", "N(0, I)", font_size=64, color=RED_A)

        self.play(FadeOut(cat), px.animate.shift(UP * 5))
        self.playw(FadeIn(pz[0]))
        self.playw(FadeIn(pz[1], pz[2]))
        self.playw(Wiggle(pz, scale_value=1.2))

        cat_array = np.array(Image.open("cat.jpg").convert("RGB"))
        noise_array = np.random.randint(0, 256, cat_array.shape).astype(np.uint8)
        noise = ImageMobject(noise_array).scale(0.3).next_to(pz[0], UP)
        self.playw(FadeIn(noise, scale=0.5, target_position=pz[0]))
        self.playw(pz.animate.set_color(PURE_RED))

        z = (
            MathTex("Z", r"\sim", font_size=64)
            .set_color_by_gradient(RED_A, RED_B)
            .move_to(noise)
        )
        z[1].set_opacity(0)
        self.play(FadeTransform(noise, z))
        self.play(z.animate.next_to(pz, LEFT, buff=0.5))
        self.playw(z[1].animate.set_opacity(1))

        comma = (
            MathTex(",", font_size=48)
            .next_to(z[0])
            .align_to(z[0], DOWN)
            .shift(DOWN * 0.1)
            .set_opacity(0)
        )
        model = (
            MathTex("model", "_", r"{\theta}", "(", ")", font_size=60)
            .next_to(z, buff=0.3)
            .set_opacity(0)
        )
        self.play(
            pz.animate.shift(UP * 2).scale(0.8).set_color(GREY_B),
            z[1].animate.set_opacity(0),
        )
        self.play(VGroup(z, comma, model).animate.move_to(ORIGIN))
        self.playw(VGroup(comma, model).animate.set_opacity(1))
        fn = MathTex("f", "(", ")", font_size=60, color=YELLOW)
        fn[:2].next_to(z, LEFT)
        fn[2].next_to(model, RIGHT)
        self.playw(FadeIn(fn))
        cat.next_to(fn, DOWN)
        cat_eq = VGroup(fn, z, comma, model).copy()
        self.playw(FadeTransform(cat_eq, cat))
        x = MathTex("X", font_size=64).next_to(cat, RIGHT).set_z_index(-1)
        self.play(
            FadeIn(x, shift=RIGHT),
            VGroup(fn, z[0], comma, model).animate.set_opacity(0.5),
        )
        self.play(x.animate.scale(1.2), cat.animate.scale(1.2))
        self.playw(x.animate.scale(1 / 1.2), cat.animate.scale(1 / 1.2))

        px2 = px.copy()
        sim = MathTex(r"\sim", font_size=64)
        px2 = VGroup(sim, px2).arrange(RIGHT).next_to(x)
        self.playw(FadeIn(px2))

        self.playw(
            cat.animate.set_opacity(0.3),
            VGroup(x, px2).animate.set_opacity(0.3),
            VGroup(fn, z[0], comma, model).animate.set_opacity(1),
        )

        self.playw(Circumscribe(z[0]))
        self.playw(Circumscribe(model))
        self.playw(Indicate(fn))

        px2.generate_target().next_to(fn, UR).rotate(20 * DEGREES).set_opacity(1)
        self.playw(MoveToTarget(px2))

        self.play(LaggedStart(*[Indicate(item) for item in [z, model, fn]]))
        catc = cat.copy().set_opacity(1)
        self.playw(FadeIn(catc, scale=0.5, target_position=fn))


class secondPrelim(Scene2D):
    def construct(self):
        prelim1 = Text(
            "What is Diffusion?", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim2 = Text(
            "How Diffusion works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim3 = Text(
            "How Transformer works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)

        prelims = VGroup(prelim1, prelim2, prelim3).arrange(
            DOWN, buff=0.75, aligned_edge=LEFT
        )

        self.addw(prelims, wait=2)
        self.playw(FadeOut(prelim1, prelim3))

        process = VGroup(
            Text(
                "1. Tractable p(z)", font_size=32, font="Noto Serif"
            ).set_color_by_gradient(GREY_A, GREY_B),
            Text(
                "2. Deeplearning Model", font_size=32, font="Noto Serif"
            ).set_color_by_gradient(GREY_A, GREY_B),
            Text("3. f( )", font_size=32, font="Noto Serif").set_color_by_gradient(
                GREY_A, GREY_B
            ),
        ).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        self.playw(
            LaggedStart(
                *[
                    Transform(pre, item, replace_mobject_with_target_in_scene=True)
                    for pre, item in zip(
                        [prelim2[:3], prelim2[3:11], prelim2[11:]], process
                    )
                ],
                lag_ratio=0.2,
            )
        )
        self.playw(Circumscribe(process[2], buff=0.05))
        denoising = (
            Text("3. Sequential Denoising", font_size=32, font="Noto Serif")
            .set_color_by_gradient(YELLOW_A, YELLOW)
            .move_to(process[2])
            .align_to(process[2], LEFT)
        )
        self.playw(
            Transform(process[2], denoising, replace_mobject_with_target_in_scene=True)
        )

        mul1 = (
            Text("1000×", font_size=24, font="Noto Serif")
            .set_color_by_gradient(RED_A, RED_C)
            .next_to(denoising, DOWN, buff=0.1)
        )
        mul2 = (
            Text("250×", font_size=24, font="Noto Serif")
            .set_color_by_gradient(RED_A, RED_C)
            .move_to(mul1)
        )
        self.play(FadeIn(mul1, scale=0.5, shift=DOWN * 0.5))
        self.playw(Transform(mul1, mul2, replace_mobject_with_target_in_scene=True))

        noise_array = np.random.randint(0, 256, (826, 831, 3)).astype(np.uint8)
        noise = (
            ImageMobject(noise_array)
            .scale(128 / 826)
            .next_to(process[0], RIGHT, buff=2.2)
        )
        self.playw(FadeIn(noise, scale=0.5, shift=RIGHT))

        self.play(noise.animate.move_to(process[1]).align_to(noise, RIGHT))
        self.playw(noise.animate.move_to(process[2]).align_to(noise, RIGHT))

        t = 0.001
        eq = interp(t).next_to(noise, RIGHT)
        self.playw(FadeIn(eq))
        for i in range(5):
            t += 0.001
            self.play(noise.animate.move_to(process[1]).align_to(noise, RIGHT))
            self.play(noise.animate.move_to(process[2]).align_to(noise, RIGHT))
            self.playw(eq.animate.become(interp(t)).next_to(noise, RIGHT))
        cat = denoised(1.0).move_to(noise).scale(128 / 826)
        self.play(noise.animate.move_to(process[1]).align_to(noise, RIGHT))
        self.play(noise.animate.become(cat))
        self.playw(eq.animate.become(interp(1.0)).next_to(noise, RIGHT))


def denoised(x):
    cat = np.array(Image.open("cat.jpg").convert("RGB"))
    noise = np.random.randint(0, 256, cat.shape).astype(np.uint8)

    _denoised = x * cat.astype(np.float32) + (1 - x) * noise.astype(np.float32)
    _denoised = np.clip(_denoised, 0, 255).astype(np.uint8)
    return ImageMobject(_denoised)


def interp(a):
    return MathTex(
        f"{a:.3f}", "X", "+", f"{1-a:.3f}", "Z", font_size=32
    ).set_color_by_gradient(BLUE_A, BLUE_B)


class secondPrelim2(Scene2D):
    def construct(self):
        process = VGroup(
            Text(
                "1. Tractable p(z)", font_size=32, font="Noto Serif"
            ).set_color_by_gradient(GREY_A, GREY_B),
            Text(
                "2. Deeplearning Model", font_size=32, font="Noto Serif"
            ).set_color_by_gradient(GREY_A, GREY_B),
            Text(
                "3. Sequential Denoising", font_size=32, font="Noto Serif"
            ).set_color_by_gradient(YELLOW_A, YELLOW),
        ).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        mul = (
            Text("250×", font_size=24, font="Noto Serif")
            .set_color_by_gradient(RED_A, RED_C)
            .next_to(process[2], DOWN, buff=0.1)
        )

        self.addw(process, mul, wait=2)
        process3 = (
            Text("3. #$%^&", font_size=32, font="Noto Serif")
            .set_color_by_gradient(YELLOW_A, YELLOW)
            .move_to(process[2])
            .align_to(process[2], LEFT)
        )
        self.play(FadeTransform(process[2][2:], process3[2:]))
        self.playw(FadeTransform(process3[2:], process[2][2:]))

        self.cf.save_state()
        self.playw(self.cf.animate.shift(RIGHT * 10))

        cat = denoised(1.0).scale(192 / 826)
        noise = denoised(0.0).scale(192 / 826)
        Group(cat, noise).arrange(RIGHT, buff=1.5).move_to(self.cf)
        latent = denoised(0.5).move_to(self.cf).scale(192 / 826)
        self.play(FadeIn(cat, noise))
        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(cat, target_position=self.cf, scale=0.7),
                    FadeOut(noise.copy(), target_position=self.cf, scale=0.7),
                ),
                FadeIn(latent, scale=0.7, target_position=self.cf),
                lag_ratio=0.2,
            )
        )

        modelt = (
            MathTex(r"Model_{\theta}", "(", ")", font_size=48)
            .set_color_by_gradient(GREY_A, GREY_B)
            .move_to(self.cf)
            .set_z_index(1)
        )
        model_rect = (
            Rectangle(width=3.5, height=2, stroke_width=2, color=GREY_B)
            .set_fill(BLACK, opacity=1)
            .move_to(modelt)
            .set_z_index(0.5)
        )
        model = VGroup(modelt, model_rect).shift(UP * 2.5)
        self.play(FadeIn(model_rect))
        self.play(latent.animate.move_to(model))
        output = denoised(0.0).move_to(model).scale(192 / 826)
        self.playw(output.animate.align_to(noise, DOWN), noise.animate.shift(RIGHT * 2))

        lossline = DashedLine(output.get_right(), noise.get_left(), color=GREY_B)
        loss = (
            MathTex(r"\mathcal{L}", font_size=48)
            .set_color_by_gradient(RED_A, RED_C)
            .next_to(lossline, UP)
        )
        self.playw(FadeIn(loss, lossline))
        self.playw(FadeIn(modelt))

        xt = MathTex("x_t", font_size=48).shift(LEFT * 5 + DOWN * 0.5)
        xtimg = denoised(0.5).scale(0.2).next_to(xt, UP, buff=0.05)
        self.add(xt, xtimg)

        self.playw(
            self.cf.animate.restore().shift(LEFT * 4),
            modelt.animate.move_to(self.cf.saved_state)
            .shift(LEFT * 5)
            .align_to(modelt, UP),
        )

        xt = Group(xt, xtimg)
        self.play(
            modelt[-1].animate.shift(RIGHT * 1.4),
            xt.animate.next_to(modelt[1], RIGHT, buff=0.1),
        )
        noise = denoised(0.0).scale(0.2).shift(LEFT * 5)
        self.playw(
            FadeTransform(VGroup(modelt, xt[0]).copy(), noise),
            FadeOut(xt[1].copy(), target_position=noise),
            Circumscribe(process[1]),
        )

        self.playw(Wiggle(noise, scale_value=1.2))
        self.playw(Indicate(modelt))
        self.playw(self.cf.animate.shift(RIGHT * 4), FadeOut(modelt, xt, noise, mul))
        self.playw(Circumscribe(process[1]))
        self.playw(Circumscribe(process[2]))


class thirdPrelim(Scene2D):
    def construct(self):
        prelim1 = Text(
            "What is Diffusion?", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim2 = Text(
            "How Diffusion works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim3 = Text(
            "How Transformer works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)

        prelims = VGroup(prelim1, prelim2, prelim3).arrange(
            DOWN, buff=0.75, aligned_edge=LEFT
        )

        self.addw(prelims, wait=2)
        self.play(FadeOut(prelim1, prelim2))
        self.playw(prelim3.animate.move_to(ORIGIN).scale(1.25))
        self.play(prelim3.animate.shift(LEFT * 15))

        img = ImageMobject("tstructure.png").scale(1.2).shift(UP * 0.5)
        self.playw(FadeIn(img), wait=4)

        encoder = RoundedRectangle(
            width=1.4, height=2.1, color=GREEN_A, corner_radius=0.1
        ).set_z_index(1)
        decoder = RoundedRectangle(
            width=1.4, height=3.1, color=BLUE_A, corner_radius=0.1
        ).set_z_index(1)
        model = VGroup(encoder, decoder).arrange(RIGHT, buff=0.25).move_to(img)
        encoder.shift(DOWN * 0.3)
        decoder.shift(UP * 0.2)
        enct = (
            Text("Encoder", font_size=16, font="Noto Serif")
            .set_color(GREEN_A)
            .next_to(encoder, LEFT, buff=0.1)
            .align_to(encoder, UP)
        )
        dect = (
            Text("Decoder", font_size=16, font="Noto Serif")
            .set_color(BLUE_A)
            .next_to(decoder, RIGHT, buff=0.1)
            .align_to(decoder, UP)
        )
        self.play(FadeOut(img), FadeIn(model, enct, dect))
        self.playw(VGroup(model, enct, dect).animate.scale(1.5).shift(UP * 0.1))
        decoder.set_z_index(0.5).set_fill(BLACK, opacity=0.8)
        dec_in = (
            Tensor(3, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, DOWN)
            .shift(LEFT * 0.3)
            .set_z_index(-1)
        )
        self.playw(FadeIn(dec_in))
        dec_out = (
            Tensor(3, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, UP)
            .shift(LEFT * 0.3)
            .set_z_index(-1)
        )
        self.playw(FadeTransform(dec_in.copy(), dec_out))
        sample = dec_out[-1]
        self.play(
            sample.animate.next_to(dect, RIGHT, buff=0.1).align_to(sample, UP),
            rate_func=linear,
            run_time=0.4,
        )
        self.play(
            sample.animate.align_to(dec_in, DOWN),
            FadeOut(dec_out[:-1]),
            rate_func=linear,
            run_time=0.8,
        )
        self.playw(
            sample.animate.next_to(dec_in, RIGHT, buff=0.1),
            rate_func=linear,
            run_time=0.3,
        )

        words_string = [
            "Some",
            "call",
            "me",
            "nature,",
        ]
        dec_in = VGroup(*dec_in, sample)
        words = VGroup(
            *[
                Text(word, font_size=18, font="Noto Serif")
                .set_color_by_gradient(GREY_A, GREY_B)
                .rotate(PI / 2)
                .move_to(dec_in[i])
                .align_to(dec_in[i], UP)
                for i, word in enumerate(words_string)
            ]
        )
        self.playw(Transform(dec_in, words))

        dec_out = (
            Tensor(4, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, UP)
            .shift(LEFT * 0.3)
            .set_z_index(-1)
        )
        self.playw(FadeTransform(dec_in.copy(), dec_out))
        sample = dec_out[-1]
        samplet = (
            Text("others", font_size=18, font="Noto Serif")
            .set_color_by_gradient(GREY_A, GREY_B)
            .rotate(PI / 2)
            .move_to(sample)
        )
        self.play(
            sample.animate.become(samplet)
            .next_to(dect, RIGHT, buff=0.1)
            .align_to(sample, UP),
            rate_func=linear,
            run_time=0.4,
        )
        self.play(
            sample.animate.align_to(dec_in, DOWN),
            FadeOut(dec_out[:-1]),
            rate_func=linear,
            run_time=0.8,
        )
        self.playw(
            sample.animate.next_to(dec_in, RIGHT, buff=0.2).align_to(dec_in, UP),
            rate_func=linear,
            run_time=0.3,
        )
        decoder.generate_target().stretch_to_fit_width(2.75 * 1.5).align_to(
            decoder, LEFT
        )
        self.playw(
            MoveToTarget(decoder),
            dect.animate.next_to(decoder.target, RIGHT, buff=0.1).align_to(
                decoder.target, UP
            ),
        )

        dec_in = VGroup(*dec_in, sample)
        dec_out = (
            Tensor(5, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, UP)
            .align_to(dec_in, LEFT)
            .set_z_index(-1)
        )
        self.playw(FadeTransform(dec_in.copy(), dec_out))
        sample = dec_out[-1]
        samplet = (
            Text("call", font_size=18, font="Noto Serif")
            .set_color_by_gradient(GREY_A, GREY_B)
            .rotate(PI / 2)
            .move_to(sample)
        )
        self.cf.save_state()
        self.playw(self.cf.animate.move_to(dec_out).scale(0.4))

        self.playw(sample.animate.become(samplet))
        self.playw(Restore(self.cf))
        self.play(
            LaggedStart(Circumscribe(dec_out), Circumscribe(dec_in), lag_ratio=0.4)
        )
        shape_in = Text("[B, 7, D]", font_size=18, font=MONO_FONT).next_to(
            dec_in, RIGHT
        )
        shape_out = Text("[B, 7, D]", font_size=18, font=MONO_FONT).next_to(
            dec_out, RIGHT
        )
        outs = (
            VGroup(
                Text("call", font_size=18, font="Noto Serif").rotate(PI / 2),
                Text("me", font_size=18, font="Noto Serif").rotate(PI / 2),
                Text("mother,", font_size=18, font="Noto Serif").rotate(PI / 2),
                Text("nature,", font_size=18, font="Noto Serif").rotate(PI / 2),
            )
            .arrange(RIGHT)
            .next_to(dec_in, RIGHT)
        )
        self.playw(FadeIn(shape_in, shape_out, shift=RIGHT * 0.4))
        self.playw(FadeOut(shape_in, shape_out))
        self.playw(LaggedStart(*[FadeIn(item) for item in outs], lag_ratio=0.8))
        self.play(FadeOut(outs))
        self.play(
            sample.animate.next_to(dect, RIGHT, buff=0.1).align_to(sample, UP),
            rate_func=linear,
            run_time=0.5,
        )
        self.play(
            sample.animate.align_to(dec_in, UP),
            FadeOut(dec_out[:-1]),
            rate_func=linear,
            run_time=0.8,
        )
        self.playw(
            sample.animate.next_to(dec_in, RIGHT, buff=0.2).align_to(dec_in, UP),
            rate_func=linear,
            run_time=0.5,
        )

        dec_in = VGroup(*dec_in, sample)
        dec_out = (
            Tensor(6, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, UP)
            .align_to(dec_in, LEFT)
            .set_z_index(-1)
        )
        self.play(FadeTransform(dec_in.copy(), dec_out))
        sample = dec_out[-1]
        samplet = (
            Text("me", font_size=18, font="Noto Serif")
            .set_color_by_gradient(GREY_A, GREY_B)
            .rotate(PI / 2)
            .move_to(sample)
        )
        self.play(sample.animate.become(samplet))
        self.play(
            sample.animate.next_to(dect, RIGHT, buff=0.1).align_to(sample, UP),
            rate_func=linear,
            run_time=0.5,
        )
        self.play(
            sample.animate.align_to(dec_in, UP),
            FadeOut(dec_out[:-1]),
            rate_func=linear,
            run_time=0.8,
        )
        self.play(
            sample.animate.next_to(dec_in, RIGHT, buff=0.2).align_to(dec_in, UP),
            rate_func=linear,
            run_time=0.5,
        )

        dec_in = VGroup(*dec_in, sample)
        dec_out = (
            Tensor(7, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, UP)
            .align_to(dec_in, LEFT)
            .set_z_index(-1)
        )
        self.play(FadeTransform(dec_in.copy(), dec_out))
        sample = dec_out[-1]
        samplet = (
            Text("mother,", font_size=18, font="Noto Serif")
            .set_color_by_gradient(GREY_A, GREY_B)
            .rotate(PI / 2)
            .move_to(sample)
        )
        self.play(sample.animate.become(samplet))
        self.play(
            sample.animate.next_to(dect, RIGHT, buff=0.1).align_to(sample, UP),
            rate_func=linear,
            run_time=0.5,
        )
        self.play(
            sample.animate.align_to(dec_in, UP),
            FadeOut(dec_out[:-1]),
            rate_func=linear,
            run_time=0.8,
        )
        self.play(
            sample.animate.next_to(dec_in, RIGHT, buff=0.2).align_to(dec_in, UP),
            rate_func=linear,
            run_time=0.5,
        )
        dec_in = VGroup(*dec_in, sample)
        dec_out = (
            Tensor(8, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.8)
            .next_to(decoder, UP)
            .align_to(dec_in, LEFT)
            .set_z_index(-1)
        )
        self.play(FadeTransform(dec_in.copy(), dec_out))
        sample = dec_out[-1]
        samplet = (
            Text("nature,", font_size=18, font="Noto Serif")
            .set_color_by_gradient(GREY_A, GREY_B)
            .rotate(PI / 2)
            .move_to(sample)
        )
        self.play(sample.animate.become(samplet))
        self.play(
            sample.animate.next_to(dect, RIGHT, buff=0.1).align_to(sample, UP),
            rate_func=linear,
            run_time=0.5,
        )
        self.play(
            sample.animate.align_to(dec_in, UP),
            FadeOut(dec_out[:-1]),
            rate_func=linear,
            run_time=0.8,
        )
        self.play(
            sample.animate.next_to(dec_in, RIGHT, buff=0.2).align_to(dec_in, UP),
            rate_func=linear,
            run_time=0.5,
        )
        self.playw(
            sample.animate.next_to(dec_in, RIGHT, buff=0.2).align_to(dec_in, UP),
            rate_func=linear,
            run_time=0.5,
        )

        dec_in = VGroup(*dec_in, sample)
        dec_in.generate_target()
        for item in dec_in.target:
            item.rotate(-PI / 2)
            dec_in.target.arrange(RIGHT, buff=0.1).move_to(dec_in).align_to(
                dec_in, LEFT
            )
        self.playw(
            self.cf.animate.move_to(dec_in.target).scale(0.6),
            MoveToTarget(dec_in),
        )


class whatDiTdoes(Scene2D):
    def construct(self):
        prelim1 = Text(
            "What is Diffusion?", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim2 = Text(
            "How Diffusion works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        prelim3 = Text(
            "How Transformer works", font_size=36, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)

        prelims = VGroup(prelim1, prelim2, prelim3).arrange(
            DOWN, buff=0.75, aligned_edge=LEFT
        )

        self.addw(prelims)
        self.play(
            FadeOut(prelim1, scale=0.7, target_position=prelim2),
            FadeOut(prelim2, scale=0.7),
            FadeOut(prelim3, scale=0.7, target_position=prelim2),
        )
        dit_full = Text(
            "Diffusion Transformer", font_size=48, font="Noto Serif"
        ).set_color_by_gradient(GREEN_B, GREEN_D)
        dit_fullc = dit_full.copy()
        self.playw(FadeIn(dit_full, scale=0.7))
        dit = Text("DiT", font_size=48, font="Noto Serif").set_color_by_gradient(
            YELLOW_A, YELLOW
        )
        self.playw(
            LaggedStart(
                AnimationGroup(
                    FadeOut(dit_full[2:8], scale=0.7), FadeOut(dit_full[9:], scale=0.7)
                ),
                AnimationGroup(
                    Transform(
                        dit_full[:2], dit[:2], replace_mobject_with_target_in_scene=True
                    ),
                    Transform(
                        dit_full[8], dit[2], replace_mobject_with_target_in_scene=True
                    ),
                ),
                lag_ratio=0.3,
            )
        )

        first = Text(
            "What DiT does", font_size=48, font="Noto Serif"
        ).set_color_by_gradient(YELLOW_A, YELLOW_C)
        self.playw(
            FadeIn(first[:4], scale=0.7),
            Transform(dit, first[4:7], replace_mobject_with_target_in_scene=True),
            FadeIn(first[7:]),
        )
        dit_fullc.next_to(first[4:7], UP).scale(0.7).set_opacity(0)
        self.playw(
            dit_fullc.animate.set_opacity(1),
            first[:4].animate.set_opacity(0.3),
            first[7:].animate.set_opacity(0.3),
        )
        self.play(Indicate(dit_fullc[:8], scale_factor=1.1))
        self.playw(Indicate(dit_fullc[8:], scale_factor=1.1))

        dit = first[4:7]
        self.play(
            FadeOut(dit_fullc),
            FadeOut(first[:4]),
            FadeOut(first[7:]),
        )
        model_rect = (
            RoundedRectangle(
                corner_radius=0.1, width=3.5, height=2, stroke_width=2, color=GREY_B
            )
            .set_fill(BLACK, opacity=0.6)
            .move_to(dit)
            .set_z_index(-1)
        )
        self.playw(FadeIn(model_rect))
        model = VGroup(dit, model_rect)

        cat = denoised(1.0).scale(192 / 826)
        noise = denoised(0.0).scale(192 / 826)
        Group(cat, noise).arrange(DOWN, buff=1.5).next_to(
            model, LEFT, buff=1.5
        ).set_z_index(-2)
        latent = (
            denoised(0.5)
            .move_to(Group(cat, noise))
            .scale(192 / 826)
            .set_z_index(-3)
            .set_opacity(0)
        )
        self.playw(FadeIn(cat, noise))
        self.playw(
            LaggedStart(
                AnimationGroup(
                    FadeOut(cat, target_position=latent),
                    FadeOut(noise, target_position=latent),
                ),
                latent.animate.set_opacity(1),
                lag_ratio=0.3,
            )
        )
        output = (
            denoised(0.0)
            .scale(192 / 826)
            .next_to(model, RIGHT, buff=1.5)
            .set_z_index(-3)
        )
        self.playw(
            Transform(latent.copy(), output, replace_mobject_with_target_in_scene=True)
        )

        self.playw(Circumscribe(latent))
        self.playw_return(model.animate.scale(1.2))
        self.playw(Circumscribe(output))

        #

        self.playw(Wiggle(dit))
        shape_in = Text("[?, ?, ?, ?]", font_size=18, font=MONO_FONT).next_to(
            latent, DOWN
        )
        shape_out = Text("[?, ?, ?, ?]", font_size=18, font=MONO_FONT).next_to(
            output, DOWN
        )
        self.playw(
            LaggedStart(
                *[FadeIn(item) for item in [shape_in, shape_out]], lag_ratio=0.3
            )
        )
        shape_in.generate_target().become(
            Text("[B, H, W, C]", font_size=18, font=MONO_FONT).next_to(latent, DOWN)
        )
        shape_out.generate_target().become(
            Text("[B, H, W, C]", font_size=18, font=MONO_FONT).next_to(output, DOWN)
        )
        self.playw(
            MoveToTarget(shape_in),
            MoveToTarget(shape_out),
        )

        shape = Text("[32, 32, 4]", font_size=24, font=MONO_FONT).next_to(
            latent, UR, buff=1
        )
        dl1 = DashedLine(shape, latent.get_top(), buff=0.1, color=GREY_B)
        dl2 = DashedLine(shape.get_right(), output.get_top(), buff=0.1, color=GREY_B)
        self.playw(
            LaggedStart(FadeIn(shape), Create(dl1), Create(dl2), lag_ratio=0.3),
            run_time=1.5,
        )
        shape_in.save_state()
        shape_out.save_state()
        self.playw(
            Transform(
                shape_in,
                Text("[B, 32, 32, 4]", font_size=18, font=MONO_FONT).next_to(
                    latent, DOWN
                ),
            ),
            Transform(
                shape_out,
                Text("[B, 32, 32, 4]", font_size=18, font=MONO_FONT).next_to(
                    output, DOWN
                ),
            ),
        )
        self.playw(Circumscribe(shape_in))
        self.playw(Circumscribe(shape_out))

        #

        self.playw(FadeOut(shape, dl1, dl2), Restore(shape_in), Restore(shape_out))
        self.play(
            FadeOut(latent, output, shape_in, shape_out),
            model_rect.animate.set_opacity(0),
        )
        self.playw(model.animate.shift(LEFT * 4), wait=4)
        dots = (
            VGroup(*[Dot(color=random_color()) for _ in range(16)])
            .arrange_in_grid(4, 4, buff=0.1)
            .next_to(model, DOWN, buff=0.5)
            .set_z_index(-2)
        )
        self.playw(FadeIn(dots), model_rect.animate.set_opacity(1))
        dotso = dots.copy().next_to(model, UP, buff=0.5)
        for d in dotso:
            d.set_color(random_color())
        self.playw(Transform(dots, dotso))
        self.playw(Circumscribe(dots))


class unmaskedDiT(Scene2D):
    def construct(self):
        dummy = (
            Tensor(1, shape="square", arrange=UP)
            .shift(DOWN * 1.5 + LEFT * 2)
            .scale(1.2)
        )
        query = (
            Tensor(5, shape="square", arrange=UP, buff=0.25)
            .scale(1.2)
            .next_to(dummy, UP)
        )
        key = (
            Tensor(5, shape="square", arrange=RIGHT, buff=0.25)
            .scale(1.2)
            .next_to(dummy, RIGHT)
        )
        qt = (
            Text("Query", font_size=18, font="Noto Serif")
            .next_to(query, UP, buff=0.1)
            .align_to(query, RIGHT)
        )
        kt = Text("Key", font_size=18, font="Noto Serif").next_to(key, RIGHT, buff=0.1)
        qidx = VGroup(
            *[
                Text(str(i), font_size=14, font="Noto Serif")
                .next_to(query[i - 1], LEFT, buff=0.05)
                .align_to(query[i - 1], DOWN)
                for i in range(1, 6)
            ]
        )
        kidx = VGroup(
            *[
                Text(str(i), font_size=14, font="Noto Serif")
                .next_to(key[i - 1], DOWN, buff=0.05)
                .align_to(key[i - 1], RIGHT)
                for i in range(1, 6)
            ]
        )

        self.playw(FadeIn(query, key, qt, kt, qidx, kidx))

        logits = (
            VGroup(*[Dot(color=random_bright_color()) for _ in range(25)])
            .arrange_in_grid(5, 5, buff=0.6, flow_order="ru")
            .next_to(query, RIGHT, buff=0.45)
        )
        tfs = []
        for i in range(25):
            tfs.append(
                Transform(
                    VGroup(query[i // 5].copy(), key[i % 5].copy()),
                    logits[i],
                    replace_mobject_with_target_in_scene=True,
                )
            )
        self.playw(LaggedStart(*tfs, lag_ratio=0.25))

        belowright = VGroup(*[logits[i] for i in range(25) if i % 5 > i // 5])
        self.playw(belowright.animate.set_opacity(0.15))
        self.playw_return(belowright.animate.set_opacity(1).set_color(PURE_RED))

        t = 2
        (qts := query[t:]).generate_target().set_opacity(0)
        (kts := key[t:]).generate_target().set_opacity(0)
        (qidxs := qidx[t:]).generate_target().set_opacity(0)
        (kidxs := kidx[t:]).generate_target().set_opacity(0)
        (lts := logits[t*5:]).generate_target().set_opacity(0)
        self.playw(
            MoveToTarget(qts),
            MoveToTarget(kts),
            MoveToTarget(qidxs),
            MoveToTarget(kidxs),
            MoveToTarget(lts),
        )
        self.play(Circumscribe(VGroup(query[1], key[1], qidx[1], kidx[1])))
        lts_ = VGroup(logits[1:5], logits[7:10])
        self.playw(FadeOut(lts_))
