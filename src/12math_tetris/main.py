from manim import *
from raenim import *
from random import seed, choice

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        grid10x10 = VGroup(
            *[
                DashedVMobject(
                    Square(side_length=0.5, stroke_color=GREY_C, stroke_width=2)
                )
                for _ in range(100)
            ]
        ).arrange_in_grid(rows=10, cols=10, buff=0)
        border = SurroundingRectangle(
            grid10x10, buff=0, stroke_width=3, stroke_color=WHITE
        ).set_z_index(1)

        self.addw(grid10x10, border)

        hor10 = VGroup(
            *[
                Text(
                    str(i),
                    font=MONO_FONT,
                    font_size=20,
                    color=GREY_A,
                )
                .move_to(
                    grid10x10[i - 1].get_center(),
                )
                .set_opacity(0)
                for i in range(1, 11)
            ]
        )
        anims = [
            AnimationGroup(hor10[i].animate.set_opacity(1), rate_func=there_and_back)
            for i in range(len(hor10))
        ]
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=2)
        hor10.set_opacity(0)
        ver10 = VGroup(
            *[
                Text(
                    str(i),
                    font=MONO_FONT,
                    font_size=20,
                    color=GREY_A,
                )
                .move_to(grid10x10[(i - 1) * 10].get_center())
                .set_opacity(0)
                for i in range(1, 11)
            ]
        )
        anims = [
            AnimationGroup(ver10[i].animate.set_opacity(1), rate_func=there_and_back)
            for i in range(len(ver10))
        ]
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=2)
        ver10.set_opacity(0)
        self.wait()

        def get_bar(row, col, vertical=True):
            w, h = (0.5, 2) if vertical else (2, 0.5)
            color = choice([BLUE, GREEN, YELLOW_B, ORANGE, RED, PURPLE])
            bar = Rectangle(
                width=w,
                height=h,
                fill_color=color,
                fill_opacity=1,
                stroke_color=interpolate_color(color, BLACK, 0.5),
                stroke_width=3,
            )
            bar.align_to(grid10x10[row * 10 + col], UL)
            return bar

        def move_bar(bar, row, col, rotate=False, wait=0.05):
            if rotate:
                bar.rotate(-PI / 2)
            bar.align_to(grid10x10[row * 10 + col], UL)
            self.addw(bar, wait=wait)

        b0 = get_bar(0, 4, vertical=True)
        self.playw(FadeIn(b0), wait=0.5)
        for i in range(1, 3):
            move_bar(b0, i, 4, wait=0.5)
        move_bar(b0, 3, 3, wait=0.2)
        move_bar(b0, 3, 2, wait=0.3)
        move_bar(b0, 4, 2, wait=0.5)
        move_bar(b0, 5, 2, wait=0.5)
        move_bar(b0, 6, 2, wait=0.5)

        b1 = get_bar(0, 4)
        self.playw(FadeIn(b1), run_time=0.5, wait=0.1)
        move_bar(b1, 1, 4)
        move_bar(b1, 2, 4)
        move_bar(b1, 2, 3, wait=0.02)
        move_bar(b1, 2, 2, wait=0.03)
        move_bar(b1, 3, 1)
        move_bar(b1, 4, 1)
        move_bar(b1, 5, 1)
        move_bar(b1, 6, 1)

        bs = VGroup(b0, b1, *[get_bar(6, i) for i in [0, 3, 5, 6, 7, 8, 9]])
        ms = VGroup(*[get_bar(2, i) for i in [0, 1, 2, 3, 5, 6, 7, 8, 9]])
        ts = VGroup(
            *[
                get_bar(r, c, vertical=False)
                for r, c in [(0, 0), (1, 0), (0, 6), (1, 6)]
            ]
        )
        self.playwl(*[FadeIn(item) for item in [*bs[2:], *ms, *ts]])

        last_two = VGroup(get_bar(2, 4), get_bar(6, 4)).set_opacity(0.5)
        self.playwl(FadeIn(last_two))


