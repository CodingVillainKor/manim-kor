from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        kwargs = Text("kwargs").set_color_by_gradient(GREEN_B, GREEN_D)
        self.addw(kwargs)

        full_kwargs = Text("keyword arguments").set_color_by_gradient(GREEN_B, GREEN_D)
        self.playwl(
            *[
                AnimationGroup(
                    Transform(
                        kwargs[0],
                        full_kwargs[0],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        kwargs[1],
                        full_kwargs[3],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        kwargs[2:5],
                        full_kwargs[7:10],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        kwargs[5],
                        full_kwargs[-1],
                        replace_mobject_with_target_in_scene=True,
                    ),
                ),
                AnimationGroup(
                    FadeIn(full_kwargs[1:3]),
                    FadeIn(full_kwargs[4:7]),
                    FadeIn(full_kwargs[10:-1]),
                ),
            ],
            lag_ratio=0.3,
            wait=2,
        )

        model_config = Code(
            code_string=r'model_config = {"dim": 64}', language="python"
        )[2]
        model = Code(code_string=r"model = Model(**model_config)", language="python")[2]
        model_ = Code(code_string=r"model = Model(dim=64)", language="python")[2]
        models = VGroup(model_config, model).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        model_.move_to(model).align_to(model, LEFT)

        self.playwl(full_kwargs.animate.shift(UP * 2), FadeIn(models), lag_ratio=0.2)

        self.play(
            VGroup(model_config[0][:12], model[0][-13:-1]).animate.set_color(YELLOW)
        )
        self.play(
            model[0][-13:-1].animate.set_opacity(0.2),
            model_config[0][14:].animate.move_to(model[0][-13:-4]),
        )
        self.playw(
            FadeOut(
                model[0][14:16], model_config[0][15], model_config[0][-1], shift=DOWN
            ),
            FadeOut(model_config[0][16], target_position=model_[0][-8]),
            FadeOut(model_config[0][20], target_position=model_[0][-4]),
            Transform(
                model_config[0][17:20],
                model_[0][-7:-4],
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                model_config[0][21],
                model_[0][-4],
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                model_config[0][23:25],
                model_[0][-3:-1],
                replace_mobject_with_target_in_scene=True,
            ),
            FadeOut(model[0][-13:-1]),
            Transform(
                model[0][-1], model_[0][-1], replace_mobject_with_target_in_scene=True
            ),
        )


class whykwargs(Scene2D):
    def construct(self):
        c = PythonCode("src/train.py").scale(0.8)
        c.code[:-2].set_opacity(0.3)
        c.code[-1].set_opacity(0.3)

        self.playw(FadeIn(c))

        self.playw_return(
            c.text_slice(6, "**model_config").animate.shift(UP * 0.3), run_time=0.75
        )

        self.playw(c.code[3].animate.set_opacity(1))

        yml = (
            Code(code_file="config.yaml", language="yaml", add_line_numbers=False)
            .scale(0.8)
            .next_to(c, LEFT)
        )
        self.playw(ApplyWave(c.text_slice(4, "model_config"), amplitude=0.1))
        self.playw(c.code[1:3].animate.set_opacity(1))
        VGroup(yml, c.generate_target()).arrange(RIGHT, buff=1)
        self.playwl(MoveToTarget(c), FadeIn(yml), lag_ratio=0.4)

        file_name = (
            Text("config.yaml", font_size=18)
            .next_to(yml, UP, buff=0.05)
            .align_to(yml, LEFT)
        )
        self.playw(FadeIn(file_name))

        carr = Arrow(
            yml.get_right(),
            c.text_slice(6, "Model").get_top() + LEFT * 0.15,
            tip_length=0.175,
            stroke_width=3,
            buff=0.1,
        )
        self.playw(GrowArrow(carr))

        self.play((ymlc := yml.copy()).animate.move_to(c.code[1:3]).scale(0.5))
        ymlc.set_z_index(1)
        self.playw(Indicate(c.code[1:3], scale_factor=1.1), FadeOut(ymlc))
        hl, hlo = c.highlight(4)
        self.playw(hl, run_time=0.7)
        self.play(
            hlo,
            (cmc := c.text_slice(4, "model_config").copy()).animate.move_to(
                c.text_slice(6, "model_config")
            ),
        )
        arg_text = (
            Text("dim=64, depth=6", font_size=24, font=MONO_FONT)
            .scale(0.8)
            .move_to(c.text_slice(6, "**model_config"))
            .align_to(c.text_slice(6, "**model_config"), LEFT)
        )
        self.play(FadeOut(cmc))
        cmc = c.text_slice(6, "**model_config")
        cmc.save_state()
        c5p = c.code[5][-1]
        c5p.save_state()
        self.playwl(
            c5p.animate.next_to(arg_text, RIGHT, buff=0.05),
            Transform(
                c.text_slice(6, "**model_config"),
                arg_text,
            ),
            lag_ratio=0.3,
        )
        self.play(Restore(cmc), Restore(c5p))
        self.playwl(
            FadeOut(yml, carr, file_name), c.animate.move_to(ORIGIN), lag_ratio=0.5
        )


