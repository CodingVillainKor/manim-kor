from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        gitworktreet = (
            Text("git worktree", font_size=36)
            .set_color_by_gradient(BLUE_A, BLUE)
            .shift(UP * 2.5 + RIGHT)
        )
        start = get_commit().shift(LEFT * 4 + DOWN * 0.5)
        # main branch
        mc1, ml1 = new_commit(start, direction=RIGHT)
        mc2, ml2 = new_commit(mc1, direction=RIGHT)
        mc3, ml3 = new_commit(mc2, direction=RIGHT)
        mc4, ml4 = new_commit(mc3, direction=RIGHT)
        mc5, ml5 = new_commit(mc4, direction=RIGHT)

        # piui branch starting from mc2
        pc1, pl1 = new_commit(mc2, direction=UR)
        pc2, pl2 = new_commit(pc1, direction=RIGHT)
        head = VGroup(
            harr := Arrow(
                mc5.get_right() + RIGHT * 0.7, mc5.get_right(), buff=0.1, color=YELLOW
            ),
            Text("HEAD", font_size=24, color=YELLOW).next_to(harr, RIGHT, buff=0.1),
        )
        self.add(head, gitworktreet)
        self.addw(
            start, mc1, ml1, mc2, ml2, mc3, ml3, mc4, ml4, mc5, ml5, pc1, pl1, pc2, pl2
        )

        now_head = SurroundingRectangle(
            VGroup(mc5, head), color=BLUE_B, stroke_width=0.3, buff=0.12
        ).set_fill(BLUE_B, opacity=0.3)

        _dot = (
            Dot(fill_opacity=0)
            .next_to(head, UP, buff=0.5)
            .align_to(head, RIGHT)
            .shift(RIGHT * 0.2)
        )
        _path = BrokenLine(
            _dot.get_center(),
            _dot.get_center() + UP + LEFT,
            _dot.get_center() + UP + LEFT * 2,
            smooth=True,
        )
        arrow = Arrow(
            start=gitworktreet.get_corner(DR + DOWN),
            end=_dot.get_center(),
            buff=0.0,
            color=MINT,
            tip_length=0.2,
            stroke_width=2,
        )
        self.playw(GrowFromEdge(now_head, RIGHT), FadeIn(arrow), wait=2)
        arrow.add_updater(
            lambda a: a.put_start_and_end_on(
                gitworktreet.get_corner(DR + DOWN), _dot.get_center()
            )
        )
        self.playw(MoveAlongPath(_dot, _path), run_time=2)


