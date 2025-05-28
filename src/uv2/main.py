from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        command_title = Text("uv commands", font_size=60).set_color_by_gradient(
            BLUE_A, BLUE_C
        )
        core_title = Text("uv core", font_size=60).set_color_by_gradient(BLUE_A, BLUE_C)

        commands = VGroup(
            Text("uv run", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
            Text("uv add", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
            Text("uv remove", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
            Text("uv sync", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)

        cores = VGroup(
            Text(".venv/", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
            Text("uv.lock", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
            Text("pyproject.toml", font_size=40).set_color_by_gradient(
                GREEN_A, GREEN_C
            ),
            Text("...", font_size=40).set_color_by_gradient(GREEN_A, GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)

        titles = (
            VGroup(command_title, core_title)
            .arrange(RIGHT, buff=2, aligned_edge=DOWN)
            .shift(UP * 2.5 + LEFT * 0.7)
        )

        commands.next_to(titles[0], DOWN, buff=1).align_to(titles[0], LEFT).shift(RIGHT)
        cores.next_to(titles[1], DOWN, buff=1).align_to(titles[1], LEFT).shift(
            RIGHT * 0.5
        )

        self.play(FadeIn(command_title))
        self.playw(
            LaggedStart(
                *[FadeIn(command) for command in commands],
                lag_ratio=0.5,
            )
        )

        self.play(FadeIn(core_title))
        self.playw(
            LaggedStart(
                *[FadeIn(core) for core in cores],
                lag_ratio=0.5,
            )
        )


class whatisuv(Scene2D):
    def construct(self):
        title = Text("uv?", font_size=60).set_color_by_gradient(BLUE_A, BLUE_C)

        self.playw(FadeIn(title))
        self.playw(title.animate.shift(UP * 2))

        sentence = Text(
            "Python package management tool", font_size=40
        ).set_color_by_gradient(GREEN_A, GREEN_C)
        word_indices = [0, 6, 13, 23, 30]
        words = [sentence[i:j] for i, j in zip(word_indices, word_indices[1:] + [None])]
        self.playw(
            LaggedStart(
                *[FadeIn(word) for word in words],
                lag_ratio=0.6,
            )
        )
        prj_folder = (
            FolderIcon("project/")
            .scale(1.2)
            .next_to(words[0], UP, buff=0.1)
            .align_to(words[0], LEFT)
        )
        pkg1 = (
            FolderIcon("numpy/")
            .next_to(prj_folder, DOWN, buff=0.3)
            .align_to(prj_folder, LEFT)
            .shift(RIGHT * 0.5)
        )
        pkg2 = FolderIcon("pandas/").next_to(pkg1, DOWN, buff=0.2).align_to(pkg1, LEFT)
        pkg3 = FolderIcon("torch/").next_to(pkg2, DOWN, buff=0.2).align_to(pkg2, LEFT)

        self.play(
            LaggedStart(
                *[
                    Transform(word, item, replace_mobject_with_target_in_scene=True)
                    for word, item in zip(words, [prj_folder, pkg1, pkg2, pkg3])
                ],
                lag_ratio=0.3,
            )
        )
        self.playw(FadeOut(pkg3))

        uvlock = File().shift(RIGHT * 3.5).scale(1.5).shift(DOWN * 0.5)
        self.playw(FadeIn(uvlock))
        numpyver = Text("numpy==1.23.5", font_size=24, color=BLACK)
        pandasver = Text("pandas==1.5.3", font_size=24, color=BLACK)
        versions = VGroup(numpyver, pandasver).arrange(DOWN, aligned_edge=LEFT).move_to(uvlock).set_z_index(1)
        self.playw(LaggedStart(
            *[FadeIn(ver) for ver in versions],
            lag_ratio=0.3,
        ))

        pyversion = Text("python==3.10.6", font_size=24, color=BLACK).next_to(
            versions, DOWN, buff=0.2
        ).align_to(versions, LEFT)
        self.play(FadeIn(pyversion))
        self.playw(Circumscribe(pyversion, color=BLUE))
