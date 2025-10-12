from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        preprocess = Text("Preprocessing", font_size=48).set_color_by_gradient(
            GREEN_A, MINT
        )

        self.playw(LaggedStart(*[FadeIn(item, run_time=0.5) for item in preprocess]))
        self.playw(preprocess.animate.set_color(PURE_RED))

        self.playw(Rotate(preprocess, angle=2 * PI, run_time=3))

        pathlib = Text("Pathlib", font_size=36).set_color_by_gradient(GREEN_A, MINT)
        multiprocessing = Text("Multiprocessing", font_size=36).set_color_by_gradient(
            GREEN_A, MINT
        )
        contents = (
            VGroup(pathlib, multiprocessing)
            .arrange(RIGHT, buff=1.5)
            .next_to(preprocess, DOWN, buff=0.5)
        )
        self.play(FadeIn(pathlib))
        self.playw(FadeIn(multiprocessing))

        self.play(FadeOut(preprocess))
        self.play(contents.animate.arrange(RIGHT, buff=1.2))
        self.playw(contents.animate.scale(1.3), run_time=5)


class pathlibIntro(Scene2D):
    def construct(self):
        pathlib = Text("Pathlib", font_size=60).set_color_by_gradient(GREEN_A, MINT)
        ospath = (
            Text("os.path", font_size=48)
            .set_color_by_gradient(RED_B, RED_D)
            .next_to(self.cf, RIGHT, buff=5)
            .shift(UP)
        )
        self.playw(LaggedStart(*[FadeIn(item, run_time=0.5) for item in pathlib]))

        self.play(
            ospath.animate.rotate(10 * DEGREES).next_to(pathlib, UR, buff=0),
            rate_func=rush_into,
            run_time=2,
        )
        self.playw(
            ospath.animate.rotate(10 * DEGREES).next_to(self.cf, UP, buff=2),
            rate_func=rush_from,
        )
        fn_strings = ".cwd(), .home(), .exists(), .is_file(), .is_dir(), .iterdir(), .glob(), .rglob(), .open(), .read_text(), .write_text(), .read_bytes(), .write_bytes(), .rename(), .replace(), .mkdir(), .rmdir(), .unlink(), .resolve(), .with_suffix()"
        fns = fn_strings.split(",")
        fn_texts = (
            VGroup(
                *[
                    Text(
                        fn.strip(), font_size=32, font="Noto Mono"
                    ).set_color_by_gradient(RED_B, RED_D)
                    for fn in fns
                ]
            )
            .arrange(RIGHT, buff=1)
            .next_to(self.cf, RIGHT, buff=1)
            .shift(UP * 1.5)
        )
        self.playw(
            fn_texts.animate.next_to(self.cf, LEFT, buff=1).shift(UP * 1.5), run_time=8
        )


