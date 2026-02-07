from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        main_branch = VGroup()
        piui_branch = VGroup()
        start = get_commit()
        c1, l1 = new_commit(start, direction="right")
        c2, l2 = new_commit(c1, direction="right")
        c3, l3 = new_commit(c2, direction="right")
        p1, pl1 = new_commit(c1, direction="down")
        p2, pl2 = new_commit(p1, direction="right")
        p3, pl3 = new_commit(p2, direction="right")
        main_branch.add(start, c1, c2, c3, l1, l2, l3)
        piui_branch.add(p1, p2, p3, pl1, pl2, pl3)
        VGroup(main_branch, piui_branch).move_to(ORIGIN).shift(LEFT * 2)

        head = chash("HEAD").scale(0.7).next_to(p3, RIGHT, buff=1)
        harr = Arrow(
            head.get_left(),
            p3.get_right(),
            buff=0.05,
            stroke_width=2,
            tip_length=0.2,
            color=RED,
        )
        h = VGroup(head, harr)
        mbt = Text("main", color=GREY_B, font="Noto Sans KR", font_size=24).next_to(
            c3, UR, buff=0.15
        )
        pbt = Text("piui", color=GREY_B, font="Noto Sans KR", font_size=24).next_to(
            p3, DR, buff=0.15
        )

        cmd = Words(
            "git rebase main", font=MONO_FONT, font_size=32, color=YELLOW_A
        ).next_to(pbt, RIGHT, buff=1)

        self.addw(main_branch, piui_branch, mbt, pbt, h)
        h.add_updater(lambda m: m.next_to(p3, RIGHT, buff=0.1))
        self.playwl(*[FadeIn(item) for item in cmd.words], lag_ratio=0.3, wait=0)
        piui = VGroup(piui_branch, pbt)
        piui.generate_target().shift(DOWN * 0.5)
        piui.target[0][3:].set_opacity(0)
        self.play(MoveToTarget(piui), FadeOut(cmd, shift=RIGHT * 0.5))
        self.playw(RWiggle(piui), run_time=3)
        self.playw(piui.animate.align_to(main_branch[-4], LEFT))

        cp1 = VGroup(p1, pl1)
        cp2 = VGroup(p2, pl2)
        cp3 = VGroup(p3, pl3)
        cp1.generate_target().next_to(c3, DOWN, buff=0)
        cp1.target[1].set_opacity(1)
        self.play(MoveToTarget(cp1))
        cp2.generate_target().next_to(cp1.target[0], RIGHT, buff=0)
        cp2.target[1].set_opacity(1)
        self.play(MoveToTarget(cp2))
        cp3.generate_target().next_to(cp2.target[0], RIGHT, buff=0)
        cp3.target[1].set_opacity(1)
        self.playw(MoveToTarget(cp3), pbt.animate.next_to(cp3.target[0], DR, buff=0.15))

        mvr = (
            Words("git merge vs rebase", font=MONO_FONT, font_size=32)
            .shift(DOWN * 1.5)
            .set_color_by_gradient(TEAL_A, TEAL_C)
        )
        self.playw(
            *[FadeIn(item, shift=DOWN * 0.5) for item in mvr.words],
            VGroup(mbt, pbt, main_branch, piui_branch).animate.shift(UP * 1.5),
        )
        gh = ImageMobject("githublogo.jpg").scale(0.4).next_to(mvr, RIGHT, buff=1)
        self.play(FadeIn(gh, shift=LEFT * 4))
        self.playw(RWiggle(gh), run_time=2)

        ol = self.overlay
        mvr.words[0::3].set_z_index(ol.z_index + 1)
        self.play(FadeIn(ol), run_time=0.5)
        self.playw(
            FadeOut(mvr.words[1:3]),
            mvr.words[3].animate.shift(LEFT * 1.5),
            mvr.words[0].animate.shift(RIGHT * 0.6),
        )


