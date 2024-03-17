from manim import *
from manimdef import DefaultManimClass
from sklearn.datasets import make_moons
import numpy as np

import torch

x = torch.tensor(make_moons(100, noise=0.01)[0], dtype=torch.float)
h = 24
e = torch.nn.Sequential(
    torch.nn.Linear(2, h),
    torch.nn.Tanh(),
    torch.nn.Linear(h, h),
    torch.nn.Tanh(),
    torch.nn.Linear(h, 1),
)
d = torch.nn.Sequential(
    torch.nn.Linear(1, h),
    torch.nn.Tanh(),
    torch.nn.Linear(h, h),
    torch.nn.Tanh(),
    torch.nn.Linear(h, 2),
)
w = torch.nn.Sequential(e, d)
opt = torch.optim.Adam(w.parameters(), 0.01, (0.9, 0.999))
scheduler = torch.optim.lr_scheduler.ExponentialLR(opt, gamma=0.9999, last_epoch=-1)
offflag = True
for i in range(25000):
    opt.zero_grad()
    x_hat = w(x)
    l = torch.nn.functional.l1_loss(x, x_hat)
    l.backward()
    if i % 100 == 0:
        print(f"{l.item():.3f}")
    opt.step()
    if i > 15000:
        if offflag:
            offflag = False
            print("start scheduler")
        scheduler.step()


def to3d(data):
    if data.shape[1] == 2:
        return np.concatenate([data, np.zeros_like(data)[:, :1]], axis=-1)
    elif data.shape[1] == 1:
        return np.concatenate([data, np.zeros_like(data), np.zeros_like(data)], axis=-1)


def criterion_func(x, amp=0.5, freq=3, phase=1.5, bias=0.2):
    return amp * np.sin(freq * x + phase) + bias


def generate_sintex(amp, freq, phase, bias):
    return MathTex(
        "y",
        "=",
        f"{amp} \\times" * (amp != 1),
        "sin",
        "(",
        f"{freq}" * (freq != 1),
        "x",
        f"+ {phase}" * (phase != 0),
        ")",
        f"+ {bias}" * (bias != 0),
        font_size=DEFAULT_FONT_SIZE * 0.7,
        color=GREEN,
    )


