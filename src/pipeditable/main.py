from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class pipinstall(Scene2D):
    def construct(self):
        cmd = Words("pip install torch", font=MONO_FONT).set_color_by_gradient(
            GREY_B, GREY_A
        )

        self.playwl(*[FadeIn(item) for item in cmd.words], lag_ratio=0.3)

        self.play(cmd.animate.scale(0.5).shift(LEFT * 3))
        code = PythonCode("src/c1.py").next_to(cmd, RIGHT, buff=1.5)
        arrow = Arrow(
            cmd.get_right(), code.get_left(), buff=0.1, tip_length=0.2, stroke_width=3
        )
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(code))
        self.playw(Indicate(code.code[0][-5:]), Indicate(cmd.words[-1]))
        self.cf.save_state()
        self.play(FadeOut(arrow), self.cf.animate.shift(UP))
        sp = FolderIcon("site-packages/").shift(UP * 2.5)
        arrowsp = Arrow(
            code.code[0][:-5].get_top(),
            sp.get_bottom(),
            buff=0.1,
            tip_length=0.2,
            stroke_width=3,
        )
        self.play(FadeIn(sp), GrowArrow(arrowsp))
        self.play(
            arrowsp.animate.put_start_and_end_on(
                code.code[0][:-5].get_top(), sp.get_bottom() + RIGHT
            )
        )
        self.play(
            arrowsp.animate.put_start_and_end_on(
                code.code[0][:-5].get_top(), sp.get_bottom() + LEFT
            )
        )
        self.playw(
            arrowsp.animate.put_start_and_end_on(
                code.code[0][:-5].get_top(), sp.get_bottom()
            )
        )

        self.play(FadeOut(arrowsp), code.code.animate.set_opacity(0.3))
        self.playw(Indicate(cmd))
        torch = FolderIcon("torch/").scale(0.85).next_to(sp, DOWN)
        self.playw(FadeIn(torch, shift=RIGHT))

        self.play(Restore(self.cf), FadeOut(code, torch, sp))
        cmd2 = Words(
            "pip install .", font=MONO_FONT, font_size=24
        ).set_color_by_gradient(GREY_B, GREY_A)
        self.playw(
            *[Transform(cmd.words[i], cmd2.words[i]) for i in range(len(cmd.words))]
        )
        cwd = Text("~/prj$", font_size=24, font=MONO_FONT).next_to(cmd, LEFT)

        cwdf = Folder().scale(0.125).next_to(cwd, LEFT, buff=0.15)
        self.playw(FadeIn(cwd))
        mypkg = (
            FolderIcon("mypkg/")
            .next_to(cmd, UP, buff=1)
            .align_to(cwdf, LEFT)
            .scale(0.7)
        )
        self.play(FadeIn(cwdf))
        cwdf.generate_target().shift(UP * 2)
        cwdd_ = Text("~/prj/", font_size=24, font=MONO_FONT).next_to(cwdf.target, RIGHT)
        self.play(
            cwdf.animate.shift(UP * 2), (cwdd := cwd.copy()).animate.become(cwdd_)
        )
        self.play(FadeIn(mypkg, target_position=cwdf, scale=0.2))

        sp.next_to(cwdf, RIGHT, buff=4)
        self.playw(FadeIn(sp))
        self.playw(mypkg.copy().animate.next_to(sp, DOWN, buff=0.2).shift(LEFT * 0.8))


