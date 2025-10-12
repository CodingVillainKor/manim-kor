from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        self.add_sound("a.mp3")
        start = get_commit()
        sc = start.copy().set_opacity(0)
        c1, cline1 = new_commit(start, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        c3, cline3 = new_commit(c2, direction="right")
        b1, bline1 = new_commit(c3, direction="down")
        VGroup(b1, bline1).set_color(GREEN)
        b1.set_fill(opacity=0)
        VGroup(start, c1, cline1, c2, cline2, c3, cline3, b1, bline1).move_to(
            ORIGIN
        ).align_to(sc, UP)

        self.playw(FadeIn(start))

        self.play(LaggedStart(FadeIn(cline1), FadeIn(c1), lag_ratio=0.5), run_time=0.5)
        self.play(LaggedStart(FadeIn(cline2), FadeIn(c2), lag_ratio=0.5), run_time=0.5)
        self.play(LaggedStart(FadeIn(cline3), FadeIn(c3), lag_ratio=0.5), run_time=0.5)
        gitbranch = Text(
            "git branch new.branch", font="Noto Mono", color=RED, font_size=24
        ).next_to(b1, DOWN)
        self.playw(
            LaggedStart(
                FadeIn(bline1),
                FadeIn(b1),
                FadeIn(gitbranch, shift=RIGHT * 0.5),
                lag_ratio=0.5,
            ),
            run_time=1,
        )
        bc2, bcline2 = new_commit(b1, direction="right")
        VGroup(bc2, bcline2).set_color(GREEN).set_fill(opacity=0)
        bc3, bcline3 = new_commit(bc2, direction="right")
        VGroup(bc3, bcline3).set_color(GREEN).set_fill(opacity=0)
        c4, cline4 = new_commit(c3, direction="right")

        self.play(
            LaggedStart(
                self.cf.animate.shift(RIGHT * 3),
                FadeIn(bcline2),
                FadeIn(bc2),
                lag_ratio=0.5,
            ),
            run_time=1.0,
        )
        self.playw(
            LaggedStart(FadeIn(bcline3), FadeIn(bc3), lag_ratio=0.5),
            run_time=0.5,
            wait=2.5,
        )
        mline = Arrow(
            bc3.get_top(),
            c4.get_bottom(),
            color=GREEN,
            stroke_width=2,
            tip_length=0.2,
            buff=0,
        )
        gitmerge = Text(
            "git merge new.branch", font="Noto Mono", color=RED, font_size=24
        ).next_to(mline, UR, buff=-0.4)
        self.playw(
            LaggedStart(
                FadeIn(gitmerge),
                FadeIn(mline),
                FadeIn(c4),
                FadeIn(cline4),
                lag_ratio=0.5,
            ),
            run_time=1.5,
            wait=0.1,
        )
        self.playw(
            VGroup(
                start,
                c1,
                cline1,
                c2,
                cline2,
                c3,
                cline3,
                b1,
                bline1,
                bc2,
                bcline2,
                bcline3,
            )
            .animate.set_opacity(0.2)
            .set_fill(opacity=0),
            gitbranch.animate.set_opacity(0.2),
        )
        self.playw(Circumscribe(gitmerge, color=RED, buff=0.08), wait=6)
        self.cf.save_state()
        self.playw(self.cf.animate.move_to(mline).scale(0.7), run_time=3, wait=4.5)

        mlinebroken = BrokenLine(
            bc3.get_top(),
            bc3.get_top() + UP * 0.8 + LEFT * 0.6,
            c4.get_bottom() + DOWN * 0.8 + LEFT * 0.3,
            c4.get_bottom(),
            color=GREEN,
            arrow=True,
            stroke_width=2,
            tip_length=0.2,
        ).set_color(PURE_RED)
        self.playw(
            LaggedStart(
                FadeOut(mline),
                *[FadeIn(mlinebroken[i]) for i in range(len(mlinebroken))],
            ),
            wait=2.5,
        )
        self.playw(
            Transform(mlinebroken, mline, replace_mobject_with_target_in_scene=True)
        )
        self.playw(FadeOut(mline, cline4, c4, gitmerge), wait=2.5)
        self.playw(Restore(self.cf), FadeIn(mline, cline4, c4, gitmerge), run_time=3)


class whygitmerge(Scene3D):
    def construct(self):
        # self.add_sound("b.mp3")
        prj = FileSystem(
            folders=["tools", "src"], files=["util.py", "main.py"], tag="project"
        )
        prj.tag.scale(0.7).align_to(prj.tag, DOWN)
        self.playw(FadeIn(prj))

        c0 = get_commit().shift(DOWN)
        c1, cline1 = new_commit(c0, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        commits = VGroup(c0, cline1, c1, cline2, c2).align_to(c0, RIGHT)
        unit_direction = -2.3 * np.array([3**0.5 / 2, 0, 1 / 2])
        self.play(
            prj.animate.rotate(-PI / 6, axis=UP).shift(
                IN * 6 + 2 * unit_direction + UP * 2
            ),
            FadeTransform(prj.copy(), commits),
            run_time=0.7,
        )
        link0 = DashedLine(
            c0.get_top(), prj.get_bottom(), color=RED, dashed_ratio=0.2, stroke_width=3
        )
        modified = lambda: Text("[M]", font_size=24, color=RED)
        m1 = modified().next_to(prj.files[0], -unit_direction, buff=0.55)
        m1line = DashedLine(
            prj.files[0].get_right(),
            m1.get_left(),
            color=GREY_B,
            dashed_ratio=0.7,
            stroke_width=3,
        )
        m1 = VGroup(m1, m1line)
        link1 = DashedLine(
            c1.get_top(),
            m1[0].get_bottom(),
            color=RED_B,
            dashed_ratio=0.7,
            stroke_width=2,
            dash_length=0.3,
        ).set_opacity(0.5)
        m2 = modified().next_to(prj.files[1], -unit_direction, buff=1.45)
        m2line = DashedLine(
            prj.files[1].get_right(),
            m2.get_left(),
            color=GREY_B,
            dashed_ratio=0.7,
            stroke_width=3,
        )
        m2 = VGroup(m2, m2line)
        link2 = DashedLine(
            c2.get_top(),
            m2[0].get_bottom(),
            color=RED_B,
            dashed_ratio=0.7,
            stroke_width=2,
            dash_length=0.3,
        ).set_opacity(0.5)

        self.playw(
            Create(link0),
            Create(link1),
            FadeIn(m1),
            Create(link2),
            FadeIn(m2),
            run_time=0.8,
            wait=0.5,
        )
        b1, bline = new_commit(c2, direction="down", buff=0.5)
        b1.set_color(GREEN).set_fill(opacity=0)
        self.playw(FadeIn(bline, b1), wait=3)
        load_file = (
            VGroup(Text("Load", font_size=24, color=GREEN), FileIcon(size=0.2))
            .arrange(RIGHT, buff=0.1)
            .next_to(b1, RIGHT)
        )
        self.play(FadeIn(load_file, shift=RIGHT * 0.5))
        self.playw(Circumscribe(VGroup(b1, load_file), color=GREEN, buff=0.1), wait=2)
        maint = Text("main", font_size=24, color=GREY_C).next_to(c2, UR, buff=0.1)
        self.playw(FadeIn(maint), FadeOut(load_file))
        maint.save_state()
        self.playw(
            maint.animate.scale(1.5)
            .align_to(maint, DL)
            .set_color_by_gradient(YELLOW, RED),
            run_time=3,
        )
        self.playw(Restore(maint), run_time=0.5)

        edit = modified().next_to(m2, -unit_direction, buff=0.55)
        editline = DashedLine(
            m2.get_right(),
            edit.get_left(),
            color=GREY_B,
            dashed_ratio=0.7,
            stroke_width=3,
        )
        self.playw(FadeIn(edit, editline))
        self.playw(VGroup(edit, editline).animate.set_color(PURE_RED))

        nb = VGroup(b1, bline)
        nb.save_state()
        self.playw(
            nb.animate.scale(1.5).align_to(nb, UP).set_color(PURE_GREEN),
            FadeOut(edit, editline),
            run_time=2.5,
            wait=2,
        )
        b1t = Text("b1/load", font_size=24, color=GREEN).next_to(bline, RIGHT, buff=0.3)
        self.playw(Restore(nb), FadeIn(b1t, shift=RIGHT * 0.5), wait=2)
        b1t.save_state()
        self.playw(b1t.animate.scale(1.5).align_to(b1t, LEFT), run_time=3)
        self.playw(Restore(b1t), run_time=0.5, wait=2)
        b1t.save_state()
        self.play(b1t.animate.set_color(PURE_RED), run_time=0.5)
        self.play(Restore(b1t), run_time=0.5)
        bc2, bcline2 = new_commit(b1, direction="right", buff=0.75)
        VGroup(bc2, bcline2).set_color(GREEN).set_fill(opacity=0)
        self.playw(
            LaggedStart(
                b1t.animate.next_to(bc2, RIGHT), FadeIn(bcline2, bc2), lag_ratio=0.5
            ),
            run_time=1,
        )
        tobemerged = VGroup(bline, b1, b1t, bc2, bcline2).copy()
        c3, cline3 = new_commit(c2, direction="right")
        mainc4 = VGroup(cline3, c3).set_color(GREEN_B).set_fill(opacity=0)
        self.playw(Transform(tobemerged, mainc4), wait=2)

        gitmerge = Text(
            "git merge b1/load", font="Noto Mono", color=ORANGE, font_size=24
        ).next_to(c3, UR)
        self.playw(
            LaggedStart(*[FadeIn(c) for c in gitmerge], lag_ratio=0.1), run_time=1.0
        )


class mergedirection(Scene2D):
    def construct(self):
        gm_command = Text(
            "git merge b1/load", font="Noto Mono", color=ORANGE, font_size=32
        )
        self.play(FadeIn(gm_command))
        self.play(gm_command.animate.shift(UP * 1.5))
        head = Text("HEAD", font_size=24, color=BLUE)
        b1load = Text("b1/load", font_size=24, color=GREEN)
        VGroup(head, b1load).arrange(RIGHT, buff=1.5)
        arrow = Arrow(
            head.get_right(),
            b1load.get_left(),
            color=RED,
            stroke_width=2,
            tip_length=0.2,
        )
        self.playw(
            LaggedStart(FadeIn(head, b1load), GrowArrow(arrow), lag_ratio=0.5),
            run_time=1.5,
        )
        self.playw(arrow.animate.rotate(PI).set_color(PURE_GREEN))

        c0 = get_commit()
        c1, cline1 = new_commit(c0, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        b1, bline = new_commit(c2, direction="down", buff=0.5)
        VGroup(b1, bline).set_color(GREEN).set_fill(opacity=0)
        bc1, bcline1 = new_commit(b1, direction="right")
        VGroup(bc1, bcline1).set_color(GREEN).set_fill(opacity=0)
        bc2, bcline2 = new_commit(bc1, direction="right")
        VGroup(bc2, bcline2).set_color(GREEN).set_fill(opacity=0)

        commits = (
            VGroup(*[c0, cline1, c1, cline2, c2, bline, b1, bcline1, bc1, bcline2, bc2])
            .move_to(ORIGIN)
            .shift(DOWN + LEFT * 2)
        )
        self.playw(
            LaggedStart(*[FadeIn(item) for item in commits], lag_ratio=0.3),
            run_time=2.0,
        )
        self.play(head.animate.next_to(bc2, UR, buff=0.1), FadeOut(arrow, b1load))
        gitmergemain = Text(
            "git merge main123", font="Noto Mono", font_size=32 * 0.8, color=ORANGE
        ).next_to(head, RIGHT, buff=0.5)
        gitmergemain[-3:].set_opacity(0)
        gm_command.save_state()
        self.playw(
            gm_command.animate.next_to(head, RIGHT, buff=0.5)
            .scale(0.8)
            .become(gitmergemain)
        )
        self.play(head.animate.next_to(c2, UR, buff=0.1))
        self.playw(
            gm_command.animate.restore().next_to(head, RIGHT, buff=0.5).scale(0.8)
        )

        head_ = Text("HEAD", font_size=24, color=BLUE)
        b1load_ = Text("b1/load", font_size=24, color=GREEN)
        VGroup(head_, b1load_).arrange(RIGHT, buff=1.5).shift(UP)
        arrow_ = Arrow(
            b1load_.get_left(),
            head_.get_right(),
            color=PURE_GREEN,
            stroke_width=2,
            tip_length=0.2,
        )
        self.playw(
            LaggedStart(FadeIn(head_, b1load_), GrowArrow(arrow_), lag_ratio=0.5),
            run_time=1.5,
        )
        self.playw(Circumscribe(VGroup(head, gm_command)))


class mergeReverse(Scene2D):
    def construct(self):
        c0 = get_commit()
        c1, cline1 = new_commit(c0, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        b1, bline = new_commit(c2, direction="down", buff=0.5)
        VGroup(b1, bline).set_color(GREEN).set_fill(opacity=0)
        bc1, bcline1 = new_commit(b1, direction="right")
        VGroup(bc1, bcline1).set_color(GREEN).set_fill(opacity=0)
        bc2, bcline2 = new_commit(bc1, direction="right")
        VGroup(bc2, bcline2).set_color(GREEN).set_fill(opacity=0)
        commits = VGroup(
            *[c0, cline1, c1, cline2, c2, bline, b1, bcline1, bc1, bcline2, bc2]
        ).move_to(ORIGIN)
        self.playw(
            LaggedStart(*[FadeIn(item) for item in commits], lag_ratio=0.3),
            run_time=2.0,
        )

        c3, cline3 = new_commit(c2, direction="right")
        c4, cline4 = new_commit(c3, direction="right")

        self.playw(
            LaggedStart(
                FadeIn(cline3), FadeIn(c3), FadeIn(cline4), FadeIn(c4), lag_ratio=0.5
            )
        )
        self.playw(Circumscribe(VGroup(c2, b1)))

        thisweek = VGroup(cline3, c3, cline4, c4)
        self.play(
            LaggedStart(*[item.animate.shift(UP) for item in thisweek], lag_ratio=0.2),
            run_time=1,
        )
        self.playw(
            LaggedStart(
                *[item.animate.shift(DOWN) for item in thisweek], lag_ratio=0.2
            ),
            run_time=1,
        )

        marrow1 = Arrow(c3.get_bottom(), bc2.get_top(), color=GREEN, buff=0.05, tip_length=0.1, stroke_width=2)
        marrow2 = Arrow(c4.get_bottom(), bc2.get_top(), color=GREEN, buff=0.05, tip_length=0.2, stroke_width=2)
        self.play(
            LaggedStart(GrowArrow(marrow1), GrowArrow(marrow2), lag_ratio=0.3),
            run_time=0.8,
        )
        self.playw(FadeOut(marrow1, marrow2))

        gitmerge = Text(
            "git merge main", font="Noto Mono", color=ORANGE, font_size=32
        ).next_to(b1, DOWN, buff=0.5)
        head = Text("HEAD", font_size=24, color=GREEN).next_to(bc2, DR, buff=0.1)
        bc3, bcline3 = new_commit(bc2, direction="right")
        VGroup(bc3, bcline3).set_color(GREEN).set_fill(opacity=0)
        self.playw(FadeIn(gitmerge[:8]))
        self.playw(FadeIn(head))
        self.playw(FadeIn(gitmerge[8:]))
        self.play(
            LaggedStart(
                FadeIn(bcline3),
                FadeIn(bc3),
                head.animate.next_to(bc3, DR, buff=0.1),
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )
        mline1 = DashedLine(c3.get_bottom(), bc3.get_top(), color=ORANGE)
        mline2 = DashedLine(c4.get_bottom(), bc3.get_top(), color=ORANGE)
        self.playw(*[Create(line) for line in [mline1, mline2]])

        self.playw(FadeOut(gitmerge))

        arrbc1 = Arrow(
            bc1.get_bottom() + DOWN,
            bc1.get_bottom(),
            color=GREEN,
            stroke_width=3,
            tip_length=0.2,
            buff=0.1,
        )
        arrbc2 = Arrow(
            bc2.get_bottom() + DOWN,
            bc2.get_bottom(),
            color=GREEN,
            stroke_width=3,
            tip_length=0.2,
            buff=0.1,
        )
        self.playw(LaggedStart(GrowArrow(arrbc1), GrowArrow(arrbc2), lag_ratio=0.3))

        self.playw(Circumscribe(VGroup(bc1, bc2, arrbc1, arrbc2), color=GREEN_D))

        load_file = (
            VGroup(Text("Load", font_size=24, color=GREEN), FileIcon(size=0.2))
            .arrange(RIGHT, buff=0.2)
            .next_to(VGroup(arrbc1, arrbc2), DOWN)
        )
        self.playw(FadeIn(load_file))
        line_direct = Line(b1.get_right(), bc3.get_left(), color=GREEN)
        original_branch = VGroup(bcline1, bcline2, bcline3, bc1, bc2, arrbc1, arrbc2, load_file)
        self.playw(
            FadeOut(bcline1, bcline2, bcline3, bc1, bc2, arrbc1, arrbc2, load_file),
            FadeIn(line_direct),
        )

        self.playw(FadeOut(line_direct), FadeIn(original_branch))

        self.playw(Circumscribe(thisweek, buff=0.1))
        tbm = thisweek.copy()
        self.play(tbm.animate.become(bc3.copy()))
        self.remove(tbm)
        self.wait()
        self.playw(
            FadeOut(bcline1, bcline2, bcline3, bc1, bc2, arrbc1, arrbc2, load_file),
            FadeIn(line_direct),
        )

        self.playw(FadeOut(line_direct), FadeIn(original_branch))

        self.playw(Circumscribe(load_file, color=GREEN, buff=0.1))


class mergeConflict(Scene2D):
    def construct(self):
        c0 = get_commit()
        c1, cline1 = new_commit(c0, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        b1, bline = new_commit(c2, direction="down", buff=0.5)
        VGroup(b1, bline).set_color(GREEN).set_fill(opacity=0)
        bc1, bcline1 = new_commit(b1, direction="right")
        VGroup(bc1, bcline1).set_color(GREEN).set_fill(opacity=0)
        bc2, bcline2 = new_commit(bc1, direction="right")
        VGroup(bc2, bcline2).set_color(GREEN).set_fill(opacity=0)
        c3, cline3 = new_commit(c2, direction="right")

        commits = VGroup(
            *[c0, cline1, c1, cline2, c2, bline, b1, bcline1, bc1, bcline2, bc2, c3, cline3]
        ).move_to(ORIGIN)
        self.addw(commits)

        file1_texts = ["def save():", "pass", "def other():", "..."]
        file2_texts = ["def save():", "    pass", "def load():", "pass"]

        codeline = lambda x: Text(x, font_size=24, font="Noto Mono")
        file1 = VGroup(*[codeline(text) for text in file1_texts]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(c2, UR)
        file1[1::2].align_to(file1[0][3], LEFT)
        file1[2:].set_color(RED)
        file2 = VGroup(*[codeline(text) for text in file2_texts]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(bc2, DR)
        file2[1::2].align_to(file2[0][3], LEFT)
        file2[2:].set_color(GREEN)
        self.playw(FadeIn(file1, file2))

        gitmerge = Text("git merge main", font="Noto Mono", color=ORANGE, font_size=32).shift(DOWN*2)
        self.playw(FadeIn(gitmerge))

        gitdiff = file1[2:].copy()
        self.play(gitdiff.animate.next_to(file2[2:], UL, buff=-0.2), FadeOut(gitmerge), rate_func=rate_functions.rush_into)
        self.playw(gitdiff.animate.shift(UL*0.2+LEFT*0.2).rotate(10*DEGREES).set_color(PURE_RED), rate_func=rate_functions.rush_from)





get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=24, color=RED)


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
