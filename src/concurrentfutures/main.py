from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        cmd = Text("python main.py", font_size=32, font=MONO_FONT)
        cmd[6:].set_color(GREEN)
        self.playw(
            LaggedStart(
                *[FadeIn(item, run_time=0.5) for item in [cmd[:6], cmd[6:]]],
                lag_ratio=0.3,
            )
        )
        code_s = PythonCode("intro.py").scale(0.75)
        process_box = SurroundingRect(color=GREY_B).surround(
            code_s, buff_h=0.5, buff_w=0.5
        )
        process_text = (
            Text("process", font_size=24, font="Noto Serif")
            .next_to(process_box, UP, buff=0.05)
            .align_to(process_box, LEFT)
        )
        process = VGroup(process_box, process_text)

        self.playw(
            LaggedStart(
                Transform(
                    cmd[:6], process_box, replace_mobject_with_target_in_scene=True
                ),
                FadeIn(process_text),
                Transform(cmd[6:], code_s, replace_mobject_with_target_in_scene=True),
                lag_ratio=0.6,
            )
        )
        for anim in code_s.exec(use_tracer=True):
            self.play(anim, run_time=0.2)

        self.wait()


class introMP(Scene3D):
    def construct(self):
        cmd = Text("python main_mp.py", font_size=32, font=MONO_FONT)
        cmd[6:].set_color(GREEN)
        self.playw(
            LaggedStart(
                *[FadeIn(item, run_time=0.5) for item in [cmd[:6], cmd[6:]]],
                lag_ratio=0.3,
            )
        )
        code_s = PythonCode("intro_mp.py").scale(0.85)
        process_box = SurroundingRect(color=GREY_B).surround(
            code_s, buff_h=0.5, buff_w=0.5
        )
        process_text = (
            Text("Process", font_size=24, font="Noto Serif")
            .next_to(process_box, UP, buff=0.05)
            .align_to(process_box, LEFT)
        )
        process = VGroup(process_box, process_text, code_s).shift(LEFT * 4)
        self.move_camera_horizontally(
            45,
            zoom=0.7,
            added_anims=[
                Transform(
                    cmd[:6], process_box, replace_mobject_with_target_in_scene=True
                ),
                FadeIn(process_text),
                Transform(cmd[6:], code_s, replace_mobject_with_target_in_scene=True),
            ],
        )

        processes = VGroup(
            *[
                get_process(code_s.code[4:6].copy().set_opacity(0)).rotate(
                    45 * DEGREES, DOWN
                )
                for _ in range(4)
            ]
        )
        processes.arrange(DOWN, buff=0.3).shift(OUT * 6 + UP * 0.5)
        ppe = code_s.text_slice(8, "ProcessPoolExecutor()").copy().set_color(YELLOW)
        self.playw(Transform(ppe, processes, replace_mobject_with_target_in_scene=True))

        anim_lines = code_s.exec(with_line_no=True)
        for anim, line in anim_lines:
            self.play(anim, run_time=0.5)
            if line == 9:
                intos = []
                exes = []
                for i in range(6):
                    arg = code_s.code[8][-23:-16].copy()
                    fn1 = processes[i % 4][-1][0].copy()
                    fn2 = processes[i % 4][-1][1].copy()
                    return_value = fn2
                    intos.append(
                        Succession(
                            arg.animate.rotate(-45 * DEGREES, UP).move_to(
                                processes[i % 4].get_center()
                            ),
                            AnimationGroup(
                                FadeOut(arg, scale=1.5),
                                VGroup(fn1, fn2).animate.set_opacity(1),
                            ),
                            AnimationGroup(
                                return_value.animate.move_to(code_s.code[8][-23]),
                                fn1.animate.set_opacity(0),
                            ),
                            FadeOut(return_value),
                        )
                    )
                self.play(LaggedStart(*intos, lag_ratio=0.13))


def get_process(code):
    process_box = SurroundingRect(color=YELLOW_B, stroke_width=3).surround(
        code, buff_h=0.5, buff_w=0.5
    )
    process_text = (
        Text("Worker process", font_size=20, color=YELLOW_B, font="Noto Serif")
        .next_to(process_box, UP, buff=0.05)
        .align_to(process_box, LEFT)
    )
    return VGroup(process_box, process_text, code)