class pipinstalleditable(Scene2D):
    def construct(self):
        cmd = Words("pip install -e .", font_size=24, font=MONO_FONT)
        cmd.words[2].set_color(PURE_GREEN)
        cwd = Text("~/prj$", font_size=24, font=MONO_FONT).next_to(cmd, LEFT)

        cwdf = Folder().scale(0.125).next_to(cwd, UP, buff=2).shift(LEFT * 1.5)
        cwdd = Text("~/prj/", font_size=24, font=MONO_FONT).next_to(cwdf, RIGHT)
        mypkg = FolderIcon("mypkg/").next_to(cwdd, DOWN).scale(0.7)
        sp = FolderIcon("site-packages/").next_to(cwdf, RIGHT, buff=4)
        self.playw(FadeIn(cmd, cwd))
        self.playw(FadeIn(cwdf, cwdd, mypkg, sp))

        symbolic_link = (
            FileIcon("mypkg.egg-link").scale(0.75).next_to(sp, DOWN, buff=0.2)
        )
        self.play(
            Transform(
                mypkg.copy(), symbolic_link, replace_mobject_with_target_in_scene=True
            )
        )
        symarrow = Arrow(
            symbolic_link.get_left(),
            mypkg.get_right(),
            buff=0.1,
            tip_length=0.2,
            stroke_width=3,
        )
        self.playw(GrowArrow(symarrow))
        code = PythonCode("src/c2.py").shift(RIGHT)
        self.playw(
            VGroup(cwd, cmd).animate.shift(LEFT * 3).scale(0.6).set_opacity(0.3),
            FadeIn(code),
        )
        sparrow = Arrow(
            code.text_slice(1, "import").get_top(),
            sp.get_bottom(),
            buff=0.1,
            tip_length=0.2,
            stroke_width=3,
        )
        self.playw(
            GrowArrow(sparrow), VGroup(symbolic_link, symarrow).animate.set_opacity(0.3)
        )
        self.playwl(
            sparrow.animate.put_start_and_end_on(
                code.text_slice(1, "mypkg").get_top(), symbolic_link.get_bottom()
            ),
            VGroup(symbolic_link, symarrow).animate.set_opacity(1),
            lag_ratio=0.5,
        )
        self.playwl(
            *[Indicate(item) for item in [symbolic_link, symarrow, mypkg]],
            lag_ratio=0.3,
        )


class difference(Scene2D):
    def construct(self):
        cwdft = Folder().scale(0.125).shift(UP * 2.5 + LEFT * 3.5)
        cwddt = Text("~/prj/", font_size=24, font=MONO_FONT).next_to(cwdft, RIGHT)
        mypkgt = FolderIcon("mypkg/").next_to(cwddt, DOWN).scale(0.7)
        spt = FolderIcon("site-packages/").next_to(cwddt, RIGHT, buff=4)
        symbolic_link = (
            FileIcon("mypkg.egg-link").scale(0.75).next_to(spt, DOWN, buff=0.2)
        )

        cwdtb = Folder().scale(0.125).shift(DOWN + LEFT * 3.5)
        cwddb = Text("~/prj/", font_size=24, font=MONO_FONT).next_to(cwdtb, RIGHT)
        mypkgb = FolderIcon("mypkg/").next_to(cwddb, DOWN).scale(0.7)
        spb = FolderIcon("site-packages/").next_to(cwddb, RIGHT, buff=4)
        pkg = mypkgb.copy().next_to(spb, DOWN, buff=0.2).shift(LEFT * 0.8)

        self.play(FadeIn(cwdft, cwddt, mypkgt, spt))
        self.play(
            Transform(
                mypkgt.copy(), symbolic_link, replace_mobject_with_target_in_scene=True
            )
        )
        symarrow = Arrow(
            symbolic_link.get_left(),
            mypkgt.get_right(),
            buff=0.1,
            tip_length=0.2,
            stroke_width=3,
        )
        self.playw(GrowArrow(symarrow))
        self.playw(FadeIn(cwdtb, cwddb, mypkgb, spb))
        self.playw(
            Transform(mypkgb.copy(), pkg, replace_mobject_with_target_in_scene=True)
        )

        self.wait()
        self.playwl(
            *[
                Indicate(item, scale_factor=1.1)
                for item in [symbolic_link, symarrow, mypkgt]
            ],
            lag_ratio=0.3,
        )
        self.playw(Flash(mypkgt), mypkgt.text.animate.set_color(BLUE))
        self.playwl(
            *[
                Indicate(item, scale_factor=1.1)
                for item in [symbolic_link, symarrow, mypkgt]
            ],
            lag_ratio=0.3,
        )
        self.wait()

        self.playw(Circumscribe(mypkgb), Circumscribe(pkg))
        self.playw(Flash(mypkgb), mypkgb.text.animate.set_color(BLUE))
        self.playw(Flash(pkg), pkg.text.animate.set_color(BLUE))

        self.playw(
            Flash(mypkgb, color=ORANGE),
            Flash(pkg, color=ORANGE),
            VGroup(mypkgb.text, pkg.text).animate.set_color(ORANGE)
        )
