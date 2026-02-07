from manim import *
from raenim import *
from random import seed, random
from PIL import Image

from kmeans import KMeans

seed(41)
np.random.seed(41)


def img_doo():
    img = Image.open("doo.jpg")
    aspect_ratio = img.width / img.height
    img = img.resize((int(360 * aspect_ratio), 360))
    return ImageMobject(img).scale(0.3)


def img_sanghai():
    img = Image.open("sanghai.jpg")
    aspect_ratio = img.width / img.height
    img = img.resize((int(360 * aspect_ratio), 360))
    return ImageMobject(img).scale(0.3)


def img_sim():
    img = Image.open("sim.png")
    aspect_ratio = img.width / img.height
    img = img.resize((int(360 * aspect_ratio), 360))
    return ImageMobject(img).scale(0.3)


def img_cat():
    img = Image.open("../vecatable.jpg")
    aspect_ratio = img.width / img.height
    img = img.resize((int(360 * aspect_ratio), 360))
    return ImageMobject(img).scale(0.3)


def img_simin():
    img = Image.open("simin.webp")
    aspect_ratio = img.width / img.height
    img = img.resize((int(360 * aspect_ratio), 360))
    return ImageMobject(img).scale(0.3)


def get_fill_img(val=200):
    img = np.zeros((200, 200, 3), dtype=np.uint8) + val
    return ImageMobject(img).scale(0.5)


def get_flower_img():
    img = Image.open("flower.png")
    aspect_ratio = img.width / img.height
    img = img.resize((int(9 * aspect_ratio), 9))
    dots = VGroup()
    for i in range(img.height):
        for j in range(img.width):
            r, g, b, _ = img.getpixel((j, i))
            if (r, g, b) != (255, 255, 255):
                dot = Square(
                    side_length=0.06,
                    stroke_width=0.0,
                    color=ManimColor((r / 255, g / 255, b / 255)),
                    fill_opacity=1.0,
                )
                dots.add(dot)
    dots.arrange_in_grid(img.height, img.width, buff=0.0)
    return dots


def get_embed(dim=5):
    return VGroup(
        *[
            Rectangle(
                width=0.3,
                height=0.15,
                color=GREY_B,
                stroke_width=2,
                fill_color=random_color(),
                fill_opacity=0.5,
            )
            for _ in range(dim)
        ]
    ).arrange(DOWN, buff=0.0)


class intro(Scene2D):
    def construct(self):
        # v1, v2, v3 - 0.09B, 1.1B, 7B
        scale = 1.5
        v1_scale = 0.09**0.5
        v2_scale = 1.1**0.5
        v3_scale = 7**0.5
        v1 = Rectangle(
            width=scale * v1_scale,
            height=scale * v1_scale,
            color=GREY_B,
            stroke_width=2,
        ).shift(LEFT * 2)
        v1t = Text("0.09B", font_size=24, font="Noto Sans", color=GREY_A).scale(0.6)
        v1n = Text("v1", font_size=24, font="Noto Sans", color=YELLOW_B)
        v2 = Rectangle(
            width=scale * v2_scale,
            height=scale * v2_scale,
            color=GREY_B,
            stroke_width=2,
        )
        v2t = Text("1.1B", font_size=24, font="Noto Sans", color=GREY_A)
        v2n = Text("v2", font_size=24, font="Noto Sans", color=YELLOW_B)
        v3 = Rectangle(
            width=scale * v3_scale,
            height=scale * v3_scale,
            color=GREY_B,
            stroke_width=2,
        ).shift(RIGHT * 3)
        v3t = Text("7B", font_size=24, font="Noto Sans", color=GREY_A).scale(1.3)
        v3n = Text("v3", font_size=24, font="Noto Sans", color=YELLOW_B)
        VGroup(v1, v2, v3).arrange(RIGHT, buff=1, aligned_edge=DOWN).shift(UP * 0.7)
        v1t.next_to(v1, UP, buff=0.1)
        v1n.next_to(v1, DOWN, buff=0.1)
        v2t.move_to(v2)
        v2n.next_to(v2, DOWN, buff=0.1)
        v3t.move_to(v3)
        v3n.next_to(v3, DOWN, buff=0.1)

        self.playw(FadeIn(v1, v1t, v1n), FadeIn(v2, v2t, v2n), FadeIn(v3, v3t, v3n))
        self.playw(
            RWiggle(VGroup(v2, v2t, v2n), amp=(0.06, 0.06, 0.06), run_time=5),
            RWiggle(VGroup(v3, v3t, v3n), amp=(0.06, 0.06, 0.06), run_time=5),
        )


