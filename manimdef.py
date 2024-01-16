from manim import *

def _find_multiple(string, target):
    return [i for i in range(len(string)) if string.find(target, i) == i]

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
    
    def find_text(self, line_no:int, text:str, nth:int=1):
        lines = self.code_string.split("\n")
        line = lines[line_no-1]
        try:
            idx = _find_multiple(line, text)[nth-1]
        except IndexError:
            raise IndexError(f"Cannot find {nth}th {text} at line {line_no}: {line}")

        indentation_level = line.count(self.indentation_chars)
        idx -= (len(self.indentation_chars)-1) * indentation_level
        return idx, idx+len(text)
    
    def generate_highlight(self):
        if getattr(self, "hightlight", None) is not None:
            raise ValueError("Line highlight already exists")
        self.highlight = SurroundingRectangle(self.code[0], color=YELLOW_D, stroke_width=DEFAULT_STROKE_WIDTH*0.5)

    def do_highlight(self, line_no:int, remainder_blur=True):
        if getattr(self, "highlight", None) is None:
            raise ValueError("There is not highlight. code.generate_highlight() first.")
        self.highlight.generate_target().surround(self.code[line_no-1]) # TODO: it works not well...






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

_surround_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

class SurroundingRect(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def surround(self, mobject, buf_height=_surround_buf, buf_width=_surround_buf):
        self.move_to(mobject)\
            .stretch_to_fit_height(mobject.height + buf_height)\
            .stretch_to_fit_width(mobject.width + buf_width)
        return self
