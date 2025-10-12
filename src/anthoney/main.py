from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        honey = ImageMobject("honey.png").scale(0.3)
        self.addw(honey)
        honeys = Group(honey, *[honey.copy() for _ in range(24)])
        self.playw(honeys.animate.arrange_in_grid(5, 5, buff=0.15).scale(0.8))
        self.playw(Indicate(honeys[11], color=PURE_RED))
        honeys.generate_target().shuffle()
        self.playw(MoveToTarget(honeys))
        ant = ImageMobject("ant.png").scale(0.8).shift(3 * LEFT)
        self.playwl(honeys.animate.shift(2 * RIGHT), FadeIn(ant, shift=RIGHT))
        ants = Group(ant, *[ant.copy() for _ in range(4)])
        self.playw(ants.animate.arrange(DOWN, buff=0.2).move_to(ant))

        ants_ = ants[:-2]
        self.playwl(
            FadeOut(ants_, honeys), self.cf.animate.move_to(ants[-2:]).scale(0.5)
        )

        ant_die = ImageMobject("ant_die.png").scale(0.8).move_to(ants[-1])
        honey_true = ImageMobject("honey.png").scale(0.25).next_to(ants[-2], LEFT)
        honey_fake = (
            ImageMobject("honey.png")
            .scale(0.25)
            .set_color(PURE_RED)
            .next_to(ants[-1], LEFT)
        )
        self.playw(FadeIn(honey_true, shift=RIGHT))
        self.play(honey_true.animate.move_to(ants[-2]).scale(0.3))
        self.playw(FadeOut(honey_true))

        self.playw(FadeIn(honey_fake, shift=RIGHT))
        self.play(honey_fake.animate.move_to(ants[-1]).scale(0.3))
        ants[-1].save_state()
        self.play(
            Transform(ants[-1], ant_die),
            FadeOut(honey_fake),
            run_time=0.5,
        )
        self.playw(Rotate(ants[-1], angle=PI), rate_func=rush_from, run_time=0.5)

        self.playw(Restore(ants[-1]), run_time=0.5)

        honeys1 = (
            Group(*[honey.copy() for _ in range(4)])
            .arrange(DOWN, buff=0.1)
            .scale(0.5)
            .next_to(ants[-2], LEFT)
        )
        honey1 = honey.copy().scale(0.5).move_to(honeys1)
        honeys2 = (
            Group(*[honey.copy() for _ in range(4)])
            .arrange(DOWN, buff=0.1)
            .scale(0.5)
            .next_to(ants[-1], LEFT)
        )
        honey2 = honey.copy().scale(0.5).move_to(honeys2)
        honeys2[1].set_color(PURE_RED)
        self.play(FadeIn(honeys1, shift=RIGHT))
        self.playw(
            *[item.animate.move_to(honey1).set_opacity(0) for item in honeys1],
            FadeIn(honey1),
        )
        self.play(honey1.animate.move_to(ants[-2]).scale(0.6))
        self.playw(FadeOut(honey1))

        ant_die = ImageMobject("ant_die.png").scale(0.8).move_to(ants[-1])
        self.play(FadeIn(honeys2, shift=RIGHT))
        self.playw(
            *[item.animate.move_to(honey2).set_opacity(0) for item in honeys2],
            FadeIn(honey2),
        )
        self.play(honey2.animate.move_to(ants[-1]).scale(0.6))
        self.playw(FadeOut(honey2))
        self.play(Transform(ants[-1], ant_die), run_time=0.5)
        self.playw(Rotate(ants[-1], angle=PI), rate_func=rush_from, run_time=0.5)


