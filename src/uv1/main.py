from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class storage(Scene2D):
    def construct(self):
        homeuser = FolderIcon("/home/user/")
        self.addw(homeuser)
        prj1 = FolderIcon("prj1/")
        prj2 = FolderIcon("prj2/")
        prj3 = FolderIcon("prj3/")
        prjs = VGroup(prj1, prj2, prj3).shift(LEFT)
        prjs.arrange(DOWN, buff=0.5)

        homeuser.generate_target()
        homeuser.target.next_to(prjs, UP, buff=0.75).align_to(prjs, LEFT).shift(
            LEFT
        ).scale(1.2)
        self.play(
            MoveToTarget(homeuser),
        )
        self.playw(LaggedStartMap(FadeIn, prjs, lag_ratio=0.2), run_time=2)

        get_command = lambda: Text(
            "uv init", font_size=24, font="Noto Mono", color=BLUE
        )
        command1 = get_command().next_to(prj1, RIGHT, buff=0.5)
        command2 = get_command().next_to(prj2, RIGHT, buff=0.5)
        command3 = get_command().next_to(prj3, RIGHT, buff=0.5)
        commands = VGroup(command1, command2, command3)
        get_venv = lambda: FolderIcon(".venv/").scale(0.8)
        venv1 = get_venv().next_to(prj1, RIGHT, buff=0.5)
        venv2 = get_venv().next_to(prj2, RIGHT, buff=0.5)
        venv3 = get_venv().next_to(prj3, RIGHT, buff=0.5)
        venvs = VGroup(venv1, venv2, venv3)

        anims = SkewedAnimations(
            [FadeIn(command) for command in commands],
            [
                Transform(command, venv, replace_mobject_with_target_in_scene=True)
                for command, venv in zip(commands, venvs)
            ],
        )
        for anim in anims:
            self.playw(anim, wait=0.5)

        self.playw(
            LaggedStart(*[venv.text.animate.set_color(PURE_RED) for venv in venvs])
        )

        anaconda = (
            FolderIcon("~/anaconda3/envs/env")
            .scale(1.3)
            .next_to(venv3, DOWN, buff=0.75)
        )
        anaconda.text.save_state()
        anaconda.text.set_color(PURE_RED)

        self.playw(FadeIn(anaconda))

        self.playw(self.cf.animate.shift(DOWN * 2.5), Restore(anaconda.text))

        get_conda = lambda: Text("(env)", font_size=24, font="Noto Mono")
        conda1 = get_conda().next_to(prj1, RIGHT, buff=0.5)
        conda2 = get_conda().next_to(prj2, RIGHT, buff=0.5)
        conda3 = get_conda().next_to(prj3, RIGHT, buff=0.5)
        condas = VGroup(conda1, conda2, conda3)

        self.playw(venvs.animate.become(condas))
        line1 = DashedLine(
            anaconda.text[-2].get_top(), conda1.get_right(), color=GREY_D, buff=0.1
        )
        line2 = DashedLine(
            anaconda.text[-2].get_top(), conda2.get_right(), color=GREY_D, buff=0.1
        )
        line3 = DashedLine(
            anaconda.text[-2].get_top(), conda3.get_right(), color=GREY_D, buff=0.1
        )
        lines = VGroup(line1, line2, line3)
        self.playw(*[Create(line) for line in lines])


class review(Scene2D):
    def construct(self):
        uv = Text("uv", font_size=60, font="Noto Mono", color=BLUE)

        better = Text(">", font_size=48, font="Noto Mono").next_to(uv, RIGHT, buff=0.5)
        pipenv = Text("pipenv", font_size=48, font="Noto Mono", color=RED).next_to(
            better, RIGHT, buff=0.5
        )
        conda = Text("conda", font_size=48, font="Noto Mono", color=YELLOW_B).next_to(
            uv, RIGHT, buff=1
        )

        self.playw(FadeIn(uv))
        self.play(FadeIn(pipenv))
        self.playw(FadeIn(better))

        self.playw(FadeOut(pipenv, better))
        self.playw(FadeIn(conda))

        faster = Text("faster", font_size=32, font="Noto Mono", color=BLUE).next_to(
            uv, UP, buff=0.5
        )
        solid = Text("solid", font_size=32, font="Noto Mono", color=YELLOW_B).next_to(
            conda, UP, buff=0.5
        )
        self.playw(FadeIn(faster, shift=UP * 0.5))
        self.playw(FadeIn(solid, shift=UP * 0.5))


class preview(Scene2D):
    def construct(self):
        title1 = Text("uv core concepts", font_size=48).set_color_by_gradient(
            BLUE_B, BLUE_E
        )
        title2 = Text("uv commands", font_size=48).set_color_by_gradient(
            BLUE_B, BLUE_E
        )

        titles = VGroup(title1, title2).arrange(RIGHT, buff=1.5).shift(UP * 2)

        self.playw(FadeIn(title2))


        uvrun = Text("uv run", font_size=32, font="Noto Mono").set_color_by_gradient(
            YELLOW_B, YELLOW_D
        )
        python = Text("python", font_size=32, font="Noto Mono").set_color_by_gradient(
            YELLOW_B, YELLOW_D
        )
        run_commands = (
            VGroup(uvrun, python)
            .arrange(DOWN, buff=0.3)
            .next_to(title2, DOWN, buff=0.75)
            .shift(LEFT)
        )
        uvadd = Text("uv add", font_size=32, font="Noto Mono").set_color_by_gradient(
            YELLOW_B, YELLOW_D
        )
        uvpipinstall = Text(
            "uv pip install", font_size=32, font="Noto Mono"
        ).set_color_by_gradient(YELLOW_B, YELLOW_D)
        add_commands = (
            VGroup(uvadd, uvpipinstall)
            .arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            .next_to(run_commands, DOWN, buff=0.5)
            .align_to(run_commands, LEFT)
        )
        self.play(FadeIn(uvrun))

        self.play(FadeIn(uvadd))
        self.playw(FadeIn(uvpipinstall))
        self.playw(FadeIn(title1))


        venv = FolderIcon(".venv/").scale(0.8)
        pyprojecttoml = File("pyproject.toml").scale(0.8)
        uvlock = File("uv.lock").scale(0.8)
        cores = (
            VGroup(venv, pyprojecttoml, uvlock)
            .arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            .next_to(title1, DOWN, buff=0.75)
        )
        self.play(FadeIn(venv, shift=DOWN * 0.5))
        self.play(FadeIn(pyprojecttoml, shift=DOWN * 0.5))
        self.playw(FadeIn(uvlock, shift=DOWN * 0.5))

        self.playw(FadeIn(python))
        self.playw(Circumscribe(add_commands, color=RED))