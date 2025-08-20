from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        gct = Text("git conflict", color=RED)

        self.playw(FadeIn(gct))
        self.play(gct.animate.shift(UP * 2.5))

        c0 = get_commit().shift(DOWN * 2)
        c1, l01 = new_commit(c0, direction="up")
        c2, l12 = new_commit(c1, direction="up")
        c3, l23 = new_commit(c2, direction="right", color=GREEN)
        c4, l34 = new_commit(c3, direction="up", color=GREEN)
        self.playw(
            Succession(
                FadeIn(c0),
                FadeIn(l01, c1),
                FadeIn(l12, c2),
                FadeIn(l23, c3),
                FadeIn(l34, c4),
            ),
            run_time=2,
        )
        c5, l25 = new_commit(c2, direction="up", color=RED)
        c2c = c2.copy()
        self.play(c2c.animate.move_to(c5))
        c4c = c4.copy()
        self.play(
            c4c.animate.next_to(c2c, RIGHT, buff=0), run_time=0.5, rate_func=rush_into
        )
        c4c.color = PURE_RED
        c2c.stroke_color = RED_E
        self.play(
            AnimationGroup(c4c.animate.shift(RIGHT * 8 + UP * 3), rate_func=rush_from),
            run_time=1.2,
        )
        linec1 = DashedLine(
            c2.get_top(), c2c.get_bottom(), color=GREY_C, dashed_ratio=0.7
        )
        linec2 = DashedLine(
            c4.get_left(), c2c.get_right(), color=GREY_C, dashed_ratio=0.7
        )
        self.playw(FadeIn(linec1, linec2))
        self.playw(self.cf.animate.move_to(c2c).scale(0.01))


get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=24, color=RED)


def new_commit(from_commit, *, direction="right", color=None, buff=0.5):
    direction_np = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}[direction]
    newc = get_commit().next_to(from_commit, direction=direction_np, buff=buff)
    if direction == "up":
        start = from_commit.get_top()
        to = newc.get_bottom()
    elif direction == "down":
        start = from_commit.get_bottom()
        to = newc.get_top()
    elif direction == "left":
        start = from_commit.get_left()
        to = newc.get_right()
    elif direction == "right":
        start = from_commit.get_right()
        to = newc.get_left()
    else:
        raise ValueError("Direction must be UP, DOWN, LEFT, or RIGHT")
    cline = Line(start, to, color=GREY_C)
    if color is not None:
        newc.stroke_color = color
    return newc, cline


class ascode(Scene2D):
    def construct(self):
        code1 = PythonCode("code1.py")
        code2 = PythonCode("code2.py")
        code1.code[:2].set_opacity(0.5)
        code2.code[:2].set_opacity(0.5)

        cs = VGroup(code1, code2).arrange(RIGHT, buff=1.5).shift(UP * 1.5)
        self.playw(FadeIn(cs))

        c0 = get_commit().shift(DOWN + LEFT * 2)
        c1, l01 = new_commit(c0, direction="right")
        c2, l12 = new_commit(c1, direction="right")
        c3, l13 = new_commit(c1, direction="down", color=GREEN)
        c4, l34 = new_commit(c3, direction="right", color=GREEN)
        c5, l45 = new_commit(c4, direction="right", color=GREEN)
        commits = VGroup(c0, c1, c2, c3, c4, c5, l01, l12, l13, l34, l45)
        self.playw(FadeIn(commits))

        l2 = DashedLine(
            c2.get_top(),
            code1.code[4][-1],
            color=YELLOW,
            dashed_ratio=0.7,
            dash_length=0.2,
        )
        l3 = DashedLine(
            c5.get_top(),
            code2.code[4][4],
            color=PURE_GREEN,
            dashed_ratio=0.7,
            dash_length=0.2,
        )

        self.playw(FadeIn(l2, l3))
        c6, l26 = new_commit(c2, direction="right")

        c2c = c2.copy()
        _l2c = lambda: DashedLine(
            c2c.get_top(),
            code1.code[4][-1],
            color=YELLOW,
            dashed_ratio=0.7,
            dash_length=0.2,
        )
        l2c = _l2c()
        c5c = c5.copy()
        _l3c = lambda: DashedLine(
            c5c.get_top(),
            code2.code[4][4],
            color=PURE_GREEN,
            dashed_ratio=0.7,
            dash_length=0.2,
        )
        l3c = _l3c()
        self.add(l2c, l3c)
        l2c.add_updater(lambda m: m.become(_l2c()))
        l3c.add_updater(lambda m: m.become(_l3c()))
        self.play(c2c.animate.move_to(c6), FadeOut(l2))
        self.play(
            c5c.animate.next_to(c2c, DOWN, buff=0),
            FadeOut(l3),
            code2.code[3:].animate.next_to(code1.code[3:], RIGHT, buff=-0.8),
            rate_func=rush_into,
            run_time=0.7,
        )
        code2.code[3:].color = PURE_RED
        c5c.color = PURE_RED
        self.playw(
            VGroup(code2.code[3:], c5c).animate.rotate(-PI / 3).shift(RIGHT * 25),
            rate_func=rush_from,
            run_time=3.0,
        )

class gitmerge(Scene2D):
    def construct(self):
        code1 = PythonCode("code1.py").set_z_index(-2)
        code2 = PythonCode("code2.py")
        
        code1.code[2:].set_opacity(0.0)

        cs = VGroup(code1, code2).arrange(RIGHT, buff=1.5).shift(UP * 1.5)
        merged = code2.code[2:].copy().set_z_index(-1)
        code2.code[2:].set_color(YELLOW)
        bh = Text("<branch hoyo>", font=MONO_FONT, font_size=20).next_to(code2, UP)

        self.playw(FadeIn(cs, bh))
        
        gitmerge = Text("git merge hoyo", font=MONO_FONT, font_size=24).next_to(code1, DOWN, buff=0.3)
        self.playwl(*[FadeIn(item) for item in gitmerge], lag_ratio=0.1, run_time=1)

        self.playw(merged.animate.align_to(code1.code[2:], LEFT))

class gitconflict(Scene3D):
    def construct(self):
        tilt_degree=45
        self.tilt_camera_vertical(tilt_degree)
        gct = Text("git conflict", color=RED, font_size=36).rotate(tilt_degree*DEGREES, RIGHT)
        self.playw(FadeIn(gct))
        self.play(gct.animate.shift(UP * 5.5 + LEFT*4))

        c0 = get_commit().shift(DOWN * 1.5)
        c1, l01 = new_commit(c0, direction="up")
        c2, l12 = new_commit(c1, direction="up")
        c3, l13 = new_commit(c1, direction="right", color=GREEN, buff=1.0)
        c4, l34 = new_commit(c3, direction="up", color=GREEN)
        c5, l45 = new_commit(c4, direction="up", color=GREEN)
        c6, l26 = new_commit(c2, direction="up", color=PURE_RED)
        graph = VGroup(c0, c1, c2, c3, c4, c5, l01, l12, l13, l34, l45, c6, l26).scale(1.5)
        l26c = DashedVMobject(l26, num_dashes=3, dashed_ratio=0.7)
        l26.set_opacity(0)
        self.playw(FadeIn(graph))
        self.playw(FadeIn(l26c))
        l56 = DashedVMobject(Line(c5.get_left(), c6.get_right(), color=GREY_B), num_dashes=5, dashed_ratio=0.7)
        self.playw(FadeIn(l56))
