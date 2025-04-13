from manim import *
from raenim import *
from random import seed

seed(41)


class intro(Scene2D):
    def construct(self):
        conv1d = Rectangle(width=16, height=9, color=BLUE).scale(0.25)
        conv1dl = (
            Text("conv = nn.Conv1d(...)", font="Noto Mono", font_size=24, color=GREY_C)
            .next_to(conv1d, LEFT, buff=0.1)
            .align_to(conv1d, UP)
        )
        conv1dt = Text("h = conv(x)", font="Noto Mono", font_size=24)

        xidx = -2
        yidx = 0
        conv1d = VGroup(conv1d, conv1dt)
        self.play(FadeIn(conv1d, conv1dl))
        self.playw(Circumscribe(conv1dt[xidx]))

        xline = DashedLine(
            conv1dt[xidx].get_top(), conv1dt[xidx].get_center() + UP * 2, color=GREY_B
        )
        self.play(Create(xline))

        shape_in = (
            Text("[B, C, L]", font="Noto Mono", font_size=24)
            .next_to(xline, UP, buff=0.05)
            .set_color_by_gradient(GREEN, TEAL)
            .shift(RIGHT * 0.1)
        )
        self.playw(FadeIn(shape_in))
        xline_out = DashedLine(
            conv1dt[yidx].get_bottom(),
            conv1dt[yidx].get_center() + DOWN * 2,
            color=GREY_B,
        )
        shape_out = (
            Text("[B, C', L]", font="Noto Mono", font_size=24)
            .next_to(xline_out, DOWN, buff=0.05)
            .set_color_by_gradient(GREEN, TEAL)
            .shift(LEFT * 0.2)
        )

        self.play(Circumscribe(shape_in[3]))
        self.playw(LaggedStart(Create(xline_out), FadeIn(shape_out), lag_ratio=0.7))

        nnLinear = Rectangle(width=16, height=9, color=BLUE).scale(0.25).shift(DOWN * 5)
        nnLinearl = (
            Text(
                "linear = nn.Linear(...)", font="Noto Mono", font_size=24, color=GREY_C
            )
            .next_to(nnLinear, LEFT, buff=0.1)
            .align_to(nnLinear, UP)
        )
        nnLineart = Text("y = linear(h)", font="Noto Mono", font_size=24).move_to(
            nnLinear
        )

        self.playw(
            LaggedStart(
                self.cf.animate.scale(1.5).move_to(VGroup(nnLinear, conv1d)),
                FadeIn(nnLinear, nnLineart, nnLinearl),
            )
        )
        xlinel = DashedLine(
            nnLineart[xidx].get_top(),
            nnLineart[xidx].get_center() + UP * 2,
            color=GREY_B,
        )

        self.wait(2)
        shape_inl = (
            Text("[B, L, C']", font="Noto Mono", font_size=24)
            .next_to(xlinel, UP, buff=0.05)
            .set_color_by_gradient(GREEN, TEAL)
            .shift(RIGHT * 0.1)
        )
        self.playw(LaggedStart(Create(xlinel), FadeIn(shape_inl), lag_ratio=0.7))

        transposet = (
            Text("h = h.tranpose(1, 2)", font="Noto Mono", font_size=24)
            .next_to(shape_out, RIGHT, buff=1)
            .set_color_by_gradient(ORANGE, RED)
        )
        line_tpin = DashedLine(
            shape_out.get_right(), transposet.get_left(), color=GREY_B
        )
        line_tpout = DashedLine(transposet.get_bottom(), shape_inl.get_top(), color=GREY_B)
        self.playw(LaggedStart(Create(line_tpin), FadeIn(transposet), Create(line_tpout), lag_ratio=0.7))