class whydatacuration(Scene2D):
    def construct(self):
        line = DashedLine(
            LEFT * 7,
            RIGHT * 7,
            color=GREY_C,
            stroke_width=2,
            dashed_ratio=0.6,
            dash_length=0.1,
        ).shift(UP * 1.5)
        web = (
            Text("web", font="Noto Sans", font_size=48, color=GREY_B)
            .scale(0.5)
            .next_to(line, UP, buff=0.1)
            .to_edge(RIGHT, buff=0.2)
        )
        data = Rectangle(
            width=6,
            height=3,
            color=GREY_B,
            stroke_width=2,
        ).shift(DOWN * 0.7)
        datat = (
            Text("data", font="Noto Sans")
            .scale(0.5)
            .next_to(data, RIGHT, buff=0.05)
            .align_to(data, DOWN)
        )
        self.playw(FadeIn(line, data))

        self.play(FadeIn(web))
        self.playw(Flash(web.get_corner(UL), color=YELLOW_B))

        doos = Group(*[img_doo().set_opacity(0) for _ in range(5)])
        sangs = Group(*[img_sanghai().set_opacity(0) for _ in range(5)])
        sims = Group(*[img_sim().set_opacity(0) for _ in range(5)])
        cat = img_cat().set_opacity(0)
        imgs = Group(*doos, *sangs, *sims, cat)
        imgs.shuffle()
        imgs.arrange_in_grid(2, 8).next_to(line, UP)
        imgs_list = list(imgs)
        imgs.shuffle()
        self.playw(FadeIn(datat))
        for item in imgs:
            item.generate_target().set_opacity(1)
        targets = Group(*[item.target for item in imgs])
        targets.arrange_in_grid(2, 8, buff=0.05).scale(0.5).move_to(data)
        self.playwl(*[MoveToTarget(item) for item in imgs], lag_ratio=0.3, run_time=4)

        self.play(self.cf.animate.move_to(data).scale(0.8))

        scale_value = 1.2
        self.play(
            *[sang.animate.set_opacity(1).scale(scale_value) for sang in sangs],
            *[item.animate.set_opacity(0.3) for item in imgs if item not in sangs],
        )
        self.play(
            *[sim.animate.set_opacity(1).scale(scale_value) for sim in sims],
            *[
                item.animate.set_opacity(0.3)
                for item in imgs
                if item not in sims and item not in sangs
            ],
            *[sang.animate.scale(1 / scale_value).set_opacity(0.3) for sang in sangs],
        )
        self.playw(
            *[doo.animate.set_opacity(1).scale(scale_value) for doo in doos],
            *[
                item.animate.set_opacity(0.3)
                for item in imgs
                if item not in doos and item not in sangs
            ],
            *[sim.animate.scale(1 / scale_value).set_opacity(0.3) for sim in sims],
        )


