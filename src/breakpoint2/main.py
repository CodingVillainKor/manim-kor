from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        buzz_code = PythonCode("print_buzz.py", add_line_numbers=False)

        self.play(FadeIn(buzz_code.frame))
        code2 = buzz_code.code[2]
        code2[-1].save_state()
        code2[-1].align_to(code2[9], LEFT)
        code2[9:-1].set_opacity(0)
        self.playw(
            LaggedStart(
                *[FadeIn(buzz_code.code[i]) for i in range(len(buzz_code.code))],
                lag_ratio=0.3,
            )
        )
        self.playw(
            VGroup(*[buzz_code.code[i] for i in [0, 3, 6]]).animate.set_opacity(0.3)
        )

        self.playw(
            LaggedStart(
                code2[-1].animate.align_to(code2[17], LEFT),
                AnimationGroup(
                    Succession(
                        buzz_code.code[3][5:14].animate.set_opacity(1),
                        buzz_code.code[3][5:14].animate.set_opacity(0.3),
                    ),
                    code2[9:17].animate.set_opacity(1),
                ),
                lag_ratio=0.5,
            )
        )

        self.playw(
            LaggedStart(
                Restore(code2[-1]),
                AnimationGroup(
                    Succession(
                        buzz_code.code[3][17:24].animate.set_opacity(1),
                        buzz_code.code[3][17:24].animate.set_opacity(0.3),
                    ),
                    code2[:-1].animate.set_opacity(1),
                ),
                lag_ratio=0.25,
            )
        )
        buzz_code.save_state()
        self.playw(
            buzz_code.code[2].animate.set_color(PURE_RED),
            buzz_code.code[4].animate.set_color(PURE_RED),
        )
        self.playw(
            Restore(buzz_code),
        )
        self.wait()

        bp = PythonCode("bp.py", add_line_numbers=False)
        bp.code[4].set_opacity(0)
        VGroup(*[bp.code[i] for i in [0, 3, -1]]).set_opacity(0.3)
        self.playw(Transform(buzz_code, bp, replace_mobject_with_target_in_scene=True))
        self.playw(
            bp.code[2]
            .animate.scale(1.5)
            .align_to(bp.code[2], LEFT)
            .align_to(bp.code[2], DOWN),
            run_time=3,
        )


class advanced(Scene3D):
    def construct(self):
        code = PythonCode("adv.py", add_line_numbers=False).scale(0.75).shift(UP * 0.6)
        self.playw(FadeIn(code))
        self.playw_return(code.code[6:].animate.set_opacity(0.2), run_time=2)

        self.playw(code.code[6:].animate.set_opacity(0.3))
        bp = code.code[2]
        bp.save_state()
        fn2_4 = code.text_slice(4, "fn2")
        fn2_8 = code.text_slice(8, "fn2")
        self.play(
            bp.animate.next_to(fn2_4, UP, buff=0),
            rate_func=rate_functions.rush_into,
            run_time=0.7,
        )
        fn2_4.save_state()
        fn2_8.save_state()
        fn2_4.set_color(PURE_RED).scale(1.3)
        fn2_8.set_color(PURE_RED).scale(1.3).set_opacity(1)
        self.playw(
            Restore(bp),
            Restore(fn2_4),
            Restore(fn2_8),
            rate_func=rate_functions.rush_from,
            run_time=0.7,
        )

        bp.save_state()
        main_13 = code.text_slice(13, "main")
        fn1_15 = code.text_slice(15, "fn1")
        self.play(
            bp.animate.next_to(main_13, UP, buff=0),
            FadeOut(code.code[7:11]),
            rate_func=rate_functions.rush_into,
            run_time=0.7,
        )
        main_13.save_state()
        fn1_15.save_state()
        main_13.set_color(PURE_RED).scale(1.3).set_opacity(1)
        fn1_15.set_color(PURE_RED).scale(1.3).set_opacity(1)
        self.playw(
            Restore(bp),
            Restore(main_13),
            Restore(fn1_15),
            FadeIn(code.code[7:11]),
            rate_func=rate_functions.rush_from,
            run_time=0.7,
        )


class bud(Scene3D):
    def construct(self):
        code = PythonCode("adv.py", add_line_numbers=False).scale(0.75).shift(UP * 0.6)
        self.addw(code)

        self.move_camera_horizontally(
            45, zoom=0.9, added_anims=[code.animate.shift(LEFT * 2 + IN)]
        )

        c = lambda x: CodeText(x, font_size=24, color=MINT).rotate(-45 * DEGREES, UP)
        command1 = c("(pdb) b fn2").next_to(code.code[2], RIGHT, buff=0.75)
        self.playw(FadeIn(command1, shift=RIGHT))
        self.playw(Indicate(code.code[7]))

        command2 = c("(pdb) c").next_to(code.code[2], RIGHT, buff=0.75)
        self.playw(
            Transform(
                command1[:3], command2[:3], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                command1[3:], command2[3:], replace_mobject_with_target_in_scene=True
            ),
        )
        fn2code = code.code[7:11]
        self.play(fn2code.animate.shift(OUT * 5))

        fn2line = DashedLine(
            code.text_slice(4, "fn2").get_bottom(),
            fn2code[0][4:6].get_top(),
            color=GREY_B,
            stroke_width=2,
        )
        self.playw(Create(fn2line), run_time=1)
        fn1fn2 = VGroup(code.code[:6], fn2code, fn2line)
        command3 = (
            c("(pdb) print(v)").next_to(fn2code[1], RIGHT, buff=1.5).shift(DOWN * 0.1)
        )
        command3[5:].set_opacity(0)
        self.playw(FadeIn(command3, shift=RIGHT), FadeOut(command2))
        self.playw(command3[5:].animate.set_opacity(1))

        self.playw(Indicate(code.code[2]))
        self.play(
            Create(
                cline := fn2line.copy().set_stroke(width=6).set_color(PURE_GREEN),
                run_time=1,
            )
        )
        fn2code.save_state()
        self.play(FadeOut(cline), fn2code.animate.set_color(YELLOW))
        self.playw(Restore(fn2code))
        self.playw(Indicate(command3))

        command4 = c("(pdb) u").move_to(command3).align_to(command3, LEFT)
        self.playw(
            Transform(
                command3[:5], command4[:5], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                command3[5:], command4[5:], replace_mobject_with_target_in_scene=True
            ),
        )

        self.playw(
            command4[:5].animate.next_to(code.code[3], RIGHT, buff=0.75),
            command4[5:].animate.next_to(code.code[3], RIGHT, buff=0.75).set_opacity(0),
        )

        command5 = (
            c("(pdb) print(h)")
            .move_to(command4)
            .align_to(command4, LEFT)
            .shift(RIGHT * 0.4)
        )
        self.playw(
            Transform(
                command4[:5], command5[:5], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                command4[5:], command5[5:], replace_mobject_with_target_in_scene=True
            ),
        )

        command6 = c("(pdb) d").move_to(command4).align_to(command4, LEFT)
        self.playw(
            Transform(
                command5[:5], command6[:5], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                command5[5:], command6[5:], replace_mobject_with_target_in_scene=True
            ),
        )
        self.playw(
            command6[:5]
            .animate.next_to(fn2code[1], RIGHT, buff=0.75)
            .shift(DOWN * 0.1),
            command6[5:]
            .animate.next_to(fn2code[1], RIGHT, buff=0.75)
            .shift(DOWN * 0.1)
            .set_opacity(0),
        )
