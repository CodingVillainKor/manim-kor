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
                model_config[0][21], model_[0][-4], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                model_config[0][23:25], model_[0][-3:-1], replace_mobject_with_target_in_scene=True
            ),
            FadeOut(model[0][-13:-1]),
            Transform(
                model[0][-1], model_[0][-1], replace_mobject_with_target_in_scene=True
            ),
        )
