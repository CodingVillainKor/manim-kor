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

        uvlock = FileIcon().shift(RIGHT * 3.5).scale(1.5).shift(DOWN * 0.5)
        self.playw(FadeIn(uvlock))
        numpyver = Text("numpy==1.23.5", font_size=24, color=BLACK)
        pandasver = Text("pandas==1.5.3", font_size=24, color=BLACK)
        versions = (
            VGroup(numpyver, pandasver)
            .arrange(DOWN, aligned_edge=LEFT)
            .move_to(uvlock)
            .set_z_index(1)
        )
        self.playw(
            LaggedStart(
                *[FadeIn(ver) for ver in versions],
                lag_ratio=0.3,
            )
        )

        pyversion = (
            Text("python==3.10.6", font_size=24, color=BLACK)
            .next_to(versions, DOWN, buff=0.2)
            .align_to(versions, LEFT)
        )
        self.play(FadeIn(pyversion))
        self.playw(Circumscribe(pyversion, color=BLUE))


class whyuvlock(Scene2D):
    def construct(self):
        title = Text(
            "Why uv.lock / pyproject.toml?",
            font_size=60,
            t2c={"uv.lock": YELLOW_C, "pyproject.toml": BLUE_D},
        )

        slices = [title[:3], title[3:11], title[11:]]
        uvlock = File("uv.lock").next_to(slices[1], UP)
        pyproject = File("pyproject.toml").next_to(slices[2], UP)
        self.play(
            LaggedStart(
                *[FadeIn(c) for c in slices],
                lag_ratio=0.1,
            )
        )
        self.playw(FadeIn(uvlock, shift=UP * 0.5), FadeIn(pyproject, shift=UP * 0.5))

        venv = FolderIcon(".venv/").next_to(uvlock, LEFT, buff=0.5)
        self.playw(FadeIn(venv, shift=UP * 0.5), FadeOut(title))
        self.playw(
            VGroup(venv, uvlock, pyproject).animate.arrange(RIGHT, buff=0.75).scale(1.2)
        )
        spec = VGroup(uvlock, pyproject)
        spec.save_state()
        self.cf.save_state()
        self.playw(spec.animate.set_color(PURE_RED))
        self.playw(
            Restore(spec), venv.animate.set_opacity(0.3), self.cf.animate.move_to(spec)
        )
        github = ImageMobject("githubmark.png").next_to(spec, UP, buff=0.3).scale(0.5)
        self.playw(FadeIn(github))
        self.playw(Restore(self.cf), venv.animate.set_opacity(1))

        fivegb = Text("5GB", color=PURE_RED).next_to(venv, DOWN)
        self.playw(Circumscribe(venv))
        self.playw(FadeIn(fivegb, shift=DOWN * 0.5))
        venv.save_state()
        self.play(
            venv.animate.next_to(github, DL, buff=0).shift(UP * 0.3),
            rate_func=rate_functions.rush_into,
        )
        github.save_state()
        github.scale(1.1)
        self.playw(
            Restore(venv),
            Restore(github),
            rate_func=rate_functions.rush_from,
            run_time=0.6,
        )
        self.playw(Circumscribe(venv, color=PURE_RED))