class problem(Scene2D):
    def construct(self):
        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange_in_grid(5, 5, buff=0.15).scale(0.8).shift(LEFT * 2)

        ants = (
            Group(*[ImageMobject("ant.png").scale(0.8) for _ in range(5)])
            .arrange(DOWN, buff=0.2)
            .shift(RIGHT * 2)
        )

        self.addw(honeys, ants)

        self.play(Indicate(honeys[12], color=PURE_RED))
        honeys.generate_target().shuffle()
        self.playw(MoveToTarget(honeys))
        self.playwl(*[Wiggle(a, scale_value=1.3) for a in ants], lag_ratio=0.1)

        clock_circle = Circle(radius=0.3, stroke_width=2, color=YELLOW_A)
        clock_hour = Line(ORIGIN, UP * 0.15, stroke_width=2)
        clock_minute = Line(ORIGIN, UP * 0.25, stroke_width=2)
        clock = VGroup(clock_circle, clock_hour, clock_minute).scale(2).shift(RIGHT * 4)
        hour_fn = lambda s: Text(
            f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}", font_size=24
        ).next_to(clock, DOWN)
        s_val = ValueTracker(0)
        hour = always_redraw(lambda: hour_fn(int(s_val.get_value())))
        self.play(FadeIn(clock, hour, shift=RIGHT))
        self.playw(
            s_val.animate.set_value(3600),
            Rotate(clock_minute, angle=-2 * PI, about_point=clock_circle.get_center()),
            Rotate(clock_hour, angle=-PI / 6, about_point=clock_circle.get_center()),
            run_time=5.9,
            rate_func=linear,
        )


class naive(Scene2D):
    def construct(self):
        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange_in_grid(5, 5, buff=0.15).scale(0.8).shift(LEFT * 2)

        ants = (
            Group(*[ImageMobject("ant.png").scale(0.8) for _ in range(5)])
            .arrange(DOWN, buff=0.2)
            .shift(RIGHT * 2)
        )

        self.addw(honeys, ants)

        rows = Group()
        for row in range(5):
            rows.add(honeys[row * 5 : (row + 1) * 5])
        self.playwl(
            *[
                AnimationGroup(
                    *[item.animate.move_to(row[-1]).set_opacity(0) for item in row[:-1]]
                )
                for row in rows
            ],
            lag_ratio=0.2,
        )

        honeys_ = Group(*[honeys[i] for i in range(4, 25, 5)]).set_z_index(1)
        self.play(*[honeys_[i].animate.move_to(ants[i]).scale(0.5) for i in range(5)])
        self.playw(FadeOut(honeys_))
        ant_die = ImageMobject("ant_die.png").scale(0.8).move_to(ants[2])
        self.play(Transform(ants[2], ant_die), run_time=0.5)
        self.playw(Rotate(ants[2], angle=PI), rate_func=rush_from, run_time=0.5)

        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange_in_grid(5, 5, buff=0.15).scale(0.8).shift(LEFT * 2)
        self.playw(FadeIn(honeys[10:15]))
        self.playw(
            honeys[10:15].animate.arrange(DOWN, buff=0.15).move_to(honeys[14]),
            FadeOut(ants[2]),
        )

        self.play(
            honeys[10].animate.move_to(ants[0]).scale(0.5),
            honeys[11].animate.move_to(ants[1]).scale(0.5),
            honeys[13].animate.move_to(ants[3]).scale(0.5),
            honeys[14].animate.move_to(ants[4]).scale(0.5),
        )
        self.playw(FadeOut(Group(honeys[10], honeys[11], honeys[13], honeys[14])))

        self.wait(5)
        self.playw(FadeOut(honeys[12], ants[0], ants[1], ants[3], ants[4]))
        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange_in_grid(5, 5, buff=0.15).scale(0.8).shift(LEFT * 2)
        ants = (
            Group(*[ImageMobject("ant.png").scale(0.8) for _ in range(5)])
            .arrange(DOWN, buff=0.2)
            .shift(RIGHT * 2)
        )
        self.playw(FadeIn(honeys, ants))