class singlemodel(Scene2D):
    def construct(self):
        c1 = PythonCode("src/train.py").scale(0.8)
        c2 = PythonCode("src/train2.py").scale(0.8).align_to(c1, UP)
        VGroup(c1.code[0], c1.code[-1], c2.code[0], c2.code[-1]).set_opacity(0.3)

        self.addw(c1)

        self.playw(
            Transform(c1.frame, c2.frame),
            Transform(c1.code[:4], c2.code[:4]),
            Transform(
                c1.text_slice(6, "model = Model("), c2.text_slice(6, "model = Model(")
            ),
            Transform(c1.text_slice(6, "**model"), c2.code[6]),
            Transform(c1.text_slice(6, "_config"), c2.code[7]),
            Transform(c1.text_slice(6, ")"), c2.text_slice(9, ")")),
            Transform(c1.code[-1], c2.code[-1]),
        )


class multimodel(Scene2D):
    def construct(self):
        c = PythonCode("src/multi.py").scale(0.8).shift(UP * 0.3)
        VGroup(c.code[0], c.code[-1]).set_opacity(0.3)
        c.code[4:9].set_opacity(0)

        self.addw(c)

        self.playw(
            c.code[4:9].animate.set_opacity(1),
            c.code[1:3].animate.set_opacity(0.3),
            c.code[-2].animate.set_opacity(0.3),
        )
        self.playw(c.animate.shift(LEFT * 2.5))

        m1 = PythonCode("src/Model1.py").scale(0.6)
        m2 = PythonCode("src/Model2.py").scale(0.6)
        ms = VGroup(m1, m2).arrange(DOWN, buff=1).next_to(c, RIGHT, buff=0.3)

        self.play(FadeIn(m1))
        self.playwl(
            Indicate(m1.text_slice(2, "n_layers")),
            Indicate(m1.text_slice(2, "hidden_dim")),
            lag_ratio=0.5,
        )
        self.play(FadeIn(m2))
        self.playwl(
            Indicate(m2.text_slice(2, "n_embed")),
            Indicate(m2.text_slice(2, "hidden_dim")),
            lag_ratio=0.5,
        )
        self.playw(
            Circumscribe(c.code[8]),
            c.text_slice(5, "models").animate.set_color(YELLOW),
            c.text_slice(9, "models").animate.set_color(YELLOW),
        )
        self.playw(Flash(c.text_slice(6, "Model1", nth=2)))
        self.playw(Flash(c.text_slice(7, "Model2", nth=2)))

        self.wait(3)

        self.playw(c.code[10].animate.set_opacity(1))
        self.playw(
            c.code[1:3].animate.set_opacity(1), c.code[3:].animate.set_opacity(0.3)
        )


class outro(Scene2D):
    def construct(self):
        # continue from multimodel's last frame
        c = PythonCode("src/multi.py").scale(0.8).shift(UP * 0.3).shift(LEFT * 2.5)
        VGroup(c.code[0], c.code[3:]).set_opacity(0.3)

        m1 = PythonCode("src/Model1.py").scale(0.6)
        m2 = PythonCode("src/Model2.py").scale(0.6)
        ms = VGroup(m1, m2).arrange(DOWN, buff=1).next_to(c, RIGHT, buff=0.3)

        self.addw(c, m1, m2)

        m3 = PythonCode("src/Model3.py").scale(0.6)
        ms.add(m3)
        ms.generate_target()
        ms.target.arrange(DOWN, buff=0.5, aligned_edge=LEFT).align_to(m1, LEFT)
        ms[-1].move_to(ms.target[-1]).set_opacity(0)
        self.playw(MoveToTarget(ms))

        c3 = PythonCode("src/multi_.py").scale(0.8).move_to(c)
        VGroup(c3.code[0], c3.code[9:]).set_opacity(0.3)
        self.playw(
            c.frame.animate.become(c3.frame),
            c.code[:7].animate.become(c3.code[:7]),
            c.code[7:].animate.become(c3.code[8:]),
            FadeIn(c3.code[7]),
        )

        self.playwl(
            m1.text_slice(2, "n_").animate.set_opacity(0),
            m1.text_slice(2, "layers, hidden_dim):").animate.align_to(
                m1.text_slice(2, "n_"), LEFT
            ),
            lag_ratio=0.5
        )

        self.play(c.code[-2].animate.set_opacity(1))
        self.playw(
            ApplyWave(c.text_slice(11, '**config["model_config"]'), amplitude=0.1)
        )