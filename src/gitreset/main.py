from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        init = get_commit()
        c1, cline1 = new_commit(init, direction="up")
        c2, cline2 = new_commit(c1, direction="up")

        graph = VGroup(init, c1, c2, cline1, cline2).shift(DOWN * 1.5)

        code_init = PythonCode("src/init.py").next_to(init, LEFT, buff=0.75)
        ccline_init = DashedLine(
            init.get_left(), code_init.get_right(), color=GREY_C, buff=0
        )
        code_c1 = PythonCode("src/c1.py").next_to(c1, RIGHT, buff=0.75)
        code_c1.code[-1].set_color(YELLOW)
        ccline_c1 = DashedLine(c1.get_right(), code_c1.get_left(), color=GREY_C, buff=0)
        code_c2 = PythonCode("src/c2.py").next_to(c2, LEFT, buff=0.75)
        code_c2.code[-1].set_color(YELLOW)
        ccline_c2 = DashedLine(c2.get_left(), code_c2.get_right(), color=GREY_C, buff=0)

        head = Text("HEAD", font_size=24, color=GREEN_D).next_to(init, UP, buff=1)
        headarrow = Arrow(head.get_bottom(), init.get_top(), color=GREEN_D, buff=0.1)
        head = VGroup(head, headarrow)

        self.play(Create(init))
        self.play(
            LaggedStart(
                Create(ccline_init),
                FadeIn(code_init, shift=LEFT, scale=0.5),
                lag_ratio=0.5,
            ),
            FadeIn(head),
        )
        self.play(
            LaggedStart(
                head.animate.next_to(c1, UP, buff=0.1),
                Create(cline1),
                FadeIn(c1),
                lag_ratio=0.3,
            )
        )
        self.play(
            LaggedStart(
                Create(ccline_c1),
                FadeIn(code_c1, shift=RIGHT, scale=0.5),
                lag_ratio=0.5,
            )
        )
        self.play(
            LaggedStart(
                head.animate.next_to(c2, UP, buff=0.1),
                Create(cline2),
                FadeIn(c2),
                lag_ratio=0.3,
            )
        )
        self.playw(
            LaggedStart(
                Create(ccline_c2), FadeIn(code_c2, shift=LEFT, scale=0.5), lag_ratio=0.5
            )
        )

        self.playw(
            LaggedStart(
                FadeOut(ccline_c2, code_c2, c2, cline2),
                head.animate.next_to(c1, UP, buff=0.1),
                lag_ratio=0.3,
            )
        )

        entire = VGroup(
            init, c1, cline1, code_init, code_c1, head, ccline_c1, ccline_init
        )
        gitreset_text = (
            lambda *text: ListText(*text, font="Noto Mono")[1:-1]
            .arrange(RIGHT, buff=0.5)
            .set_color_by_gradient(BLUE_B, BLUE_E)
            .next_to(head, UP, buff=1)
        )
        gitreset = gitreset_text("git", "reset", "|")
        gitreset[-1].set_opacity(0)
        self.playw(
            entire.animate.set_opacity(0.1),
            LaggedStart(*[FadeIn(item) for item in gitreset]),
        )
        commands = [
            ["git", "reset", "--soft"],
            ["git", "reset", "--mixed"],
            ["git", "reset", "--hard"],
        ]
        for c in commands:
            self.playw(gitreset.animate.become(gitreset_text(*c)), wait=0.5)
        self.wait(1)
        options_list = ["--soft", "--mixed", "--hard"]
        options = (
            VGroup(
                *[
                    Text(opt, font="Noto Mono", color=BLUE, font_size=36)
                    for opt in options_list
                ]
            )
            .arrange(DOWN, buff=0.75)
            .next_to(gitreset, RIGHT)
            .align_to(gitreset, UP)
        )
        self.playw(
            LaggedStart(
                *[FadeIn(opt, target_position=gitreset) for opt in options[:-1]],
                lag_ratio=0.1,
            ),
            gitreset[-1].animate.become(options[-1]),
            gitreset[:-1].animate.become(gitreset_text("git", "reset")),
        )

        self.play(self.cf.animate.shift(UP * 2))
        self.playw(LaggedStart(*[item.animate.set_color(PURE_RED) for item in options]))
        self.playw(Circumscribe(options[-1], color=PURE_RED))