class MoonManual(DefaultManimClass):
    def construct(self):
        self.sceneA()
        self.clear()
        self.sceneB()

    def sceneA(self):
        num_dot = 100
        sampled_2d, _ = make_moons(num_dot, noise=0.01)
        sampled = to3d(sampled_2d)

        xys_list = []
        for i in range(20):
            row_list = []
            for j in range(5):
                point_np = sampled_2d[i * 5 + j]
                t = Text(
                    f"<{point_np[0]:.2f}, {point_np[1]:.2f}>",
                    font_size=DEFAULT_FONT_SIZE * 0.25,
                    font="Consolas",
                )
                row_list.append(t)
            row = VGroup(*row_list).arrange(
                RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1
            )
            xys_list.append(row)
            if i:
                row.stretch_to_fit_width(xys_list[0].width)

        xys = VGroup(*xys_list).arrange(
            DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.5
        )
        self.playw(Write(xys), run_time=2)
        self.playw(xys.animate.set_opacity(0.3))
        nump = NumberPlane(
            x_range=[-1.5, 3.0],
            y_range=[-1.0, 1.5],
            color=GREY_D,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3,
            },
        ).scale(2)

        self.playw(FadeIn(nump))
        dots = VGroup(
            *[
                Dot(nump.c2p(*s), color=YELLOW, radius=DEFAULT_DOT_RADIUS * 0.5)
                for s in sampled
            ]
        )
        amp0, freq0, phase0, bias0 = 1, 1, 0, 0
        amp, freq, phase, bias = 0.5, 3, 1.5, 0.2
        target_plot = (
            nump.plot(criterion_func, color=GREY)
            .set_opacity(0.3)
            .set_fill(BLACK, opacity=0.0)
        )
        plot_tex = generate_sintex(amp0, freq0, phase0, bias0).move_to(nump.c2p(3, 1.2))
        self.playw(
            LaggedStart(
                *[Transform(xys[i // 5][i % 5], dots[i]) for i in range(num_dot)]
            )
        )
        upper_curve = nump.plot(
            lambda x: (1 - x**2) ** 0.5, x_range=(-1, 1), color=PURE_RED
        )
        below_curve = nump.plot(
            lambda x: -((1 - (x - 1) ** 2) ** 0.5) + 0.5, x_range=(0, 2), color=PURE_RED
        )
        self.playw(Write(upper_curve))
        self.playw(Write(below_curve))

        encoded_fail = VGroup(
            *[
                Dot(
                    (nump.c2p(*[s[0], 0, 0])),
                    color=YELLOW,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in sampled
            ]
        )
        xys.save_state()
        self.playw(
            LaggedStart(
                *[
                    Transform(xys[i // 5][i % 5], encoded_fail[i])
                    for i in range(num_dot)
                ]
            ),
            FadeOut(upper_curve, below_curve),
            run_time=1.5,
        )
        arrow_up = Arrow(nump.c2p(0.3, 0, 0), nump.c2p(0.3, 0.5, 0), color=GREEN)
        arrow_down = Arrow(nump.c2p(0.6, 0, 0), nump.c2p(0.6, -0.5, 0), color=BLUE)
        self.playw(
            LaggedStart(GrowArrow(arrow_up), GrowArrow(arrow_down), lag_ratio=0.4)
        )
        self.playw(
            arrow_up.animate.set_color(PURE_RED), arrow_down.animate.set_color(PURE_RED)
        )
        self.playw(FadeOut(arrow_up, arrow_down))
        self.playw(Restore(xys))
        xys.save_state()
        encoded_target = VGroup(
            *[
                Dot(
                    (
                        nump.c2p(*[s[0] - 2, 0, 0])
                        if s[1] > criterion_func(s[0])
                        else nump.c2p(*[s[0] + 1, 0, 0])
                    ),
                    color=YELLOW,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in sampled
            ]
        )
        self.playw(
            LaggedStart(
                *[
                    Transform(xys[i // 5][i % 5], encoded_target[i])
                    for i in range(num_dot)
                ]
            ),
            run_time=1.5,
        )
        self.playw(Restore(xys))

        self.playw(FadeIn(target_plot))
        self.playw(FadeOut(target_plot))

        plot = nump.plot(
            lambda x: criterion_func(x, amp0, freq0, phase0, bias0), color=GREEN
        )
        self.playw(FadeIn(plot))
        self.playw(Write(plot_tex))
        new_plot = nump.plot(
            lambda x: criterion_func(x, amp0, freq, phase0, bias0), color=GREEN
        )
        self.playw(
            Transform(plot, new_plot),
            TransformMatchingTex(
                plot_tex,
                plot_tex := generate_sintex(amp0, freq, phase0, bias0).move_to(
                    nump.c2p(3, 1.2)
                ),
            ),
        )
        new_plot = nump.plot(
            lambda x: criterion_func(x, amp, freq, phase0, bias0), color=GREEN
        )
        self.playw(
            Transform(plot, new_plot),
            TransformMatchingTex(
                plot_tex,
                plot_tex := generate_sintex(amp, freq, phase0, bias0).move_to(
                    nump.c2p(3, 1.2)
                ),
            ),
        )
        new_plot = nump.plot(
            lambda x: criterion_func(x, amp, freq, phase0, bias), color=GREEN
        )
        self.playw(
            Transform(plot, new_plot),
            TransformMatchingTex(
                plot_tex,
                plot_tex := generate_sintex(amp, freq, phase0, bias).move_to(
                    nump.c2p(3, 1.2)
                ),
            ),
        )
        new_plot = nump.plot(
            lambda x: criterion_func(x, amp, freq, phase, bias), color=GREEN
        )
        self.playw(
            Transform(plot, new_plot),
            TransformMatchingTex(
                plot_tex,
                plot_tex := generate_sintex(amp, freq, phase, bias).move_to(
                    nump.c2p(3, 1.2)
                ),
            ),
        )
        encoded_x_list = [
            s[0] - 2 if s[1] > criterion_func(s[0]) else s[0] + 1 for s in sampled_2d
        ]
        sample_encoded = VGroup(
            *[
                Dot(
                    (
                        nump.c2p(*[s[0] - 2, 0, 0])
                        if s[1] > criterion_func(s[0])
                        else nump.c2p(*[s[0] + 1, 0, 0])
                    ),
                    color=YELLOW,
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                )
                for s in sampled
            ]
        )
        nump2 = (
            NumberPlane(
                x_range=[-3.3, 3.3],
                y_range=[-1.0, 1.5],
                color=GREY_D,
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 4,
                    "stroke_opacity": 0.1,
                },
            )
            .shift(LEFT * 1.5)
            .scale(2)
        )
        self.wait(5)
        rule_upper = MathTex(
            "[x, y] \\rightarrow [x-2, 0]", font_size=DEFAULT_FONT_SIZE * 0.7
        ).move_to(nump.c2p(-1.3, 1, 0))
        rule_below = MathTex(
            "[x, y] \\rightarrow [x+1, 0]", font_size=DEFAULT_FONT_SIZE * 0.7
        ).move_to(nump.c2p(1, -0.7, 0))
        self.playw(FadeIn(rule_upper))
        self.playw(FadeIn(rule_below))
        self.playw(
            plot.animate.set_opacity(0.3).set_fill(BLACK, opacity=0.0),
            nump.animate.set_x_range((-3, 3)),
            LaggedStart(
                *[
                    Transform(xys[i // 5][i % 5], sample_encoded[i])
                    for i in range(num_dot)
                ]
            ),
            FadeOut(nump),
            FadeIn(nump2),
        )
        self.playw(
            FadeOut(plot_tex),
            plot.animate.set_opacity(0.0),
            self.camera.frame.animate.shift(LEFT * 1.5),
            FadeOut(rule_upper, rule_below),
        )
        self.playw(
            FadeIn(
                upper_curve.set_opacity(0.5).set_fill(BLACK, opacity=0.0),
                below_curve.set_opacity(0.5).set_fill(BLACK, opacity=0.0),
            )
        )
        self.playw(FadeOut(upper_curve, below_curve))

        recon_x = VGroup(
            *[
                Dot(
                    (
                        nump.c2p(x + 2, 1 - (x + 2) ** 2, 0)
                        if x < 0
                        else nump.c2p(x - 1, (x - 1 - 1) ** 2 - 0.5, 0)
                    ),
                    radius=DEFAULT_DOT_RADIUS * 0.5,
                    color=YELLOW,
                )
                for x in encoded_x_list
            ]
        )
        upper_eq = MathTex("y=1-x^2", font_size=DEFAULT_FONT_SIZE * 0.7).move_to(
            nump2.c2p(-1.3, 1, 0)
        )
        below_eq = MathTex(
            "y=(x-1)^2 - 0.5", font_size=DEFAULT_FONT_SIZE * 0.7
        ).move_to(nump2.c2p(1, -0.7, 0))
        self.playw(
            LaggedStart(
                *[Transform(xys[i // 5][i % 5], recon_x[i]) for i in range(num_dot)]
            ),
            FadeIn(upper_eq, below_eq),
        )

    def sceneB(self):
        num_dot = 100
        sampled_2d, _ = make_moons(num_dot, noise=0.01)
        sampled = to3d(sampled_2d)

        sampled_2d_tensor = torch.tensor(sampled_2d, dtype=torch.float)

        h = 24
        e = torch.nn.Sequential(
            torch.nn.Linear(2, h),
            torch.nn.Tanh(),
            torch.nn.Linear(h, h),
            torch.nn.Tanh(),
            torch.nn.Linear(h, 1),
        )
        d = torch.nn.Sequential(
            torch.nn.Linear(1, h),
            torch.nn.Tanh(),
            torch.nn.Linear(h, h),
            torch.nn.Tanh(),
            torch.nn.Linear(h, 2),
        )
        w = torch.nn.Sequential(e, d)

        w.load_state_dict(torch.load("piui.ckpt"))
        encoded_tensor = w[0](sampled_2d_tensor)
        encoded = encoded_tensor.detach().numpy()

        encoded_3d = to3d(encoded)

        nump = NumberPlane(
            x_range=[-1.5, 3.0],
            y_range=[-1.0, 1.5],
            color=GREY_D,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3,
            },
        ).scale(2)

        self.playw(FadeIn(nump))
        dots = VGroup(
            *[
                Dot(nump.c2p(*s), color=YELLOW, radius=DEFAULT_DOT_RADIUS * 0.5)
                for s in sampled
            ]
        )
        encoded_dots = VGroup(
            *[
                Dot(nump.c2p(*s), color=YELLOW, radius=DEFAULT_DOT_RADIUS * 0.5)
                for s in encoded_3d
            ]
        )
        self.playw(FadeIn(dots))
        self.playw(
            LaggedStart(
                *[Transform(dots[i], encoded_dots[i]) for i in range(num_dot)],
                run_time=2.0,
            ),
            self.camera.frame.animate.scale(2.0),
        )
        decoded_tensor = w[1](encoded_tensor)
        decoded = decoded_tensor.detach().numpy()
        decoded_3d = to3d(decoded)
        decoded_dots = VGroup(
            *[
                Dot(nump.c2p(*s), color=YELLOW, radius=DEFAULT_DOT_RADIUS * 0.5)
                for s in decoded_3d
            ]
        )
        self.playw(
            LaggedStart(
                *[Transform(dots[i], decoded_dots[i]) for i in range(num_dot)],
                run_time=2.0,
            ),
            self.camera.frame.animate.scale(0.5),
        )
