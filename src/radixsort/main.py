from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        title = Words(
            "정렬 알고리즘", font_size=40, font="Noto Sans KR"
        ).set_color_by_gradient(BLUE_A, BLUE)
        self.playwl(*[FadeIn(item) for item in title.words], lag_ratio=0.5)

        nump = NumberPlane(
            x_range=[-0.5, 30, 2],
            y_range=[-0.5, 10, 2],
            x_length=7,
            y_length=5,
            background_line_style={"stroke_opacity": 0.0},
            axis_config={"stroke_color": GREY_B},
        )
        x_label = Text("n", font_size=24, color=GREY_B).next_to(
            nump.x_axis.get_end(), DOWN
        )
        y_label = Text("time", font_size=24, color=GREY_B).next_to(
            nump.y_axis.get_end(), LEFT
        )
        self.playwl(
            title.animate.to_edge(UP, buff=0.25),
            FadeIn(nump, x_label, y_label),
            lag_ratio=0.5,
            run_time=0.5,
            wait=0.1,
        )
        on2 = nump.plot(lambda x: 0.012 * x**2 + 0.2, x_range=[0, 29], color=RED)
        on2_label = MathTex("O(n^2)", font_size=32, color=RED).next_to(
            on2.get_end(), UP + RIGHT, buff=0.1
        )
        self.playw(FadeIn(on2, on2_label), run_time=1)

        onlogn = nump.plot(
            lambda x: 0.05 * x * np.log2(x + 1) + 0.2, x_range=[0, 29], color=GREEN
        )
        onlogn_label = MathTex("O(n\\log n)", font_size=32, color=GREEN).next_to(
            onlogn.get_end(), UP + RIGHT, buff=0.1
        )
        self.playw(FadeIn(onlogn, onlogn_label), run_time=1)

        on1 = nump.plot(lambda x: 0.12 * x + 0.2, x_range=[0, 29], color=BLUE)
        on1_label = MathTex("O(n)", font_size=32, color=BLUE).next_to(
            on1.get_end(), UP + RIGHT, buff=0.1
        )
        self.playw(FadeIn(on1, on1_label), run_time=1)

        rt = (
            Words("radix sort", font_size=32, color=BLUE, font="Noto Sans KR")
            .next_to(on1_label, DOWN, buff=0.1)
            .align_to(on1_label, LEFT)
        )
        self.playwl(*[FadeIn(item) for item in rt.words], lag_ratio=0.5)
        self.play(Flash(onlogn_label.get_corner(UL), color=PURE_GREEN))
        self.playw(Flash(on1_label.get_corner(UL), color=BLUE))

        self.play(
            self.cf.animate.move_to(VGroup(on1_label, rt)).scale(1.3),
            FadeOut(on2, on2_label, onlogn, onlogn_label, title),
            run_time=1,
        )
        self.playw(
            VGroup(on1_label, rt)
            .animate.scale(1.3)
            .align_to(VGroup(on1_label, rt), LEFT),
            run_time=2,
        )


