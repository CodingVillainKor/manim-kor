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
            VGroup(
                file, c2.text_slice(4, 'config["data"]'), config_model
            ).animate.set_color(YELLOW)
        )
        self.playw(self.cf.animate.shift(UP * 3), hydra_text.animate.scale(1.5))


class usecase(Scene3D):
    def construct(self):
        root = FileSystem(folders=["configs"], files=["run.py"]).scale(0.8)
        configs = FileSystem(folders=[], files=["config.yaml"]).scale(0.6)
        VGroup(root, configs).arrange(RIGHT, aligned_edge=UP, buff=0.5).shift(LEFT * 3)
        configs_text = (
            Text("configs/", font_size=18, color=YELLOW_B)
            .next_to(configs, UP, buff=0.1)
            .align_to(configs, LEFT)
        )
        folder_link = DashedLine(root.folders[0].get_right(), configs.frame.get_left())
        self.playw(FadeIn(root))
        self.playw(FadeIn(configs, configs_text, folder_link))

        c3 = (
            PythonCode("src/c3.py")
            .rotate(PI / 4, DOWN)
            .scale(0.8)
            .next_to(configs, RIGHT, buff=1)
        )
        c3.code[4:7].set_opacity(0.3)
        self.playw(FadeIn(c3, shift=RIGHT))
        arg_config = c3.text_slice(4, "config")
        self.playw(Flash(arg_config), arg_config.animate.set_color(YELLOW))
        config_file = configs.files[0].copy()
        self.playw(config_file.animate.become(arg_config.copy()))

        self.playw(c3.code[4:7].animate.set_opacity(1.0))

        self.playw(
            Flash(c3.text_slice(5, 'config["data"]')),
            c3.text_slice(5, 'config["data"]').animate.set_color(YELLOW),
        )
        self.playw(
            Flash(c3.text_slice(6, "config.model")),
            c3.text_slice(6, "config.model").animate.set_color(YELLOW),
        )

        c4 = (
            PythonCode("src/c4.py")
            .rotate(PI / 4, DOWN)
            .scale(0.8)
            .move_to(c3)
            .align_to(c3, UP)
            .align_to(c3, LEFT)
        )
        c3.frame.set_z_index(-1)
        c4.frame.set_z_index(-1)
        c4.code[4:9].set_opacity(0)
        self.playw(
            c3.frame.animate.become(c4.frame),
            c3.code[:4].animate.become(c4.code[:4]),
            c3.code[-2:].animate.become(c4.code[-2:]),
            c3.code[4:7].animate.set_opacity(0),
            arg_config.animate.set_opacity(0),
            c4.code[4:10].animate.set_opacity(1),
        )

        self.playw(
            Flash(c4.text_slice(5, "config.data")),
            c4.text_slice(5, "config.data").animate.set_color(YELLOW),
        )
        self.playw(
            Flash(c4.text_slice(6, '.get("pretrained")')),
            c4.text_slice(6, '.get("pretrained")').animate.set_color(YELLOW),
        )
        
