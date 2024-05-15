from manim import *
from manimdef import DefaultManimClass

class Requirements(DefaultManimClass):
    def construct(self):
        self.sceneA()
        self.sceneB()

    def sceneA(self):
        cond_bayes = "p(x \mid y)"
        joint_bayes = "p(x, y)"
        y_bayes = "p(y)"
        bayes = MathTex(cond_bayes, "=", "{", joint_bayes, "\\over", y_bayes, "}", font_size=36)
        
        redundant_mc = "q(x_t \mid x_{t-1}, x_{t-2}, x_0)"
        compact_mc = "q(x_t \mid x_{t-1})"
        mc = MathTex(redundant_mc, "=", compact_mc, font_size=36)

        requirements = VGroup(bayes, mc).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10)
        self.playw(Write(bayes), Write(mc))
        bayesc = bayes.copy().set_color(YELLOW)
        self.playw(mc.animate.set_opacity(0.4), self.camera.frame.animate.move_to(bayes), FadeIn(bayesc, scale=1.1))

        mcc = mc.copy().set_color(YELLOW).set_opacity(1.0)
        self.playw(self.camera.frame.animate.move_to(mc), mc.animate.set_opacity(1.0), FadeIn(mcc, scale=1.1), FadeOut(bayes), bayesc.animate.set_color(WHITE).set_opacity(0.4), FadeOut(mc))
        mc.set_opacity(1.0)
        self.playw(self.camera.frame.animate.move_to(ORIGIN), FadeOut(mcc), FadeIn(mc), bayesc.animate.set_opacity(1.0))
        bayes = bayesc

        self.playw(mc.animate.shift(UP).shift(UP).shift(UP*1.5).scale(0.7), bayes.animate.shift(UP).shift(UP).shift(UP*1.5).scale(0.7))
        self.mc = mc
        self.bayes = bayes

    def sceneB(self):
        e = r"\mathbb{E}_q"
        llbracket = r"["
        prior = r"-\log p(x_T)"
        msig = (r"-\sum", r"_{t \geq 1}", r"^T")
        msiglog = r"\log"
        nom = [r"p_{\theta}(", r"x_{t-1}|x_t", r")"]
        denom = [r"q(", r"x_t|x_{t-1}", r")"]
        frac = self.frac(nom, denom)
        rrbracket = r"]"
        tex_exp1 = (e, llbracket, prior, *msig, msiglog, *frac, rrbracket)
        expectation1 = MathTex(*tex_exp1)
        self.playw(Write(expectation1))

        msig2 = (r"-\sum", r"_{t > 1}", r"^T")
        msig2log = r"-\log"
        nom2 = (r"p_{\theta}(", r"x_0|x_1", r")")
        denom2 = (r"q(", r"x_1|x_0", r")")
        frac2 = self.frac(nom2, denom2)
        tex_exp2 = (e, llbracket, prior, *msig2, msiglog, *frac, rrbracket)
        tex_exp3 = (e, llbracket, prior, *msig2, msiglog, *frac, msig2log, *frac2, rrbracket)
        expectation2 = MathTex(*tex_exp2)
        expectation3 = MathTex(*tex_exp3)
        expectation2[4][1:].set_color(PURE_GREEN)
        expectation2[5].set_color(PURE_GREEN)
        expectation3[4][1:].set_color(PURE_GREEN)
        expectation3[5].set_color(PURE_GREEN)
        expectation3[-12:-1].set_color(PURE_GREEN)
        self.playw(TransformMatchingTex(expectation1, expectation2, key_map={msig: msig2}, transform_mismatches=True))
        self.playw(TransformMatchingTex(expectation2, expectation3, transform_mismatches=True))

        self.playw(
            expectation3[4][1:].animate.set_color(WHITE),
            expectation3[5].animate.set_color(WHITE),
            expectation3[-12:-1].animate.set_color(WHITE),
        )
        self.playw(expectation3.animate.shift(UP).shift(UP).scale(0.7))

        nom4 = (r"q( ", r"x_{t-1}|x_0 ", r" )")
        denom4 = (r"q( ", r"x_t|x_0", r" )")
        frac4 = ["{", *nom4, r"\over ", *denom4, "}"]
        denom5 = (r"q(", r"x_{t-1}|x_t, x_0", r" )")
        frac5 = self.frac(nom, denom5)
        sigmadot = r"\cdot"
        tex_exp4 = (e, llbracket, prior, *msig2, msiglog, *frac5, sigmadot, *frac4, msig2log, *frac2, rrbracket)
        expectation4 = MathTex(*tex_exp4, font_size=36)
        self.playw(TransformMatchingTex(expectation3.copy(), expectation4))

        self.playw(
            expectation3[:12].animate.set_opacity(0.5),
            expectation3[15:].animate.set_opacity(0.5),
            expectation4[:12].animate.set_opacity(0.5),
            expectation4[25:].animate.set_opacity(0.5),
            expectation3[12:15].animate.set_color(YELLOW),
            expectation4[12:25].animate.set_color(YELLOW),
        )
        self.playw(FadeOut(expectation4))

        core_str1 = r"q(", r"x_t", r"|", r"x_{t-1}", r")"
        core_q1 = MathTex(*core_str1).next_to(expectation3, DOWN)
        self.playw(FadeIn(core_q1, scale=0.7, target_position=expectation3[12:15]))
        core_str1a = r"q(", r"x_t", r"|", r"x_{t-1}", r", ", r"x_{t-2}", r", ", r"x_0", r")"
        core_q1a = MathTex(*core_str1a).move_to(core_q1).align_to(core_q1, LEFT)
        mcc = self.mc.copy().set_color(PURE_GREEN)
        self.playw(mcc.animate.next_to(core_q1, DOWN).align_to(core_q1, LEFT))
        self.playw(TransformMatchingTex(core_q1, core_q1a))
        self.playw(TransformMatchingTex(core_q1a, core_q1), FadeOut(mcc))

        core_str2 = r"q(", r"x_t", r"|", r"x_{t-1}", r", ", r"x_0", r")"
        core_q2 = MathTex(*core_str2).next_to(core_q1, DOWN)
        self.playw(TransformMatchingTex(core_q1.copy(), core_q2))

        bayesc = self.bayes.copy().set_color(PURE_GREEN)
        self.playw(bayesc.animate.align_to(core_q2, DOWN), FadeOut(core_q1))
        core_str3_nom = r"q(", r"x_t", r",", r"x_{t-1}", r", ", r"x_0", r")"
        core_str3_denom = r"q(", r"x_{t-1}", r", ", r"x_0", r")"
        core_str3 = self.frac(core_str3_nom, core_str3_denom)
        core_q3 = MathTex(*core_str3).move_to(core_q2)
        self.playw(TransformMatchingTex(core_q2, core_q3))

        core_str4_nom = r"q( ", r"x_t ", r",  ", r"x_0 ", r") "
        core_str4_denom = r"q( ", r"x_t ", r",  ", r"x_0 ", r") "
        core_str4 = self.frac(core_str4_nom, core_str4_denom)
        core_q4 = MathTex(*core_str3, r"\cdot", *core_str4).next_to(core_q3, DOWN)
        self.playw(TransformMatchingTex(core_q3.copy(), core_q4), FadeOut(bayesc))
        bayesc = self.bayes.copy().set_color(PURE_GREEN)
        self.playw(
            core_q4[:4].animate.set_color(YELLOW),
            core_q4[4:6].animate.set_color(PURE_RED),
            core_q4[6:8].animate.set_color(YELLOW),
            core_q4[-6:].animate.set_color(YELLOW),
            core_q4[8:-6].animate.set_opacity(0.5),
            FadeOut(core_q3),
            bayesc.animate.align_to(core_q4, DOWN)
        )
        core_str5a = r"q(", r"x_{t-1}", r"|", r"x_t", r",", r"x_0", r")"
        core_str5_nom = r"q( ", r"x_t ", r",  ", r"x_0 ", r") "
        core_str5_denom = r"q(", r"x_{t-1}", r", ", r"x_0", r")"
        core_str5 = self.frac(core_str5_nom, core_str5_denom)
        core_q5 = MathTex(*core_str5a, r"\cdot", *core_str5).align_to(core_q4, DOWN)
        core_q5[:1].set_color(YELLOW)
        core_q5[1:2].set_color(PURE_RED)
        core_q5[2:7].set_color(YELLOW)
        denom4 = core_q4[-6:].copy()
        core_q4[-6:].set_opacity(0)
        expectation4.move_to(VGroup(expectation3, core_q5))
        self.playw(TransformMatchingTex(core_q4, core_q5), FadeOut(denom4, target_position=core_q5[:7]), FadeOut(bayesc))
        self.playw(TransformMatchingTex(expectation3.copy(), expectation4))

        bayesc = self.bayes.copy().set_color(PURE_GREEN)
        hidden_mul = MathTex(r"\cdot", *self.frac(["q(x_0)"], ["q(x_0)"])).set_opacity(0.5).next_to(core_q5, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.5)
        self.playw(
            FadeIn(hidden_mul), 
            bayesc.animate.next_to(hidden_mul, RIGHT)
        )
        self.playw(
            FadeOut(bayesc, hidden_mul, core_q5, expectation3, self.mc, self.bayes),
            expectation4.animate.set_color(WHITE).set_opacity(1.0)
        )
        self.playw(expectation4.animate.shift(UP).shift(UP).shift(UP).scale(0.8))
        self.playw(
            expectation4[:3].animate.set_opacity(0.5),
            expectation4[25:].animate.set_opacity(0.5),
            expectation4[3:25].animate.set_color(YELLOW)
        )

        tex_exp5 = (e, llbracket, prior, *msig2, msiglog, *frac5, *msig2, msiglog, *frac4, msig2log, *frac2, rrbracket)
        expectation5 = MathTex(*tex_exp5, font_size=36)
        expectation5[:3].set_opacity(0.5),
        expectation5[29:].set_opacity(0.5),
        expectation5[3:29].set_color(YELLOW)
        self.playw(TransformMatchingTex(expectation4.copy(), expectation5))
        self.playw(
            expectation5[:3].animate.set_opacity(0.0),
            expectation5[29:].animate.set_opacity(0.0),
            expectation5[3:29].animate.next_to(expectation4, DOWN)
        )
        self.playw(
            expectation4[3:25].animate.set_color(WHITE).set_opacity(0.5),
            expectation5[3:15].animate.set_color(WHITE).set_opacity(0.5),
        )
        flatten_sigma = VGroup(*[MathTex(r"-\log", *self.frac([f"q(x_{i-1}|x_0)"], [f"q(x_{i}|x_0)"]), font_size=32) for i in range(2, 7)], MathTex("-", "...", font_size=32)).arrange(RIGHT)
        self.playw(LaggedStart(*[FadeIn(flatten_sigma[i], target_position=expectation5[15:29], scale=0.7) for i in range(len(flatten_sigma))], lag_ratio=0.25))
        flatten_sigma.save_state()
        self.playw(LaggedStart(*[Transform(flatten_sigma[i][0], MathTex(r"\cdot", font_size=32).move_to(flatten_sigma[i][0])) for i in range(1, len(flatten_sigma))], lag_ratio=0.15))
        self.playw(LaggedStart(*[AnimationGroup(FadeOut(flatten_sigma[i][-2], target_position=flatten_sigma[i+1][2], scale=0.7), FadeOut(flatten_sigma[i+1][2], target_position=flatten_sigma[i][-2], scale=0.7)) for i in range(len(flatten_sigma)-2)], FadeOut(flatten_sigma[-2][-2], target_position=flatten_sigma[-1], scale=0.7), lag_ratio=0.25))
        for i in range(len(flatten_sigma)-2):
            flatten_sigma[i][-2].set_opacity(0)
            flatten_sigma[i+1][2].set_opacity(0)
        flatten_sigma[-2][-2].set_opacity(0)
        last_T0 = MathTex(r"q(x_T|x_0)", font_size=32).move_to(flatten_sigma[0][-2])
        self.playw(FadeIn(last_T0, shift=LEFT))
        self.playw(expectation4[-5:-2].animate.set_color(YELLOW).set_opacity(1), flatten_sigma[0][2].animate.set_color(YELLOW), expectation5[15:29].animate.set_color(WHITE).set_opacity(0.5))
        self.playw(FadeOut(expectation4[-5:-2], flatten_sigma[0][2]))
        expectation4[-5:-2].set_opacity(0)
        flatten_sigma[0][2].set_opacity(0)

        final_prior = MathTex(r"-\log", *self.frac([r"p(x_T)"], [r"q(x_T|x_0)"]), font_size=36).scale(0.6).move_to(expectation4[2])
        self.playw(FadeTransform(expectation4[2], final_prior), FadeOut(last_T0))
        expectation4.generate_target().set_opacity(1.0)
        expectation4[2].set_opacity(0)
        expectation4.target[2].set_opacity(0)
        expectation4.target[-5:-2].set_opacity(0)
        self.playw(MoveToTarget(expectation4), FadeOut(flatten_sigma, expectation5))
        self.playw(self.camera.frame.animate.move_to(expectation4).scale(0.7))
        

    @staticmethod
    def frac(nom, denom):
        return "{", *nom, r"\over", *denom, "}"