from manim import *
from random import random

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

def texbox(*msg, tex_config=dict(), box_config=dict()):
    tex = Tex(*msg, **tex_config)
    box = rect(height=tex.height, width=tex.width, 
               stroke_color=GOLD, **box_config).surround(tex)
    return VGroup(box, tex)


def NumBox(text, text_config={}, box_config={}):
    text = NumText(text, **text_config)
    rect = Square(**box_config).surround(text)
    return VGroup(text, rect)

_next_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
_e = 2.71828

def softmax(*nums):
    _e = 2.71828
    exp_nums = [_e**num for num in nums]
    sum_exp_nums = sum(exp_nums)
    softmax_out = [e_num / sum_exp_nums for e_num in exp_nums]
    return softmax_out

def six_three_zero(x, y):
    if x==y: return 4
    elif x==y-1: return 3.3
    else: return 0

class EncDec(MovingCameraScene):
    def construct(self):
        query, key, value = self.sceneA()
        enc_out = self.sceneB(query, key, value)
        self.sceneC(enc_out)

    def sceneA(self):
        self.play(self.camera.frame.animate.scale(1.5), run_time=0.1)
        vectors = VGroup(
            rect(0.5, 0.5, color=RED_D),
            rect(0.5, 0.5, color=BLUE_D),
            rect(0.5, 0.5, color=GOLD_D),
            rect(0.5, 0.5, color=GREEN_D),
            rect(0.5, 0.5, color=PURPLE_D),
            rect(0.5, 0.5, color=TEAL_D),
        ).arrange(DOWN)
        tbq = texbox("$W_q$", box_config={"color": BLACK, "opacity":1.0}).next_to(vectors, UP, buff=_next_buf*2)
        tbk = texbox("$W_k$", box_config={"color": BLACK, "opacity":1.0}).next_to(tbq, RIGHT, buff=_next_buf*8)
        tbv = texbox("$W_v$", box_config={"color": BLACK, "opacity":1.0}).next_to(tbk, RIGHT, buff=_next_buf*2)

        query, key, value = vectors.copy(), vectors.copy(), vectors.copy()
        self.playw(FadeIn(query))
        self.playw(FadeIn(tbq), FadeIn(tbk), FadeIn(tbv))
        query.generate_target(); key.generate_target(); value.generate_target()
        query.target.next_to(tbq, UP, buff=_next_buf*2)
        key.target.move_to((tbk.get_x(), query.get_y(), 0))
        value.move_to((tbk.get_x(), query.get_y(), 0))
        self.add(key)
        self.playw(MoveToTarget(query), self.camera.frame.animate.scale(1.2).move_to(VGroup(tbq, tbk, tbv)))
        self.playw(MoveToTarget(key))
        key.generate_target()
        key_colors = [self.weighted_sum_hex([k.get_color().hex, "#000000"], [0.9, 0.1]) for k in key]
        self.bring_to_front(tbk)
        for k, c in zip(key.target, key_colors):
            k.set_color(c).set_stroke_color(WHITE)
        key.target.next_to(tbk, UP, buff=_next_buf*2)
        self.add(value)
        self.playw(MoveToTarget(key))
        value.generate_target()
        value.target.move_to((tbv.get_x(), vectors.get_y(), 0))
        self.playw(MoveToTarget(value))
        value.generate_target()
        self.bring_to_front(tbv)
        value_colors = [self.weighted_sum_hex([v.get_color().hex, "#FFFFFF"], [0.9, 0.1]) for v in value]
        for v, c in zip(value.target, value_colors):
            v.set_color(c).set_stroke_color(WHITE)
        value.target.next_to(tbv, UP, buff=_next_buf*2)
        self.playw(MoveToTarget(value))
        self.playw(FadeOut(tbq), FadeOut(tbk), FadeOut(tbv),
                   self.camera.frame.animate.scale(0.7).move_to(VGroup(query, key, value)))
        
        return query, key, value

    def sceneB(self, query, key, value):
        attn_result = []
        for i in range(len(query)):
            random_logits = [random()*2-1 + six_three_zero(i, j) for j in range(len(key))]
            one_attn_out = self.one_query_attention(query, key, value, i, random_logits)
            attn_result.append(one_attn_out)
            if i != len(query)-1:
                self.playw(FadeIn(query[:i], query[i+1:], key, value))

        attn_out = VGroup(*attn_result)
        self.playw(FadeOut(query[-1]), self.camera.frame.animate.move_to(attn_out))

        return attn_out

    def sceneC(self, enc_out):
        tbk = texbox("$W_k$", box_config={"color": BLACK, "opacity":1.0}).next_to(enc_out, UP, buff=_next_buf*2)
        enc_out.generate_target()
        enc_out.target.next_to(tbk, UP, buff=_next_buf*2)
        self.playw(Write(tbk))
        vectors = VGroup(
            rect(0.5, 0.5, color=RED_D),
            rect(0.5, 0.5, color=BLUE_D),
            rect(0.5, 0.5, color=GOLD_D),
            rect(0.5, 0.5, color=GREEN_D),
            rect(0.5, 0.5, color=PURPLE_D),
            rect(0.5, 0.5, color=TEAL_D),
        ).arrange(RIGHT).align_to(enc_out.target, LEFT).align_to(tbk, DOWN).shift(RIGHT)
        self.playw(LaggedStart(MoveToTarget(enc_out), self.camera.frame.animate.move_to(VGroup(vectors, enc_out.target)), lag_ratio=0.4))
        self.playw(FadeIn(vectors), FadeOut(tbk))

    def one_query_attention(self, query, key, value, idx, logits):
        self.playw(FadeOut(VGroup(query[:idx], query[idx+1:])))
        q = query[idx]
        tlogits = [Text(f"{logits[i]:.2f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(key[i]) for i in range(len(key))]
        for i in range(len(key)):
            q.save_state(); q.generate_target()
            q.target.move_to(key[i])
            self.play(MoveToTarget(q))
            self.play(q.animate.restore(), FadeTransform(key[i], tlogits[i]))
        self.wait()
        elogits = [_e**l for l in logits]
        sum_elogits = sum(elogits)
        weights = [el/sum_elogits for el in elogits]
        tweights = VGroup(*[Text(f"{weights[i]:.3f}", font="Consolas", color=YELLOW_A, font_size=DEFAULT_FONT_SIZE*0.5).move_to(key[i]) for i in range(len(weights))])
        multiples = VGroup(*[MathTex(r"\times").next_to(tweights[i], buff=_next_buf) for i in range(len(tweights))])
        self.playw(LaggedStart(*[FadeTransform(tlogits[i], tweights[i]) for i in range(len(tweights))], lag_ratio=0.15),
                   LaggedStart(*[FadeIn(m) for m in multiples], lag_ratio=0.15))
        
        attn_result_color = self.weighted_sum_hex([value[i].get_color().hex for i in range(len(value))], weights)
        result = rect(0.5, 0.5, color=attn_result_color).next_to(value[idx], RIGHT, buff=_next_buf*3)
        qkv = VGroup(tweights, multiples, value)
        self.playw(FadeTransform(qkv, result))

        return result



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
    