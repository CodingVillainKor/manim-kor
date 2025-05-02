from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class init(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(45)

        init_commit = get_commit().shift(DOWN * 3)
        c1, cline1 = new_commit(init_commit, direction="up")
        c2, cline2 = new_commit(c1, direction="up")
        c3, cline3 = new_commit(c2, direction="up")
        c4, cline4 = new_commit(c3, direction="up")
        head_arrow = Arrow(
            c4.get_top() + UP + RIGHT,
            c4.get_right(),
            color=GREEN,
            buff=0.1,
            stroke_width=3,
            tip_length=0.2,
        )
        head_arrow_label = (
            Text("HEAD", font_size=24, color=GREEN)
            .rotate(45 * DEGREES, RIGHT)
            .next_to(head_arrow.start, UP)
        )
        head = VGroup(head_arrow, head_arrow_label)
        self.play(FadeIn(init_commit))
        self.play(LaggedStart(Create(cline1), FadeIn(c1), lag_ratio=0.5))
        self.play(LaggedStart(Create(cline2), FadeIn(c2), lag_ratio=0.5))
        self.play(LaggedStart(Create(cline3), FadeIn(c3), lag_ratio=0.5))
        self.play(LaggedStart(Create(cline4), FadeIn(c4), lag_ratio=0.5))
        self.playw(FadeIn(head))

        head.save_state()
        self.playw(head.animate.shift(DOWN * 2.6))
        self.playw(Restore(head))
        self.playw(
            head.animate.shift(DOWN * 1.3), VGroup(c4, cline4).animate.set_opacity(0)
        )

        new_branch, nb_line = new_commit(c3, direction="left")
        new_branch.set_color(BLUE).set_fill(BLACK, opacity=1)
        nb_line.set_color(BLUE_B)
        self.playw(LaggedStart(Create(nb_line), FadeIn(new_branch), lag_ratio=0.5))

        graph = VGroup(
            init_commit,
            c1,
            c2,
            c3,
            cline1,
            cline2,
            cline3,
            new_branch,
            nb_line,
        )
        remote = graph.copy()
        github = (
            Text("Github", font_size=36, color=GREY_B)
            .next_to(remote[-2], LEFT)
            .set_opacity(0)
        )
        github.generate_target().shift(OUT * 3 + LEFT * 2).set_opacity(0.5)
        remote.generate_target().shift(OUT * 3 + LEFT * 2).set_opacity(0.5)
        self.playw(MoveToTarget(remote), MoveToTarget(github))

        self.play(FadeOut(remote, github))
        self.playw(FadeOut(nb_line, new_branch))
        self.move_camera_vertically(
            0,
            added_anims=[
                head[1].animate.rotate(-45 * DEGREES, RIGHT).shift(UP * 0.8),
                head[0].animate.shift(UP),
                VGroup(init_commit, c1, c2, c3, cline1, cline2, cline3).animate.shift(
                    UP
                ),
            ],
        )


class gitaddcommit(Scene2D):
    def construct(self):
        init_commit = get_commit().shift(DOWN * 2 + LEFT * 3)
        c1, cline1 = new_commit(init_commit, direction="right", buff=1.5)
        c2, cline2 = new_commit(c1, direction="right", buff=1.5)
        c3, cline3 = new_commit(c2, direction="right", buff=1.5)

        file = PythonCode("src/file.py").scale(0.8)
        filet = (
            Text("file.py", font_size=18, color=GREY_C)
            .next_to(file, UP, buff=0.05)
            .align_to(file, LEFT)
        )
        fileg = VGroup(file, filet)
        stage = RoundedRectangle(width=4, height=5, color=GREY_C, stroke_width=3).scale(
            0.8
        )
        stage_label = Text("Staging Area", font_size=24, color=BLUE_B).next_to(
            stage, UP, buff=-0.5
        )
        stage = VGroup(stage, stage_label)

        VGroup(fileg, stage).arrange(RIGHT, buff=1).shift(UP)

        file.code[1].save_state()
        file.code[3].save_state()
        file.code[4].save_state()
        file.code[1:].set_opacity(0)
        self.playw(FadeIn(init_commit, scale=1.5))
        self.playw(FadeIn(fileg, stage))

        file.code[1].set_color(GREEN_E)
        file.code[3].set_color(GREEN_E)
        file.code[4].set_color(GREEN_E)
        self.playw(
            LaggedStart(
                *[c.animate.set_opacity(1) for c in file.code[1]], lag_ratio=0.05
            )
        )

        gitadd = lambda: Text(
            "git add file.py", font="Noto Mono", font_size=18, color=WHITE
        )
        gitcommit = lambda: Text(
            "git commit", font="Noto Mono", font_size=18, color=WHITE
        )

        gitadd1 = gitadd().next_to(cline1, UP, buff=0.2)
        gitcommit1 = gitcommit().next_to(cline1, UP, buff=0.2)
        self.playw(
            FadeIn(gitadd1, shift=UP * 0.3, scale=0.6),
            Create(cline1),
            (filetc := filet.copy()).animate.move_to(stage),
            (code1c := file.code[1].copy()).animate.move_to(stage).shift(DOWN * 0.4),
        )
        self.playw(
            FadeIn(gitcommit1, shift=UP * 0.3, scale=0.6),
            gitadd1.animate.shift(UP * 0.4).set_opacity(0),
        )
        staged = VGroup(filetc, code1c)
        self.play(
            FadeOut(gitcommit1, scale=1.3, shift=UP * 0.3),
            Transform(staged, c1, replace_mobject_with_target_in_scene=True),
        )
        self.playw(Restore(file.code[1]))

        gitadd2 = gitadd().next_to(cline2, UP, buff=0.2)
        gitcommit2 = gitcommit().next_to(cline2, UP, buff=0.2)
        self.playw(
            LaggedStart(
                *[c.animate.set_opacity(1) for c in file.code[3]], lag_ratio=0.05
            )
        )
        self.playw(
            FadeIn(gitadd2, shift=UP * 0.3, scale=0.6),
            Create(cline2),
            (filetc := filet.copy()).animate.move_to(stage),
            (code2c := file.code[3].copy())
            .animate.move_to(stage)
            .scale(0.6)
            .shift(DOWN * 0.4),
        )
        self.playw(
            FadeIn(gitcommit2, shift=UP * 0.3, scale=0.6),
            gitadd2.animate.shift(UP * 0.4).set_opacity(0),
        )
        staged = VGroup(filetc, code2c)
        self.play(
            FadeOut(gitcommit2, scale=1.3, shift=UP * 0.3),
            Transform(staged, c2, replace_mobject_with_target_in_scene=True),
        )
        self.playw(Restore(file.code[3]))

        gitadd3 = gitadd().next_to(cline3, UP, buff=0.2)
        gitcommit3 = gitcommit().next_to(cline3, UP, buff=0.2)
        self.playw(
            LaggedStart(
                *[c.animate.set_opacity(1) for c in file.code[4]], lag_ratio=0.05
            )
        )
        self.playw(
            FadeIn(gitadd3, shift=UP * 0.3, scale=0.6),
            Create(cline3),
            (filetc := filet.copy()).animate.move_to(stage),
            (code3c := file.code[4].copy()).animate.move_to(stage).shift(DOWN * 0.4),
        )
        self.playw(
            FadeIn(gitcommit3, shift=UP * 0.3, scale=0.6),
            gitadd3.animate.shift(UP * 0.4).set_opacity(0),
        )
        staged = VGroup(filetc, code3c)
        self.play(
            FadeOut(gitcommit3, scale=1.3, shift=UP * 0.3),
            Transform(staged, c3, replace_mobject_with_target_in_scene=True),
        )
        self.playw(Restore(file.code[4]))


class gitcheckoutreset(Scene2D):
    def construct(self):
        init_commit = get_commit().shift(DOWN + LEFT * 3)
        inithash = chash("a1b2c3").next_to(init_commit, UP, buff=0.2)
        c1, cline1 = new_commit(init_commit, direction="right", buff=1.5)
        ch1 = chash("d4e5f6").next_to(c1, UP, buff=0.2)
        c2, cline2 = new_commit(c1, direction="right", buff=1.5)
        ch2 = chash("g7h8i9").next_to(c2, UP, buff=0.2)
        c3, cline3 = new_commit(c2, direction="right", buff=1.5)
        ch3 = chash("j0k1l2").next_to(c3, UP, buff=0.2)
        head_arrow = Arrow(
            c3.get_top() + UP + RIGHT,
            c3.get_right(),
            color=GREEN,
            buff=0.1,
            stroke_width=3,
            tip_length=0.2,
        )
        head = Text("HEAD", font_size=24, color=GREEN).next_to(
            head_arrow.start, UR, buff=0.1
        )
        head = VGroup(head, head_arrow)
        self.addw(init_commit, c1, c2, c3, cline1, cline2, cline3, head)

        gitlog_cmd = Text(
            "git log --oneline", font_size=32, color=WHITE, font="Noto Mono"
        ).set_color_by_gradient(YELLOW_B, YELLOW_E)
        self.playw(LaggedStart(*[FadeIn(c) for c in gitlog_cmd], lag_ratio=0.05))
        self.playw(FadeOut(gitlog_cmd, shift=DOWN * 0.5, scale=1.5))
        self.playw(
            LaggedStart(*[FadeIn(h) for h in [inithash, ch1, ch2, ch3]], lag_ratio=0.3)
        )

        self.playw(
            LaggedStart(
                AnimationGroup(
                    head_arrow.animate.become(
                        Arrow(
                            c3.get_bottom() + DOWN + RIGHT,
                            c3.get_bottom(),
                            color=GREEN,
                            buff=0.1,
                            stroke_width=3,
                            tip_length=0.2,
                        )
                    ),
                    head[0].animate.shift(DOWN * 2.5),
                ),
                self.cf.animate.shift(DOWN),
                lag_ratio=0.3,
            )
        )
        graph = VGroup(init_commit, c1, c2, c3, cline1, cline2, cline3)
        gitcheckout = lambda t: Text(
            f"git checkout {t}", font="Noto Mono", font_size=24
        ).set_color_by_gradient(YELLOW_B, YELLOW_E)
        gc1 = gitcheckout("d4e5f6").next_to(graph, DOWN, buff=0.3)
        self.playw(FadeIn(gc1))
        head.save_state()
        self.playw(head.animate.align_to(cline2, LEFT), FadeOut(gc1))

        gc2 = gitcheckout("j0k1l2").next_to(c3, DOWN, buff=0.3)
        self.playw(FadeIn(gc2))
        self.playw(gc2.animate.become(gitcheckout("-").next_to(c3, DOWN, buff=0.3)))
        self.playw(Restore(head), FadeOut(gc2))

        gitreset = lambda t: Text(
            f"git reset {t}", font="Noto Mono", font_size=24
        ).set_color_by_gradient(YELLOW_B, YELLOW_E)
        gr1 = gitreset("d4e5f6").next_to(graph, DOWN, buff=0.3)
        file = PythonCode("src/file.py").scale(0.8).next_to(graph, UP, buff=1)
        self.play(FadeIn(file))
        self.playw(FadeIn(gr1), scale=1.3)
        self.play(
            head.animate.align_to(cline2, LEFT),
            FadeOut(gr1, shift=UP * 0.5, scale=1.5),
            VGroup(c3, cline3, c2, cline2, ch3, ch2).animate.set_opacity(0),
        )
        modified = SurroundingRect(color=RED_E, stroke_width=3).surround(file.code[3:])
        modifiedt = (
            Text("Modified", font_size=18, color=RED_E)
            .next_to(modified, UP, buff=0.05)
            .align_to(modified, RIGHT)
        )
        self.playw(FadeIn(modified, scale=1.1), FadeIn(modifiedt))

        git_restore = (
            Text("git restore file.py", font="Noto Mono", font_size=24)
            .set_color_by_gradient(YELLOW_B, YELLOW_E)
            .next_to(c1, RIGHT, buff=2)
        )
        self.playw(FadeIn(git_restore, scale=1.3))
        self.playw(FadeOut(git_restore), FadeOut(modified, modifiedt, file.code[3:]))


class gitbranchPreview(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(45)

        init_commit = get_commit().shift(DOWN * 3)
        c1, cline1 = new_commit(init_commit, direction="up")
        c2, cline2 = new_commit(c1, direction="up")
        c3, cline3 = new_commit(c2, direction="up")
        head_arrow = Arrow(
            c3.get_top() + UP + RIGHT,
            c3.get_right(),
            color=GREEN,
            buff=0.1,
            stroke_width=3,
            tip_length=0.2,
        )
        head_arrow_label = (
            Text("HEAD", font_size=24, color=GREEN)
            .rotate(45 * DEGREES, RIGHT)
            .next_to(head_arrow.start, UP)
        )
        head = VGroup(head_arrow, head_arrow_label)
        self.add(init_commit, c1, c2, c3, cline1, cline2, cline3, head)

        branch_start, bline = new_commit(c3, direction="left")
        branch_start.set_color(BLUE).set_fill(BLACK, opacity=1)
        bline.set_color(BLUE_B)
        self.add(bline, branch_start)
        bc1, bcline1 = new_commit(branch_start, direction="up")
        bc1.set_color(BLUE).set_fill(BLACK, opacity=1)
        bcline1.set_color(BLUE_B)
        c4, cline4 = new_commit(c3, direction="up")
        bc2, bcline2 = new_commit(bc1, direction="up")
        bc2.set_color(BLUE).set_fill(BLACK, opacity=1)
        bcline2.set_color(BLUE_B)
        c5, cline5 = new_commit(c4, direction="up")
        self.playw(FadeOut(head))
        self.play(LaggedStart(Create(bcline1), FadeIn(bc1), lag_ratio=0.5))
        self.playw(LaggedStart(Create(cline4), FadeIn(c4), lag_ratio=0.5))
        self.play(LaggedStart(Create(bcline2), FadeIn(bc2), lag_ratio=0.5))
        self.playw(LaggedStart(Create(cline5), FadeIn(c5), lag_ratio=0.5))

        merge_line = Arrow(
            bc2.get_right(),
            c5.get_left(),
            color=YELLOW,
            buff=0,
            stroke_width=3,
            tip_length=0.2,
        )
        conflict = Text("Conflict", font_size=24, color=PURE_RED).rotate(45*DEGREES, RIGHT).next_to(
            merge_line, UP, buff=0.3
        )
        self.play(GrowArrow(merge_line))
        self.playw(FadeIn(conflict, shift=UP * 0.5, scale=0.7))
        self.playw(self.cf.animate.shift(UP*10+LEFT*0.7+IN*6))


get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=20, color=RED)


def new_commit(from_commit, *, direction="right", buff=1):
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
    return newc, cline