class dedupandretrieval(Scene2D):
    def construct(self):
        sangs = Group(*[img_sanghai().set_opacity(1) for _ in range(3)])
        doos = Group(*[img_doo().set_opacity(1) for _ in range(3)])
        sims = Group(*[img_sim().set_opacity(1) for _ in range(3)])
        fills = Group(
            *[
                get_fill_img((1 - random() ** 1.5) * 255).set_opacity(1)
                for _ in range(3)
            ]
        )
        imgs = Group(*sangs, *doos, *sims, *fills)
        imgs.shuffle()
        imgs.arrange_in_grid(6, 2, buff=0.1).shift(UP * 0.7)
        self.playw(FadeIn(imgs))

        sang_embed = get_embed(dim=5)
        doo_embed = get_embed(dim=5)
        sim_embed = get_embed(dim=5)

        embeds = VGroup()
        embeds_sang = VGroup()
        embeds_doo = VGroup()
        embeds_sim = VGroup()
        fill_pairs = Group()
        for item in imgs:
            item.generate_target()
        targets = Group(*[item.target for item in imgs])
        targets.arrange_in_grid(6, 2, buff=(0.9, 0.1))
        for item in imgs:
            if item in sangs:
                e = sang_embed.copy()
                e.next_to(item.target, RIGHT, buff=0.1)
                embeds_sang.add(e)
            elif item in doos:
                e = doo_embed.copy()
                e.next_to(item.target, RIGHT, buff=0.1)
                embeds_doo.add(e)
            elif item in sims:
                e = sim_embed.copy()
                e.next_to(item.target, RIGHT, buff=0.1)
                embeds_sim.add(e)
            else:
                e = get_embed(dim=5)
                e.next_to(item.target, RIGHT, buff=0.1)
                fill_pairs.add(Group(item, e))
            embeds.add(e)
        self.play(*[MoveToTarget(item) for item in imgs])
        self.play(*[FadeIn(e) for e in embeds])

        embeds_doo.set_z_index(self.overlay.z_index + 1)
        self.play(FadeIn(self.overlay))
        self.playw(
            FadeOut(embeds_doo[1:], Group(*[item for item in imgs if item in doos])[1:])
        )
        self.play(FadeOut(self.overlay), run_time=0.5)
        embeds_doo[0].set_z_index(self.overlay.z_index - 1)
        embeds_sang.set_z_index(self.overlay.z_index + 1)
        self.play(FadeIn(self.overlay))
        self.play(
            FadeOut(
                embeds_sang[1:], Group(*[item for item in imgs if item in sangs])[1:]
            ),
            run_time=0.5,
        )
        self.play(FadeOut(self.overlay), run_time=0.5)
        embeds_sang[0].set_z_index(self.overlay.z_index - 1)
        embeds_sim.set_z_index(self.overlay.z_index + 1)
        self.play(FadeIn(self.overlay))
        self.play(
            FadeOut(
                embeds_sim[1:], Group(*[item for item in imgs if item in sims])[1:]
            ),
            run_time=0.5,
        )
        self.play(FadeOut(self.overlay), run_time=0.5)

        remain = Group(
            Group([item for item in imgs if item in sims][0], embeds_sim[0]),
            Group([item for item in imgs if item in doos][0], embeds_doo[0]),
            Group([item for item in imgs if item in sangs][0], embeds_sang[0]),
            *fill_pairs,
        )
        self.playw(
            remain.animate.arrange_in_grid(3, 2, buff=(1.0, 0.5))
            .move_to(ORIGIN)
            .shift(UP * 0.5)
        )

        simin = img_simin()
        simin_embed = get_embed(dim=5).next_to(simin, RIGHT, buff=0.1)
        simin = Group(simin, simin_embed)
        simin.to_edge(LEFT, buff=0.5)
        self.play(FadeIn(simin, shift=RIGHT * 1.5))

        lines = VGroup(
            *[
                DashedLine(
                    simin_embed[i].get_right(),
                    remain[i].get_left(),
                    color=YELLOW_B,
                    stroke_width=2,
                    dashed_ratio=0.6,
                    dash_length=0.05,
                )
                for i in range(3)
            ]
        )
        self.playw(*[Create(line) for line in lines], run_time=1)
        self.play(fill_pairs.animate.arrange(DOWN, buff=0.7).shift(RIGHT * 4))

        lines[0].add_updater(
            lambda m: m.put_start_and_end_on(
                simin_embed[0].get_right(), remain[0].get_left()
            )
        )
        lines[1].add_updater(
            lambda m: m.put_start_and_end_on(
                simin_embed[1].get_right(), remain[1].get_left()
            )
        )
        lines[2].add_updater(
            lambda m: m.put_start_and_end_on(
                simin_embed[2].get_right(), remain[2].get_left()
            )
        )
        self.playw(remain[:3].animate.arrange(DOWN, buff=0.7))


