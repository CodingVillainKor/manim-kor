from manim import *
import numpy as np

def Linear(in_channels: int, out_channels: int):
    in_layer = VGroup(*[Circle(radius=0.2, color=BLUE) for i in range(in_channels)]).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.4)
    out_layer = VGroup(*[Circle(radius=0.2, color=GREEN) for i in range(out_channels)]).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.4)
    VGroup(in_layer, out_layer).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*4)
    weights = []
    for i in range(in_channels):
        weight = []
        for j in range(out_channels):
            weight.append(Line(in_layer[i].get_right(), out_layer[j].get_left(), buff=0.05, stroke_width=0.8))
        weight = VGroup(*weight)
        weights.append(weight)
    weights = VGroup(*weights)

    return VGroup(in_layer, weights, out_layer)

def MLP(*dims):
    layers = []
    for d in dims:
        color_layer = random_color()
        layer = VGroup(*[Circle(radius=0.2, color=color_layer) for i in range(d)]).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.4)
        layers.append(layer)
    layers = VGroup(*layers).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)

    weights = []
    for k, (d1, d2) in enumerate(zip(dims[:-1], dims[1:])):
        weight = []
        for i in range(d1):
            w = []
            for j in range(d2):
                w.append(Line(layers[k][i].get_right(), layers[k+1][j].get_left(), buff=0.05, stroke_width=0.8))
            w = VGroup(*w)
            weight.append(w)
        weight = VGroup(*weight)
        weights.append(weight)
    weights = VGroup(*weights)

    result = []
    for i in range(len(weights)):
        result.append(layers[i])
        result.append(weights[i])
    result.append(layers[i+1])
    return VGroup(*result)

class Vector(VGroup):
    def __init__(self, dim: int, arrange=DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.4):
        super().__init__()
        self.add(*[Circle(radius=0.2, stroke_width=DEFAULT_STROKE_WIDTH*0.4, color=GREY).set_fill(color=random_color(), opacity=1) for i in range(dim)]).arrange(arrange, buff=buff)
    
    def to_numbers(self, numbers=None):
        if numbers is None:
            numbers = np.random.randn(len(self))
        assert len(numbers) == len(self)
        nums = VGroup(*[Text(f"{n:.1f}" if n < 0 else f"+{n:.1f}", font_size=18, font="Consolas").move_to(self[i]) for i, n in enumerate(numbers)])
        return Transform(self, nums)

def propagation(mlp, indices):
    anims = []
    for i, idx in enumerate(indices):
        prop_sample = mlp[idx].copy()
        if i == 0:
            anims.append(FadeIn(prop_sample, scale=1.2))
        else:
            anims.append(AnimationGroup(FadeIn(prop_sample, scale=1.2), FadeOut(previous_prop_sample), run_time=0.3))
        previous_prop_sample = prop_sample
    anims.append(FadeOut(previous_prop_sample))
    return LaggedStart(*anims, lag_ratio=1)

def forward_prop(mlp):
    return propagation(mlp, range(len(mlp)))

def backward_prop(mlp):
    return propagation(mlp, reversed(range(len(mlp))))