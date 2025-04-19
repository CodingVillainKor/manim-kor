from manim import *
from manimdef import DefaultManimClass, CodeText, SurroundingRect
import torch
import torch.nn as nn
from torchdiffeq import odeint_adjoint as odeint
from functools import partial

true_A = torch.tensor([[-0.1, 2.0], [-2.0, -0.1]])
true_y0 = torch.tensor([[2.0, 0.0]])
t = torch.linspace(0.0, 25.0, 1000)


class Lambda(nn.Module):
    def forward(self, t, y):
        if isinstance(y, (list, tuple)):
            y = torch.tensor(y)[None]
        if y.ndim == 1:
            y = y[None]
        return torch.mm(y**3, true_A).squeeze()


fn = Lambda()
with torch.no_grad():
    true_y = odeint(fn, true_y0, t, method="dopri5")


def vel_dest(start, vel):
    if isinstance(vel, (list, tuple)):
        vel = torch.tensor(vel)
    if isinstance(start, (list, tuple)):
        start = torch.tensor(start)

    return (start + vel).tolist()


class NumericalMeaning(DefaultManimClass):
    def construct(self):
        nump = NumberPlane(x_range=(-3, 3, 1.5), y_range=(-3, 3, 1.5)).set_opacity(0.3)
        x_v = torch.tensor([0.5, 0.3])
        x = Dot(nump.c2p(*x_v.tolist()), color=BLUE)
        x_text = (
            Text("data x", font="Noto Serif KR", font_size=24)
            .next_to(x, direction=RIGHT + UP, buff=0.1)
            .set_color_by_gradient(YELLOW, PURE_GREEN)
        )
        x_t = (
            MathTex("x", "(", "t_0", ")", font_size=24)
            .set_color_by_gradient(BLUE, TEAL)
            .next_to(x, buff=0.1)
        )

        self.playw(FadeIn(nump))
        self.play(FadeIn(x, x_text, x_t))
        self.playw(FadeOut(x_text))
        x_t.add_updater(lambda p: p.next_to(x, buff=0.1))

        dest = vel_dest(x_v, fn(None, x_v))
        vel_arrow = Arrow(
            nump.c2p(*x_v.tolist()), nump.c2p(*dest), color=YELLOW, stroke_width=2
        )
        dxdt = MathTex(
            "{",
            "dx",
            r"\over",
            r"dt",
            "}",
            r"\cdot",
            r"\Delta",
            "t",
            font_size=18,
            color=YELLOW,
        ).next_to(vel_arrow, direction=RIGHT + UP, buff=0.03)
        self.playw(GrowArrow(vel_arrow), FadeIn(dxdt), self.cf.animate.scale(0.7))
        self.play(
            FadeOut(vel_arrow),
            FadeOut(dxdt),
            x.animate.move_to(nump.c2p(*dest)),
            x_t.animate.become(
                MathTex(
                    "x", "(", "t_0 + \\Delta t", ")", font_size=24
                ).set_color_by_gradient(BLUE, TEAL)
            ),
        )
        x_v = torch.tensor(dest)
        for i in range(3):
            dest = vel_dest(x_v, fn(None, x_v))
            varr = Arrow(
                nump.c2p(*x_v.tolist()),
                nump.c2p(*dest),
                color=YELLOW,
                stroke_width=2,
                buff=0,
            )
            dxdt.next_to(nump.c2p(*dest), direction=UP, buff=0.2)
            self.play(GrowArrow(varr), FadeIn(dxdt))
            self.play(
                FadeOut(varr),
                FadeOut(dxdt),
                x.animate.move_to(nump.c2p(*dest)),
                x_t.animate.become(
                    MathTex(
                        "x", "(", f"t_0+{i+2} \\times \\Delta t", ")", font_size=24
                    ).set_color_by_gradient(BLUE, TEAL)
                ),
            )
            x_v = torch.tensor(dest)