class clustersampling(Scene2D):
    def construct(self):
        scale_value = 0.35
        imgs1 = VGroup(
            *[
                Text(f"image_{i}", font="Noto Sans").scale(scale_value)
                for i in range(25)
            ]
        )
        imgs2 = VGroup(
            *[
                Text(f"image_{i}", font="Noto Sans").scale(scale_value)
                for i in range(25)
            ]
        )
        imgs1.shuffle()
        imgs2.shuffle()
        imgs1.arrange_in_grid(5, 5, buff=(0.3, 0.2))
        imgs2.arrange_in_grid(5, 5, buff=(0.3, 0.2))

        VGroup(imgs1, imgs2).arrange(RIGHT, buff=0.5)
        b1 = SurroundingRectangle(imgs1, color=GREY_C, buff=0.2, stroke_width=2)
        b2 = SurroundingRectangle(imgs2, color=GREY_C, buff=0.2, stroke_width=2)

        self.playw(FadeIn(imgs1, b1))
        nimgs1 = VGroup(*imgs1)
        nimgs1.shuffle()
        imgs1.save_state()
        self.playw(
            *[item.animate.scale(1.2).set_color(GREEN) for item in nimgs1[:4]],
            *[item.animate.set_opacity(0.3) for item in nimgs1[4:]],
        )

        self.play(FadeIn(imgs2, b2))
        nimgs2 = VGroup(*imgs2)
        nimgs2.shuffle()
        clustert = (
            VGroup(
                *[
                    Text(f"cluster_{i}", font="Noto Sans", color=YELLOW_B).scale(
                        scale_value * 1.2
                    )
                    for i in range(6)
                ]
            )
            .arrange_in_grid(2, 3, buff=(1, 3))
            .move_to(b2)
            .shift(UP * 1.5)
        )
        c0 = nimgs2[:4]
        c1 = nimgs2[4:6]
        c2 = nimgs2[6:13]
        c3 = nimgs2[13:18]
        c4 = nimgs2[18:22]
        c5 = nimgs2[22:25]
        c0.generate_target().arrange(DOWN, buff=0.15).next_to(
            clustert[0], DOWN, buff=0.3
        )
        c1.generate_target().arrange(DOWN, buff=0.15).next_to(
            clustert[1], DOWN, buff=0.3
        )
        c2.generate_target().arrange(DOWN, buff=0.15).next_to(
            clustert[2], DOWN, buff=0.3
        )
        c3.generate_target().arrange(DOWN, buff=0.15).next_to(
            clustert[3], DOWN, buff=0.3
        )
        c4.generate_target().arrange(DOWN, buff=0.15).next_to(
            clustert[4], DOWN, buff=0.3
        )
        c5.generate_target().arrange(DOWN, buff=0.15).next_to(
            clustert[5], DOWN, buff=0.3
        )
        # breakpoint()
        piui = SurroundingRectangle(
            VGroup(clustert, c3.target), color=YELLOW_B, buff=0.2, stroke_width=2
        )
        self.play(
            MoveToTarget(c0),
            b2.animate.become(piui),
            MoveToTarget(c1),
            MoveToTarget(c2),
            MoveToTarget(c3),
            MoveToTarget(c4),
            MoveToTarget(c5),
            FadeIn(clustert),
        )
        imgs2.save_state()
        clustert.save_state()
        self.play(
            VGroup(*[clustert[i] for i in [0, 2, 4, 5]]).animate.set_color(GREEN),
            VGroup(*[clustert[i] for i in [1, 3]]).animate.set_opacity(0.3),
            VGroup(*[item for item in nimgs2]).animate.set_opacity(0.3),
        )
        self.playw(
            VGroup(c0[0], c2[3], c4[1], c5[2]).animate.set_color(GREEN),
            VGroup(
                *[item for item in nimgs2 if item in [c0[0], c2[3], c4[1], c5[2]]]
            ).animate.set_opacity(1),
        )

        ol = self.overlay
        VGroup(b1, imgs1).set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol), Restore(imgs1))
        self.playwl(
            *[Indicate(item, scale_factor=1.1, color=YELLOW) for item in imgs1],
            lag_ratio=0.1,
        )
        self.play(FadeOut(ol), Restore(imgs2), Restore(clustert))
        VGroup(b1, imgs1).set_z_index(ol.z_index - 1)
        VGroup(b2, imgs2, clustert).set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))

        self.play(
            *[RWiggle(item, amp=(0.1, 0.1, 0.1)) for item in [c0, c1, c2, c3, c4, c5]],
            run_time=4,
        )

        self.playw(
            VGroup(*[clustert[i] for i in [0, 2, 4, 5]]).animate.set_color(GREEN),
            VGroup(*[clustert[i] for i in [1, 3]]).animate.set_opacity(0.3),
            VGroup(*[item for item in nimgs2]).animate.set_opacity(0.3),
        )