class preprocessPattern(Scene3D):
    def construct(self):
        pattern = Text("Preprocessing Pattern", font_size=60).set_color_by_gradient(
            GREEN_A, MINT
        )
        self.playw(LaggedStart(*[FadeIn(item, run_time=0.5) for item in pattern]))

        self.playw(pattern.animate.shift(LEFT * 13))
        pattern.set_opacity(0)
        self.tilt_camera_horizontal(45)

        scene1 = RoundedRectangle(corner_radius=0.2, width=16, height=9).scale(0.6)
        scene2 = (
            RoundedRectangle(corner_radius=0.2, width=16, height=9)
            .scale(0.6)
            .set_opacity(0.2)
            .set_fill(opacity=0)
            .next_to(scene1, RIGHT)
        )
        scene3 = (
            RoundedRectangle(corner_radius=0.2, width=16, height=9)
            .scale(0.6)
            .set_opacity(0.2)
            .set_fill(opacity=0)
            .next_to(scene2, RIGHT)
        )
        scenes = VGroup(scene1, scene2, scene3)
        self.playw(FadeIn(scene1, scene2, scene3))

        # about scene1
        folder = FolderIcon(text="data/").scale(0.7)
        folder_rect = Rectangle(width=4, height=3, color=YELLOW_B)
        folder.next_to(folder_rect, UP, buff=0.1).align_to(folder_rect, LEFT)
        folder = VGroup(folder, folder_rect).shift(RIGHT * 2.5)
        self.playw(FadeIn(folder))
        num_row, num_col = 5, 7
        files = (
            VGroup(*[FileIcon(size=0.3) for i in range(num_row) for j in range(num_col)])
            .arrange_in_grid(rows=num_row, cols=num_col, buff=0.2)
            .move_to(folder[1])
        )
        self.playw(FadeIn(files))

        samples = (
            VGroup(
                *[
                    Square(
                        side_length=0.35,
                        color=(c := random_color()),
                        fill_opacity=0.9,
                        stroke_width=2,
                    )
                    for i in range(num_row)
                    for j in range(num_col)
                ]
            )
            .arrange_in_grid(rows=num_row, cols=num_col, buff=0.2)
            .next_to(folder[1], LEFT, buff=0.5)
            .set_z_index(1)
        )

        transforms = []
        for f, s in zip(files, samples):
            tr = Transform(f.copy(), s, replace_mobject_with_target_in_scene=True)
            transforms.append(tr)
        self.playw(LaggedStart(*transforms, lag_ratio=0.1))

        shadow = samples.copy().set_opacity(0.1).set_z_index(-1)
        self.add(shadow)
        self.play(samples.animate.shift(OUT * 2.5).scale(1.2), FadeOut(folder, files))
        scenes.generate_target().move_to(ORIGIN)
        scenes.target[0].set_opacity(0.2).set_fill(opacity=0)
        scenes.target[1].set_opacity(1).set_fill(opacity=0)
        self.play(MoveToTarget(scenes))
        self.playw(samples.animate.shift(IN * 2.5).scale(1 / 1.2))
        self.remove(shadow)

        # about scene2

        fn_samples = (
            VGroup(
                *[
                    fn(item.generate_target()).arrange(RIGHT, buff=0.1)
                    for item in samples
                ]
            )
            .arrange_in_grid(rows=num_row, cols=num_col, buff=0.2)
            .move_to(samples)
            .shift(RIGHT * 1.8)
        )
        self.playw(
            *[FadeIn(VGroup(item[0], item[2])) for item in fn_samples],
            *[MoveToTarget(item) for item in samples],
        )
        fn_samples = VGroup(
            *[VGroup(fns[0], item, fns[2]) for fns, item in zip(fn_samples, samples)]
        )

        datas = VGroup(
            *[
                Pentagon()
                .move_to(fn_samples[i])
                .set_color(samples[i].get_color())
                .set_fill(opacity=0.9)
                .scale(0.5)
                for i in range(num_row * num_col)
            ]
        )
        trs = []
        for f, s in zip(fn_samples, datas):
            tr = Transform(f, s, replace_mobject_with_target_in_scene=True)
            trs.append(tr)
        self.play(*trs)
        self.playw(datas.animate.arrange_in_grid(rows=num_row, cols=num_col, buff=0.2))

        shadow = datas.copy().set_opacity(0.1).set_z_index(-1)
        self.add(shadow)
        self.play(datas.animate.shift(OUT * 2.5).scale(1.2))
        scenes.generate_target().align_to(scene2, RIGHT)
        scenes.target[1].set_opacity(0.2).set_fill(opacity=0)
        scenes.target[2].set_opacity(1).set_fill(opacity=0)
        self.play(
            MoveToTarget(scenes),
            datas.animate.shift(LEFT * 2),
            shadow.animate.shift(LEFT * 2),
        )

        self.play(datas.animate.shift(IN * 2.5).scale(1 / 1.2))
        self.remove(shadow)
        self.wait()

        # about scene3
        prep_folder = FolderIcon(text="preprocessed/").scale(0.7)
        prep_folder_rect = Rectangle(width=4, height=3, color=GREEN_B)
        prep_folder.next_to(prep_folder_rect, UP, buff=0.1).align_to(
            prep_folder_rect, LEFT
        )
        prep_folder = VGroup(prep_folder, prep_folder_rect).shift(RIGHT * 2.5)
        self.playw(FadeIn(prep_folder))

        prep_files = (
            VGroup(*[FileIcon(size=0.3) for i in range(num_row) for j in range(num_col)])
            .arrange_in_grid(rows=num_row, cols=num_col, buff=0.2)
            .move_to(prep_folder[1])
        )
        trs = []
        for f, s in zip(datas, prep_files):
            tr = Transform(f.copy(), s, replace_mobject_with_target_in_scene=True)
            trs.append(tr)
        self.playw(*trs, lag_ratio=0.1)

        self.playw(FadeOut(datas, prep_folder, prep_files))

        scenes.generate_target().align_to(scene3, LEFT)
        scenes.target[0].set_opacity(1).set_fill(opacity=0)
        scenes.target[2].set_opacity(0.2).set_fill(opacity=0)
        self.play(MoveToTarget(scenes))
        first = (
            Text("1st", font_size=28)
            .next_to(scene1, UP, buff=0.1)
            .align_to(scene1, LEFT)
        )
        self.play(FadeIn(first))
        self.play(FadeOut(first))

        self.move_camera_horizontally(0, zoom=1.5)

        self.playw(FadeIn(folder, files))

        code1 = (
            PythonCode("pathlib1.py", add_line_numbers=False)
            .scale(0.6)
            .next_to(folder, LEFT, buff=0.5)
        )
        code1.code[4:].set_opacity(0.2)
        self.playw(FadeIn(code1))
        hlin, hlout = code1.highlight(3, 'Path("data/")')
        self.playw(hlin)

        self.play(
            self.mouse.scale(0.7).move_to(files[0]).shift(UP * 10).animate.on(files[0]),
            hlout,
        )
        self.playw(self.mouse.animate.on(files[-1]))

        self.play(code1.text_slice(5, 'p.rglob("*")').animate.set_opacity(1))
        self.playw(Circumscribe(code1.text_slice(5, 'p.rglob("*")')))


