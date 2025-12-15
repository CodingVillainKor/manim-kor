from manim import *
from raenim import *
from random import random, seed

seed(1)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        nump = NumberPlane(
            x_range=[-0.5, 10],
            y_range=[-0.5, 10],
            background_line_style={"stroke_opacity": 0.0},
            x_length=9,
            y_length=6.5,
            axis_config={"stroke_color": GREY_B},
        ).shift(UP * 0.5)
        xt = (
            Text("반복 수", font="Noto Sans KR", font_size=20, color=GREY_A)
            .next_to(nump.x_axis, DR, buff=0.1)
            .shift(LEFT * 0.8)
        )
        yt = (
            Text("성능", font="Noto Sans KR", font_size=20, color=GREY_A)
            .next_to(nump.y_axis, UL, buff=0.1)
            .shift(DOWN * 0.4)
        )
        self.addw(nump, xt, yt)

        model = Rectangle(
            width=1.5,
            height=0.75,
            color=GREEN_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        ).move_to(nump.c2p(1, 1))
        modelt = Text(
            "Model", font="Noto Sans KR", font_size=24, color=GREEN_C
        ).move_to(model)
        model = VGroup(model, modelt)
        self.play(FadeIn(model))
        ema_model = Rectangle(
            width=3,
            height=1.5,
            color=YELLOW_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        ).move_to(nump.c2p(1, 2.5))
        ema_modelt = Text(
            "EMA Model", font="Noto Sans KR", font_size=40, color=YELLOW_C
        ).move_to(ema_model)
        ema_model = VGroup(ema_model, ema_modelt).scale(0.5)
        self.play(FadeIn(ema_model, target_position=model))
        arrow = Arrow(
            start=ema_model.get_center(),
            end=model.get_center(),
            buff=0.1,
            stroke_width=3,
            color=GREEN_A,
            tip_length=0.2,
        )
        self.play(GrowArrow(arrow))
        self.playw(FadeOut(arrow), model.animate.move_to(nump.c2p(3, 2)))

        for i in range(3):
            ema_model_ = Rectangle(
                width=3,
                height=1.5,
                color=YELLOW_B,
                stroke_width=2,
                fill_opacity=1,
                fill_color=BLACK,
            ).move_to(nump.c2p(3 + i * 2, 3.5 + i))
            ema_modelt_ = Text(
                "EMA Model", font="Noto Sans KR", font_size=40, color=YELLOW_C
            ).move_to(ema_model_)
            ema_model_ = VGroup(ema_model_, ema_modelt_).scale(0.5)
            self.play(
                FadeIn(ema_model_, target_position=model),
                ema_model.set_z_index(-1).animate.move_to(ema_model_),
            )
            self.remove(ema_model)
            arrow = Arrow(
                start=ema_model_.get_center(),
                end=model.get_center(),
                buff=0.1,
                stroke_width=3,
                color=GREEN_A,
                tip_length=0.2,
            )
            self.play(GrowArrow(arrow))
            self.play(FadeOut(arrow), model.animate.move_to(nump.c2p(5 + i * 2, 3 + i)))
            ema_model = ema_model_


