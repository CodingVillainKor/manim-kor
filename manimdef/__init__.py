from manim import *
from functools import wraps

MOUSE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 100, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 249, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 244, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 230, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 230, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 253, 250, 10, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 237, 200, 10, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 250, 200, 10, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 252, 240, 200, 10, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 161, 118, 149, 164, 182, 197, 214, 227, 242, 247, 255, 255, 10, 0],
    [1, 140, 255, 255, 255, 255, 255, 140, 165, 222, 255, 174, 1, 1, 1, 1, 3, 17, 26, 34, 59, 59, 40, 10, 0],
    [1, 140, 255, 255, 255, 255, 140, 50, 1, 144, 255, 254, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 140, 60, 0, 0, 56, 253, 255, 161, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 140, 50, 0, 0, 0, 2, 193, 255, 241, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 140, 40, 0, 0, 0, 0, 0, 20, 255, 255, 129, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 140, 32, 0, 0, 0, 0, 0, 0, 21, 232, 255, 223, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 140, 75, 0, 0, 0, 0, 0, 0, 0, 0, 20, 255, 255, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 252, 255, 199, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 193, 255, 255, 69, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 255, 255, 174, 40, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 231, 255, 247, 46, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 147, 255, 255, 30, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 253, 255, 248, 43, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 197, 255, 208, 50, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def _find_multiple(string, target):
    return [i for i in range(len(string)) if string.find(target, i) == i]

def _count_indentation(text):
    for i in range(len(text)):
        if text[i] == " ":
            continue
        else:
            return i // 4

class NotoSerifText(Text):
    def __init__(self, *args, **kwargs):
        kwargs["font"] = "Noto Serif KR"
        super().__init__(*args, **kwargs)

class PythonCode(Code):
    def __init__(self, filename, **kwargs):
        kwargs["tab_width"] = kwargs.pop("tab_width", 4)
        kwargs["language"] = kwargs.pop("language", "python")
        kwargs["line_spacing"] = kwargs.pop("line_spacing", 0.6)
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
        
        indentation_level = _count_indentation(line)
        idx -= (len(self.indentation_chars)-1) * indentation_level
        return idx, idx+len(text)
    
    def text_slice(self, line_no:int, text:str, nth:int=1, exclusive=False) -> Mobject:
        idx_start, idx_end = self.find_text(line_no, text, nth)
        if exclusive:
            return VGroup(self.code[line_no-1][:idx_start], self.code[line_no-1][idx_end:])
        else:
            return self.code[line_no-1][idx_start:idx_end]
    
    def highlight(self, line_no:int, text:str=None, nth:int=1, 
                  anim=Write, color="#FFFF00", anim_out=FadeOut):
        if text is None:
            target = self.code[line_no-1].copy().set_color(color)
        else:
            target = self.text_slice(line_no, text, nth).copy().set_color(color)
        return anim(target), anim_out(target)

    def __call__(self, *line) -> VMobject:
        if len(line) == 1:
            return self.code[line[0]-1]
        elif len(line) == 2:
            return self.code[line[0]-1:line[1]]
        else:
            raise ValueError(f"The number of argument line should be 1 or 2, but {len(line)} given")

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

class CodeText(Text):
    def __init__(self, text, **kwargs):
        kwargs["font_size"] = kwargs.pop("font_size", 24)
        kwargs["font"] = kwargs.pop("font", "Consolas")
        super().__init__(text, **kwargs)

class Mouse(ImageMobject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on(self, target):
        self.move_to(target)
        self.shift(RIGHT*0.1 + DOWN*0.2)

class ListText(VGroup):
    def __init__(self, *texts, font_size=48, color=WHITE, arrange=RIGHT, **kwargs):
        super().__init__(**kwargs)
        t = VGroup(*[text if isinstance(text, Mobject) else Text(str(text), font_size=font_size, color=color, **kwargs) for text in texts]).arrange(arrange)
        bracket0 = Text("[", font_size=font_size, color=color, **kwargs).next_to(t[0], LEFT)
        bracket1 = Text("]", font_size=font_size, color=color, **kwargs).next_to(t[-1], RIGHT)
        self.add(bracket0, *t, bracket1)

class DefaultManimClass(MovingCameraScene):
    def construct(self):
        pass
    
    @wraps(MovingCameraScene.play)
    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    @wraps(MovingCameraScene.wait)
    def addw(self, *args, wait=1, **kwargs):
        self.add(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

    def to_front(self, *mobjects):
        self.add_foreground_mobjects(*mobjects)

    def playw_return(self, *args, **kwargs):
        self.playw(*args, rate_func=rate_functions.there_and_back, **kwargs)

    def play_camera(self, to=ORIGIN, scale=1, **play_kwargs):
        self.playw(self.camera.frame.animate.move_to(to).scale(scale), **play_kwargs)

    @property
    def cf(self) -> VMobject:
        return self.camera.frame

    @property
    def mouse(self):
        if getattr(self, "_mouse", None) is None:
            self._mouse = Mouse(self._get_mouse_array())
        return self._mouse
    
    @staticmethod
    def _get_mouse_array():
        mouse = MOUSE.copy()
        mouse = np.array(mouse)[..., None].repeat(4, -1)
        mouse[..., -1] = (mouse[..., 0] != 0) * 255
        return mouse

class File(VGroup):
    def __init__(self, size=2):
        super().__init__()
        nump = NumberPlane()
        ul = (-size/2, size/2*16/9)
        ur = (size/2, size/2*16/9)
        dl = (-size/2, -size/2*16/9)
        dr = (size/2, -size/2*16/9)
        
        rect_coords = [nump.c2p(*item) for item in [ul, ur, dr, dl]]
        paper = Polygon(*rect_coords, stroke_width=3*size, color=GREY_C).set_fill(WHITE, opacity=1)
        
        cut_ratio = 0.3
        fold_top = (ul[0] + cut_ratio*size, ul[1])
        fold_left = (ul[0], ul[1]-cut_ratio*size)
        fold_in = (fold_top[0], fold_left[1])
        fold_out_coords = [nump.c2p(*item) for item in [ul, fold_top, fold_left]]
        folded_out = Polygon(*fold_out_coords)
        fold_in_coords = [nump.c2p(*item) for item in [fold_top, fold_in, fold_left]]
        folded_in = Polygon(*fold_in_coords, stroke_width=3*size, color=GREY_C).set_fill(GREY_A, opacity=1)
        cut = Difference(paper, folded_out).set_fill(WHITE, opacity=1)
        self.add(cut)
        self.add(folded_in)

class DefaultManimClass3D(ThreeDScene):
    def construct(self):
        pass
    
    @wraps(ThreeDScene.play)
    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    @wraps(ThreeDScene.wait)
    def addw(self, *args, wait=1, **kwargs):
        self.add(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

    def to_front(self, *mobjects):
        self.add_foreground_mobjects(*mobjects)

    def playw_return(self, *args, **kwargs):
        self.playw(*args, rate_func=rate_functions.there_and_back, **kwargs)

    def play_camera(self, to=ORIGIN, scale=1, **play_kwargs):
        self.playw(self.camera.frame.animate.move_to(to).scale(scale), **play_kwargs)

    @wraps(ThreeDScene.set_camera_orientation)
    def set_camera(self, *args, **kwargs):
        return self.set_camera_orientation(*args, **kwargs)

    @property
    def cf(self) -> VMobject:
        return self.renderer.camera._frame_center

    @property
    def mouse(self):
        if getattr(self, "_mouse", None) is None:
            self._mouse = Mouse(self._get_mouse_array())
        return self._mouse
    
    @staticmethod
    def _get_mouse_array():
        mouse = MOUSE.copy()
        mouse = np.array(mouse)[..., None].repeat(4, -1)
        mouse[..., -1] = (mouse[..., 0] != 0) * 255
        return mouse

_surround_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

class SurroundingRect(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def surround(self, mobject, buf_height=_surround_buf, buf_width=_surround_buf):
        self.move_to(mobject)\
            .stretch_to_fit_height(mobject.height + buf_height)\
            .stretch_to_fit_width(mobject.width + buf_width)
        return self
    
class Chainer(VGroup):
    _chain_class = {
        "plain": Line,
        "dashedline": DashedLine,
        "arrow": Arrow
    }
    def __init__(self, *args, chain_type="plain", chain_kwargs={"buff":0}, **kwargs):
        super().__init__(**kwargs)
        if len(args) <= 1:
            raise ValueError("The number of args should be larger than one.")
        
        line_cls = self._chain_class.get(chain_type, "plain")
        for now_, next_ in zip(args[:-1], args[1:]):
            self.add(line_cls(now_, next_, **chain_kwargs))

class BrokenLine(VGroup):
    def __init__(self, *pos, arrow=False, **kwargs):
        assert len(pos) > 2
        super().__init__()
        starts = pos[:-1]
        ends = pos[1:]
        for i, (s, e) in enumerate(zip(starts, ends)):
            line_kwargs = kwargs.copy()
            if i != len(starts)-1:
                if arrow and "max_tip_length_to_length_ratio" in kwargs:
                    line_kwargs.pop("max_tip_length_to_length_ratio")
                self.add(Line(s, e, **line_kwargs))
            else:
                L = Arrow if arrow else Line
                self.add(L(s, e, buff=0, **line_kwargs))
