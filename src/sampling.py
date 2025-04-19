from manim import *
from manimdef import DefaultManimClass
from random import uniform
from math import sin


def arbitrary_func(x):
    return 0.5 - 0.1 * x + 0.3 * sin(x * 3)


class SamplingOne(DefaultManimClass):
    def scene1(self):
        u01 = MathTex("u(0, 1)")
        grid = Axes(
            x_range=[0, 1.3, 0.2],  # step size determines num_decimal_places.
            y_range=[0, 1.3, 0.2],
            x_length=6,
            y_length=3.0,
            axis_config={
                "numbers_to_include": [0.4, 0.8, 1],
                "font_size": 24,
            },
            tips=False,
        ).next_to(u01, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
        grid += Line(grid.c2p(0, 1), grid.c2p(1, 1), color=BLUE)
        grid += Line(grid.c2p(1, 0), grid.c2p(1.3, 0), color=BLUE)
        grid += grid.get_vertical_line(grid.c2p(1, 1))
        self.playw(FadeIn(u01))
        self.playw(self.camera.frame.animate.move_to(VGroup(u01, grid)), FadeIn(grid))

        x_float = uniform(0, 1)
        prob = self.get_dx_prob(grid, x_float)
        self.playw(FadeIn(prob))
        x = MathTex("x =", f"{x_float:.2f}", color=YELLOW).next_to(grid, DOWN)
        x_in = AnimationGroup(
            Transform(prob, x[-1]), FadeIn(x[0], target_position=prob)
        )
        self.playw(
            LaggedStart(x_in, self.camera.frame.animate.move_to(x), lag_ratio=0.3)
        )
        self.playw(Write(u01.copy().set_color("#00FF00")))
        self.clear()
        self.camera.frame.move_to(ORIGIN)

    def scene2(self):
        grid = Axes(
            x_range=[0, 3.3, 0.5],  # step size determines num_decimal_places.
            y_range=[0, 1.3, 0.5],
            x_length=6,
            y_length=3.0,
            axis_config={
                "numbers_to_include": [3.0],
                "font_size": 24,
            },
            tips=False,
        )
        plot = grid.plot(arbitrary_func, [0.0, 3.0], color=GREEN)
        self.playw(FadeIn(grid))
        self.playw(
            LaggedStart(
                Write(plot),
                FadeIn(
                    MathTex("y = p(x)", font_size=36, color=GREEN).move_to(
                        grid.c2p(3, 0.7)
                    )
                ),
                Write(
                    grid.get_vertical_line(grid.c2p(3, arbitrary_func(3)), color=GREEN)
                ),
                lag_ratio=0.3,
            )
        )

        x_float = uniform(0, 3)
        prob = self.get_dx_prob(grid, x_float, func=arbitrary_func)
        self.playw(FadeIn(prob))
        x = MathTex("x =", f"{x_float:.2f}", color=YELLOW).next_to(grid, DOWN)
        x_in = AnimationGroup(
            Transform(prob, x[-1]), FadeIn(x[0], target_position=prob)
        )
        self.playw(
            LaggedStart(x_in, self.camera.frame.animate.move_to(x), lag_ratio=0.3)
        )

    def scene3(self):
        u101 = MathTex("u_1(0, 1)", color=RED)
        u201 = MathTex("u_2(0, 1)", color=GREEN)
        u301 = MathTex("u_3(0, 1)", color=BLUE)
        us = (
            VGroup(u101, u201, u301)
            .arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 4)
            .move_to(ORIGIN)
        )
        grid = Axes(
            x_range=[0, 1.3, 0.5],  # step size determines num_decimal_places.
            y_range=[0, 1.3, 0.5],
            x_length=6,
            y_length=3.0,
            axis_config={
                "numbers_to_include": [0.5, 1],
                "font_size": 24,
            },
            tips=False,
        ).next_to(us, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
        grid += Line(grid.c2p(0, 1), grid.c2p(1, 1), color=YELLOW)
        grid += Line(grid.c2p(1, 0), grid.c2p(1.3, 0), color=YELLOW)
        grid += grid.get_vertical_line(grid.c2p(1, 1))
        self.playw(Write(us))
        self.playw(FadeIn(grid), self.camera.frame.animate.move_to(grid))

        x1_float, x2_float, x3_float = [uniform(0, 1) for _ in range(3)]
        prob1 = self.get_dx_prob(grid, x1_float, color=RED)
        prob2 = self.get_dx_prob(grid, x2_float, color=GREEN)
        prob3 = self.get_dx_prob(grid, x3_float, color=BLUE)
        self.playw(
            LaggedStart(FadeIn(prob1), FadeIn(prob2), FadeIn(prob3), lag_ratio=0.2)
        )
        x1 = MathTex("x_1 =", f"{x1_float:.2f}", color=RED)
        x2 = MathTex("x_2 =", f"{x2_float:.2f}", color=GREEN)
        x3 = MathTex("x_3 =", f"{x3_float:.2f}", color=BLUE)
        xs = (
            VGroup(x1, x2, x3)
            .arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 4)
            .next_to(grid, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
        )

        x1_in = AnimationGroup(
            Transform(prob1, x1[-1]), FadeIn(x1[0], target_position=prob1)
        )
        x2_in = AnimationGroup(
            Transform(prob2, x2[-1]), FadeIn(x2[0], target_position=prob2)
        )
        x3_in = AnimationGroup(
            Transform(prob3, x3[-1]), FadeIn(x3[0], target_position=prob3)
        )
        self.playw(
            x1_in, x2_in, x3_in, self.camera.frame.animate.move_to(VGroup(grid, xs))
        )

        self.playw(
            FadeOut(grid, u101, u201, u301),
            (
                rgb := VGroup(
                    MathTex("[").next_to(prob1, LEFT).set_opacity(0.0),
                    prob1[-4:],
                    prob2[-4:],
                    prob3[-4:],
                    MathTex("]").next_to(prob3, RIGHT).set_opacity(0.0),
                )
            )
            .animate.arrange(RIGHT)
            .move_to(grid)
            .set_opacity(1.0),
        )

        def n2h(x):
            return hex(int(x * 255))[2:].zfill(2).upper()

        square = (
            Square(side_length=1)
            .set_fill(
                color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}", opacity=1.0
            )
            .set_stroke(color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}")
            .move_to(rgb)
        )
        self.playw(
            rgb.copy().animate.next_to(square, UP),
            Transform(
                rgb,
                square,
            ),
            FadeOut(x1[0], x2[0], x3[0]),
        )
        self.clear()

    def scene4(self):
        image = []
        num_length = 24
        for i in range(num_length):
            row = []
            for j in range(num_length):
                ur01 = MathTex("u_r(0, 1)", color=RED)
                ug01 = MathTex("u_g(0, 1)", color=GREEN)
                ub01 = MathTex("u_b(0, 1)", color=BLUE)
                us = (
                    VGroup(ur01, ug01, ub01)
                    .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.0879)
                    .move_to(ORIGIN)
                )
                row.append(us)
            row = VGroup(*row).arrange(RIGHT)
            image.append(row)
        square_width = us.width
        image = VGroup(*image).arrange(DOWN)
        self.camera.frame.move_to(image[0][0])
        image_remainder = VGroup(image[0][1:], image[1:])

        self.playw(FadeIn(image[0][0]))
        self.play(FadeIn(image_remainder))
        original_frame_height = self.camera.frame_height
        self.playw(
            self.camera.frame.animate.scale(
                image.height * 1.3 / self.camera.frame_height
            ).move_to(ORIGIN)
        )
        self.camera.frame.save_state()
        self.playw(
            self.camera.frame.animate.scale(
                original_frame_height / image.height
            ).move_to(image[0][0])
        )
        tas, nums = [], []

        floats = []
        for i in range(num_length):
            row = []
            for j in range(num_length):
                num_floats = [uniform(0.0, 1.0) for _ in range(3)]
                nums.append(num_floats)
                xs = [
                    MathTex(
                        f"x_{i+1} =",
                        f"{num_floats[i]:.2f}",
                        color=c,
                        font_size=int(DEFAULT_FONT_SIZE * 0.8),
                    )
                    for i, c in zip(range(3), [RED, GREEN, BLUE])
                ]
                xs = (
                    VGroup(*xs)
                    .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.3)
                    .move_to(image[i][j])
                )
                row.append(xs)
                ta = Transform(image[i][j], xs)
                tas.append(ta)
            # row = VGroup(*row).arrange(RIGHT)
            floats.append(row)
        # floats = VGroup(*floats).arrange(DOWN).move_to(ORIGIN)
        self.playw(LaggedStart(*tas, lag_ratio=0.05), run_time=1.5)

        def n2h(x):
            return hex(int(x * 255))[2:].zfill(2).upper()

        def new_sampling(new_num=True):
            sqts, squares = [], []
            for i in range(num_length):
                row = []
                for j in range(num_length):
                    if new_num:
                        num_floats = [uniform(0.0, 1.0) for _ in range(3)]
                    else:
                        num_floats = nums[i * num_length + j]
                    x1_float, x2_float, x3_float = num_floats
                    square = (
                        Square(side_length=square_width)
                        .set_fill(
                            color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}",
                            opacity=1.0,
                        )
                        .set_stroke(
                            color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}"
                        )
                    )
                    row.append(square)
                    sqts.append(Transform(image[i][j], square))
                row = VGroup(*row).arrange(RIGHT)
                squares.append(row)
            squares = VGroup(*squares).arrange(DOWN).move_to(ORIGIN)
            if new_num:
                self.playw(*sqts, run_time=1.0)
            else:
                self.playw(LaggedStart(*sqts, lag_ratio=0.05), run_time=1.5)

        new_sampling(new_num=False)
        self.playw(Restore(self.camera.frame))
        new_sampling()
        new_sampling()
        new_sampling()
        new_sampling()
        new_sampling()
        self.clear()

    def scene5(self):
        image = []
        num_length = 24
        for i in range(num_length):
            row = []
            for j in range(num_length):
                ur01 = MathTex("u_r(0, 1)", color=RED)
                ug01 = MathTex("u_g(0, 1)", color=GREEN)
                ub01 = MathTex("u_b(0.9, 1)", color=BLUE)
                us = (
                    VGroup(ur01, ug01, ub01)
                    .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
                    .move_to(ORIGIN)
                )
                row.append(us)
            row = VGroup(*row).arrange(RIGHT)
            image.append(row)
        square_width = us.width
        image = VGroup(*image).arrange(DOWN)
        self.camera.frame.move_to(image[0][0])
        image_remainder = VGroup(image[0][1:], image[1:])
        self.playw(FadeIn(image[0][0]))
        self.play(Write(highlight := image[0][0][2].copy().set_color("#0000FF")))
        self.play(FadeOut(highlight))
        self.playw(FadeIn(image_remainder), run_time=1.0)
        original_frame_height = self.camera.frame_height
        self.playw(
            self.camera.frame.animate.scale(
                image.height * 1.3 / self.camera.frame_height
            ).move_to(ORIGIN)
        )
        self.camera.frame.save_state()
        self.playw(
            self.camera.frame.animate.scale(
                original_frame_height / image.height
            ).move_to(image[0][0])
        )
        tas, nums = [], []

        floats = []
        for i in range(num_length):
            row = []
            for j in range(num_length):
                num_floats = [uniform(0.0 if ci != 2 else 0.9, 1.0) for ci in range(3)]
                nums.append(num_floats)
                xs = [
                    MathTex(
                        f"x_{i+1} =",
                        f"{num_floats[i]:.2f}",
                        color=c,
                        font_size=int(DEFAULT_FONT_SIZE * 0.8),
                    )
                    for i, c in zip(range(3), [RED, GREEN, BLUE])
                ]
                xs = (
                    VGroup(*xs)
                    .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.3)
                    .move_to(image[i][j])
                )
                row.append(xs)
                ta = Transform(image[i][j], xs)
                tas.append(ta)
            # row = VGroup(*row).arrange(RIGHT)
            floats.append(row)
        # floats = VGroup(*floats).arrange(DOWN).move_to(ORIGIN)
        self.playw(LaggedStart(*tas, lag_ratio=0.05), run_time=1.5)

        def n2h(x):
            return hex(int(x * 255))[2:].zfill(2).upper()

        def new_sampling(new_num=True):
            sqts, squares = [], []
            for i in range(num_length):
                row = []
                for j in range(num_length):
                    if new_num:
                        num_floats = [
                            uniform(0.0 if ci != 2 else 0.9, 1.0) for ci in range(3)
                        ]
                    else:
                        num_floats = nums[i * num_length + j]
                    x1_float, x2_float, x3_float = num_floats
                    square = (
                        Square(side_length=square_width)
                        .set_fill(
                            color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}",
                            opacity=1.0,
                        )
                        .set_stroke(
                            color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}"
                        )
                    )
                    row.append(square)
                    sqts.append(Transform(image[i][j], square))
                row = VGroup(*row).arrange(RIGHT)
                squares.append(row)
            squares = VGroup(*squares).arrange(DOWN).move_to(ORIGIN)
            if new_num:
                self.playw(*sqts, run_time=1.0)
            else:
                self.playw(LaggedStart(*sqts, lag_ratio=0.05), run_time=1.5)

        new_sampling(new_num=False)
        self.playw(Restore(self.camera.frame))
        new_sampling()
        new_sampling()
        new_sampling()
        self.clear()

    def scene6(self):
        image = []
        num_length = 24
        for i in range(num_length):
            row = []
            for j in range(num_length):
                randrange = "0.5, 1" if i < num_length // 2 else "0, 0.5"
                ur01 = MathTex(f"u_r({randrange})", color=RED)
                ug01 = MathTex(f"u_g({randrange})", color=GREEN)
                ub01 = MathTex(f"u_b({randrange})", color=BLUE)
                us = (
                    VGroup(ur01, ug01, ub01)
                    .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.8)
                    .move_to(ORIGIN)
                )
                row.append(us)
            row = VGroup(*row).arrange(RIGHT)
            image.append(row)
        square_width = us.width
        image = VGroup(*image).arrange(DOWN)
        self.camera.frame.move_to(image[0][0])
        image_remainder = VGroup(image[0][1:], image[1:])
        self.playw(FadeIn(image[0][0]))
        self.play(Write(highlight := image[0][0][2].copy().set_color("#0000FF")))
        self.play(FadeOut(highlight))
        self.playw(FadeIn(image_remainder), run_time=1.0)
        original_frame_height = self.camera.frame_height
        self.playw(
            self.camera.frame.animate.scale(
                image.height * 1.3 / self.camera.frame_height
            ).move_to(ORIGIN)
        )
        self.camera.frame.save_state()
        self.playw(
            self.camera.frame.animate.scale(
                original_frame_height / image.height
            ).move_to(image[0][0])
        )
        tas, nums = [], []

        floats = []
        for i in range(num_length):
            row = []
            for j in range(num_length):
                num_floats = [
                    uniform(0.5, 1) if i < num_length // 2 else uniform(0, 0.5)
                    for ci in range(3)
                ]
                nums.append(num_floats)
                xs = [
                    MathTex(
                        f"x_{i+1} =",
                        f"{num_floats[i]:.2f}",
                        color=c,
                        font_size=int(DEFAULT_FONT_SIZE * 0.8),
                    )
                    for i, c in zip(range(3), [RED, GREEN, BLUE])
                ]
                xs = (
                    VGroup(*xs)
                    .arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.3)
                    .move_to(image[i][j])
                )
                row.append(xs)
                ta = Transform(image[i][j], xs)
                tas.append(ta)
            # row = VGroup(*row).arrange(RIGHT)
            floats.append(row)
        # floats = VGroup(*floats).arrange(DOWN).move_to(ORIGIN)
        self.playw(LaggedStart(*tas, lag_ratio=0.05), run_time=1.5)

        def n2h(x):
            return hex(int(x * 255))[2:].zfill(2).upper()

        def new_sampling(new_num=True):
            sqts, squares = [], []
            for i in range(num_length):
                row = []
                for j in range(num_length):
                    if new_num:
                        num_floats = [
                            uniform(0.5, 1) if i < num_length // 2 else uniform(0, 0.5)
                            for ci in range(3)
                        ]
                    else:
                        num_floats = nums[i * num_length + j]
                    x1_float, x2_float, x3_float = num_floats
                    square = (
                        Square(side_length=square_width)
                        .set_fill(
                            color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}",
                            opacity=1.0,
                        )
                        .set_stroke(
                            color=f"#{n2h(x1_float)}{n2h(x2_float)}{n2h(x3_float)}"
                        )
                    )
                    row.append(square)
                    sqts.append(Transform(image[i][j], square))
                row = VGroup(*row).arrange(RIGHT)
                squares.append(row)
            squares = VGroup(*squares).arrange(DOWN).move_to(ORIGIN)
            if new_num:
                self.playw(*sqts, run_time=1.0)
            else:
                self.playw(LaggedStart(*sqts, lag_ratio=0.05), run_time=1.5)

        new_sampling(new_num=False)
        self.playw(Restore(self.camera.frame))
        new_sampling()
        new_sampling()
        new_sampling()
        self.clear()

    def scene7(self):
        pass

    def construct(self):
        # self.scene1()  # ~ 이 확률 분포, u(0, 1)에서 비롯된 겁니다
        # self.scene2()  # ~ 정확히 가능하다고 가정하고 설명하겠습니다
        # self.clear()
        # self.camera.frame.move_to(ORIGIN)
        # self.scene3()  # ~ 아무 색깔이나 하나 적당히 나올 겁니다
        self.scene4()  # ~ 정말 무작위한 노이즈 그림만 나올 뿐입니다
        # self.scene5()  # ~ 파란색 성분이 강조된 그런 그림을 얻을 수 있습니다
        # self.scene6()  # ~ 아래쪽은 좀 더 어두운 그런 특성을 갖는 그림이 샘플링됩니다 #TODO: 카메라를 어두운쪽에도 보내는거 필요
        # self.scene7()

    def get_dx_prob(self, grid: Axes, x, dx=0.02, func=lambda x: 1, color=YELLOW):
        fill = (
            Polygon(
                grid.c2p(x - dx / 2, func(x)),
                grid.c2p(x - dx / 2, 0),
                grid.c2p(x + dx / 2, 0),
                grid.c2p(x + dx / 2, func(x)),
            )
            .set_fill(color, opacity=1.0)
            .set_stroke(color=color)
        )
        return fill