class solution(Scene2D):
    def construct(self):
        grid10x10 = (
            VGroup(
                *[
                    DashedVMobject(
                        Square(side_length=0.5, stroke_color=GREY_C, stroke_width=2)
                    )
                    for _ in range(100)
                ]
            )
            .arrange_in_grid(rows=10, cols=10, buff=0)
            .set_z_index(-2)
        )
        grid10x10_ = (
            VGroup(
                *[
                    Square(side_length=0.5, stroke_color=GREY_E, stroke_width=1)
                    for _ in range(100)
                ]
            )
            .arrange_in_grid(rows=10, cols=10, buff=0)
            .set_z_index(-1)
        )
        border = SurroundingRectangle(
            grid10x10, buff=0, stroke_width=3, stroke_color=WHITE
        )

        def pos(i, j):
            return grid10x10_[i * 10 + j]

        color_patterns = [
            [RED_D, ORANGE, YELLOW, GREEN],
            [GREEN, RED_D, ORANGE, YELLOW],
            [YELLOW, GREEN, RED_D, ORANGE],
            [ORANGE, YELLOW, GREEN, RED_D],
        ]

        def color_gen(i):
            pattern = color_patterns[i]
            while True:
                for color in pattern:
                    yield color

        anims = []
        squares_dict = {
            RED_D: VGroup(),
            ORANGE: VGroup(),
            YELLOW: VGroup(),
            GREEN: VGroup(),
        }
        for i in range(10):
            gen = color_gen(i % 4)
            for j in range(10):
                color = next(gen)
                pos(i, j).set_fill(color, opacity=1)
                squares_dict[color].add(pos(i, j))
                anims.append(FadeIn(pos(i, j)))
        self.addw(grid10x10, border)
        self.playw(LaggedStart(*anims), run_time=2)

        def bar(row, col, vertical=True):
            w, h = (0.5, 2) if vertical else (2, 0.5)
            color = choice([BLUE, TEAL, MINT, DARK_BROWN, PURPLE])
            bar = Rectangle(
                width=w,
                height=h,
                fill_color=color,
                fill_opacity=1,
                stroke_color=interpolate_color(color, BLACK, 0.5),
                stroke_width=4,
            )
            bar.align_to(grid10x10[row * 10 + col], UL)
            return bar

        b0 = bar(2, 4, vertical=True).set_z_index(1)
        self.playw(FadeIn(b0))

        self.play(b0.animate.align_to(grid10x10[56], UL))
        self.playw(
            Rotating(b0, radians=PI / 2, about_point=b0.get_corner(UL)),
            run_time=1,
            rate_func=smooth,
        )

        bars = VGroup(
            b0, *[bar(4, 6, vertical=False).set_z_index(0) for _ in range(24)]
        )
        bars.generate_target()
        b5 = bars.target[:5].arrange(DOWN, buff=0.1)
        b10 = bars.target[5:10].arrange(DOWN, buff=0.1)
        b15 = bars.target[10:15].arrange(DOWN, buff=0.1)
        b20 = bars.target[15:20].arrange(DOWN, buff=0.1)
        b25 = bars.target[20:].arrange(DOWN, buff=0.1)
        VGroup(b5, b10).arrange(DOWN, buff=0.5).next_to(grid10x10, LEFT, buff=1)
        VGroup(b15, b20, b25).arrange(DOWN, buff=0.5).next_to(grid10x10, RIGHT, buff=1)
        self.playwl(
            MoveToTarget(bars),
            self.cf.animate.scale(1.6).shift(DOWN),
            run_time=1.5,
            lag_ratio=0.1,
        )

        bars.shuffle()
        bars.generate_target()
        for i, b in enumerate(bars.target):
            if i % 2 == 0:
                b.rotate(PI / 2)
            b.align_to(grid10x10_[i * 4], UL).set_opacity(0)
        self.playw(MoveToTarget(bars), run_time=2)

        self.play(
            self.cf.animate.shift(UP * 0.5 + RIGHT * 4.5).scale(1 / 1.6).scale(1.2)
        )

        s1 = Words(
            "가정: 25개의 일자로 100칸을 커버할 수 있다.",
            font_size=32,
            font="Noto Sans KR",
        )
        s1.words[0].set_color(YELLOW)
        s2 = Words(
            "놓여진 일자는 네 칸의 색이 모두 다르다.", font_size=32, font="Noto Sans KR"
        )
        s3 = Words(
            "일자가 25개 놓이면 네 색은 각각 25개씩 있다.",
            font_size=32,
            font="Noto Sans KR",
        )
        s4 = Words(
            "하지만 빨간색은 26개, 노란색이 24개이다. 모순 발생",
            font_size=32,
            font="Noto Sans KR",
        )
        s4.words[-2:].set_color(RED)
        ss = VGroup(
            Words("... 모순", font_size=32, font="Noto Sans KR"),
            Words(
                "따라서 25개의 일자로 100칸을 커버할 수 없다.",
                font_size=32,
                font="Noto Sans KR",
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sg = (
            VGroup(s1, s2, s3, s4)
            .arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            .next_to(grid10x10, RIGHT, buff=0.5)
            .align_to(grid10x10, UP)
        )
        ss[0].words[-1].set_color(RED)
        ss[1].words[-1].set_color(RED)
        ss.next_to(s1, DOWN, buff=0.5).align_to(s1, LEFT)
        self.playwl(*[FadeIn(item) for item in s1.words], lag_ratio=0.1)
        self.playw(FadeIn(ss[0]))
        self.playw(
            Transform(
                s1.words.copy(), ss[1].words, replace_mobject_with_target_in_scene=True
            )
        )
        self.playw(FadeOut(ss))

        self.playwl(*[FadeIn(item) for item in s2.words], lag_ratio=0.1)
        b1 = bar(0, 0, vertical=False).set_fill(opacity=0.1).set_stroke(color=PURE_BLUE)
        self.playw(FadeIn(b1))
        for i in range(6):
            self.play(
                b1.animate.align_to(pos(0, i + 1), UL),
                Transform(
                    (temp := grid10x10_[i].copy()),
                    grid10x10_[i + 4].copy(),
                    path_arc=PI / 1.4,
                ),
            )
            self.remove(temp)
            if i == 0:
                self.wait()
        b2 = bar(0, 0, vertical=True).set_fill(opacity=0.1).set_stroke(color=PURE_BLUE)
        self.play(FadeOut(b1), FadeIn(b2))
        for i in range(6):
            self.play(
                b2.animate.align_to(pos(i + 1, 0), UL),
                Transform(
                    (temp := grid10x10_[i * 10].copy()),
                    grid10x10_[i * 10 + 40].copy(),
                    path_arc=PI / 1.4,
                ),
            )
            self.remove(temp)
        self.wait()

        self.playwl(*[FadeIn(item) for item in s3.words], lag_ratio=0.1)

        color_dict = {
            RED_D: VGroup(),
            ORANGE: VGroup(),
            YELLOW: VGroup(),
            GREEN: VGroup(),
        }

        def color_bar(row, col, i, vertical=True):
            cp = color_patterns[i]

            bar = VGroup(*[Square(side_length=0.5) for _ in range(4)]).arrange(
                DOWN if vertical else RIGHT, buff=0
            )
            for j in range(4):
                bar[j].set_fill(cp[j], opacity=1).set_stroke(
                    interpolate_color(cp[j], BLACK, 0.5), width=2
                )
                color_dict[cp[j]].add(bar[j])
            bar.align_to(grid10x10_[row * 10 + col], UL)
            return bar

        cbs = VGroup(*[color_bar(0, 0, i % 4, vertical=True) for i in range(25)])
        for i, cb in enumerate(cbs):
            if i % 2 == 0:
                cb.rotate(PI / 2)
        cbs.shuffle()
        for i, cb in enumerate(cbs):
            cb.align_to(grid10x10_[(i // 5) * 2 * 7 + (i % 5) * 2], UL).set_opacity(0)
        cbs.generate_target()
        for cbt in cbs.target:
            if cbt.get_width() > cbt.get_height():
                cbt.rotate(PI / 2)
        cbs.target.arrange(RIGHT, buff=0.1).scale(0.5).next_to(
            s3, DOWN, buff=1.5
        ).set_opacity(1)
        self.playw(MoveToTarget(cbs), FadeOut(b2), run_time=2)

        color_dict[RED_D] = VGroup(
            *sorted([color_dict[RED_D][i] for i in range(25)], key=lambda m: m.get_x())
        )
        self.playw(
            color_dict[RED_D]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(s3, DOWN, buff=0.3),
        )
        color_dict[ORANGE] = VGroup(
            *sorted([color_dict[ORANGE][i] for i in range(25)], key=lambda m: m.get_x())
        )
        self.play(
            color_dict[ORANGE]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(color_dict[RED_D], DOWN, buff=0.1),
        )
        color_dict[YELLOW] = VGroup(
            *sorted([color_dict[YELLOW][i] for i in range(25)], key=lambda m: m.get_x())
        )
        self.play(
            color_dict[YELLOW]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(color_dict[ORANGE], DOWN, buff=0.1),
        )
        color_dict[GREEN] = VGroup(
            *sorted([color_dict[GREEN][i] for i in range(25)], key=lambda m: m.get_x())
        )
        self.playw(
            color_dict[GREEN]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(color_dict[YELLOW], DOWN, buff=0.1),
        )

        self.playw(
            squares_dict[RED_D]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.5)
            .next_to(color_dict[GREEN], DOWN, buff=0.3)
            .align_to(color_dict[GREEN], LEFT),
        )
        self.play(
            squares_dict[ORANGE]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.5)
            .next_to(squares_dict[RED_D], DOWN, buff=0.1)
            .align_to(squares_dict[RED_D], LEFT),
        )
        self.playw(
            squares_dict[YELLOW]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.5)
            .next_to(squares_dict[ORANGE], DOWN, buff=0.1)
            .align_to(squares_dict[ORANGE], LEFT),
        )
        self.playw(
            squares_dict[GREEN]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.5)
            .next_to(squares_dict[YELLOW], DOWN, buff=0.1)
            .align_to(squares_dict[YELLOW], LEFT),
        )
        s4.next_to(squares_dict[GREEN], DOWN, buff=0.5).align_to(s3, LEFT)
        self.playw(
            self.cf.animate.shift(DOWN),
            AnimationGroup(*[FadeIn(item) for item in s4.words], lag_ratio=0.2),
        )

        s5 = Words(
            "따라서 25개의 일자로 100칸을 커버할 수 없다.",
            font_size=32,
            font="Noto Sans KR",
        )
        s5.words[-1].set_color(RED)
        s5.move_to(s1).align_to(s1, LEFT)
        self.playwl(
            AnimationGroup(
                FadeOut(s2, s3, s4, cbs, *squares_dict.values()), lag_ratio=0.2
            ),
            self.cf.animate.shift(UP),
            *[Transform(s1.words[i], s5.words[i]) for i in range(len(s5.words))],
            lag_ratio=0.5,
            wait=0.1,
        )
        self.playw(self.cf.animate.move_to(s1), FadeOut(border, grid10x10))


class solution2(Scene2D):
    def construct(self):
        grid10x10 = (
            VGroup(
                *[
                    DashedVMobject(
                        Square(side_length=0.5, stroke_color=GREY_C, stroke_width=2)
                    )
                    for _ in range(100)
                ]
            )
            .arrange_in_grid(rows=10, cols=10, buff=0)
            .set_z_index(-2)
        )
        grid10x10_ = (
            VGroup(
                *[
                    Square(
                        side_length=0.5, stroke_color=GREY_E, stroke_width=1
                    ).set_opacity(0)
                    for _ in range(100)
                ]
            )
            .arrange_in_grid(rows=10, cols=10, buff=0)
            .set_z_index(-1)
        )
        border = SurroundingRectangle(
            grid10x10, buff=0, stroke_width=3, stroke_color=WHITE
        ).set_z_index(1)
        board = VGroup(grid10x10, grid10x10_, border)

        self.addw(grid10x10, border)
        self.play(board.animate.shift(LEFT * 4).scale(0.8))
        s1 = (
            Words(
                "가정: 25개의 일자로 100칸을 커버할 수 있다.",
                font_size=24,
                font="Noto Sans KR",
            )
            .next_to(grid10x10, RIGHT, buff=0.5)
            .shift(UP * 1.5)
        )
        s1.words[0].set_color(YELLOW)
        s1.words[-1].set_color(GREEN)
        self.playwl(*[FadeIn(item) for item in s1.words], lag_ratio=0.1)

        color_dict = {
            RED_D: VGroup(),
            ORANGE: VGroup(),
            YELLOW: VGroup(),
            GREEN: VGroup(),
        }
        # set color
        color_patterns = [
            [RED_D, ORANGE, YELLOW, GREEN],
            [GREEN, RED_D, ORANGE, YELLOW],
            [YELLOW, GREEN, RED_D, ORANGE],
            [ORANGE, YELLOW, GREEN, RED_D],
        ]

        def color_gen(i):
            pattern = color_patterns[i]
            while True:
                for color in pattern:
                    yield color

        for i in range(10):
            gen = color_gen(i % 4)
            for j in range(10):
                grid10x10_[i * 10 + j].generate_target()
                color = next(gen)
                grid10x10_[i * 10 + j].target.set_fill(color, opacity=1).set_stroke(
                    width=1, color=GREY_E, opacity=1
                )
                color_dict[color].add(grid10x10_[i * 10 + j])

        self.playwl(
            *[MoveToTarget(m) for m in grid10x10_[:30]], lag_ratio=0.3, wait=0.5
        )
        self.playwl(*[MoveToTarget(m) for m in grid10x10_[30:]])

        text_patterns = [
            ["빨", "주", "노", "초"],
            ["초", "빨", "주", "노"],
            ["노", "초", "빨", "주"],
            ["주", "노", "초", "빨"],
        ]
        th = VGroup(
            Text(
                text_patterns[0][i], font="Noto Sans KR", font_size=20, color=BLACK
            ).move_to(grid10x10_[i].get_center())
            for i in range(4)
        )
        self.playwl(*[FadeIn(t) for t in th], lag_ratio=0.1, wait=0)
        self.playwl(*[FadeOut(t) for t in th], lag_ratio=0.1, wait=0.5)
        tv = VGroup(
            Text(
                ["빨", "초", "노", "주"][i],
                font="Noto Sans KR",
                font_size=20,
                color=BLACK,
            ).move_to(grid10x10_[i * 10].get_center())
            for i in range(4)
        )
        self.playwl(*[FadeIn(t) for t in tv], lag_ratio=0.1, wait=0)
        self.playwl(*[FadeOut(t) for t in tv], lag_ratio=0.1, wait=0.5)

        # bar
        def bar(row, col, vertical=True):
            w, h = (0.5 * 0.8, 2 * 0.8) if vertical else (2 * 0.8, 0.5 * 0.8)
            color = choice([BLUE, TEAL, MINT, DARK_BROWN, PURPLE])
            bar = Rectangle(
                width=w,
                height=h,
                fill_color=color,
                fill_opacity=1,
                stroke_color=interpolate_color(color, BLACK, 0.5),
                stroke_width=4,
            )
            bar.align_to(grid10x10[row * 10 + col], UL)
            return bar

        y, x = 2, 4
        b0 = bar(y, x, vertical=False).set_z_index(1)
        s2 = (
            Words(
                "놓여진 일자는 네 칸의 색이 모두 다르다.",
                font_size=24,
                font="Noto Sans KR",
            )
            .next_to(s1, DOWN, buff=0.5)
            .align_to(s1, LEFT)
        )
        self.playwl(*[FadeIn(item) for item in s2.words], FadeIn(b0), lag_ratio=0.15)
        self.playw(b0.animate.set_fill(opacity=0))
        tb = VGroup(
            Text(item, font="Noto Sans KR", font_size=20, color=BLACK).move_to(
                grid10x10_[y * 10 + x + i].get_center()
            )
            for i, item in enumerate(["노", "초", "빨", "주"])
        )
        self.playwl(*[FadeIn(t) for t in tb], lag_ratio=0.1)

        y, x = 5, 2
        self.play(b0.animate.align_to(grid10x10[y * 10 + x], UL), FadeOut(tb))
        tb = VGroup(
            Text(item, font="Noto Sans KR", font_size=20, color=BLACK).move_to(
                grid10x10_[y * 10 + x + i].get_center()
            )
            for i, item in enumerate(["주", "노", "초", "빨"])
        )
        self.playwl(*[FadeIn(t) for t in tb], lag_ratio=0.1)

        self.play(
            Rotating(b0, radians=PI / 2, about_point=b0.get_corner(UL)),
            FadeOut(tb),
            run_time=1,
        )
        tb = VGroup(
            Text(item, font="Noto Sans KR", font_size=20, color=BLACK).move_to(
                grid10x10_[(y - 4 + i) * 10 + x].get_center()
            )
            for i, item in enumerate(["주", "빨", "초", "노"])
        )
        self.playwl(*[FadeIn(t) for t in tb], lag_ratio=0.1)

        self.playw(Circumscribe(s1))
        self.playw(Circumscribe(s2))

        squares_dict = {
            RED_D: VGroup(),
            ORANGE: VGroup(),
            YELLOW: VGroup(),
            GREEN: VGroup(),
        }

        def color_bar(row, col, i, vertical=True):
            cp = color_patterns[i]

            bar = VGroup(*[Square(side_length=0.5 * 0.8) for _ in range(4)]).arrange(
                DOWN if vertical else RIGHT, buff=0
            )
            for j in range(4):
                bar[j].set_fill(cp[j], opacity=1).set_stroke(
                    interpolate_color(cp[j], BLACK, 0.5), width=2
                )
                squares_dict[cp[j]].add(bar[j])
            bar.align_to(grid10x10_[row * 10 + col], UL)
            return bar

        b0c = color_bar(0, 2, 0, vertical=True)
        bs = VGroup(
            b0,
            *[
                color_bar(
                    min(i // 10, 6), min(i % 10, 6), j % 4, vertical=i % 8 == 0
                ).set_z_index(0)
                for j, i in enumerate(range(4, 100, 4))
            ],
        ).set_opacity(0)
        b0.set_opacity(1).set_fill(opacity=0)

        bs.generate_target()
        for i, item in enumerate(bs.target):
            if i == 0:
                item.become(b0c)
            item.set_stroke(width=1)
            if item.get_width() > item.get_height():
                item.rotate(PI / 2)
        bs.target.arrange(RIGHT, buff=0.1).scale(0.6).next_to(
            s2, DOWN, buff=1.5
        ).set_opacity(1).align_to(s2, LEFT)
        self.playw(MoveToTarget(bs), FadeOut(tb))
        squares_dict[RED_D][0] = bs[0][0]
        squares_dict[ORANGE][0] = bs[0][1]
        squares_dict[YELLOW][0] = bs[0][2]
        squares_dict[GREEN][0] = bs[0][3]

        self.play(
            squares_dict[RED_D]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(s2, DOWN, buff=0.3)
            .align_to(s2, LEFT),
        )
        self.play(
            squares_dict[ORANGE]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(squares_dict[RED_D], DOWN, buff=0.1)
            .align_to(squares_dict[RED_D], LEFT),
        )
        self.play(
            squares_dict[YELLOW]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(squares_dict[ORANGE], DOWN, buff=0.1)
            .align_to(squares_dict[ORANGE], LEFT),
        )
        self.playw(
            squares_dict[GREEN]
            .animate.set_opacity(1)
            .arrange(RIGHT, buff=0.05)
            .next_to(squares_dict[YELLOW], DOWN, buff=0.1)
            .align_to(squares_dict[YELLOW], LEFT),
        )

        s3 = (
            Words(
                "일자가 25개 놓이면 네 색은 각각 25개씩 있다.",
                font_size=24,
                font="Noto Sans KR",
            )
            .move_to(s2)
            .align_to(s2, LEFT)
        )
        self.playwl(
            VGroup(s1, s2).animate.shift(UP * 0.8),
            *[FadeIn(item) for item in s3.words],
            lag_ratio=0.1,
        )

        self.wait()

        color_dict = {
            RED_D: VGroup(),
            ORANGE: VGroup(),
            YELLOW: VGroup(),
            GREEN: VGroup(),
        }
        for i in range(10):
            gen = color_gen(i % 4)
            for j in range(10):
                color = next(gen)
                color_dict[color].add(grid10x10_[i * 10 + j])
        color_dict[RED_D] = VGroup(
            *sorted(
                [color_dict[RED_D][i] for i in range(len(color_dict[RED_D]))],
                key=lambda m: m.get_x(),
            )
        )
        color_dict[ORANGE] = VGroup(
            *sorted(
                [color_dict[ORANGE][i] for i in range(len(color_dict[ORANGE]))],
                key=lambda m: m.get_x(),
            )
        )
        color_dict[YELLOW] = VGroup(
            *sorted(
                [color_dict[YELLOW][i] for i in range(len(color_dict[YELLOW]))],
                key=lambda m: m.get_x(),
            )
        )
        color_dict[GREEN] = VGroup(
            *sorted(
                [color_dict[GREEN][i] for i in range(len(color_dict[GREEN]))],
                key=lambda m: m.get_x(),
            )
        )
        self.playw(
            color_dict[RED_D]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.582)
            .next_to(squares_dict[GREEN], DOWN, buff=0.3)
            .align_to(squares_dict[GREEN], LEFT),
        )
        self.play(
            color_dict[ORANGE]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.582)
            .next_to(color_dict[RED_D], DOWN, buff=0.1)
            .align_to(color_dict[RED_D], LEFT),
            run_time=0.5,
        )
        self.playw(
            color_dict[GREEN]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.582)
            .next_to(color_dict[ORANGE], DOWN, buff=0.1)
            .align_to(color_dict[ORANGE], LEFT),
            run_time=0.5,
        )
        self.playw(
            color_dict[YELLOW]
            .animate.arrange(RIGHT, buff=0.1)
            .scale(0.582)
            .next_to(color_dict[GREEN], DOWN, buff=0.1)
            .align_to(color_dict[GREEN], LEFT),
        )

        self.playwl(
            Circumscribe(color_dict[RED_D]),
            Circumscribe(color_dict[YELLOW]),
            lag_ratio=0.5,
        )

        s4 = (
            Words(
                "100칸 내 각 색깔 수가 전부 25개는 아니다",
                font_size=24,
                font="Noto Sans KR",
            )
            .move_to(s1.words[3])
            .align_to(s1.words[3], LEFT)
            .set_opacity(0)
        )
        s4.words[0].set_opacity(1)
        self.play(Circumscribe(s1.words[3], buff=0.05, stroke_width=2), run_time=0.5)
        self.playw(s4.animate.shift(UP * 0.6).set_opacity(1))

        self.playw(
            FadeOut(*[squares_dict[item] for item in squares_dict]),
            s4.animate.next_to(s3, DOWN, buff=0.5).align_to(s3, LEFT),
        )

        contradict = SurroundingRectangle(VGroup(s3, s4), buff=0.2, stroke_color=RED, stroke_width=2)
        self.playw(Create(contradict), VGroup(s3, s4).animate.set_color(PURE_RED))

        self.playw(Flash(grid10x10.get_corner(UL)))