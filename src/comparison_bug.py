from manim import *

class ConsolasText(Text):
    def __init__(self, text, **kwargs):
        kwargs["font"] = "Consolas"
        if "color" not in kwargs:
            kwargs["color"] = BLUE_A
        super().__init__(text, **kwargs)


class Bug1(Scene):
    def construct(self):
        text_buf = 2.0

        falsea1 = ConsolasText("False")
        dequala = ConsolasText("==").next_to(falsea1, RIGHT*text_buf)
        falsea2 = ConsolasText("False").next_to(dequala, RIGHT*text_buf)
        textain = ConsolasText("in").next_to(falsea2, RIGHT*text_buf)
        falsea3 = ConsolasText("[False]").next_to(textain, RIGHT*text_buf)
        first_line = [falsea1, dequala, falsea2, textain, falsea3]
        first_line_group = VGroup(*first_line).move_to(ORIGIN)
        rectde = Rectangle(color=YELLOW_B).surround(dequala, buff=MED_LARGE_BUFF)
        rectin = Rectangle(color=YELLOW_B).surround(textain, buff=MED_LARGE_BUFF*1.3)

        self.play(FadeIn(first_line_group))
        self.wait()
        self.play(Write(rectde))
        self.wait()
        self.play(LaggedStart(FadeOut(rectde), Write(rectin), lag_ratio=0.5, run_time=1.5))
        self.wait()
        self.play(FadeOut(rectin))
        self.play(first_line_group.animate.shift(UP*3))
        self.wait()


        falseb1 = ConsolasText("(False")
        dequalb = ConsolasText("==").next_to(falseb1, RIGHT*text_buf)
        falseb2 = ConsolasText("False)").next_to(dequalb, RIGHT*text_buf)
        textbin = ConsolasText("in").next_to(falseb2, RIGHT*text_buf)
        falseb3 = ConsolasText("[False]").next_to(textbin, RIGHT*text_buf)
        second_line = [falseb1, dequalb, falseb2, textbin, falseb3]
        second_line_group = VGroup(*second_line).move_to(ORIGIN)

        paren_group = VGroup(falseb1, dequalb, falseb2)
        trueb1 = ConsolasText("True", color=BLUE_D).move_to(paren_group)
        final_group = VGroup(trueb1, textbin, falseb3)
        final_false = ConsolasText("False", color=YELLOW_C).move_to(final_group)

        
        self.play(FadeIn(second_line_group))
        self.wait()
        self.play(Transform(paren_group, trueb1, replace_mobject_with_target_in_scene=True))
        self.wait()
        self.play(trueb1.animate.shift(RIGHT*2))
        self.wait()
        self.play(trueb1.animate.set_color(RED_E), falseb3.animate.set_color(RED_E))
        self.wait()
        self.play(Transform(final_group, final_false, replace_mobject_with_target_in_scene=True))
        self.wait()

        summary_text = ConsolasText(" == -> in :", color=YELLOW_C).scale(0.7).next_to(first_line_group, DOWN*2.5).shift(LEFT*2)
        rectde = Rectangle(color=YELLOW_B).surround(dequala, buff=MED_LARGE_BUFF)
        rectin = Rectangle(color=YELLOW_B).surround(textain, buff=MED_LARGE_BUFF*1.3)
        self.play(Write(summary_text))
        self.wait()
        self.play(Write(rectde), run_time=0.5)
        self.play(LaggedStart(FadeOut(rectde), Write(rectin), lag_ratio=0.5, run_time=1.0))
        self.play(FadeOut(rectin), run_time=0.5)
        self.wait(0.5)
        self.play(final_false.animate.next_to(summary_text, RIGHT))
        self.wait()

        falsec1 = ConsolasText("False")
        dequalc = ConsolasText("==").next_to(falsec1, RIGHT*text_buf)
        falsec2 = ConsolasText("(False").next_to(dequalc, RIGHT*text_buf)
        textcin = ConsolasText("in").next_to(falsec2, RIGHT*text_buf)
        falsec3 = ConsolasText("[False])").next_to(textcin, RIGHT*text_buf)
        third_line = [falsec1, dequalc, falsec2, textcin, falsec3]
        third_line_group = VGroup(*third_line).move_to(ORIGIN)

        paren_group = VGroup(falsec2, textcin, falsec3)
        truec1 = ConsolasText("True", color=BLUE_D).move_to(paren_group)
        final_group = VGroup(falsec1, dequalc, truec1)
        final_false2 = ConsolasText("False", color=GREEN_C).move_to(final_group)


        self.play(FadeIn(third_line_group))
        self.wait()
        self.play(Transform(paren_group, truec1, replace_mobject_with_target_in_scene=True))
        self.wait()
        self.play(truec1.animate.shift(LEFT*2))
        self.wait()
        self.play(truec1.animate.set_color(RED_E), falsec1.animate.set_color(RED_E))
        self.wait()
        self.play(Transform(final_group, final_false2, replace_mobject_with_target_in_scene=True))
        self.wait()

        summary_text2 = ConsolasText(" in -> == :", color=GREEN_C).scale(0.7).next_to(summary_text, DOWN*2.5)
        self.play(Write(summary_text2))
        self.wait()
        self.play(Write(rectin), run_time=0.5)
        self.play(LaggedStart(FadeOut(rectin), Write(rectde), lag_ratio=0.5, run_time=1.0))
        self.play(FadeOut(rectde), run_time=0.5)
        self.wait(0.5)
        self.play(final_false2.animate.next_to(summary_text2, RIGHT))
        self.wait()
        self.clear_all()
        self.wait()

        falseb1 = ConsolasText("(False", color=YELLOW_D)
        dequalb = ConsolasText("==", color=YELLOW_D).next_to(falseb1, RIGHT*text_buf)
        falseb2 = ConsolasText("False)", color=YELLOW_D).next_to(dequalb, RIGHT*text_buf)
        textbin = ConsolasText("in", color=YELLOW_D).next_to(falseb2, RIGHT*text_buf)
        falseb3 = ConsolasText("[False]", color=YELLOW_D).next_to(textbin, RIGHT*text_buf)
        second_line = [falseb1, dequalb, falseb2, textbin, falseb3]
        second_line_group = VGroup(*second_line).next_to(first_line_group, DOWN*3).scale(0.7)
        falsec1 = ConsolasText("False", color=GREEN_D)
        dequalc = ConsolasText("==", color=GREEN_D).next_to(falsec1, RIGHT*text_buf)
        falsec2 = ConsolasText("(False", color=GREEN_D).next_to(dequalc, RIGHT*text_buf)
        textcin = ConsolasText("in", color=GREEN_D).next_to(falsec2, RIGHT*text_buf)
        falsec3 = ConsolasText("[False])", color=GREEN_D).next_to(textcin, RIGHT*text_buf)
        third_line = [falsec1, dequalc, falsec2, textcin, falsec3]
        third_line_group = VGroup(*third_line).next_to(second_line_group, DOWN*2).scale(0.7)
        total_group = VGroup(first_line_group, second_line_group, third_line_group).move_to(ORIGIN)
        self.play(Write(total_group))
        self.wait()
        self.play(Transform(second_line_group, ConsolasText("False", color=YELLOW_D).scale(0.7).move_to(second_line_group)))
        self.wait(0.5)
        self.play(Transform(third_line_group, ConsolasText("False", color=GREEN_D).scale(0.7).move_to(third_line_group)))
        self.wait()
        self.play(Transform(first_line_group, ConsolasText("False").move_to(first_line_group)))
        self.wait(1)

        self.clear_all()
        self.wait(3)

        numt1 = ConsolasText("3 < num < 7").move_to(ORIGIN)
        numt2 = VGroup(
            (nt21 := ConsolasText("3 < num")), 
            (nt22 := ConsolasText("and", color=GREEN)).next_to(nt21, RIGHT*2),
            (nt23 := ConsolasText("num < 7")).next_to(nt22, RIGHT*2)).move_to(ORIGIN)
        self.play(FadeIn(numt1))
        self.wait()
        self.play(Transform(numt1, numt2), run_time=0.5)
        self.wait()
        self.clear_all()

        deq = ConsolasText("a == 3")
        tin = ConsolasText("a in [1, 2, 3]").next_to(deq, DOWN*2)
        deqtin = VGroup(deq, tin).move_to(ORIGIN)
        self.play(Write(deq))
        self.wait()
        self.play(Write(tin))
        self.wait(3)

        self.clear_all()

        falsea1 = ConsolasText("False")
        dequala = ConsolasText("==").next_to(falsea1, RIGHT*text_buf)
        falsea2 = ConsolasText("False").next_to(dequala, RIGHT*text_buf)
        textain = ConsolasText("in").next_to(falsea2, RIGHT*text_buf)
        falsea3 = ConsolasText("[False]").next_to(textain, RIGHT*text_buf)
        first_line = [falsea1, dequala, falsea2, textain, falsea3]
        first_line_group = VGroup(*first_line).move_to(ORIGIN)
        rectde = Rectangle(color=YELLOW_B).surround(dequala, buff=MED_LARGE_BUFF)
        rectin = Rectangle(color=YELLOW_B).surround(textain, buff=MED_LARGE_BUFF*1.3)

        self.play(FadeIn(first_line_group))
        self.wait()
        self.play(Write(rectde))
        self.wait()
        self.play(LaggedStart(FadeOut(rectde), Write(rectin), lag_ratio=0.5, run_time=1.5))
        self.wait()
        self.play(FadeOut(rectin))
        self.wait()

        real_text1 = ConsolasText("False == False")
        and_text = ConsolasText("and", color=GREEN).next_to(real_text1, RIGHT*2)
        real_text2 = ConsolasText("False in [False]").next_to(and_text, RIGHT*2)
        real_final = VGroup(real_text1, and_text, real_text2).move_to(ORIGIN)

        self.play(Transform(first_line_group, real_final, replace_mobject_with_target_in_scene=True))
        self.wait()
        self.play(Transform(real_text1, (real_true1:=ConsolasText("True")).move_to(real_text1), replace_mobject_with_target_in_scene=True))
        self.wait()
        self.play(Transform(real_text2, (real_true2:=ConsolasText("True")).move_to(real_text2), replace_mobject_with_target_in_scene=True))
        self.wait()

        final = VGroup(real_true1, and_text, real_true2)
        final_true = ConsolasText("True", color=PURE_BLUE).move_to(ORIGIN).scale(2).shift(UP)
        self.play(Transform(final, final_true, replace_mobject_with_target_in_scene=True))
        self.wait()

        falseb1 = ConsolasText("(False", color=YELLOW_D)
        dequalb = ConsolasText("==", color=YELLOW_D).next_to(falseb1, RIGHT*text_buf)
        falseb2 = ConsolasText("False)", color=YELLOW_D).next_to(dequalb, RIGHT*text_buf)
        textbin = ConsolasText("in", color=YELLOW_D).next_to(falseb2, RIGHT*text_buf)
        falseb3 = ConsolasText("[False]", color=YELLOW_D).next_to(textbin, RIGHT*text_buf)
        second_line = [falseb1, dequalb, falseb2, textbin, falseb3]
        second_line_group = VGroup(*second_line).next_to(final_true, DOWN*3).scale(0.7)
        falsec1 = ConsolasText("False", color=GREEN_D)
        dequalc = ConsolasText("==", color=GREEN_D).next_to(falsec1, RIGHT*text_buf)
        falsec2 = ConsolasText("(False", color=GREEN_D).next_to(dequalc, RIGHT*text_buf)
        textcin = ConsolasText("in", color=GREEN_D).next_to(falsec2, RIGHT*text_buf)
        falsec3 = ConsolasText("[False])", color=GREEN_D).next_to(textcin, RIGHT*text_buf)
        third_line = [falsec1, dequalc, falsec2, textcin, falsec3]
        third_line_group = VGroup(*third_line).next_to(second_line_group, DOWN*1.2).scale(0.7)
        total_group = VGroup(second_line_group, third_line_group)
        self.play(Write(total_group))
        self.wait()
        self.play(Transform(second_line_group, ConsolasText("False", color=YELLOW_D).scale(0.7).move_to(second_line_group)), run_time=0.6)
        self.play(Transform(third_line_group, ConsolasText("False", color=GREEN_D).scale(0.7).move_to(third_line_group)), run_time=0.6)
        self.wait()

    def clear_all(self):
        self.play(*[FadeOut(item) for item in self.mobjects])







        