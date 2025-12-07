from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        alt = Words("accelerate launch main.py", font_size=32, font=MONO_FONT)
        alt.words[-1].set_color(GREY_C)
        alt.words[:-1].set_color(YELLOW_B)

        self.playwl(*[FadeIn(item) for item in alt.words], lag_ratio=0.5)
        acc1 = (
            Text("check the number of GPU", font_size=24, color=GREY_C)
            .next_to(alt, UP, buff=0.5)
            .align_to(alt, LEFT)
        )
        acc2 = (
            Text("check dynamo-backend", font_size=24, color=GREY_C)
            .next_to(alt, UP, buff=0.5)
            .align_to(alt, LEFT)
        )
        acc3 = (
            Text("check mixed precision", font_size=24, color=GREY_C)
            .next_to(alt, UP, buff=0.5)
            .align_to(alt, LEFT)
        )
        pt = Words("python main.py", font_size=32, font=MONO_FONT).align_to(alt, RIGHT)
        pt.words[-1].set_color(GREY_C)
        pt.words[0].set_color(YELLOW_B)

        self.play(FadeIn(acc1, shift=UP * 0.3))
        self.play(FadeIn(acc2, shift=UP * 0.3), acc1.animate.shift(UP * 0.5))
        self.play(
            FadeIn(acc3, shift=UP * 0.3),
            acc2.animate.shift(UP * 0.5),
            acc1.animate.shift(UP * 0.5),
        )
        self.play(
            Transform(
                alt.words[:2], pt.words[0], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                alt.words[2], pt.words[1], replace_mobject_with_target_in_scene=True
            ),
        )
        self.playw(pt.animate.move_to(ORIGIN))


class num_processes(Scene2D):
    def construct(self):
        act = Text("accelerate", font_size=36).set_color_by_gradient(YELLOW_A, YELLOW_C)
        acc1 = Words("Multi-GPU", font_size=32).set_color_by_gradient(GREEN_A, GREEN_C)
        acc2 = Words("Mixed Precision", font_size=32).set_color_by_gradient(
            GREEN_A, GREEN_C
        )
        accs = VGroup(acc1, acc2).arrange(RIGHT, buff=1.5).next_to(act, DOWN, buff=0.5)
        self.playwl(*[FadeIn(item) for item in act], lag_ratio=0.1)
        self.playw(FadeIn(acc1))
        self.playw(FadeIn(acc2))

        self.play(FadeOut(act, acc2))
        self.playw(acc1.animate.move_to(ORIGIN))
        bs = 16
        data = (
            VGroup(
                *[
                    RoundedRectangle(
                        height=0.5,
                        width=0.8,
                        corner_radius=0.1,
                        stroke_color=GREY_B,
                        stroke_width=3,
                        fill_opacity=1,
                        fill_color=BLACK,
                    )
                    for _ in range(bs)
                ]
            )
            .arrange(DR + RIGHT * 0.5, buff=-0.4)
            .set_z_index(1)
        )
        datat = Text("data", font_size=24, font="Noto Sans KR").next_to(
            data, DOWN, buff=0.1
        )
        self.playwl(
            acc1.animate.shift(UP * 2.5), FadeIn(data), FadeIn(datat), lag_ratio=0.5
        )
        b1, b2, b3, b4 = [data[i : i + 4] for i in range(0, bs, 4)]

        def get_gpu():
            gpub = Rectangle(color=GREY_C, height=2, width=3).scale(0.7)
            gput = (
                Text("GPU", font_size=20, color=GREY_B)
                .next_to(gpub, UP, buff=0.05)
                .align_to(gpub, LEFT)
            )
            gpu = VGroup(gput, gpub)

            return gpu

        gpus = VGroup(*[get_gpu() for _ in range(4)]).arrange(RIGHT, buff=1)
        self.playw(
            FadeIn(gpus, shift=UP),
            FadeOut(datat),
            *[b.animate.move_to(gpus[i][1]) for i, b in enumerate([b1, b2, b3, b4])],
        )

        cmd = Words(
            "accelerate launch --num_processes 4 main.py", font=MONO_FONT, font_size=24
        ).next_to(gpus, DOWN, buff=0.75)
        cmd.words[-1].set_color(GREY_C)
        cmd.words[2:4].set_color(YELLOW_B)
        cmd.words[:2].set_color(GREY_A)

        self.playwl(*[FadeIn(item) for item in cmd.words], lag_ratio=0.3)

        self.wait(2)

        self.playw(
            *[
                Rotating(
                    VGroup(gpus[i], b), radians=TAU * 3, rate_func=smooth, run_time=2
                )
                for i, b in enumerate([b1, b2, b3, b4])
            ]
        )