class solution(Scene2D):
    def construct(self):
        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange_in_grid(5, 5, buff=0.15).scale(0.8).shift(LEFT * 2)

        ants = (
            Group(*[ImageMobject("ant.png").scale(0.8) for _ in range(5)])
            .arrange(DOWN, buff=0.2)
            .shift(RIGHT * 2)
        )

        self.addw(honeys, ants, wait=2)

        ants.generate_target().arrange(RIGHT, buff=0.2).shift(DOWN * 2)
        honeys.generate_target().next_to(ants.target, UP, buff=0.5)
        self.playw(MoveToTarget(ants), MoveToTarget(honeys))
        anims, integers = [], []
        for i in range(5):
            integers.append(
                Integer(0, num_decimal_places=0).scale(0.8).move_to(ants[i])
            )
            anims.append(
                FadeTransform(
                    ants[i],
                    integers[i],
                )
            )
        self.playw(*anims)
        self.playw(*[FadeTransform(integers[i], ants[i]) for i in range(5)])

        self.play(
            honeys.animate.arrange(RIGHT, buff=0.1)
            .scale(0.7)
            .next_to(ants, UP, buff=2.5)
        )
        indices = VGroup(
            *[
                Integer(i, font_size=28, color=YELLOW_B).next_to(
                    honeys[i - 1], UP, buff=0.15
                )
                for i in range(1, 25 + 1)
            ]
        )
        self.playw(FadeIn(indices, shift=UP * 0.5))

        self.playw(Group(indices, honeys, ants).animate.shift(UP))

        labels = VGroup(
            *[
                Text(chr(65 + i), font_size=24).next_to(ants[4 - i], DOWN, buff=0.1)
                for i in range(5)
            ]
        )
        self.playwl(
            *[FadeIn(label, shift=DOWN * 0.5) for label in labels], lag_ratio=0.3
        )

        honeys.generate_target().arrange(RIGHT, buff=0.5).move_to(honeys)
        indices.generate_target()
        for i, item in enumerate(indices.target):
            item.next_to(honeys.target[i], UP, buff=0.15)
        self.playw(
            MoveToTarget(honeys), MoveToTarget(indices), self.cf.animate.scale(1.7)
        )
        binidx = lambda x: bin(x)[2:].zfill(5)
        bin_indices = VGroup(
            *[
                Text(binidx(i), font_size=20).next_to(honeys[i - 1], DOWN, buff=0.1)
                for i in range(1, 26)
            ]
        )
        self.playw(FadeIn(bin_indices, shift=DOWN * 0.5))

        items = Group()
        for i in range(25):
            item = Group(honeys[i], indices[i], bin_indices[i])
            items.add(item)

        As = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-1] == "1"]).copy()
        for item in As:
            item[-1][-1].set_color(PURE_RED)
        self.playw(As.animate.shift(DOWN * 1.5))
        self.play(*[item.animate.move_to(ants[-1]).scale(0.5) for item in As])
        self.playw(FadeOut(As))

        Bs = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-2] == "1"]).copy()
        for item in Bs:
            item[-1][-2].set_color(PURE_RED)
        self.playw(Bs.animate.shift(DOWN * 1.5))
        self.play(*[item.animate.move_to(ants[-2]).scale(0.5) for item in Bs])
        self.playw(FadeOut(Bs))

        Cs = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-3] == "1"]).copy()
        for item in Cs:
            item[-1][-3].set_color(PURE_RED)
        self.playw(Cs.animate.shift(DOWN * 1.5))
        self.play(*[item.animate.move_to(ants[-3]).scale(0.5) for item in Cs])
        self.playw(FadeOut(Cs))

        Ds = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-4] == "1"]).copy()
        for item in Ds:
            item[-1][-4].set_color(PURE_RED)
        self.playw(Ds.animate.shift(DOWN * 1.5))
        self.play(*[item.animate.move_to(ants[-4]).scale(0.5) for item in Ds])
        self.playw(FadeOut(Ds))

        Es = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-5] == "1"]).copy()
        for item in Es:
            item[-1][-5].set_color(PURE_RED)
        self.playw(Es.animate.shift(DOWN * 1.5))
        self.play(*[item.animate.move_to(ants[-5]).scale(0.5) for item in Es])
        self.playw(FadeOut(Es))

        As = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-1] == "1"]).copy()
        for item in As:
            item[-1][-1].set_color(PURE_RED)
        self.play(As.animate.shift(DOWN * 1.3))
        ants_buff = 4.5
        items_buff = 3.5
        self.playw(
            As.animate.arrange(RIGHT, buff=0.3),
            self.cf.animate.scale(0.7),
            ants.animate.shift(DOWN * ants_buff),
            labels.animate.shift(DOWN * ants_buff),
            items.animate.shift(UP * items_buff),
        )
        self.playw(
            ants.animate.shift(UP * ants_buff),
            labels.animate.shift(UP * ants_buff),
            items.animate.shift(DOWN * items_buff),
            self.cf.animate.scale(1 / 0.7),
            FadeOut(As),
        )

        Bs = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-2] == "1"]).copy()
        for item in Bs:
            item[-1][-2].set_color(PURE_RED)
        self.play(Bs.animate.shift(DOWN * 1.3))
        self.playw(
            Bs.animate.arrange(RIGHT, buff=0.3),
            self.cf.animate.scale(0.7),
            ants.animate.shift(DOWN * ants_buff),
            labels.animate.shift(DOWN * ants_buff),
            items.animate.shift(UP * items_buff),
        )
        self.playw(
            ants.animate.shift(UP * ants_buff),
            labels.animate.shift(UP * ants_buff),
            items.animate.shift(DOWN * items_buff),
            self.cf.animate.scale(1 / 0.7),
            FadeOut(Bs),
        )

        Cs = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-3] == "1"]).copy()
        for item in Cs:
            item[-1][-3].set_color(PURE_RED)
        self.play(Cs.animate.shift(DOWN * 1.3))
        self.playw(
            Cs.animate.arrange(RIGHT, buff=0.3),
            self.cf.animate.scale(0.7),
            ants.animate.shift(DOWN * ants_buff),
            labels.animate.shift(DOWN * ants_buff),
            items.animate.shift(UP * items_buff),
        )
        self.playw(
            ants.animate.shift(UP * ants_buff),
            labels.animate.shift(UP * ants_buff),
            items.animate.shift(DOWN * items_buff),
            self.cf.animate.scale(1 / 0.7),
            FadeOut(Cs),
        )

        clock_circle = Circle(radius=0.3, stroke_width=2, color=YELLOW_A)
        clock_hour = Line(ORIGIN, UP * 0.15, stroke_width=2)
        clock_minute = Line(ORIGIN, UP * 0.25, stroke_width=2)
        clock = (
            VGroup(clock_circle, clock_hour, clock_minute)
            .scale(2)
            .next_to(ants, RIGHT, buff=2)
        )
        s_val = ValueTracker(0)
        hour_fn = lambda s: Text(
            f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}", font_size=24
        ).next_to(clock, DOWN)
        hour = always_redraw(lambda: hour_fn(int(s_val.get_value())))
        self.play(FadeIn(clock, hour, shift=RIGHT))
        self.play(
            s_val.animate.set_value(3600),
            Rotate(clock_minute, angle=-2 * PI, about_point=clock_circle.get_center()),
            Rotate(clock_hour, angle=-PI / 6, about_point=clock_circle.get_center()),
            run_time=2.9,
            rate_func=linear,
        )

        ants_die = Group(
            *[
                ImageMobject("ant_die.png").scale(0.8).move_to(ant)
                for ant in [ants[1], ants[4]]
            ]
        )
        self.play(self.cf.animate.move_to(ants).scale(0.35), FadeOut(clock))
        self.play(
            Transform(ants[1], ants_die[0]),
            Transform(ants[4], ants_die[1]),
            run_time=0.5,
        )
        self.playw(
            Rotate(ants[1], angle=PI),
            Rotate(ants[4], angle=PI),
            rate_func=rush_from,
            run_time=0.5,
        )

        binary_list = [0, 1, 0, 0, 1]
        binary = VGroup(
            *[
                Text(str(b), font_size=32, font=MONO_FONT).next_to(ants[i], UP)
                for i, b in enumerate(binary_list)
            ]
        )
        self.playw(FadeIn(binary, shift=UP * 0.5))


