from manim import *

class PythonCode(Code):
    def __init__(self, filename, **kwargs):
        kwargs["tab_width"] = kwargs.pop("tab_width", 4)
        kwargs["language"] = kwargs.pop("language", "python")
        kwargs["line_spacing"] = kwargs.pop("line_spacing", 1)
        kwargs["background"] = kwargs.pop("background", "window")
        kwargs["font"] = kwargs.pop("font", "Consolas")
        super().__init__(filename, **kwargs)

    @property
    def frame(self):
        return self[:2]
    
    @property
    def script(self):
        return self[2]

class NumText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
    
    @property
    def num(self):
        return float(self.text)

def rect(height=0.3, width=0.3, opacity=0.8, 
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

def NumBox(text, text_config={}, box_config={}):
    text = NumText(text, **text_config)
    rect = Square(**box_config).surround(text)
    return VGroup(text, rect)

def texbox(*msg, tex_config=dict(), box_config=dict()):
    tex = Tex(*msg, **tex_config)
    box = rect(height=tex.height, width=tex.width, 
               stroke_color=GOLD, **box_config).surround(tex)
    return VGroup(box, tex)

class DefaultManimClass(MovingCameraScene):
    def construct(self):
        pass

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

