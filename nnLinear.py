from manim import *
from manimdef import DefaultManimClass, DefaultManimClass3D
from random import random
from copy import deepcopy


class LinearWandB(DefaultManimClass):
    def construct(self):
        in_dim, out_dim = 3, 5
        lineart = Text(
            f"nn.Linear({in_dim}, {out_dim})", font_size=36
        ).set_color_by_gradient(BLUE, TEAL)
        self.playw(FadeIn(lineart))
        weightt = Text(
            f"weight ({out_dim}*{in_dim})", font="Noto Sans KR", font_size=36
        ).set_color_by_gradient(BLUE)
        biast = Text(
            f"bias ({out_dim})", font="Noto Sans KR", font_size=36
        ).set_color_by_gradient(TEAL)

        self.playw(
            Transform(
                lineart,
                VGroup(weightt, biast).arrange(RIGHT, buff=1),
                replace_mobject_with_target_in_scene=True,
            )
        )
        matrix_list = [
            [MathTex(f"w_{{{i}{j}}}") for j in range(in_dim)] for i in range(out_dim)
        ]
        vector_list = [[MathTex(f"b_{{{i}}}")] for i in range(out_dim)]
        weight = MobjectMatrix(matrix_list).move_to(weightt).scale(0.7).set_color(BLUE)
        bias = MobjectMatrix(vector_list).move_to(biast).scale(0.7).set_color(TEAL)
        VGroup(weight, bias).arrange(RIGHT, buff=1.5).shift(LEFT)
        self.playw(
            Transform(weightt, weight, replace_mobject_with_target_in_scene=True)
        )
        self.playw(Transform(biast, bias, replace_mobject_with_target_in_scene=True))
        plus = Text("+", font_size=36).set_opacity(0)
        x_list = [[MathTex(f"x_{{{i}}}")] for i in range(in_dim)]
        x = MobjectMatrix(x_list).scale(0.7).set_color(GREEN).set_opacity(0)
        for item in [weight, x, plus, bias]:
            item.generate_target()
        plus.target.set_opacity(1)
        x.target.set_opacity(1)
        VGroup(weight.target, x.target, plus.target, bias.target).arrange(RIGHT).shift(
            LEFT * 0.7
        )

        self.playw(*[MoveToTarget(item) for item in [weight, x, plus, bias]])

        wx_list = [
            [
                MathTex(
                    *" + ".join(
                        [f"w_{{{i}{j}}} x_{{{j}}}" for j in range(in_dim)]
                    ).split(" ")
                )
            ]
            for i in range(out_dim)
        ]
        wx = (
            MobjectMatrix(wx_list)
            .scale(0.7)
            .next_to(plus, LEFT)
            .set_color_by_gradient(BLUE, GREEN)
        )
        self.playw(
            *[
                TransformMatchingTex(weight[0][i * in_dim : (i + 1) * in_dim], wx[0][i])
                for i in range(out_dim)
            ],
            Transform(weight[1], wx[1], replace_mobject_with_target_in_scene=True),
            Transform(x[2], wx[2], replace_mobject_with_target_in_scene=True),
            FadeOut(weight[2], x[1]),
            FadeOut(x[0], shift=LEFT),
        )
        wxb_list = [
            [
                VGroup(
                    MathTex(
                        *" + ".join(
                            [f"w_{{{i}{j}}} x_{{{j}}}" for j in range(in_dim)]
                        ).split(" ")
                    ),
                    MathTex(" + "),
                    MathTex(f"b_{{{i}}}"),
                ).arrange(RIGHT)
            ]
            for i in range(out_dim)
        ]
        wxb = (
            MobjectMatrix(wxb_list).scale(0.7).set_color_by_gradient(BLUE, GREEN, TEAL)
        )
        self.playw(
            *[
                Transform(
                    wx[0][i], wxb[0][i][0], replace_mobject_with_target_in_scene=True
                )
                for i in range(out_dim)
            ],
            *[
                Transform(
                    bias[0][i], wxb[0][i][2], replace_mobject_with_target_in_scene=True
                )
                for i in range(out_dim)
            ],
            *[
                Transform(
                    plus if i == out_dim // 2 else plus.copy(),
                    wxb[0][i][1],
                    replace_mobject_with_target_in_scene=True,
                )
                for i in range(out_dim)
            ],
            Transform(wx[1], wxb[1], replace_mobject_with_target_in_scene=True),
            Transform(bias[2], wxb[2], replace_mobject_with_target_in_scene=True),
            FadeOut(wx[2], bias[1]),
        )