class second(Scene3D):
    def construct(self):
        self.tilt_camera_horizontal(45)
        scene1 = (
            RoundedRectangle(corner_radius=0.2, width=16, height=9)
            .scale(0.6)
            .set_opacity(0.2)
            .set_fill(opacity=0)
        )
        scene2 = (
            RoundedRectangle(corner_radius=0.2, width=16, height=9)
            .scale(0.6)
            .set_opacity(1)
            .set_fill(opacity=0)
        )
        scene3 = (
            RoundedRectangle(corner_radius=0.2, width=16, height=9)
            .scale(0.6)
            .set_opacity(0.2)
            .set_fill(opacity=0)
        )
        second = Text("2nd", font_size=28, color=GREY_B).next_to(scene2, UP, buff=0.1)
        second.align_to(scene2, LEFT)
        scenes = VGroup(scene1, scene2, scene3).arrange(RIGHT)
        self.addw(scenes)
        self.play(FadeIn(second))
        self.play(FadeOut(second))

        samples = (
            VGroup(
                *[
                    Square(
                        side_length=0.35,
                        color=(c := random_color()),
                        fill_opacity=0.9,
                        stroke_width=2,
                    )
                    for i in range(5)
                    for j in range(7)
                ]
            )
            .arrange_in_grid(rows=5, cols=7, buff=0.2)
            .move_to(scene2)
            .set_z_index(1)
        )
        self.play(FadeIn(samples))
        samples.generate_target()
        fn_samples = (
            VGroup(
                *[
                    fn(item.generate_target()).arrange(RIGHT, buff=0.1)
                    for item in samples
                ]
            )
            .arrange_in_grid(rows=5, cols=7, buff=0.2)
            .move_to(samples)
        )
        self.play(
            *[FadeIn(VGroup(item[0], item[2])) for item in fn_samples],
            *[MoveToTarget(item) for item in samples],
        )
        fn_samples = VGroup(
            *[VGroup(fns[0], item, fns[2]) for fns, item in zip(fn_samples, samples)]
        )

        data = VGroup(
            *[
                Pentagon()
                .move_to(fn_samples[i])
                .set_color(samples[i].get_color())
                .set_fill(opacity=0.9)
                .scale(0.5)
                for i in range(5 * 7)
            ]
        )
        trs = []
        for f, s in zip(fn_samples, data):
            tr = Transform(f, s, replace_mobject_with_target_in_scene=True)
            trs.append(tr)
        self.play(*trs)
        self.playw(
            data.animate.arrange_in_grid(rows=5, cols=7, buff=0.2),
        )

        shadow = data.copy().set_opacity(0.1).set_z_index(-1)
        self.add(shadow)
        self.playw(data.animate.shift(OUT * 2.5).scale(1.2))
        scenes.generate_target().align_to(scene2, RIGHT).set_opacity(0.2).set_fill(opacity=0)
        scenes.target[-1].set_opacity(1).set_fill(opacity=0)
        self.play(MoveToTarget(scenes))
        self.play(data.animate.shift(IN * 2.5).scale(1 / 1.2))
        self.remove(shadow)
        self.move_camera_horizontally(0, zoom=1.5)
        self.playw(data.animate.scale(0.7).shift(LEFT * 2))

        folder = FolderIcon(text="preprocessed/").scale(0.7)
        folder_rect = Rectangle(width=4, height=3, color=GREEN_B)
        folder.next_to(folder_rect, UP, buff=0.1).align_to(folder_rect, LEFT)
        folder = VGroup(folder, folder_rect).shift(RIGHT * 2)
        path = Text(
            'Path("preprocessed/").mkdir(\n    parents=True, exist_ok=True\n)',
            font="Noto Mono",
            font_size=16,
            line_spacing=1,
        ).next_to(data, RIGHT, buff=0.25)
        self.playw(
            LaggedStart(*[FadeIn(item, run_time=0.5) for item in path], lag_ratio=0.1)
        )

        self.playw(
            Transform(
                path[6:19], folder[0]._text, replace_mobject_with_target_in_scene=True
            ),
            Transform(
                VGroup(path[:6], path[19:]),
                VGroup(folder[0]._icon, folder[1]),
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.wait(10)
        file = (
            File("preprocessed/file.txt")
            .scale(0.5)
            .move_to(folder[1])
            .set_opacity(0.3)
        )
        self.play(FadeIn(file))
        self.playw(Circumscribe(file, buff=0.05))

        pathexist = Text(
            "path.exists()", font_size=16, font="Noto Mono", color=GREY_B
        ).next_to(file, UP)
        self.playw(FadeIn(pathexist))

        self.wait(3)

        pathunlink = Text(
            "file.unlink()", font_size=16, font="Noto Mono", color=GREY_B
        ).move_to(pathexist)
        self.playw(
            file.animate.set_opacity(1),
            Transform(
                pathexist[:5], pathunlink[:5], replace_mobject_with_target_in_scene=True
            ),
            Transform(pathexist[5:], pathunlink[5:], replace_mobject_with_target_in_scene=True),
        )

        self.playw(FadeOut(file))

        total = VGroup(scenes, data, folder, pathunlink)
        total.generate_target()
        total.target.align_to(scene2, LEFT)
        total.target[0][-1].set_opacity(0.2).set_fill(opacity=0)

        folder_data = FolderIcon(text="data/").scale(0.7)
        folder_data_rect = Rectangle(width=4, height=3, color=YELLOW_B, stroke_width=3)
        folder_data.next_to(folder_data_rect, UP, buff=0.1).align_to(
            folder_data_rect, LEFT
        )
        folder_data = VGroup(folder_data, folder_data_rect).move_to(total.target[0][0]).shift(RIGHT*2.5)
        data_files = (
            VGroup(*[FileIcon(size=0.3) for i in range(5) for j in range(7)])
            .arrange_in_grid(rows=5, cols=7, buff=0.2)
            .move_to(folder_data[1])
        )

        self.move_camera_horizontally(0, zoom=0.45, added_anims=[MoveToTarget(total), FadeIn(folder_data, data_files)])

        self.play(scene1.animate.set_opacity(1).set_fill(opacity=0))
        self.playw(scene1.animate.set_opacity(0.2).set_fill(opacity=0))

        self.play(scene3.animate.set_opacity(1).set_fill(opacity=0))
        self.playw(scene3.animate.set_opacity(0.2).set_fill(opacity=0))

        self.playw(scene2.animate.set_opacity(1).set_fill(opacity=0))
        self.playw(self.cf.animate.shift(IN*14), run_time=4)


def fn(item):
    str_prefix = "fn("
    prefix = Text(str_prefix, font_size=20, font="Noto Mono", color=GREY_B)
    str_suffix = ")"
    suffix = Text(str_suffix, font_size=20, font="Noto Mono", color=GREY_B)
    return VGroup(prefix, item, suffix)


def Pentagon():
    pent = RegularPolygon(n=5, color=YELLOW_B, fill_opacity=0.2).scale(0.5)
    pent.set_fill(YELLOW_B, opacity=0.2)
    pent.set_stroke(width=2)
    return pent