class howradixsort(Scene2D):
    def construct(self):
        exp = Words(
            "Radix sort: 자릿수별 숫자 위치에 나열하는 방식",
            font_size=36,
            font="Noto Sans KR",
        ).set_color_by_gradient(BLUE_A, BLUE)
        self.addw(exp.words[:2], wait=1.5)
        self.playwl(*[FadeIn(item) for item in exp.words[2:]], lag_ratio=0.3)

        self.play(exp.animate.scale(0.7).to_corner(UL, buff=0.3))

        arr_list = [170, 45, 75, 90, 2, 802, 24, 66]

        def tb(num, text_kwargs, box_kwargs):
            textbox = TextBox(
                text=f"{num:03d}",
                text_kwargs=text_kwargs,
                box_kwargs=box_kwargs,
            )
            textbox.text[: 3 - len(str(num))].set_opacity(0)
            return textbox

        arr = VGroup(
            *[
                tb(
                    item,
                    text_kwargs=dict(font_size=32, color=GREY_A),
                    box_kwargs=dict(
                        stroke_color=GREY_B,
                        stroke_width=3,
                        buff=0.15,
                        fill_color=BLACK,
                        fill_opacity=1,
                    ),
                )
                for item in arr_list
            ]
        ).arrange(RIGHT)
        self.playwl(*[FadeIn(item) for item in arr], lag_ratio=0.4)

        digit_buffer = VGroup(
            *[
                TextBox(
                    str(num),
                    text_kwargs=dict(font_size=36, color=GREEN, font=MONO_FONT),
                    box_kwargs=dict(stroke_color=GREEN_E, stroke_width=2, buff=0.2),
                )
                for num in range(10)
            ]
        )
        for db in digit_buffer:
            db.box.stretch_to_fit_width(0.7)
        digit_buffer.arrange(RIGHT, buff=0.55).shift(DOWN * 1.3)
        self.playwl(*[FadeIn(item) for item in digit_buffer], lag_ratio=0.1)

        self.mouse.next_to(self.cf, RIGHT).align_to(exp.words[3:5].get_bottom(), UP)
        self.play(self.mouse.animate.next_to(exp.words[3:5], DOWN, buff=-0.05))
        self.play(Indicate(exp.words[3:5], scale_factor=1.1), FadeOut(self.mouse))
        self.playw(*[Indicate(item) for item in digit_buffer])

        self.playw(arr.animate.shift(UP * 1.3))
        digit1 = VGroup(*[item.text[2] for item in arr])
        self.playw(digit1.animate.set_color(YELLOW))

        digit1t = (
            Text("일의 자리", font_size=24, color=GREEN_E, font="Noto Sans KR")
            .next_to(digit_buffer, DOWN)
            .align_to(digit_buffer, RIGHT)
        )
        self.playw(FadeIn(digit1t))
        self.playwl(*[Flash(item) for item in digit1], lag_ratio=0.2)

        lasts = [item for item in digit_buffer]
        first_sorted = [[] for _ in range(10)]
        first_sorted_num = sorted(arr_list, key=lambda x: x % 10)

        for i in range(len(arr_list)):
            digit = int(arr_list[i] % 10)
            target_last = lasts[digit]
            arr[i].generate_target()
            arr[i].target.next_to(target_last, UP, buff=0.2)
            lasts[digit] = arr[i].target
            first_sorted[digit].append(arr[i])
        first_sorted = [item for sublist in first_sorted for item in sublist]

        self.playwl(*[MoveToTarget(item) for item in arr], lag_ratio=0.5)
        self.playwl(
            *[
                AnimationGroup(Flash(item), item.text[2].animate.set_color(GREY_A))
                for item in first_sorted
            ],
            lag_ratio=0.3,
        )

        self.mouse.next_to(self.cf, RIGHT).align_to(digit1t.get_center(), UP)
        self.play(self.mouse.animate.next_to(digit1t[0], DR, buff=-0.1))
        digit10t = Text(
            "십의 자리", font_size=24, color=GREEN_E, font="Noto Sans KR"
        ).move_to(digit1t)
        self.playw(Transform(digit1t, digit10t), FadeOut(self.mouse))

        digit2 = VGroup(*[item.text[1] for item in first_sorted])
        self.play(digit2.animate.set_color(YELLOW).set_opacity(1))
        self.playwl(*[Flash(item.text[1]) for item in first_sorted], lag_ratio=0.2)

        lasts = [item for item in digit_buffer]
        second_sorted = [[] for _ in range(10)]
        second_sorted_num = sorted(first_sorted_num, key=lambda x: (x // 10) % 10)
        for i in range(len(first_sorted)):
            num = int(first_sorted_num[i])
            digit = int((num // 10) % 10)
            target_last = lasts[digit]
            first_sorted[i].generate_target()
            first_sorted[i].target.next_to(target_last, UP, buff=0.2)
            lasts[digit] = first_sorted[i].target
            second_sorted[digit].append(first_sorted[i])
        second_sorted = [item for sublist in second_sorted for item in sublist]
        self.mouse.next_to(self.cf, LEFT).align_to(first_sorted[0].get_center(), UP)
        self.play(self.mouse.animate.next_to(first_sorted[0], DOWN, buff=-0.1))

        for i in range(len(first_sorted)):
            mouse_anim = (
                self.mouse.animate.next_to(first_sorted[i + 1], DOWN, buff=-0.1)
                if i + 1 < len(first_sorted)
                else FadeOut(self.mouse)
            )
            self.play(MoveToTarget(first_sorted[i]), mouse_anim)
        self.wait()

        self.playwl(
            *[
                AnimationGroup(Flash(item), item.text[1].animate.set_color(GREY_A))
                for item in second_sorted
            ],
            lag_ratio=0.3,
        )

        digit100t = Text(
            "백의 자리", font_size=24, color=GREEN_E, font="Noto Sans KR"
        ).move_to(digit1t)
        self.mouse.next_to(self.cf, RIGHT).align_to(digit1t.get_center(), UP)
        self.play(self.mouse.animate.next_to(digit1t[0], DR, buff=-0.1))
        self.playw(Transform(digit1t, digit100t), FadeOut(self.mouse))

        digit3 = VGroup(*[item.text[0] for item in second_sorted])
        self.play(digit3.animate.set_color(YELLOW).set_opacity(1))
        self.playwl(*[Flash(item.text[0]) for item in second_sorted], lag_ratio=0.2)

        lasts = [item for item in digit_buffer]
        final_sorted = [[] for _ in range(10)]
        for i in range(len(second_sorted)):
            num = int(second_sorted_num[i])
            digit = int((num // 100) % 10)
            target_last = lasts[digit]
            second_sorted[i].generate_target()
            second_sorted[i].target.next_to(target_last, UP, buff=0.2)
            lasts[digit] = second_sorted[i].target
            final_sorted[digit].append(second_sorted[i])
        final_sorted = [item for sublist in final_sorted for item in sublist]
        self.mouse.next_to(self.cf, LEFT).align_to(second_sorted[0].get_center(), UP)
        self.play(self.mouse.animate.next_to(second_sorted[0], DOWN, buff=-0.1))
        for i in range(len(second_sorted)):
            mouse_anim = (
                self.mouse.animate.next_to(second_sorted[i + 1], DOWN, buff=-0.1)
                if i + 1 < len(second_sorted)
                else FadeOut(self.mouse)
            )
            if i == len(second_sorted) - 1:
                mouse_anim = AnimationGroup(
                    mouse_anim,
                    self.cf.animate.scale(1.2).align_to(self.cf, DL),
                    exp.animate.shift(UP * 1.6),
                )
            self.play(MoveToTarget(second_sorted[i]), mouse_anim)
        self.wait()
        self.playwl(
            *[
                AnimationGroup(Flash(item), item.text[0].animate.set_color(GREY_A))
                for item in final_sorted
            ],
            lag_ratio=0.3,
        )

        final_sorted = VGroup(*final_sorted)
        final_sorted[-2].set_z_index(-100)
        for fs in final_sorted:
            fs.generate_target()
        VGroup(*[fs.target for fs in final_sorted]).arrange(RIGHT, buff=0.5).shift(
            DOWN * 1.5
        )
        self.playwl(
            FadeOut(digit_buffer, digit1t),
            AnimationGroup(*[MoveToTarget(fs) for fs in final_sorted], lag_ratio=0.5),
            lag_ratio=0.1,
            wait=0.1,
        )
        self.playw(
            self.cf.animate.scale(1 / 1.2).align_to(self.cf, DL).shift(DOWN * 1.5)
        )


class radixsortComplexity(Scene2D):
    def construct(self):
        arr_list = [170, 45, 75, 90, 2, 802, 24, 66]

        def tb(num, text_kwargs, box_kwargs):
            textbox = TextBox(
                text=f"{num:03d}",
                text_kwargs=text_kwargs,
                box_kwargs=box_kwargs,
            )
            textbox.text[: 3 - len(str(num))].set_opacity(0)
            return textbox

        arr = VGroup(
            *[
                tb(
                    item,
                    text_kwargs=dict(font_size=32, color=GREY_A),
                    box_kwargs=dict(
                        stroke_color=GREY_B,
                        stroke_width=3,
                        buff=0.15,
                        fill_color=BLACK,
                        fill_opacity=1,
                    ),
                )
                for item in arr_list
            ]
        ).arrange(RIGHT, buff=0.5)
        self.addw(arr)

        digit1 = VGroup(*[item.text[2] for item in arr])
        digit2 = VGroup(*[item.text[1] for item in arr])
        digit3 = VGroup(*[item.text[0] for item in arr])
        self.play(digit1.animate.set_color(YELLOW))
        self.play(digit2.animate.set_color(BLUE).set_opacity(1))
        self.playw(digit3.animate.set_color(RED).set_opacity(1))

        num = ValueTracker(3)
        get_d = lambda n: Text(
            f"자릿수: {int(n.get_value())}", font_size=32, font="Noto Sans KR"
        )
        digit_text = get_d(num).set_color(GREY_C).next_to(arr, UP).align_to(arr, RIGHT)
        self.playw(FadeIn(digit_text))

        new_arr_list = [1799.15, 750.6, 9094.2, 1.22, 80120.19, 66055.46]

        def new_tb(num, text_kwargs, box_kwargs):
            textbox = TextBox(
                text=f"{num:.2f}",
                text_kwargs=text_kwargs,
                box_kwargs=box_kwargs,
            )
            return textbox

        new_arr = VGroup(
            *[
                new_tb(
                    item,
                    text_kwargs=dict(font_size=32, color=GREY_A),
                    box_kwargs=dict(
                        stroke_color=GREY_B,
                        stroke_width=3,
                        buff=0.15,
                        fill_color=BLACK,
                        fill_opacity=1,
                    ),
                )
                for item in new_arr_list
            ]
        ).arrange(RIGHT, buff=0.2)
        self.playw(FadeTransform(arr, new_arr))
        digit_text.add_updater(
            lambda m: m.become(
                get_d(num).set_color(GREY_C).next_to(new_arr, UP).align_to(new_arr, RIGHT)
            )
        )
        self.play(num.animate.set_value(7), run_time=2)
        digit_text.suspend_updating()
        digit_text.remove_updater(digit_text.updaters[0])
        digit_text[-1].set_color(YELLOW)
        self.wait()

        ond = MathTex("O(nd)", font_size=60).set_color_by_gradient(BLUE_A, BLUE)
        ond.next_to(new_arr, DOWN, buff=0.8)
        self.playw(FadeIn(ond), self.cf.animate.shift(DOWN))
        self.playw(ond[0][-2].animate.set_color(PURE_RED))

        self.play(FadeOut(new_arr))
        self.playw(digit_text.animate.next_to(ond, DOWN, buff=0.4))

from random import random
class radixsortgood(Scene2D):
    def construct(self):
        nums_list = [random() * 999 for _ in range(100)]
        nums = VGroup(
            *[
                Text(f"{num:.1f}", font_size=24, color=GREY_A, font=MONO_FONT)
                for num in nums_list
            ]
        ).arrange(DOWN).align_to(ORIGIN, UP).shift(LEFT*3)
        datat = Text("Data", font_size=32, color=GREY_C, font="Noto Sans KR").next_to(nums, UP).align_to(nums, LEFT)
        self.play(FadeIn(datat))
        self.playwl(*[FadeIn(item) for item in nums], lag_ratio=0.2)
        self.cf.save_state()
        self.playw(self.cf.animate.scale(7).align_to(self.cf, UL))
        self.playw(Restore(self.cf), VGroup(datat, nums).animate.shift(LEFT))