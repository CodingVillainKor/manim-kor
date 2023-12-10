from manim import *

class NumText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, font="Consolas", width=0.3, **kwargs)
    
    @property
    def num(self):
        return float(self.text)

def NumBox(text, text_config={}, box_config={}):
    text = NumText(text, **text_config)
    rect = Square(**box_config).surround(text)
    return VGroup(text, rect)

class LinearAndSquare(MovingCameraScene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 30],
            x_length=6,
            y_length=5,
            tips=False,
            axis_config={"include_ticks":False}
        )

        graphx = ax.plot(
            lambda x: 2*x,
            color=PURE_GREEN,
            x_range=[0, 5.0, 0.01],
            use_smoothing=False,
        )
        texx = MathTex("O(N)", color=PURE_GREEN).next_to(graphx).shift(UP)

        graphx2 = ax.plot(
            lambda x: x*x,
            color=PURE_RED,
            x_range=[0, 5.0, 0.01],
            use_smoothing=False,
        )
        texx2 = MathTex("O(N^2)", color=PURE_RED).next_to(graphx2).shift(UP).shift(UP)

        self.play(Write(ax))
        self.play(Write(graphx), Write(graphx2))
        self.play(Write(texx), Write(texx2))



    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class Addition(MovingCameraScene):
    def construct(self):
        num1 = VGroup(NumText("3"), NumText("1"), NumText("4"), NumText("1"), NumText("5")).arrange(RIGHT)
        num2 = VGroup(NumText("2"), NumText("7"), NumText("1"), NumText("8"), NumText("2")).arrange(RIGHT).next_to(num1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        num3 = VGroup(NumText("5", color=PURE_GREEN), NumText("8", color=PURE_GREEN), NumText("5", color=PURE_GREEN), NumText("9", color=PURE_GREEN), NumText("7", color=PURE_GREEN)).arrange(RIGHT).next_to(num2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        VGroup(num1, num2, num3).move_to(ORIGIN)
        line = Line(start=(num2.get_left()[0], num2[0].get_bottom()[1], 0), end=(num2.get_right()[0], num2[0].get_bottom()[1], 0)).next_to(num2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
        self.playw(Write(num1))
        self.playw(Write(num2))
        self.playw(Write(line))

        mathsymbol_add = Tex("$+$").next_to(num2, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)
        mathsymbol_mul = Tex("$\\times$").move_to(mathsymbol_add)
        
        self.playw(FadeIn(mathsymbol_add))
        for i in reversed(range(len(num1))):
            self.touch_and_return(num1[i], num2[i])
            self.playw(FadeIn(num3[i], scale=2))

        #self.playw(FadeIn(mathsymbol_mul))

    def touch_and_return(self, src, tgt):
        src.generate_target()
        src.save_state()
        src.target.next_to(tgt, UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.1)
        self.play(MoveToTarget(src), run_time=0.5)
        self.play(src.animate.restore(), run_time=0.5)


    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class Multiply(MovingCameraScene):
    def construct(self):
        left_coeff = 0.75
        num1 = VGroup(NumText("3"), NumText("1"), NumText("4"), NumText("1"), NumText("5")).arrange(RIGHT)
        num2 = VGroup(NumText("2"), NumText("7"), NumText("1"), NumText("8"), NumText("2")).arrange(RIGHT).next_to(num1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        num3 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "135910"]).arrange(RIGHT).next_to(num2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2).align_to(num2, RIGHT)
        num4 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "27182"] ).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).align_to(num3[-2], RIGHT)
        num5 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "108728"]).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).align_to(num4[-2], RIGHT)
        num6 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "27182"] ).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).align_to(num5[-2], RIGHT)
        num7 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "81546"] ).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).align_to(num6[-2], RIGHT)
        layers = [num3, num4, num5, num6, num7]
        num_result = VGroup(*[NumText(c, color=PURE_GREEN) for c in "853922530"]).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN).align_to(num3[-1], RIGHT)
        VGroup(num1, num2, num3, num4, num5, num6, num7, num_result).move_to(ORIGIN)
        self.play(self.camera.frame.animate.set(width=self.camera.frame_width*1.5), run_time=0.1)
        line = Line(start=(num2.get_left()[0], num2[0].get_bottom()[1], 0), end=(num2.get_right()[0], num2[0].get_bottom()[1], 0)).next_to(num2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
        line2 = Line(start=(num7.get_left()[0], num7[0].get_bottom()[1], 0), end=(num2.get_right()[0], num7[0].get_bottom()[1], 0)).shift(DOWN*0.3)
        self.playw(Write(num1))
        self.playw(Write(num2))
        self.playw(Write(line))
        
        mathsymbol_mul = Tex("$\\times$").next_to(num2, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)
        
        self.playw(FadeIn(mathsymbol_mul))
        for i in reversed(range(len(num1))):
            for j in reversed(range(len(num2))):
                straight_idx = len(num2)-j-1 # 0, 1, 2, ...
                self.touch_and_return(num1[i], num2[j])
                self.playw(FadeIn(layers[len(num1)-i-1][-1-straight_idx], scale=2), wait=0.2)
            if len(num2) < len(layers[len(num1)-i-1]):
                self.playw(FadeIn(layers[len(num1)-i-1][0], scale=2), wait=0.2)
        self.playw(Write(line2))
        self.playw(FadeIn(num_result))

    def touch_and_return(self, src, tgt):
        src.generate_target()
        src.save_state()
        src.target.next_to(tgt, UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.1)
        self.play(MoveToTarget(src), run_time=0.5)
        self.play(src.animate.restore(), run_time=0.5)


    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class MultiplyTooMuch(MovingCameraScene):
    def construct(self):
        left_coeff = 0.75
        num1 = VGroup(*[NumText(c) for c in str(31415926535897950288419716939937510582097494459230781640628620899862803482534)]).arrange(RIGHT)
        num2 = VGroup(*[NumText(c) for c in str(27182818284590452353602874713526624977572470936999595749669676277240766303535)]).arrange(RIGHT).next_to(num1, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        num3 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "108731273138361809414411498854106499910289883747998382998678705108963065214140"]).arrange(RIGHT).next_to(num2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2).align_to(num2, RIGHT)
        num4 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "1902797279921328"] ).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).align_to(num3[-2], RIGHT)
        num5 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "108728"]).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).align_to(num4[-2], RIGHT)
        num6 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "27182"] ).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).align_to(num5[-2], RIGHT)
        num7 = VGroup(*[NumText(c, color=PURE_GREEN) for c in "81546"] ).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).align_to(num6[-2], RIGHT)
        layers = [num3, num4, num5, num6, num7]
        num_result = VGroup(*[NumText(c, color=PURE_GREEN) for c in "853922530"]).arrange(RIGHT).move_to(num3).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN*0.7).shift(DOWN).align_to(num3[-1], RIGHT)
        VGroup(num1, num2, num3, num4, num5, num6, num7, num_result).move_to(ORIGIN)
        self.play(self.camera.frame.animate.set(width=self.camera.frame_width*1.5), run_time=0.1)
        self.play(self.camera.frame.animate.move_to(num2.get_right()), run_time=0.1)
        line = Line(start=(num2.get_left()[0], num2[0].get_bottom()[1], 0), end=(num2.get_right()[0], num2[0].get_bottom()[1], 0)).next_to(num2, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
        line2 = Line(start=(num7.get_left()[0], num7[0].get_bottom()[1], 0), end=(num2.get_right()[0], num7[0].get_bottom()[1], 0)).shift(DOWN*0.3)
        self.playw(Write(num1))
        self.playw(Write(num2))
        self.playw(Write(line))
        
        mathsymbol_mul = Tex("$\\times$").next_to(num2, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)
        
        self.playw(FadeIn(mathsymbol_mul))
        for i in reversed(range(len(num1))):
            for j in reversed(range(len(num2))):
                straight_idx = len(num2)-j-1 # 0, 1, 2, ...
                self.touch_and_return(num1[i], num2[j])
                self.playw(FadeIn(layers[len(num1)-i-1][-1-straight_idx], scale=2), wait=0.2)
            break
            # if len(num2) < len(layers[len(num1)-i-1]):
            #     self.playw(FadeIn(layers[len(num1)-i-1][0], scale=2), wait=0.2)
        # self.playw(Write(line2))
        # self.playw(FadeIn(num_result))

    def touch_and_return(self, src, tgt):
        src.generate_target()
        src.save_state()
        src.target.next_to(tgt, UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.1)
        self.play(MoveToTarget(src), run_time=0.5)
        self.play(src.animate.restore(), run_time=0.5)


    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

def get_open_par():
    return Tex("$($")

def get_close_par_times_3():
    return Tex("$) \\times 3$")

class Karatsuba(MovingCameraScene):
    def construct(self):
        num1, num2 = 1972, 1121
        self.sceneA(num1, num2)
        self.clear()
        self.sceneB(num1, num2)
        self.clear()
        self.sceneC()

    def sceneA(self, num1, num2):
        # multiplying two number, and decomposition by 100_coefficient
        tnum1 = Tex(f"{{{num1//100}}}", f"{{{num1%100}}}")
        tnum2 = Tex(f"{{{num2//100}}}", f"{{{num2%100}}}").next_to(tnum1, DOWN)
        VGroup(tnum1, tnum2).move_to(ORIGIN)

        mathsymbol_mul = Tex("$\\times$").next_to(tnum2, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5)

        self.playw(FadeIn(tnum1))
        self.playw(FadeIn(tnum2))
        self.playw(FadeIn(mathsymbol_mul))

        a1, a0 = Tex(f"{{{num1//100}}}", color=YELLOW_C), Tex(f"{{{num1%100}}}", color=YELLOW_C)
        amul100 = Tex(f"$\\times 100\\quad+$", font_size=DEFAULT_FONT_SIZE*0.6)
        agroup = VGroup(a1, amul100, a0).arrange(RIGHT)
        b1, b0 = Tex(f"{{{num2//100}}}", color=YELLOW_C), Tex(f"{{{num2%100}}}", color=YELLOW_C)
        bmul100 = Tex(f"$\\times 100\\quad+$", font_size=DEFAULT_FONT_SIZE*0.6)
        bgroup = VGroup(b1, bmul100, b0).arrange(RIGHT).next_to(agroup, DOWN)
        VGroup(agroup, bgroup).move_to(ORIGIN)
        self.playw(TransformMatchingTex(tnum1, agroup))
        self.playw(TransformMatchingTex(tnum2, bgroup), mathsymbol_mul.animate.shift(LEFT))
        
        mul_of_the_two = VGroup(agroup, bgroup, mathsymbol_mul)
        self.playw(mul_of_the_two.animate.shift(UP).shift(UP))

        # start of "Time complexity is still N^2"
        a1_, b1_ = a1.copy(), b1.copy()
        a1_.generate_target()
        b1_.generate_target()
        a1b1mul = Tex("$\\times$")
        a1b1mul1002 = Tex(f"$\\times 100^2\\quad+$", font_size=DEFAULT_FONT_SIZE*0.6)
        a1b1group = VGroup(a1_.target, a1b1mul, b1_.target, a1b1mul1002).arrange(RIGHT)

        a0_100, b1_100 = a0.copy(), b1.copy()
        a1_100, b0_100 = a1.copy(), b0.copy()
        a0_100.generate_target()
        b1_100.generate_target()
        a1_100.generate_target()
        b0_100.generate_target()
        a0b1mul = Tex("$\\times$")
        a0b1a1b0add = Tex("$+$")
        a1b0mul = Tex("$\\times$")
        a0b1mul100 = Tex(f"$\\times 100\\quad+$", font_size=DEFAULT_FONT_SIZE*0.6)
        a0b1a1b0_open  = Tex("$($")
        a0b1a1b0_close = Tex("$)$")
        reducedgroup = VGroup(a0b1a1b0_open,
                              a0_100.target,
                              a0b1mul,
                              b1_100.target,
                              a0b1a1b0add,
                              a1_100.target,
                              a1b0mul,
                              b0_100.target,
                              a0b1a1b0_close,
                              a0b1mul100).arrange(RIGHT).move_to(ORIGIN)

        a0_1, b0_1 = a0.copy(), b0.copy()
        a0_1.generate_target()
        b0_1.generate_target()
        a0b0mul = Tex("$\\times$")
        a0b0group = VGroup(a0_1.target, a0b0mul, b0_1.target).arrange(RIGHT)

        decomposed_group = VGroup(a1b1group, reducedgroup, a0b0group).arrange(RIGHT).move_to(ORIGIN)
        self.playw(MoveToTarget(a1_), MoveToTarget(b1_), FadeIn(a1b1mul))
        self.playw(Write(a1b1mul1002))
        self.playw(FadeIn(a0b1a1b0_open), FadeIn(a0b1mul), FadeIn(a0b1a1b0add), FadeIn(a1b0mul), FadeIn(a0b1a1b0_close), FadeIn(a0b1mul100))
        self.playw(MoveToTarget(a0_100), MoveToTarget(b1_100))
        self.playw(MoveToTarget(a1_100), MoveToTarget(b0_100))
        self.playw(MoveToTarget(a0_1), MoveToTarget(b0_1), FadeIn(a0b0mul))

        muls = [decomposed_group[0][:3], decomposed_group[1][1:4], decomposed_group[1][5:8], decomposed_group[2]]
        rects_surround_muls = [Rectangle(color=GREEN_B).surround(mul) for mul in muls]
        halfns = [Tex("$N \\over 2$", "$\\times$", "$N \\over 2 $").next_to(rect, DOWN) for rect in rects_surround_muls]
        halfns_ns4 = [Tex("$N^2 \\over 4$").next_to(rect, DOWN) for rect in rects_surround_muls]
        for r, h in zip(rects_surround_muls, halfns):
            self.playw(Write(r))
            self.playw(Write(h))
        self.playw(*[FadeTransform(halfns[i], halfns_ns4[i]) for i in range(len(halfns))])
        nsquare = Tex("$N^2$").align_to(halfns[0], DOWN)
        self.playw(FadeTransform(VGroup(*halfns_ns4), nsquare))
        self.playw(FadeOut(nsquare))

        # end of "Time complexity is still N^2", re-define groups
        a1b1group = VGroup(a1_, a1b1mul, b1_, a1b1mul1002)
        reducedgroup = VGroup(a0b1a1b0_open,
                        a0_100,
                        a0b1mul,
                        b1_100,
                        a0b1a1b0add,
                        a1_100,
                        a1b0mul,
                        b0_100,
                        a0b1a1b0_close,
                        a0b1mul100)
        a0b0group = VGroup(a0_1, a0b0mul, b0_1)
        decomposed_group = VGroup(a1b1group, reducedgroup, a0b0group)

        # start of "Solution key"
        self.playw(FadeOut(mul_of_the_two), FadeOut(VGroup(*rects_surround_muls)))
        self.playw(decomposed_group.animate.shift(UP).shift(UP))

        z0 = decomposed_group[0].copy() # 10000
        z1 = decomposed_group[1][:-1].copy() # 100
        z2 = decomposed_group[2].copy() # 1
        z0.generate_target(); z1.generate_target(); z2.generate_target()
        z1_add_z2 = Tex("$+$")
        z1_mul100 = Tex(f"$\\times 100$", font_size=DEFAULT_FONT_SIZE*0.6)
        VGroup(z0.target, z2.target, z1_add_z2, z1.target, z1_mul100).arrange(RIGHT).move_to(ORIGIN)
        self.playw(MoveToTarget(z0))
        self.playw(MoveToTarget(z2), FadeIn(z1_add_z2))
        self.playw(MoveToTarget(z1), FadeIn(z1_mul100), FadeOut(decomposed_group))
        rect_buf = 0.2
        z1_box = Rectangle(color=PURE_GREEN, width=z1.width+rect_buf, height=z1.height+rect_buf).move_to(z1)
        self.playw(FadeIn(z1_box))

        z1_a1, z1_a0 = z1[5].copy(), z1[1].copy()
        z1_b1, z1_b0 = z1[3].copy(), z1[7].copy()
        z0_new = z0[:-1].copy()
        z2_new = z2.copy()
        z0_new.generate_target(); z2_new.generate_target()
        sol = VGroup((new_first := VGroup(Tex("$($"), z1_a1, Tex("$+$"), z1_a0, Tex("$)$")).arrange(RIGHT)), 
                     (new_second :=Tex("$\\times$")), 
                     (new_third := VGroup(Tex("$($"), z1_b1, Tex("$+$"), z1_b0, Tex("$)$")).arrange(RIGHT)),
                     (new_fourth := Tex("$-$")),
                     (new_fifth := VGroup(Tex("$($"), z0_new.target, Tex("$+$"), z2_new.target, Tex("$)$")).arrange(RIGHT))).arrange(RIGHT).scale(0.7).next_to(z1_box, UP)
        
        self.playw(FadeIn(new_first))
        self.playw(FadeIn(new_second))
        self.playw(FadeIn(new_third))
        self.playw(FadeIn(new_fourth))
        self.playw(FadeIn(new_fifth[::2]))
        self.playw(MoveToTarget(z0_new))
        self.playw(MoveToTarget(z2_new))
        self.playw(FadeOut(z1_box))
        new_fifth[1], new_fifth[3] = z0_new, z2_new

        mul_z0 = z0[:-1]
        mul_z2 = z2
        mul_sol = sol[:3]
        rect_z0 = Rectangle(color=RED_C, width=mul_z0.width+rect_buf, height=mul_z0.height+rect_buf).move_to(mul_z0)
        rect_z2 = Rectangle(color=RED_C, width=mul_z2.width+rect_buf, height=mul_z2.height+rect_buf).move_to(mul_z2)
        rect_sol = Rectangle(color=RED_C, width=mul_sol.width+rect_buf, height=mul_sol.height+rect_buf).move_to(mul_sol)
        self.playw(Write(rect_z0))
        self.playw(Write(rect_z2))
        self.playw(Write(rect_sol))

        # end of "Solution key"

    def sceneB(self, num1, num2):
        original_On = Tex("$N^2$")
        decomposed_On = Tex("$\\frac { {N^2} }{ {4} } \\times 4 $")
        reduced_On = Tex("$\\frac { {N^2} }{ {4} } \\times 3 $")
        VGroup(original_On, decomposed_On, reduced_On).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3).move_to(ORIGIN)
        
        self.playw(FadeIn(original_On))
        self.playw(FadeIn(decomposed_On))
        self.playw(FadeIn(reduced_On))

        On2_1, On2_2, On2_3 = Tex("$O(N^2)$"), Tex("$O(N^2)$"), Tex("$O(N^2)$")
        On2_1.move_to(original_On)
        On2_2.move_to(decomposed_On)
        On2_3.move_to(reduced_On)

        self.playw(FadeTransform(original_On, On2_1))
        self.playw(FadeTransform(decomposed_On, On2_2))
        self.playw(FadeTransform(reduced_On, On2_3))

    def sceneC(self):
        start = Tex(r"${ N }\quad \times \quad { N }$")
        N2_times_N2 = Tex("$\\frac{ {N} } { {2} }$", "$\\quad \\times \\quad $", "$\\frac{ {N} } { {2} }$")
        N4_times_N4 = Tex("$\\frac{ {N} } { {4} }$", "$\\quad \\times \\quad $", "$\\frac{ {N} } { {4} }$")
        N8_times_N8 = Tex("$\\frac{ {N} } { {8} }$", "$\\quad \\times \\quad $", "$\\frac{ {N} } { {8} }$")
        first_cover = VGroup(get_open_par().next_to(N2_times_N2, LEFT), get_close_par_times_3().next_to(N2_times_N2, RIGHT))
        second_cover = VGroup(get_open_par().next_to(first_cover[0], LEFT), get_close_par_times_3().next_to(first_cover[1], RIGHT))
        third_cover = VGroup(get_open_par().next_to(second_cover[0], LEFT), get_close_par_times_3().next_to(second_cover[1], RIGHT))

        last_group = VGroup(N8_times_N8, first_cover, second_cover, third_cover)
        normalized = Tex(r"$\frac{ N } { 2^k }$", r"$\quad \times \quad $", r"$\frac{ N } { 2^k }$", r"$\quad \times 3^k$").move_to(third_cover)
        normalized[0][3].set_fill(color=PURE_GREEN)
        normalized[2][3].set_fill(color=PURE_GREEN)
        normalized[3][2].set_fill(color=PURE_GREEN)

        normalized2 = Tex(r"$\frac{ N } { 2^{\lceil \log_2{N} \rceil} }$", r"$\quad \times \quad $", r"$\frac{ N } { 2^{\lceil \log_2{N} \rceil} }$", r"$\quad \times 3^{\lceil \log_2{N} \rceil}$").move_to(third_cover)
        normalized2[0][3:10].set_fill(color=PURE_GREEN)
        normalized2[2][3:10].set_fill(color=PURE_GREEN)
        normalized2[3][2:9].set_fill(color=PURE_GREEN)

        normalized3 = Tex(r"$\frac{ N } { \approx N }$", r"$\quad \times \quad $", r"$\frac{ N } { \approx N }$", r"$\quad \times 3^k$").move_to(third_cover)
        normalized3[0][3].set_fill(color=PURE_GREEN)
        normalized3[2][3].set_fill(color=PURE_GREEN)

        normalized4 = Tex(r"$\frac{ N } { \approx N }$", r"$\quad \times \quad $", r"$\frac{ N } { \approx N }$", r"$\quad \times 3^{\log_2{N}}$").move_to(third_cover)
        normalized4[3][2:7].set_fill(color=PURE_GREEN)

        self.playw(FadeIn(start))
        self.playw(FadeTransform(start, N2_times_N2), FadeIn(first_cover), self.camera.frame.animate.move_to(first_cover))
        self.playw(TransformMatchingShapes(N2_times_N2, N4_times_N4), FadeIn(second_cover), self.camera.frame.animate.move_to(second_cover))
        self.playw(TransformMatchingShapes(N4_times_N4, N8_times_N8), FadeIn(third_cover), self.camera.frame.animate.move_to(third_cover))
        self.playw(FadeTransform(last_group, normalized))
        self.playw(FadeTransform(normalized, normalized2))
        self.playw(FadeTransform(normalized2, normalized3))
        self.playw(TransformMatchingTex(normalized3, normalized4))
        normalized4[3][2:7].set_fill(color=WHITE)
        self.playw(FadeOut(normalized4[:3]), FadeOut(normalized4[-1][0]), self.camera.frame.animate.move_to(normalized4[-1]))

        changed = Tex(r"$N^{\log_2{3}}$").move_to(normalized4[-1][1:])
        last = Tex(r"$N^{1.58}$").move_to(normalized4[-1][1:])
        Oopen = Tex(r"$O($").scale(0.8).next_to(last, LEFT)
        close = Tex(r"$)$").scale(0.8).next_to(last, RIGHT)
        self.playw(TransformMatchingShapes(normalized4[-1][1:], changed))
        self.playw(TransformMatchingShapes(changed, last), FadeIn(Oopen), FadeIn(close))

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])