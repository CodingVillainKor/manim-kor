from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(38)


class whatisma(Scene2D):
    def construct(self):
        emat = Text("EMA", font_size=48).set_color_by_gradient(GREY_A, GREY_B)
        ema_fullt = (
            Words("Exponential Moving Average", font_size=48)
            .set_color_by_gradient(GREY_A, GREY_C)
            .set_opacity(0.3)
        )
        for word in ema_fullt.words:
            word[0].set_color(WHITE).set_opacity(1.0)
        self.playw(FadeIn(emat))
        self.playw(
            Transform(
                emat[0], ema_fullt.words[0], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                emat[1], ema_fullt.words[1], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                emat[2], ema_fullt.words[2], replace_mobject_with_target_in_scene=True
            ),
        )
        e_m_a = VGroup(*[word[0] for word in ema_fullt.words]).copy()
        self.playw(
            e_m_a.animate.arrange(RIGHT),
            ema_fullt.animate.shift(UP * 1.5).set_opacity(0.3),
        )

        self.playw(ema_fullt.words[1:].animate.set_opacity(1.0))
        self.playw(ema_fullt.words[0].animate.set_opacity(1).set_color(YELLOW))
        self.playw(
            FadeOut(ema_fullt.words[0], shift=LEFT),
            ema_fullt.words[1:].animate.move_to(ORIGIN),
            FadeOut(e_m_a, shift=DOWN),
        )
        self.wait(2)

        data_list = [10, 12, 14, 13, 11.5, 15, 14, 17, 16, 18, 17, 19, 20, 18, 21]
        data_ma3_list = [
            sum(data_list[max(0, i - 2) : i + 1]) / min(i + 1, 3)
            for i in range(len(data_list))
        ]
        nump = NumberPlane(
            x_range=[0, len(data_list) + 1, 1],
            y_range=[5, 25, 1],
            background_line_style={"stroke_opacity": 0.2},
            x_length=10,
            y_length=5.5,
        ).shift(UP * 0.3)
        xt = Text("Time", font_size=20, color=GREY_B).next_to(
            nump.x_axis.get_end(), RIGHT, buff=0.1
        )
        yt = Text("Stock price", font_size=20, color=GREY_B).next_to(
            nump.y_axis.get_end(), LEFT, buff=0.1
        )
        data = VGroup(
            *[
                Dot(nump.c2p(i + 1, data_list[i]), radius=DEFAULT_SMALL_DOT_RADIUS)
                for i in range(len(data_list))
            ]
        )
        data_nums = VGroup(
            *[
                DecimalNumber(data_list[i], font_size=22, num_decimal_places=1).next_to(
                    nump.c2p(i + 1, data_list[i]), UP, buff=0.1
                )
                for i in range(len(data_list))
            ]
        )
        data_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_list[i]),
                    nump.c2p(i + 2, data_list[i + 1]),
                    stroke_width=2,
                    color=GREY_B,
                ).set_opacity(0.5)
                for i in range(len(data_list) - 1)
            ]
        )
        data_ma3 = VGroup(
            *[
                Dot(
                    nump.c2p(i + 1, data_ma3_list[i]),
                    radius=DEFAULT_SMALL_DOT_RADIUS,
                    color=RED,
                )
                for i in range(len(data_list))
            ]
        )
        data_ma3_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_ma3_list[i]),
                    nump.c2p(i + 2, data_ma3_list[i + 1]),
                    stroke_width=2,
                    color=RED,
                )
                for i in range(len(data_list) - 1)
            ]
        )

        self.playwl(
            ema_fullt.words[1:].animate.to_edge(UP, 0.1).scale(0.6),
            FadeIn(nump, data, data_lines, xt, yt, data_nums),
            lag_ratio=0.5,
            wait=0.1,
        )
        self.playw(
            Transform(data.copy(), data_ma3, replace_mobject_with_target_in_scene=True),
            Transform(
                data_lines.copy(),
                data_ma3_lines,
                replace_mobject_with_target_in_scene=True,
            ),
            rate_func=rush_from,
        )

        self.playw(Flash(xt), FadeOut(data_ma3, data_ma3_lines))
        self.playw(Flash(yt))

        eday_brace = Brace(
            Line(nump.c2p(len(data_list) - 1, 5), nump.c2p(len(data_list), 5)),
            UP,
            buff=0,
            color=GREY,
        )
        eday = Text("1 day", font_size=20, color=YELLOW).next_to(
            eday_brace, UP, buff=0.05
        )
        self.playw(FadeIn(eday_brace, eday))
        path_ = BrokenLine(
            *[nump.c2p(i + 1, data_list[i]) for i in range(len(data_list))],
        )
        path_.set_stroke(GREEN, 2)
        self.playw(FadeOut(eday_brace, eday), Create(path_), run_time=1.5)

        self.playw(self.cf.animate.scale(1.15).align_to(self.cf, LEFT))

        ma3t = Words("3-day Moving Average", font_size=28).set_color_by_gradient(
            RED_C, RED_A
        )
        VGroup(ma3t.words[0], ma3t.words[1:]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1
        ).next_to(nump, RIGHT, buff=0.3).shift(UP * 1.5)
        self.playw(FadeIn(ma3t))

        avg_fnt = Words(
            "mean(    )", font_size=24, font=MONO_FONT, color=RED_B
        ).move_to(nump.c2p(len(data_list) - 1, 12))
        self.playw(FadeIn(avg_fnt))

        def get_mean(end_idx):
            comma1 = (
                Text(",", font_size=24, font=MONO_FONT).set_opacity(0).move_to(avg_fnt)
            )
            comma2 = (
                Text(",", font_size=24, font=MONO_FONT).set_opacity(0).move_to(avg_fnt)
            )
            nums = VGroup(
                data_nums[max(end_idx - 2, 0)].copy(),
                data_nums[max(end_idx - 1, 0)].copy(),
                data_nums[end_idx].copy(),
            )
            items = VGroup(
                avg_fnt.words[0],
                nums[0],
                comma1,
                nums[1],
                comma2,
                nums[2],
                avg_fnt.words[1],
            )
            items.generate_target()
            items.target.arrange(RIGHT, buff=0.1).move_to(avg_fnt)
            items.target[1::2].scale(1.1)
            items.target[2].set_opacity(1).shift(DOWN * 0.1 + LEFT * 0.03)
            items.target[4].set_opacity(1).shift(DOWN * 0.1 + LEFT * 0.03)
            return items

        mean = get_mean(len(data_list) - 1)
        self.playw(MoveToTarget(mean))
        ts = VGroup(mean[0].copy(), mean[-1].copy(), mean[1:-1])
        self.playw(
            Transform(ts, data_ma3[-1], replace_mobject_with_target_in_scene=True)
        )

        self.play(avg_fnt.animate.move_to(nump.c2p(len(data_list) - 2, 12)))
        mean = get_mean(len(data_list) - 2)
        self.play(MoveToTarget(mean))
        ts = VGroup(mean[0].copy(), mean[-1].copy(), mean[1:-1])
        self.playw(
            Transform(ts, data_ma3[-2], replace_mobject_with_target_in_scene=True)
        )

        for i in range(len(data_list) - 3, -1, -1):
            run_time = 0.5
            self.play(
                avg_fnt.animate.move_to(nump.c2p(i, 7 + i * 0.333)), run_time=run_time
            )
            mean = get_mean(i)
            self.play(MoveToTarget(mean), run_time=run_time)
            ts = VGroup(mean[0].copy(), mean[-1].copy(), mean[1:-1])
            self.playw(
                Transform(ts, data_ma3[i], replace_mobject_with_target_in_scene=True),
                run_time=run_time,
                wait=0.1,
            )
        self.playw(FadeIn(data_ma3_lines), FadeOut(avg_fnt))


