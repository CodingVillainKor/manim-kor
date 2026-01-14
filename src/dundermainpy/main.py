from functools import partial
from manim import *
from raenim import *
from random import seed


seed(41)
np.random.seed(41)


class scene(Scene3D):
    def construct(self):
        s1 = self.s1()
        vs1 = VGroup(item for item in s1.values()).set_z_index(1)
        bvs1 = SurroundingRectangle(
            vs1, buff=1, color=GREY_D, stroke_width=2, fill_color=BLACK, fill_opacity=1
        ).set_z_index(0.9)
        bvs1.stretch_to_fit_width(bvs1.width * 1.1)
        scene1 = VGroup(bvs1, vs1).move_to(ORIGIN).set_opacity(0)
        # self.addw(scene1)

        s2 = self.s2()
        vs2 = VGroup(item for item in s2.values()).set_z_index(2)
        bvs2 = SurroundingRectangle(
            vs2, buff=1, color=GREY_D, stroke_width=2, fill_color=BLACK, fill_opacity=1
        ).set_z_index(1.9)
        bvs2.stretch_to_fit_width(bvs2.width * 1.1)
        scene2 = VGroup(bvs2, vs2).move_to(ORIGIN)
        scene2.scale(scene1.height / scene2.height).set_opacity(0).shift(RIGHT * 8)

        self.cf.shift(OUT * 5)
        orig_center = s1.title.get_center()
        s1.title.move_to(ORIGIN)
        self.playw(s1.title.animate.set_opacity(1))
        self.play(s1.title.animate.move_to(orig_center), run_time=0.5)
        self.playw(
            AnimationGroup(
                *[item.animate.set_opacity(1) for item in s1.words.words], lag_ratio=0.1
            ),
            AnimationGroup(
                *[item.animate.set_opacity(1) for item in s1.exdesc.words],
                lag_ratio=0.1,
            ),
        )

        scene1.generate_target().set_opacity(1).rotate(PI / 3.5, axis=UP).move_to(
            ORIGIN
        ).shift(LEFT * 3.5)
        self.playw(
            MoveToTarget(scene1),
            scene2.animate.rotate(PI / 4, axis=UP)
            .move_to(ORIGIN)
            .shift(RIGHT * 5.5)
            .set_opacity(1),
            self.cf.animate.shift(OUT * 10 + DOWN * 0.5),
        )

        scene1.generate_target().rotate(-PI / 3.5, axis=UP).move_to(ORIGIN)
        scene1.target[0].scale(1.5).set_opacity(0)
        scene1.target[1][2:].set_opacity(0)
        self.play(
            MoveToTarget(scene1),
            scene2.animate.set_opacity(0).shift(RIGHT * 4),
            self.cf.animate.shift(IN * 15 + UP * 1.5),
        )
        self.playw(Circumscribe(s1.words, color=YELLOW_D, stroke_width=2, buff=0.1))
        self.playw(s1.cmd1.animate.set_opacity(1))
        self.playw(s1.cmd2.animate.set_opacity(1))
        self.play(s1.f.animate.set_opacity(1))
        self.play(s1.file.animate.set_opacity(1))
        self.playw(Indicate(s1.file, color=YELLOW_D, scale_factor=1.1))

        scene1.generate_target().rotate(PI / 3.5, axis=UP).move_to(ORIGIN).shift(
            LEFT * 4
        )
        scene2.generate_target().move_to(ORIGIN).shift(RIGHT * 4).set_opacity(1)
        scene2.target[1][4:].set_opacity(0)
        scene2.target[0].set_opacity(0)
        self.cf.generate_target().shift(OUT * 15 + DOWN * 1.5)
        self.play(
            MoveToTarget(scene1),
            MoveToTarget(scene2),
            MoveToTarget(self.cf),
            run_time=0.5,
            rate_func=smooth,
        )

        scene2.generate_target().rotate(-PI / 4, axis=UP).move_to(ORIGIN).shift(
            RIGHT * 2.5 + DOWN * 1.2
        )
        self.play(
            MoveToTarget(scene2),
            scene1.animate.set_opacity(0).shift(LEFT * 4),
            self.cf.animate.shift(IN * 10 + UP * 0.5),
            run_time=0.5,
            rate_func=smooth,
        )
        self.playw(s2.ex2.animate.set_opacity(0.5))
        self.playw(
            s2.exb.animate.set_opacity(1),
            *[item.animate.set_opacity(1) for item in s2.desc.words],
        )
        self.play(Circumscribe(s2.ex1, color=YELLOW_D, stroke_width=2, buff=0.1))
        self.playw(
            Circumscribe(s2.desc.words[1:], color=YELLOW_D, stroke_width=2, buff=0.1)
        )
        self.playw(
            Circumscribe(s2.desc.words[1:], color=YELLOW_D, stroke_width=2, buff=0.1)
        )
        self.playw(s2.cmd.animate.set_opacity(1))
        self.play(s2.sitepkg.animate.set_opacity(1))
        self.remove(s2.piparr.set_opacity(1))
        self.play(GrowArrow(s2.piparr))
        self.playw(s2.pipfile.animate.set_opacity(1))

        self.playwl(
            s2.imp.animate.set_opacity(1),
            self.cf.animate.shift(DOWN + RIGHT * 0.5),
            lag_ratio=0.2,
        )
        self.playw(s2.cmd2.animate.set_opacity(1))
        self.playw(s2.cmd2.words[-1][:-3].animate.set_color(RED_C), run_time=0.5)

        # scene1.rotate(PI / 3, axis=UP).move_to(ORIGIN).shift(LEFT*4)
        # scene2.rotate(PI / 3.5, axis=UP).move_to(ORIGIN).shift(RIGHT*4)
        # self.cf.shift(OUT*10 + DOWN*0.5)
        # self.addw(scene1, scene2)

        for item in [
            *[s2.ex1, s2.ex2],
            *[s2.exb, s2.desc, s2.cmd, s2.piparr],
            *[s2.sitepkg, s2.pipfile],
            *[s2.imp, s2.cmd2],
        ]:
            item.generate_target()
        s2.ex1.target.set_opacity(0).shift(LEFT * 3)
        s2.ex2.target.set_opacity(0).shift(LEFT * 3)
        s2.exb.target.set_opacity(0).shift(LEFT * 3)
        s2.desc.target.shift(LEFT * 3)
        s2.cmd.target.align_to(s2.desc.target, LEFT)
        s2.piparr.target.put_start_and_end_on(
            s2.cmd.target.words[2].get_bottom(), s2.sitepkg.target.get_corner(UR)
        )
        s2.pipfile.target.icon.set_opacity(0)
        s2.pipfile.target.text.scale(1.1).next_to(
            s2.sitepkg.target.text, RIGHT, buff=0.05
        )
        s2.imp.target.shift(UP).set_opacity(0)
        s2.cmd2.target.shift(UP + LEFT * 2)
        self.play(
            *[
                MoveToTarget(item)
                for item in [
                    *[s2.ex1, s2.ex2],
                    *[s2.exb, s2.desc, s2.cmd, s2.piparr],
                    *[s2.pipfile, s2.imp, s2.cmd2],
                ]
            ],
        )
        self.playw(
            Flash(s2.cmd.words[2].get_corner(UL), color=YELLOW_D),
            Circumscribe(s2.cmd.words[2], color=YELLOW_D, stroke_width=2, buff=0.1),
        )
        self.playwl(
            *[Indicate(item, color=YELLOW_D, scale_factor=1.1) for item in s2.cmd.words]
        )
        s2.pipmain.next_to(s2.pipfile.text, RIGHT, buff=0.1)
        self.playw(s2.pipmain.animate.set_opacity(1))

        self.playwl(
            *[
                Indicate(item, color=YELLOW_D, scale_factor=1.1)
                for item in s2.cmd.words
            ],
            lag_ratio=0.3,
            wait=0,
        )
        self.playwl(
            Indicate(s2.sitepkg.text, color=YELLOW_D, scale_factor=1.05),
            Indicate(s2.pipfile.text, color=YELLOW_D, scale_factor=1.1),
            Indicate(s2.pipmain.text, color=YELLOW_D, scale_factor=1.1),
            lag_ratio=0.3,
        )

        scene2.generate_target().rotate(PI / 4, axis=UP).shift(RIGHT * 8).set_opacity(0)
        scene1.generate_target().set_opacity(1).move_to(ORIGIN)
        scene1.target[1][2:].set_opacity(0)
        scene1.target[1][7].set_opacity(1)
        scene1.target[0].scale(1 / 1.5)
        self.play(
            MoveToTarget(scene2),
            MoveToTarget(scene1),
            self.cf.animate.shift(LEFT + OUT * 5),
            run_time=1.5,
        )
        scene1.generate_target().rotate(-PI / 3.5, axis=UP)
        scene1.target[0].set_opacity(0)
        self.playw(MoveToTarget(scene1), self.cf.animate.shift(IN * 10 + UP), wait=2)
        self.playw(
            Flash(s1.exdesc[1:9].get_corner(UL), color=YELLOW_D),
            s1.exdesc[1:9].animate.set_color(YELLOW_D),
        )
        self.play(
            VGroup(s1.exdesc, s1.sitepkg, s1.pkg_folder, s1.pkg_file).animate.shift(
                UP * 1.5
            )
        )
        self.playw(VGroup(s1.sitepkg, s1.pkg_file).animate.set_opacity(1))
        self.play(
            s1.pkg_file.animate.set_opacity(0), s1.pkg_folder.animate.set_opacity(1)
        )
        self.playw(s1.pkg_folder.animate.align_to(s1.pkg_file, UP))
        self.playw(
            Flash(s1.pkg_folder[1].get_corner(UL), color=RED_C),
            Wiggle(s1.pkg_folder[1], scale_value=1.05),
        )
        s1.pkg_init = (
            File("__init__.py")
            .scale(0.65)
            .next_to(s1.pkg_folder[1], DOWN, buff=0.1)
            .align_to(s1.pkg_folder[1], LEFT)
            .set_opacity(0)
        )
        self.playw(s1.pkg_init.animate.set_opacity(1))

        self.playwl(
            VGroup(s1.title, s1.words, s1.exdesc, s1.sitepkg).animate.set_opacity(0.2),
            self.cf.animate.shift(DR + RIGHT * 2 + IN * 5),
        )

    def s1(self):
        title = (
            Text("__main__.py", font=MONO_FONT).set_color(YELLOW_A).shift(2 * UP + LEFT)
        )
        words = (
            Words("폴더가 python 대상일 때 실행", font="Noto Sans KR", font_size=28)
            .set_color(TEAL_A)
            .next_to(title, DOWN, buff=0.5)
            .shift(RIGHT)
        )
        words.words[0].set_color(YELLOW_D)
        cmd1 = Words("python test.py", font=MONO_FONT, font_size=24)
        cmd2 = Words("python folder", font=MONO_FONT, font_size=24)
        cmd2.words[1].set_color(YELLOW_D)
        cmds = (
            VGroup(cmd1, cmd2)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(words, DOWN, buff=0.5)
            .shift(LEFT * 0.5)
        )
        f = Folder("folder/").scale(0.7).next_to(cmd2, buff=0.5)
        file = (
            File("__main__.py")
            .scale(0.7)
            .next_to(f, DOWN, buff=0.2)
            .align_to(f, LEFT)
            .shift(RIGHT * 0.3)
        )
        exdesc = (
            Words("+ python -m으로 활용", font="Noto Sans KR", font_size=28)
            .set_color(TEAL_A)
            .next_to(words, DOWN, buff=2.5, aligned_edge=LEFT)
        )
        sitepkg = (
            Folder(".../lib/python3.11/site-packages/")
            .scale(0.7)
            .next_to(exdesc, DOWN, buff=0.3)
            .shift(RIGHT * 2.5)
        )
        pkg_file = File("pytest.py").scale(0.6).next_to(sitepkg, DOWN, buff=0.2)
        pkg_folder = VGroup(
            (
                pf := Folder("pytest/")
                .scale(0.6)
                .next_to(pkg_file, DOWN, buff=0.2)
                .align_to(pkg_file, LEFT)
            ),
            File("__main__.py").scale(0.65).next_to(pf, RIGHT, buff=0.1),
        )

        return self.organize(locals())

    def s2(self):
        title = Text("활용 사례", font="Noto Sans KR").set_color(YELLOW_A).shift(UL * 2)

        ex1 = Words("pip", font=MONO_FONT, font_size=28).set_color(TEAL_A)
        ex2 = Words("pytest", font=MONO_FONT, font_size=28).set_color(TEAL_A)
        exs = (
            VGroup(ex1, ex2)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .next_to(title, DOWN, buff=0.5)
        )
        exb = Brace(exs, RIGHT, buff=0.5, sharpness=3).set_color(GREY_C)
        desc = Words(
            "파이썬을 모듈로 실행", font="Noto Sans KR", font_size=24, color=GREY_B
        ).next_to(exb, RIGHT, buff=0.1)
        desc.words[1].set_color(YELLOW_D)
        cmd = (
            Words("python -m pip", font=MONO_FONT, font_size=24, color=GREY_A)
            .next_to(desc, DOWN, buff=0.3)
            .shift(RIGHT * 0.2)
        )
        sitepkg = (
            Folder(".../lib/python3.11/site-packages/")
            .scale(0.9)
            .next_to(VGroup(ex2, cmd), DOWN, buff=0.7)
        )
        piparr = Arrow(
            cmd.words[1].get_bottom(),
            sitepkg.get_corner(UR),
            buff=0.1,
            stroke_width=2,
            tip_length=0.15,
            color=GREY_A,
        )
        imp = Words("import pip", font=MONO_FONT, font_size=24, color=GREY_A)
        imp.words[0].set_color(PURPLE_B)
        cmd2 = Words(
            "python .../lib/python3.11/site-packages/pip",
            font=MONO_FONT,
            font_size=24,
            color=GREY_A,
        )
        cmd2.words[0].set_color(YELLOW_B)
        VGroup(imp, cmd2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(
            sitepkg, DOWN, buff=0.7
        ).shift(RIGHT)
        pipfile = (
            Folder("pip/")
            .scale(0.8)
            .next_to(sitepkg, DOWN, buff=0.2)
            .shift(RIGHT * 3.2)
        )
        pipmain = (
            File("__main__.py")
            .scale(0.7)
            .next_to(pipfile, DOWN, buff=0.2)
            .align_to(pipfile, LEFT)
            .shift(RIGHT * 0.3)
        )

        return self.organize(locals())


class forTN(Scene2D):
    def construct(self):
        d = Folder("src/").set_opacity(0.4)
        f1 = File("__main__.py")
        f1.text.set_color(YELLOW)
        f2 = File("A.py").set_opacity(0.4)
        f3 = File("B.py").set_opacity(0.4)

        fs = (
            VGroup(f1, f2, f3)
            .arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            .next_to(d, DOWN, buff=0.4)
            .align_to(d, LEFT)
            .shift(RIGHT * 0.5)
        )
        VGroup(d, fs).move_to(ORIGIN).scale(1.7)
        self.addw(d, fs, wait=10)
