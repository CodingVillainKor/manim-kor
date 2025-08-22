from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        hydra_text = Text("Hydra").set_color_by_gradient(BLUE, BLUE_D)
        self.playwl(*[FadeIn(item) for item in hydra_text], lag_ratio=0.1)
        self.playw(hydra_text.animate.shift(UP * 3))

        c1 = PythonCode("src/c1.py")
        c2 = PythonCode("src/c2.py")

        c1.code[1].set_opacity(0.3)
        self.playw(FadeIn(c1))
        config_model = c1.text_slice(5, "config.model")
        config_model.save_state()
        self.playwl(
            Flash(config_data := c1.text_slice(4, "config.data")),
            config_data.animate.set_color(YELLOW),
            Flash(config_model),
            config_model.animate.set_color(YELLOW),
            lag_ratio=0.3,
        )

        self.playw(
            c1.code[1].animate.set_opacity(1), c1.code[3:].animate.set_opacity(0.3)
        )

        self.play(
            c1.code[1].animate.set_opacity(0.3), c1.code[3:].animate.set_opacity(1)
        )
        self.playw(
            FadeTransform(
                c1.text_slice(4, "config.data)"), c2.text_slice(4, 'config["data"])')
            ),
            Restore(config_model),
        )
        c1.text_slice(4, "config.data)").set_opacity(0)
        self.playw(Flash(config_model), wait=3)

        self.playw(
            VGroup(c1, c2.text_slice(4, 'config["data"])'))
            .animate.rotate(PI / 4, DOWN)
            .shift(RIGHT * 2)
        )

        command = (
            Text("python main.py -c file", font=MONO_FONT, font_size=24)
            .next_to(c1, LEFT, buff=0.5)
            .set_color_by_gradient(GREEN_B, GREEN_C)
        )
        self.playwl(
            *[FadeIn(item) for item in command], c1.code[1].animate.set_opacity(0)
        )
        file = command[-4:].copy().set_color(YELLOW)
        self.playw(
            file.animate.become(
                VGroup(c2.text_slice(4, "config"), c1.text_slice(5, "config")).copy()
            )
        )
        self.playw(
            VGroup(file, c2.text_slice(4, 'config["data"]'), config_model).animate.set_color(YELLOW)
        )
        self.playw(self.cf.animate.shift(UP*3), hydra_text.animate.scale(1.5))
