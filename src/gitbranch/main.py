from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        c0 = get_commit()
        c1, cline1 = new_commit(c0, direction="up")
        c2, cline2 = new_commit(c1, direction="up")
        c3, cline3 = new_commit(c2, direction="up")
        branch = VGroup(c0, cline1, c1, cline2, c2, cline3, c3)
        branch.shift(DOWN * 2)
        self.playw(LaggedStart(*[FadeIn(item) for item in branch], lag_ratio=0.3))

        b1c0, bline1 = new_commit(c3, direction="left")
        b2c0, bline2 = new_commit(c3, direction="right")

        branch1 = VGroup(b1c0, bline1).set_color(GREEN).set_fill(opacity=0)
        branch2 = VGroup(b2c0, bline2).set_color(BLUE).set_fill(opacity=0)
        self.play(LaggedStart(*[FadeIn(item) for item in branch1], lag_ratio=0.3))
        self.playw(LaggedStart(*[FadeIn(item) for item in branch2], lag_ratio=0.3))

        b1text = Text("Add login", font_size=24, color=GREEN).next_to(b1c0, UL)
        b2text = Text("Modify landing page", font_size=24, color=BLUE).next_to(b2c0, UR)
        self.playw(FadeIn(b1text))
        self.playw(FadeIn(b2text))

        branches = VGroup(branch, branch1, branch2)
        texts = VGroup(b1text, b2text)
        branches.save_state()
        texts.save_state()
        self.playw(
            VGroup(branch1, branch2).animate.set_opacity(0.2).set_fill(opacity=0),
            VGroup(b1text, b2text).animate.set_opacity(0.2),
            branch.animate.scale(1.2).align_to(branch, UP),
        )

        self.playw(Restore(branches), Restore(texts))

        b1c1, bcl11 = new_commit(b1c0, direction="up")
        VGroup(b1c1, bcl11).set_color(GREEN).set_fill(opacity=0)
        b2c1, bcl21 = new_commit(b2c0, direction="up")
        VGroup(b2c1, bcl21).set_color(BLUE).set_fill(opacity=0)
        b1c2, bcl12 = new_commit(b1c1, direction="up")
        VGroup(b1c2, bcl12).set_color(GREEN).set_fill(opacity=0)
        b2c2, bcl22 = new_commit(b2c1, direction="up")
        VGroup(b2c2, bcl22).set_color(BLUE).set_fill(opacity=0)

        self.play(LaggedStart(*[FadeIn(item) for item in [bcl11, b1c1]], lag_ratio=0.3))
        self.play(LaggedStart(*[FadeIn(item) for item in [bcl21, b2c1]], lag_ratio=0.3))
        self.play(LaggedStart(*[FadeIn(item) for item in [bcl12, b1c2]], lag_ratio=0.3))
        self.playw(
            LaggedStart(*[FadeIn(item) for item in [bcl22, b2c2]], lag_ratio=0.3)
        )

        merged2, mline2 = new_commit(c3, direction="up")
        merge_arrow2 = Arrow(
            start=b2c2.point_at_angle(-3 * PI / 4),
            end=merged2.point_at_angle(PI / 4),
            color=BLUE,
            buff=0,
        )
        self.play(GrowArrow(merge_arrow2))
        self.playw(
            LaggedStart(*[FadeIn(item) for item in [mline2, merged2]], lag_ratio=0.3)
        )
        merged1, mline1 = new_commit(merged2, direction="up")
        merge_arrow1 = Arrow(
            start=b1c2.get_right(),
            end=merged1.get_left(),
            color=GREEN,
            buff=0,
        )
        self.play(GrowArrow(merge_arrow1))
        self.playw(
            LaggedStart(*[FadeIn(item) for item in [mline1, merged1]], lag_ratio=0.3)
        )
        tilt_degree = 60
        self.move_camera_vertically(
            tilt_degree, zoom=1.3, added_anims=[texts.animate.set_opacity(0.4)]
        )
        # "new branch", "working on the branch", "commit", "merge"
        procedure1 = Text("New branch", font_size=24, color=WHITE).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )
        procedure2 = Text("Working on the branch", font_size=24, color=WHITE).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )
        procedure3 = Text("Commit", font_size=24, color=WHITE).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )
        procedure4 = Text("Merge", font_size=24, color=WHITE).rotate(
            tilt_degree * DEGREES, axis=RIGHT
        )
        procedure = (
            VGroup(procedure1, procedure2, procedure3, procedure4)
            .arrange(RIGHT, buff=0.5)
            .shift(OUT * 2)
        )

        for p in procedure:
            self.playw(FadeIn(p))

        self.playw(
            LaggedStart(
                FadeOut(procedure2, procedure3),
                VGroup(procedure1, procedure4)
                .animate.arrange(RIGHT, buff=0.75)
                .shift(OUT * 2),
                lag_ratio=0.5,
            )
        )

        # fade out the commits which appears after the new branches
        fadeouts = AnimationGroup(
            *[
                FadeOut(item)
                for item in [
                    b1c0,
                    b2c0,
                    bcl11,
                    bcl21,
                    bcl12,
                    bcl22,
                    b1c1,
                    b2c1,
                    b1c2,
                    b2c2,
                    bline1,
                    bline2,
                    merge_arrow1,
                    merge_arrow2,
                    mline1,
                    mline2,
                    merged1,
                    merged2,
                    texts,
                    procedure4,
                ]
            ]
        )
        self.move_camera_vertically(
            0,
            zoom=1.0,
            added_anims=[
                fadeouts,
                procedure1.animate.rotate(-tilt_degree * DEGREES, axis=RIGHT)
                .shift(LEFT)
                .set_color(GREEN),
            ],
        )
        self.playw(FadeIn(bline1, b1c0))
        self.play(FadeIn(b1c1, bcl11))
        self.playw(FadeIn(b1c2, bcl12))


