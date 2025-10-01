from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        data = VGroup(*[File(size=0.25) for _ in range(45)]).arrange_in_grid(
            5, 9, buff=0.2
        )
        dot3 = Text("...", font_size=72).rotate(-PI / 4).next_to(data, DR)
        data.set_opacity(0)
        for i in range(3):
            for j in range(4):
                data[i * 9 + j].set_opacity(1)
                self.add(data[i * 9 + j])

        self.wait()

        self.play(data.animate.set_opacity(1))
        self.playw(FadeIn(dot3))

        folder = Folder(size=1).next_to(data, UP, buff=0.5)
        self.play(FadeIn(folder))
        self.play(
            *[item.animate.move_to(folder) for item in data],
            FadeOut(dot3, target_position=folder),
        )
        foldert = Text("data_folder", font=MONO_FONT, font_size=24).next_to(
            folder, DOWN
        )
        self.playw(FadeIn(foldert, shift=DOWN * 0.5))
        files = (
            Words("[fname for fname in data_folder]", font=MONO_FONT, font_size=32)
            .shift(DOWN * 0.5)
            .set_color_by_gradient(GREY_B, GREY_BROWN)
        )
        self.playw(*[FadeIn(item) for item in files.words])

        gen_box = DashedVMobject(
            SurroundingRect(stroke_width=2, color=GREY_B).surround(
                VGroup(folder, foldert)
            ),
            dashed_ratio=0.7,
            num_dashes=20,
        )
        gen_arrow = DashedVMobject(
            Arrow(
                gen_box.get_right(),
                gen_box.get_right() + RIGHT * 4.5,
                stroke_width=2,
                color=GREY_B,
                tip_length=0.2,
                buff=0,
            ),
            dashed_ratio=0.7,
            num_dashes=20,
        )
        generator = TextBox(
            "file_generator",
            text_kwargs={"font": MONO_FONT, "font_size": 24, "color": YELLOW},
            box_kwargs={
                "stroke_width": 2,
                "color": GREY_B,
                "fill_opacity": 1.0,
                "fill_color": BLACK,
            },
        ).move_to(gen_arrow)
        self.play(FadeIn(gen_box))
        self.playw(FadeIn(gen_arrow), FadeIn(generator))


class generator(Scene2D):
    def construct(self):
        half_line = DashedLine(
            UP * 6,
            DOWN * 6,
            dashed_ratio=0.7,
            dash_length=0.15,
            stroke_width=2,
            color=GREY_D,
        )

        listt = (
            Text("list", font=MONO_FONT, font_size=24)
            .move_to((half_line.get_center() + self.cf.get_right()) / 2)
            .shift(UP * 3)
        )
        gent = (
            Text("generator", font=MONO_FONT, font_size=24)
            .move_to((half_line.get_center() + self.cf.get_left()) / 2)
            .shift(UP * 3)
        )
        self.cf.save_state()
        self.cf.move_to(gent).scale(0.48)
        self.addw(half_line, listt, gent)
        self.playw(Restore(self.cf), run_time=2)

        folder = Folder(size=1).shift(UP * 2)
        foldert = (
            Text("data/", font=MONO_FONT, font_size=18, color=BLACK)
            .move_to(folder[0])
            .set_z_index(1)
        )
        self.playw(FadeIn(folder, foldert))
        data_list = Words(
            '[ "data/f1.npz", "data/f2.npz", "data/f3.npz", "data/f4.npz", "data/f5.npz", "data/f6.npz", ... ]',
            font=MONO_FONT,
            font_size=24,
        )
        data_list.words[1:-1].arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        data_list.words[0].next_to(data_list.words[1], LEFT)
        data_list.words[-1].next_to(data_list.words[-2], RIGHT)
        data_list.next_to(listt, DOWN, buff=2)
        self.playw(FadeIn(data_list))

        lbrace = Brace(data_list, LEFT, buff=0.1, color=GREY_B)
        self.playw(FadeIn(lbrace))
        self.playw(data_list.animate.set_color(PURE_RED))
        items = Tensor(6, shape="square")
        for i in range(6):
            items[i].move_to(data_list.words[i + 1]).align_to(
                data_list.words[i + 1], LEFT
            )
        self.playw(
            *[
                Transform(
                    data_list.words[i + 1],
                    items[i],
                    replace_mobject_with_target_in_scene=True,
                )
                for i in range(6)
            ]
        )

        self.playw(
            FadeOut(lbrace),
            VGroup(
                items, items, data_list[0], data_list.words[-2:]
            ).animate.set_opacity(0.2),
        )

        garr = Arrow(
            folder.get_bottom() + LEFT * 0.4,
            folder.get_bottom() + DL * 2 + LEFT,
            color=GREY_B,
            buff=0.1,
            stroke_width=3,
            tip_length=0.25,
        )
        self.playw(GrowArrow(garr))

        f1 = Text("data/f1.npz", font=MONO_FONT, font_size=24).move_to(
            garr.get_end() + DL * 0.2
        )
        f2 = Text("data/f2.npz", font=MONO_FONT, font_size=24).move_to(
            garr.get_end() + DL * 0.2
        )
        self.playw(FadeIn(f1, target_position=folder, scale=0.5), run_time=2)
        self.playw(
            f1.animate.shift(DOWN*0.5),
            FadeIn(f2, target_position=folder, scale=0.5),
            run_time=2,
        )