class LinearIO(DefaultManimClass):
    def construct(self):
        in_dim, out_dim = 5, 9
        model = Rectangle(color=GREEN, height=9, width=16).scale(0.25)
        modelt = Text(
            f"nn.Linear({in_dim}, {out_dim})", font_size=28
        ).set_color_by_gradient(GREEN_A, GREEN_D)
        model = VGroup(model, modelt)
        self.playw(FadeIn(model))
        self.playw(Circumscribe(modelt[-4], stroke_width=3))
        self.playw(Circumscribe(modelt[-2], stroke_width=3))

        x_list = [[MathTex(f"x_{{{i}}}")] for i in range(in_dim)]
        x = MobjectMatrix(x_list).scale(0.7).next_to(model, LEFT, buff=0.75)
        y_hat_list = [[MathTex(f"\\hat{{y}}_{{{i}}}")] for i in range(out_dim)]
        y_hat = MobjectMatrix(y_hat_list).scale(0.7).next_to(model, RIGHT, buff=0.75)
        self.playw(FadeIn(x))
        self.playw(FadeOut(x, shift=RIGHT * 1.2, scale=0.5))
        self.playw(FadeIn(y_hat, shift=RIGHT * 1.2, scale=0.5))

        self.playw(VGroup(model, y_hat).animate.shift(UP * 8))

        fc_text = Text(f"fc = nn.Linear({in_dim}, {out_dim})", font_size=28)
        self.playw(FadeIn(fc_text))
        self.playw(
            fc_text[2:].animate.set_opacity(0), fc_text[:2].animate.move_to(ORIGIN)
        )

        matrix_list = [
            [MathTex(f"w_{{{i}{j}}}") for j in range(in_dim)] for i in range(out_dim)
        ]
        vector_list = [[MathTex(f"b_{{{i}}}")] for i in range(out_dim)]
        weight = MobjectMatrix(matrix_list).scale(0.6).set_color(BLUE)
        bias = MobjectMatrix(vector_list).scale(0.6).set_color(TEAL)
        wb = VGroup(weight, bias).arrange(RIGHT, buff=1).shift(LEFT)
        self.playw(
            LaggedStart(fc_text[:2].animate.shift(UP * 3), FadeIn(wb), lag_ratio=0.3)
        )
        r = lambda: f"{(random()-0.5)*1.9:.1f}"
        matrix_list = [
            [MathTex(f"{r()}") for j in range(in_dim)] for i in range(out_dim)
        ]
        vector_list = [[MathTex(f"{r()}")] for i in range(out_dim)]

        weight_init = (
            MobjectMatrix(matrix_list).scale(0.6).set_color(BLUE).move_to(weight)
        )
        bias_init = MobjectMatrix(vector_list).scale(0.6).set_color(TEAL).move_to(bias)
        self.playw(Transform(weight, weight_init), Transform(bias, bias_init))