class img1(Scene2D):
    def construct(self):
        code = PythonCode("img_example.py").shift(UP * 0.5)

        self.playw(FadeIn(code))

        hlin, _ = code.highlight(1, "range(1000)", anim=Circumscribe)
        self.playw(hlin)

        et = Text("0.1 sec", font_size=24, font="Noto Serif", color=RED).next_to(
            code.code[3][-1]
        )
        hlin, hlout = code.highlight(4, color=RED)
        self.playw(Write(et), hlin)

        anims = code.exec(with_line_no=True)
        for anim, line in anims:
            if line == 4:
                file = (
                    File(size=0.3)
                    .move_to(code.code[3][-1])
                    .shift(DOWN * 0.2)
                    .set_opacity(0.4)
                )
                self.play(
                    anim,
                    AnimationGroup(
                        file.animate.shift(DR * 0.5).set_opacity(0), rate_func=rush_from
                    ),
                    run_time=0.4,
                )
            else:
                self.play(anim, run_time=0.2)
        self.wait()


class imgMP(Scene3D):
    def construct(self):
        code = PythonCode("img_example_mp.py").scale(0.85).shift(UP * 0.5 + LEFT * 4)
        self.tilt_camera_horizontal(45, zoom=0.7)
        self.addw(code)

        hlin, hlout = code.highlight(3, "ProcessPoolExecutor()", color=PURE_GREEN)
        self.play(hlin, run_time=1)
        self.playw(hlout)
        pcode = (
            PythonCode("process.py")
            .scale(0.9)
            .rotate(45 * DEGREES, DOWN)
            .set_opacity(0)
        )
        processes = VGroup(
            *[
                get_process(pcode.code.copy()).rotate(45 * DEGREES, DOWN)
                for _ in range(4)
            ]
        )

        processes.arrange(DOWN, buff=0.3).shift(OUT * 4 + UP * 0.5)
        self.playw(
            Transform(
                code.text_slice(3, "ProcessPoolExecutor()").copy().set_color(YELLOW),
                processes,
                replace_mobject_with_target_in_scene=True,
            )
        )

        braces = VGroup(
            *[
                Brace(p[0], RIGHT, color=YELLOW_A).rotate(45 * DEGREES, DOWN).shift(OUT)
                for p in processes
            ]
        )
        brace_texts = VGroup(
            *[
                Text(f"0.1 sec", font_size=20, font="Noto Serif", color=YELLOW_A)
                .rotate(45 * DEGREES, DOWN)
                .next_to(b, RIGHT, buff=0.05)
                .shift(OUT * 0.5)
                for i, b in enumerate(braces)
            ]
        )
        self.playw(
            LaggedStart(
                *[FadeIn(b, bt, run_time=0.5) for b, bt in zip(braces, brace_texts)],
                lag_ratio=0.3,
            )
        )

        anims = code.exec(with_line_no=True)
        for anim, line in anims:
            if line == 4:
                self.play(anim, run_time=0.3)
                intos = []
                for i in range(20):
                    arg = code.text_slice(4, "process, d").copy()
                    fn1 = (
                        processes[i % 4][-1][0]
                        .copy()
                        .rotate(45 * DEGREES, UP)
                        .scale(0.8)
                    )
                    fn2 = (
                        processes[i % 4][-1][1]
                        .copy()
                        .rotate(45 * DEGREES, UP)
                        .scale(0.8)
                    )
                    return_value = fn2
                    intos.append(
                        Succession(
                            arg.animate.rotate(-45 * DEGREES, UP).move_to(
                                processes[i % 4].get_center()
                            ),
                            AnimationGroup(
                                FadeOut(arg, scale=1.5),
                                VGroup(fn1, fn2).animate.set_opacity(1),
                            ),
                            AnimationGroup(
                                return_value.animate.move_to(
                                    code.text_slice(5, "future.result()")
                                ),
                                fn1.animate.set_opacity(0),
                            ),
                        )
                    )
                self.play(LaggedStart(*intos, lag_ratio=0.18))
            else:
                self.play(anim, run_time=0.3)

        self.wait()


class forTN(Scene2D):
    def construct(self):
        box_cpu = lambda t: TextBox(
            f"CPU | {t}%",
            text_kwargs={
                "font_size": 32,
                "font": "Noto Serif",
                "color": BLUE,
            },
            box_kwargs={
                "stroke_width": 3,
                "color": BLUE,
                "buff": 0.2
            }
        )

        boxes = VGroup(
            *[box_cpu(100 if i == 0 else 0) for i in range(6)]
        ).arrange(DOWN, aligned_edge=RIGHT).shift(LEFT*3)
        boxes[0].set_color(RED).set_fill(RED, opacity=0.5)
        boxes[0].text.set_color(PURE_RED)

        brace = Brace(boxes[1:], RIGHT, buff=0.7, sharpness=1.5)
        
        self.addw(boxes, brace)