class howtogitreset(Scene2D):
    def construct(self):
        init = get_commit()
        c1, cline1 = new_commit(init, direction="up")
        c2, cline2 = new_commit(c1, direction="up")

        graph = VGroup(init, c1, c2, cline1, cline2).shift(DOWN * 1.5)

        code_init = PythonCode("src/init.py").next_to(init, LEFT, buff=0.75)
        ccline_init = DashedLine(
            init.get_left(), code_init.get_right(), color=GREY_C, buff=0
        )
        hash_str = lambda item: hex(hash(item))[-6:]
        init_chash = chash(hash_str(code_init)).next_to(init, RIGHT, buff=0.1)
        code_c1 = PythonCode("src/c1.py").next_to(c1, RIGHT, buff=0.75)
        code_c1.code[-1].set_color(YELLOW)
        ccline_c1 = DashedLine(c1.get_right(), code_c1.get_left(), color=GREY_C, buff=0)
        c1_chash = chash(hash_str(code_c1)).next_to(c1, LEFT, buff=0.1)
        code_c2 = PythonCode("src/c2.py").next_to(c2, LEFT, buff=0.75)
        code_c2.code[-1].set_color(YELLOW)
        ccline_c2 = DashedLine(c2.get_left(), code_c2.get_right(), color=GREY_C, buff=0)
        c2_chash = chash(hash_str(code_c2(1))).next_to(c2, RIGHT, buff=0.1)

        head = Text("HEAD", font_size=24, color=GREEN_D).next_to(init, UP, buff=1)
        headarrow = Arrow(head.get_bottom(), init.get_top(), color=GREEN_D, buff=0.1)
        head = VGroup(head, headarrow).next_to(c2, UP, buff=0.1)

        entire_butchash = VGroup(
            init,
            c1,
            c2,
            cline1,
            cline2,
            code_init,
            code_c1,
            code_c2,
            ccline_c1,
            ccline_init,
            ccline_c2,
            head,
        )
        self.playw(FadeIn(entire_butchash))
        head.save_state()
        self.playw(
            LaggedStart(
                VGroup(ccline_c2, code_c2, c2, cline2).animate.set_opacity(0),
                head.animate.next_to(c1, UP, buff=0.1),
                lag_ratio=0.3,
            )
        )
        chashes = VGroup(init_chash, c1_chash, c2_chash)
        self.playw(
            Restore(head),
            entire_butchash[:-1].animate.set_opacity(0.2),
            FadeIn(chashes),
            # lag_ratio=0.3,
        )

        gitreset_text = (
            lambda *text: ListText(*text, font="Noto Mono")[1:-1]
            .arrange(RIGHT, buff=0.5)
            .set_color_by_gradient(BLUE_B, BLUE_E)
            .next_to(head, UP, buff=1)
        )
        gitreset = (
            gitreset_text("git", "reset", hash_str(code_c1))
            .arrange(RIGHT, buff=0.5, aligned_edge=UP)
            .scale(0.75)
            .next_to(head[0], RIGHT, buff=1)
        )
        self.playw(
            *[FadeIn(item) for item in gitreset[:-1]],
            Transform(c1_chash.copy(), gitreset[-1]),
        )


class togitcommit(Scene2D):
    def construct(self):
        init = get_commit()
        c1, cline1 = new_commit(init, direction="up")
        c2, cline2 = new_commit(c1, direction="up")

        graph = VGroup(init, c1, c2, cline1, cline2).shift(DOWN * 1.5)

        code_init = PythonCode("src/init.py").next_to(init, LEFT, buff=0.75)
        ccline_init = DashedLine(
            init.get_left(), code_init.get_right(), color=GREY_C, buff=0
        )
        hash_str = lambda item: hex(hash(item))[-6:]
        init_chash = chash(hash_str(code_init)).next_to(init, RIGHT, buff=0.1)
        code_c1 = PythonCode("src/c1.py").next_to(c1, RIGHT, buff=0.75)
        code_c1.code[-1].set_color(YELLOW)
        ccline_c1 = DashedLine(c1.get_right(), code_c1.get_left(), color=GREY_C, buff=0)
        c1_chash = chash(hash_str(code_c1)).next_to(c1, LEFT, buff=0.1)
        code_c2 = PythonCode("src/c2.py").next_to(c2, LEFT, buff=0.75)
        code_c2.code[-1].set_color(YELLOW)
        ccline_c2 = DashedLine(c2.get_left(), code_c2.get_right(), color=GREY_C, buff=0)
        c2_chash = chash(hash_str(code_c2(1))).next_to(c2, RIGHT, buff=0.1)

        head = Text("HEAD", font_size=24, color=GREEN_D).next_to(init, UP, buff=1)
        headarrow = Arrow(head.get_bottom(), init.get_top(), color=GREEN_D, buff=0.1)
        head = VGroup(head, headarrow).next_to(c2, UP, buff=0.1)

        entire_butchash = VGroup(
            init,
            c1,
            c2,
            cline1,
            cline2,
            code_init,
            code_c1,
            code_c2,
            ccline_c1,
            ccline_init,
            ccline_c2,
            head,
        )
        self.playw(FadeIn(entire_butchash))

        self.play(FadeOut(init, cline1, ccline_init, code_init))
        cline2.add_updater(lambda m: m.put_start_and_end_on(c1.get_top(), c2.get_bottom()))
        ccline_c1.add_updater(lambda m: m.put_start_and_end_on(c1.get_right(), code_c1.get_left()))
        code_c1.add_updater(lambda m: m.next_to(c1, RIGHT, buff=0.75))
        self.playw(c1.animate.shift(DOWN*2), self.cf.animate.shift(DOWN*0.5))

        dots = VGroup(*[Dot(color=BLUE).move_to(cline2.point_from_proportion(p)) for p in [1/3, 2/3]])
        self.playw(FadeIn(dots))
        modified = Text("modified: main.py", font_size=24, color=RED).next_to(code_c1, UP, buff=0.5).align_to(code_c1, LEFT)
        marrow = Arrow(modified.get_left(), dots[0].get_right(), color=WHITE, buff=0.05, stroke_width=2)
        staged = Text("to be committed: main.py", font_size=24, color=PURE_GREEN).next_to(modified, UP, buff=0.5).align_to(code_c1, LEFT)
        sarrow = Arrow(staged[1].get_left(), dots[1].get_right(), color=WHITE, buff=0.05, stroke_width=2)
        self.playw(LaggedStart(FadeIn(marrow), FadeIn(modified), lag_ratio=0.3))
        self.playw(LaggedStart(FadeIn(sarrow), FadeIn(staged), lag_ratio=0.3))

        prohibit_arrow = Arrow(c1.get_top(), c2.get_bottom(), color=PURE_RED, stroke_width=12, buff=0)
        self.playw(GrowArrow(prohibit_arrow))
        prohibit_arrow.generate_target()
        prohibit_arrow.target.rotate(120*DEGREES, about_point=prohibit_arrow.get_bottom()).shift(DOWN*3 + LEFT*2)
        self.playw(MoveToTarget(prohibit_arrow))

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