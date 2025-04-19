from manim import *

class NumText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
    
    @property
    def num(self):
        return float(self.text)

def NumBox(text, text_config={}, box_config={}):
    text = NumText(text, **text_config)
    rect = Square(**box_config).surround(text)
    return VGroup(text, rect)

class Equation(MovingCameraScene):
    def construct(self):
        tex1 = MathTex("a_1*r^t > n", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex2 = MathTex("10*r^t > n", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex3 = MathTex("10*2^t > {{n}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex4 = MathTex("10*2^{{t}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex5 = MathTex("10*2^{{1}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex6 = MathTex("10*2^{{2}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex7 = MathTex("10*2^{{3}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex8 = MathTex("10*2^{{{...}}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex9 = MathTex("10*2^{{9}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex10 = MathTex("10*2^{{{10}}} > {{10000}}", font_size=DEFAULT_FONT_SIZE*2, color=PURE_GREEN)

        #a = Tex("$\\frac{a_1*(r^{이사횟수}-1)}{r-1}>10000$", font_size=DEFAULT_FONT_SIZE*2)
        self.add(tex1)
        self.wait()
        self.playw(TransformMatchingTex(tex1, tex2))
        self.playw(TransformMatchingTex(tex2, tex3))
        self.playw(TransformMatchingTex(tex3, tex4))
        self.playw(TransformMatchingTex(tex4, tex5))
        self.play(TransformMatchingTex(tex5, tex6))
        self.play(TransformMatchingTex(tex6, tex7))
        self.play(TransformMatchingTex(tex7, tex8))
        self.play(TransformMatchingTex(tex8, tex9))
        self.play(TransformMatchingTex(tex9, tex10))
        self.wait()
        

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class Equation2(MovingCameraScene):
    def construct(self):
        tex1 = MathTex("a_1*r^t > n", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex2 = MathTex("{{t}} {{>}} {{ \\log_r{\\frac{n}{a_1}} }}", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)
        tex3 = MathTex("{{t}} {{=}} \\lceil{{ \\log_r{\\frac{n}{a_1}} }}\\rceil", font_size=DEFAULT_FONT_SIZE*2, color=GOLD)

        #a = Tex("$\\frac{a_1*(r^{이사횟수}-1)}{r-1}>10000$", font_size=DEFAULT_FONT_SIZE*2)
        self.add(tex1)
        self.playw(TransformMatchingTex(tex1, tex2))
        self.playw(TransformMatchingTex(tex2, tex3, key_map={">":"="}))
        self.wait()
        

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class Equation3(MovingCameraScene):
    def construct(self):
        tex1 = MathTex("\\frac{a_1*(r^{t}-1)}{r-1}", font_size=DEFAULT_FONT_SIZE*1.5, color=GOLD)
        tex2 = MathTex("\\frac{a_1*(r^{\\lceil{ \\log_r{\\frac{n}{a_1}} }\\rceil}-1)}{r-1}", font_size=DEFAULT_FONT_SIZE*1.5, color=GOLD)

        #a = Tex("$\\frac{a_1*(r^{이사횟수}-1)}{r-1}>10000$", font_size=DEFAULT_FONT_SIZE*2)
        self.add(tex1)
        self.wait()
        self.playw(TransformMatchingTex(tex1, tex2))
        

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class Equation4(MovingCameraScene):
    def construct(self):
        tex1 = MathTex("a^{\\log_a{ {{b}} }}", font_size=DEFAULT_FONT_SIZE*1.5, color=GOLD)
        tex2 = MathTex("{{b}}", font_size=DEFAULT_FONT_SIZE*1.5, color=GOLD)

        #a = Tex("$\\frac{a_1*(r^{이사횟수}-1)}{r-1}>10000$", font_size=DEFAULT_FONT_SIZE*2)
        self.add(tex1)
        self.wait()
        self.playw(TransformMatchingTex(tex1, tex2))
        

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class Equation5(MovingCameraScene):
    def construct(self):
        tex1 = MathTex("{ {{ a_1 * }} ( r^{ \\lceil \\log_r { {n \\over a_1} } \\rceil } {{ -1 }} ) \\over {{ r-1 }} }", font_size=DEFAULT_FONT_SIZE*1.5, color=GOLD)
        tex2 = MathTex("{ {{ a_1 * }} ( {{ {n \\over a_1} }} {{ -1 }} ) \\over {{ r-1 }} }", font_size=DEFAULT_FONT_SIZE*1.5, color=GOLD)
        index_labels(tex1[0])
        #a = Tex("$\\frac{a_1*(r^{이사횟수}-1)}{r-1}>10000$", font_size=DEFAULT_FONT_SIZE*2)
        self.add(tex1)
        self.wait()
        self.playw(TransformMatchingTex(tex1, tex2))
        

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])