from manim import *
from manimdef import DefaultManimClass


class EncoderInst(DefaultManimClass):
    def sceneA(self):
        squares = VGroup(*[Square(side_length=0.7) for _ in range(10)]).arrange(
            RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.6
        )
        nums = VGroup(
            *[
                Text(f"{i}", font="Consolas", font_size=24).next_to(squares[i], UP)
                for i in range(10)
            ]
        )
        self.playw(
            LaggedStart(
                *[FadeIn(squares[i], nums[i]) for i in range(10)], lag_ratio=0.1
            )
        )
        pressed_int = 3
        self.playw(squares[pressed_int].animate.set_fill(color=GREY, opacity=1.0))
        self.playw(
            squares[pressed_int].animate.set_fill(color=GREY, opacity=1.0),
            squares[pressed_int * 2].animate.set_fill(color=GREY, opacity=1.0),
        )
        self.playw(
            squares[pressed_int].animate.set_fill(color=PURE_RED),
            squares[pressed_int * 2].animate.set_fill(color=PURE_RED),
        )
        self.playw(
            squares[pressed_int].animate.set_fill(color=GREY),
            squares[pressed_int * 2].animate.set_fill(opacity=0.0),
        )

        pressed = VGroup(
            *[
                Text(
                    f"{1 if i == pressed_int else 0}",
                    font="Consolas",
                    font_size=24,
                    color=YELLOW,
                ).next_to(squares[i], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
                for i in range(10)
            ]
        )
        self.playw(
            LaggedStart(
                *[FadeIn(pressed[i], shift=DOWN) for i in range(10)], lag_ratio=0.1
            ),
            self.camera.frame.animate.shift(DOWN),
        )

        self.playw(
            FadeIn(
                (
                    pressed_bin := Text(
                        f"{bin(pressed_int)[2:].zfill(4)}",
                        font_size=36,
                        font="Consolas",
                        color=PURE_GREEN,
                    ).next_to(nums[pressed_int], UP)
                ),
                target_position=nums[pressed_int],
                scale=0.5,
            )
        )
        squares.set_fill(BLACK)
        squares[pressed_int].set_fill(GREY)
        pressed.save_state()
        self.play(
            pressed.animate.arrange(
                RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.6
            ).next_to(squares, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2),
            pressed_bin.animate.move_to(ORIGIN).next_to(
                pressed, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 4
            ),
            nums.animate.set_opacity(0.3),
            squares.animate.set_opacity(0.3),
        )
        self.playw(
            GrowArrow(encoder := Arrow(pressed.get_center(), pressed_bin.get_center()))
        )
        self.wait(3)

        self.playw(
            Restore(pressed),
            nums.animate.set_opacity(1.0),
            squares.animate.set_opacity(1.0),
            FadeOut(encoder),
        )
        self.playw(
            GrowArrow(
                decoder := Arrow(
                    pressed_bin.get_center(),
                    pressed[pressed_int].get_center(),
                    buff=MED_LARGE_BUFF,
                    stroke_width=3,
                )
            ),
        )

        for i in range(10):
            encoded = Text(
                f"{bin(i)[2:].zfill(4)}",
                color=PURE_GREEN,
                font="Consolas",
                font_size=36,
            ).move_to(pressed_bin)
            squares_list = [squares[j] for j in range(10)]
            fill_square = squares_list.pop(i)
            squares_none = VGroup(*squares_list)
            self.play(
                Transform(pressed_bin, encoded),
                GrowArrow(
                    arr := Arrow(
                        pressed_bin.get_center() if i else encoded.get_center(),
                        squares[i].get_center(),
                        stroke_width=3,
                        color=YELLOW,
                        buff=MED_LARGE_BUFF,
                    )
                ),
                pressed.animate.set_opacity(0.0),
                FadeOut(pre_arr if i else decoder),
                fill_square.animate.set_fill(GREY, opacity=1.0),
                squares_none.animate.set_fill(GREY, opacity=0.0),
            )
            if i == 0 or i == 8:
                self.wait(1)
            pre_arr = arr
        self.playw(FadeOut(pre_arr))

        pressed_decoded = VGroup(
            *[
                Text(
                    f"{1 if i == 9 else 0}",
                    font="Consolas",
                    font_size=24,
                    color=YELLOW,
                ).next_to(squares[i], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
                for i in range(10)
            ]
        )
        self.playw(FadeIn(pressed_decoded))
        squares[:-1].set_fill(BLACK)
        self.playw(
            pressed_decoded.animate.arrange(
                RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 0.6
            ).move_to(pressed_decoded),
            GrowArrow(Arrow(pressed_bin, pressed_decoded.get_center(), stroke_width=3)),
            nums.animate.set_opacity(0.3),
            squares.animate.set_opacity(0.3),
        )

    def construct(self):
        self.sceneA()  # ~ 원본 정보로 복원하는 것을 디코딩이라고 합니다


class EncoderImage(DefaultManimClass):
    def construct(self):
        img = ImageMobject("2424cat2.png")

        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["box"])
        img.scale(36)
        self.playw(FadeIn(img))
        self.camera.frame.save_state()
        self.playw(self.camera.frame.animate.shift(UP * 3).shift(LEFT * 3).scale(0.3))
        self.wait()
        self.playw(Restore(self.camera.frame), img.animate.scale(0.4))

        random_vector_list = [[0.36], [-0.11], ["..."], [0.3], [0.42]]
        random_vector = Matrix(random_vector_list).next_to(
            img, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 5
        )
        self.playw(
            FadeIn(random_vector),
            self.camera.frame.animate.move_to(random_vector),
        )

        encoder = Arrow(img.get_right(), random_vector.get_left(), color=PURE_GREEN)
        decoder = Arrow(random_vector.get_left(), img.get_right(), color=PURE_GREEN)
        self.playw(GrowArrow(encoder), self.camera.frame.animate.move_to(encoder))
        self.playw(FadeOut(encoder))
        self.playw(GrowArrow(decoder))


class EncoderAssumption1(DefaultManimClass):
    def sceneA(self):
        squares = VGroup(*[Square(side_length=0.7) for _ in range(10)]).arrange(
            RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.6
        )
        nums = VGroup(
            *[
                Text(f"{i}", font="Consolas", font_size=24).next_to(squares[i], UP)
                for i in range(10)
            ]
        )
        self.playw(
            LaggedStart(
                *[FadeIn(squares[i], nums[i]) for i in range(10)], lag_ratio=0.1
            )
        )
        pressed_int = 3
        self.playw(squares[pressed_int].animate.set_fill(color=GREY, opacity=1.0))
        self.playw(
            squares[pressed_int].animate.set_fill(color=GREY, opacity=1.0),
            squares[pressed_int * 2].animate.set_fill(color=GREY, opacity=1.0),
        )
        self.playw(
            squares[pressed_int].animate.set_fill(color=PURE_RED),
            squares[pressed_int * 2].animate.set_fill(color=PURE_RED),
        )
        self.playw(squares[9].animate.set_fill(color=PURE_RED, opacity=1.0))
        self.playw(
            *[
                squares[i].animate.set_fill(color=PURE_RED, opacity=1.0)
                for i in [0, 1, 2, 4, 5, 7, 8]
            ]
        )

    def construct(self):
        self.sceneA()


class EncoderImageAssumption1(DefaultManimClass):
    def construct(self):
        img = ImageMobject("2424cat2.png")

        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["box"])
        img.scale(24)
        self.playw(FadeIn(img))

        random_vector_list = [[0.36], [-0.11], ["..."], [0.3], [0.42]]
        random_vector = Matrix(random_vector_list).next_to(
            img, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 5
        )
        encoder = Arrow(img.get_right(), random_vector.get_left(), color=PURE_GREEN)
        self.playw(
            FadeIn(random_vector),
            self.camera.frame.animate.move_to(encoder),
            GrowArrow(encoder),
        )
        self.playw(encoder.animate.set_color(PURE_RED))