class mixed_precision(Scene2D):
    def construct(self):
        act = Text("accelerate", font_size=36).set_color_by_gradient(YELLOW_A, YELLOW_C)
        acc1 = Words("Multi-GPU", font_size=32).set_color_by_gradient(GREEN_A, GREEN_C)
        acc2 = Words("Mixed Precision", font_size=32).set_color_by_gradient(
            GREEN_A, GREEN_C
        )
        accs = VGroup(acc1, acc2).arrange(RIGHT, buff=1.5).next_to(act, DOWN, buff=0.5)
        self.addw(act, accs)

        self.play(FadeOut(act, acc1))
        self.playw(acc2.animate.move_to(ORIGIN))

        model = Rectangle(width=4, height=2, color=BLUE_C, fill_opacity=0)
        modelt = (
            Text("model", font_size=18, font="Noto Sans KR")
            .next_to(model, UP, buff=0.1)
            .align_to(model, LEFT)
        )
        self.play(acc2.animate.shift(UP * 2.5))
        self.playw(FadeIn(model), FadeIn(modelt))

        model_dtype = Words(
            "model.dtype = float32", font_size=18, font=MONO_FONT
        ).move_to(model)
        model_dtype_ = Words(
            "model.dtype = float16", font_size=18, font=MONO_FONT
        ).move_to(model)

        self.playw(FadeIn(model_dtype))
        self.playw(Transform(model_dtype, model_dtype_))

        torch_mp = (
            Words("torch.cuda.amp", font_size=20, font=MONO_FONT)
            .set_color_by_gradient(RED_A, RED_C)
            .next_to(model, DOWN, buff=0.5)
        )
        self.playw(FadeIn(torch_mp))

        acc_mp = Words(
            "accelerate launch --mixed_precision='fp16' main.py",
            font=MONO_FONT,
            font_size=20,
        ).move_to(torch_mp)
        acc_mp.words[2].set_color(BLUE_C)
        acc_mp.words[:2].set_color(GREY_A)
        acc_mp.words[3:].set_color(GREY_C)
        self.play(FadeTransform(torch_mp, acc_mp))
        self.playw(Flash(acc_mp.words[2].get_corner(UL)))

        modules = (
            VGroup(
                Rectangle(
                    width=2.3, height=0.4, color=BLUE_D, fill_opacity=0, stroke_width=2
                ),
                Rectangle(
                    width=2.3, height=0.4, color=BLUE_D, fill_opacity=0, stroke_width=2
                ),
                Rectangle(
                    width=2.3, height=0.4, color=BLUE_D, fill_opacity=0, stroke_width=2
                ),
            )
            .arrange(DOWN, buff=0.15)
            .move_to(model)
        )
        self.playw(FadeOut(model_dtype), FadeIn(modules))

        a1 = Arrow(
            acc_mp.words[2][-3],
            modules[0].get_corner(DR),
            buff=0.05,
            stroke_width=2,
            tip_length=0.13,
        )
        a2 = Arrow(
            acc_mp.words[2][-3],
            modules[1].get_corner(DR),
            buff=0.05,
            stroke_width=2,
            tip_length=0.13,
        )
        a3 = Arrow(
            acc_mp.words[2][-3].get_top(),
            modules[2].get_corner(DR),
            buff=0.05,
            stroke_width=2,
            tip_length=0.13,
        )
        self.playwl(*[GrowArrow(a) for a in [a1, a2, a3]], lag_ratio=0.2)


class acc_code(Scene2D):
    def construct(self):
        title = Text(
            "코드에 필요한 것", font="Noto Sans KR", font_size=32
        ).set_color_by_gradient(GREEN_A, GREEN_C)
        self.play(FadeIn(title))
        self.playw(title.animate.to_edge(UP, buff=0.75))

        req1 = Words("acc = Accelerator()", font=MONO_FONT, font_size=24).set_color(
            GREY_A
        )
        req1[4:-2].set_color(YELLOW_B)
        req2 = Words(
            "dataloader, model, optim = acc.prepare(...)", font=MONO_FONT, font_size=24
        ).set_color(GREY_A)
        req2[-12:-5].set_color(YELLOW_B)
        req3 = Words("with acc.autocast():", font=MONO_FONT, font_size=24).set_color(
            GREY_A
        )
        req3[-11:-1].set_color(YELLOW_B)
        reqs = VGroup(req1, req2, req3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        self.playwl(*[FadeIn(item) for item in req1.words], lag_ratio=0.2)
        self.playwl(*[FadeIn(item) for item in req2.words], lag_ratio=0.2)
        self.playwl(*[FadeIn(item) for item in req3.words], lag_ratio=0.2)

        self.playw(VGroup(req2, req3).animate.shift(RIGHT * 15))

        mg = Text("Multi-GPU", font_size=28).set_color_by_gradient(BLUE_A, BLUE_C)
        mp = Text("Mixed Precision", font_size=28).set_color_by_gradient(BLUE_A, BLUE_C)
        settings = (
            VGroup(mg, mp)
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            .next_to(req1, RIGHT, buff=0.3)
        )

        self.play(FadeIn(mg))
        self.playw(FadeIn(mp))

        self.playw(req2.words[:3].animate.align_to(req1, LEFT))

        self.playwl(Flash(mg.get_corner(UL)), Flash(mp.get_corner(UL)), lag_ratio=0.5)
        self.playw(Flash(req1[4:-2].get_corner(UL)))

        self.play(req2.words[3:].animate.next_to(req2.words[:3], RIGHT))
        self.playw(
            FadeOut(mg, target_position=req2.words[0]),
            FadeOut(mp, target_position=req2.words[1]),
        )

        self.wait(2)

        self.playw(req3.animate.align_to(req1, LEFT))

        fprop = (
            Words("loss = model(data)", font=MONO_FONT, font_size=24)
            .set_color(GREY_A)
            .next_to(req3[3], RIGHT, buff=0.02)
            .shift(DOWN * 0.5)
        )
        self.play(FadeIn(fprop))
        self.playw(Wiggle(fprop.words[-1]))
