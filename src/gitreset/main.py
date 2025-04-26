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
        cline2.add_updater(
            lambda m: m.put_start_and_end_on(c1.get_top(), c2.get_bottom())
        )
        ccline_c1.add_updater(
            lambda m: m.put_start_and_end_on(c1.get_right(), code_c1.get_left())
        )
        code_c1.add_updater(lambda m: m.next_to(c1, RIGHT, buff=0.75))
        self.playw(c1.animate.shift(DOWN * 2), self.cf.animate.shift(DOWN * 0.5))

        dots = VGroup(
            *[
                Dot(color=BLUE).move_to(cline2.point_from_proportion(p))
                for p in [1 / 3, 2 / 3]
            ]
        )
        self.playw(FadeIn(dots))
        modified = (
            Text("modified: main.py", font_size=24, color=RED)
            .next_to(code_c1, UP, buff=0.5)
            .align_to(code_c1, LEFT)
        )
        marrow = Arrow(
            modified.get_left(),
            dots[0].get_right(),
            color=WHITE,
            buff=0.05,
            stroke_width=2,
        )
        staged = (
            Text("to be committed: main.py", font_size=24, color=PURE_GREEN)
            .next_to(modified, UP, buff=0.5)
            .align_to(code_c1, LEFT)
        )
        sarrow = Arrow(
            staged[1].get_left(),
            dots[1].get_right(),
            color=WHITE,
            buff=0.05,
            stroke_width=2,
        )
        self.playw(LaggedStart(FadeIn(marrow), FadeIn(modified), lag_ratio=0.3))
        self.playw(LaggedStart(FadeIn(sarrow), FadeIn(staged), lag_ratio=0.3))

        prohibit_arrow = Arrow(
            c1.get_top(), c2.get_bottom(), color=PURE_RED, stroke_width=12, buff=0
        )
        self.playw(GrowArrow(prohibit_arrow))
        prohibit_arrow.generate_target()
        prohibit_arrow.target.rotate(
            120 * DEGREES, about_point=prohibit_arrow.get_bottom()
        ).shift(DOWN * 3 + LEFT * 2)
        self.playw(MoveToTarget(prohibit_arrow))


class saveaddcommit(Scene3D):
    def construct(self):
        self.tilt_camera_vertical(60)
        _scale = 0.4
        before = (
            RoundedRectangle(
                corner_radius=0.25, width=22, height=9, stroke_width=3, color=GREY_B
            )
            .scale(_scale)
            .shift(DOWN * 3)
        )
        commit1t = (
            Text("commit1", font_size=24, color=GREEN_B)
            .rotate(60 * DEGREES, RIGHT)
            .next_to(before, LEFT)
            .align_to(before, UP)
        )
        stage = (
            RoundedRectangle(
                corner_radius=0.25, width=16, height=9, stroke_width=3, color=GREY_B
            )
            .scale(_scale)
            .shift(UP * 2)
        )
        staget = (
            Text("stage", font_size=24, color=GREEN_B)
            .rotate(60 * DEGREES, RIGHT)
            .next_to(stage, LEFT)
            .align_to(stage, UP)
        )
        commited = (
            RoundedRectangle(
                corner_radius=0.25, width=24, height=9, stroke_width=3, color=GREY_B
            )
            .scale(_scale)
            .shift(UP * 7)
        )
        commit2t = (
            Text("commit2", font_size=24, color=GREEN_B)
            .rotate(60 * DEGREES, RIGHT)
            .next_to(commited, LEFT)
            .align_to(commited, UP)
        )
        self.playw(
            LaggedStart(
                *[
                    FadeIn(item)
                    for item in [
                        VGroup(before, commit1t),
                        VGroup(stage, staget),
                        VGroup(commited, commit2t),
                    ]
                ],
                lag_ratio=0.3,
            )
        )
        mainpy0 = FileIcon("main.py")
        utilpy0 = FileIcon("util.py")
        modulepy0 = FileIcon("module.py")
        commit1 = (
            VGroup(mainpy0, utilpy0, modulepy0).arrange(RIGHT, buff=0.5).move_to(before)
        )
        self.playw(FadeIn(commit1))

        changed_mainpy = Text("modified", font_size=24, color=RED).next_to(
            mainpy0, UP, buff=0.25
        )
        changed_utilpy = Text("modified", font_size=24, color=RED).next_to(
            utilpy0, UP, buff=0.25
        )
        self.playw(
            FadeIn(changed_mainpy, shift=UP * 0.5),
            FadeIn(changed_utilpy, shift=UP * 0.5),
        )

        command_gitadd = (
            Text("git add main.py", font_size=24, font="Noto Mono", color=YELLOW)
            .rotate(60 * DEGREES, RIGHT)
            .next_to(before, UP, buff=0.5)
        )
        self.playw(LaggedStart(*[FadeIn(c) for c in command_gitadd], lag_ratio=0.05))
        mainpy1 = mainpy0.copy()
        self.playw(
            LaggedStart(
                FadeOut(command_gitadd),
                mainpy1.animate.move_to(stage).set_color(RED_B),
                lag_ratio=0.3,
            )
        )
        command_gitcommit = (
            Text("git commit -m 'update main.py'", font_size=24, color=YELLOW)
            .rotate(60 * DEGREES, RIGHT)
            .next_to(stage, UP, buff=0.5)
        )
        self.playw(LaggedStart(*[FadeIn(c) for c in command_gitcommit], lag_ratio=0.05))
        self.play(
            LaggedStart(
                FadeOut(command_gitcommit),
                mainpy1.animate.move_to(commited),
                FadeOut(changed_mainpy),
                lag_ratio=0.3,
            )
        )
        commit2 = VGroup(mainpy1, utilpy0.copy(), modulepy0.copy())
        commit2.generate_target()
        commit2.target.arrange(RIGHT, buff=0.5).move_to(commited)

        self.playw(
            MoveToTarget(commit2),
            changed_utilpy.copy().animate.next_to(commit2.target[1], UP, buff=0.25),
        )