class EncoderAssumption2(DefaultManimClass):
    def sceneA(self):
        squares = VGroup(*[Square(side_length=0.7) for _ in range(10)]).arrange(
            RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.6
        )
        nums = VGroup(
            *[
                Text(f"{i}", font="Consolas", font_size=24).next_to(squares[i], UP)
                for i in range(10)
            ]
        )
        self.playw(
            LaggedStart(
                *[FadeIn(squares[i], nums[i]) for i in range(10)], lag_ratio=0.1
            )
        )

        encoded = VGroup(
            *[
                Text(
                    bin(i)[2:].zfill(4), font="Consolas", font_size=24, color=PURE_GREEN
                ).next_to(nums[i], UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 3)
                for i in range(10)
            ]
        )
        self.playw(LaggedStart(*[FadeIn(encoded[i], shift=UP) for i in range(10)]))
        encoded[0].generate_target().move_to(encoded[4])
        encoded[4].generate_target().move_to(encoded[0])
        self.playw(
            LaggedStart(
                MoveToTarget(
                    encoded[0], path_func=utils.paths.path_along_arc(-TAU * 1 / 3)
                ),
                MoveToTarget(
                    encoded[4], path_func=utils.paths.path_along_arc(TAU * 3 / 7)
                ),
            )
        )
        encoded[1].generate_target().move_to(encoded[3])
        encoded[3].generate_target().move_to(encoded[1])
        self.playw(
            LaggedStart(
                MoveToTarget(
                    encoded[1], path_func=utils.paths.path_along_arc(-TAU * 1 / 3)
                ),
                MoveToTarget(
                    encoded[3], path_func=utils.paths.path_along_arc(-TAU * 1 / 4)
                ),
            )
        )
        new_order = [4, 3, 2, 1, 0, 5, 6, 7, 8, 9]
        new_encoded_list = [16, 24, 12, 9, 28, 31, 2, 17, 8, 7]
        new_encoded = VGroup(
            *[
                Text(
                    bin(num)[2:].zfill(5), color=YELLOW, font_size=19, font="Consolas"
                ).move_to(encoded[new_order[i]])
                for i, num in enumerate(new_encoded_list)
            ]
        )

        for i, o in enumerate(new_order[:3]):
            self.playw(Transform(encoded[o], new_encoded[i]))

        self.playw(
            LaggedStart(
                *[
                    Transform(encoded[o], new_encoded[i])
                    for i, o in enumerate(new_order[3:], 3)
                ],
                lag_ratio=0.4,
            )
        )

    def construct(self):
        self.sceneA()
