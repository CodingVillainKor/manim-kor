from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)

class intro(Scene2D):
    def construct(self):
        after = PythonCode("src/after1.py")
        before = PythonCode("src/before1.py").align_to(after, LEFT)
        self.playw(FadeIn(before))
        self.cf.save_state()
        self.playw(self.cf.animate.scale(2.5).move_to(before))
        self.play(Restore(self.cf))
        self.playw(
            Transform(
                before.frame, after.frame, replace_mobject_with_target_in_scene=True
            ),
            Transform(
                before.code[:-1],
                after.code[:-1],
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                before.code[-1],
                after.code[-1],
                replace_mobject_with_target_in_scene=True,
            ),
        )

        after.generate_target()
        after.target.code.set_opacity(0.2)
        [line[-1].set_color(YELLOW).set_opacity(1) for line in after.target.code[:4]]
        self.playw(MoveToTarget(after))
        self.playw(FadeOut(after))

        annotation_code = PythonCode("src/annotation.py")
        self.playw(FadeIn(annotation_code))
        annotation_code.generate_target()
        annotation_code.target.code.set_opacity(0.2)
        shap_idx1 = annotation_code.find_text(1, "# This is a simple string.")
        annotation_code.target.code[0][shap_idx1[0] : shap_idx1[1]].set_color(
            GREEN
        ).set_opacity(1)
        annotation_code.target.code[1].set_color(GREEN).set_opacity(1)
        self.playw(MoveToTarget(annotation_code))
        hl, hl_out = annotation_code.highlight(2)
        self.playw(hl, run_time=0.8)

        self.playw(FadeOut(annotation_code), hl_out)

        error_code = PythonCode("src/backslash_shap.py")
        annot = error_code.text_slice(1, r"# This is greeting.").set_opacity(0)
        self.playw(FadeIn(error_code))
        self.playw(annot.animate.set_opacity(1))
        error = error_code.find_text(1, r"\# This is greeting.")
        error_code.generate_target()
        error_code.target.code.set_opacity(0.2)
        error_code.target.code[0][error[0] : error[1]].set_color(PURE_RED).set_opacity(
            1
        )
        self.playw(MoveToTarget(error_code))


class importInDef(Scene2D):
    def construct(self):
        code = PythonCode("src/imdef.py")
        code[0].set_color(WHITE)
        code[0].set_fill(opacity=0)
        code.code[-2:].set_opacity(0)
        code.code.set_z_index(1)

        self.playw(FadeIn(code))

        global_os = PythonCode("src/example.py").shift(RIGHT * 16).set_opacity(0)
        self.playw(self.cf.animate.move_to(global_os), global_os.animate.set_opacity(1))
        self.playw(
            global_os.code[0]
            .animate.scale(1.3)
            .set_color(PURE_GREEN)
            .align_to(global_os.code[0], LEFT)
        )
        self.playw(self.cf.animate.move_to(ORIGIN))
        self.playw_return(
            code[0]
            .animate.set_color(YELLOW)
            .set_opacity(1)
            .scale(1.2)
            .set_fill(opacity=0),
            code.code[1].animate.set_color(YELLOW).scale(1.3),
        )

        self.playw(code.code[-2:].animate.set_opacity(1))
        self.playw(
            *[
                item.animate.scale(1.2).set_color(YELLOW).align_to(item, LEFT)
                for item in [code.code[0], code.code[1], code.code[3]]
            ],
            code.code[-2:].animate.set_opacity(0.2),
        )


class checkNum(Scene2D):
    def construct(self):
        string1 = CodeText('"123"', font_size=28)
        string2 = CodeText('"piui"', font_size=28)
        strings = VGroup(string1, string2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.playw(FadeIn(string1, string2))
        string1_numeric = CodeText(
            "number? True", font_size=28, color=PURE_GREEN
        ).next_to(string1, buff=0.5)
        string2_numeric = CodeText(
            "number? False", font_size=28, color=PURE_RED
        ).next_to(string2, buff=0.5)
        self.playw(
            LaggedStart(
                FadeIn(string1_numeric, shift=RIGHT),
                FadeIn(string2_numeric, shift=RIGHT),
                lag_ratio=0.5,
            )
        )
        int_string1 = CodeText("int(", font_size=28, color=YELLOW).next_to(
            string1, LEFT
        ), CodeText(")", font_size=28, color=YELLOW).next_to(string1, RIGHT)
        int_string2 = CodeText("int(", font_size=28, color=YELLOW).next_to(
            string2, LEFT
        ), CodeText(")", font_size=28, color=YELLOW).next_to(string2, RIGHT)
        self.playw(
            FadeOut(string1_numeric, string2_numeric),
            FadeIn(*int_string1, *int_string2),
        )
        self.playw(
            Transform(
                string1[1:-1],
                CodeText("123", font_size=28, color=GREEN).move_to(string1),
            ),
            FadeOut(*int_string1, string1[0], string1[-1])
        )
        self.playw(
            FadeTransform(
                VGroup(string2, *int_string2),
                error:=CodeText("ERROR", font_size=28, color=PURE_RED).move_to(string2),
            )
        )