class gitworktree(Scene2D):
    def construct(self):
        prjfolder = Folder("prj/")
        start = get_commit().shift(LEFT * 4 + DOWN * 0.5)
        # main branch
        mc1, ml1 = new_commit(start, direction=RIGHT)
        mc2, ml2 = new_commit(mc1, direction=RIGHT)
        mc3, ml3 = new_commit(mc2, direction=RIGHT)
        mc4, ml4 = new_commit(mc3, direction=RIGHT)
        mc5, ml5 = new_commit(mc4, direction=RIGHT)

        # piui branch starting from mc2
        pc1, pl1 = new_commit(mc2, direction=UR)
        pc2, pl2 = new_commit(pc1, direction=RIGHT)
        head = VGroup(
            harr := Arrow(
                mc5.get_right() + RIGHT * 0.7, mc5.get_right(), buff=0.1, color=YELLOW
            ),
            Text("HEAD", font_size=24, color=YELLOW).next_to(harr, RIGHT, buff=0.1),
        )
        self.add(head)
        prjfolder.next_to(start, LEFT)
        folder_box = DashedVMobject(
            SurroundingRectangle(
                VGroup(prjfolder, start, pc2, head),
                color=YELLOW_B,
                buff=0.2,
                stroke_width=1,
            ),
            num_dashes=60,
            dashed_ratio=0.6,
        )
        piuit = (
            Text("piui", font_size=24)
            .set_color_by_gradient(GREY_B, GREY_C)
            .next_to(pc2, RIGHT, buff=0.1)
        )
        self.addw(
            prjfolder,
            folder_box,
            start,
            mc1,
            ml1,
            mc2,
            ml2,
            mc3,
            ml3,
            mc4,
            ml4,
            mc5,
            ml5,
            pc1,
            pl1,
            pc2,
            pl2,
            piuit,
        )
        piuifolder = Folder("prj_piui/").next_to(pc2, UP, buff=1)
        piui_arr = Arrow(
            start=piuifolder.get_bottom(),
            end=pc2.get_top(),
            buff=0.1,
            color=MINT,
            tip_length=0.2,
            stroke_width=2,
        )
        self.playw(GrowArrow(piui_arr))
        self.playw(FadeIn(piuifolder))

        self.playw(Circumscribe(head, color=GREEN, stroke_width=2))
        self.playw(Circumscribe(VGroup(piuit, pc2), color=GREEN, stroke_width=2))

        cmd3_str = "../prj_piui"
        cmd4_str = "piui"
        cmd = Words(
            "git worktree add <dir> <branch>", font_size=20, font=MONO_FONT
        ).next_to(pc1, UL, buff=0.75)
        cmd.words.set_color_by_gradient(BLUE, BLUE_A)
        self.playwl(*[FadeIn(item) for item in cmd.words], lag_ratio=0.5)
        _dir = cmd.words[3]
        _branch = cmd.words[4]
        self.playw(_dir.copy().animate.become(piuifolder.icon.copy()))
        self.play(_branch.copy().animate.become(_temp:=piuit.copy()))
        self.remove(_temp)
        piui_arrc = piui_arr.copy().set_color(YELLOW)
        self.playw(GrowArrow(piui_arrc))
        self.playw(Circumscribe(prjfolder, color=YELLOW, stroke_width=2))

        cmd2 = (
            Words(
                f"git worktree add {cmd3_str} {cmd4_str}", font_size=20, font=MONO_FONT
            )
            .move_to(cmd)
            .align_to(cmd, LEFT)
        )
        cmd2.set_color_by_gradient(BLUE, BLUE_A)
        self.playwl(
            *[
                Transform(cmd.words[i], cmd2.words[i], path_arc=PI / 8)
                for i in range(len(cmd.words))
            ],
            lag_ratio=0.2,
            wait=2,
        )

        self.playw(
            Indicate(cmd.words[-1], scale_factor=1.3), Indicate(piuit, scale_factor=1.3)
        )

        self.playw(Indicate(piuifolder.text))

        # piui branch from prj_piui
        start_ = get_commit().next_to(piuifolder, RIGHT)
        mc1_, ml1_ = new_commit(start_, direction=RIGHT)
        mc2_, ml2_ = new_commit(mc1_, direction=RIGHT)
        pc1_, pl1_ = new_commit(mc2_, direction=UR)
        pc2_, pl2_ = new_commit(pc1_, direction=RIGHT)
        piuit_ = (
            Text("piui", font_size=24)
            .set_color_by_gradient(GREY_B, GREY_C)
            .next_to(pc2_, RIGHT, buff=0.1)
        )
        piui_box = DashedVMobject(
            SurroundingRectangle(
                VGroup(piuifolder, start_, pc2_, piuit_),
                color=YELLOW_B,
                buff=0.2,
                stroke_width=1,
            ),
            num_dashes=60,
            dashed_ratio=0.6,
        )
        self.playw(
            FadeIn(
                start_, mc1_, ml1_, mc2_, ml2_, pc1_, pl1_, pc2_, pl2_, piuit_, piui_box
            ),
            self.cf.animate.move_to(mc2_),
            FadeOut(piui_arr, piui_arrc),
        )


get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=24, color=RED)


def new_commit(from_commit, *, direction=RIGHT):
    newc = get_commit().next_to(from_commit, direction=direction, buff=1)
    start = from_commit.get_corner(direction)
    to = newc.get_corner(-direction)
    cline = Line(start, to, color=GREY_C)
    return newc, cline
