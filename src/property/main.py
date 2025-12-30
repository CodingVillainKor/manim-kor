from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        pc = PythonCode("src/intro0.py")
        pi = PythonCode("src/intro1.py").next_to(pc).shift(LEFT * 1.5)
        pi.code[0].set_opacity(0.3)
        pi.text_slice(2, "p.item", exclusive=True).set_opacity(0.3)
        pc.code[:3].set_opacity(0.3)
        pc.code[5:].set_opacity(0.7)
        self.addw(pc)
        self.playw(Indicate(pc.code[4], scale_factor=1.05))

        self.wait(5)

        self.playw(pc.code[5:].animate.set_opacity(1))

        self.play(pc.animate.shift(LEFT * 2))
        self.playw(FadeIn(pi))

        code = VGroup(pc, pi)
        self.playw(code.animate.shift(DOWN).scale(0.9).rotate(-PI / 3, axis=RIGHT))

        why = Text("why?", font_size=40).set_color_by_gradient(RED_A, RED_B).shift(UP)
        code.generate_target().set_opacity(0.3)
        code.target[0].code[4].shift(UP * 0.25).set_opacity(1).rotate(
            PI / 3, axis=RIGHT
        )
        self.playw(FadeIn(why, shift=UP), MoveToTarget(code))


class contextA(Scene3D):
    def construct(self):
        pc = PythonCode("src/contextA0.py").scale(0.8)
        pi = PythonCode("src/contextA1.py")
        VGroup(pc, pi).arrange(RIGHT, buff=0.75).shift(UP * 0.5)
        pc.code[3].set_opacity(0)
        pc.code[:3].set_opacity(0.5)
        pc.code[6:].set_opacity(0.5)
        pi.code[0].set_opacity(0.5)
        pi.text_slice(2, "p.item", exclusive=True).set_opacity(0.5)
        self.addw(pc, pi)
        self.playw(Indicate(pc.code[5], scale_factor=1.02))

        self.playw(Circumscribe(pi.text_slice(2, "p.item"), buff=0.1, stroke_width=2))
        self.play(pc.code[3].animate.set_opacity(1), pc.code[5:].animate.set_opacity(0))
        self.playw(Flash(pc.code[3].get_left()))

        self.play(pc.code[5:].animate.set_opacity(1))
        attr = pc.code[3].copy()
        pro = pc.code[5:].copy()
        self.add(pro, attr)
        self.play(FadeOut(pc, pi), run_time=0.5)
        self.playw(VGroup(attr, pro).animate.scale(1.2).arrange(DOWN, buff=0.75))
        vs = Text("vs", font_size=32, color=GREY_B).move_to(
            VGroup(attr, pro).get_center()
        )
        self.playw(FadeIn(vs, scale=1.3), run_time=0.5)

        tilt = VGroup(attr, pro, vs)
        self.play(
            tilt.animate.set_opacity(0.5).rotate(-PI / 3, axis=RIGHT).shift(DOWN * 0.75)
        )
        msg = (
            Text("1. [외형 ↔ 내부] 차이", font_size=28, font="Noto Serif KR")
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .shift(UP)
        )
        self.playw(FadeIn(msg, shift=UP * 0.5))
        prop = pro[0]
        self.playw(
            prop.animate.set_opacity(1).rotate(PI / 3, axis=RIGHT).shift(UP * 0.25)
        )


