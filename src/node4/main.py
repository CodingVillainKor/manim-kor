from manim import *
from manimdef import DefaultManimClass, PythonCode, BrokenLine


class ResnetEq(DefaultManimClass):
    def construct(self):
        eq = MathTex(
            "y", "=", "x", "+", r"\operatorname{module}", "(", r"x", ")", font_size=48
        ).set_opacity(0.3)
        VGroup(eq[-4:-2], eq[-1]).set_color(GREEN)
        paper_eq = MathTex(
            r"h_{t+1}",
            "=",
            r"h_t",
            "+",
            "f(",
            r"h_t",
            ",",
            r"\theta_t" ")",
            font_size=48,
        ).next_to(eq, UP)
        VGroup(paper_eq[-4], paper_eq[-2:]).set_color(GREEN)
        self.playw(FadeIn(eq))

        nump = NumberPlane()
        x = MathTex("x", font_size=36).move_to(nump.c2p(0, 1.8))
        y = MathTex("y", font_size=36).move_to(nump.c2p(0, -1.8))
        model = Rectangle(height=0.9, width=1.6, color=GREY_A).set_fill(
            GREEN, opacity=0.3
        )
        linein = Line(nump.c2p(0, 1.5), model.get_top(), stroke_width=2)
        lineout = Arrow(
            model.get_bottom(),
            nump.c2p(0, -1.5),
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        lineu = Line(nump.c2p(0, 1), nump.c2p(-2, 1), stroke_width=2)
        linel = Line(nump.c2p(-2, 1), nump.c2p(-2, -1), stroke_width=2)
        lined = Arrow(
            nump.c2p(-2, -1),
            nump.c2p(0, -1),
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        resline = VGroup(lineu, linel, lined)
        inoutline = VGroup(linein, lineout)
        VGroup(x, y, resline, inoutline, model).shift(RIGHT * 5)
        self.playw(FadeIn(x, y, inoutline, model), self.cf.animate.shift(RIGHT * 5))
        self.playw(FadeIn(resline))

        eqc = eq.copy().set_color(PURE_GREEN)
        paper_eqc = paper_eq.copy()
        self.playw(eq.animate.set_opacity(1), self.cf.animate.shift(LEFT * 5))
        self.playw(FadeIn(paper_eq))
        self.playw_return(
            Transform(paper_eqc[0], eqc[0], replace_mobject_with_target_in_scene=True),
            wait=0,
        )
        self.remove(eqc[0])
        self.wait()
        self.playw_return(
            Transform(
                VGroup(paper_eqc[2], paper_eqc[5]),
                piui := VGroup(eqc[2], eqc[6]),
                replace_mobject_with_target_in_scene=True,
            ),
            wait=0,
        )
        self.remove(piui)
        self.wait()
        self.playw_return(
            Transform(
                VGroup(paper_eqc[4], paper_eqc[6:]),
                piui := VGroup(eqc[4:6], eqc[-1]),
                replace_mobject_with_target_in_scene=True,
            ),
            wait=0,
        )
        self.remove(piui)
        self.wait()


class ResnetT(DefaultManimClass):
    def construct(self):
        eq = MathTex(
            "y", "=", "x", "+", r"\operatorname{module}", "(", r"x", ")", font_size=48
        )
        VGroup(eq[-4:-2], eq[-1]).set_color(GREEN)
        paper_eq = MathTex(
            r"h_{t+1}",
            "=",
            r"h_t",
            "+",
            "f(",
            r"h_t",
            ",",
            r"\theta_t",
            ")",
            font_size=48,
        ).next_to(eq, UP)
        VGroup(paper_eq[-5], paper_eq[-3:]).set_color(GREEN)

        self.addw(eq, paper_eq)
        self.playw(self.cf.animate.scale(0.7))
        paper_eq.save_state()
        self.playw(
            Flash(paper_eq[0][1:].get_top(), line_length=0.1),
            Flash(paper_eq[2][-1].get_top(), line_length=0.1),
            Flash(paper_eq[5][-1].get_top(), line_length=0.1),
            Flash(paper_eq[-2][-1].get_top(), line_length=0.1),
            VGroup(
                paper_eq[0][:1],
                paper_eq[1],
                paper_eq[2][:-1],
                paper_eq[3:5],
                paper_eq[5][:-1],
                paper_eq[6],
                paper_eq[-2][:-1],
                paper_eq[-1],
            ).animate.set_opacity(0.3),
            eq.animate.set_opacity(0.3),
        )
        self.playw(Restore(paper_eq), FadeOut(eq), self.cf.animate.move_to(paper_eq))


class DepthIsContinuous(DefaultManimClass):
    def construct(self):
        nump = NumberPlane()
        x = MathTex("x", font_size=40).move_to(nump.c2p(0, 1.8))
        h1 = MathTex("h_1", font_size=36).move_to(nump.c2p(0, -1.8))
        h2 = MathTex("h_2", font_size=36).move_to(nump.c2p(0, -5.2))
        model1 = Rectangle(height=1.2, width=1.6, color=GREY_C).set_fill(
            GREEN, opacity=0.3
        )
        line1in = Line(nump.c2p(0, 1.5), model1.get_top(), stroke_width=2)
        line1out = Arrow(
            model1.get_bottom(),
            nump.c2p(0, -1.5),
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        line1u = Line(nump.c2p(0, 1), nump.c2p(-1.5, 1), stroke_width=2)
        linelr = Line(nump.c2p(-1.5, 1), nump.c2p(-1.5, -1), stroke_width=2)
        line1d = Arrow(
            nump.c2p(-1.5, -1),
            nump.c2p(0, -1),
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        resline1 = VGroup(line1u, linelr, line1d)
        inoutline1 = VGroup(line1in, line1out)

        model2 = (
            Rectangle(height=1.2, width=1.6, color=GREY_C)
            .set_fill(GREEN, opacity=0.3)
            .move_to(nump.c2p(0, -3.5))
        )

        line2in = Line(nump.c2p(0, -2), model2.get_top(), stroke_width=2)
        line2out = Arrow(
            model2.get_bottom(),
            nump.c2p(0, -5),
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.2,
        )
        line2u = Line(nump.c2p(0, -2.5), nump.c2p(-1.5, -2.5), stroke_width=2)
        line2r = Line(nump.c2p(-1.5, -2.5), nump.c2p(-1.5, -4.5), stroke_width=2)
        line2d = Arrow(
            nump.c2p(-1.5, -4.5),
            nump.c2p(0, -4.5),
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        resline2 = VGroup(line2u, line2r, line2d)
        inoutline2 = VGroup(line2in, line2out)
        self.playw(FadeIn(x, h1, resline1, inoutline1, model1))
        self.cf.save_state()
        self.playw(
            FadeIn(h2, resline2, inoutline2, model2),
            self.cf.animate.move_to(line2in).scale(1.2),
        )
        self.playw(
            self.cf.animate.scale(0.7).move_to(ORIGIN),
            FadeOut(h2, resline2, inoutline2, model2),
        )

        model1_scale = lambda x: (0.6 - x) / 1.2  # 0 -> 1
        t = ValueTracker(0.36)  # 0.6 -> -0.6
        tline = (
            get_tl := lambda x: Line(
                nump.c2p(-0.8, x), nump.c2p(0.8, x), stroke_width=3, color=BLUE
            )
        )(t.get_value()).set_opacity(0)
        tt = (
            get_tt := lambda x: MathTex(
                f"h_{{{model1_scale(x):.2f}}}", font_size=36, color=BLUE
            ).next_to(tline, buff=0.1)
        )(t.get_value()).set_opacity(0)

        self.playw(tt.animate.set_opacity(1), tline.animate.set_opacity(1))

        tt.add_updater(lambda x: x.become(get_tt(t.get_value())))
        tline.add_updater(lambda x: x.become(get_tl(t.get_value())))
        self.playw(t.animate.set_value(0.06), run_time=2)  # 0.45
        self.playw(t.animate.set_value(-0.564), run_time=2)  # 0.97


class ODESolverModule(DefaultManimClass):
    def construct(self):
        c = PythonCode("src/odecode.py").scale(0.7).shift(LEFT * 5).set_opacity(0.3)
        tc, xc = c.text_slice(4, "t"), c.text_slice(4, "x")
        c.code[3].set_opacity(1)

        x0_data = (0, [-3, -1, 1, 3])
        xt_data = [
            (1, [-2.5, -0.9, 0.9, 2.5]),
            (2, [-2, -0.7, 0.7, 2]),
            (3, [-2.3, -0.8, 0.8, 2.3]),
            (4, [-2.5, -0.9, 0.9, 2.6]),
        ]
        nump = (
            NumberPlane(x_range=(-4, 4), y_range=(-0.3, 5))
            .scale(0.5)
            .shift(RIGHT * 3 + UP * 0.5)
        )
        set_numl = (
            lambda t: NumberLine(x_range=(-4, 4), tick_size=0)
            .scale(0.5)
            .move_to(nump.c2p(0, t))
        )
        numl = set_numl(x0_data[0])

        x0 = VGroup(*[Dot(numl.n2p(d), color=BLUE) for d in x0_data[1]])
        vt_t = ValueTracker(0)
        set_t = (
            lambda: MathTex(
                "t", "=", f"{float(vt_t.get_value()*0.1):.2f}", font_size=24
            )
            .move_to(nump.c2p(-5, vt_t.get_value()))
            .set_color_by_gradient(TEAL, BLUE)
        )
        t = set_t()
        self.addw(c, x0, t, numl)
        self.playw(
            LaggedStart(
                Flash(tc.get_top(), line_length=0.1),
                Flash(xc.get_top(), line_length=0.1),
                lag_ratio=0.3,
            )
        )
        self.wait(3)
        t.add_updater(lambda x: x.become(set_t()))
        for t_, data in xt_data:
            new_numl = set_numl(t_)
            tcc = set_t()
            self.playw(
                tcc.animate.move_to(tc).scale(0.2).set_opacity(0),
                x0.copy().animate.move_to(xc).scale(0.1).set_opacity(0),
            )
            x = VGroup(*[Dot(new_numl.n2p(d), color=BLUE) for d in data])
            arrows = VGroup(
                *[
                    Arrow(x0[i].get_top(), x[i], buff=0, stroke_width=1)
                    for i in range(len(x))
                ]
            )
            arrows.save_state()
            arrows.move_to(tc).scale(0.1)
            self.playw(Restore(arrows))
            self.play(
                numl.animate.become(new_numl),
                vt_t.animate.set_value(t_),
                x0.animate.become(x),
            )
            self.playw(FadeOut(arrows))


class ResnetVsODESolver(DefaultManimClass):
    def construct(self):
        nump = NumberPlane().shift(LEFT * 3).shift(UP * 0.5).scale(0.9)

        mh, mw = 1, 1.6
        module1 = Rectangle(height=mh, width=mw, color=GREY_A, stroke_width=2).move_to(
            nump.c2p(0, 2)
        )
        module2 = Rectangle(height=mh, width=mw, color=GREY_A, stroke_width=2).move_to(
            nump.c2p(0, 0)
        )
        module3 = Rectangle(height=mh, width=mw, color=GREY_A, stroke_width=2).move_to(
            nump.c2p(0, -2)
        )
        l1 = Arrow(
            nump.c2p(0, 3.5),
            module1.get_top(),
            stroke_width=2,
            color=GREY_A,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        res1 = BrokenLine(
            nump.c2p(0, 3),
            nump.c2p(-1.5, 3),
            nump.c2p(-1.5, 1.1),
            nump.c2p(0, 1.1),
            arrow=True,
            stroke_width=2,
            color=GREY_A,
            max_tip_length_to_length_ratio=0.1,
        )
        l2 = Arrow(
            module1.get_bottom(),
            module2.get_top(),
            stroke_width=2,
            color=GREY_A,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        res2 = BrokenLine(
            nump.c2p(0, 0.9),
            nump.c2p(-1.5, 0.9),
            nump.c2p(-1.5, -0.9),
            nump.c2p(0, -0.9),
            arrow=True,
            stroke_width=2,
            color=GREY_A,
            max_tip_length_to_length_ratio=0.1,
        )
        l3 = Arrow(
            module2.get_bottom(),
            module3.get_top(),
            stroke_width=2,
            color=GREY_A,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        res3 = BrokenLine(
            nump.c2p(0, -1.1),
            nump.c2p(-1.5, -1.1),
            nump.c2p(-1.5, -2.8),
            nump.c2p(0, -2.8),
            arrow=True,
            stroke_width=2,
            color=GREY_A,
            max_tip_length_to_length_ratio=0.1,
        )
        l4 = Arrow(
            module3.get_bottom(),
            nump.c2p(0, -3.5),
            stroke_width=2,
            color=GREY_A,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        module1t = Text("block(x)", font_size=20).move_to(module1)
        module2t = Text("block(x)", font_size=20).move_to(module2)
        module3t = Text("block(x)", font_size=20).move_to(module3)
        module1 = VGroup(module1, module1t)
        module2 = VGroup(module2, module2t)
        module3 = VGroup(module3, module3t)
        lines = VGroup(l1, l2, l3, l4, res1, res2, res3)
        self.playw(
            LaggedStart(
                *[FadeIn(m) for m in [module1, module2, module3, lines]], lag_ratio=0.1
            )
        )
        self.playw(LaggedStart(
            module1[0].animate.set_fill(RED_C, opacity=0.3),
            module2[0].animate.set_fill(GREEN_C, opacity=0.3),
            module3[0].animate.set_fill(BLUE_C, opacity=0.3), lag_ratio=0.2
        ))

        odemodule = Rectangle(height=mh+0.3, width=mw+0.5, color=GREY_A, stroke_width=2).shift(RIGHT*3).set_fill(YELLOW, 0.3)
        odemodulet = Text("block(t, x)", font_size=20).move_to(odemodule)
        odemodule = VGroup(odemodule, odemodulet)
        self.playw(FadeIn(odemodule))
        self.playw(Flash(odemodulet[6], line_length=0.15, color=PURE_RED))

        tx1 = Text("(t, x) = (0, ...)", font_size=24).next_to(odemodule, UP, buff=0.4)
        tx2 = Text("(t, x) = (1, ...)", font_size=24).next_to(tx1, UP)
        tx3 = Text("(t, x) = (2, ...)", font_size=24).next_to(tx2, UP)

        self.play(FadeIn(tx1))
        self.play(FadeIn(tx2))
        self.playw(FadeIn(tx3))
        self.play(FadeOut(tx1, shift=DOWN*0.8, scale=0.5))
        self.play(FadeOut(tx2, shift=DOWN*1.3, scale=0.5))
        self.playw(FadeOut(tx3, shift=DOWN*1.7, scale=0.5))


class WhatIsNFE1(DefaultManimClass):
    def construct(self):
        c = PythonCode("src/odecode.py").scale(0.7).shift(LEFT * 3).set_opacity(0.3)
        tc, xc = c.text_slice(4, "t"), c.text_slice(4, "x")
        c.code[3].set_opacity(1)

        x0_data = (0, [-3, -1, 1, 3])
        xt_data = [
            x0_data,
            (1, [-2.5, -0.9, 0.9, 3.4]),
            (2, [-2.0, -0.7, 0.7, 3.5]),
            (3, [-1.7, -0.5, 0.5, 3.2]),
            (4, [-1.9, -0.9, 0.2, 2.9]),
            (5, [-2.3, -1.7, -0.1, 2.5]),
        ]
        nump = (
            NumberPlane(x_range=(-4, 4), y_range=(-0.3, 5))
            .scale(0.5)
            .shift(RIGHT * 3 + UP * 0.5)
        )
        all_arrows = self.get_all_arrows(nump, xt_data).set_opacity(0.3)
        xt_data.pop(0)
        set_numl = (
            lambda t: NumberLine(x_range=(-4, 4), tick_size=0)
            .scale(0.5)
            .move_to(nump.c2p(0, t))
        )
        numl = set_numl(x0_data[0])

        x0 = VGroup(*[Dot(numl.n2p(d), color=BLUE) for d in x0_data[1]])
        vt_t = ValueTracker(0)
        set_t = (
            lambda: MathTex(
                "t", "=", f"{float(vt_t.get_value()*0.2):.2f}", font_size=24
            )
            .move_to(nump.c2p(-5, vt_t.get_value()))
            .set_color_by_gradient(TEAL, BLUE)
        )
        t = set_t()
        self.addw(c, x0, t, numl)
        tline = DashedVMobject(Arrow(nump.c2p(-3.5, 0), nump.c2p(-3.5, 5), stroke_width=3, buff=0, color=TEAL, max_tip_length_to_length_ratio=0.05))
        deltat = MathTex(r"\Delta", "t", "=", "1", font_size=24, color=TEAL).next_to(tline, LEFT, buff=0.1)
        self.playw(FadeIn(tline), FadeIn(deltat))
        self.playw(FadeIn(all_arrows))
        t.add_updater(lambda x: x.become(set_t()))
        xt_data = [
            (5, [-0.5, -0.5, 0.5, 5.0]),
        ]
        for t_, data in xt_data:
            new_numl = set_numl(t_)
            tcc = set_t()
            self.playw(
                tcc.animate.move_to(tc).scale(0.2).set_opacity(0),
                x0.copy().animate.move_to(xc).scale(0.1).set_opacity(0),
            )
            x = VGroup(*[Dot(new_numl.n2p(d), color=BLUE) for d in data])
            unit_arrow = all_arrows[0].copy().set_opacity(1)
            unit_arrow.save_state()
            unit_arrow.move_to(tc).scale(0.1)
            arrows = VGroup(
                *[
                    Arrow(x0[i].get_top(), x[i], buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.1, color=RED)
                    for i in range(len(x))
                ]
            )
            self.playw(Restore(unit_arrow))
            self.playw(Transform(unit_arrow, arrows, replace_mobject_with_target_in_scene=True))
            self.play(
                numl.animate.become(new_numl),
                vt_t.animate.set_value(t_),
                x0.animate.become(x),
            )
            self.playw(FadeOut(arrows))
            break

    def get_all_arrows(self, nump: NumberPlane, xt_data):
        starts = xt_data[:-1]
        ends = xt_data[1:]
        arrows = []
        for s, e in zip(starts, ends):
            st, et = s[0], e[0]
            sx, ex = s[1], e[1]
            ss = [nump.c2p(x, st) for x in sx]
            es = [nump.c2p(x, et) for x in ex]
            arrows_ = VGroup(*[Arrow(s_, e_, buff=0, stroke_width=1) for s_, e_ in zip(ss, es)])
            arrows.append(arrows_)
        return VGroup(*arrows)
    
class WhatIsNFE2(DefaultManimClass):
    def construct(self):
        c = PythonCode("src/odecode.py").scale(0.7).shift(LEFT * 3).set_opacity(0.3)
        tc, xc = c.text_slice(4, "t"), c.text_slice(4, "x")
        c.code[3].set_opacity(1)

        x0_data = (0, [-3, -1, 1, 3])
        xt_data = [
            x0_data,
            (0.25, [-2.87, -0.99, 0.99, 3.1]),
            (0.50, [-2.75, -0.97, 0.97, 3.2]),
            (0.75, [-2.62, -0.93, 0.93, 3.3]),
            (1.00, [-2.50, -0.9, 0.9, 3.4]),
            (1.25, [-2.38, -0.8, 0.8, 3.42]),
            (1.50, [-2.25, -0.75, 0.75, 3.45]),
            (1.75, [-2.12, -0.73, 0.73, 3.48]),
            (2.00, [-2.00, -0.7, 0.7, 3.5]),
            (2.25, [-1.9, -0.69, 0.69, 3.41]),
            (2.50, [-1.8, -0.67, 0.67, 3.34]),
            (2.75, [-1.75, -0.6, 0.55, 3.27]),
            (3.00, [-1.70, -0.5, 0.5, 3.2]),
            (3.25, [-1.75, -0.49, 0.47, 3.1]),
            (3.50, [-1.80, -0.55, 0.4, 3.03]),
            (3.75, [-1.85, -0.75, 0.3, 2.97]),
            (4.00, [-1.9, -0.9, 0.2, 2.9]),
            (4.25, [-2.0, -1.5, 0.11, 2.8]),
            (4.50, [-2.1, -1.6, 0.02, 2.7]),
            (4.75, [-2.2, -1.65, -0.12, 2.6]),
            (5.00, [-2.3, -1.7, -0.1, 2.5]),
        ]
        nump = (
            NumberPlane(x_range=(-4, 4), y_range=(-0.3, 5))
            .scale(0.5)
            .shift(RIGHT * 3 + UP * 0.5)
        )
        all_arrows = self.get_all_arrows(nump, xt_data).set_opacity(0.3)
        xt_data.pop(0)
        set_numl = (
            lambda t: NumberLine(x_range=(-4, 4), tick_size=0)
            .scale(0.5)
            .move_to(nump.c2p(0, t))
        )
        numl = set_numl(x0_data[0])

        x0 = VGroup(*[Dot(numl.n2p(d), color=BLUE) for d in x0_data[1]])
        vt_t = ValueTracker(0)
        set_t = (
            lambda: MathTex(
                "t", "=", f"{float(vt_t.get_value()*0.2):.2f}", font_size=24
            )
            .move_to(nump.c2p(-5, vt_t.get_value()))
            .set_color_by_gradient(TEAL, BLUE)
        )
        t = set_t()
        self.addw(c, x0, t, numl)
        tline = DashedVMobject(Arrow(nump.c2p(-3.5, 0), nump.c2p(-3.5, 0.5), stroke_width=3, buff=0, color=YELLOW, max_tip_length_to_length_ratio=0.2))
        deltat = MathTex(r"\Delta", "t", "=", "0.05", font_size=24, color=YELLOW).next_to(tline, UP, buff=0.1)
        self.playw(FadeIn(tline), FadeIn(deltat))
        # self.playw(FadeIn(all_arrows))
        t.add_updater(lambda x: x.become(set_t()))
        for i, (t_, data) in enumerate(xt_data):
            new_numl = set_numl(t_)
            tcc = set_t()
            self.play(
                tcc.animate.move_to(tc).scale(0.2).set_opacity(0),
                x0.copy().animate.move_to(xc).scale(0.1).set_opacity(0),
                VGroup(tline, deltat).animate.set_opacity(0)
            )
            x = VGroup(*[Dot(new_numl.n2p(d), color=BLUE) for d in data])
            arrows = VGroup(
                *[
                    Arrow(x0[i].get_center(), x[i].get_center(), buff=0, stroke_width=1, max_tip_length_to_length_ratio=0.2)
                    for i in range(len(x))
                ]
            )
            arrows.save_state()
            arrows.move_to(tc).scale(0.1)
            self.play(Restore(arrows))
            self.play(
                numl.animate.become(new_numl),
                vt_t.animate.set_value(t_),
                x0.animate.become(x),
            )
            self.play(FadeOut(arrows), run_time=0.5)

    def get_all_arrows(self, nump: NumberPlane, xt_data):
        starts = xt_data[:-1]
        ends = xt_data[1:]
        arrows = []
        for s, e in zip(starts, ends):
            st, et = s[0], e[0]
            sx, ex = s[1], e[1]
            ss = [nump.c2p(x, st) for x in sx]
            es = [nump.c2p(x, et) for x in ex]
            arrows_ = VGroup(*[Arrow(s_, e_, buff=0, stroke_width=1) for s_, e_ in zip(ss, es)])
            arrows.append(arrows_)
        return VGroup(*arrows)