from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class gitstash(Scene2D):
    def construct(self):
        start = get_commit().shift(UP * 2.5 + LEFT * 3.5)

        dot3 = (
            Text(". . .", color=GREY_A, font_size=36)
            .rotate(PI / 2)
            .move_to(start)
            .shift(UP * 0.3)
        )
        c1, l1 = new_commit(start, direction="down")
        c2, l2 = new_commit(c1, direction="down")
        graph = VGroup(c1, c2, l1, l2, dot3)

        code1 = PythonCode("src/c1.py").shift(RIGHT)
        code1(1, 3).set_color(RED_B)
        commit_code1 = SurroundingRect(
            color=GREEN, stroke_width=3, stroke_opacity=0.5
        ).surround(code1.code[0])
        link1 = DashedLine(c1.get_right(), commit_code1.get_left(), color=GREEN)

        commit_code2 = SurroundingRect(
            color=BLUE, stroke_width=3, stroke_opacity=0.5
        ).surround(code1.code[-2:])
        link2 = DashedLine(c2.get_right(), commit_code2.get_left(), color=BLUE)

        self.playw(FadeIn(graph, code1, commit_code1, link1, commit_code2, link2))
        self.playw(Circumscribe(VGroup(code1.code[1][5:], code1.code[2]), color=RED))

        stack = (
            BrokenLine(ORIGIN, ORIGIN + DOWN, ORIGIN + DOWN + RIGHT, ORIGIN + RIGHT)
            .next_to(graph, LEFT, buff=1)
            .shift(DOWN * 1.5)
        )
        stashed = Text("stashed", font_size=18).next_to(stack, DOWN, buff=0.1)
        updated = code1(1, 3).set_z_index(1)
        updated.save_state()
        updated_square = (
            Square(0.6, color=RED, stroke_width=3)
            .set_fill(BLACK, opacity=1)
            .move_to(updated[1])
            .shift(LEFT)
        )
        updated_squarec = updated_square.copy()
        self.play(FadeIn(stack, stashed), updated.animate.become(updated_squarec))
        updated.set_opacity(0)
        updated_square.save_state()
        self.playw(updated_square.animate.move_to(stack))

        gc_other = Text(
            "git checkout <other_branch>", font=MONO_FONT, font_size=20
        ).shift(DOWN * 2.2)
        self.playwl(*[FadeIn(item) for item in gc_other], lag_ratio=0.05)

        graphc = graph.copy().set_color(YELLOW_A).set_fill(opacity=0)
        dot3c = dot3.copy().set_color(YELLOW_A)
        self.playwl(
            FadeOut(code1, link1, link2, commit_code1, commit_code2),
            FadeOut(graph, shift=UL),
            FadeIn(graphc, dot3c, shift=DL),
            lag_ratio=0.4,
        )
        self.playw(Wiggle(graphc))

        gc_original = Text(
            "git checkout <original_branch>", font=MONO_FONT, font_size=20
        ).shift(DOWN * 2.2)
        self.playw(
            *[
                Transform(
                    gc_other[s],
                    gc_original[s],
                    replace_mobject_with_target_in_scene=True,
                )
                for s in [slice(None, 3), slice(3, 11), slice(11, None)]
            ]
        )
        self.playwl(
            FadeOut(graphc, dot3c, shift=UL),
            FadeIn(graph, code1, link1, link2, commit_code1, commit_code2, shift=DL),
            lag_ratio=0.4,
        )
        gs_pop = Text("git stash pop", font=MONO_FONT, font_size=20).shift(DOWN * 2.2)
        self.playw(
            *[
                Transform(
                    gc_original[s1],
                    gs_pop[s2],
                    replace_mobject_with_target_in_scene=True,
                )
                for s1, s2 in [
                    [slice(None, 3), slice(None, 3)],
                    [slice(3, 11), slice(3, 8)],
                    [slice(11, None), slice(8, None)],
                ]
            ]
        )

        self.play(Restore(updated_square))
        updated_square.set_opacity(0)
        updated.set_opacity(1)
        self.playw(Restore(updated))


get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=24, color=RED)


def new_commit(from_commit, *, direction="right"):
    direction_np = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}[direction]
    newc = get_commit().next_to(from_commit, direction=direction_np, buff=1)
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
    return newc, cline