class characteristics(Scene3D):
    def construct(self):
        data_list = [10, 12, 14, 13, 11.5, 15, 14, 17, 16, 18, 17, 19, 20, 18, 21]
        data_ma3_list = [
            sum(data_list[max(0, i - 2) : i + 1]) / min(i + 1, 3)
            for i in range(len(data_list))
        ]
        nump = NumberPlane(
            x_range=[0, len(data_list) + 1, 1],
            y_range=[5, 25, 1],
            background_line_style={"stroke_opacity": 0.2},
            x_length=10,
            y_length=5.5,
        ).shift(UP * 0.3)
        data = VGroup(
            *[
                Dot(nump.c2p(i + 1, data_list[i]), radius=DEFAULT_SMALL_DOT_RADIUS)
                for i in range(len(data_list))
            ]
        )
        xt, yt = (
            Text("Time", font_size=20, color=GREY_B).next_to(
                nump.x_axis.get_end(), RIGHT, buff=0.1
            ),
            Text("Stock price", font_size=20, color=GREY_B).next_to(
                nump.y_axis.get_end(), LEFT, buff=0.1
            ),
        )
        data_lines = VGroup(
            *[
                Arrow(
                    nump.c2p(i + 1, data_list[i]),
                    nump.c2p(i + 2, data_list[i + 1]),
                    stroke_width=2,
                    color=GREY_B,
                    buff=0,
                    tip_length=0.15,
                ).set_opacity(0.5)
                for i in range(len(data_list) - 1)
            ]
        )
        data_ma3 = VGroup(
            *[
                Dot(
                    nump.c2p(i + 1, data_ma3_list[i]),
                    radius=DEFAULT_SMALL_DOT_RADIUS,
                    color=GREEN,
                )
                for i in range(len(data_list))
            ]
        )
        data_ma3_lines = VGroup(
            *[
                Arrow(
                    nump.c2p(i + 1, data_ma3_list[i]),
                    nump.c2p(i + 2, data_ma3_list[i + 1]),
                    stroke_width=2,
                    color=GREEN,
                    buff=0,
                    tip_length=0.1,
                )
                for i in range(len(data_list) - 1)
            ]
        )

        self.addw(nump, data, xt, yt, data_lines)
        data_linesc = data_lines.copy()
        self.move_camera_horizontally(
            50,
            zoom=0.8,
            added_anims=[
                data_linesc.animate.arrange(RIGHT, buff=0.01)
                .shift(OUT * 3)
                .set_color(RED)
                .set_opacity(1)
            ],
        )

        self.play(FadeIn(data_ma3_lines))
        data_ma3_linesc = data_ma3_lines.copy()
        self.playw(
            data_ma3_lines.animate.arrange(RIGHT, buff=0.01).shift(OUT * 3),
            FadeOut(data_linesc),
            run_time=1.5,
        )

        self.move_camera_horizontally(0, zoom=1, added_anims=[FadeOut(data_ma3_lines)])

        day_increase = VGroup(
            *[
                item
                for item in data_lines
                if item.get_start()[0] < item.get_end()[0]
                and item.get_end()[1] > item.get_start()[1]
            ]
        )
        day_decrease = VGroup(
            *[
                item
                for item in data_lines
                if item.get_start()[0] < item.get_end()[0]
                and item.get_end()[1] < item.get_start()[1]
            ]
        )
        day_increase.save_state()
        day_decrease.save_state()
        self.playw(day_increase.animate.set_color(GREEN).set_opacity(1))
        self.playw(
            Restore(day_increase), day_decrease.animate.set_color(RED).set_opacity(1)
        )

        day_decrease_x = VGroup(
            *[
                Line(nump.c2p(i + 1, 5), nump.c2p(i + 2, 5), stroke_width=4, color=RED)
                for i in range(len(data_list) - 1)
                if data_list[i + 1] < data_list[i]
            ]
        )
        self.playw(
            Transform(
                day_decrease.copy(),
                day_decrease_x,
                replace_mobject_with_target_in_scene=True,
            )
        )

        self.playw(
            FadeOut(day_decrease_x),
            Restore(day_decrease),
            data.animate.set_opacity(0.5),
            FadeIn(data_ma3_linesc),
        )
        path_ = BrokenLine(
            *[nump.c2p(i + 1, data_ma3_list[i]) for i in range(len(data_list))],
        )
        path_.set_stroke(GREEN, 4)
        self.playw(Create(path_), run_time=2)

        mat = Words("3-day Moving Average", font_size=28).set_color_by_gradient(
            GREEN_C, GREEN_A
        )
        VGroup(mat.words[0], mat.words[1:]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1
        ).next_to(nump, RIGHT, buff=0.3).shift(UP * 1.5)

        self.playw(FadeOut(path_), self.cf.animate.shift(OUT * 3 + RIGHT), FadeIn(mat))
        data_ma4_list = [
            sum(data_list[max(0, i - 3) : i + 1]) / min(i + 1, 4)
            for i in range(len(data_list))
        ]
        data_ma4 = VGroup(
            *[
                Dot(
                    nump.c2p(i + 1, data_ma4_list[i]),
                    radius=DEFAULT_SMALL_DOT_RADIUS,
                    color=GREEN,
                )
                for i in range(len(data_list))
            ]
        )
        data_ma4_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_ma4_list[i]),
                    nump.c2p(i + 2, data_ma4_list[i + 1]),
                    stroke_width=2,
                    color=GREEN,
                )
                for i in range(len(data_list) - 1)
            ]
        )
        mat_ = Words("4-day Moving Average", font_size=28).set_color_by_gradient(
            GREEN_C, GREEN_A
        )
        VGroup(mat_.words[0], mat_.words[1:]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1
        ).next_to(nump, RIGHT, buff=0.3).shift(UP * 1.5)
        self.playw(
            Transform(
                data_ma3,
                data_ma4,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                data_ma3_linesc,
                data_ma4_lines,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(mat, mat_),
            rate_func=rush_from,
        )

        data_ma5_list = [
            sum(data_list[max(0, i - 4) : i + 1]) / min(i + 1, 5)
            for i in range(len(data_list))
        ]
        data_ma5 = VGroup(
            *[
                Dot(
                    nump.c2p(i + 1, data_ma5_list[i]),
                    radius=DEFAULT_SMALL_DOT_RADIUS,
                    color=GREEN,
                )
                for i in range(len(data_list))
            ]
        )
        data_ma5_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_ma5_list[i]),
                    nump.c2p(i + 2, data_ma5_list[i + 1]),
                    stroke_width=2,
                    color=GREEN,
                )
                for i in range(len(data_list) - 1)
            ]
        )
        mat_ = Words("5-day Moving Average", font_size=28).set_color_by_gradient(
            GREEN_C, GREEN_A
        )
        VGroup(mat_.words[0], mat_.words[1:]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1
        ).next_to(nump, RIGHT, buff=0.3).shift(UP * 1.5)
        self.playw(
            Transform(
                data_ma4,
                data_ma5,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                data_ma4_lines,
                data_ma5_lines,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(mat, mat_),
            rate_func=rush_from,
        )


class following(Scene2D):
    def construct(self):
        def get_mat(day):
            mat = Words(
                f"{day}-day Moving Average", font_size=28
            ).set_color_by_gradient(GREEN_C, GREEN_A)
            VGroup(mat.words[0], mat.words[1:]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1
            ).next_to(nump, RIGHT, buff=0.3).shift(UP * 1.5)
            return mat

        data_list = [10 + i * 0.5 + np.random.randn() * 2 for i in range(50)]
        nump = NumberPlane(
            x_range=[0, len(data_list) + 1, 1],
            y_range=[5, 40, 1],
            background_line_style={"stroke_opacity": 0.2},
            x_length=10,
            y_length=5.5,
        ).shift(UP * 0.3)
        data = VGroup(
            *[
                Dot(nump.c2p(i + 1, data_list[i]), radius=DEFAULT_SMALL_DOT_RADIUS)
                for i in range(len(data_list))
            ]
        )
        xt, yt = (
            Text("Time", font_size=20, color=GREY_B).next_to(
                nump.x_axis.get_end(), RIGHT, buff=0.1
            ),
            Text("Stock price", font_size=20, color=GREY_B).next_to(
                nump.y_axis.get_end(), LEFT, buff=0.1
            ),
        )
        data_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_list[i]),
                    nump.c2p(i + 2, data_list[i + 1]),
                    stroke_width=2,
                    color=GREY_B,
                ).set_opacity(0.5)
                for i in range(len(data_list) - 1)
            ]
        )
        mat = get_mat(3)
        self.addw(nump, data, xt, yt, data_lines)
        self.playw(self.cf.animate.scale(1.15).align_to(self.cf, LEFT), run_time=0.1)
        ma_window = Integer(3)

        def get_mas(win_size):
            data_ma_list = [
                sum(data_list[max(0, i - (win_size - 1)) : i + 1])
                / min(i + 1, win_size)
                for i in range(len(data_list))
            ]
            data_ma = VGroup(
                *[
                    Dot(
                        nump.c2p(i + 1, data_ma_list[i]),
                        radius=DEFAULT_SMALL_DOT_RADIUS,
                        color=GREEN,
                    )
                    for i in range(len(data_list))
                ]
            )
            data_ma_lines = VGroup(
                *[
                    Line(
                        nump.c2p(i + 1, data_ma_list[i]),
                        nump.c2p(i + 2, data_ma_list[i + 1]),
                        stroke_width=2,
                        color=GREEN,
                    )
                    for i in range(len(data_list) - 1)
                ]
            )
            return data_ma, data_ma_lines

        data_ma, data_ma_lines = get_mas(ma_window.get_value())
        mat = get_mat(ma_window.get_value())
        self.playw(FadeIn(data_ma, data_ma_lines, mat))
        data_ma_, data_ma_lines_ = get_mas(ma_window.get_value() + 1)
        mat_ = get_mat(ma_window.get_value() + 1)
        self.playw(
            Transform(data_ma, data_ma_),
            Transform(data_ma_lines, data_ma_lines_),
            Transform(mat, mat_),
        )
        data_ma_, data_ma_lines_ = get_mas(ma_window.get_value() + 2)
        mat_ = get_mat(ma_window.get_value() + 2)
        self.playw(
            Transform(data_ma, data_ma_),
            Transform(data_ma_lines, data_ma_lines_),
            Transform(mat, mat_),
        )

        for i in range(3, 30, 6):
            data_ma_, data_ma_lines_ = get_mas(ma_window.get_value() + i)
            mat_ = get_mat(ma_window.get_value() + i)
            self.playw(
                Transform(data_ma, data_ma_),
                Transform(data_ma_lines, data_ma_lines_),
                Transform(mat, mat_),
                run_time=0.5,
                wait=0.1,
            )
        self.wait()
        self.playw(VGroup(data_ma, data_ma_lines).animate.set_color(PURE_RED))


