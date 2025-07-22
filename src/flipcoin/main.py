from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(42)


def coin(color=RED):
    c = Circle(radius=0.2, color=color, fill_opacity=1)
    return c


class intro(Scene2D):
    def construct(self):
        n_coins = 100
        coins = (
            VGroup(*[coin(color=BLUE_D if i < 10 else RED_D) for i in range(n_coins)])
            .arrange_in_grid(n_rows=n_coins // 10, n_cols=10, buff=0.2)
            .shift(UP * 0.5)
        )

        self.playw(LaggedStart(*[FadeIn(c) for c in coins], lag_ratio=0.05))
        blues = coins[:10]
        reds = coins[10:]
        self.playw(*[Indicate(c, color=PURE_BLUE) for c in blues])
        self.playw(*[Indicate(c, color=PURE_RED) for c in reds])
        shuffled = [item for item in coins]
        shuffled.sort(key=lambda x: np.random.random())
        shuffled = VGroup(*shuffled)

        self.playw(
            shuffled.animate.arrange_in_grid(n_rows=n_coins // 10, n_cols=10, buff=0.2)
        )
        g1_indices = np.random.choice(range(n_coins), size=10, replace=False)
        g1 = VGroup(*[shuffled[i] for i in g1_indices])
        g2 = VGroup(*[shuffled[i] for i in range(n_coins) if i not in g1_indices])
        g1_colors = [g1[i].get_color() for i in range(len(g1))]
        g2_colors = [g2[i].get_color() for i in range(len(g2))]

        self.playw(*[item.animate.set_color(GREY_C) for item in shuffled])

        self.playw(
            g1.animate.arrange(DOWN, buff=0.2).shift(LEFT * 4 + UP * 0.5),
            g2.animate.shift(RIGHT * 2),
        )

        g1.save_state()
        self.play(*[g1[i].animate.set_color(g1_colors[i]) for i in range(len(g1))])
        self.playw(Restore(g1))

        self.playw(Circumscribe(g1))
        self.playw(Circumscribe(g2))

        # curious

        self.playw_return(shuffled.animate.set_color(GREY_E))
        self.play(self.cf.animate.scale(1.5).align_to(self.cf, UP))

        num_bluel = (
            VGroup(
                Text("num(", font_size=36, font=MONO_FONT),
                coin(color=BLUE_D),
                Text("in left)", font_size=36, font=MONO_FONT),
            )
            .arrange(RIGHT, buff=0.3)
            .next_to(g1, DOWN, buff=1)
        )

        num_bluer = (
            VGroup(
                Text("num(", font_size=36, font=MONO_FONT),
                coin(color=BLUE_D),
                Text("in right)", font_size=36, font=MONO_FONT),
            )
            .arrange(RIGHT, buff=0.3)
            .next_to(g2, DOWN, buff=1)
        )

        self.play(FadeIn(num_bluel))
        self.playw(FadeIn(num_bluer))
        eq = Text("=", font_size=36, font=MONO_FONT).move_to(
            VGroup(num_bluel[-1][-1], num_bluer[0][0])
        )
        self.playw(FadeIn(eq))

        self.playw(Circumscribe(VGroup(g1, g2)))
        q = Text("?", font_size=48, font=MONO_FONT).next_to(g1, RIGHT, buff=1.3)
        self.playw(FadeIn(q))

        random_indices = np.random.choice(range(n_coins), size=20, replace=False)
        self.playw(
            LaggedStart(
                *[shuffled[i].animate.rotate(PI, UP) for i in random_indices],
                lag_ratio=0.1,
            )
        )

        self.mouse.scale(1.7).next_to(self.cf, UP).align_to(g1, LEFT)
        self.playw(self.mouse.animate.on(g1[-2]))
        self.playw(
            self.mouse.animate.rotate(PI / 3)
            .next_to(self.cf, LEFT, buff=2)
            .shift(UP * 3),
            rate_func=rush_from,
        )
        self.play(Indicate(num_bluel, color=BLUE_D))
        self.play(Indicate(num_bluer, color=BLUE_D))
        self.playw(Circumscribe(VGroup(num_bluel, num_bluer, eq)), wait=4)

        g1.save_state()
        g2.save_state()
        self.playw(*[g1[i].animate.set_color(BLUE_D) for i in [1]])
        self.playw(*[g1[i].animate.set_color(BLUE_D) for i in [1, 2, 5, 6, 7]])
        cond = Text("if num(BLUE) in left == ", font_size=36, font=MONO_FONT).next_to(
            shuffled, DOWN, buff=1.5
        )
        cond[6:10].set_color(BLUE_D)
        one = Text("1", font_size=36, font=MONO_FONT).next_to(cond, RIGHT, buff=0.3)
        five = Text("5", font_size=36, font=MONO_FONT).next_to(cond, RIGHT, buff=0.3)
        self.playw(FadeTransform(VGroup(num_bluel, num_bluer, eq), VGroup(cond, one)))
        self.playw(Transform(one, five), Circumscribe(one))

        self.playw(*[g1[i].animate.set_color(GREY_C) for i in range(len(g1))])

        self.playw(
            LaggedStart(
                *[g1[i].animate.rotate(PI, UP) for i in [5, 6, 7]], lag_ratio=0.1
            )
        )

        #

        self.playw(
            LaggedStart(
                *[g1[i].animate.rotate(PI, UP) for i in range(len(g1))], lag_ratio=0.1
            )
        )
        self.playw(FadeTransform(VGroup(cond, one), num_bluel))
        eqx = Text("= x", font_size=36, font=MONO_FONT).next_to(
            num_bluel, RIGHT, buff=0.3
        )
        self.playw(FadeIn(eqx))
        num_bluer.shift(RIGHT)
        self.playw(FadeIn(num_bluer))
        eqx2 = Text("= 10 - x", font_size=36, font=MONO_FONT).next_to(
            num_bluer, RIGHT, buff=0.3
        )
        eqx2c = eqx2.copy()
        self.playw(FadeIn(eqx2))
        self.playw(
            VGroup(eqx[-1], eqx2[-4:])
            .animate.arrange(RIGHT, buff=2)
            .next_to(VGroup(num_bluel, num_bluer), DOWN, buff=1)
        )
        noteq = Text("≠", font_size=48, font=MONO_FONT, color=RED).move_to(
            VGroup(eqx[-1], eqx2[-4]).get_center()
        )
        self.playw(FadeIn(noteq))

        num_redl = (
            VGroup(
                Text("num(", font_size=36, font=MONO_FONT),
                coin(color=RED_D),
                Text("in left)", font_size=36, font=MONO_FONT),
            )
            .arrange(RIGHT, buff=0.3)
            .move_to(num_bluel)
        )
        eqx3 = Text("= 10 - x", font_size=36, font=MONO_FONT).next_to(
            num_redl, RIGHT, buff=0.3
        )
        self.playw(
            Transform(num_bluel, num_redl, replace_mobject_with_target_in_scene=True),
            Circumscribe(num_bluel[1]),
            FadeIn(eqx3),
            FadeOut(eqx, eqx2, noteq),
            FadeOut(num_bluer, shift=RIGHT),
        )
        self.playw(Circumscribe(num_redl[1]))

        self.playw(
            LaggedStart(
                *[g1[i].animate.rotate(PI, UP) for i in range(len(g1))], lag_ratio=0.1
            )
        )
        self.playw(
            num_redl[1].animate.rotate(PI, UP).set_color(BLUE_D),
            Circumscribe(num_redl[1]),
        )
        self.play(
            VGroup(num_redl, eqx3).animate.shift(LEFT*2),
            FadeIn(num_bluer, eqx2c)
        )
        self.playw(Circumscribe(VGroup(num_redl, eqx3)))
        self.playw(Circumscribe(VGroup(num_bluer, eqx2c)))
        self.playw(FadeOut(eqx2c, eqx3))
        eqfinal = Text("=", font_size=48, font=MONO_FONT).next_to(num_redl, RIGHT, buff=2)
        self.playw(FadeIn(eqfinal))