class hierarchicalclustering(Scene3D):
    def construct(self):
        rotate_under = 2.6
        plane = (
            NumberPlane(
                x_range=[-8, 8, 1],
                y_range=[-5, 5, 1],
                background_line_style={
                    "stroke_color": GREY_C,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3,
                },
            )
            .rotate(-PI / rotate_under, axis=RIGHT)
            .scale(0.7)
            .shift(DOWN * 1.5)
        )
        plane.x_axis.set_color(GREY_C).set_opacity(0.7)
        plane.y_axis.set_color(GREY_C).set_opacity(0.7)
        self.addw(plane)

        X = np.random.randn(500, 2) * 2
        dot_radius = 0.04
        dots = VGroup()
        for i in range(len(X)):
            dot = Dot(
                point=plane.c2p(X[i, 0], X[i, 1]),
                radius=dot_radius,
                color=WHITE,
                fill_opacity=1.0,
            ).rotate(-PI / rotate_under, axis=RIGHT)
            dots.add(dot)
        self.playw(FadeIn(dots))

        clusters = {0: {"indices": np.arange(len(X)), "color": WHITE}}
        color_palette = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, TEAL]
        color_idx = 0

        for level in range(1, 5):
            # 이번 레벨에서 분할할 클러스터 (항상 이전에 분할된 첫 번째 클러스터)
            cluster_to_split = max(clusters.keys())

            indices_to_split = clusters[cluster_to_split]["indices"]
            X_to_split = X[indices_to_split]

            kmeans = KMeans(
                n_clusters=3 if level < 4 else 2, max_iters=10, random_state=42
            )
            kmeans.fit(X_to_split)
            labels = kmeans.labels

            # 새 클러스터 색상 선택
            color1 = color_palette[color_idx % len(color_palette)]
            color2 = color_palette[(color_idx + 1) % len(color_palette)]
            color3 = color_palette[(color_idx + 2) % len(color_palette)]
            color_idx += 3

            indices1 = indices_to_split[labels == 0]
            indices2 = indices_to_split[labels == 1]
            indices3 = indices_to_split[labels == 2]

            # 클러스터 업데이트
            # breakpoint()
            new_cluster_id1 = max(clusters.keys()) + 1
            new_cluster_id2 = new_cluster_id1 + 1
            new_cluster_id3 = new_cluster_id2 + 1
            clusters[new_cluster_id1] = {"indices": indices1, "color": color1}
            clusters[new_cluster_id2] = {"indices": indices2, "color": color2}
            clusters[new_cluster_id3] = {"indices": indices3, "color": color3}

            # dots 색상 변경 (현재 분할된 클러스터에 속한 dots만 변경)
            dots.generate_target()
            for idx in indices_to_split:
                if idx in indices1:
                    color = color1
                elif idx in indices2:
                    color = color2
                elif idx in indices3:
                    color = color3

                dot_ = Dot(
                    point=plane.c2p(X[idx, 0], X[idx, 1]),
                    radius=dot_radius * (1 + 0.2 * level),
                    color=color,
                    fill_opacity=1.0,
                ).rotate(-PI / (rotate_under + level * 0.3), axis=RIGHT)
                if level == 1:
                    dots.target[idx].become(dot_)
                else:
                    dots.target[idx].become(dot_).shift(UP * level)
            for idx in range(len(X)):
                if idx not in indices_to_split:
                    dots.target[idx].set_opacity(0.2)
            self.playw(MoveToTarget(dots), run_time=2)


