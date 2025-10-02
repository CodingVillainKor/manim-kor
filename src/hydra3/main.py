from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        import1 = Words("from modela import ModelA", font=MONO_FONT, font_size=24)
        import2 = Words("from modelb import ModelB", font=MONO_FONT, font_size=24)
        import3 = Words("from modelc import ModelC", font=MONO_FONT, font_size=24)
        for item in [import1, import2, import3]:
            item.words[0].set_color(PURPLE_B)
            item.words[2].set_color(PURPLE_B)
        imports = (
            VGroup(import1, import2, import3)
            .arrange(DOWN, buff=0.2)
            .shift(UP + LEFT * 2)
        )

        ia = (
            Text("m = ModelA(**config.model)", font=MONO_FONT, font_size=24)
            .next_to(imports, DOWN, buff=1)
            .align_to(imports, LEFT)
        )
        ib = (
            Text("m = ModelB(**config.model)", font=MONO_FONT, font_size=24)
            .next_to(imports, DOWN, buff=1)
            .align_to(imports, LEFT)
        )
        ic = (
            Text("m = ModelC(**config.model)", font=MONO_FONT, font_size=24)
            .next_to(imports, DOWN, buff=1)
            .align_to(imports, LEFT)
        )

        ma = PythonCode("src/modela.py").scale(1.2)
        mb = PythonCode("src/modelb.py").scale(1.2)
        mc = PythonCode("src/modelc.py").scale(1.2)
        ms = (
            VGroup(ma, mb, mc)
            .arrange(DOWN, buff=0.5)
            .scale(0.7)
            .next_to(imports, RIGHT, buff=2)
            .shift(DOWN)
        )
        self.playw(FadeIn(import1, ia, ma))
        self.playw(FadeIn(import2, mb))
        self.playw(FadeIn(import3, mc))

        self.play(FadeOut(ia[7], shift=UP * 0.3), FadeIn(ib[7], shift=UP * 0.3))
        self.playw(FadeOut(ib[7], shift=UP * 0.3), FadeIn(ic[7], shift=UP * 0.3))
        ia = VGroup(*ia[:7], ic[7], *ia[8:])

        self.playwl(*[Flash(item.words[-1]) for item in imports], lag_ratio=0.3)

        self.wait(2)

        ii = (
            Text("m = instantiate(config.model)", font=MONO_FONT, font_size=24)
            .move_to(ia)
            .align_to(ia, LEFT)
        )
        ii[2:13].set_color(YELLOW)
        self.playw(Transform(ia, ii, replace_mobject_with_target_in_scene=True))
        self.playw(
            ii.animate.scale(1.1).align_to(ii, LEFT),
            VGroup(ma, mb, mc, imports).animate.set_opacity(0.2),
            run_time=2.5,
        )


class outro(Scene3D):
    def construct(self):
        main = PythonCode("src/main.py").scale(0.8)
        cfg = Code("src/config.yaml", language="yaml", add_line_numbers=False).scale(
            0.8
        )

        VGroup(main, cfg).arrange(RIGHT, buff=1, aligned_edge=UP)
        models = PythonCode("src/models.py").rotate(-PI / 3, axis=UP).next_to(cfg, DOWN)

        main.code[:-1].set_opacity(0.3)
        main.text_slice(6, "config.model").set_color(YELLOW)
        cfg[-1][0].set_color(YELLOW)

        self.playw(FadeIn(main, cfg, models))

        get_cline = lambda: DashedLine(
            main.text_slice(6, ")").get_right(),
            cfg[-1][0].get_left(),
            stroke_width=2,
            color=YELLOW,
            buff=0.05,
        )
        cline = get_cline()
        mline = DashedLine(
            cfg[-1][1][-6].get_bottom(),
            models.text_slice(1, "Transformer").get_top(),
            stroke_width=2,
            color=BLUE_B,
            buff=0.1,
        )
        self.play(FadeIn(cline))
        self.playw(FadeIn(mline))

        tclass = models.text_slice(1, "Transformer")
        dim256 = cfg[-1][2]
        dimc = dim256.copy()
        dimc.generate_target()
        dimc.target.become(
            Text("dim=256", font=MONO_FONT, font_size=24)
            .scale(0.8)
            .set_color(YELLOW)
            .move_to(main.text_slice(6, "config.model"))
            .align_to(main.text_slice(6, "config.model"), LEFT)
        )
        cline.add_updater(lambda l: l.become(get_cline()))
        self.playw(
            (tclassc := tclass.copy())
            .animate.rotate(PI / 3, UP)
            .scale(0.8)
            .move_to(main.text_slice(6, "instantiate")),
            FadeOut(main.text_slice(6, "instantiate")),
            MoveToTarget(dimc),
            FadeOut(main.text_slice(6, "config.model")),
            main.text_slice(6, ")").animate.next_to(dimc.target, RIGHT, buff=0.05),
        )