class ssl(Scene2D):
    def construct(self):
        dino = Text("DiNO", font="Noto Sans KR", font_size=40).set_color_by_gradient(
            GREEN_A, GREEN_C
        )
        self.playw(FadeIn(dino))
        ssl = Text(
            "Self-Supervised Learning", font="Noto Sans KR", font_size=32
        ).set_color_by_gradient(GREEN_A, GREEN_C)
        self.play(FadeOut(dino), run_time=0.5)
        self.playw(FadeIn(ssl))

        sl = (
            (
                Text(
                    "Supervised Learning", font="Noto Sans KR", font_size=32
                ).set_color_by_gradient(GREY_B, GREY_C)
            )
            .shift(UP * 3 + LEFT * 3.5)
            .scale(0.8)
        )
        self.play(ssl.animate.shift(UP * 3 + RIGHT * 3.5).scale(0.8))
        self.playw(FadeIn(sl))

        def get_model():
            box = Rectangle(
                width=1.5,
                height=0.75,
                color=GREY_B,
                stroke_width=2,
                fill_opacity=1,
                fill_color=BLACK,
            )
            text = Text(
                "Model", font="Noto Sans KR", font_size=24, color=GREY_C
            ).move_to(box)
            return VGroup(box, text)

        model_ssl = get_model().shift(RIGHT * 3.5)
        model_sl = get_model().shift(LEFT * 3.5)
        self.playw(FadeIn(model_ssl), FadeIn(model_sl))

        img_sl = ImageMobject("cat.jpg").scale(0.25).next_to(model_sl, UP, buff=0.5)
        pred_sl = Words(
            "Prediction: Cat", font="Noto Sans KR", font_size=20, color=GREY_A
        ).next_to(model_sl, DOWN, buff=0.6)
        pred_sl.words[1].set_color(GREEN_B)
        label_sl = Words(
            "Label: Cat", font="Noto Sans KR", font_size=20, color=GREY_A
        ).next_to(pred_sl, DOWN, buff=0.8)
        label_sl.words[1].set_color(GREEN_B)
        arrow_sl = Arrow(
            start=img_sl.get_bottom(),
            end=pred_sl.get_top(),
            buff=0.1,
            stroke_width=3,
            color=GREY_B,
            tip_length=0.15,
        ).set_z_index(-1)
        arrow_loss_sl = Arrow(
            start=label_sl.get_top(),
            end=pred_sl.get_bottom(),
            buff=0.1,
            stroke_width=3,
            color=RED_B,
            tip_length=0.15,
        ).set_z_index(-1)
        self.play(FadeIn(img_sl))
        self.play(GrowArrow(arrow_sl))
        self.play(FadeIn(pred_sl))
        self.playw(FadeIn(label_sl), GrowArrow(arrow_loss_sl))

        img_ssl1 = ImageMobject("cat.jpg").scale(0.25).next_to(model_ssl, UP, buff=0.5)
        pred_ssl1 = Words(
            "Prediction: ???", font="Noto Sans KR", font_size=20, color=GREY_A
        ).next_to(model_ssl, DOWN, buff=0.6)
        pred_ssl1.words[1].set_color(RED_B)
        arrow_ssl1 = Arrow(
            start=img_ssl1.get_bottom(),
            end=pred_ssl1.get_top(),
            buff=0.1,
            stroke_width=3,
            color=GREY_B,
            tip_length=0.15,
        ).set_z_index(-1)
        self.play(FadeIn(img_ssl1))
        self.play(GrowArrow(arrow_ssl1))
        self.playw(FadeIn(pred_ssl1))

        self.playw(Flash(model_ssl.get_corner(UL), color=GREEN_C), Wiggle(model_ssl))

        sl_box = SurroundingRectangle(
            sl,
            model_sl,
            img_sl,
            pred_sl,
            label_sl,
            arrow_sl,
            arrow_loss_sl,
            buff=0.3,
            color=GREY_B,
            stroke_width=2,
        )
        ssl_box = (
            SurroundingRectangle(
                ssl,
                model_ssl,
                img_ssl1,
                pred_ssl1,
                buff=0.3,
                color=GREEN_A,
                stroke_width=2,
            )
            .stretch_to_fit_height(sl_box.height)
            .align_to(sl_box, UP)
        )
        self.play(FadeIn(ssl_box, sl_box))

        pt = (
            Text("Pretrain", font="Noto Sans KR", font_size=24)
            .set_color_by_gradient(GREEN_A, GREEN_C)
            .next_to(ssl_box, DOWN, buff=0.2)
            .align_to(ssl_box, LEFT)
        )
        ft = (
            Text("Finetune", font="Noto Sans KR", font_size=24)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .next_to(sl_box, DOWN, buff=0.2)
            .align_to(sl_box, RIGHT)
        )
        self.play(self.cf.animate.scale(1.1).shift(DOWN * 0.4), FadeIn(pt))
        arrow_ptft = Arrow(
            start=pt.get_left(),
            end=ft.get_right(),
            buff=0.1,
            stroke_width=3,
            color=GREY_B,
            tip_length=0.15,
        )
        self.playw(GrowArrow(arrow_ptft), FadeIn(ft))

        sl_data = VGroup(
            SurroundingRectangle(img_sl, color=RED_C, stroke_width=3, buff=0.1),
            SurroundingRectangle(label_sl, color=RED_C, stroke_width=3, buff=0.1),
        ).set_z_index(10)
        ssl_data = SurroundingRectangle(
            img_ssl1.set_z_index(10), color=GREEN_B, stroke_width=3, buff=0.1
        ).set_z_index(10)
        shade = Rectangle(
            height=self.cf.height,
            width=self.cf.width,
            fill_opacity=0.7,
            fill_color=BLACK,
            stroke_opacity=0,
        ).set_z_index(5)
        self.playw(FadeIn(shade, ssl_data))

        self.mouse.next_to(ssl_data, RIGHT).shift(RIGHT * 5).set_z_index(12)
        self.playw(self.mouse.animate.move_to(ssl_data.get_corner(DR)))

        ptc = pt.copy().set_z_index(10)
        self.playw(FadeIn(ptc), FadeOut(pt))
        arr_ptftc = arrow_ptft.copy().set_z_index(10)
        ftc = ft.copy().set_z_index(10)
        self.play(FadeIn(arr_ptftc), FadeOut(arrow_ptft))
        self.playw(FadeIn(ftc), FadeOut(ft))

        img_slc, label_slc = img_sl.copy().set_z_index(10), label_sl.copy().set_z_index(
            10
        )
        self.playw(FadeIn(img_slc, label_slc, sl_data))

        slc = sl.copy().set_z_index(10).set_color_by_gradient(YELLOW_A, YELLOW_C)
        self.play(FadeIn(slc))
        self.playw(self.mouse.animate.move_to(sl_data[0].get_corner(DR)))
        self.playw(self.mouse.animate.move_to(sl_data[1].get_corner(DR)))


