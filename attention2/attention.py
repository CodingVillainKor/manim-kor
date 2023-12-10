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

class Attention(MovingCameraScene):
    def construct(self):
        self.sceneA()

    def sceneA(self):
        query = rect(0.5, 0.5)
        keys = VGroup(
            rect(0.5, 0.5, color=RED), 
            rect(0.5, 0.5, color=BLUE),
            rect(0.5, 0.5, color=GOLD),
            rect(0.5, 0.5, color=GREEN),
            rect(0.5, 0.5, color=PURPLE),
            rect(0.5, 0.5, color=TEAL),
        ).arrange(DOWN).next_to(query, buff=_next_buf*10)
        values = keys.copy().next_to(keys, buff=_next_buf*4)
        for i in range(len(values)):
            values[i].set_color(self.weighted_sum_hex([values[i].get_color().hex, "#FFFFFF"], [0.6, 0.4])).set_stroke_color(WHITE)

        VGroup(query, keys, values).move_to(ORIGIN)
        multiples = [MathTex(r"\times").next_to(keys[i], buff=_next_buf*2) for i in range(len(keys))]
        key_mul_values = VGroup(keys, values, *multiples)

        self.playw(Write(query))
        self.playw(Write(keys))
        self.playw(FadeIn(values))

        # query inner-products each key
        logits = [1.81, 4.23, -3.14, -5.01, 0.019, -1.18]
        weights = softmax(*logits)
        l_text = [Text(f"{logits[i]:.2f}", 
                       font="Consolas", 
                       font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[i]) for i in range(len(logits))]
        w_text = [Text(f"{weights[i]:.2f}", 
                       font="Consolas", color=YELLOW_A,
                       font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[i]) for i in range(len(weights))]
        result_color = self.weighted_sum_hex([values[i].get_color().hex for i in range(len(values))],
                                             weights)
        result_rect = rect(0.5, 0.5).set_color(result_color).move_to(key_mul_values.get_center())
        for i in range(len(keys)):
            query.generate_target(); query.save_state()
            query.target.move_to(keys[i])
            self.play(MoveToTarget(query))
            self.play(query.animate.restore(), FadeTransform(keys[i], l_text[i]))
        self.wait()
        self.playw(*[FadeTransform(l_text[i], w_text[i]) for i in range(len(l_text))])
        self.playw(*[FadeIn(multiples[i]) for i in range(len(multiples))])
        w_mul_values = VGroup(*w_text, values, *multiples)
        arrow = Arrow(start=query.get_right(), end=result_rect.get_left(), stroke_width=4, color=YELLOW_B)
        self.playw(LaggedStart(FadeTransform(w_mul_values, result_rect), Write(arrow), lag_ratio=0.7))

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

    @staticmethod
    def weighted_sum_hex(hexes, coeffs):
        assert len(hexes) == len(coeffs)
        
        return rgb_to_hex(sum([hex_to_rgb(h)*c for h, c in zip(hexes, coeffs)]))
    