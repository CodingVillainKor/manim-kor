from manim import *

def rect(height=0.3, width=1.0, opacity=0.8, 
         stroke_width=DEFAULT_STROKE_WIDTH/2,
         color=[BLUE, YELLOW], stroke_color=WHITE,
         **kwargs):
    return Rectangle(
        height=height,
        width=width,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        **kwargs)

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

_next_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

def softmax(*nums):
    _e = 2.71828
    exp_nums = [_e**num for num in nums]
    sum_exp_nums = sum(exp_nums)
    softmax_out = [e_num / sum_exp_nums for e_num in exp_nums]
    return softmax_out

class PositionalEncoding(MovingCameraScene):
    def construct(self):
        self.sceneA()

    def sceneA(self):
        keys = VGroup(
            rect(0.5, 0.5, color=RED), 
            rect(0.5, 0.5, color=BLUE),
            rect(0.5, 0.5, color=GOLD),
            rect(0.5, 0.5, color=GREEN),
            rect(0.5, 0.5, color=PURPLE),
            rect(0.5, 0.5, color=TEAL),
        ).arrange(DOWN).move_to(ORIGIN)
        pes = VGroup(
            rect(0.5, 0.5, color=BLUE_A), 
            rect(0.5, 0.5, color=TEAL_A),
            rect(0.5, 0.5, color=GOLD_A),
            rect(0.5, 0.5, color=GREEN_A),
            rect(0.5, 0.5, color=GREY_A),
            rect(0.5, 0.5, color=RED_A),
        ).arrange(DOWN).next_to(keys, RIGHT, buff=_next_buf*5)
        multiples = VGroup(*[MathTex(r"+").next_to(keys[i], buff=_next_buf*2) for i in range(len(keys))])
        
        self.playw(Write(keys))
        self.playw(Write(pes))
        self.playw(Write(multiples))
        self.playw(FadeOut(multiples))
        
        # for i in range(len(pes)):
        #     pes[i].generate_target()
        #     pes[i].target.move_to(keys[i])
        # self.playw(LaggedStart(*[MoveToTarget(pes[i]) for i in range(len(pes))], lag_ratio=0.3))
        self.playw(LaggedStart(*[FadeOut(pes[i], target_position=keys[i]) for i in range(len(pes))], lag_ratio=0.3))
        mixed_color = [self.weighted_sum_hex([keys[i].get_color().hex, pes[i].get_color().hex], [0.5, 0.5]) for i in range(len(pes))]

        self.playw(LaggedStart(*[keys[i].animate.set_color(mixed_color[i]).set_stroke_color(WHITE) for i in range(len(keys))]))


    @staticmethod
    def weighted_sum_hex(hexes, coeffs):
        assert len(hexes) == len(coeffs)
        
        return rgb_to_hex(sum([hex_to_rgb(h)*c for h, c in zip(hexes, coeffs)]))

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])
