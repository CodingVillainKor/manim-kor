from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        gil_text = Text("GIL").set_color_by_gradient(BLUE_A, BLUE_D)
        self.playw(FadeIn(gil_text))  # 그 중에서도 GIL
        self.playw(
            gil_text.animate.scale(1.5), run_time=3
        )  # 들을 일이 없는 단어라서요..
        self.playw(gil_text.animate.set_color(PURE_RED))  # 정신을 못차리게 만드는

        self.wait()

        get_thread = lambda c: Text(f"Thread {c}", font_size=18, color=GREEN)
        threads = VGroup(*[get_thread(i) for i in ["↘", "→", "↗"]]).arrange(
            DOWN, buff=0.1
        )
        threads[0].set_opacity(0.3)
        threads[-1].set_opacity(0.3)

        test_code = PythonCode("src/code.py")
        threads.next_to(test_code.code[0], LEFT, buff=0.5)
        self.playw(
            LaggedStart(
                gil_text.animate.shift(RIGHT * 10), FadeIn(test_code), lag_ratio=0.3
            )
        )  # 대충 설명하면은요
        self.playw(
            FadeIn(threads),
        )
        self.playw(
            threads.animate.next_to(test_code.code[1], LEFT, buff=0.5),
        )
        self.playw(
            threads.animate.next_to(test_code.code[3], LEFT, buff=0.5),
        )  # 파이썬이 느리다, 뭐 이런 내용입니다

        # 그래서 GIL을 공부하고 나면은요
        self.playw(
            test_code.animate.shift(RIGHT * 15),
            threads.animate.shift(RIGHT * 15),
            run_time=2,
        )


class multiprocessing(Scene3D):
    def construct(self):
        mcode = PythonCode("src/multip.py").scale(0.7)
        mcode.code[:6].set_opacity(0.3)
        self.playw(FadeIn(mcode))
        processpool = mcode.text_slice(7, "ProcessPoolExecutor()")
        num_processes = 3
        tilt_degree = 45
        processes = (
            VGroup(*[process(f"process {i}") for i in range(num_processes)])
            .arrange(DOWN, buff=0.5)
            .rotate(-tilt_degree * DEGREES, axis=UP)
            .next_to(mcode, RIGHT, buff=1)
            .shift(UP)
        )
        processpool.save_state()
        processpool.set_color(PURE_GREEN)
        self.move_camera_horizontally(
            tilt_degree,
            zoom=0.9,
            added_anims=[
                FadeIn(p, target_position=processpool, scale=0.1) for p in processes
            ]
            + [Restore(processpool), mcode.animate.shift(LEFT * 2.5)],
        )
        fncode = mcode.code[2:4]
        multifns = VGroup(
            *[fncode.copy().set_opacity(0.1) for i in range(num_processes)]
        )
        multifns.generate_target()
        for i, f in enumerate(multifns.target):
            f.rotate(-tilt_degree * DEGREES, UP).move_to(processes[i]).scale(
                1.3
            ).set_opacity(1)

        self.playw(MoveToTarget(multifns))

        def single_seq(n):
            sequence = []
            i_n = Text(f"{n}", font_size=24, color=GREEN_D).move_to(
                mcode.text_slice(8, "n", 3)
            )
            i_n.generate_target()
            i_n.target.move_to(multifns[n % num_processes][0][-3]).rotate(
                -tilt_degree * DEGREES, UP
            )
            sequence.append(MoveToTarget(i_n))
            result = (
                Text(f"{n} * {n}", font_size=24)
                .rotate(-tilt_degree * DEGREES, axis=UP)
                .move_to(multifns[n % num_processes][1][-2])
            )
            result.generate_target()
            result.target.become(mcode.text_slice(9, "future"))
            sequence.append(AnimationGroup(FadeOut(i_n), MoveToTarget(result)))
            sequence.append(FadeOut(result))
            return sequence

        sequences = [single_seq(i) for i in range(10)]
        anims = SkewedAnimations(*sequences)
        for anim in anims:
            self.play(anim)
        self.wait()

        process_texts = [processes[i][1][:-1] for i in range(num_processes)]
        for p in process_texts:
            p.generate_target()
            p.target.become(
                Text("Thread", font_size=24, color=YELLOW)
                .rotate(-tilt_degree * DEGREES, UP)
                .move_to(p)
                .align_to(p, LEFT)
            )
        self.play(LaggedStart(*[Indicate(p) for p in process_texts], lag_ratio=0.3))
        self.playw(*[MoveToTarget(p) for p in process_texts])


def process(text: str, text_color=GREY_B):
    box = RoundedRectangle(
        height=2, width=2 * 16 / 9, corner_radius=0.3, color=GREY_B, stroke_width=3
    )
    t = (
        Text(text, font_size=24, color=text_color)
        .next_to(box, UP, buff=0.1)
        .align_to(box, LEFT)
    )

    return VGroup(box, t)