class honey1(Scene2D):
    def construct(self):
        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange(RIGHT, buff=0.4).scale(0.5).shift(UP * 1.5)
        indices = VGroup(
            *[
                Integer(i, font_size=28, color=YELLOW_B).next_to(
                    honeys[i - 1], UP, buff=0.15
                )
                for i in range(1, 25 + 1)
            ]
        )
        binidx = lambda x: bin(x)[2:].zfill(5)
        bin_indices = VGroup(
            *[
                Text(binidx(i), font_size=16).next_to(honeys[i - 1], DOWN, buff=0.1)
                for i in range(1, 26)
            ]
        )

        items = Group()
        for i in range(25):
            item = Group(honeys[i], indices[i], bin_indices[i])
            items.add(item)
        ants = (
            Group(*[ImageMobject("ant.png").scale(0.8) for _ in range(5)])
            .arrange(RIGHT, buff=0.2)
            .shift(DOWN * 1.5)
        )
        labels = VGroup(
            *[
                Text(chr(65 + i), font_size=24).next_to(ants[4 - i], DOWN, buff=0.1)
                for i in range(5)
            ]
        )
        self.cf.scale(1.1)
        self.addw(items, ants, labels)
        self.playw(Indicate(items[0], color=PURE_RED))

        fake = items[0].copy()
        self.play(fake.animate.next_to(ants, UP, buff=0.5).scale(1.3))
        self.play(fake[-1].animate.next_to(fake[0], RIGHT))
        self.playw(fake[-1].animate.scale(1.5).align_to(fake[-1], LEFT))

        ant_die = ImageMobject("ant_die.png").scale(0.8).move_to(ants[-1])
        self.play(Transform(ants[-1], ant_die), run_time=0.5)
        self.playw(Rotate(ants[-1], angle=PI), rate_func=rush_from, run_time=0.5)