class rect(Scene3D):
    def construct(self):
        pc = PythonCode("src/rect0.py").scale(0.8)
        prop = pc.code[5:].set_opacity(0)
        pc.code[:5].set_opacity(0.3)
        pc.code[0].set_opacity(1)
        pi = PythonCode("src/rect1.py").scale(0.7)

        coeff = 0.5
        r1 = Rectangle(height=coeff * 2, width=coeff * 2.5, color=GREY_C)
        r2 = Rectangle(height=coeff * 4, width=coeff * 3, color=GREY_C)
        r = VGroup(r1, r2).arrange(DOWN, buff=0.7)
        VGroup(r, pc, pi).arrange(RIGHT, buff=0.75).shift(UP * 0.5)
        self.play(FadeIn(r))
        self.playw(FadeIn(pc))

        r1h = Line(r1.get_corner(UR), r1.get_corner(DR), color=GREEN_C, stroke_width=8)
        r2h = Line(r2.get_corner(UR), r2.get_corner(DR), color=GREEN_C, stroke_width=8)
        r1w = Line(r1.get_corner(UL), r1.get_corner(UR), color=BLUE_C, stroke_width=8)
        r2w = Line(r2.get_corner(UL), r2.get_corner(UR), color=BLUE_C, stroke_width=8)
        h1t = Text("h", font=MONO_FONT, font_size=24, color=GREEN_C).next_to(
            r1h.get_center(), RIGHT, buff=0.1
        )
        h2t = Text("h", font=MONO_FONT, font_size=24, color=GREEN_C).next_to(
            r2h.get_center(), RIGHT, buff=0.1
        )
        w1t = Text("w", font=MONO_FONT, font_size=24, color=BLUE_C).next_to(
            r1w.get_center(), UP, buff=0.1
        )
        w2t = Text("w", font=MONO_FONT, font_size=24, color=BLUE_C).next_to(
            r2w.get_center(), UP, buff=0.1
        )
        wlines = VGroup(r1w, r2w)
        hlines = VGroup(r1h, r2h)
        pc.generate_target()
        pc.target.code[:5].set_opacity(0.3)
        pc.target.code[2].set_opacity(1)
        self.play(FadeIn(hlines, h1t, h2t), MoveToTarget(pc))
        self.playw(FadeIn(wlines, w1t, w2t), pc.code[3].animate.set_opacity(1))

        self.playw_return(
            r1.animate.set_fill(GREY_C, opacity=0.6),
            r2.animate.set_fill(GREY_C, opacity=0.6),
            run_time=2,
        )

        self.playw(pc.code[4].animate.set_opacity(1))
        self.playw(Indicate(pc.code[4], scale_factor=1.05))

        pi.scale(1.2).next_to(pc, RIGHT, buff=0.5)
        pi.code[:2].set_opacity(0.5)
        pi.code[4:].set_opacity(0)
        self.play(
            FadeIn(pi),
            pc.code[4].animate.set_opacity(0),
            prop[2:].animate.set_opacity(1),
        )
        self.playw(
            pi.text_slice(4, "r1.area()", exclusive=True).animate.set_opacity(0.5),
            pi.text_slice(4, "()").animate.set_color(PURE_RED),
        )
        self.playwl(
            FadeOut(pi.text_slice(4, "()")),
            pi.code[3][-1].animate.move_to(pi.code[3][-3]),
            AnimationGroup(
                prop[2:].animate.set_opacity(0), pc.code[4].animate.set_opacity(1)
            ),
            lag_ratio=0.5,
        )
        self.playw(
            Indicate(pc.code[4], color=RED, scale_factor=1.05),
            Flash(pc.code[4].get_left(), color=RED),
        )

        self.playwl(
            pi.code[4].animate.set_opacity(1),
            Flash(pi.code[4].get_left()),
            lag_ratio=0.4,
        )
        self.playwl(
            pi.code[5].animate.set_opacity(1),
            Flash(pi.code[5].get_left(), color=RED),
            lag_ratio=0.4,
            wait=0.1,
        )
        self.playw(pi.code[5].animate.set_color(RED))

        self.playw(
            Indicate(pi.text_slice(4, "r1.area"), scale_factor=1.05),
            Circumscribe(pi.text_slice(4, "r1.area"), buff=0.1, stroke_width=2),
        )

        self.playw(pc.code[4].animate.set_color(RED))

        self.playw(prop[2:].animate.set_opacity(1), pc.code[4].animate.set_opacity(0))
        self.playwl(
            prop[1].animate.set_opacity(1),
            Flash(prop[1].get_left() + DOWN * 0.3),
            lag_ratio=0.4,
        )
        self.mouse.next_to(pi, RIGHT, buff=2)
        self.play(self.mouse.animate.move_to(pi.code[3][-3].get_bottom()))
        self.playw(Indicate(pi.text_slice(4, "r1.area"), scale_factor=1.05))
        self.play(
            self.mouse.animate.move_to(
                pc.text_slice(8, "def").get_bottom() + DOWN * 0.15
            )
        )
        self.playwl(
            Indicate(prop[2], scale_factor=1.05),
            self.mouse.animate.set_opacity(0),
            lag_ratio=0.2,
        )
        self.play(
            Indicate(pc.text_slice(9, "self.h"), scale_factor=1.1),
            Indicate(pc.code[2], scale_factor=1.1),
        )
        self.playw_return(
            Indicate(pc.text_slice(9, "self.w"), scale_factor=1.1),
            Indicate(pc.code[3], scale_factor=1.1),
        )