class outro(Scene3D):
    def construct(self):
        uvadd = Text("uv add", font_size=32, font="Noto Mono", color=GREEN_B)
        uvpipinstall = Text(
            "uv pip install", font_size=32, font="Noto Mono", color=YELLOW_B
        )

        venv = FolderIcon(".venv/").scale(1.2).shift(UP * 0.5 + LEFT * 3)
        pyproject = File("pyproject.toml")
        pyproject[0].scale(6)
        pyproject.arrange(DOWN)
        uvlock = File("uv.lock")
        uvlock[0].scale(6)
        uvlock.arrange(DOWN).shift(RIGHT * 3.5 + DOWN * 0.5)

        elements = (
            VGroup(venv, pyproject, uvlock)
            .arrange(RIGHT, buff=0.5)
            .shift(DOWN * 0.5 + RIGHT * 1.2)
        )
        elements.save_state()
        commands = (
            VGroup(uvadd, uvpipinstall)
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.75)
            .shift(LEFT * 5 + UP)
        )
        self.playw(FadeIn(uvadd))
        self.playw(*[FadeIn(item) for item in elements])
        package1 = (
            Text("numpy >= 1.23.5", font_size=18, color=BLACK)
            .move_to(pyproject[0])
            .shift(UP * 0.5)
        )
        package2 = (
            Text("name=numpy", font_size=18, color=BLACK)
            .move_to(uvlock[0])
            .shift(UP * 0.5)
        )
        installed = FolderIcon("numpy/").next_to(venv, DOWN)
        self.playw(
            FadeIn(package1, target_position=uvadd),
            FadeIn(package2, target_position=uvadd),
            FadeIn(installed, target_position=uvadd),
        )
        self.playw(
            FadeIn(uvpipinstall), FadeOut(package1, package2), FadeOut(installed)
        )

        self.playw(FadeIn(installed, target_position=uvpipinstall))
        self.playw(LaggedStart(FadeOut(uvpipinstall, installed), Circumscribe(uvadd)))
        self.playw(
            FadeIn(package1, target_position=uvadd),
            FadeIn(package2, target_position=uvadd),
            FadeIn(installed, target_position=uvadd),
        )

        self.playw(
            FadeOut(uvadd, package1, package2, installed),
            VGroup(*elements[1:]).animate.set_opacity(0.3),
            FadeIn(uvpipinstall),
        )
        self.playw(uvlock.animate.set_color(GOLD_D).set_opacity(1))
        self.playw(Circumscribe(uvpipinstall))

        self.playw(FadeOut(uvpipinstall), Restore(elements))

        self.playw(elements.animate.arrange(RIGHT, buff=0.75))
        package1.move_to(pyproject[0]).shift(UP * 0.5)
        package2.move_to(uvlock[0]).shift(UP * 0.5)
        self.play(Circumscribe(pyproject, color=BLUE_D), FadeIn(package1))
        self.playw(Circumscribe(uvlock, color=YELLOW_C), FadeIn(package2))
        installed.next_to(venv, DOWN)
        self.playw(
            LaggedStart(
                Circumscribe(venv, color=GREEN_B),
                FadeIn(installed, shift=DOWN * 0.5),
                lag_ratio=0.5,
            )
        )
        venv.save_state()
        installed.save_state()
        self.play(
            venv.animate.set_color(PURE_RED), installed.animate.set_color(PURE_RED)
        )
        self.playw(Restore(venv), Restore(installed))
        github = (
            ImageMobject("githubmark.png")
            .scale(0.3)
            .next_to(pyproject, UP)
            .set_z_index(1)
        )
        self.play(FadeIn(github))
        venvs = VGroup(venv, installed)
        venvs.save_state()
        spec = VGroup(pyproject, uvlock, package1, package2)
        spec.save_state()
        self.play(
            spec
            .animate.move_to(github)
            .scale(0.1),
            venvs.animate.scale(0.5).next_to(github, DL, buff=0.02).shift(UP*0.3),
            rate_func=rate_functions.rush_into,
        )
        github.save_state()
        github.scale(1.2)
        venvs.set_color(PURE_RED)
        self.playw(Restore(venvs), Restore(github), rate_func=rate_functions.rush_from)

        self.playw(Restore(spec), venv.animate.set_opacity(0.3), FadeOut(installed))
        uvrun = Text("uv run main.py", font_size=32, font="Noto Mono", color=BLUE_B).next_to(pyproject, UP, buff=0.5)
        self.playw(FadeOut(github), FadeIn(uvrun))
        self.playw(FadeTransform(VGroup(package1, package2).copy(), installed), venv.animate.set_opacity(1))

        self.clear()
        uvremove = Text("uv remove", font_size=32, font="Noto Mono", color=RED_B)
        commands.add(uvrun)
        commands.add(uvremove)
        commands.arrange(DOWN, buff=0.75, aligned_edge=RIGHT).shift(LEFT * 2)
        self.playw(
            LaggedStart(
                *[FadeIn(command) for command in commands],
                lag_ratio=0.3,
            )
        )