class gramanchoring(Scene2D):
    def construct(self):
        model = Rectangle(
            width=13.3,
            height=3,
            color=GREY_B,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=2,
        )
        modelt = (
            Text("Teacher model (≒200k)", font="Noto Sans", color=GREY_B)
            .scale(0.7)
            .move_to(model)
        )
        model = VGroup(model, modelt).shift(UP)
        img = get_flower_img().scale(2).next_to(model, DOWN, buff=0.5)
        self.addw(img, model)
        self.play(
            img.animate.scale(1 / 2)
            .arrange(RIGHT, buff=0.03)
            .next_to(model, DOWN, buff=0.5)
        )
        img_out = img.copy().next_to(model, UP, buff=0.5)
        for dot in img_out:
            dot.set_color(interpolate_color(dot.color, GREY_C, 0.6))

        self.playw(img.animate.become(img_out))
        ir = img_out.copy()
        self.play(FadeOut(model))
        self.play(
            ir.animate.rotate(-PI / 2).align_to(img_out, LEFT).shift(LEFT * 0.2),
            self.cf.animate.shift(LEFT + UP * 3),
        )

        eq = MathTex(r" X X^\top").scale(0.8).next_to(img.get_left(), UR, buff=0.3)
        eq2 = (
            MathTex(
                r"\mathcal{L}",
                r"_",
                r"{\text{Gram}}",
                r"=",
                r"\left\| X_S X_S^\top - X_G X_G^\top \right\|_F^2",
            )
            .scale(0.8)
            .next_to(eq, UP, buff=0.5)
            .align_to(eq, LEFT)
        )

        self.play(FadeIn(eq, shift=UR * 0.2))
        self.play(FadeIn(eq2, shift=UP * 0.2))
        self.playw(
            RWiggle(eq, amp=(0.07, 0.07, 0.07), run_time=3),
            RWiggle(eq2, amp=(0.07, 0.07, 0.07), run_time=3),
        )