class gitcheckoutCommithash(Scene3D):
    def construct(self):
        self.cf.shift(IN * 1.5)
        c0 = get_commit()
        chash0 = chash("abc123").next_to(c0, LEFT)
        c1, cline1 = new_commit(c0, direction="up")
        chash1 = chash("bcd456").next_to(c1, LEFT)
        c2, cline2 = new_commit(c1, direction="up")
        chash2 = chash("cde789").next_to(c2, LEFT)
        c3, cline3 = new_commit(c2, direction="up")
        chash3 = chash("def012").next_to(c3, LEFT)
        branch = VGroup(
            c0, cline1, c1, cline2, c2, cline3, c3, chash0, chash1, chash2, chash3
        )
        branch.shift(DOWN)

        head = Text("HEAD", font_size=24, color=WHITE).next_to(c3, UR, buff=1)
        heada = Arrow(
            head.get_left(),
            c3.point_at_angle(PI / 4),
            buff=0.1,
            color=GREY_B,
            stroke_width=2,
            tip_length=0.2,
        )
        head = VGroup(head, heada)
        self.addw(branch, head)

        command = Text(
            "git checkout bcd456", font_size=24, font="Noto Mono", color=GREY_A
        ).shift(UP * 3 + LEFT * 3)
        self.playw(
            LaggedStart(*[FadeIn(c, run_time=0.1) for c in command], lag_ratio=0.4)
        )
        self.playw(
            Indicate(command[11:]),
            Indicate(chash1),
            head.animate.align_to(c1.point_at_angle(PI / 4), DOWN),
        )


class outro(Scene3D):
    def construct(self):

        c0 = get_commit()
        c1, cline1 = new_commit(c0, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        c3, cline3 = new_commit(c2, direction="right")
        branch = VGroup(c0, cline1, c1, cline2, c2, cline3, c3).move_to(ORIGIN)
        head = Text("HEAD", font_size=24, color=GREY_A).next_to(c3, UR, buff=0.75)
        heada = Arrow(
            head.get_bottom(),
            c3.point_at_angle(PI / 4),
            buff=0.1,
            color=GREY_B,
            stroke_width=2,
            tip_length=0.2,
        )
        head = VGroup(head, heada)
        self.play(LaggedStart(*[FadeIn(item) for item in branch], lag_ratio=0.3))
        self.playw(FadeIn(head))

        gitbranch_command = Text(
            "git branch piui", font="Noto Mono", color=GREEN, font_size=24
        ).shift(UP * 2)
        piuib, pline = new_commit(c3, direction="up")
        piuib.set_color(GREEN).set_fill(opacity=0)
        pline.set_color(GREEN)
        self.playw(
            LaggedStart(
                *[FadeIn(c, run_time=0.1) for c in gitbranch_command], lag_ratio=0.4
            )
        )
        self.playw(
            LaggedStart(
                Transform(
                    gitbranch_command[:9],
                    VGroup(pline, piuib),
                    replace_mobject_with_target_in_scene=True,
                ),
                gitbranch_command[9:].animate.next_to(piuib, LEFT, buff=0.2).scale(0.8),
                lag_ratio=0.3,
            )
        )

        gitcheckout_command = Text(
            "git checkout piui", font="Noto Mono", color=GREEN, font_size=24
        ).shift(UP * 2)
        self.playw(
            LaggedStart(
                *[FadeIn(c, run_time=0.1) for c in gitcheckout_command], lag_ratio=0.4
            )
        )
        self.playw(
            FadeOut(gitcheckout_command), head.animate.align_to(piuib.get_right(), DOWN)
        )
        pc1, pcline1 = new_commit(piuib, direction="right")
        pc1.set_color(GREEN).set_fill(opacity=0)
        pcline1.set_color(GREEN)
        pc2, pcline2 = new_commit(pc1, direction="right")
        pc2.set_color(GREEN).set_fill(opacity=0)
        pcline2.set_color(GREEN)
        self.playw(
            LaggedStart(
                FadeIn(pcline1),
                head.animate.align_to(pc1.get_right(), LEFT),
                FadeIn(pc1),
                lag_ratio=0.3,
            )
        )
        self.playw(
            LaggedStart(
                FadeIn(pcline2),
                head.animate.align_to(pc2.get_right(), LEFT),
                FadeIn(pc2),
                lag_ratio=0.3,
            )
        )

        c4, cline4 = new_commit(c3, direction="right")
        marrow = Arrow(
            start=pc2.point_at_angle(-3 * PI / 4),
            end=c4.point_at_angle(PI / 4),
            color=GREEN,
            buff=0.0,
            stroke_width=2,
            tip_length=0.2,
        )
        self.playw(
            GrowArrow(marrow), LaggedStart(FadeIn(cline4), FadeIn(c4), lag_ratio=0.3)
        )
        self.playw(
            branch.animate.set_opacity(0.2).set_fill(opacity=0),
            gitbranch_command[9:].animate.set_opacity(0.2),
            VGroup(pline, piuib, pcline1, pc1, pcline2)
            .animate.set_opacity(0.2)
            .set_fill(opacity=0),
            head.animate.set_opacity(0.2),
        )


get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=24, color=RED)


def new_commit(from_commit, *, direction="right"):
    direction_np = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}[direction]
    newc = get_commit().next_to(from_commit, direction=direction_np, buff=0.5)
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
