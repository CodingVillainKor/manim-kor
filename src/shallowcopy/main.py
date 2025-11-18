from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        code = PythonCode("src/intro.py")

        self.playw(FadeIn(code))
        code.generate_target().set_opacity(0.3)
        code.target.code[1].set_opacity(1)
        code.target.text_slice(2, "copy()").set_color(YELLOW)
        self.playw(MoveToTarget(code))
        code.save_state()

        self.playwl(
            *[code.code[i].animate.set_opacity(1) for i in range(2, 4)], lag_ratio=0.5
        )

        self.playw(code.code.animate.set_color(PURE_RED))

        self.play(Restore(code))
        call_code = Words(
            "num = second_largest(profiles)", font=MONO_FONT, font_size=24
        )
        self.playwl(
            code.animate.scale(0.7).shift(UP * 2), FadeIn(call_code), lag_ratio=0.3
        )

        self.playw(call_code[-9:-1].animate.set_color(PURE_RED))
        self.wait(2)

        sct = Words(
            "Shallow copy", font="Noto Sans KR", font_size=40
        ).set_color_by_gradient(RED_A, RED)
        code.save_state()
        call_code.save_state()
        self.playw(
            code.code[1].animate.set_opacity(0.3),
            call_code.animate.set_opacity(0.3).shift(DOWN),
            FadeIn(sct),
        )

        self.playwl(FadeOut(sct), Restore(code), Restore(call_code), lag_ratio=0.1)

        cdc = (
            Text("copy.deepcopy()", font_size=28, font="Noto Sans KR")
            .set_color_by_gradient(GREY_A, GREY)
            .next_to(self.cf, RIGHT)
            .shift(DOWN * 2)
        )
        self.playw(cdc.animate.next_to(self.cf, LEFT).shift(DOWN * 2), rate_func=linear)


class shallowCopy(Scene2D):
    def construct(self):
        sct = Words(
            "Shallow copy", font="Noto Sans KR", font_size=48
        ).set_color_by_gradient(RED_A, RED)
        self.playw(FadeIn(sct))
        self.playw(sct.animate.shift(UP * 2.5).scale(40 / 48))

        check1 = Words(
            "1. '복사한다'라는 말에서 떠오르는 개념",
            font="Noto Sans KR",
            font_size=32,
            color=ORANGE,
        )
        check2 = Words(
            "2. list, dict의 구현은 주소값",
            font="Noto Sans KR",
            font_size=32,
            color=ORANGE,
        )
        checks = VGroup(check1, check2).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        self.playw(
            FadeIn(check1.words[0], check2.words[0]), lag_ratio=0.5, run_time=0.5
        )

        self.playwl(*[FadeIn(item) for item in checks[0].words[1:]], lag_ratio=0.3)
        self.playwl(*[FadeIn(item) for item in checks[1].words[1:]], lag_ratio=0.3)

        self.playw(
            check1.animate.move_to(ORIGIN),
            FadeOut(check2, shift=DOWN),
            FadeOut(sct, shift=UP),
        )
        copyt = check1[3:7]
        copyt.save_state()
        _copyt_rest = VGroup(check1[:3], check1[7:])
        self.play(copyt.animate.set_color(YELLOW), FadeOut(_copyt_rest))
        self.play(copyt.animate.move_to(ORIGIN).shift(UP * 2.5))

        paper_scale = 2.5
        paper = Rectangle(
            width=paper_scale, height=paper_scale * 1.618, color=WHITE
        ).set_fill(WHITE, opacity=1)
        content = Words(
            "Huggingface.co: \n\n허-긴빠이치시오", font_size=18, color=BLACK
        )
        copy_ = VGroup(paper, content).copy().set_z_index(-1)
        orig = VGroup(paper, content)

        self.play(copyt.animate.set_color(YELLOW_A), FadeIn(paper))
        self.playw(Write(content), run_time=1)

        self.playw(VGroup(orig, copy_).animate.arrange(RIGHT, buff=1))

        self.play(Wiggle(orig))
        self.playw(Wiggle(copy_))

        file = File("main.py")
        filec = File("main (copy).py")
        self.playwl(FadeOut(orig, copy_), FadeIn(file), lag_ratio=0.3)
        file.generate_target()
        VGroup(file.target, filec).arrange(RIGHT, buff=1)
        self.playw(
            Transform(file.copy(), filec, replace_mobject_with_target_in_scene=True),
            MoveToTarget(file),
        )
        size = Words("2 KB", font_size=24, color=YELLOW).next_to(file, DOWN)
        sizec = Words("2 KB", font_size=24, color=YELLOW).next_to(filec, DOWN)
        self.play(FadeIn(size, shift=DOWN * 0.5))
        self.playw(FadeIn(sizec, shift=DOWN * 0.5), run_time=0.5)

        self.playw(FadeOut(size, sizec))
        arrow1 = Arrow(
            file.get_bottom() + DOWN,
            file.get_bottom(),
            stroke_width=2,
            tip_length=0.2,
            color=YELLOW,
        )
        arrow2 = Arrow(
            filec.get_bottom() + DOWN,
            filec.get_bottom(),
            stroke_width=2,
            tip_length=0.2,
            color=YELLOW,
        )
        self.play(GrowArrow(arrow1))
        self.playw(GrowArrow(arrow2))
        answer = (
            Words("별개의 존재를 만듦", font_size=20, font="Noto Sans KR")
            .set_color_by_gradient(ORANGE, RED_B)
            .next_to(_copyt_rest, DOWN)
            .shift(RIGHT)
        )
        self.playwl(
            FadeOut(file, filec, arrow1, arrow2, shift=LEFT * 4),
            AnimationGroup(
                FadeIn(_copyt_rest, shift=LEFT * 3),
                Restore(copyt),
            ),
            lag_ratio=0.2,
            wait=0.1,
        )
        self.playwl(*[FadeIn(item) for item in answer.words], lag_ratio=0.4)