class LinearExec(DefaultManimClass):
    def construct(self):
        in_dim, out_dim = 5, 9

        matrix_list = [
            [MathTex(f"w_{{{i}{j}}}") for j in range(in_dim)] for i in range(out_dim)
        ]
        vector_list = [[MathTex(f"b_{{{i}}}")] for i in range(out_dim)]
        weight = MobjectMatrix(matrix_list).scale(0.6).set_color(BLUE)
        bias = MobjectMatrix(vector_list).scale(0.6).set_color(TEAL)
        x_list = [[MathTex(f"x_{{{i}}}")] for i in range(in_dim)]
        x = MobjectMatrix(x_list).scale(0.7).next_to(weight, RIGHT, buff=0.5)

        heightb = Brace(weight, LEFT)
        widthb = Brace(weight, UP)
        heightt = Text(f"{out_dim}", font_size=24).next_to(heightb, LEFT)
        widtht = Text(f"{in_dim}", font_size=24).next_to(widthb, UP)
        self.play(FadeIn(weight), DrawBorderThenFill(heightb), FadeIn(heightt))
        self.playw(DrawBorderThenFill(widthb), FadeIn(widtht))
        self.playw(
            FadeIn(x),
            FadeOut(heightb, widthb, heightt, widtht),
            self.cf.animate.move_to(VGroup(weight, x)),
        )
        self.playw(VGroup(weight, x, self.cf).animate.move_to(ORIGIN))

        self.playw(
            LaggedStart(
                *[Wiggle(item[0], scale_value=1.5) for item in x_list], lag_ratio=0.1
            )
        )
        WxTex = MathTex("W", "\\cdot", "x", font_size=48).next_to(VGroup(weight, x), UP)
        WxTex[0].set_color(BLUE)
        self.playw(FadeIn(WxTex, scale=1.1))
        self.playw(
            Circumscribe(
                VGroup(*[item for item in matrix_list[0]]), stroke_width=2, color=BLUE
            ),
            Circumscribe(x[0], stroke_width=2, color=WHITE),
        )
        orig_lists = []
        for j in range(out_dim):
            plus = lambda: VGroup(MathTex("+", font_size=28))
            x_list_ = deepcopy(x_list) if j != out_dim - 1 else x_list
            for i in range(len(matrix_list[j])):
                matrix_list[j][i].generate_target()
                x_list_[i][0].generate_target()

            arrange_list = []
            orig_list = []
            orig_plus_list = []
            for i in range(len(matrix_list[j])):
                if i:
                    arrange_list.append(p := plus())
                    orig_plus_list.append(p)
                arrange_list.extend([matrix_list[j][i].target, x_list_[i][0].target])
                orig_list.extend([matrix_list[j][i], x_list_[i][0]])
            VGroup(*arrange_list).arrange(RIGHT, buff=0.05).move_to(
                matrix_list[j][in_dim // 2]
            )
            x_ = VGroup(
                VGroup(*[x_list[i][0] for i in range(len(x_list_))]), x[1], x[2]
            )
            if j == 0:
                self.playw(
                    *[MoveToTarget(item) for item in orig_list],
                    *[FadeIn(item) for item in orig_plus_list],
                    x_.animate.shift(RIGHT),
                    weight[1]
                    .animate.next_to(arrange_list[0], LEFT)
                    .align_to(weight[1], UP),
                    weight[2]
                    .animate.next_to(arrange_list[-1], RIGHT)
                    .align_to(weight[2], UP),
                )
                self.playw(Circumscribe(VGroup(*orig_list), stroke_width=2))
            else:
                self.play(
                    *[MoveToTarget(item) for item in orig_list],
                    *[FadeIn(item) for item in orig_plus_list],
                )
            if j == out_dim - 1:
                self.playw(FadeOut(x[1], x[2]))
            orig_lists.append(orig_list)
        p = plus().next_to(weight[2])
        bias.next_to(p)
        self.playw(FadeIn(p, bias))
        self.playw(
            LaggedStart(
                *[Wiggle(item[0], scale_value=1.5) for item in vector_list],
                lag_ratio=0.1,
            )
        )
        pluses = []
        for i in range(out_dim):
            pluses.append(plus().next_to(orig_lists[i][-1], buff=0.05))
            vector_list[i][0].generate_target().next_to(pluses[-1], buff=0.05)
        self.playw(
            *[FadeIn(p_) for p_ in pluses],
            *[MoveToTarget(vector_list[i][0]) for i in range(out_dim)],
            FadeOut(bias[1:], p),
            weight[2].animate.next_to(vector_list[0][0].target).align_to(weight[2], UP),
        )


class LinearError(DefaultManimClass):
    def construct(self):
        in_dim, out_dim = 5, 9

        matrix_list = [
            [MathTex(f"w_{{{i}{j}}}") for j in range(in_dim)] for i in range(out_dim)
        ]
        vector_list = [[MathTex(f"b_{{{i}}}")] for i in range(out_dim)]
        weight = MobjectMatrix(matrix_list).scale(0.6).set_color(BLUE)
        bias = MobjectMatrix(vector_list).scale(0.6).set_color(TEAL)
        x_list = [[MathTex(f"x_{{{i}}}")] for i in range(in_dim + 1)]
        x = MobjectMatrix(x_list).scale(0.7).next_to(weight, RIGHT, buff=0.5)

        self.playw(FadeIn(weight, x))
        orig_lists = []
        for j in range(out_dim):
            plus = lambda: VGroup(MathTex("+", font_size=28))
            x_list_ = deepcopy(x_list) if j != out_dim - 1 else x_list
            for i in range(len(matrix_list[j])):
                matrix_list[j][i].generate_target()
                x_list_[i][0].generate_target()

            arrange_list = []
            orig_list = []
            orig_plus_list = []
            for i in range(len(matrix_list[j])):
                if i:
                    arrange_list.append(p := plus())
                    orig_plus_list.append(p)
                arrange_list.extend([matrix_list[j][i].target, x_list_[i][0].target])
                orig_list.extend([matrix_list[j][i], x_list_[i][0]])
            VGroup(*arrange_list).arrange(RIGHT, buff=0.05).move_to(
                matrix_list[j][in_dim // 2]
            )
            x_ = VGroup(
                VGroup(*[x_list[i][0] for i in range(len(x_list_))]), x[1], x[2]
            )

            if j == 0:
                x_[0].set_opacity(0)
                x_[0][-1].set_opacity(1)
                self.playw(
                    *[MoveToTarget(item) for item in orig_list],
                    *[FadeIn(item) for item in orig_plus_list],
                    # x_.animate.shift(RIGHT),
                    x_.animate.shift(RIGHT),
                    weight[1]
                    .animate.next_to(arrange_list[0], LEFT)
                    .align_to(weight[1], UP),
                    weight[2]
                    .animate.next_to(arrange_list[-1], RIGHT)
                    .align_to(weight[2], UP),
                )
                self.playw(x_[0][-1].animate.set_color(PURE_RED).scale(1.2))
            else:
                self.play(
                    *[MoveToTarget(item) for item in orig_list],
                    *[FadeIn(item) for item in orig_plus_list],
                )
            if j == out_dim - 1:
                self.playw(FadeOut(x[1], x[2]))
            orig_lists.append(orig_list)
            break


class LinearTensor(DefaultManimClass3D):
    def construct(self):
        in_dim, out_dim = 5, 9
        tensor_shape = 6, 7
        tilt_degree = 60 * DEGREES
        self.set_camera_orientation(zoom=1)
        self.rotate_camera(phi=tilt_degree)

        def gen_x(in_dim):
            x_list = [[MathTex(f"x_{{{i}}}")] for i in range(in_dim)]
            x = MobjectMatrix(x_list).scale(0.7).rotate(angle=tilt_degree, axis=RIGHT)
            VGroup(x[1], x[2]).set_opacity(0.3)
            return x

        tensor_list = [
            [gen_x(in_dim) for j in range(tensor_shape[0])] for i in range(tensor_shape[1])
        ]
        tensor = MobjectMatrix(tensor_list, h_buff=2.6, v_buff=1.6).scale(0.7).shift(OUT)
        tensor.save_state()
        tensor.set_opacity(0)
        tensor_list[tensor_shape[1]//2][tensor_shape[0]//2].set_opacity(1).scale(1.5)
        self.playw(FadeIn(tensor))

        self.move_camera(
            phi=tilt_degree, theta=-60 * DEGREES, zoom=0.7, run_time=1.5, added_anims=[Restore(tensor)]
        )
        self.wait()
        out_tensor_list = [
            [gen_x(out_dim) for j in range(tensor_shape[0])] for i in range(tensor_shape[1])
        ]
        out_tensor = MobjectMatrix(out_tensor_list, h_buff=2.6, v_buff=1.6).scale(0.7).shift(OUT)
        self.playw(Transform(tensor, out_tensor))
        tensor.save_state()
        tensor.generate_target().set_opacity(0)
        item = tensor_list[tensor_shape[1]//2][tensor_shape[0]//2].copy().set_color(PURE_GREEN)
        self.move_camera(
            phi=tilt_degree, theta=-60 * DEGREES, zoom=1.5, run_time=1.5, added_anims=[MoveToTarget(tensor), FadeIn(item)]
        )
        self.move_camera(
            phi=tilt_degree, theta=-60 * DEGREES, zoom=0.7, run_time=1.5, added_anims=[Restore(tensor), FadeOut(item)]
        )