class NODEData(DefaultManimClass):
    def construct(self):
        nump = NumberPlane(x_range=(-3, 3, 1.5), y_range=(-3, 3, 1.5)).set_opacity(0.3)
        self.playw(FadeIn(nump))

        xdot = Dot(
            nump.c2p(*true_y0[0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        ).set_opacity(0)
        self.playw(xdot.animate.set_opacity(1.0))
        # v = ValueTracker(0)
        # get_point = lambda i: true_y[i].squeeze().tolist()
        # xdot.add_updater(lambda x: x.move_to(nump.c2p(*get_point(int(v.get_value())))))
        # self.playw(v.animate.set_value(999), run_time=15)
        data_indices = [10, 50, 100, 200, 300, 400, 500, 600, 700]
        data_dots = []
        for i in range(1000):
            if i in data_indices:
                data_dot = xdot.copy().set_color(YELLOW).scale(0.8)
                data_dots.append(data_dot)
                self.add(data_dot)
            self.play(
                xdot.animate.move_to(nump.c2p(*true_y[i].squeeze().tolist())),
                run_time=0.03,
                rate_func=rate_functions.linear,
            )
        self.wait()
        data_dots = VGroup(*data_dots)
        data_dots_arrange = data_dots.copy()
        data_dots_arrange.generate_target().arrange(DOWN).next_to(nump, RIGHT)
        dlines = VGroup(
            *[
                DashedLine(d, da, stroke_width=3, color=GREY_D)
                for d, da in zip(data_dots, data_dots_arrange.target)
            ]
        )
        data_texts = VGroup(
            *[
                CodeText(
                    f"[{t[di].item():5.2f}, {true_y[di][0, 0].item():5.2f}, {true_y[di][0, 1].item():5.2f}]",
                    font_size=18,
                )
                .next_to(data_dots_arrange.target[i])
                .set_color_by_gradient(BLUE, TEAL)
                for i, di in enumerate(data_indices)
            ]
        )
        data_rep = MathTex("[", "t,", "x_0,", "x_1", "]", font_size=20)
        data_rep[0].next_to(data_texts[0][0], UP)
        data_rep[-1].next_to(data_texts[0][-1], UP)
        data_rep[1].next_to(data_texts[0][1:5], UP).scale(1.3)
        data_rep[2].next_to(data_texts[0][6:10], UP).scale(1.3)
        data_rep[3].next_to(data_texts[0][11:15], UP).scale(1.3)
        self.play(
            self.cf.animate.shift(RIGHT),
            FadeIn(data_rep),
            MoveToTarget(data_dots_arrange),
            *[Create(dl) for dl in dlines],
            run_time=1,
        )
        self.playw(LaggedStart(*[FadeIn(dt) for dt in data_texts], lag_ratio=0.1))


class RNNModel(DefaultManimClass):
    def construct(self):
        nump = NumberPlane(x_range=(-3, 3, 1.5), y_range=(-3, 3, 1.5)).set_opacity(0.3)

        xdot = Dot(
            nump.c2p(*true_y0[0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        ).set_opacity(0)
        self.playw(FadeIn(nump), xdot.animate.set_opacity(1.0))
        data_indices = [10, 17, 23, 40, 55, 65, 70, 80, 90, 95]
        data_dots = []
        ttexts = []
        for i in range(130):
            if i in data_indices:
                data_dot = xdot.copy().set_color(YELLOW).scale(0.8)
                ttext = CodeText(f"{t[i].item():.1f}", font_size=16).next_to(
                    data_dot, UP + LEFT, buff=0.05
                )
                data_dots.append(data_dot)
                ttexts.append(ttext)
                self.add(data_dot, ttext)
            self.play(
                xdot.animate.move_to(nump.c2p(*true_y[i].squeeze().tolist())),
                run_time=0.03,
                rate_func=rate_functions.linear,
            )
        self.playw(FadeOut(xdot), run_time=0.5)
        data_dots = VGroup(*data_dots)
        ttexts = VGroup(*ttexts)
        dls = []
        for i in range(len(data_dots) - 1):
            dls.append(
                DashedLine(data_dots[i], data_dots[i + 1], stroke_width=3, color=GREY_D)
            )
        dls = VGroup(*dls)
        for i in range(len(dls)):
            self.play(Create(dls[i]), run_time=0.5)
        self.wait(2)

        numl = (
            NumberLine(x_range=(-0.1, 2.6, 1), length=12)
            .next_to(nump, UP, buff=0.5)
            .set_opacity(0.5)
        )

        def dl_fn(item, si, ei):
            return item.become(
                DashedLine(data_dots[si], data_dots[ei], stroke_width=3, color=GREY_D)
            )

        def tn_fn(x, target):
            return x.next_to(target, UP + LEFT, buff=0.05)

        for i, dd in enumerate(data_dots):
            ttexts[i].add_updater(partial(tn_fn, target=dd))
            if i < len(dls):
                dls[i].add_updater(partial(dl_fn, si=i, ei=i + 1))
        self.playw(
            self.cf.animate.move_to(numl),
            FadeIn(numl),
            LaggedStart(
                *[
                    dd.animate.move_to(numl.n2p(t[data_indices[i]].item()))
                    for i, dd in enumerate(data_dots)
                ]
            ),
        )


class NeuralODEModel(DefaultManimClass):
    def construct(self):
        nump = (
            NumberPlane(x_range=(-3, 3, 1.5), y_range=(-3, 3, 1.5))
            .set_opacity(0.3)
            .scale(0.8)
        )
        model = ImageMobject("odefunccode.png").scale(1.5)
        Group(nump, model).arrange(RIGHT)

        xdot = Dot(
            nump.c2p(*true_y0[0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        )
        self.add(nump, xdot, model)
        self.wait()

        for i in range(1, 10 + 1):
            xdot_in = xdot.copy()
            next_c = true_y[i, 0].tolist()
            arrow_model_out = Arrow(xdot_in, nump.c2p(*next_c), buff=0)
            dxdt = MathTex(r"{dx", r"\over", "dt}", font_size=20).next_to(
                arrow_model_out, RIGHT if i < 5 else UP, buff=0.08
            )
            dxdt.save_state()
            arrow_model_out.save_state()
            dxdt.move_to(model).set_opacity(0)
            arrow_model_out.move_to(model).set_opacity(0)
            self.play(xdot_in.animate.move_to(model).set_opacity(0.0), run_time=0.5)
            self.play(Restore(arrow_model_out), Restore(dxdt), run_time=0.5)
            self.play(
                xdot.animate.move_to(nump.c2p(*next_c)),
                FadeOut(arrow_model_out, dxdt),
                run_time=0.7,
            )
            if i == 0:
                self.wait()


class ModelTrain(DefaultManimClass):
    def construct(self):
        x_data = MathTex("[", "0.0,", "0.8,", "0.1", "]", font_size=36)
        y_data = MathTex("[", "0.1,", "0.7,", "0.3", "]", font_size=36)
        model = Text("model", font="Noto Serif KR", font_size=36).set_color_by_gradient(
            YELLOW, PURE_GREEN
        )
        model = VGroup(
            SurroundingRect(color=GREEN_D).surround(
                model, buf_height=0.5, buf_width=0.5
            ),
            model,
        ).shift(UP * 2)
        VGroup(x_data, y_data).arrange(RIGHT, buff=0.5)
        x_label = CodeText("x").next_to(x_data, DOWN, buff=0.2)
        y_label = CodeText("y").next_to(y_data, DOWN, buff=0.2)
        y_hat_data = MathTex("[", "0.2", "-0.1,", "0.7", "]", font_size=36).move_to(
            x_data
        )
        yhat_label = CodeText("y_hat").next_to(y_hat_data, DOWN, buff=0.2)
        y_hat_data.save_state()
        y_hat_data.move_to(model).set_opacity(0)

        self.playw(FadeIn(x_data, model, y_data, x_label, y_label))
        self.play(x_data.animate.move_to(model).set_opacity(0), FadeOut(x_label))
        self.play(Wiggle(model, scale_value=1.3, rotation_angle=0.02 * TAU))
        self.playw(Restore(y_hat_data), FadeIn(yhat_label))
        loss = MathTex(r"\operatorname{loss} = 0.13", font_size=36)
        self.playw(
            FadeOut(y_hat_data, yhat_label, shift=RIGHT * 0.5),
            FadeOut(y_data, y_label, shift=LEFT * 0.5),
            FadeIn(loss),
        )


class NeuralODETrainProblem(DefaultManimClass):
    def construct(self):
        x_data = MathTex("[", "0.0,", "0.8,", "0.1", "]", font_size=36)
        y_data = MathTex("[", "0.1,", "0.7,", "0.3", "]", font_size=36)
        model = Text("model", font="Noto Serif KR", font_size=36).set_color_by_gradient(
            YELLOW, PURE_GREEN
        )
        model = VGroup(
            SurroundingRect(color=GREEN_D).surround(
                model, buf_height=0.5, buf_width=0.5
            ),
            model,
        ).shift(UP * 2)
        VGroup(x_data, y_data).arrange(RIGHT, buff=0.5)
        x_label = CodeText("x").next_to(x_data, DOWN, buff=0.2)
        y_label = CodeText("y").next_to(y_data, DOWN, buff=0.2)
        y_hat_data = MathTex("[", "-0.1,", "0.7", "]", font_size=36).move_to(x_data)
        yhat_label = CodeText("y_hat").next_to(y_hat_data, DOWN, buff=0.2)
        y_hat_data.save_state()
        y_hat_data.move_to(model).set_opacity(0)

        self.playw(FadeIn(x_data, model, y_data, x_label, y_label))
        self.play(x_data.animate.move_to(model).set_opacity(0), FadeOut(x_label))
        self.play(Wiggle(model, scale_value=1.3, rotation_angle=0.02 * TAU))
        self.playw(Restore(y_hat_data), FadeIn(yhat_label))

        self.playw(Indicate(VGroup(y_hat_data, yhat_label)))
        self.playw(Indicate(VGroup(y_data, y_label)))
        self.playw(
            VGroup(y_hat_data, yhat_label, y_data, y_label).animate.set_color(PURE_RED)
        )


class NeuralODETrain(DefaultManimClass):
    def construct(self):
        nump = (
            NumberPlane(x_range=(-3, 3, 1.5), y_range=(-3, 3, 1.5))
            .set_opacity(0.3)
            .scale(0.8)
        )
        model = ImageMobject("odefunccode.png").scale(1.5)
        Group(nump, model).arrange(RIGHT)

        xdot = Dot(
            nump.c2p(*true_y0[0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        )
        self.add(nump, xdot, model)
        self.wait()

        for i in range(1, 1 + 1):
            xdot_in = xdot.copy()
            purturb = torch.zeros_like(true_y[i, 0]) + 0.3
            model_out = true_y[i, 0] + purturb
            true_out = true_y[i, 0].tolist()
            model_out = model_out.tolist()
            arrow_model_out = Arrow(xdot_in, nump.c2p(*model_out), buff=0)
            dxdt = MathTex(r"{dx", r"\over", "dt}", font_size=20).next_to(
                arrow_model_out, RIGHT if i < 5 else UP, buff=0.08
            )
            dxdt.save_state()
            arrow_model_out.save_state()
            dxdt.move_to(model).set_opacity(0)
            arrow_model_out.move_to(model).set_opacity(0)
            self.play(xdot_in.animate.move_to(model).set_opacity(0.0), run_time=0.5)
            self.playw(Restore(arrow_model_out), Restore(dxdt), run_time=0.5)
            xdot_hat = xdot.copy()
            self.playw(
                xdot_hat.animate.move_to(nump.c2p(*model_out)),
                FadeOut(dxdt),
                run_time=0.7,
            )
            xdot_ = xdot.copy().set_opacity(0)
            arrow_true = Arrow(xdot, nump.c2p(*true_out), buff=0, color=PURE_GREEN)
            self.play(GrowArrow(arrow_true))
            self.play(xdot.animate.move_to(nump.c2p(*true_out)))
            self.playw(
                self.cf.animate.move_to(xdot).scale(0.25),
                xdot.animate.scale(0.5),
                xdot_hat.animate.scale(0.5),
                arrow_true.animate.set_opacity(0.3),
                arrow_model_out.animate.set_opacity(0.3),
            )
            dl = DashedLine(
                xdot,
                xdot_hat,
                stroke_width=2,
                color=PURE_RED,
                dash_length=DEFAULT_DASH_LENGTH * 0.3,
            )
            self.playw(Create(dl))

            dl.add_updater(
                lambda x: x.become(
                    DashedLine(
                        xdot,
                        xdot_hat,
                        stroke_width=2,
                        color=PURE_RED,
                        dash_length=DEFAULT_DASH_LENGTH * 0.3,
                    )
                )
            )
            arrow_model_out.add_updater(
                lambda x: x.become(
                    Arrow(xdot_.get_top(), xdot_hat.get_center(), buff=0).set_opacity(
                        0.3
                    )
                )
            )
            self.playw(xdot_hat.animate.shift((LEFT + DOWN) * 0.1))
            self.playw(xdot_hat.animate.shift((RIGHT + UP) * 0.5))


class SumUp(DefaultManimClass):
    def construct(self):
        nump = (
            NumberPlane(x_range=(-3, 3, 1.5), y_range=(-3, 3, 1.5))
            .set_opacity(0.3)
            .scale(0.8)
        )
        model = CodeText("Model").set_color_by_gradient(YELLOW, PURE_GREEN)
        model = VGroup(
            SurroundingRect(color=YELLOW_B).surround(
                model, buf_height=0.5, buf_width=0.5
            ),
            model,
        )
        VGroup(nump, model).arrange(RIGHT, buff=0.75)
        xdot = Dot(
            nump.c2p(*true_y0[0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        )
        xdot1 = Dot(
            nump.c2p(*true_y[1, 0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        )
        self.cf.scale(0.6).move_to(VGroup(xdot, model))
        self.playw(FadeIn(nump, xdot, model, xdot1))

        xdot_in = xdot1.copy()
        self.play(LaggedStart(xdot_in.animate.move_to(model).set_opacity(0.0), Wiggle(model), lag_ratio=0.4), run_time=1)
        model_out0 = DashedLine(model.get_left(), nump.c2p(*true_y[2, 0].tolist()), stroke_width=3)
        xdot_out = Dot(
            nump.c2p(*true_y[2, 0].tolist()), radius=DEFAULT_DOT_RADIUS, color=BLUE
        ).set_opacity(0.5)
        self.play(Create(model_out0), run_time=0.5)
        self.playw(FadeIn(xdot_out, scale=2))

        self.playw(FadeOut(xdot_out, model_out0))

        xdot_in = xdot1.copy()
        self.play(LaggedStart(xdot_in.animate.move_to(model).set_opacity(0.0), Wiggle(model), lag_ratio=0.4), run_time=1)
        model_out = Arrow(xdot1, nump.c2p(*true_y[2, 0].tolist()), buff=0, stroke_width=2)
        model_out.save_state()
        model_out.move_to(model).set_opacity(0)
        self.playw(Restore(model_out))
