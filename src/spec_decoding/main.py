from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        topic1 = Text("KV cache", font_size=36).set_color_by_gradient(GREEN_A, GREEN_D)
        topic2 = Text("Prefill chunks", font_size=36).set_color_by_gradient(
            GREEN_A, GREEN_D
        )
        topic3 = Text("Speculative decoding", font_size=36).set_color_by_gradient(
            GREEN_A, GREEN_D
        )
        VGroup(topic1, topic2, topic3).arrange(DOWN, buff=0.5)

        self.playwl(*[FadeIn(item) for item in [topic1, topic2, topic3]], lag_ratio=0.3)
        self.playwl(
            FadeOut(topic1, topic2),
            topic3.animate.move_to(ORIGIN).set_color_by_gradient(BLUE_A, BLUE_D),
            lag_ratio=0.3,
        )

        self.playw(FadeOut(topic3, shift=LEFT * 5))


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


class llmgen(Scene2D):
    def construct(self):
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 3.5 + DOWN)
        )
        sp = Words(
            "[System] You are a super- -ior assist- -ant [User]",
            font_size=20,
            color=GREY_C,
        )
        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).shift(LEFT * 0.7).align_to(
            spt, UP
        )
        ui = Words("What is piui?", font_size=20).to_edge(RIGHT).align_to(sp, UP)
        model = (
            Rectangle(width=5.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.6)
            .set_z_index(1)
            .next_to(sp, UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )
        self.addw(spt, sp, model, wait=3)
        self.playw(FadeIn(ui, shift=LEFT))
        self.play(ui.animate.next_to(sp, RIGHT, buff=0.1).align_to(sp, UP))
        ui.generate_target()
        for w in ui.target.words:
            w.rotate(PI / 2)
        ui.target.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(sp, UP)
        self.play(MoveToTarget(ui), wait=2)
        resp = (
            Text("[Assistant]", font_size=20, color=GREEN_B)
            .rotate(PI / 2)
            .next_to(ui, RIGHT, buff=0.1)
            .align_to(ui, UP)
        )
        kvcache = (
            Tensor(
                len(sp.words) + len(ui.words), shape="square", arrange=RIGHT, buff=0.1
            )
            .scale(0.64)
            .move_to(model)
            .align_to(model, LEFT)
            .shift(DOWN * 0.3 + RIGHT * 0.2)
        )
        self.play(
            Transform(
                VGroup(*sp.words, *ui.words).copy(),
                kvcache,
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(FadeIn(resp, shift=UP), wait=1)

        latent_resp = (
            Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .next_to(kvcache, RIGHT, buff=0.064)
        )
        self.play(
            Transform(
                resp.copy(),
                latent_resp,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor = (
            Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .next_to(model, UP)
            .align_to(latent_resp, LEFT)
        )
        self.play(
            Transform(
                VGroup(kvcache, latent_resp).copy(),
                out_tensor,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out = Text("Piui", font_size=20, color=GREEN_B).move_to(out_tensor)
        self.playw(
            Transform(out_tensor, out, replace_mobject_with_target_in_scene=True)
        )
        os1 = out.copy().next_to(model, RIGHT).align_to(out, UP)
        os2 = out.copy().next_to(model, RIGHT).align_to(resp, UP)
        os3 = out.copy().next_to(resp, RIGHT, buff=0.1).align_to(resp, UP)
        path = BrokenLine(
            out.get_center(), os1.get_center(), os2.get_center(), os3.get_center()
        )
        self.play(MoveAlongPath(out, path), run_time=2)
        out.generate_target().rotate(PI / 2).next_to(resp, RIGHT, buff=0.1).align_to(
            resp, UP
        )
        self.playw(MoveToTarget(out), run_time=0.5)

        self.playw(Indicate(sp.words[2]))
        self.playwl(Indicate(sp.words[4]), Indicate(sp.words[5]), lag_ratio=0.2)

        self.playw(model.animate.stretch_to_fit_width(7.5).align_to(model, LEFT))

        answer_list = "is the sound of a sparrow crying".split(" ")
        for w in answer_list:
            kvcache = VGroup(*kvcache, latent_resp)
            latent_resp = (
                Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
                .scale(0.64)
                .next_to(kvcache, RIGHT, buff=0.064)
            )
            resp = out
            self.play(
                Transform(
                    resp.copy(), latent_resp, replace_mobject_with_target_in_scene=True
                )
            )
            out_tensor = (
                Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
                .scale(0.64)
                .next_to(model, UP)
                .align_to(latent_resp, LEFT)
            )
            self.play(
                Transform(
                    VGroup(kvcache, latent_resp).copy(),
                    out_tensor,
                    replace_mobject_with_target_in_scene=True,
                )
            )
            out = Text(w, font_size=20, color=GREEN_B).move_to(out_tensor)
            self.play(
                Transform(out_tensor, out, replace_mobject_with_target_in_scene=True)
            )
            os1 = out.copy().next_to(model, RIGHT).align_to(out, UP)
            os2 = out.copy().next_to(model, RIGHT).align_to(resp, UP)
            os3 = out.copy().next_to(resp, RIGHT, buff=0.1).align_to(resp, UP)
            path = BrokenLine(
                out.get_center(), os1.get_center(), os2.get_center(), os3.get_center()
            )
            self.play(MoveAlongPath(out, path), run_time=1.5)
            out.generate_target().rotate(PI / 2).next_to(
                resp, RIGHT, buff=0.1
            ).align_to(resp, UP)
            self.playw(MoveToTarget(out), run_time=0.5)


class llmeval(Scene2D):
    def construct(self):
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 5 + DOWN)
        )
        sp = Words(
            "[System] You are a super- -ior assist- -ant [User]",
            font_size=20,
            color=GREY_C,
        )
        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).shift(LEFT * 2.2).align_to(
            spt, UP
        )
        ui = Words("What is piui?", font_size=20)
        for w in ui.words:
            w.rotate(PI / 2)
        ui.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(spt, UP)
        model = (
            Rectangle(width=7.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.6)
            .set_z_index(1)
            .next_to(sp, UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )
        resp = (
            Text("[Assistant]", font_size=20, color=GREEN_B)
            .rotate(PI / 2)
            .next_to(ui, RIGHT, buff=0.1)
            .align_to(ui, UP)
        )
        answer = Words(
            "Piui is the sound of a sparrow crying", font_size=20, color=ORANGE
        )
        for w in answer.words:
            w.rotate(PI / 2)
        answer.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            resp, RIGHT, buff=0.1
        ).align_to(spt, UP)
        kvcache = (
            Tensor(
                len(sp.words) + len(ui.words) + 1,
                shape="square",
                arrange=RIGHT,
                buff=0.1,
            )
            .scale(0.64)
            .move_to(model)
            .align_to(model, LEFT)
            .shift(DOWN * 0.3 + RIGHT * 0.2)
        )
        self.addw(spt, sp, ui, model, resp, kvcache)

        self.playw(FadeIn(answer, shift=UP))

        latent_answer = (
            Tensor(len(answer.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .next_to(kvcache, RIGHT, buff=0.064)
        )
        self.play(
            Transform(
                answer.copy(),
                latent_answer,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor = (
            Tensor(len(answer.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(0.64)
            .next_to(model, UP)
            .align_to(latent_answer, LEFT)
        )
        self.playw(
            FadeTransform(
                VGroup(kvcache, latent_answer).copy(),
                out_tensor,
                # replace_mobject_with_target_in_scene=True,
            )
        )
        probs_list = [0.95, 0.97, 0.62, 0.85, 0.9, 0.82, 0.7, 0.73]
        probs_vt = [ValueTracker(p) for p in probs_list]

        def set_decimal(p):
            return DecimalNumber(
                p,
                num_decimal_places=2,
                font_size=18,
                color=WHITE if p > 0.5 else interpolate_color(PURE_RED, WHITE, p * 2),
            )[1:]

        probs = VGroup(*[set_decimal(p.get_value()) for p in probs_vt])
        probs.arrange(RIGHT, buff=0.1).move_to(out_tensor)
        self.play(self.cf.animate.move_to(out_tensor).scale(0.4))
        self.playw(
            Transform(out_tensor, probs, replace_mobject_with_target_in_scene=True)
        )

        wrong_answer = Words("Piui is a typo of the word π", font_size=16, color=RED)
        for w in wrong_answer.words:
            w.rotate(PI / 2)
        wrong_answer.words.arrange(RIGHT, aligned_edge=DOWN, buff=0.15).next_to(
            probs, UP, buff=0.5
        ).set_opacity(0.5)

        self.playw(FadeIn(wrong_answer, shift=DOWN))
        probs_new_list = [0.95, 0.97, 0.3, 0.17, 0.7, 0.75, 0.3, 0.01]
        probs.add_updater(
            lambda mob: mob.become(
                VGroup(*[set_decimal(p.get_value()) for p in probs_vt])
                .arrange(RIGHT, buff=0.1)
                .move_to(out_tensor)
            )
        )
        self.playw(
            *[p.animate.set_value(pn) for p, pn in zip(probs_vt, probs_new_list)],
            run_time=2,
        )

        right_answer = Words(
            "Piui is the sound of a sparrow crying", font_size=16, color=GREEN
        )
        for w in right_answer.words:
            w.rotate(PI / 2)
        right_answer.words.arrange(RIGHT, aligned_edge=DOWN, buff=0.15).next_to(
            probs, UP, buff=0.5
        ).set_opacity(0.5)
        self.playw(Transform(wrong_answer.words, right_answer.words), run_time=2)
        probs_new_list = [0.95, 0.97, 0.62, 0.85, 0.9, 0.82, 0.75, 0.78]
        self.playw(
            *[p.animate.set_value(pn) for p, pn in zip(probs_vt, probs_new_list)],
            run_time=2,
        )


class chunkwise(Scene2D):
    def construct(self):
        const = 0.645
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 5 + DOWN)
        )
        sp = Words(
            "[System] You are a helpful assistant [User]",
            font_size=20,
            color=GREY_C,
        )
        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            spt, RIGHT, buff=0.5
        ).align_to(spt, UP)
        ui = Words(
            "Explain the theory of relativity [Assistant]",
            font_size=20,
            color=GREY_C,
        )
        for w in ui.words:
            w.rotate(PI / 2)
        ui.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(spt, UP)
        model = (
            Rectangle(width=7.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.6)
            .set_z_index(1)
            .next_to(sp, UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )
        kv_cache = (
            Tensor(
                len(sp.words) + len(ui.words), shape="square", arrange=RIGHT, buff=0.1
            )
            .scale(const)
            .move_to(model)
            .align_to(model, LEFT)
            .shift(DOWN * 0.3 + RIGHT * 0.2)
        )
        self.addw(spt, sp, ui, model, kv_cache)

        response1 = Words(
            "The theory of relativity , developed by", font_size=20, color=GREEN_C
        )
        response2 = Words(
            "Albert Einstein, revolutionized our understanding of time",
            font_size=20,
            color=GREEN_C,
        )
        response3 = Words(
            "and gravity . It consists of",
            font_size=20,
            color=GREEN_C,
        )
        for w in response1.words:
            w.rotate(PI / 2)
        response1.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            ui, RIGHT, buff=0.1
        ).align_to(spt, UP)
        for w in response2.words:
            w.rotate(PI / 2)
        response2.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response1, RIGHT, buff=0.1
        ).align_to(spt, UP)
        for w in response3.words:
            w.rotate(PI / 2)
        response3.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response2, RIGHT, buff=0.1
        ).align_to(spt, UP)

        self.playw(FadeIn(response1.words, shift=UP))
        latent_response1 = (
            Tensor(len(response1.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(kv_cache, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response1.copy(),
                latent_response1,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor1 = (
            Tensor(len(response1.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response1, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response1).copy(),
                out_tensor1,
            )
        )
        checked = Text("✔", font_size=24, color=GREEN).next_to(out_tensor1, UP)
        self.playw(
            FadeIn(checked, shift=UP * 0.5),
        )
        self.play(
            FadeOut(checked),
            self.cf.animate.shift(RIGHT * 2.1),
            model.animate.stretch_to_fit_width(11.5).align_to(model, LEFT),
            FadeIn(response2.words, shift=UP),
        )
        latent_response2 = (
            Tensor(len(response2.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(latent_response1, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response2.copy(),
                latent_response2,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor2 = (
            Tensor(len(response2.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response2, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response2).copy(),
                out_tensor2,
            )
        )
        checked = Text("✔", font_size=24, color=GREEN).next_to(out_tensor2, UP)
        self.play(
            FadeIn(checked, shift=UP * 0.5),
        )
        self.play(FadeOut(checked), FadeIn(response3.words, shift=UP))
        latent_response3 = (
            Tensor(len(response3.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(latent_response2, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response3.copy(),
                latent_response3,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor3 = (
            Tensor(len(response3.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response3, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response3).copy(),
                out_tensor3,
            )
        )
        checked = Text("✔", font_size=24, color=GREEN).next_to(out_tensor3, UP)
        self.play(
            FadeIn(checked, shift=UP * 0.5),
        )
        self.playw(
            FadeOut(checked),
        )

        response4 = Words(
            "the relationship between Elon Musk and gravity",
            font_size=20,
            color=GREEN_C,
        )
        response4.words[3:5].set_color(PURE_RED)
        for w in response4.words:
            w.rotate(PI / 2)
        response4.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response3, RIGHT, buff=0.1
        ).align_to(spt, UP)
        self.play(
            FadeIn(response4.words, shift=UP),
            self.cf.animate.shift(RIGHT * 2.1),
            model.animate.stretch_to_fit_width(14).align_to(model, LEFT),
        )
        latent_response4 = (
            Tensor(len(response4.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(latent_response3, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response4.copy(),
                latent_response4,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor4 = (
            Tensor(len(response4.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response4, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response4).copy(),
                out_tensor4,
            )
        )
        wrong = Text("✘", font_size=24, color=PURE_RED).next_to(out_tensor4, UP)
        self.playw(
            FadeIn(wrong, shift=UP * 0.5), out_tensor4[2:4].animate.set_color(PURE_RED)
        )
        self.playw(
            FadeOut(out_tensor4[3:], wrong, latent_response4[3:], response4.words[3:]),
        )
        pre_generated_box = DashedVMobject(
            SurroundingRect(color=YELLOW_B, stroke_width=2).surround(
                VGroup(response1, response2, response3, response4.words[:3]), buff_w=0.1
            ),
            num_dashes=60,
            dashed_ratio=0.7,
        )
        self.playwl(
            Create(pre_generated_box), self.cf.animate.shift(DOWN * 0.7), lag_ratio=0.3
        )
        self.wait(3)

        smodel = (
            Rectangle(width=14, height=1.6, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.6)
            .set_z_index(1)
            .next_to(sp, UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2 + DOWN * 6.9)
        )

        smallmodel = (
            Text("Smaller model", font_size=24)
            .set_color_by_gradient(GREY_A, GREY_C)
            .next_to(smodel, RIGHT, buff=0.2)
            .align_to(smodel, UP)
        )
        sptc, spc, uic, kvcachec = (
            spt.copy().next_to(smodel, DOWN, buff=0.3).align_to(spt, LEFT),
            sp.copy().next_to(smodel, DOWN, buff=0.3).align_to(sp, LEFT),
            ui.copy().next_to(smodel, DOWN, buff=0.3).align_to(ui, LEFT),
            kv_cache.copy().move_to(smodel).align_to(kv_cache, LEFT),
        )
        self.add(smodel, smallmodel, sptc, spc, uic, kvcachec)
        self.playw(
            self.cf.animate.scale(2.0).shift(DOWN * 3.5), FadeOut(pre_generated_box)
        )
        responses_model = VGroup(
            *response1.words, *response2.words, *response3.words, *response4.words
        )

        sout_tensor = (
            Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(smodel, UP)
            .align_to(kvcachec[-1], LEFT)
        )
        self.play(FadeTransform(kvcachec.copy(), sout_tensor))
        responses = (
            VGroup(
                *response1.words, *response2.words, *response3.words, *response4.words
            )
            .copy()
            .arrange(RIGHT, buff=0.1, aligned_edge=UP)
        )
        responses.next_to(uic, RIGHT, buff=0.1).align_to(sptc, UP)
        sout = (
            responses.copy()
            .arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            .next_to(smodel, UP)
            .align_to(sout_tensor, LEFT)
        )
        self.play(
            Transform(sout_tensor, sout[0], replace_mobject_with_target_in_scene=True)
        )
        chunk_idx = [
            len(response1.words),
            len(response1.words) + len(response2.words),
            len(response1.words) + len(response2.words) + len(response3.words),
        ]
        chunk_start = 0
        for i in range(1, len(sout)):
            run_time = 0.5
            if i in chunk_idx:
                self.play(
                    Transform(sout[i - 1].copy(), responses[i - 1]),
                    Transform(
                        sout[chunk_start:i].copy(),
                        temp := responses_model[chunk_start:i].copy(),
                        replace_mobject_with_target_in_scene=True,
                    ),
                    run_time=run_time,
                )
                chunk_start = i
                self.remove(temp)
            else:
                self.play(
                    Transform(sout[i - 1].copy(), responses[i - 1]),
                    run_time=run_time,
                )
            latent = (
                Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
                .scale(const)
                .next_to(kvcachec, RIGHT, buff=0.1 * const)
            )
            self.play(
                Transform(
                    responses[i - 1].copy(),
                    latent,
                    replace_mobject_with_target_in_scene=True,
                ),
                run_time=run_time,
            )
            kvcachec.add(latent)
            sout_tensor = (
                Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
                .scale(const)
                .next_to(smodel, UP)
                .align_to(latent, LEFT)
            )
            self.play(
                FadeTransform(
                    VGroup(latent).copy(),
                    sout_tensor,
                ),
                run_time=run_time,
            )
            self.play(
                Transform(
                    sout_tensor, sout[i], replace_mobject_with_target_in_scene=True
                ),
                run_time=run_time,
            )


class bigllm(Scene2D):
    def construct(self):
        const = 0.645
        spt = (
            Text("System Prompt", font_size=24)
            .set_color_by_gradient(BLUE, PURPLE)
            .shift(LEFT * 5 + DOWN)
        )
        sp = Words(
            "[System] You are a helpful assistant [User]",
            font_size=20,
            color=GREY_C,
        )
        for w in sp.words:
            w.rotate(PI / 2)
        sp.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            spt, RIGHT, buff=0.5
        ).align_to(spt, UP)
        ui = Words(
            "Explain the theory of relativity [Assistant]",
            font_size=20,
            color=GREY_C,
        )
        for w in ui.words:
            w.rotate(PI / 2)
        ui.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            sp, RIGHT, buff=0.1
        ).align_to(spt, UP)
        model = (
            Rectangle(width=7.5, height=3, stroke_width=3, color=GREY_B)
            .set_fill(BLACK, 0.6)
            .set_z_index(1)
            .next_to(sp, UP, buff=0.5)
            .align_to(sp, LEFT)
            .shift(LEFT * 0.2)
        )
        kv_cache = (
            Tensor(
                len(sp.words) + len(ui.words), shape="square", arrange=RIGHT, buff=0.1
            )
            .scale(const)
            .move_to(model)
            .align_to(model, LEFT)
            .shift(DOWN * 0.3 + RIGHT * 0.2)
        )
        self.addw(spt, sp, ui, model, kv_cache)

        response1 = Words(
            "The theory of relativity , developed by", font_size=20, color=GREEN_C
        )
        response2 = Words(
            "Albert Einstein, revolutionized our understanding of time",
            font_size=20,
            color=GREEN_C,
        )
        response3 = Words(
            "and gravity . It consists of",
            font_size=20,
            color=GREEN_C,
        )
        for w in response1.words:
            w.rotate(PI / 2)
        response1.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            ui, RIGHT, buff=0.1
        ).align_to(spt, UP)
        for w in response2.words:
            w.rotate(PI / 2)
        response2.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response1, RIGHT, buff=0.1
        ).align_to(spt, UP)
        for w in response3.words:
            w.rotate(PI / 2)
        response3.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response2, RIGHT, buff=0.1
        ).align_to(spt, UP)

        self.playw(FadeIn(response1.words, shift=UP))
        latent_response1 = (
            Tensor(len(response1.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(kv_cache, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response1.copy(),
                latent_response1,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor1 = (
            Tensor(len(response1.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response1, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response1).copy(),
                out_tensor1,
            )
        )
        checked = Text("✔", font_size=24, color=GREEN).next_to(out_tensor1, UP)
        self.playw(
            FadeIn(checked, shift=UP * 0.5),
        )
        self.play(
            FadeOut(checked),
            self.cf.animate.shift(RIGHT * 2.1),
            model.animate.stretch_to_fit_width(11.5).align_to(model, LEFT),
            FadeIn(response2.words, shift=UP),
        )
        latent_response2 = (
            Tensor(len(response2.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(latent_response1, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response2.copy(),
                latent_response2,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor2 = (
            Tensor(len(response2.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response2, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response2).copy(),
                out_tensor2,
            )
        )
        checked = Text("✔", font_size=24, color=GREEN).next_to(out_tensor2, UP)
        self.play(
            FadeIn(checked, shift=UP * 0.5),
        )
        self.play(FadeOut(checked), FadeIn(response3.words, shift=UP))
        latent_response3 = (
            Tensor(len(response3.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(latent_response2, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response3.copy(),
                latent_response3,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor3 = (
            Tensor(len(response3.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response3, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response3).copy(),
                out_tensor3,
            )
        )
        checked = Text("✔", font_size=24, color=GREEN).next_to(out_tensor3, UP)
        self.play(
            FadeIn(checked, shift=UP * 0.5),
        )
        self.playw(
            FadeOut(checked),
        )

        response4 = Words(
            "the relationship between Elon Musk and gravity",
            font_size=20,
            color=GREEN_C,
        )
        response4.words[3:5].set_color(PURE_RED)
        for w in response4.words:
            w.rotate(PI / 2)
        response4.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response3, RIGHT, buff=0.1
        ).align_to(spt, UP)
        self.play(
            FadeIn(response4.words, shift=UP),
            self.cf.animate.shift(RIGHT * 2.1),
            model.animate.stretch_to_fit_width(14).align_to(model, LEFT),
        )
        latent_response4 = (
            Tensor(len(response4.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(latent_response3, RIGHT, buff=0.1 * const)
        )
        self.play(
            Transform(
                response4.copy(),
                latent_response4,
                replace_mobject_with_target_in_scene=True,
            )
        )
        out_tensor4 = (
            Tensor(len(response4.words), shape="square", arrange=RIGHT, buff=0.1)
            .scale(const)
            .next_to(model, UP)
            .align_to(latent_response4, LEFT)
        )
        self.play(
            FadeTransform(
                VGroup(latent_response4).copy(),
                out_tensor4,
            )
        )
        wrong = Text("✘", font_size=24, color=PURE_RED).next_to(out_tensor4, UP)
        self.playw(
            FadeIn(wrong, shift=UP * 0.5), out_tensor4[2:4].animate.set_color(PURE_RED)
        )
        self.playw(
            FadeOut(out_tensor4[3:], wrong, latent_response4[3:], response4.words[3:]),
        )

        correct_text = Words("space , time and matter", font_size=20, color=GREEN_D)
        for w in correct_text.words:
            w.rotate(PI / 2)
        correct_text.words.arrange(RIGHT, aligned_edge=UP, buff=0.1).next_to(
            response4.words[:3], RIGHT, buff=0.1
        ).align_to(spt, UP)
        correct_text_out = correct_text.copy()
        correct_text_out.words.arrange(RIGHT, buff=0.1, aligned_edge=DOWN).next_to(
            model, UP
        ).align_to(out_tensor4[2], LEFT)
        self.play(
            Transform(
                out_tensor4[2],
                correct_text_out.words[0],
                replace_mobject_with_target_in_scene=True,
            )
        )
        new_latent = latent_response4[:3]
        for i in range(1, len(correct_text.words)):
            self.play(
                Transform(
                    correct_text_out.words[i - 1].copy(), correct_text.words[i - 1]
                )
            )
            latent = (
                Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
                .scale(const)
                .next_to(new_latent, RIGHT, buff=0.1 * const)
            )
            self.play(
                Transform(
                    correct_text.words[i - 1].copy(),
                    latent,
                    replace_mobject_with_target_in_scene=True,
                )
            )
            new_latent.add(latent)
            out_tensor = (
                Tensor(1, shape="square", arrange=RIGHT, buff=0.1)
                .scale(const)
                .next_to(model, UP)
                .align_to(latent, LEFT)
            )
            self.play(
                FadeTransform(
                    VGroup(latent).copy(),
                    out_tensor,
                )
            )
            self.play(
                Transform(
                    out_tensor,
                    correct_text_out.words[i],
                    replace_mobject_with_target_in_scene=True,
                )
            )