class scene2(Scene2D):
    def construct(self):
        model = Rectangle(
            width=1.5,
            height=2.75,
            color=GREEN_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        ).move_to(ORIGIN)
        modelt = Text(
            "Model", font="Noto Sans KR", font_size=24, color=GREEN_C
        ).move_to(model)
        model = VGroup(model, modelt)
        self.playw(FadeIn(model))
        slt = (
            Words(
                "Supervised Learning", font="Noto Sans KR", font_size=32
            ).set_color_by_gradient(GREY_B, GREY_C)
        ).shift(UP * 3)
        self.playw(*[FadeIn(item) for item in slt.words])

        out_ch = 10
        final = (
            nn.Linear(2, out_ch).move_to(model.get_right()).set_z_index(-1).scale(0.7)
        )
        img_in = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        self.play(FadeIn(img_in))
        self.play(img_in.animate.move_to(model).scale(0.5))
        self.remove(img_in)
        self.play(FadeIn(final))

        label = (
            Words("Label: Cat", font="Noto Sans KR", font_size=20, color=GREY_A)
            .next_to(final[-1][1], RIGHT, buff=0.5)
            .set_z_index(-1)
        )
        self.play(FadeIn(label))
        self.play(FadeOut(label, scale=0.3, target_position=final[-1][1]))

        self.playwl(
            Indicate(final[-1][1], color=YELLOW_C, scale_factor=1.0),
            Indicate(
                VGroup(final[-1][0], final[-1][2:]), color=RED_B, scale_factor=1.0
            ),
            lag_ratio=0.3,
        )

        def softmax(vect: list):
            exps = np.exp(vect - np.max(vect))
            return exps / exps.sum()

        pred_nums = [random() * 15 for _ in range(out_ch)]
        pred_vector = VGroup(
            *[
                DecimalNumber(num, num_decimal_places=2, color=GREY_A, font_size=30)
                .move_to(final[-1][i])
                .align_to(final[-1][i], LEFT)
                for i, num in enumerate(softmax(pred_nums))
            ]
        )
        final[-1].save_state()
        self.playw(final[-1].animate.become(pred_vector))

        label_strings = [
            "Dog",
            "Cat",
            "Sparrow",
            "Fish",
            "Horse",
            "Sheep",
            "Cow",
            "Elephant",
            "Tiger",
            "Eagle",
        ]
        somethings_strings = [f"something{i}" for i in range(out_ch)]
        pred_words = VGroup(
            *[
                Words(
                    f"p(y={label_strings[i]})",
                    font="Noto Sans KR",
                    font_size=24,
                    color=GREY_A,
                )
                .scale(0.8)
                .next_to(final[-1][i], RIGHT, buff=0.5)
                .set_z_index(-1)
                for i in range(out_ch)
            ]
        )
        something_words = VGroup(
            *[
                Words(
                    f"{somethings_strings[i]}",
                    font="Noto Sans KR",
                    font_size=24,
                    color=GREY_C,
                )
                .scale(0.8)
                .next_to(final[-1][i], RIGHT, buff=0.3)
                .set_z_index(-1)
                for i in range(out_ch)
            ]
        )
        swc = something_words.copy()
        predt = (
            Text("Prediction:", font="Noto Sans KR", font_size=24, color=GREEN_A)
            .scale(0.8)
            .next_to(pred_words, UP)
            .shift(LEFT * 0.3)
        )
        self.playw(FadeIn(predt))
        self.playw(
            *[FadeIn(something_words[i], shift=RIGHT * 0.5) for i in range(out_ch)],
        )

        label_words = VGroup(
            *[
                Words(
                    f"{label_strings[i]}",
                    font="Noto Sans KR",
                    font_size=24,
                    color=GREEN_B,
                )
                .scale(0.8)
                .next_to(something_words[i], RIGHT, buff=0.7)
                for i in range(out_ch)
            ]
        )
        labelt = (
            Text("Label:", font="Noto Sans KR", font_size=24, color=YELLOW_A)
            .scale(0.8)
            .next_to(predt, RIGHT, buff=0.8)
        )
        self.playw(FadeIn(labelt))
        self.play(FadeIn(label_words[0], shift=LEFT * 0.5))
        self.play(
            FadeOut(
                label_words[0].copy(), target_position=something_words[0], scale=0.7
            ),
            run_time=0.5,
        )
        self.playw(
            Indicate(something_words[0], color=GREEN_B),
            Indicate(something_words[1:], color=RED_B, scale_factor=1.0),
        )
        self.playw(
            Transform(
                something_words[0],
                pred_words[0],
                replace_mobject_with_target_in_scene=True,
            )
        )

        self.play(FadeIn(label_words[1], shift=LEFT * 0.5))
        self.play(
            FadeOut(
                label_words[1].copy(), target_position=something_words[1], scale=0.7
            ),
            run_time=0.5,
        )
        self.play(
            Indicate(something_words[1], color=GREEN_B),
            Indicate(something_words[2:], color=RED_B, scale_factor=1.0),
            Indicate(pred_words[0], color=RED_B, scale_factor=1.0),
        )
        self.playw(
            Transform(
                something_words[1],
                pred_words[1],
                replace_mobject_with_target_in_scene=True,
            )
        )

        self.playwl(
            *[FadeIn(label_words[i], shift=LEFT * 0.5) for i in range(2, out_ch)],
            wait=0,
        )
        self.playwl(
            *[
                FadeOut(
                    label_words[i].copy(), target_position=something_words[i], scale=0.7
                )
                for i in range(2, out_ch)
            ],
            run_time=1,
            wait=0,
        )
        self.playwl(
            *[
                Transform(
                    something_words[i],
                    pred_words[i],
                    replace_mobject_with_target_in_scene=True,
                )
                for i in range(2, out_ch)
            ],
            run_time=1,
        )

        img_in1 = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )

        img_in2 = (
            ImageMobject("cat2.jpg")
            .scale(0.25)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        imgs = (
            Group(img_in1, img_in2)
            .arrange(DOWN, buff=0.5)
            .next_to(model, LEFT, buff=0.5)
        )
        self.playw(Restore(final[-1]))

        self.playw(FadeIn(imgs))
        pred_words.generate_target().set_color(GREY_D)
        label_words.generate_target().set_color(GREY_D)
        pred_words.target[1].set_color(PURE_GREEN)
        label_words.target[1].set_color(PURE_GREEN)
        self.play(MoveToTarget(pred_words), MoveToTarget(label_words), run_time=3)
        self.playw(
            Circumscribe(
                VGroup(pred_words[1], label_words[1]),
                color=PURE_GREEN,
                stroke_width=2,
                buff=0.1,
            )
        )

        self.playw(FadeOut(labelt, label_words))
        self.playw(
            Transform(pred_words, swc, replace_mobject_with_target_in_scene=True)
        )
        self.playw(swc.animate.set_color(RED_B), predt.animate.set_color(RED_A))

        self.play(img_in1.animate.move_to(model).scale(0.5))
        self.remove(img_in1)
        self.playwl(
            Wiggle(model),
            Transform(
                final[-1], pred_vector, replace_mobject_with_target_in_scene=True
            ),
            lag_ratio=0.5,
        )
        pred_nums2 = [random() * 15 for _ in range(out_ch)]
        pred_vector2 = VGroup(
            *[
                DecimalNumber(num, num_decimal_places=2, color=GREY_A, font_size=30)
                .move_to(final[-1][i])
                .align_to(final[-1][i], LEFT)
                for i, num in enumerate(softmax(pred_nums2))
            ]
        )

        self.play(img_in2.animate.move_to(model).scale(0.5))
        self.remove(img_in2)
        self.playwl(
            Wiggle(model), pred_vector.animate.become(pred_vector2), lag_ratio=0.5
        )


class dinodistill(Scene2D):
    def construct(self):
        dino = Text("DiNO", font="Noto Sans KR", font_size=48)
        distill = Text(
            "Distillation", font="Noto Sans KR", font_size=40
        ).set_color_by_gradient(GREEN_A, GREEN_B)
        ema = Text("EMA", font="Noto Sans KR", font_size=40).set_color_by_gradient(
            YELLOW_A, YELLOW_B
        )
        methods = VGroup(distill, ema).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.playw(FadeIn(dino), wait=0.5)
        self.playw(dino.animate.shift(UP * 2.5).set_color(GREY_B))
        self.playw(FadeIn(distill))
        self.playw(FadeIn(ema))
        ema_full = Words(
            "Exponential Moving Average",
            font="Noto Sans KR",
            font_size=32,
            color=YELLOW_A,
        ).next_to(ema, RIGHT, buff=0.5)
        self.playwl(*[FadeIn(item) for item in ema_full.words], lag_ratio=0.3)
        self.play(FadeOut(dino, ema_full, ema))
        self.playw(distill.animate.shift(UP * 2.5))

        student = Rectangle(
            width=2,
            height=1,
            color=GREEN_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        )
        studentt = Text(
            "Student\n   Model",
            font="Noto Sans KR",
            font_size=24,
            color=GREEN_C,
            line_spacing=0.8,
        ).move_to(student)
        student = VGroup(student, studentt).shift(DOWN * 1.4)
        teacher = Rectangle(
            width=2,
            height=1,
            color=GREY_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        )
        teachert = Text(
            "Teacher\n   Model",
            font="Noto Sans KR",
            font_size=24,
            color=GREY_C,
            line_spacing=0.8,
        ).move_to(teacher)
        teacher = VGroup(teacher, teachert).shift(UP * 0.7 + RIGHT * 0.3)
        self.playw(FadeIn(student), FadeIn(teacher))

        img_in1 = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(student, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        img_in2 = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(teacher, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        self.play(FadeIn(img_in1, img_in2))
        self.play(
            img_in1.animate.move_to(student).scale(0.5),
            img_in2.animate.move_to(teacher).scale(0.5),
        )
        self.remove(img_in1, img_in2)
        out_ch = 10
        final_s = (
            nn.Linear(2, out_ch).move_to(student.get_right()).set_z_index(-1).scale(0.5)
        )
        final_s[-1].set_stroke(width=2)
        final_t = (
            nn.Linear(2, out_ch).move_to(teacher.get_right()).set_z_index(-1).scale(0.5)
        )
        final_t[-1].set_color(BLUE).set_stroke(width=2)
        self.play(FadeIn(final_s), FadeIn(final_t))
        final_tc = final_t[-1].copy()
        final_t[0].set_opacity(0)
        self.play(final_tc.animate.move_to(final_s[-1]), FadeOut(teacher, final_t[:-1]))
        self.playw(
            FadeOut(final_tc), Indicate(final_s[-1], color=PURE_BLUE, scale_factor=1.0)
        )

        final_tc = final_t[-1].copy()
        self.add(final_tc)
        self.remove(final_t[-1])
        student_ = VGroup(student, final_s)
        student_.generate_target().move_to(ORIGIN)
        self.playw(
            MoveToTarget(student_),
            final_tc.animate.next_to(student_.target, RIGHT, buff=1.0),
        )
        labelt = Text("Label", font="Noto Sans KR", font_size=20, color=BLUE_A).next_to(
            final_tc, UP, buff=0.3
        )
        self.playw(FadeIn(labelt))
        self.play(FadeOut(final_tc.copy(), target_position=final_s[-1]))
        self.playw(Indicate(final_s[-1], color=BLUE_D, scale_factor=1.0))


class dinoema(Scene2D):
    def construct(self):
        ema = Text("EMA", font="Noto Sans KR", font_size=48).set_color_by_gradient(
            YELLOW_A, YELLOW_B
        )
        ema_full = Words(
            "Exponential Moving Average",
            font="Noto Sans KR",
            font_size=32,
        ).set_color_by_gradient(YELLOW_A, YELLOW_B)
        ema_ = VGroup(*[item[1:] for item in ema_full.words])
        self.playw(FadeIn(ema))
        self.playwl(
            AnimationGroup(
                *[
                    Transform(
                        ema[i],
                        ema_full.words[i][0],
                        replace_mobject_with_target_in_scene=True,
                    )
                    for i in range(len(ema))
                ]
            ),
            FadeIn(ema_),
            lag_ratio=0.5,
        )


class howdino(Scene2D):
    def construct(self):
        dino = Text("DiNO", font="Noto Sans KR", font_size=48).set_color_by_gradient(
            BLUE_A, BLUE_B
        )
        distill = Text(
            "Distillation", font="Noto Sans KR", font_size=36
        ).set_color_by_gradient(GREEN_A, GREEN_B)
        ema = Text("EMA", font="Noto Sans KR", font_size=36).set_color_by_gradient(
            YELLOW_A, YELLOW_B
        )
        methods = VGroup(distill, ema).arrange(RIGHT, buff=0.5)
        self.playw(FadeIn(dino))
        self.playw(dino.animate.shift(UP * 3), FadeIn(distill, shift=UP), wait=0.5)
        self.playw(FadeIn(ema))

        self.play(FadeOut(methods))

        model = Rectangle(
            width=2,
            height=1,
            color=GREEN_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        )
        modelt = Text(
            "Model", font="Noto Sans KR", font_size=24, color=GREEN_C
        ).move_to(model)
        model = VGroup(model, modelt)
        self.playw(FadeIn(model))

        img_in = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        self.playw(FadeIn(img_in))
        self.playw(img_in.animate.move_to(model).scale(0.5))
        self.remove(img_in)
        out_ch = 10
        final = (
            nn.Linear(2, out_ch).move_to(model.get_right()).set_z_index(-1).scale(0.7)
        )
        final[0].set_opacity(0)
        self.playw(FadeIn(final))

        something_words = VGroup(
            *[
                Words(
                    f"something{i}",
                    font="Noto Sans KR",
                    font_size=24,
                    color=GREY_C,
                )
                .scale(0.8)
                .next_to(final[-1][i], RIGHT, buff=0.3)
                .set_z_index(-1)
                for i in range(out_ch)
            ]
        )
        predt = (
            Text("Prediction:", font="Noto Sans KR", font_size=24, color=GREEN_A)
            .scale(0.8)
            .next_to(something_words, UP)
        )
        self.playw(
            *[FadeIn(something_words[i], shift=RIGHT * 0.5) for i in range(out_ch)],
            FadeIn(predt),
        )

        left = VGroup(model, final, something_words, predt)
        self.play(left.animate.shift(LEFT * 5))

        model_t = Rectangle(
            width=2.5,
            height=1.1,
            color=GREY_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        )
        modelt_t = (
            Text("EMA Model", font="Noto Sans KR", font_size=24, color=BLUE_C)
            .move_to(model_t)
            .set_opacity(0)
        )
        model_t = VGroup(model_t, modelt_t).shift(RIGHT * 3)
        self.playw(FadeIn(model_t))
        final_t = (
            nn.Linear(2, out_ch).move_to(model_t.get_right()).set_z_index(-1).scale(0.7)
        )
        final_t[0].set_opacity(0)
        final_t[-1].set_color(BLUE)
        self.playw(FadeIn(final_t))
        self.play(modelt_t.animate.set_opacity(1))
        self.playw(Flash(modelt_t.get_corner(UL), color=BLUE_C))

        shade = Rectangle(
            height=self.cf.height,
            width=self.cf.width,
            fill_opacity=0.7,
            fill_color=BLACK,
            stroke_opacity=0,
        ).set_z_index(5)
        VGroup(model, model_t).set_z_index(10)
        self.playw(FadeIn(shade))

        model.save_state(), model_t.save_state(), self.cf.save_state()
        self.playw(
            VGroup(model, model_t).animate.arrange(RIGHT).shift(DOWN * 10),
            self.cf.animate.shift(DOWN * 10),
        )
        self.playw(Wiggle(model_t))
        self.play(Restore(model), Restore(model_t), Restore(self.cf))
        self.playw(shade.animate.set_opacity(0))

        self.playw(FadeOut(model_t, final_t[:-1]))

        arrows = VGroup(
            *[
                Arrow(
                    start=final_t[-1][i].get_left(),
                    end=something_words[i].get_right(),
                    buff=0.1,
                    stroke_width=3,
                    color=TEAL_A,
                    tip_length=0.15,
                )
                for i in range(out_ch)
            ]
        )
        self.play(*[GrowArrow(arrows[i]) for i in range(out_ch)])
        self.play(FadeOut(arrows), Indicate(final[-1], color=BLUE_B, scale_factor=1.0))
        self.playw(Wiggle(model))

        self.playw(FadeOut(something_words, predt), FadeIn(model_t, final_t[1]))

        modelc = VGroup(model, final).copy()
        self.play(modelc.animate.become(VGroup(model_t, final_t)))
        self.remove(modelc)

        self.playw(
            Flash(model_t.get_corner(UL), color=BLUE_C),
            Wiggle(VGroup(model_t, final_t)),
        )


class naivedino(Scene2D):
    def construct(self):
        model = Rectangle(
            width=2,
            height=1,
            color=GREEN_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        ).shift(LEFT * 0.5)
        modelt = Text(
            "Model", font="Noto Sans KR", font_size=24, color=GREEN_C
        ).move_to(model)
        final = nn.Linear(2, 10).move_to(model.get_right()).set_z_index(-1).scale(0.7)
        model = VGroup(model, modelt, final)
        self.playw(FadeIn(model))

        img_in1 = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        img_in2 = (
            ImageMobject("husky.png")
            .scale(0.5)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )

        out_ch = 10
        collapsed_num = [1.00 if i == 3 else 0.00 for i in range(out_ch)]
        collapsed_vector = VGroup(
            *[
                DecimalNumber(num, num_decimal_places=2, color=GREY_A, font_size=30)
                .move_to(final[-1][i])
                .align_to(final[-1][i], LEFT)
                for i, num in enumerate(collapsed_num)
            ]
        )
        collapsed_vector[3].set_color(GREEN_C)
        final[-1].save_state()
        self.play(FadeIn(img_in1))
        self.play(img_in1.animate.move_to(model).scale(0.5))
        self.remove(img_in1)
        self.playwl(
            final[-1].animate.become(collapsed_vector),
            lag_ratio=0.5,
        )

        self.play(Restore(final[-1]))
        self.play(FadeIn(img_in2))
        self.play(img_in2.animate.move_to(model).scale(0.5))
        self.remove(img_in2)
        self.playwl(
            final[-1].animate.become(collapsed_vector),
            lag_ratio=0.5,
        )

        left = VGroup(model, final)
        self.play(left.animate.shift(LEFT * 3))
        ema_model = Rectangle(
            width=2.5,
            height=1.1,
            color=BLUE_B,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        )
        ema_modelt = Text(
            "EMA Model", font="Noto Sans KR", font_size=24, color=BLUE_C
        ).move_to(ema_model)
        final_t = (
            nn.Linear(2, out_ch)
            .move_to(ema_model.get_right())
            .set_z_index(-1)
            .scale(0.7)
        )
        final_t[0].set_opacity(0)
        final_t[-1].set_color(BLUE)
        ema_model = VGroup(ema_model, ema_modelt, final_t).shift(RIGHT * 2)
        self.playw(FadeIn(ema_model))

        img_int1 = (
            ImageMobject("cat.jpg")
            .scale(0.25)
            .next_to(ema_model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        img_int2 = (
            ImageMobject("husky.png")
            .scale(0.5)
            .next_to(ema_model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        self.play(FadeIn(img_int1))
        self.play(img_int1.animate.move_to(ema_model).scale(0.5))
        self.remove(img_int1)
        collapsed_vectort = VGroup(
            *[
                DecimalNumber(num, num_decimal_places=2, color=GREY_A, font_size=30)
                .move_to(final_t[-1][i])
                .align_to(final_t[-1][i], LEFT)
                for i, num in enumerate(collapsed_num)
            ]
        )
        collapsed_vectort[3].set_color(BLUE_C)
        final_t[-1].save_state()
        self.playwl(
            final_t[-1].animate.become(collapsed_vectort),
            lag_ratio=0.5,
        )
        self.play(Restore(final_t[-1]), FadeIn(img_int2))
        self.play(img_int2.animate.move_to(ema_model).scale(0.5))
        self.remove(img_int2)
        self.playwl(
            final_t[-1].animate.become(collapsed_vectort),
            lag_ratio=0.5,
        )
        img1 = (
            ImageMobject("cat.jpg")
            .scale(0.2)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        img2 = (
            ImageMobject("husky.png")
            .scale(0.5)
            .next_to(model, LEFT, buff=0.5)
            .set_z_index(-1)
        )
        eq = Text("=", color=RED)
        imgs = Group(img1, eq, img2).arrange(RIGHT, buff=0.5).shift(UP*2.5)
        self.playw(FadeIn(imgs))

        shade = Rectangle(
            height=self.cf.height,
            width=self.cf.width,
            fill_opacity=0.7,
            fill_color=BLACK,
            stroke_opacity=0,
        ).set_z_index(5)
        left.set_z_index(10)
        model[:2].set_z_index(11)
        self.playw(
            left.animate.set_stroke(color=RED_C),
            final.animate.set_color(RED_C),
            modelt.animate.set_color(RED_C),
            FadeIn(shade),
            FadeOut(imgs)
        )