class ema(Scene2D):
    def construct(self):
        data_list = [10 + i * 0.5 + np.random.randn() * 2 for i in range(30)]
        nump = NumberPlane(
            x_range=[0, len(data_list) + 1, 1],
            y_range=[5, 40, 1],
            background_line_style={"stroke_opacity": 0.2},
            x_length=10,
            y_length=5.5,
        ).shift(UP * 0.3)
        data = VGroup(
            *[
                Dot(nump.c2p(i + 1, data_list[i]), radius=DEFAULT_SMALL_DOT_RADIUS)
                for i in range(len(data_list))
            ]
        )
        xt, yt = (
            Text("Time", font_size=20, color=GREY_B).next_to(
                nump.x_axis.get_end(), RIGHT, buff=0.1
            ),
            Text("Stock price", font_size=20, color=GREY_B).next_to(
                nump.y_axis.get_end(), LEFT, buff=0.1
            ),
        )
        data_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_list[i]),
                    nump.c2p(i + 2, data_list[i + 1]),
                    stroke_width=2,
                    color=GREY_B,
                ).set_opacity(0.5)
                for i in range(len(data_list) - 1)
            ]
        )
        data_nums = VGroup(
            *[
                DecimalNumber(data_list[i], font_size=22, num_decimal_places=1).next_to(
                    nump.c2p(i + 1, data_list[i]),
                    (
                        DOWN
                        if min(data_list[max(i - 1, 0) : i + 2]) == data_list[i]
                        else UP
                    ),
                    buff=0.1,
                )
                for i in range(len(data_list))
            ]
        )
        self.addw(nump, data, xt, yt, data_lines, data_nums)

        avg_fnt = MathTex(
            "MA_{", "n", "}(", 2 * "\\qquad", ")", font_size=24, color=GREEN_B
        ).move_to(nump.c2p(len(data_list) - 2, 35))
        self.playwl(
            FadeIn(avg_fnt),
            self.cf.animate.move_to(avg_fnt).scale(0.6),
            nump.background_lines.animate.set_opacity(0.0),
        )

        def get_mas(end_idx, window):
            commas = VGroup(
                *[
                    Text(",", font_size=20, font=MONO_FONT)
                    .set_opacity(0)
                    .move_to(avg_fnt)
                    for _ in range(window - 1)
                ]
            )
            nums = VGroup(
                *[
                    data_nums[max(end_idx - (window - 1 - i), 0)].copy()
                    for i in range(window)
                ]
            )
            items = VGroup(avg_fnt[:-2], nums[0])
            for i in range(1, window):
                items.add(commas[i - 1], nums[i])
            items.add(avg_fnt[-1])
            items.generate_target()
            items.target.arrange(RIGHT, buff=0.1).move_to(avg_fnt)
            items.target[1::2].scale(1.1)
            for i in range(1, window):
                items.target[2 * i].set_opacity(1).shift(DOWN * 0.1 + LEFT * 0.03)
            return items

        ma_window = 3
        ma = get_mas(len(data_list) - 1, ma_window)
        self.playw(MoveToTarget(ma))

        def ma_unwrapped(end_idx, window):
            values_list = data_list[max(0, end_idx - (window - 1)) : end_idx + 1]
            t = MathTex(
                r"{",
                r"{",
                "+".join([f"{v:.1f}" for v in values_list]),
                "}",
                r"\over",
                rf"{{{window}}}",
                font_size=24,
            )[-2:].set_color(GREEN)
            return t

        def ma_unwrapped2(window):
            unit = MathTex(r"{1}", r"\over", rf"{{{window}}}", font_size=24)
            units = VGroup(*[unit.copy() for _ in range(window)])
            return units

        ma_ = ma_unwrapped(len(data_list) - 1, ma_window).next_to(avg_fnt, DOWN, buff=0)
        ma_nums = ma[1:-1:2]
        ma_commas = ma[2:-1:2]
        ma_upper = VGroup(ma_nums, ma_commas)
        ma_upper.generate_target()
        for comma in ma_upper.target[-1]:
            comma.become(Text("+", font_size=24, font=MONO_FONT))
        temp_ = VGroup()
        for num, comma in zip(*ma_upper.target):
            temp_.add(num).add(comma)
        temp_.add(ma_upper.target[0][-1])
        temp_.arrange(RIGHT, buff=0.1).next_to(ma_, UP, buff=0.05)
        self.playw(Transform(ma[0], ma_), MoveToTarget(ma_upper), FadeOut(ma[-1]))

        units = (
            ma_unwrapped2(ma_window).move_to(ma_).align_to(ma_, DOWN).set_color(GREEN)
        )
        temp_ = VGroup()
        for i in range(ma_window):
            if i != ma_window // 2:
                temp_.add(units[i].set_opacity(0))
            else:
                temp_.add(VGroup(*ma[0]))
            temp_.add(ma_nums[i])
            if i < ma_window - 1:
                temp_.add(ma_commas[i])
        temp_.generate_target().set_opacity(1)
        temp_.target[ma_window].become(units[ma_window // 2])
        temp_.target.arrange(RIGHT, buff=0.1).next_to(units, UP, buff=0.05).align_to(
            units, DOWN
        )
        self.playw(MoveToTarget(temp_))
        self.playw(
            units[-1].animate.become(
                MathTex("\\gamma_0", font_size=20).set_color(GREEN).move_to(units[-1])
            ),
            MathTex("\\cdot", font_size=24)
            .next_to(ma_nums[0], LEFT, buff=0.03)
            .set_color(GREEN)
            .set_opacity(0)
            .animate.set_opacity(1),
            temp_[ma_window].animate.become(
                MathTex("\\gamma_1", font_size=20)
                .set_color(GREEN)
                .move_to(temp_[ma_window])
            ),
            MathTex("\\cdot", font_size=24)
            .next_to(ma_nums[1], LEFT, buff=0.03)
            .set_color(GREEN)
            .set_opacity(0)
            .animate.set_opacity(1),
            units[0].animate.become(
                MathTex("\\gamma_2", font_size=20).set_color(GREEN).move_to(units[0])
            ),
            MathTex("\\cdot", font_size=24)
            .next_to(ma_nums[2], LEFT, buff=0.03)
            .set_color(GREEN)
            .set_opacity(0)
            .animate.set_opacity(1),
        )
        self.playw(Circumscribe(units[-1]))
        self.playw(Circumscribe(units[0]))

        nump2 = (
            NumberPlane(
                x_range=[0, 3, 1],
                y_range=[0, 1.5**3 + 2, 1],
                background_line_style={"stroke_opacity": 0.2},
                x_length=3,
                y_length=1.5,
            )
            .next_to(temp_, UP)
            .set_opacity(0.2)
        )
        plot = nump2.plot(
            lambda x: 1.8**x, color=GREEN, x_range=[3, -3, -0.01], stroke_width=2
        )
        self.playw(FadeIn(nump2), Create(plot, run_time=2))


class emaformula(Scene2D):
    def construct(self):
        _fs = 32
        terms = VGroup(*[ema_raw_term(i, font_size=_fs) for i in range(5)])
        terms = Joiner(*terms, join=lambda: MathTex("+", font_size=_fs))
        terms.add(VGroup(Text("...", font_size=_fs))).arrange(RIGHT, buff=0.1)
        # self.addw(terms)
        self.cf.move_to(terms[0]).scale(0.4)
        self.playw(FadeIn(terms[0][2]))
        self.playw(FadeIn(terms[0][:2]))

        self.play(FadeIn(terms[1:3]), self.cf.animate.scale(1.2).move_to(terms[:3]))
        self.play(FadeIn(terms[3:5]), self.cf.animate.scale(1.2).move_to(terms[:5]))
        self.play(FadeIn(terms[5:7]), self.cf.animate.scale(1.2).move_to(terms[:7]))
        self.play(FadeIn(terms[7:9]), self.cf.animate.scale(1.2).move_to(terms[:9]))
        self.playw(FadeIn(terms[9:11]), self.cf.animate.scale(1.1).move_to(terms[:11]))

        naive_terms = Joiner(
            *[naive_term(i+1, font_size=_fs) for i in range(5)],
            join=lambda: MathTex("+", font_size=_fs),
        )
        naive_terms.add(VGroup(Text("...", font_size=_fs))).set_color(RED).arrange(
            RIGHT, buff=0.1
        ).next_to(terms, DOWN, buff=0.5)
        self.playwl(
            terms.animate.set_opacity(0.4),
            *[FadeIn(naive_terms[i : i + 2]) for i in range(0, 11, 2)],
            run_time=3,
            lag_ratio=0.5,
        )

        coeffs1 = Joiner(
            *[
                item[:2].copy() if i else item[:1].copy()
                for i, item in enumerate(terms[0::2])
            ],
            join=lambda: MathTex("+", font_size=_fs),
        )
        coeffs1.generate_target().set_opacity(1).arrange(RIGHT).next_to(
            terms, UP, buff=1.2
        )
        for i, coeff in enumerate(coeffs1[1::2]):
            coeff.move_to(coeffs1.target[1::2][i]).set_opacity(0).shift(DOWN * 0.5)

        coeffs2 = Joiner(
            *[item[0].copy() for item in naive_terms[0::2]],
            join=lambda: MathTex("+", font_size=_fs),
        )
        coeffs2.generate_target().set_opacity(1).arrange(RIGHT).next_to(
            terms, UP, buff=0.6
        )
        for i, coeff in enumerate(coeffs2[1::2]):
            coeff.move_to(coeffs2.target[1::2][i]).set_opacity(0).shift(DOWN * 0.5)
        self.play(MoveToTarget(coeffs1))
        self.playw(MoveToTarget(coeffs2))

        eq1 = MathTex("=1", font_size=_fs, color=YELLOW).next_to(
            coeffs1, RIGHT, buff=0.25
        )
        eq2 = MathTex("=1", font_size=_fs, color=YELLOW).next_to(
            coeffs2, RIGHT, buff=0.25
        )
        self.playw(FadeIn(eq1, eq2, shift=RIGHT * 0.5))

        simple1 = (
            MathTex(
                r"\alpha",  # 0
                r"\over",  # 1
                r"{",  # 2
                r"1",  # 3
                r"-",  # 4
                r"(",  # 5
                "1",  # 6
                "-",  # 7
                r"\alpha",  # 8
                r")",  # 9
                r"}",  # 10
                font_size=_fs,
            )
            .move_to(coeffs1)
            .shift(UP * 0.3)
        )
        simple2 = MathTex(
            r"\gamma", r"\over", r"{", r"1 - \gamma", r"}", font_size=_fs
        ).move_to(coeffs2)
        self.playw(FadeTransform(coeffs2, simple2), FadeOut(eq2, shift=RIGHT * 0.5))
        self.playw(FadeTransform(coeffs1, simple1), FadeOut(eq1, shift=RIGHT * 0.5))

        self.playw(FadeOut(simple1[3], simple1[6], shift=DL * 0.5))
        malpha = simple1[7:9]
        malpha.generate_target().next_to(simple1[1], DOWN).align_to(simple1[7:9], DOWN)
        minus = simple1[4]
        minus.generate_target().rotate(PI/2).move_to(malpha.target[0].get_center())
        self.playw(
            FadeOut(simple1[5], simple1[9], shift=DR * 0.5),
            MoveToTarget(malpha),
            MoveToTarget(minus),
        )
        one = MathTex("1", font_size=_fs*1.5, color=YELLOW).move_to(simple1[1])
        self.playw(FadeIn(one, scale=1.5), FadeOut(malpha, minus, simple1[:2], scale=1.2))

        self.play(FadeOut(one, simple2, shift=UP), FadeOut(naive_terms, shift=DOWN*0.5), terms.animate.set_opacity(1))
        term_brace = Brace(terms, DOWN, buff=0.2, color=GREY, sharpness=1)
        not_infty = Text("Actually not ∞", font_size=24).next_to(
            term_brace, DOWN, buff=0.1
        ).set_color_by_gradient(RED_A, RED_C)
        self.playwl(FadeIn(term_brace), FadeIn(not_infty), lag_ratio=0.4)


def ema_raw_term(i, font_size=32):
    alpha = MathTex("\\alpha", font_size=font_size)
    one_minus_alpha_pow = (
        MathTex(f"(1 - \\alpha)", "^", f"{{{i}}}" * bool(i != 1), font_size=font_size)
        if i > 0
        else MathTex(r"\cdot", font_size=font_size)
    )
    data_term = MathTex(rf"x_{{T-{{{i}}}}}" if i else rf"x_{{T}}", font_size=font_size)

    g = VGroup(alpha, one_minus_alpha_pow, data_term).arrange(RIGHT, buff=0.05)
    return g


def naive_term(i, font_size=32):
    gamma = MathTex(rf"\gamma^{{{i}}}" if i!=1 else rf"\gamma", font_size=font_size)
    data_term = MathTex(rf"x_{{T-{{{i}}}}}" if i else rf"x_{{T}}", font_size=font_size)
    g = VGroup(gamma, data_term).arrange(RIGHT, buff=0.1)
    return g


class emavsma(Scene2D):
    def construct(self):
        num_data = 50
        data_list = [11 + 0.009 * i**2  + np.random.randn() * 3 for i in range(num_data)]
        nump = NumberPlane(
            x_range=[0, len(data_list) + 1, 1],
            y_range=[5, 40, 1],
            background_line_style={"stroke_opacity": 0.2},
            x_length=10,
            y_length=5.5,
        ).shift(UP * 0.3)

        data = VGroup(
            *[
                Dot(nump.c2p(i + 1, data_list[i]), radius=DEFAULT_SMALL_DOT_RADIUS*0.5)
                for i in range(len(data_list))
            ]
        )
        xt, yt = (
            Text("Time", font_size=20, color=GREY_C).next_to(
                nump.x_axis.get_end(), RIGHT, buff=0.1
            ),
            Text("Stock price", font_size=20, color=GREY_C).next_to(
                nump.y_axis.get_end(), LEFT, buff=0.1
            ),
        )
        data_lines = VGroup(
            *[
                Line(
                    nump.c2p(i + 1, data_list[i]),
                    nump.c2p(i + 2, data_list[i + 1]),
                    stroke_width=2,
                    color=GREY_C,
                ).set_opacity(0.5)
                for i in range(len(data_list) - 1)
            ]
        )

        ma_window = 8
        data_ma_list = [
            sum(data_list[max(0, i - ma_window + 1) : i + 1]) / min(i + 1, ma_window)
            for i in range(len(data_list))
        ]

        data_ema_list = []
        alpha = 0.2
        for i in range(len(data_list)):
            if i == 0:
                data_ema_list.append(data_list[0])
            else:
                ema_val = alpha * data_list[i] + (1 - alpha) * data_ema_list[i - 1]
                data_ema_list.append(ema_val)
        data_ema_list_new = []
        alpha_new = 0.3
        for i in range(len(data_list)):
            if i == 0:
                data_ema_list_new.append(data_list[0])
            else:
                ema_val = alpha_new * data_list[i] + (1 - alpha_new) * data_ema_list_new[i - 1]
                data_ema_list_new.append(ema_val)
        path_data = BrokenLine(
            *[nump.c2p(i + 1, data_list[i]) for i in range(len(data_list))],
        ).set_stroke(GREY_C, 4)
        path_ma_data = BrokenLine(
            *[nump.c2p(i + 1, data_ma_list[i]) for i in range(len(data_ma_list))],
        ).set_stroke(GREEN, 2)
        path_ema_data = BrokenLine(
            *[nump.c2p(i + 1, data_ema_list[i]) for i in range(len(data_ema_list))],
        ).set_stroke(PURE_RED, 2)
        path_camera_data = BrokenLine(
            *[nump.c2p(i + 1, data_ema_list_new[i]) for i in range(len(data_ema_list_new))],
        ).set_stroke(PURE_RED, 2).set_opacity(0)
        self.cf.move_to(nump.c2p(1, data_ema_list[0])).scale(0.4)
        
        dot_data_ema = Dot(nump.c2p(1, data_ema_list[0]), radius=DEFAULT_DOT_RADIUS, color=YELLOW).set_opacity(0.3)
        dot_data = Dot(nump.c2p(1, data_list[0]), radius=DEFAULT_DOT_RADIUS, color=GREY_C).set_opacity(0.3)
        dot_data_ma = Dot(nump.c2p(1, data_ma_list[0]), radius=DEFAULT_DOT_RADIUS, color=GREEN).set_opacity(0.3)
        dot_camera = Dot(nump.c2p(1, data_ema_list_new[0]), radius=DEFAULT_DOT_RADIUS, color=PURE_RED).set_opacity(0)
        data_label = Text("Data", font_size=20, color=GREY_C).next_to(dot_data, UR, buff=0.03).set_z_index(1)
        data_label.add_updater(lambda m: m.next_to(dot_data, UR, buff=0.03))
        data_ma_label = Text("MA", font_size=20, color=GREEN).next_to(dot_data_ma, DL, buff=0.03).set_z_index(1)
        data_ma_label.add_updater(lambda m: m.next_to(dot_data_ma, DL, buff=0.03))
        data_ema_label = Text("EMA", font_size=20, color=PURE_RED).next_to(dot_data_ema, DR, buff=0.03).set_z_index(1)
        data_ema_label.add_updater(lambda m: m.next_to(dot_data_ema, DR, buff=0.03))
        self.addw(nump, xt, yt, data_label, data_ma_label, data_ema_label, dot_data_ema, dot_data, dot_data_ma)
        self.playw(
            Create(path_data, rate_func=linear),
            Create(path_ma_data, rate_func=linear),
            Create(path_ema_data, rate_func=linear),
            Create(path_camera_data, rate_func=linear),
            MoveAlongPath(dot_camera, path_camera_data, rate_func=linear),
            MoveAlongPath(dot_data, path_data, rate_func=linear),
            MoveAlongPath(dot_data_ma, path_ma_data, rate_func=linear),
            MoveAlongPath(dot_data_ema, path_ema_data, rate_func=linear),
            UpdateFromFunc(self.cf, lambda m: m.move_to(dot_camera.get_center())),
            run_time=15,
            rate_func=linear
        )