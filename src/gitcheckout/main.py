from manim import *
from raenim import *
from random import seed

seed(41)

Commit = lambda: Circle(
    radius=0.15, color=GREY_A, stroke_width=4, fill_color=BLACK, fill_opacity=1
).set_z_index(1)


class intro(Scene2D):
    def construct(self):
        c0 = Commit().shift(UP)
        file1 = PythonCode("src/file1.py").next_to(c0, DOWN, buff=1)
        c0f = DashedLine(c0.get_center(), file1.get_top(), color=GREY_B, stroke_width=2)
        self.play(FadeIn(c0))
        self.playw(FadeIn(file1, target_position=c0, scale=0.2), Create(c0f))

        c1 = Commit().next_to(c0, RIGHT, buff=3)
        file2 = PythonCode("src/file2.py").next_to(c1, DOWN, buff=1)
        file2.code[-1].set_color(YELLOW)
        line = Line(c0.get_center(), c1.get_center(), color=GREY_B, stroke_width=2)
        gitadd = Text("git add", font_size=24).next_to(line, UP).set_color(GREY_B)
        gitcommit = (
            Text('git commit -m "add print"', font_size=24)
            .next_to(line, UP)
            .set_color(GREY_B)
        )
        gitadd_anim = [FadeIn(gitadd), gitadd.animate.shift(UP * 0.5), FadeOut(gitadd)]
        gitcommit_anim = [
            FadeIn(gitcommit),
            gitcommit.animate.shift(UP * 0.5),
            FadeOut(gitcommit),
        ]
        symbol_anim = [Create(line), FadeIn(c1), self.cf.animate.shift(RIGHT)]
        anims = SkewedAnimations(gitadd_anim, symbol_anim, gitcommit_anim)
        for anim in anims:
            self.play(anim)
        c1f = DashedLine(c1.get_center(), file2.get_top(), color=GREY_B, stroke_width=2)
        self.playw(
            FadeIn(file2, target_position=c1, scale=0.2),
            Create(c1f),
            file1.animate.shift(LEFT),
        )
        HEAD = Arrow(
            c1.get_top() + UP, c1.get_top(), color=GREEN_C, stroke_width=2, buff=0.1
        )
        headt = Text("HEAD", font_size=24, color=GREEN_C).next_to(HEAD, UP, buff=0.1)
        HEAD = VGroup(HEAD, headt)
        self.playw(FadeIn(HEAD))

        version1 = Text("v1", font_size=24, color=GREY_B).next_to(c0, DL, buff=0.1)
        version2 = Text("v2", font_size=24, color=GREY_B).next_to(c1, DR, buff=0.1)
        self.playw(LaggedStart(*[FadeIn(version1), FadeIn(version2)], lag_ratio=0.5))
        self.playw(Indicate(c0))
        self.playw(Indicate(c1))

        file2.save_state()
        self.playw(
            HEAD.animate.next_to(c0, UP, buff=0.1), file2.animate.set_opacity(0.2)
        )
        self.playw(
            HEAD.animate.next_to(c1, UP, buff=0.1),
            Restore(file2),
            file1.animate.set_opacity(0.2),
        )


class githashcheckout(Scene2D):
    def construct(self):
        c0 = Commit().shift(UP)
        file1 = PythonCode("src/file1.py").next_to(c0, DOWN, buff=1)
        c0f = DashedLine(c0.get_center(), file1.get_top(), color=GREY_B, stroke_width=2)
        c1 = Commit().next_to(c0, RIGHT, buff=3)
        file2 = PythonCode("src/file2.py").next_to(c1, DOWN, buff=1)
        file2.code[-1].set_color(YELLOW)
        line = Line(c0.get_center(), c1.get_center(), color=GREY_B, stroke_width=2)
        c1f = DashedLine(c1.get_center(), file2.get_top(), color=GREY_B, stroke_width=2)
        head = Arrow(
            c1.get_top() + UP, c1.get_top(), color=GREEN_C, stroke_width=2, buff=0.1
        )
        headt = Text("HEAD", font_size=24, color=GREEN_C).next_to(head, UP, buff=0.1)
        head = VGroup(head, headt)

        version1 = Text("v1", font_size=24, color=GREY_B).next_to(c0, DL, buff=0.1)
        version2 = Text("v2", font_size=24, color=GREY_B).next_to(c1, DR, buff=0.1)
        starting = VGroup(
            c0, file1, c0f, line, c1, file2, c1f, head, version1, version2
        )
        file1.shift(LEFT)
        self.cf.move_to(starting).align_to(self.cf, UP)
        self.playw(FadeIn(starting))

        commithash1 = (
            Text("fd96c2b77608451a412ded7d3ba71614e077bc23", font_size=16, color=GREY_B)
            .next_to(c0, DL, buff=0.1)
            .align_to(version1, RIGHT)
        )
        commithash2 = (
            Text("b40c2c3b3fc15ef9e34da5a5b2d5556fb1adf7fc", font_size=16, color=GREY_B)
            .next_to(c1, DR, buff=0.1)
            .align_to(version2, LEFT)
        )
        self.playw(Transform(version1, commithash1, replace_mobject_with_target_in_scene=True))
        commithash1.generate_target()
        commithash1.target[4:].set_opacity(0)
        commithash1.target[:4].set_color(YELLOW).scale(1.3).align_to(commithash1, RIGHT)
        self.playw(MoveToTarget(commithash1))

        entire = VGroup(starting, commithash1)
        entire.generate_target()
        entire.target.shift(UP*1.5)
        VGroup(entire.target[0][1:3], entire.target[0][5:7]).set_opacity(0)
        self.playw(MoveToTarget(entire))

class whygitcheckout(Scene2D):
    def construct(self):
        c0, c1, c2 = [Commit() for _ in range(3)]
        cs = VGroup(*[c0, c1, c2])
        f0, f1, f2 = [PythonCode(f"src/file{i+1}.py") for i in range(3)]
        fs = VGroup(*[f0, f1, f2]).arrange(RIGHT, buff=0.75, aligned_edge=UP)
        f1.code[-1].set_color(YELLOW)
        f2.code[-1].set_color(YELLOW)

        for c, f in zip(cs, fs):
            c.next_to(f, UP, buff=0.5)
        c0f, c1f, c2f = [
            DashedLine(c.get_center(), f.get_top(), color=GREY_B, stroke_width=2)
            for c, f in zip(cs, fs)
        ]
        cfs = VGroup(*[c0f, c1f, c2f])

        line0 = Line(c0.get_center(), c1.get_center(), color=GREY_B, stroke_width=2)
        line1 = Line(c1.get_center(), c2.get_center(), color=GREY_B, stroke_width=2)
        lines = VGroup(line0, line1)
        starting = VGroup(cs, fs, cfs, lines)

        head = Arrow(
            c2.get_top() + UP, c2.get_top(), color=GREEN_C, stroke_width=2, buff=0.1
        )
        headt = Text("HEAD", font_size=24, color=GREEN_C).next_to(head, UP, buff=0.1)
        head = VGroup(head, headt)
        self.playw(FadeIn(head, starting))
        head.save_state()
        self.playw(head.animate.next_to(c0, UP, buff=0.1))
        self.playw(Restore(head))

        # git reset

        self.playw(head.animate.next_to(c1, UP, buff=0.1), FadeOut(cs[-1], lines[-1], cfs[-1], f2))