class saveaddcommitDetail(Scene3D):
    def construct(self):
        init = get_commit()
        c1, cline1 = new_commit(init, direction="right")
        c2, cline2 = new_commit(c1, direction="right")
        c3, cline3 = new_commit(c2, direction="right")
        commits = (
            VGroup(init, cline1, c1, cline2, c2, cline3, c3)
            .move_to(ORIGIN)
            .shift(DOWN * 1.5 + LEFT * 2)
        )
        cts = VGroup(
            *[
                Text(item, font_size=24, color=YELLOW_A).next_to(c, DOWN)
                for item, c in [["c0", init], ["c1", c1], ["c2", c2], ["c3", c3]]
            ]
        )
        code = PythonCode("src/example.py", add_line_numbers=False).shift(
            UP + RIGHT * 3
        )
        code.frame.stroke_color = YELLOW
        code.frame.set_opacity(1).set_fill(opacity=0.7)

        c0line_midpoint = init.get_top() + UP * 3.58
        c0line = BrokenLine(
            init.get_top(),
            c0line_midpoint,
            code.get_left() + UP * 1.2,
            stroke_width=2,
            color=YELLOW,
            arrow=True,
            tip_length=0.2,
        )
        c1code = code(1).set_color(BLUE)
        c1line = Arrow(
            c1.get_top(),
            c1code[0].get_left(),
            color=BLUE,
            buff=0.05,
            tip_length=0.2,
            stroke_width=2,
        )
        c2code = code(2).set_color(PURPLE_D)
        c2line = Arrow(
            c2.get_top(),
            c2code[0].get_left(),
            color=PURPLE_D,
            buff=0.05,
            tip_length=0.2,
            stroke_width=2,
        )
        c3code = code(4).set_color(GREEN)
        c3line = Arrow(
            c3.get_top(),
            c3code[0].get_left(),
            color=GREEN,
            buff=0.05,
            tip_length=0.2,
            stroke_width=2,
        )

        modified = SurroundingRect(color=PURE_RED).surround(
            code(-1).set_color(PURE_RED)
        )
        modifiedt = (
            Text("modified", font_size=16, color=PURE_RED)
            .next_to(modified, RIGHT, buff=0.05)
            .align_to(modified, UP)
        )

        self.playw(
            FadeIn(
                commits, cts, code, c0line, c1line, c2line, c3line, modified, modifiedt
            )
        )
        self.playw(Indicate(VGroup(modified, modifiedt, code(-1))))
        self.playw(
            LaggedStart(
                *[Indicate(item) for item in [c3line, c2line, c1line, c0line]],
                lag_ratio=0.1,
            )
        )

        gitresetc2 = (
            Text("git reset c2", font_size=24, font="Noto Mono")
            .set_color_by_gradient(RED_B, RED_D)
            .next_to(c3, RIGHT, buff=2)
        )
        self.playw(LaggedStart(*[FadeIn(c) for c in gitresetc2], lag_ratio=0.05))
        self.playw(
            LaggedStart(
                *[Indicate(item) for item in [c3line, c2line, c1line, c0line]],
                lag_ratio=0.1,
            )
        )
        c3.save_state()
        self.playw(
            FadeOut(c3line, cts[-1]),
            c3.animate.become(
                Text("staged", font_size=24, font="Noto Mono", color=GREEN)
                .move_to(c3)
                .align_to(c3, LEFT)
            ),
        )
        modifiedt.add_updater(
            lambda m: m.next_to(modified, RIGHT, buff=0.05).align_to(modified, UP)
        )
        code(4).save_state()
        self.playw(
            LaggedStart(
                FadeOut(c3, cline3, gitresetc2),
                modified.animate.surround(code(4, 6), buff_w=-1.05),
                code(4).animate.set_color(PURE_RED),
                lag_ratio=0.3,
            )
        )

        modifiedt.suspend_updating()
        modified = VGroup(modified, modifiedt)
        self.playw(modified.animate.become(cline3), FadeIn(c3))
        self.play(Restore(c3), FadeIn(cts[-1]))
        c3line2 = Arrow(
            c3.get_top(),
            code(-1).get_left(),
            color=GREEN,
            buff=0.05,
            tip_length=0.2,
            stroke_width=2,
        )
        self.playw(
            FadeIn(c3line, c3line2), Restore(code(4)), code(-1).animate.set_color(GREEN)
        )