class forTNIntegrated(Scene3D):
    def construct(self):
        xc = Circle(
            radius=0.5,
            color=GREY_B,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.9,
        )
        xt = MathTex("x").scale(0.75)
        x = VGroup(xc, xt).shift(DOWN * 3.5 + LEFT*4.3)

        x1c = Circle(
            radius=0.5,
            color=GREY_B,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.9,
        )
        x1t = MathTex("x_1").scale(0.75)
        x1 = VGroup(x1c, x1t).next_to(x, LEFT, buff=1.5).shift(UP)
        x2c = Circle(
            radius=0.5,
            color=GREY_B,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.9,
        )
        x2t = MathTex("x_2").scale(0.75)
        x2 = VGroup(x2c, x2t).next_to(x, RIGHT, buff=1.5).shift(UP)

        student_box = Rectangle(
            width=2.5,
            height=1.3,
            color=GREY_B,
            stroke_width=3,
            fill_color=GREY_E,
            fill_opacity=1,
        )
        student_text = (
            Tex("student", "\\,", "$\\mathrm{g}_{\\theta_s}$")
            .scale(0.75)
            .move_to(student_box)
        )
        student = VGroup(student_box, student_text).next_to(x1, UP, buff=0.5)
        teacher_box = Rectangle(
            width=2.5,
            height=1.3,
            color=GREY_B,
            stroke_width=3,
            fill_color=GREY_E,
            fill_opacity=1,
        )
        teacher_text = (
            Tex("teacher", "\\,", "$\\mathrm{g}_{\\theta_t}$")
            .scale(0.75)
            .move_to(teacher_box)
        )
        teacher = VGroup(teacher_box, teacher_text).next_to(x2, UP, buff=0.5)

        centering_box = Rectangle(
            width=2.5,
            height=0.75,
            color=GREY_C,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=3,
        )
        centering_text = Tex("centering").scale(0.6).move_to(centering_box)
        centering = VGroup(centering_box, centering_text).next_to(
            teacher, UP, buff=0.35
        )
        softmax_box = Rectangle(
            width=2.5,
            height=0.75,
            color=GREY_C,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=1
        )
        softmax_text = Tex("softmax").scale(0.6).move_to(softmax_box)
        softmax = VGroup(softmax_box, softmax_text).next_to(centering, UP, buff=0.35)
        softmax2_box = Rectangle(
            width=2.5,
            height=0.75,
            color=GREY_C,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=1
        )
        softmax2_text = Tex("softmax").scale(0.6).move_to(softmax2_box)
        softmax2 = (
            VGroup(softmax2_box, softmax2_text)
            .next_to(student, UP, buff=0.35)
            .align_to(softmax, UP)
        )

        p1c = Circle(
            radius=0.5,
            color=GREY_B,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.9,
        )
        p1t = MathTex("p_1").scale(0.75)
        p1 = VGroup(p1c, p1t).next_to(softmax2, UP, buff=0.7)
        p2c = Circle(
            radius=0.5,
            color=GREY_B,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.9,
        )
        p2t = MathTex("p_2").scale(0.75)
        p2 = VGroup(p2c, p2t).next_to(softmax, UP, buff=0.7)

        arrow1 = Arrow(
            x.get_left(),
            x1[0].point_at_angle(-PI / 4),
            buff=0.01,
            stroke_width=3,
            tip_length=0.15,
            color=GREY_B,
        )
        arrow2 = Arrow(
            x.get_right(),
            x2[0].point_at_angle(-3 * PI / 4),
            buff=0.01,
            stroke_width=3,
            tip_length=0.15,
            color=GREY_B,
        )
        arrow3 = Arrow(
            x1[0].get_top(),
            p1[0].get_bottom(),
            buff=0.01,
            stroke_width=3,
            tip_length=0.15,
            color=GREY_B,
        ).set_z_index(-1)
        arrow4 = Arrow(
            x2[0].get_top(),
            p2[0].get_bottom(),
            buff=0.01,
            stroke_width=3,
            tip_length=0.15,
            color=GREY_B,
        ).set_z_index(-1)
        stop_grad1 = Line(
            DOWN*0.1 + LEFT*0.5,
            UP*0.1 + RIGHT*0.5,
            color=GREY_B,
            stroke_width=3
        )
        stop_grad2 = Line(
            DOWN*0.1 + LEFT*0.5,
            UP*0.1 + RIGHT*0.5,
            color=GREY_B,
            stroke_width=3
        )
        stop_grad = VGroup(stop_grad1, stop_grad2).arrange(DOWN, buff=-0.3).next_to(softmax, UP, buff=0.17)
        sg = Text("sg", font="Noto Sans KR", color=GREY_B).scale(0.4).next_to(stop_grad, RIGHT, buff=0.1)
        ema_arr = Arrow(student.get_right(), teacher.get_left(), buff=0.5, stroke_width=3, tip_length=0.15, color=GREY_B)
        emat = Tex("ema", color=GREY_B).scale(0.7).next_to(ema_arr, UP, buff=0.1)
        ema = VGroup(ema_arr, emat)
        self.tilt_camera_horizontal(45, zoom=0.8)
        self.addw(
            x, x1, x2, student, teacher, centering, softmax, softmax2, p1, p2, arrow1, arrow2, arrow3, arrow4, stop_grad, sg, ema
        )