class whenrebase(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(60)

        start = get_commit().shift(DOWN * 3)
        c1, l1 = new_commit(start, direction="up")
        c2, l2 = new_commit(c1, direction="up")
        c2.set_stroke(color=GREY_C, width=3)
        l2.set_stroke(color=GREY_D, width=3)
        c3, l3 = new_commit(c2, direction="up")
        c3.set_stroke(color=GREY_C, width=3)
        l3.set_stroke(color=GREY_D, width=3)
        main_branch = VGroup(start, c1, c2, c3, l1, l2, l3).shift(LEFT * 1.5)
        p1, pl1 = new_commit(c1, direction="right")
        p2, pl2 = new_commit(p1, direction="up")
        p3, pl3 = new_commit(p2, direction="up")
        piui_branch = VGroup(p1, p2, p3, pl1, pl2, pl3)
        tree = VGroup(main_branch, piui_branch).scale(1.3)

        mbt = (
            Text("main", color=GREY_B, font="Noto Sans KR", font_size=24)
            .next_to(c1, UL, buff=0.15)
            .rotate(60 * DEGREES, axis=RIGHT)
        )
        pbt = (
            Text("piui", color=BLUE_C, font="Noto Sans KR", font_size=24)
            .next_to(p1, UL, buff=0.15)
            .rotate(60 * DEGREES, axis=RIGHT)
        )

        self.addw(start, c1, l1, mbt)
        self.play(FadeIn(p1, pl1, pbt))
        self.play(FadeIn(p2, pl2), pbt.animate.next_to(p2, UL, buff=0.15))
        self.play(FadeIn(p3, pl3), pbt.animate.next_to(p3, UL, buff=0.15))
        self.play(FadeIn(c2, l2), mbt.animate.next_to(c2, UL, buff=0.15))
        self.playw(FadeIn(c3, l3), mbt.animate.next_to(c3, UL, buff=0.15))

        srmain = DashedVMobject(
            SurroundingRectangle(
                VGroup(c2, c3), buff=0.3, color=GREY_B, stroke_width=2
            ),
            num_dashes=30,
            stroke_color=GREY_C,
        )
        srarr = Arrow(
            srmain.get_right(), pbt, buff=0.05, tip_length=0.2, stroke_width=2
        ).put_start_and_end_on(srmain.get_right(), pbt.get_corner(DL) + DOWN * 0.3)
        self.playwl(
            mbt.animate.next_to(c3, UL, buff=0.45),
            FadeOut(l2, l3),
            FadeIn(srmain, srarr),
            lag_ratio=0.2,
        )

        gitmerge = (
            Words("git merge main", font=MONO_FONT)
            .scale(0.6)
            .rotate(60 * DEGREES, axis=RIGHT)
            .set_color_by_gradient(GREY_A, GREY_C)
        )
        gitrebase = (
            Words("git rebase main", font=MONO_FONT)
            .scale(0.6)
            .rotate(60 * DEGREES, axis=RIGHT)
            .set_color_by_gradient(TEAL_A, TEAL_C)
        )
        cmds = (
            VGroup(gitmerge, gitrebase)
            .arrange(DOWN, buff=1, aligned_edge=LEFT)
            .next_to(piui_branch, RIGHT, buff=1)
        )
        self.play(FadeIn(gitmerge, shift=RIGHT * 0.5))
        self.playw(FadeIn(gitrebase, shift=RIGHT * 0.5))

        srarr.add_updater(
            lambda m: m.put_start_and_end_on(
                srmain.get_right(), pbt.get_corner(DL) + DOWN * 0.3
            )
        )
        self.playw(RWiggle(VGroup(srmain, c2, c3)), run_time=3)

        ol = self.overlay
        cmds.set_z_index(ol.z_index + 1)
        self.play(self.cf.animate.shift(RIGHT * 2), FadeIn(ol), run_time=0.7)
        self.playw(
            RWiggle(gitrebase, amp=(0.07, 0.07, 0.07)),
            RWiggle(gitmerge, amp=(0.05, 0.05, 0.05)),
            run_time=2,
        )

        merge_or_rebase = "rebase"

        if merge_or_rebase == "merge":
            self.playw(
                gitrebase.animate.shift(RIGHT * 1.5).set_opacity(0),
                self.cf.animate.shift(LEFT * 2),
                FadeOut(ol),
            )
            p4, pl4 = new_commit(p3, direction="up")
            p4.set_stroke(color=TEAL_B, width=3)
            VGroup(p4, pl4).scale(1.3).next_to(p3, UP, buff=0)
            merged = VGroup(c2, c3, srmain).copy()
            self.playw(
                Transform(merged, p4),
                FadeIn(pl4),
                pbt.animate.next_to(p4, UL, buff=0.15),
                FadeOut(srarr),
            )

        elif merge_or_rebase == "rebase":
            self.playw(
                gitmerge.animate.shift(RIGHT * 1.5).set_opacity(0),
                self.cf.animate.shift(LEFT * 2),
                FadeOut(ol),
            )
            self.play(VGroup(pl1, pl2, pl3).animate.set_opacity(0))
            self.play(FadeOut(srmain, srarr), FadeIn(l2, l3))
            self.playw(
                VGroup(pbt, p1, p2, p3, pl1, pl2, pl3).animate.align_to(c3, DOWN)
            )
            self.play(
                pl1.animate.set_opacity(1), p1.animate.set_stroke(color=TEAL_B, width=3)
            )
            self.play(
                pl2.animate.set_opacity(1), p2.animate.set_stroke(color=TEAL_C, width=3)
            )
            self.playw(
                pl3.animate.set_opacity(1), p3.animate.set_stroke(color=BLUE_B, width=3)
            )


class rebasehash(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(60)
        start = get_commit().shift(DOWN * 3)
        c1, l1 = new_commit(start, direction="up")
        c2, l2 = new_commit(c1, direction="up")
        c2.set_stroke(color=GREY_C, width=3)
        l2.set_stroke(color=GREY_D, width=3)
        c3, l3 = new_commit(c2, direction="up")
        c3.set_stroke(color=GREY_C, width=3)
        l3.set_stroke(color=GREY_D, width=3)
        main_branch = VGroup(start, c1, c2, c3, l1, l2, l3).shift(LEFT * 1.5)
        p1, pl1 = new_commit(c1, direction="right")
        p2, pl2 = new_commit(p1, direction="up")
        p3, pl3 = new_commit(p2, direction="up")
        piui_branch = VGroup(p1, p2, p3, pl1, pl2, pl3)
        tree = VGroup(main_branch, piui_branch).scale(1.3)

        mbt = (
            Text("main", color=GREY_B, font="Noto Sans KR", font_size=24)
            .next_to(c1, UL, buff=0.15)
            .rotate(60 * DEGREES, axis=RIGHT)
        )
        pbt = (
            Text("piui", color=BLUE_C, font="Noto Sans KR", font_size=24)
            .next_to(p3, UL, buff=0.15)
            .rotate(60 * DEGREES, axis=RIGHT)
        )
        srmain = DashedVMobject(
            SurroundingRectangle(
                VGroup(c2, c3), buff=0.3, color=GREY_B, stroke_width=2
            ),
            num_dashes=30,
            stroke_color=GREY_C,
        )
        srarr = Arrow(
            srmain.get_right(), pbt, buff=0.05, tip_length=0.2, stroke_width=2
        ).put_start_and_end_on(srmain.get_right(), pbt.get_corner(DL) + DOWN * 0.3)

        gitrebase = (
            Words("git rebase main", font=MONO_FONT)
            .scale(0.6)
            .rotate(60 * DEGREES, axis=RIGHT)
            .set_color_by_gradient(TEAL_A, TEAL_C)
        ).next_to(piui_branch, RIGHT, buff=1.6)
        phashs = VGroup()
        phash_strings = ["a1b2c31", "q1w2e32", "z9x8c33"]
        for i, pc in enumerate([p1, p2, p3]):
            phash = (
                chash(phash_strings[i])
                .scale(0.7)
                .rotate(60 * DEGREES, axis=RIGHT)
                .next_to(pc, RIGHT, buff=0.3)
            )
            phashs.add(phash)
        self.add(tree, mbt, pbt, srmain, srarr, phashs)
        self.playwl(*[FadeIn(item) for item in gitrebase.words], lag_ratio=0.3, wait=0)

        plines = VGroup(pl1, pl2, pl3)
        pcommits = VGroup(p1, p2, p3)
        pcommits.generate_target().align_to(c3, DOWN)
        self.playw(plines.animate.set_opacity(0))
        self.playw(
            FadeOut(srmain, srarr),
            MoveToTarget(pcommits),
            pbt.animate.next_to(pcommits.target[2], UL, buff=0.15),
            *[
                phash.animate.next_to(pcommits.target[i], RIGHT, buff=0.3)
                for i, phash in enumerate(phashs)
            ],
        )

        self.playw(
            *[
                RWiggle(VGroup(item, h), amp=(0.12, 0.12, 0.12))
                for item, h in zip(pcommits, phashs)
            ],
            run_time=3,
        )
        plines[0].put_start_and_end_on(c3.get_right(), pcommits[0].get_left())
        plines[1].put_start_and_end_on(pcommits[0].get_top(), pcommits[1].get_bottom())
        plines[2].put_start_and_end_on(pcommits[1].get_top(), pcommits[2].get_bottom())

        hash_strings_new = ["d4e5f41", "r4t5y42", "v7b8n43"]
        phashs_new = VGroup()
        for i, hs in enumerate(hash_strings_new):
            phash_new = (
                chash(hs).scale(0.7).rotate(60 * DEGREES, axis=RIGHT).move_to(phashs[i])
            )
            phashs_new.add(phash_new)
        self.play(
            FadeIn(phashs_new[0], scale=1.5),
            FadeOut(phashs[0], scale=1.5),
            pcommits[0].animate.set_stroke(color=TEAL_B, width=3),
            plines[0].animate.set_opacity(1),
        )
        self.play(
            FadeIn(phashs_new[1], scale=1.5),
            FadeOut(phashs[1], scale=1.5),
            pcommits[1].animate.set_stroke(color=TEAL_C, width=3),
            plines[1].animate.set_opacity(1),
        )
        self.playw(
            FadeIn(phashs_new[2], scale=1.5),
            FadeOut(phashs[2], scale=1.5),
            pcommits[2].animate.set_stroke(color=BLUE_B, width=3),
            plines[2].animate.set_opacity(1),
        )


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