class shallowCopy2(Scene3D):
    def construct(self):
        sct = (
            Words("Shallow copy", font="Noto Sans KR", font_size=48)
            .set_color_by_gradient(RED_A, RED)
            .shift(UP * 2.5)
        )
        check1 = Words(
            "1. '복사한다'라는 말에서 떠오르는 개념",
            font="Noto Sans KR",
            font_size=32,
            color=ORANGE,
        )
        check2 = Words(
            "2. list, dict의 구현은 주소값",
            font="Noto Sans KR",
            font_size=32,
            color=ORANGE,
        )
        checks = VGroup(check1, check2).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        checks.save_state()
        checks.set_opacity(0)
        sct.save_state()
        sct.set_opacity(0)

        check1.set_opacity(1).move_to(ORIGIN)
        answer1 = (
            Words("별개의 존재를 만듦", font_size=20, font="Noto Sans KR")
            .set_color_by_gradient(ORANGE, RED_B)
            .next_to(check1, DOWN)
            .shift(RIGHT)
        )
        self.addw(check1, answer1)
        self.playwl(
            Restore(checks),
            FadeOut(answer1, shift=UP * 0.75),
            Restore(sct),
        )
        self.playw(FadeOut(sct, check1), check2.animate.move_to(ORIGIN))
        self.playw(check2.animate.scale(1.1), run_time=2.5)

        code = Code(
            code_string="nums = [1, 2, 3, 4, 5]",
            language="python",
            add_line_numbers=False,
        )
        self.playwl(
            check2.animate.shift(UP * 2.5).scale(1 / 1.1), FadeIn(code), lag_ratio=0.3
        )
        tilt_angle = PI / 3.5
        self.play(code.animate.rotate(tilt_angle, axis=UP).shift(RIGHT))
        code_in = (
            Words("nums = <위치1>", font=MONO_FONT, font_size=24, color=GREY_B)
            .next_to(code, LEFT)
            .rotate(tilt_angle, axis=UP)
        )
        self.playw(FadeIn(code_in.words[:2], shift=LEFT))
        self.playw(FadeIn(code_in.words[2:]))

        locate = Words(
            "<위치1> [1, 2, 3, 4, 5]", font=MONO_FONT, font_size=20, color=GREY_C
        ).next_to(code, DOWN, buff=1.5)
        locate.words[0].set_color(GREY_B)
        self.play(FadeIn(locate, shift=DOWN))
        self.playw(Indicate(locate.words[0]), Indicate(code_in.words[2]))

        code2 = (
            Code(
                code_string="nums = [1, 2, 3, 4, 5]\nnums.append(6)",
                language="python",
                add_line_numbers=False,
            )
            .rotate(tilt_angle, axis=UP)
            .move_to(code)
            .align_to(code, UP)
        )
        self.playw(Transform(code, code2))
        locate2 = (
            Words(
                "<위치1> [1, 2, 3, 4, 5, 6]",
                font=MONO_FONT,
                font_size=20,
                color=GREY_C,
            )
            .move_to(locate)
            .align_to(locate, LEFT)
        )
        locate2.words[0].set_color(GREY_B)
        self.playwl(
            *[Indicate(item, scale_factor=1.0) for item in code_in.words],
            Indicate(locate.words[0], scale_factor=1.0),
            Transform(locate[-1], locate2[-3:]),
            lag_ratio=0.15,
        )