class preprocess(Scene2D):
    def construct(self):
        c = PythonCode("src/example.py")
        c.code.set_opacity(0.3)
        self.playw(FadeIn(c))

        self.play(c.code[0].animate.set_opacity(1))
        self.playw(c.code[1].animate.set_opacity(1))

        self.playw(c.code[3].animate.set_opacity(1))

        self.playw(c.code[5].animate.set_opacity(1))

        hl1, hl1_out = c.highlight(2, color=PURE_RED)
        hl2, hl2_out = c.highlight(6, color=PURE_RED)

        self.playw(hl1, hl2, run_time=6)

        iobound1 = Text("I/O bound", font_size=28, color=YELLOW).next_to(
            c.code[1], buff=1.05
        )
        iobound2 = Text("I/O bound", font_size=28, color=YELLOW).next_to(
            c.code[-1][-1], buff=2.4
        )
        self.playw(FadeIn(iobound1, iobound2, shift=RIGHT))


class iobound(Scene2D):
    def construct(self):
        c = PythonCode("src/example.py")
        code = (
            VGroup(c.code[1][4:], c.code[3][4:], c.code[5][4:])
            .arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            .scale(0.75)
        )
        get_code = lambda: code.copy()
        num_threads = 3
        threads = VGroup(
            *[process(f"thread {i}", text_color=GREY_C) for i in range(num_threads)]
        ).arrange(RIGHT, buff=0.5)

        codes = VGroup(*[get_code().move_to(threads[i][0]) for i in range(num_threads)])
        self.addw(threads, codes)

        yellow = Text("Yellow: No GIL", font_size=32, color=YELLOW)
        red = Text("Red: Under GIL", font_size=32, color=PURE_RED)
        notes = (
            VGroup(yellow, red)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .shift(UP * 2.5)
        )

        self.playw(FadeIn(notes))

        self.play(
            LaggedStart(
                Write(codes[0][2].copy().set_color(YELLOW), run_time=4),
                Succession(
                    Write(codes[1][0].copy().set_color(YELLOW), run_time=1),
                    Write(codes[1][1].copy().set_color(PURE_RED), run_time=1),
                    Write(Dot().set_opacity(0), run_time=1.2),
                    Write(codes[1][2].copy().set_color(YELLOW), run_time=4),
                ),
                Succession(
                    Write(codes[2][0].copy().set_color(YELLOW), run_time=1),
                    Write(Dot().set_opacity(0), run_time=0.5),
                    Write(codes[2][1].copy().set_color(PURE_RED), run_time=1),
                    Write(Dot().set_opacity(0), run_time=0.15),
                    Write(codes[2][2].copy().set_color(YELLOW), run_time=4),
                ),
                lag_ratio=0.1,
            )
        )


class sequenceiobound(Scene2D):
    def construct(self):
        c = PythonCode("src/example.py")
        code = VGroup(c.code[1][4:], c.code[3][4:], c.code[5][4:]).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT
        )
        codecont = (
            CodeText("do_something()", color=GREY_B)
            .next_to(code[-1], DOWN)
            .align_to(code[-1], LEFT)
        )
        singlethread = process("Single thread", text_color=GREY_C).scale(1.5)
        self.addw(singlethread, code, codecont)

        self.play(
            Write(piui := code[0].copy().set_color(YELLOW), run_time=2),
        )
        self.play(
            AnimationGroup(
                Write(ppiui := code[1].copy().set_color(PURE_RED), run_time=0.5),
                FadeOut(piui),
            ),
        )
        self.play(
            AnimationGroup(
                Write(pppiui := code[2].copy().set_color(YELLOW), run_time=4),
                FadeOut(ppiui),
            ),
        )
        self.play(
            AnimationGroup(
                Write(ppppiui := codecont.copy().set_color(PURE_RED), run_time=2),
                FadeOut(pppiui),
            )
        )

        self.playw(FadeOut(ppppiui))


class outro(Scene2D):
    def construct(self):
        code = PythonCode("src/cpubound.py").code

        num_threads = 3
        threads = VGroup(
            *[process(f"thread {i}", text_color=GREY_C) for i in range(num_threads)]
        ).arrange(RIGHT, buff=0.5)
        codes = VGroup(
            *[code.copy().scale(0.9).move_to(threads[i][0]) for i in range(num_threads)]
        )
        self.addw(threads, codes)

        order = [c[i] for i in range(num_threads) for c in codes]
        for i, o in enumerate(order):
            executed = o.copy().set_color(PURE_RED)
            anims = [Write(executed)]
            if i > 0:
                anims.append(FadeOut(old))
            self.play(*anims, run_time=0.3)
            old = executed
        self.play(FadeOut(old))
        self.wait()