class options(Scene2D):
    def construct(self):
        gitreset_text = Text(
            "git reset", font_size=28, font="Noto Mono"
        ).set_color_by_gradient(RED_B, RED_D)
        self.playw(LaggedStart(*[FadeIn(c) for c in gitreset_text], lag_ratio=0.05))
        gitreset_text1, gitreset_text2, gitreset_text3 = (
            gitreset_text.copy().shift(UP * 2),
            gitreset_text,
            gitreset_text.copy().shift(DOWN * 2),
        )
        self.playw(
            FadeIn(gitreset_text1, scale=0.8, shift=UP),
            FadeIn(gitreset_text3, scale=0.8, shift=DOWN),
        )

        soft = (
            Text("--soft", font_size=28, font="Noto Mono")
            .set_color_by_gradient(RED_B, RED_D)
            .next_to(gitreset_text1, RIGHT, buff=0.5)
        )
        mixed = (
            Text("--mixed", font_size=28, font="Noto Mono")
            .set_color_by_gradient(RED_B, RED_D)
            .next_to(gitreset_text2, RIGHT, buff=0.5)
        )
        hard = (
            Text("--hard", font_size=28, font="Noto Mono")
            .set_color_by_gradient(RED_B, RED_D)
            .next_to(gitreset_text3, RIGHT, buff=0.5)
        )
        for item, gr in [
            [soft, gitreset_text1],
            [mixed, gitreset_text2],
            [hard, gitreset_text3],
        ]:
            self.play(
                LaggedStart(*[FadeIn(c) for c in item], lag_ratio=0.05),
                gr.animate.set_color(GREY_B),
            )
        self.wait()
        self.playw(
            self.cf.animate.shift(RIGHT), VGroup(soft, hard).animate.set_opacity(0.3)
        )
        self.playw(mixed.animate.set_opacity(0))
        self.play(soft.animate.set_opacity(1))
        self.playw(hard.animate.set_opacity(1))
        self.wait(3)

        grsoft, grmixed, grhard = [
            VGroup(gitreset_text1, soft),
            VGroup(gitreset_text2, mixed),
            VGroup(gitreset_text3, hard),
        ]
        self.playw(
            VGroup(grsoft, grmixed, grhard)
            .animate.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            .shift(UP * 2.0),
            self.cf.animate.move_to(ORIGIN),
        )

        init = get_commit().shift(DOWN * 1.5)
        followed = DashedLine(
            init.get_left() + LEFT * 2, init.get_left()
        ).set_color_by_gradient(GREY_E, GREY_B)
        modified = (
            Text("modified", font_size=24, color=RED)
            .next_to(init, UP, buff=0.1)
            .align_to(init, LEFT)
        )
        self.playw(FadeIn(init, followed))
        first = Text("①", color=YELLOW, font_size=24).next_to(modified, LEFT, buff=0.1)
        self.playw(FadeIn(modified, first))
        c1, add_line = new_commit(init, direction="right")
        second = Text("②", color=YELLOW, font_size=24).next_to(add_line, DOWN, buff=0.1)
        c1.set_color(GREEN).set_fill(opacity=0)
        third = Text("③", color=YELLOW, font_size=24).next_to(c1, DOWN, buff=0.1)
        staged = Text("staged", font_size=24, color=GREEN).move_to(c1).align_to(c1, LEFT)
        stagedc = staged.copy()
        s0 = modified.copy()
        self.playw(FadeIn(add_line, second), s0.animate.become(staged))
        self.playw(s0.animate.become(c1), FadeIn(third))

        self.playw(VGroup(grsoft, grhard).animate.set_opacity(0.2))
        self.playw(grmixed.animate.set_opacity(1))
        c1 = s0
        
        graph = VGroup(first, second, third, init, followed, modified, add_line, c1)
        graph.save_state()
        self.playw(VGroup(third, c1, add_line, second).animate.set_opacity(0))
        self.play(Restore(graph))
        self.playw(grmixed.animate.set_opacity(0.2), grsoft.animate.set_opacity(1))
        graph.save_state()
        self.playw(third.animate.set_opacity(0), c1.animate.become(stagedc))
        self.wait(2)
        self.playw(Restore(graph))

        self.playw(grsoft.animate.set_opacity(0.2), grhard.animate.set_opacity(1))
        self.playw(VGroup(third, c1, add_line, second, modified, first).animate.set_opacity(0))
        self.wait(3)



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
