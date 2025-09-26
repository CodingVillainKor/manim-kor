from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        halfl = DashedLine(
            UP * 8,
            DOWN * 8,
            color=GREY_C,
            dash_length=0.1,
            dashed_ratio=0.6,
            stroke_width=1,
        )

        kvx = Text("KV cache X", font_size=24)
        kvx[-1].set_color(PURE_RED)
        kvo = Text("KV cache O", font_size=24)
        kvo[-1].set_color(PURE_GREEN)

        kvtext = VGroup(kvx, kvo).arrange(RIGHT, buff=0.5).shift(UP * 3.5)
        self.addw(halfl)

        model1 = (
            Rectangle(width=4.5, height=4, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.2)
            .set_z_index(1)
        )
        model2 = (
            Rectangle(width=4.5, height=4, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.2)
            .set_z_index(1)
        )
        models = VGroup(model1, model2).arrange(RIGHT, buff=2.75)

        self.playw(FadeIn(models))

        input_size = 5
        # no kv cache
        model1_in = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .next_to(model1, DOWN)
            .align_to(model1, LEFT)
            .shift(RIGHT * 0.2)
        )
        latent1 = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .move_to(model1)
            .align_to(model1_in, LEFT)
            .shift(DOWN * 0.3)
        )
        sa1 = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .move_to(model1)
            .align_to(model1_in, LEFT)
            .shift(UP * 0.3)
        )
        sa1_anim = [
            Transform(
                latent1[: i + 1].copy(),
                sa1[i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(input_size)
        ]
        out1 = Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1).scale(0.7)
        out1.next_to(model1, UP).align_to(model1, LEFT).shift(RIGHT * 0.2)
        attached1 = out1[-1].copy().next_to(model1_in, RIGHT, buff=0.07)

        # with kv cache
        model2_in = (
            model1_in.copy()
            .next_to(model2, DOWN)
            .align_to(model2, LEFT)
            .shift(RIGHT * 0.2)
        )
        latent2 = (
            latent1.copy().move_to(model2).align_to(model2_in, LEFT).shift(DOWN * 0.3)
        )
        sa2 = sa1.copy().move_to(model2).align_to(model2_in, LEFT).shift(UP * 0.3)
        sa2_anim = [
            Transform(
                latent2[: i + 1].copy(),
                sa2[i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(input_size)
        ]
        out2 = out1.copy().next_to(model2, UP).align_to(model2, LEFT).shift(RIGHT * 0.2)
        attached2 = attached1.copy().next_to(model2_in, RIGHT, buff=0.07)

        # animation
        self.playw(FadeIn(model1_in, model2_in))
        self.playw(
            Transform(
                model1_in.copy(), latent1, replace_mobject_with_target_in_scene=True
            ),
            Transform(
                model2_in.copy(), latent2, replace_mobject_with_target_in_scene=True
            ),
        )
        self.playwl(
            *[AnimationGroup(a1, a2) for a1, a2 in zip(sa1_anim, sa2_anim)],
            lag_ratio=0.4,
        )
        self.playw(
            Transform(sa1.copy(), out1, replace_mobject_with_target_in_scene=True),
            Transform(sa2.copy(), out2, replace_mobject_with_target_in_scene=True),
        )
        os1 = out1.copy()
        os2 = out2.copy()

        self.playw(FadeIn(kvtext))
        self.playw(
            Transform(
                out1[-1],
                attached1,
                replace_mobject_with_target_in_scene=True,
                path_arc=-PI / 3,
                path_axis=RIGHT,
            ),
            Transform(
                out2[-1],
                attached2,
                replace_mobject_with_target_in_scene=True,
                path_arc=-PI / 3,
                path_axis=RIGHT,
            ),
            FadeOut(out1[:-1], out2[:-1]),
            FadeOut(latent1, sa1, sa2),
        )

        # second inference: kv cache
        latent1b = VGroup(
            *latent1.copy(),
            last_ := Tensor(1, shape="square")
            .scale(0.7)
            .next_to(latent1, RIGHT, buff=0.07),
        )
        latent2b = VGroup(*latent2, last_.copy().next_to(latent2, RIGHT, buff=0.07))
        model1_in = VGroup(*model1_in, attached1)
        model2_in = attached2
        self.playw(
            Transform(
                model1_in.copy(), latent1b, replace_mobject_with_target_in_scene=True
            ),
            Transform(
                model2_in.copy(),
                latent2b[-1],
                replace_mobject_with_target_in_scene=True,
            ),
        )

        sa1b = VGroup(
            *sa1,
            last_ := Tensor(1, shape="square")
            .scale(0.7)
            .next_to(sa1, RIGHT, buff=0.07),
        )
        sa2b = last_.copy().next_to(sa2, RIGHT, buff=0.07)

        sa1b_anim = [
            Transform(
                latent1b[: i + 1].copy(),
                sa1b[i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(input_size + 1)
        ]
        sa2b_anim = [
            (
                Transform(
                    latent2b[: i + 1].copy(),
                    sa2b,
                    replace_mobject_with_target_in_scene=True,
                )
                if i == input_size
                else None
            )
            for i in range(input_size + 1)
        ]
        self.playwl(
            *[
                AnimationGroup(a1, a2) if a2 else AnimationGroup(a1)
                for a1, a2 in zip(sa1b_anim, sa2b_anim)
            ],
            lag_ratio=0.4,
        )

        out1b = VGroup(
            *os1,
            last_ := Tensor(1, shape="square")
            .scale(0.7)
            .next_to(os1, RIGHT, buff=0.07),
        )
        out2b = last_.copy().next_to(os2, RIGHT, buff=0.07)
        self.playw(
            Transform(sa1b.copy(), out1b, replace_mobject_with_target_in_scene=True),
            Transform(sa2b.copy(), out2b, replace_mobject_with_target_in_scene=True),
        )
        attached1b = out1b[-1].copy().next_to(model1_in, RIGHT, buff=0.07)
        attached2b = out2b[-1].copy().next_to(model2_in, RIGHT, buff=0.07)
        self.playw(
            Transform(
                out1b[-1],
                attached1b,
                replace_mobject_with_target_in_scene=True,
                path_arc=-PI / 3,
                path_axis=RIGHT,
            ),
            Transform(
                out2b[-1],
                attached2b,
                replace_mobject_with_target_in_scene=True,
                path_arc=-PI / 3,
                path_axis=RIGHT,
            ),
            FadeOut(out1b[:-1], out2b[:-1]),
            FadeOut(latent1b, sa1b, sa2b),
        )


class prefillPreview(Scene3D):
    def construct(self):
        model = (
            Rectangle(width=4.5, height=4, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.2)
            .set_z_index(1)
        )
        self.addw(model)
        input_size = 5
        model_in = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .next_to(model, DOWN)
            .align_to(model, LEFT)
            .shift(RIGHT * 0.2)
        )
        user_input = (
            Tensor(3, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .next_to(model_in, RIGHT)
            .set_opacity(0.3)
        )
        latent = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .move_to(model)
            .align_to(model_in, LEFT)
            .shift(DOWN * 0.3)
        )
        sa = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.7)
            .move_to(model)
            .align_to(model_in, LEFT)
            .shift(UP * 0.3)
        )
        sa_anim = [
            Transform(
                latent[: i + 1].copy(),
                sa[i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(input_size)
        ]
        out = Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1).scale(0.7)
        out.next_to(model, UP).align_to(model, LEFT).shift(RIGHT * 0.2)
        attached = out[-1].copy().next_to(model_in, RIGHT, buff=0.07)
        self.playw(FadeIn(model_in, user_input))
        model_in_box = DashedVMobject(
            SurroundingRect(stroke_width=2).surround(model_in, buff_w=0.15),
            dashed_ratio=0.6,
            num_dashes=30,
        )
        system_prompt = (
            Text("system prompt", font_size=24)
            .next_to(model_in_box, LEFT, buff=0.1)
            .set_color_by_gradient(BLUE, PURPLE)
        )
        user_input_box = DashedVMobject(
            SurroundingRect(stroke_width=2).surround(user_input, buff_w=0.15),
            dashed_ratio=0.6,
            num_dashes=25,
        )
        user_prompt = (
            Text("user input", font_size=24)
            .next_to(user_input_box, RIGHT, buff=0.1)
            .set_color_by_gradient(GREEN, GREEN_E)
        )
        self.playw(FadeIn(model_in_box, user_input_box, system_prompt, user_prompt))
        self.playw(
            Transform(
                model_in.copy(), latent, replace_mobject_with_target_in_scene=True
            )
        )


class prefill(Scene3D):
    def construct(self):
        rh = (
            Text("Request Handler", font_size=24)
            .set_color_by_gradient(BLUE, BLUE_D)
            .shift(LEFT * 4.5 + DOWN * 0.5)
        )
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 5.5 + UP)
        )
        uit = (
            Text("User", font_size=24)
            .set_color_by_gradient(YELLOW_B, YELLOW_D)
            .shift(RIGHT * 5.5 + DOWN * 0.5)
        )
        sp = Words(
            "[System] You are a helpful assistant [User]", font_size=20, color=GREY_C
        )
        ui = Words("What is piui?", font_size=20).next_to(uit, LEFT, buff=0.5)
        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).shift(LEFT * 3).align_to(
            spt, UP
        )

        self.add(rh, spt, sp, uit)
        self.cf.move_to(ui).shift(IN * 10 + LEFT * 0.5)
        self.wait()

        self.playwl(*[FadeIn(item) for item in ui.words], lag_ratio=0.5)

        self.playwl(
            ui.animate.next_to(rh, RIGHT, buff=0.5),
            self.cf.animate.move_to(rh).shift(IN * 5),
            run_time=2.5,
            lag_ratio=0.15,
            wait=0,
        )

        ui.generate_target()
        for w in ui.target.words:
            w.rotate(PI / 2)
        ui.target.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(sp, UP)
        self.playw(MoveToTarget(ui))

        model = (
            Rectangle(width=4.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.2)
            .set_z_index(1)
            .next_to(VGroup(sp, ui), UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )

        self.playw(FadeIn(model), self.cf.animate.shift(UP * 2.5 + OUT * 3.5))
        input_size = len(sp.words) + len(ui.words)
        model_in = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .align_to(sp, UL)
        )
        words = VGroup(*sp.words, *ui.words)
        words_ = words.copy()
        self.playw(
            Transform(
                words,
                model_in,
                replace_mobject_with_target_in_scene=True,
            )
        )

        latent = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(model_in, LEFT)
            .shift(DOWN * 0.3)
        )
        sa = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(model_in, LEFT)
            .shift(UP * 0.3)
        )
        sa_anim = [
            Transform(
                latent[: i + 1].copy(),
                sa[i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(input_size)
        ]
        self.playw(
            Transform(
                model_in.copy(), latent, replace_mobject_with_target_in_scene=True
            )
        )
        self.playwl(*sa_anim, lag_ratio=0.4, run_time=3)

        self.playw(Transform(model_in[: len(sp.words)], words_[: len(sp.words)]))

        self.wait(3)


class howPrefill(Scene3D):
    def construct(self):
        rh = (
            Text("Request Handler", font_size=24)
            .set_color_by_gradient(BLUE, BLUE_D)
            .shift(LEFT * 4.5 + DOWN * 0.5)
        )
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 5.5 + UP)
        )
        sp = Words(
            "[System] You are a helpful assistant [User]", font_size=20, color=GREY_C
        )
        ui = Words("What is piui?", font_size=20).next_to(rh, RIGHT, buff=0.5)

        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).shift(LEFT * 3).align_to(
            spt, UP
        )
        model = (
            Rectangle(width=4.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.2)
            .set_z_index(1)
            .next_to(VGroup(sp, ui), UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )
        self.cf.shift(LEFT + UP * 0.7)
        self.addw(rh, spt, sp, ui, model)

        input_size = len(sp.words) + len(ui.words)
        model_in = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .align_to(sp, UL)
        )
        # words = VGroup(*sp.words, *ui.words)
        # words_ = words.copy()
        # self.playw(
        #     Transform(
        #         words,
        #         model_in,
        #         replace_mobject_with_target_in_scene=True,
        #     )
        # )

        latent = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(model_in, LEFT)
            .shift(DOWN * 0.3)
        )
        prefilled = latent[: len(sp.words)]
        prefilled.save_state()

        latent[: len(sp.words)].shift(LEFT * 9)

        self.playw(Restore(prefilled))
        self.playw(Circumscribe(prefilled, color=YELLOW, stroke_width=3), wait=2)

        ui.generate_target()
        for w in ui.target.words:
            w.rotate(PI / 2)
        ui.target.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(sp, UP)
        self.playw(MoveToTarget(ui))

        lp = VGroup(
            brace := Brace(sp.words, UP, color=GREY_B),
            MathTex("L_p").next_to(brace, UP, buff=0.1),
        )
        lu = VGroup(
            brace := Brace(ui.words, UP, color=GREY_B),
            MathTex("L_u").next_to(brace, UP, buff=0.1),
        )
        model_ = VGroup(model, prefilled)
        model_.save_state()
        self.playwl(model_.animate.set_opacity(0), FadeIn(lp), lag_ratio=0.5)
        self.playw(FadeIn(lu))

        self.playwl(FadeOut(lp, lu), Restore(model_), lag_ratio=0.5)
        self.playw(
            Transform(
                ui.copy(),
                latent[len(sp.words) :],
                replace_mobject_with_target_in_scene=True,
            )
        )

        sa = (
            Tensor(input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(model_in, LEFT)
            .shift(UP * 0.3)
        )
        sa_anim = [
            Transform(
                latent[: i + 1].copy(),
                sa[i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(len(sp.words), input_size)
        ]
        self.playwl(*sa_anim, lag_ratio=0.4, run_time=2)

        empty_brace = Brace(sa[: len(sp.words)], UP, color=GREY_B)
        self.playw(FadeIn(empty_brace))
        self.playw(Circumscribe(latent[: len(sp.words)], color=YELLOW, stroke_width=3))

        ui_add = Words(
            "I do not have any idea what piui is. it sounds like a typo. I googled it but found nothing about it.",
            font_size=20,
        )
        for w in ui_add.words:
            w.rotate(PI / 2)
        ui_add.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            ui, RIGHT, buff=0.1
        ).align_to(ui, UP)
        self.playwl(
            FadeOut(empty_brace, sa[len(sp.words) :]),
            *[FadeIn(item) for item in ui_add.words],
            lag_ratio=0.1,
            wait=0,
        )
        self.playw(model.animate.stretch_to_fit_width(12).align_to(model, LEFT))
        ui = VGroup(*ui.words, *ui_add.words)
        latent_add = (
            Tensor(len(ui_add.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(ui_add, LEFT)
            .shift(DOWN * 0.3)
        )
        latent = VGroup(*latent, *latent_add)

        self.playw(
            Transform(
                ui_add.copy(),
                latent[len(sp.words) + len(ui) - len(ui_add.words) :],
                replace_mobject_with_target_in_scene=True,
            )
        )
        sa_add = (
            Tensor(len(ui_add.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(ui_add, LEFT)
            .shift(UP * 0.3)
        )
        sa = VGroup(*sa, *sa_add)
        sa_add_anim = [
            Transform(
                latent[: len(sp.words) + len(ui) - len(ui_add.words) + i + 1].copy(),
                sa[len(sp.words) + len(ui) - len(ui_add.words) + i],
                replace_mobject_with_target_in_scene=True,
            )
            for i in range(len(ui_add.words))
        ]
        self.playwl(*sa_add_anim, lag_ratio=0.4, run_time=10)


class prefillChunk(Scene3D):
    def construct(self):
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 7 + UP)
        )
        sp = Words(
            "[System] You are a helpful assistant [User]", font_size=20, color=GREY_C
        )
        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).shift(LEFT * 4.5).align_to(
            spt, UP
        )

        model = (
            Rectangle(width=10.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.2)
            .set_z_index(1)
            .next_to(VGroup(sp), UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )
        self.cf.shift(LEFT + UP * 0.7)

        ui = Words(
            "What is piui? I do not have any idea what piui is. it sounds like a typo. I googled it but found nothing about it.",
            font_size=20,
        )
        for w in ui.words:
            w.rotate(PI / 2)
        ui.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(sp, UP)

        total_input_size = len(sp.words) + len(ui.words)
        chunk_size = 4
        latent = (
            Tensor(total_input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(sp, LEFT)
            .shift(DOWN * 0.3)
        )
        prefilled = latent[: len(sp.words)]
        sa = (
            Tensor(total_input_size, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .move_to(model)
            .align_to(sp, LEFT)
            .shift(UP * 0.3)
        )
        self.addw(spt, sp, model, ui, prefilled)

        self.playwl(
            *[
                Indicate(ui.words[i : i + chunk_size], color=random_bright_color())
                for i in range(0, len(ui.words), chunk_size)
            ],
            lag_ratio=0.5,
        )
        self.playw(Circumscribe(ui.words[:chunk_size], stroke_width=3))
        for i in range(0, len(ui.words), chunk_size):
            chunk_in = ui.words[i : i + chunk_size]
            chunk_latent = latent[len(sp.words) + i : len(sp.words) + i + chunk_size]
            self.play(
                Transform(
                    VGroup(*chunk_in).copy(),
                    chunk_latent,
                    replace_mobject_with_target_in_scene=True,
                )
            )

            sa_anim = [
                Transform(
                    latent[: len(sp.words) + i + j + 1].copy(),
                    sa[len(sp.words) + i + j],
                    replace_mobject_with_target_in_scene=True,
                )
                for j in range(min(chunk_size, len(ui.words) - i))
            ]
            self.playwl(*sa_anim, lag_ratio=0.3, run_time=1.5, wait=0)
            if i == 0:
                self.wait()

            self.play(FadeOut(sa[len(sp.words) + i : len(sp.words) + i + chunk_size], shift=UP*2))