class whatisshallowcopy(Scene3D):
    def construct(self):
        sct = (
            Words("Shallow copy", font="Noto Sans KR", font_size=48)
            .set_color_by_gradient(RED_A, RED)
            .shift(UP * 2.5)
        )
        check1 = Words(
            "1. '복사한다'라는 말에서 떠오르는 개념",
            font="Noto Sans KR",
            font_size=32,
            color=ORANGE,
        )
        check2 = Words(
            "2. list, dict의 구현은 주소값",
            font="Noto Sans KR",
            font_size=32,
            color=ORANGE,
        )
        checks = VGroup(check1, check2).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        c1c, c2c = check1.copy(), check2.copy()
        check1.scale(7 / 8).align_to(c1c, LEFT)
        check2.scale(7 / 8).align_to(c2c, LEFT)
        self.addw(sct, checks)

        self.playw(check1.animate.scale(8 / 7).align_to(c1c, LEFT), run_time=2)
        self.playw(check2.animate.scale(8 / 7).align_to(c2c, LEFT), run_time=2)

        self.playw(Flash(sct.get_corner(UL)), FadeOut(checks))

        code = Code(
            code_string="nums = [1, 2, 3, 4, 5]\nnums2 = nums",
            language="python",
            add_line_numbers=False,
        )

        self.playw(FadeIn(code))
        code_in1 = Words(
            "nums = <위치1>", font=MONO_FONT, font_size=24, color=GREY_B
        ).shift(LEFT * 2.5)
        code_in2 = (
            Words("nums2 = <위치1>", font=MONO_FONT, font_size=24, color=GREY_B).shift(
                DOWN * 0.5
            )
        ).align_to(code_in1, RIGHT)
        tilt_angle = PI / 3.5
        self.play(code.animate.rotate(tilt_angle, axis=UP).shift(RIGHT))
        self.playw(
            FadeIn(code_in1.words[1:], shift=LEFT * 0.5),
            Transform(
                code.code_lines[0][:4].copy(),
                code_in1.words[0],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.play(FadeIn(code_in2, shift=DOWN * 0.3))

        locate = Words(
            "<위치1> [1, 2, 3, 4, 5]", font=MONO_FONT, font_size=20, color=GREY_C
        ).next_to(code, DOWN, buff=1)
        locate.words[0].set_color(GREY_B)
        self.playw(FadeIn(locate, shift=DOWN))

        self.playw(Write(code.code_lines[1].copy().set_color(YELLOW)), run_time=1)
        self.playw(
            Indicate(locate.words[0]),
            Indicate(code_in1.words[-1]),
            Indicate(code_in2.words[-1]),
        )

        rect = SurroundingRectangle(
            VGroup(code_in1.words[-1], code_in2.words[-1]),
            stroke_width=2,
            color=YELLOW_B,
        )
        arrow = Arrow(
            rect.get_corner(DOWN + RIGHT * 0.7),
            locate.get_corner(UL),
            buff=0.1,
            stroke_width=3,
            tip_length=0.15,
            color=YELLOW_B,
        )
        self.playwl(FadeIn(rect), GrowArrow(arrow), lag_ratio=0.1, wait=0.1)
        self.playw(Flash(locate.get_corner(UL)))


class whyBug(Scene3D):
    def construct(self):
        t1 = Text("실제 동작", font="Noto Sans KR", font_size=32, color=GREY_B)
        t2 = Text("우리의 의도", font="Noto Sans KR", font_size=32, color=GREY_B)
        mid_lane = DashedLine(
            start=UP * 4,
            end=DOWN * 4,
            stroke_width=2,
            dashed_ratio=0.7,
            dash_length=0.2,
            color=GREY_D,
        )
        VGroup(t1, t2).arrange(RIGHT, buff=5.5).to_edge(UP)

        self.play(FadeIn(t1))
        self.playw(FadeIn(t2))
        self.playw(Create(mid_lane))

        code = Code(
            code_string="nums = [1, 2, 3, 4, 5]\nnums2 = nums\nnums2.append(6)",
            language="python",
            add_line_numbers=False,
        ).shift(RIGHT * 3.5)
        self.playw(FadeIn(code), run_time=1.5)
        tilt_angle = PI / 6
        self.play(code.animate.rotate(tilt_angle, axis=UP).shift(UP))
        code_in1 = Words(
            "nums = <위치1>", font=MONO_FONT, font_size=24, color=GREY_B
        ).shift(RIGHT * 3.5 + DOWN * 0.5)
        code_in1.words[-1].set_color(RED_B)
        code_in2 = (
            Words("nums2 = <위치2>", font=MONO_FONT, font_size=24, color=GREY_B)
            .shift(RIGHT * 3.5 + DOWN * 1)
            .align_to(code_in1, RIGHT)
        )
        code_in2.words[-1].set_color(YELLOW_B)
        self.playw(
            FadeIn(code_in1.words[1:], shift=LEFT * 0.5),
            Transform(
                code.code_lines[0][:4].copy(),
                code_in1.words[0],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.playw(
            FadeIn(code_in2.words[1:], shift=LEFT * 0.5),
            Transform(
                code.code_lines[1][:5].copy(),
                code_in2.words[0],
                replace_mobject_with_target_in_scene=True,
            ),
        )

        code_real = code.copy().shift(LEFT * 7)
        code_real_in1 = code_in1.copy().shift(LEFT * 7)
        code_real_in2 = (
            Words("nums2 = <위치1>", font=MONO_FONT, font_size=24, color=GREY_B)
            .shift(LEFT * 7 + DOWN)
            .align_to(code_real_in1, RIGHT)
        )
        code_real_in2.words[-1].set_color(RED_B)

        self.play(
            Transform(
                code.copy(), code_real, replace_mobject_with_target_in_scene=True
            ),
            Transform(
                code_in1.copy(),
                code_real_in1,
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.playw(
            Transform(
                code_in2.copy(),
                code_real_in2,
                replace_mobject_with_target_in_scene=True,
            ),
        )

        self.playw(
            Circumscribe(code_in2.words[-1], color=YELLOW_B),
            Circumscribe(code_real_in2.words[-1], color=RED_B),
        )
        self.playw(
            Indicate(code_real_in1.words[-1], color=RED_D),
            Indicate(code_real_in2.words[-1], color=RED_D),
        )

        self.playw(
            Flash(code_in1.get_corner(UR), color=RED),
            Flash(code_in2.get_corner(UR), color=YELLOW),
        )
        self.playw(
            Flash(code_real_in1.get_corner(UR), color=RED),
            Flash(code_real_in2.get_corner(UR), color=RED),
        )

        self.wait(2)

        total = VGroup(*[item for item in self.mobjects if isinstance(item, VMobject)])
        bug = PythonCode("src/pattern.py")
        self.playw(FadeOut(total, shift=LEFT * 14), FadeIn(bug, shift=LEFT * 14))
        bug.generate_target().set_opacity(0.3)
        bug.target.text_slice(1, "nums: list").set_opacity(1)
        self.playwl(
            MoveToTarget(bug),
            self.cf.animate.move_to(bug.text_slice(1, "nums: list")),
            lag_ratio=0.4,
        )


class piuiandp(Scene2D):
    def construct(self):
        p = Words("p = [1, 2, 3]", font=MONO_FONT, font_size=32).shift(UP)
        piui = (
            Words("piui = p", font=MONO_FONT, font_size=32)
            .next_to(p, DOWN, buff=0.5)
            .align_to(p, LEFT)
        )

        list_ = (
            Text("[1, 2, 3]", font=MONO_FONT, color=GREY_C, font_size=32)
            .next_to(piui, DL, buff=1.2)
            .shift(RIGHT * 2.5)
        )
        VGroup(p.words[0], piui.words[0]).set_color(YELLOW_B)

        arrow_p = Arrow(
            p.words[0].get_corner(DL),
            list_.get_left(),
            stroke_width=2,
            tip_length=0.15,
            color=GREY_B,
        )
        arrow_piui = Arrow(
            piui.words[0].get_corner(DL),
            list_.get_left(),
            stroke_width=2,
            tip_length=0.15,
            color=GREY_B,
            buff=0.1,
        )
        self.addw(p, piui, list_, arrow_p, arrow_piui)

        append = (
            Words("piui.append(4)", font=MONO_FONT, font_size=32)
            .next_to(piui, DOWN, buff=0.2)
            .align_to(piui, LEFT)
        )
        self.playw(FadeIn(append))

        list2_ = (
            Text("[1, 2, 3, 4]", font=MONO_FONT, color=GREY_C, font_size=32)
            .move_to(list_)
            .align_to(list_, LEFT)
        )
        self.playw(
            Transform(
                list_[-1],
                VGroup(list2_[-3], list2_[-1]),
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                append[-2].copy(), list2_[-2], replace_mobject_with_target_in_scene=True
            ),
        )


class listcopy(Scene2D):
    def construct(self):
        numbers = Words("numbers: list", font=MONO_FONT, font_size=32).shift(UP * 1.5)
        numbers.words[-1].set_color(GREEN_B)
        numbers_copy = (
            Words("numbers = numbers.copy()", font=MONO_FONT, font_size=32)
            .next_to(numbers, DOWN, buff=0.5)
            .align_to(numbers, LEFT)
        )

        list_ = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=32)
            .next_to(numbers_copy, DL, buff=1.2)
            .shift(RIGHT * 1.5)
        )
        list2 = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=32)
            .move_to(list_)
            .shift(DR + RIGHT * 2)
        )
        arrow1 = Arrow(
            numbers.words[0].get_corner(DL),
            list_.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=GREEN_B,
            buff=0.1,
        )
        self.addw(numbers, list_, arrow1)
        self.play(FadeIn(numbers_copy))
        self.playw(
            numbers_copy[-7:].animate.set_color(YELLOW_C),
            Flash(numbers_copy[-7:].get_corner(LEFT)),
        )
        self.play(
            Transform(list_.copy(), list2, replace_mobject_with_target_in_scene=True)
        )
        arrow2 = Arrow(
            numbers_copy.words[0].get_corner(DOWN),
            list2.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=GREEN_B,
            buff=0.1,
        )
        self.playw(GrowArrow(arrow2))


class listcopyshallow(Scene2D):
    def construct(self):
        numbers = Words("numbers: list", font=MONO_FONT, font_size=32).shift(UP * 1.5)
        numbers.words[-1].set_color(GREEN_B)
        numbers_copy = (
            Words("numbers = numbers.copy()", font=MONO_FONT, font_size=32)
            .next_to(numbers, DOWN, buff=0.5)
            .align_to(numbers, LEFT)
        )

        list_ = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=32)
            .next_to(numbers_copy, DL, buff=1.2)
            .shift(RIGHT * 1.5)
        )
        list2 = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=32)
            .move_to(list_)
            .shift(DR + RIGHT * 2)
        )
        arrow1 = Arrow(
            numbers.words[0].get_corner(DL),
            list_.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=GREEN_B,
            buff=0.1,
        )
        self.addw(numbers, list_, arrow1, numbers_copy)
        self.play(
            numbers_copy[-7:].animate.set_color(YELLOW_C),
            Flash(numbers_copy[-7:].get_corner(LEFT)),
        )
        self.play(
            Transform(list_.copy(), list2, replace_mobject_with_target_in_scene=True)
        )
        arrow2 = Arrow(
            numbers_copy.words[0].get_corner(DOWN),
            list2.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=GREEN_B,
            buff=0.1,
        )
        self.playw(GrowArrow(arrow2))

        list_list = (
            Words("[[1, 2], [3, 4]]", font=MONO_FONT, font_size=28)
            .move_to(list_)
            .shift(LEFT * 0.3)
        )
        self.play(
            FadeTransform(list_, list_list),
            arrow1.animate.put_start_and_end_on(
                arrow1.get_start(), list_list.get_corner(UL) + UP * 0.1
            ),
        )
        list_list_ = (
            (Words("[<주소A>, <주소B>]", font=MONO_FONT, font_size=28))
            .move_to(list_list)
            .align_to(list_list, LEFT)
        )
        # list_list_.words[0][1:-1].set_color(RED_B)
        addra = list_list_.words[0][1:-1].set_color(RED_B)
        # list_list_.words[1][:-1].set_color(RED_B)
        addrb = list_list_.words[1][:-1].set_color(RED_B)

        listA = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=24)
            .next_to(list_list, DL, buff=1.0)
            .shift(RIGHT * 1.1 + UP * 0.2)
        )
        listB = (
            Text("[3, 4]", font=MONO_FONT, color=GREY_C, font_size=24)
            .next_to(list_list, DR, buff=1.0)
            .shift(LEFT * 1.5 + DOWN * 0.6)
        )
        self.playwl(
            AnimationGroup(
                Transform(
                    list_list[1:6].copy(),
                    listA,
                    replace_mobject_with_target_in_scene=True,
                ),
                Transform(
                    list_list[-6:-1].copy(),
                    listB,
                    replace_mobject_with_target_in_scene=True,
                ),
                lag_ratio=0.2,
            ),
            AnimationGroup(Transform(list_list, list_list_), FadeOut(arrow2, list2)),
            self.cf.animate.shift(DOWN),
            lag_ratio=0.2,
            wait=0.1,
        )
        arrowA = Arrow(
            list_list_.words[0][1:-1].get_corner(DOWN),
            listA.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        arrowB = Arrow(
            list_list_.words[1][:-1].get_corner(DOWN),
            listB.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        self.playw(GrowArrow(arrowA), GrowArrow(arrowB))

        self.play(Flash(numbers_copy[-7:].get_corner(LEFT)))

        list2_list = list_list_.copy().move_to(list2).shift(RIGHT * 2 + UP * 0.5)
        addra2 = list2_list.words[0][1:-1].set_color(RED_B)
        addrb2 = list2_list.words[1][:-1].set_color(RED_B)
        arrow2.put_start_and_end_on(
            numbers_copy.words[0].get_corner(DOWN),
            list2_list.get_corner(UL),
        )
        self.play(
            Transform(
                list_list_.copy(), list2_list, replace_mobject_with_target_in_scene=True
            ),
        )
        self.play(GrowArrow(arrow2))
        arrow2A = Arrow(
            list2_list.words[0][1:-1].get_corner(LEFT),
            listA.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        arrow2B = Arrow(
            list2_list.words[1][:-1].get_corner(DOWN),
            listB.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        self.playw(GrowArrow(arrow2A), GrowArrow(arrow2B))

        brackets1 = VGroup(list_list[0], list_list[-1])
        brackets2 = VGroup(list2_list[0], list2_list[-1])
        self.play(Indicate(brackets1, scale_factor=1.1))
        self.playw(Indicate(brackets2, scale_factor=1.1))

        addrac = addra.copy()
        addrbc = addrb.copy()
        addrac2 = addra2.copy()
        addrbc2 = addrb2.copy()

        self.playw(
            Transform(addrac, addrac2, replace_mobject_with_target_in_scene=True),
            Transform(addrbc, addrbc2, replace_mobject_with_target_in_scene=True),
        )
        self.playw(VGroup(addra, addrb, addrac2, addrbc2).animate.set_color(PURE_RED))

        dct = (
            Text("copy.deepcopy()", font=MONO_FONT, font_size=32)
            .shift(RIGHT * 14 + DOWN)
            .set_color_by_gradient(BLUE_A, BLUE)
        )
        self.add(dct)
        self.playw(self.cf.animate.move_to(dct))

        list_list = Words("[[1, 2], [3, 4]]", font=MONO_FONT, font_size=28).move_to(
            self.cf
        ).shift(LEFT*2)
        list_list_ = (
            (Words("[<주소A>, <주소B>]", font=MONO_FONT, font_size=28))
            .move_to(list_list)
            .align_to(list_list, LEFT)
        )
        listA = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=24)
            .next_to(list_list, DL, buff=1.0)
            .shift(RIGHT * 1.1 + UP * 0.2)
        )
        listB = (
            Text("[3, 4]", font=MONO_FONT, color=GREY_C, font_size=24)
            .next_to(list_list, DR, buff=1.0)
            .shift(LEFT * 1.5 + DOWN * 0.6)
        )
        arrowA = Arrow(
            list_list_.words[0][1:-1].get_corner(DOWN),
            listA.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        arrowB = Arrow(
            list_list_.words[1][:-1].get_corner(DOWN),
            listB.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        self.play(
            LaggedStart(
            dct.animate.next_to(self.cf, UL, buff=-0.75)
            .shift(RIGHT * 3.3)
            .set_color_by_gradient(GREY, GREY_A),
            FadeIn(list_list), lag_ratio=0.3)
        )
        self.playw(
            Transform(
                list_list[1:6].copy(),
                listA,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                list_list[-6:-1].copy(),
                listB,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(list_list[1:6], list_list_[1:6], replace_mobject_with_target_in_scene=True),
            Transform(list_list[-6:-1], list_list_[-6:-1], replace_mobject_with_target_in_scene=True),
            GrowArrow(arrowA), GrowArrow(arrowB),
        )

        list_list_dc = (
            (Words("[<주소C>, <주소D>]", font=MONO_FONT, font_size=28))
            .next_to(list_list, RIGHT, buff=1.5).shift(UP*0.7)
        )
        listC = (
            Text("[1, 2]", font=MONO_FONT, color=GREY_C, font_size=24)
            .next_to(list_list_dc, DL, buff=1.0)
            .shift(RIGHT * 1.8 + DOWN * 0.2)
        )
        listD = (
            Text("[3, 4]", font=MONO_FONT, color=GREY_C, font_size=24)
            .next_to(list_list_dc, DR, buff=1.0)
            .shift(LEFT * 1.9 + DOWN * 0.4)
        )
        arrowC = Arrow(
            list_list_dc.words[0][1:-1].get_corner(DOWN),
            listC.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        arrowD = Arrow(
            list_list_dc.words[1][:-1].get_corner(DOWN),
            listD.get_corner(UL),
            stroke_width=2,
            tip_length=0.15,
            color=RED_B,
            buff=0.1,
        )
        self.play(
            Transform(
                list_list_.copy(),
                list_list_dc,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                listA.copy(),
                listC,
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                listB.copy(),
                listD,
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.playw(
            GrowArrow(arrowC), GrowArrow(arrowD),
        )
