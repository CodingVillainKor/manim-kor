from manim import *
import numpy as np

_fn_dict = {
    "tanh": np.tanh,
    "relu": lambda x: max(x, 0),
}

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

def MLP(*dims, layer_distance=3):
    layers = []
    for d in dims:
        color_layer = random_color()
        layer = VGroup(*[Circle(radius=0.2, color=color_layer) for i in range(d)]).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.4)
        layers.append(layer)
    layers = VGroup(*layers).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*layer_distance)

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

class Conv1d(VGroup):
    def __init__(self):
        super().__init__()

class Conv2d(VGroup):
    def __init__(self):
        super().__init__()

class RNN(VGroup):
    def __init__(self):
        super().__init__()

class Tensor(VGroup):
    def __init__(self, dim: int, shape="circle", arrange=DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.4):
        super().__init__()
        if shape == "circle":
            fig = lambda: Circle(radius=0.2, stroke_width=DEFAULT_STROKE_WIDTH*0.4, color=GREY)
        elif shape == "square":
            fig = lambda: Square(side_length=0.4, stroke_width=DEFAULT_STROKE_WIDTH*0.4, color=GREY)
        self.add(*[fig().set_fill(color=random_color(), opacity=1) for i in range(dim)]).arrange(arrange, buff=buff)
    
    def to_numbers(self, numbers=None, font_size=18):
        if numbers is None:
            numbers = np.random.randn(len(self))
        assert len(numbers) == len(self)
        nums = VGroup(*[Text(f"{n:.1f}" if n < 0 else f"+{n:.1f}", font_size=font_size, font="Consolas").move_to(self[i]) for i, n in enumerate(numbers)])
        return Transform(self, nums)

def propagation(mlp, indices, scene_instance=None, run_time=0.3):
    anims = []
    for i, idx in enumerate(indices):
        prop_sample = mlp[idx].copy().set_color(GREEN_E)
        if i == 0:
            anims.append(AnimationGroup(FadeIn(prop_sample), run_time=0.3))
        else:
            anims.append(AnimationGroup(FadeIn(prop_sample), previous_prop_sample.animate.set_opacity(0.), run_time=0.3))
        previous_prop_sample = prop_sample
    anims.append(AnimationGroup(FadeOut(previous_prop_sample), run_time=0.2))
    if scene_instance is None:
        return anims
    else:
        for anim in anims:
            scene_instance.play(anim, run_time=run_time)

def forward_prop(mlp, scene_instance=None, run_time=0.3):
    return propagation(mlp, range(len(mlp)), scene_instance, run_time)

def backward_prop(mlp, scene_instance=None, run_time=0.3):
    return propagation(mlp, reversed(range(len(mlp))), scene_instance, run_time)


def Activation(function="tanh"):
    fn = _fn_dict[function]
    nump = NumberPlane(x_range=(-1.5, 1.5), y_range=(-1.5, 1.5), x_length=0.35, y_length=0.35)
    if function=="relu":
        plot = nump.plot(fn, x_range=(-1.5, 1.2), stroke_width=2)
    else:
        plot = nump.plot(fn, stroke_width=2)
    c = Circle(radius=0.2, stroke_width=3)
    return VGroup(c, plot)