class readonly(Scene3D):
    def construct(self):
        pc = PythonCode("src/contextA0.py").scale(0.8)
        attr = pc.code[3].copy()
        pro = pc.code[5:].copy()
        vs = Text("vs", font_size=32, color=GREY_B).move_to(
            VGroup(attr, pro).get_center()
        )
        ground = VGroup(attr, vs, pro).arrange(DOWN, buff=0.75).scale(1.2)
        pro.shift(UP * 0.75)
        ground.rotate(-PI / 3, axis=RIGHT).shift(DOWN).set_opacity(0.3)
        pro[0].rotate(PI / 3, axis=RIGHT).shift(UP * 0.25).set_opacity(1)
        self.addw(ground)

        msg = (
            Text("2. 읽기 전용 속성", font_size=28, font="Noto Serif KR")
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .shift(UP)
        )
        self.playw(FadeIn(msg, shift=UP * 0.5))

        self.playw(msg.animate.scale(1.2), run_time=3, rate_func=linear)

        self.play(FadeOut(msg, ground), run_time=0.5)
        pc = PythonCode("src/readonly0.py").scale(0.9)
        pi = PythonCode("src/readonly1.py").scale(0.9)
        VGroup(pc, pi).arrange(RIGHT, buff=0.75).shift(UP * 0.5)
        pc.code[:4].set_opacity(0.5)
        pi.code[:2].set_opacity(0.5)
        pi.code[2:].set_opacity(0)
        self.playw(FadeIn(pc, pi))
        self.mouse.next_to(pc.code[6], LEFT, buff=3)
        self.play(
            self.mouse.animate.move_to(pc.code[6].get_bottom() + LEFT + DOWN * 0.1)
        )
        self.playwl(
            Indicate(pc.code[6], scale_factor=1.05),
            self.mouse.animate.set_opacity(0),
            lag_ratio=0.2,
        )
        self.playw(pi.code[3].animate.set_opacity(1))
        area_arr = Arrow(
            pi.code[3].get_left(),
            pc.code[6].get_right(),
            buff=0.1,
            color=GREY_B,
            stroke_width=3,
            tip_length=0.2,
        )
        self.playw(GrowArrow(area_arr))
        area_arr.generate_target().rotate(PI / 2, about_point=area_arr.get_end()).shift(
            UL * 5 + LEFT * 4
        ).set_color(PURE_RED)
        area_arr.set_color(PURE_RED)
        self.playw(MoveToTarget(area_arr), rate_func=rush_from)

        self.play(pi.code[4].animate.set_opacity(1))
        check = Text("✔", color=GREEN, font_size=24).next_to(pi.code[4], RIGHT)
        x = Text("✘", color=RED, font_size=24).next_to(pi.code[3], RIGHT)
        self.playw(FadeIn(check))

        self.playw(pi.code[3].animate.set_color(RED), FadeIn(x))

        area_arr = Arrow(
            pi.code[3].get_left(),
            pc.code[6].get_right(),
            buff=0.1,
            color=GREY_B,
            stroke_width=3,
            tip_length=0.2,
        )
        self.play(GrowArrow(area_arr), run_time=2)
        area_arr.generate_target().rotate(PI / 2, about_point=area_arr.get_end()).shift(
            UL * 5 + LEFT * 4
        ).set_color(PURE_RED)
        area_arr.set_color(PURE_RED)
        self.playw(MoveToTarget(area_arr), rate_func=rush_from)