class honey18(Scene2D):
    def construct(self):
        honeys = Group(*[ImageMobject("honey.png").scale(0.3) for _ in range(25)])
        honeys.arrange(RIGHT, buff=0.4).scale(0.5).shift(UP * 1.5)
        indices = VGroup(
            *[
                Integer(i, font_size=28, color=YELLOW_B).next_to(
                    honeys[i - 1], UP, buff=0.15
                )
                for i in range(1, 25 + 1)
            ]
        )
        binidx = lambda x: bin(x)[2:].zfill(5)
        bin_indices = VGroup(
            *[
                Text(binidx(i), font_size=16).next_to(honeys[i - 1], DOWN, buff=0.1)
                for i in range(1, 26)
            ]
        )

        items = Group()
        for i in range(25):
            item = Group(honeys[i], indices[i], bin_indices[i])
            items.add(item)
        ants = (
            Group(*[ImageMobject("ant.png").scale(0.8) for _ in range(5)])
            .arrange(RIGHT, buff=0.2)
            .shift(DOWN * 1.5)
        )
        labels = VGroup(
            *[
                Text(chr(65 + i), font_size=24).next_to(ants[4 - i], DOWN, buff=0.1)
                for i in range(5)
            ]
        )
        self.cf.scale(1.1)
        self.addw(items, ants, labels, wait=2)

        ants_die = Group(
            *[
                ImageMobject("ant_die.png").scale(0.8).move_to(ant)
                for ant in [ants[0], ants[3]]
            ]
        )
        self.play(
            Transform(ants[0], ants_die[0]),
            Transform(ants[3], ants_die[1]),
            run_time=0.5,
        )
        self.playw(
            Rotate(ants[0], angle=PI),
            Rotate(ants[3], angle=PI),
            rate_func=rush_from,
            run_time=0.5,
        )
        self.playw_return(Group(ants[1], ants[2], ants[4]).animate.shift(UP * 0.5))

        self.play(
            self.cf.animate.shift(UP * 3.5).scale(1.1).align_to(self.cf, RIGHT),
            Group(ants, labels).animate.shift(DOWN),
        )
        abcde = Words("A B C D E", font_size=36)
        abcde.words.arrange(DOWN, buff=0.75).next_to(honeys, LEFT, buff=0.5).shift(
            UP * 3.5
        )
        self.playw(FadeIn(abcde, shift=RIGHT))

        Es = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-5] == "1"]).copy()
        for item in Es:
            item[-1][-5].set_color(PURE_RED)
        self.play(Es.animate.next_to(abcde.words[-1], RIGHT).align_to(Es, RIGHT))

        Bs = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-2] == "1"]).copy()
        for item in Bs:
            item[-1][-2].set_color(PURE_RED)
        self.play(Bs.animate.next_to(abcde.words[1], RIGHT).align_to(Bs, RIGHT))

        intersection_be = Group(
            *[Bs[i] for i in [8, 9, 10, 11]],
            *[Es[i] for i in [2, 3, 6, 7]],
        ).copy()
        self.add(intersection_be)
        self.playw(FadeOut(Bs, Es))

        Ds = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-4] == "1"]).copy()
        for item in Ds:
            item[-1][-4].set_color(PURE_RED)
        Cs = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-3] == "1"]).copy()
        for item in Cs:
            item[-1][-3].set_color(PURE_RED)
        As = Group(*[items[i - 1] for i in range(1, 26) if binidx(i)[-1] == "1"]).copy()
        for item in As:
            item[-1][-1].set_color(PURE_RED)
        self.playwl(
            Ds.animate.next_to(abcde.words[3], RIGHT).align_to(Ds, RIGHT),
            Cs.animate.next_to(abcde.words[2], RIGHT).align_to(Cs, RIGHT),
            As.animate.next_to(abcde.words[0], RIGHT).align_to(As, RIGHT),
            lag_ratio=0.2,
        )
        self.playw(Group(Ds, Cs, As).animate.set_color(PURE_GREEN))

        h18 = Group(intersection_be[0], intersection_be[4])
        intersection_be_remove = Group(
            *[item for i, item in enumerate(intersection_be) if i not in [0, 4]]
        )
        self.add(h18)
        self.play(FadeOut(intersection_be_remove, As, Cs, Ds, shift=UP))
        self.playw(Group(items[17], h18[0][0], h18[1][0]).animate.set_color(PURE_RED))

        self.playw(self.cf.animate.move_to(h18).scale(0.75), FadeOut(items, shift=DOWN))


class outro(Scene2D):
    def construct(self):
        eq = MathTex(
            "2",
            "^",
            r"{",
            r"N_{",
            r"\text{ants}",
            r"}",
            r"}",
            " ",
            r"\geq",
            " ",
            r"N_{",
            r"\text{honeys}",
            r"}",
        ).scale(1.5)
        eq[4].set_color(YELLOW)
        eq[11].set_color(YELLOW)
        ants_idx = 4
        honeys_idx = 11
        ant = ImageMobject("ant.png").scale(0.4).next_to(eq[ants_idx], UP, buff=0.1)
        honey = (
            ImageMobject("honey.png").scale(0.15).next_to(eq[honeys_idx], UP, buff=0.1)
        )
        self.playw(FadeIn(eq[:7], ant))
        self.playw(FadeIn(eq[-3:], honey))
        self.playw(FadeIn(eq[7:10]))

        eq2 = MathTex(
            "2",
            "^",
            r"{",
            "5",
            r"}",
            " ",
            r"\geq",
            " ",
            r"25",
        ).scale(1.5)
        eq2[3].set_color(YELLOW)
        eq2[-1].set_color(YELLOW)

        transform_idx = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            [0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 8, 8, 8],
        ]

        self.playw(
            *[ReplacementTransform(eq[i], eq2[j]) for i, j in zip(*transform_idx)],
            ant.animate.next_to(eq2[3], UP, buff=0.1),
            honey.animate.next_to(eq2[-1], UP, buff=0.1),
        )

        self.playwl(
            Flash(eq2[3], color=YELLOW), Flash(eq2[-1], color=YELLOW), lag_ratio=0.5
        )

        self.playw(self.cf.animate.shift(DOWN))

        eq3 = MathTex(r"5", r"\times", r"5", "=", "25").scale(1.5)
        five_ = eq2[3].copy()
        fivefive_ = eq2[-1].copy()
        self.play(
            VGroup(five_, fivefive_).animate.arrange(RIGHT, buff=1).shift(DOWN * 2)
        )
        eq3.move_to(VGroup(five_, fivefive_))
        self.playw(
            Transform(five_, eq3[0], replace_mobject_with_target_in_scene=True),
            Transform(fivefive_, eq3[-1], replace_mobject_with_target_in_scene=True),
            FadeIn(eq3[1:-1])
        )
        eq4 = MathTex(r"5", r"^", r"2", "=", "25").scale(1.5).move_to(eq3)
        transform_idx = [
            [0, 1, 2, 3, 4],
            [0, 2, 2, 3, 4],
        ]
        self.playw(
            *[ReplacementTransform(eq3[i], eq4[j]) for i, j in zip(*transform_idx)]
        )

        self.playw(eq4.animate.set_opacity(0.0), self.cf.animate.shift(UP))
        eq2_ = MathTex(
            "2",
            "^",
            r"{",
            "5",
            r"}",
            " ",
            r"=",
            " ",
            r"32",
        ).scale(1.5).move_to(eq2)
        eq2_[3].set_color(YELLOW)
        eq2_[-1].set_color(YELLOW)
        transform_idx = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
        ]
        eq2.save_state()
        self.playw(
            *[ReplacementTransform(eq2[i], eq2_[j]) for i, j in zip(*transform_idx)]
        )

