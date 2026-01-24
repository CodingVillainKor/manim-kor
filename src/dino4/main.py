from manim import *
from raenim import *
from random import random, seed
from PIL import Image
from torchvision.datasets import MNIST, CIFAR10

seed(41)
np.random.seed(41)

cat_path = "../vecatable.jpg"
mnist = MNIST(root="../", train=True, download=False)
cifar10 = CIFAR10(root="../", train=True, download=False)


def patchify(img_array, h, w):
    """
    img_array를 h x w 크기의 패치들로 분할
    img_array: (H, W, C) 형태의 numpy array
    h, w: 각 패치의 높이와 너비
    returns: list of patches [(h, w, C), ...]
    """
    H, W, C = img_array.shape
    n_h = H // h  # 세로 방향 패치 개수
    n_w = W // w  # 가로 방향 패치 개수

    patches = []
    for i in range(n_h):
        for j in range(n_w):
            patch = img_array[i * h : (i + 1) * h, j * w : (j + 1) * w, :]
            patches.append(patch)

    return patches


class intro(Scene2D):
    def construct(self):
        # 1. cat 이미지를 np.array로 읽기
        cat_img = Image.open(cat_path)
        cat_array = np.array(cat_img)

        H, W, C = cat_array.shape
        cat_img_resized = cat_img.resize((W // 8, H // 8), Image.LANCZOS)
        cat_array = np.array(cat_img_resized)

        patch_h, patch_w = 8, 8
        patches = patchify(cat_array, patch_h, patch_w)
        scale_factor = 3
        patch_mobjects = [ImageMobject(patch).scale(scale_factor) for patch in patches]

        H, W = cat_array.shape[:2]
        n_h = H // patch_h
        n_w = W // patch_w

        patch_group = Group(*patch_mobjects)
        patch_group.arrange_in_grid(rows=n_h, cols=n_w, buff=0.0)

        self.playw(FadeIn(patch_group))

        crop1_h_patches = 9
        crop1_w_patches = 9
        crop2_h_patches = 5
        crop2_w_patches = 7

        crop1_start_row = 1
        crop1_start_col = 1
        crop1_indices = []
        for i in range(crop1_start_row, crop1_start_row + crop1_h_patches):
            for j in range(crop1_start_col, crop1_start_col + crop1_w_patches):
                idx = i * n_w + j
                crop1_indices.append(idx)

        crop2_start_row = 3
        crop2_start_col = 4
        crop2_indices = []
        for i in range(crop2_start_row, crop2_start_row + crop2_h_patches):
            for j in range(crop2_start_col, crop2_start_col + crop2_w_patches):
                idx = i * n_w + j
                crop2_indices.append(idx)

        crop1_patches = [patch_mobjects[i] for i in crop1_indices]
        crop1_rect = SurroundingRectangle(
            Group(*crop1_patches), color=YELLOW, buff=0, stroke_width=2
        ).set_z_index(1)

        crop2_patches = [patch_mobjects[i] for i in crop2_indices]
        crop2_rect = SurroundingRectangle(
            Group(*crop2_patches), color=BLUE, buff=0, stroke_width=2
        ).set_z_index(1)

        self.play(FadeIn(crop1_rect, scale=1.1))

        crop1_copies = [
            ImageMobject(patches[i]).scale(scale_factor) for i in crop1_indices
        ]
        crop1_group = Group(*crop1_copies)
        crop1_group.arrange_in_grid(
            rows=crop1_h_patches, cols=crop1_w_patches, buff=0.0
        )
        crop1_group.move_to(Group(*crop1_patches).get_center())

        self.playw(
            crop1_group.animate.arrange_in_grid(
                rows=crop1_h_patches, cols=crop1_w_patches, buff=0.05
            ).shift(LEFT * 4)
        )

        self.play(FadeIn(crop2_rect, scale=1.1))
        crop2_copies = [
            ImageMobject(patches[i]).scale(scale_factor) for i in crop2_indices
        ]
        crop2_group = Group(*crop2_copies)
        crop2_group.arrange_in_grid(
            rows=crop2_h_patches, cols=crop2_w_patches, buff=0.0
        )
        crop2_group.move_to(Group(*crop2_patches).get_center())

        self.playw(
            crop2_group.animate.arrange_in_grid(
                rows=crop2_h_patches, cols=crop2_w_patches, buff=0.05
            ).shift(RIGHT * 4)
        )

        gvt = Words("Global view", font_size=24, font="Noto Sans KR").next_to(
            crop1_group, DOWN, buff=0.5
        )
        lvt = (
            Words("Local view", font_size=24, font="Noto Sans KR")
            .next_to(crop2_group, DOWN, buff=0.5)
            .align_to(gvt, DOWN)
        )
        gvt.words.set_color_by_gradient(YELLOW_B, YELLOW_A)
        lvt.words.set_color_by_gradient(BLUE_B, BLUE_A)
        self.playw(*[FadeIn(item) for item in gvt.words])
        self.playw(*[FadeIn(item) for item in lvt.words])

        tm_text = Words(
            "Teacher Model", font_size=24, font="Noto Sans KR", color=YELLOW_A
        ).next_to(crop1_group, UP, buff=0.75)
        tm_box = SurroundingRectangle(tm_text, color=YELLOW, buff=0.2, stroke_width=2)
        tm = VGroup(tm_box, tm_text)
        sm_text = (
            Words("Student Model", font_size=24, font="Noto Sans KR", color=BLUE_A)
            .next_to(crop2_group, UP, buff=0.75)
            .align_to(tm_text, UP)
        )
        sm_box = SurroundingRectangle(sm_text, color=BLUE, buff=0.2, stroke_width=2)
        sm = VGroup(sm_box, sm_text)
        self.playw(FadeIn(tm), FadeIn(sm))


class vit1(Scene3D):
    def construct(self):
        # 먼저, multi crop 전에요 ViT 설명이 좀 필요해서 먼저 보겠습니다
        title = Words(
            "Vision Transformer", font="Noto Sans KR", font_size=72, color=YELLOW_B
        )
        self.playwl(*[FadeIn(item) for item in title.words], lag_ratio=0.5)

        # ViT, Vision Transformer에서는요 이 3가지를 알면 됩니다
        # 1) 이미지를 patch 단위로 쪼갠다 2) transformer 구조로 이미지를 이해한다 3) classification은 CLS token을 쓴다
        key_points = VGroup(
            Words("① 이미지를 patch로 쪼갠다", font="Noto Sans KR", font_size=28),
            Words(
                "② Transformer로 이미지를 이해한다", font="Noto Sans KR", font_size=28
            ),
            Words("③ CLS token의 역할", font="Noto Sans KR", font_size=28),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        self.playwl(
            title.animate.scale(0.25).to_corner(UL).set_opacity(0.5),
            FadeIn(key_points[0], shift=RIGHT * 0.3),
            lag_ratio=0.3,
        )
        self.playw(FadeIn(key_points[1], shift=RIGHT * 0.3))
        self.playw(FadeIn(key_points[2], shift=RIGHT * 0.3))

        # 우선 첫 번째, patch 단위
        self.play(FadeOut(key_points[1:], shift=DOWN))
        self.playw(
            key_points[0]
            .animate.scale(0.7)
            .next_to(title, DOWN, buff=0.25)
            .set_opacity(0.7)
            .align_to(title, LEFT)
        )
        # ViT 이전에는 딥러닝 모델에 주로 pixel 단위 이미지를 입력했습니다
        # pixel 시각화
        # MNIST 이미지 가져오기
        mnist_img, _ = mnist[0]  # 첫 번째 MNIST 이미지
        mnist_array = np.array(mnist_img)  # 28x28 grayscale

        # 20x20으로 리사이즈
        mnist_img_resized = mnist_img.resize((20, 20), Image.LANCZOS)
        mnist_array_20 = np.array(mnist_img_resized)

        # 정규화 (0~255 -> 0~1)
        mnist_normalized = mnist_array_20 / 255.0

        pixel_grid = VGroup(
            *[
                Square(
                    0.08,
                    stroke_width=1,
                    stroke_color=GREY_D,
                    fill_opacity=0.9,
                    fill_color=interpolate_color(BLACK, WHITE, mnist_normalized[i, j]),
                )
                for i in range(20)
                for j in range(20)
            ]
        ).arrange_in_grid(20, 20, buff=0)
        pixel_grid.scale(0.8).move_to(ORIGIN + LEFT * 2)

        pixel_label = (
            Words("Pixel 단위", font="Noto Sans KR", font_size=48)
            .scale(0.5)
            .next_to(pixel_grid, DOWN)
        )

        self.playw(FadeIn(pixel_grid))
        self.play(FadeIn(pixel_label))
        self.playw(
            pixel_grid.animate.arrange_in_grid(20, 20, buff=0.05).align_to(
                pixel_grid, DOWN
            )
        )
        # 그런데 ViT의 Transformer는 마치 언어에서의 token처럼요
        # 의미 단위 취급을 위해서 이미지를 patch로 만듭니다
        # patch 시각화
        patch_grid = (
            VGroup(
                *[
                    VGroup(
                        *[
                            pixel_grid[i * 20 + j]
                            for i in range(r * 4, (r + 1) * 4)
                            for j in range(c * 4, (c + 1) * 4)
                        ]
                    )
                    .copy()
                    .arrange_in_grid(4, 4, buff=0)
                    for r in range(5)
                    for c in range(5)
                ]
            )
            .arrange_in_grid(5, 5, buff=0.1)
            .move_to(ORIGIN + RIGHT * 2)
            .align_to(pixel_grid, DOWN)
        )

        patch_label = (
            Words("Patch 단위", font="Noto Sans KR", font_size=48)
            .scale(0.5)
            .next_to(patch_grid, DOWN)
        )

        self.playw(FadeIn(patch_grid))
        self.playw(FadeIn(patch_label))

        # 이걸 한 샘플당 정보의 크기 관점에서 보면은요
        # patch 단위가 pixel 단위보다 정보가 많죠?
        pixel_one = pixel_grid[105].copy()
        patch_one = patch_grid[6].copy()

        pixel_one.generate_target()
        patch_one.generate_target()
        VGroup(pixel_one.target.scale(2), patch_one.target.scale(2)).arrange(
            RIGHT, buff=1
        )
        self.playw(
            MoveToTarget(pixel_one),
            MoveToTarget(patch_one),
            pixel_grid.animate.set_opacity(0.3).shift(LEFT),
            patch_grid.animate.set_opacity(0.3).shift(RIGHT),
            pixel_label.animate.scale(0.8).next_to(pixel_one.target, DOWN),
            patch_label.animate.scale(0.8).next_to(patch_one.target, DOWN),
        )

        # pixel은 단순히 한 점이지만요 patch는 의미 단위, NLP에서의 subword같은 단위라고 볼 수 있습니다
        self.wait()

        # 그래서 ViT에서는 의미 단위로 attention할 수 있도록요
        # 이미지를 patch 단위의 2D 나열로 입력받습니다
        self.play(FadeOut(pixel_one), FadeOut(patch_one))
        self.play(
            FadeOut(pixel_grid),
            FadeOut(pixel_label),
            patch_grid.animate.move_to(ORIGIN).scale(1.5).set_opacity(1),
            FadeOut(patch_label),
        )
        self.playw(patch_grid.animate.scale(1 / 1.5 * 0.6).arrange(RIGHT, buff=0.1))

        # 그리고 그 다음 두 번째로 볼 건
        self.mouse.next_to(key_points[0], LEFT, buff=1)
        key_points[1].scale(0.7).set_opacity(0.7).move_to(key_points[0]).align_to(
            key_points[0], LEFT
        )
        self.playw(self.mouse.animate.on(key_points[0][0]))

        # Transformer 구조로 이미지를 이해한다 라는 점인데요
        self.playw(
            FadeOut(self.mouse),
            Transform(
                key_points[0], key_points[1], replace_mobject_with_target_in_scene=True
            ),
        )

        # 그 중에서도 특히 encoder only transformer 형태로
        encoder_text = Words(
            "Encoder-only Transformer", font="Noto Sans KR", font_size=48, color=BLUE_B
        ).scale(0.5)
        encoder_box = SurroundingRectangle(
            encoder_text,
            color=BLUE,
            buff=1.5,
            stroke_width=2,
            fill_opacity=0.9,
            fill_color=BLACK,
        ).stretch_to_fit_height(2)
        encoder = VGroup(encoder_box, encoder_text)
        self.play(patch_grid.animate.shift(DOWN * 1.5))
        self.playw(FadeIn(encoder))

        # patch 단위로 self attention해서 이미지를 이해합니다
        self.playw(patch_grid.animate.next_to(encoder, UP, buff=0.5).set_opacity(0.9))

        # 아까 말했듯이 이미지를 patch 단위로 표현하고요
        self.playwl(
            *[Indicate(patch, scale_factor=1.1, color=GREY_B) for patch in patch_grid]
        )

        # self attention은 patch 간의 상관관계를 분석합니다
        self.play(Indicate(encoder_text, scale_factor=1.1, color=YELLOW_B))
        lines = VGroup(
            *[
                ArcBetweenPoints(
                    start=patch_grid[i].get_top(),
                    end=patch_grid[j].get_top(),
                    angle=PI / 4,
                    stroke_width=1,
                    color=GREY_B,
                ).set_stroke(opacity=random())
                for i in range(len(patch_grid))
                for j in range(len(patch_grid))
                if i > j and random() < 0.13
            ]
        )

        self.playwl(*[FadeIn(line) for line in lines])

        # 그리고 마지막 CLS token
        self.play(
            self.mouse.next_to(key_points[1], LEFT, buff=1).animate.on(key_points[1][0])
        )
        key_points[2].scale(0.7).set_opacity(0.7).move_to(key_points[1]).align_to(
            key_points[1], LEFT
        )
        self.playw(
            FadeOut(self.mouse),
            Transform(
                key_points[1], key_points[2], replace_mobject_with_target_in_scene=True
            ),
        )
        cls_token = (
            Square(
                0.4,
                stroke_width=2,
                stroke_color=GREY_B,
                fill_opacity=0.9,
                fill_color=YELLOW_A,
            )
            .next_to(patch_grid, LEFT, buff=0.1)
            .scale(1 / 1.5 * 0.6)
        )
        # 이건 BERT에서도 쓰죠?
        cls_label = (
            Words("CLS Token", font="Noto Sans KR", font_size=48)
            .scale(0.3)
            .next_to(cls_token, DOWN, buff=0.05)
        )
        self.playw(FadeIn(cls_token, cls_label))

        # CLS token의 필요성을 설명하기 위해서요
        # self attention 구조를 먼저 보겠습니다
        self.play(FadeOut(encoder_text))
        self.playw(
            encoder_box.animate.stretch_to_fit_height(3.5).align_to(encoder_box, UP)
        )


class selfattn(Scene3D):
    def construct(self):
        # self attention은 입력과 출력이 같은 shape고
        sa_text = Words(
            "Self-Attention", font="Noto Sans KR", font_size=48, color=YELLOW_A
        ).scale(0.5)
        sa_box = (
            SurroundingRectangle(
                sa_text,
                color=GREY_C,
                buff=2.5,
                stroke_width=2,
                fill_opacity=0.4,
                fill_color=BLACK,
            )
            .stretch_to_fit_height(3)
            .set_z_index(2)
        )
        sa = VGroup(
            sa_box, sa_text.next_to(sa_box, LEFT, buff=0.1).align_to(sa_box, UP)
        ).rotate(-PI / 3, axis=RIGHT)
        dim = 12
        # MNIST 이미지 가져오기
        mnist_img, _ = mnist[0]
        mnist_img_resized = mnist_img.resize((16, 16), Image.LANCZOS)
        mnist_array_16 = np.array(mnist_img_resized)
        mnist_normalized = mnist_array_16 / 255.0

        # 4x4 패치로 분할 (4x4 = 16개 패치)
        sa_in = (
            VGroup(
                *[
                    VGroup(
                        *[
                            Square(
                                0.08,
                                stroke_width=1,
                                stroke_color=GREY_D,
                                fill_opacity=0.9,
                                fill_color=interpolate_color(
                                    BLACK, WHITE, mnist_normalized[i, j]
                                ),
                            )
                            for i in range(r * 4, (r + 1) * 4)
                            for j in range(c * 4, (c + 1) * 4)
                        ]
                    ).arrange_in_grid(4, 4, buff=0)
                    for r in range(4)
                    for c in range(4)
                ]
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(sa[0], DOWN, buff=0.5)
            .rotate(-PI / 3, axis=RIGHT)
        )
        self.playw(FadeIn(sa, sa_in))

        # 그 shape는 patch의 나열입니다
        shape = Text(".reshape(h*w)", font=MONO_FONT, color=GREY_B).scale(0.5)
        self.playw(FadeIn(shape.next_to(sa_in, DR, buff=0.2)))

        # self attention 출력의 각 patch는요 전체 patch와의 상관관계가 한 차례 분석된 결과입니다
        self.play(FadeOut(shape), sa_in.animate.move_to(sa[0]))
        lines = VGroup(
            *[
                ArcBetweenPoints(
                    start=sa_in[i].get_center(),
                    end=sa_in[j].get_center(),
                    angle=PI / 4,
                    stroke_width=1.5,
                    color=BLUE_C,
                ).set_stroke(opacity=random())
                for i in range(len(sa_in))
                for j in range(len(sa_in))
                if i > j and random() < 0.2
            ]
        ).set_z_index(3)
        self.play(FadeIn(lines))
        out = sa_in.copy().set_opacity(0.7)
        self.playw(out.animate.next_to(sa[0], UP, buff=0.5).scale(0.9))

        # 하지만 이 구조에서는 classification같은 task에 쓸 patch 정의가 어렵습니다
        self.cf.save_state()
        sa.save_state()
        self.play(
            self.cf.animate.shift(IN * 7 + UP * 1.3),
            lines.animate.set_stroke(opacity=0.2),
            sa[0].animate.set_fill(opacity=0.7).set_stroke(opacity=0.5),
            sa[1].animate.set_opacity(0.3),
            out.animate.scale(1 / 0.9),
        )
        questions = VGroup(Text("?", color=RED).scale(0.4).next_to(p, UP) for p in out)

        # 왜일까요? 어떤 patch를 classification에 쓸 거라고 정해야하는데요
        self.playw(FadeIn(questions, shift=UP * 0.2))
        self.playwl(
            *[Indicate(o, scale_factor=1.1, color=RED_A) for o in out], lag_ratio=0.1
        )

        # 심지어 더 최악은요 이미지 크기가 다르면 patch 개수도 다르니까요
        # 출력이 일관된 구조인 상황도 아닙니다
        self.play(
            self.cf.animate.restore(),
            FadeOut(questions),
            sa.animate.restore(),
            FadeOut(out, sa_in, lines),
        )
        cifar_img, _ = cifar10[1]
        cifar_img_resized = cifar_img.resize((24, 24), Image.LANCZOS)
        cifar_array = np.array(cifar_img_resized)
        cifar_normalized = cifar_array / 255.0

        # 8x8 패치로 분할 (3x3 = 9개 패치)
        input_patches = (
            VGroup(
                *[
                    VGroup(
                        *[
                            Square(
                                0.06,
                                stroke_width=1,
                                stroke_color=GREY_D,
                                fill_opacity=0.9,
                                fill_color=rgb_to_color(cifar_normalized[i, j]),
                            )
                            for i in range(r * 8, (r + 1) * 8)
                            for j in range(c * 8, (c + 1) * 8)
                        ]
                    ).arrange_in_grid(8, 8, buff=0)
                    for r in range(3)
                    for c in range(3)
                ]
            )
            .arrange_in_grid(3, 3, buff=0.0)
            .next_to(sa[0], DOWN, buff=0.5)
        )
        self.play(FadeIn(input_patches))
        self.play(
            input_patches.animate.rotate(-PI / 3, axis=RIGHT)
            .arrange(RIGHT, buff=0.1)
            .next_to(sa[0], DOWN, buff=0.5)
        )
        self.play(input_patches.animate.move_to(sa[0]).scale(0.9))
        lines = VGroup(
            *[
                ArcBetweenPoints(
                    start=input_patches[i].get_center(),
                    end=input_patches[j].get_center(),
                    angle=PI / 4,
                    stroke_width=1.5,
                    color=BLUE_C,
                ).set_stroke(opacity=random())
                for i in range(len(input_patches))
                for j in range(len(input_patches))
                if i > j and random() < 0.3
            ]
        ).set_z_index(3)
        out = input_patches.copy().set_opacity(0.7)
        self.playw(FadeIn(lines), out.animate.next_to(sa[0], UP, buff=0.5).scale(0.9))

        # 바로 그래서 CLS token을 씁니다
        cls_token = Square(
            0.4,
            stroke_width=2,
            stroke_color=GREY_B,
            fill_opacity=0.9,
            fill_color=YELLOW_A,
        ).scale(0.9)
        cls_label = Words("CLS Token", font="Noto Sans KR", font_size=48).scale(0.3)
        self.play(
            input_patches.animate.next_to(sa[0], DOWN, buff=0.5).scale(1 / 0.9),
            FadeOut(lines, out),
        )
        cls_token.next_to(input_patches, LEFT, buff=0.1)
        cls_label.next_to(cls_token, DOWN, buff=0.05)
        self.playw(FadeIn(cls_token, cls_label))

        # 이미지랑 상관없이 특정 task에 쓸 임시 patch를 두고요
        self.playw(cls_token.animate.rotate(-PI / 3, axis=RIGHT))

        # encoder layer stack의 마지막에 CLS token을 task에 씁니다
        input_wcls = VGroup(cls_token, *input_patches)
        self.play(input_wcls.animate.move_to(sa[0]).scale(0.9), FadeOut(cls_label))
        lines = VGroup(
            *[
                ArcBetweenPoints(
                    start=input_wcls[i].get_center(),
                    end=input_wcls[j].get_center(),
                    angle=PI / 4,
                    stroke_width=1.5,
                    color=BLUE_C,
                ).set_stroke(opacity=random())
                for i in range(len(input_wcls))
                for j in range(len(input_wcls))
                if i > j and random() < 0.3
            ]
        ).set_z_index(3)
        out_wcls = input_wcls.copy().set_opacity(0.7)
        self.playw(
            FadeIn(lines), out_wcls.animate.next_to(sa[0], UP, buff=0.5).scale(0.9)
        )

        # 그러면 이 CLS token은 어떤 이미지 입력에서든 존재해서 항상 task를 수행해왔죠?
        self.cf.save_state()
        sa.save_state()
        lines.save_state()
        self.play(
            self.cf.animate.shift(IN * 7 + UP * 1.3),
            lines.animate.set_stroke(opacity=0.2),
            sa[0].animate.set_fill(opacity=0.7).set_stroke(opacity=0.5),
            sa[1].animate.set_opacity(0.3),
            out_wcls.animate.scale(1 / 0.9),
        )
        self.playw(
            out_wcls[0].animate.shift(UP * 0.3), out_wcls[1:].animate.set_opacity(0.5)
        )
        # 그래서 task에 맞는 attention mapping이 되어있을 겁니다
        self.playw(lines.animate.restore())

        # 그래서 inference 단계에서도요 이 CLS token은 attention mapping이 잘 되어있고
        # 이 task를 잘 수행할 준비가 되어있습니다
        self.play(
            self.cf.animate.restore(),
            sa.animate.restore(),
            out_wcls[0].animate.shift(DOWN * 0.3),
        )
        # CIFAR-10으로 다시 보여주기
        self.play(
            FadeOut(out_wcls, input_wcls, lines),
        )

        # CIFAR-10 이미지로 전환
        cifar_img2, _ = cifar10[2]
        cifar_img2_resized = cifar_img2.resize((24, 24), Image.LANCZOS)
        cifar_array2 = np.array(cifar_img2_resized)
        cifar_normalized2 = cifar_array2 / 255.0

        # 8x8 패치로 분할 (3x3 = 9개 패치)
        cifar_patches = (
            VGroup(
                *[
                    VGroup(
                        *[
                            Square(
                                0.06,
                                stroke_width=1,
                                stroke_color=GREY_D,
                                fill_opacity=0.9,
                                fill_color=rgb_to_color(cifar_normalized2[i, j]),
                            )
                            for i in range(r * 8, (r + 1) * 8)
                            for j in range(c * 8, (c + 1) * 8)
                        ]
                    ).arrange_in_grid(8, 8, buff=0)
                    for r in range(3)
                    for c in range(3)
                ]
            )
            .arrange_in_grid(3, 3, buff=0.0)
            .next_to(sa[0], DOWN, buff=0.5)
        )
        self.play(FadeIn(cifar_patches))
        self.play(
            cifar_patches.animate.rotate(-PI / 3, axis=RIGHT)
            .arrange(RIGHT, buff=0.1)
            .next_to(sa[0], DOWN, buff=0.5)
        )

        # CLS token 추가
        cls_token2 = (
            Square(
                0.4,
                stroke_width=2,
                stroke_color=GREY_B,
                fill_opacity=0.9,
                fill_color=YELLOW_A,
            )
            .scale(0.9)
            .next_to(cifar_patches, LEFT, buff=0.1)
            .rotate(-PI / 3, axis=RIGHT)
        )
        self.playw(FadeIn(cls_token2))

        # Encoder 통과
        input_wcls2 = VGroup(cls_token2, *cifar_patches)
        self.play(input_wcls2.animate.move_to(sa[0]).scale(0.9))
        lines2 = VGroup(
            *[
                ArcBetweenPoints(
                    start=input_wcls2[i].get_center(),
                    end=input_wcls2[j].get_center(),
                    angle=PI / 4,
                    stroke_width=1.5,
                    color=BLUE_C,
                ).set_stroke(opacity=random())
                for i in range(len(input_wcls2))
                for j in range(len(input_wcls2))
                if i > j and random() < 0.3
            ]
        ).set_z_index(3)
        out_wcls2 = input_wcls2.copy().set_opacity(0.7)
        self.playw(
            FadeIn(lines2), out_wcls2.animate.next_to(sa[0], UP, buff=0.5).scale(0.8)
        )

        # CLS token 강조
        self.cf.save_state()
        sa.save_state()
        lines2.save_state()
        self.play(
            self.cf.animate.shift(IN * 7 + UP * 1.3),
            lines2.animate.set_stroke(opacity=0.2),
            sa[0].animate.set_fill(opacity=0.7).set_stroke(opacity=0.5),
            sa[1].animate.set_opacity(0.3),
            out_wcls2.animate.scale(1 / 0.9),
        )
        self.playw(
            out_wcls2[0].animate.shift(UP * 0.5), out_wcls2[1:].animate.set_opacity(0.5)
        )

        cls_label.next_to(out_wcls2[0], DOWN, buff=0.05)
        self.playw(FadeIn(cls_label))
        return

        conclusion_text = Words(
            "CLS Token = 일관된 Task 수행을 위한 임시 토큰",
            font="Noto Sans KR",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN)

        self.playw(FadeIn(conclusion_text))

        # 최종 강조
        self.playw(
            output_with_cls[0].animate.scale(1.4).set_stroke(width=6),
            Indicate(cls_to_task, scale_factor=1.2, color=YELLOW),
        )

        self.playw(
            FadeOut(title),
            FadeOut(input_with_cls),
            FadeOut(output_with_cls),
            FadeOut(output_cls_label),
            FadeOut(encoder_stack),
            FadeOut(stack_label),
            FadeOut(cls_through_encoder),
            FadeOut(task_box),
            FadeOut(task_label),
            FadeOut(cls_to_task),
            FadeOut(mapping_arrows),
            FadeOut(mapping_text),
            FadeOut(conclusion_text),
        )


class multicropinvit(Scene2D):
    def construct(self):
        # 고양이 이미지 로드
        cat_img = Image.open(cat_path)
        cat_array = np.array(cat_img)
        cat_img_resized = cat_img.resize((100, 100), Image.LANCZOS)
        cat_array = np.array(cat_img_resized)

        # patch 단위로 자르기 위한 img
        patch_h = 10
        patch_w = 10
        scale_factor = 0.5
        img = (
            Group(
                *[
                    ImageMobject(
                        cat_array[
                            i * patch_h : (i + 1) * patch_h,
                            j * patch_w : (j + 1) * patch_w,
                            :,
                        ]
                    ).scale(scale_factor)
                    for i in range(10)
                    for j in range(10)
                ]
            )
            .arrange_in_grid(10, 10, buff=0.000)
            .scale(7)
        )

        # 1. "아까 말한대로 crop을 다양하게 한다는 말인데요"
        self.play(FadeIn(img))
        # 두 crop 영역 표시
        crop1_h_patches = 7
        crop1_w_patches = 7
        crop2_h_patches = 5
        crop2_w_patches = 5

        crop1_start_row = 1
        crop1_start_col = 1
        crop2_start_row = 2
        crop2_start_col = 4
        original_img = img.copy()

        img_crop1 = Group(
            *[
                img[i * 10 + j]
                for i in range(crop1_start_row, crop1_start_row + crop1_h_patches)
                for j in range(crop1_start_col, crop1_start_col + crop1_w_patches)
            ]
        ).copy()
        img_crop2 = Group(
            *[
                img[i * 10 + j]
                for i in range(crop2_start_row, crop2_start_row + crop2_h_patches)
                for j in range(crop2_start_col, crop2_start_col + crop2_w_patches)
            ]
        ).copy()
        crop1_rect = SurroundingRectangle(
            img_crop1, color=YELLOW_A, stroke_width=3, buff=0.0
        )
        crop2_rect = SurroundingRectangle(
            img_crop2, color=BLUE_A, stroke_width=3, buff=0.0
        )
        self.play(FadeIn(crop1_rect), FadeIn(crop2_rect))
        self.playw(
            img_crop1.animate.next_to(img, LEFT * 3),
            img_crop2.animate.next_to(img, RIGHT * 3),
        )

        # 2-3. "crop은 모델에다가 이미지 전체가 아니라 일부만 입력하는 잡기술입니다"
        self.play(Flash(img_crop1.get_corner(UL), color=YELLOW_B))
        self.playw(Flash(img_crop2.get_corner(UR), color=BLUE_B))

        # 4-6. "그러면 모델인 ViT 입장에서는요 / 어떤 patch들이 주어지죠? / 바로 CLS token과 crop된 이미지를 이루는 patch들입니다"
        # ViT 박스 등장
        vit_box = Rectangle(
            width=10,
            height=1.6,
            color=GREY_C,
            stroke_width=2,
            fill_opacity=0.4,
            fill_color=BLACK,
        )
        vit_text = Words("ViT", font="Noto Sans KR", font_size=36).move_to(vit_box)
        vit = VGroup(vit_box, vit_text).shift(UP * 1.5)

        self.playw(
            FadeIn(vit),
            FadeOut(img, crop1_rect, crop2_rect),
            Group(img_crop1, img_crop2)
            .animate.arrange(RIGHT, buff=1.5)
            .shift(DOWN * 1.5),
        )

        img_crop2.generate_target()
        img_crop2.target.scale(0.5).arrange(RIGHT, buff=0.05).next_to(
            vit, DOWN, buff=0.5
        )
        cls_token = Square(
            0.12,
            fill_color=YELLOW_A,
            fill_opacity=0.9,
            stroke_width=2,
            stroke_color=GREY_B,
        ).next_to(img_crop2.target, LEFT, buff=0.15)
        cls_label = (
            Words("CLS Token", font="Noto Sans KR", font_size=48)
            .scale(0.25)
            .next_to(cls_token, DOWN, buff=0.05)
        )
        self.playw(
            MoveToTarget(img_crop2),
            FadeIn(cls_token, cls_label),
        )

        # 7-10. 작게 crop됐을수록 적은 patch들, 즉 적은 정보만 있습니다
        self.wait()
        brace2 = Brace(img_crop2, DOWN, buff=0.2, color=GREY_C)
        info_text2 = Words(
            str(len(img_crop2)), font="Noto Sans KR", font_size=24, color=RED_A
        ).next_to(brace2, DOWN, buff=0.1)
        self.playw(FadeIn(brace2), FadeIn(info_text2))

        # 반대로 크게 crop됐으면 더 많은 patch들, 더 많은 정보가 있습니다
        self.play(
            VGroup(cls_token, cls_label).animate.shift(UP * 3).set_opacity(0),
            FadeOut(img_crop2, shift=UP * 3),
            FadeOut(brace2, info_text2),
        )
        img_crop1.generate_target()
        img_crop1.target.scale(0.5).arrange(RIGHT, buff=0.05).next_to(
            vit, DOWN, buff=0.5
        )
        cls_token1 = Square(
            0.12,
            fill_color=YELLOW_A,
            fill_opacity=0.9,
            stroke_width=2,
            stroke_color=GREY_B,
        ).next_to(img_crop1.target, LEFT, buff=0.15)
        cls_label1 = (
            Words("CLS Token", font="Noto Sans KR", font_size=48)
            .scale(0.25)
            .next_to(cls_token1, DOWN, buff=0.05)
        )
        self.playw(
            MoveToTarget(img_crop1),
            FadeIn(cls_token1, cls_label1),
        )
        brace1 = Brace(img_crop1, DOWN, buff=0.2, color=GREY_C)
        info_text1 = Words(
            str(len(img_crop1)), font="Noto Sans KR", font_size=24, color=GREEN_A
        ).next_to(brace1, DOWN, buff=0.1)
        self.playw(FadeIn(brace1), FadeIn(info_text1))
        self.playw(
            VGroup(cls_token1, cls_label1).animate.shift(UP * 3).set_opacity(0),
            FadeOut(img_crop1, shift=UP * 3),
            FadeOut(brace1, info_text1),
        )

        # 11-13. "그래서 ViT에 crop된 이미지를 입력한다는 건 / CLS token이 분석할 정보를 / 제한한다는 의미입니다"
        self.playw(vit.animate.move_to(ORIGIN))


class dinomulticropexample(Scene2D):
    def construct(self):
        # 고양이 이미지 로드
        cat_img = Image.open(cat_path)
        cat_array = np.array(cat_img)
        cat_img_resized = cat_img.resize((100, 100), Image.LANCZOS)
        cat_array = np.array(cat_img_resized)

        # patch 단위로 자르기 위한 img
        patch_h = 10
        patch_w = 10
        scale_factor = 0.5
        img = (
            Group(
                *[
                    ImageMobject(
                        cat_array[
                            i * patch_h : (i + 1) * patch_h,
                            j * patch_w : (j + 1) * patch_w,
                            :,
                        ]
                    ).scale(scale_factor)
                    for i in range(10)
                    for j in range(10)
                ]
            )
            .arrange_in_grid(10, 10, buff=0.000)
            .scale(7)
        )

        # 첫 번째 crop
        crop1_h_patches = 7
        crop1_w_patches = 7
        crop1_start_row = 1
        crop1_start_col = 1

        patches = img.submobjects

        crop1_indices = [
            i * 10 + j
            for i in range(crop1_start_row, crop1_start_row + crop1_h_patches)
            for j in range(crop1_start_col, crop1_start_col + crop1_w_patches)
        ]
        crop1_patches = [patches[i] for i in crop1_indices]
        crop1_group = Group(*crop1_patches).copy()
        crop1_group.arrange_in_grid(
            rows=crop1_h_patches, cols=crop1_w_patches, buff=0.0
        )
        crop1_group.move_to(Group(*crop1_patches).get_center())

        # 두 번째 crop
        crop2_h_patches = 5
        crop2_w_patches = 5
        crop2_start_row = 2
        crop2_start_col = 4
        crop2_indices = [
            i * 10 + j
            for i in range(crop2_start_row, crop2_start_row + crop2_h_patches)
            for j in range(crop2_start_col, crop2_start_col + crop2_w_patches)
        ]
        crop2_patches = [patches[i] for i in crop2_indices]
        crop2_group = Group(*crop2_patches).copy()
        crop2_group.arrange_in_grid(
            rows=crop2_h_patches, cols=crop2_w_patches, buff=0.0
        )
        crop2_group.move_to(Group(*crop2_patches).get_center())
        crops = Group(crop1_group, crop2_group).arrange(RIGHT, buff=2)
        self.playw(FadeIn(crops))

        # ViT 박스 등장
        crops.generate_target().arrange(RIGHT, buff=10).shift(DOWN)
        vit_box = Rectangle(
            width=10,
            height=1.6,
            color=GREY_C,
            stroke_width=2,
            fill_opacity=0.8,
            fill_color=BLACK,
        ).set_z_index(1)
        vit_text = (
            Words("ViT (Teacher model)", font="Noto Sans KR", color=YELLOW_A)
            .move_to(vit_box)
            .scale(0.75)
        ).set_z_index(2)
        vit1 = VGroup(vit_box, vit_text).next_to(crops.target[0], UP, buff=1)
        vit_box = Rectangle(
            width=10,
            height=1.6,
            color=GREY_C,
            stroke_width=2,
            fill_opacity=0.8,
            fill_color=BLACK,
        ).set_z_index(1)
        vit_text = (
            Words("ViT (Student model)", font="Noto Sans KR", color=BLUE_A)
            .move_to(vit_box)
            .scale(0.75)
        ).set_z_index(2)
        vit2 = (
            VGroup(vit_box, vit_text)
            .next_to(crops.target[1], UP, buff=1)
            .align_to(vit1, UP)
        )
        self.playw(
            MoveToTarget(crops),
            FadeIn(vit1),
            FadeIn(vit2),
            self.cf.animate.scale(1.8),
        )
        crop1_group.generate_target().scale(0.5).arrange(RIGHT, buff=0.05).next_to(
            vit1, DOWN, buff=0.5
        )
        cls_t = Square(
            0.12,
            fill_color=YELLOW_A,
            fill_opacity=0.9,
            stroke_width=2,
            stroke_color=GREY_B,
        ).next_to(crop1_group.target[0], LEFT, buff=0.15)
        cls_label = (
            Words("CLS Token(teacher)", font="Noto Sans KR", font_size=48)
            .scale(0.25)
            .next_to(cls_t, DOWN, buff=0.05)
        )
        self.cf.save_state()
        self.playw(
            self.cf.animate.move_to(Group(vit1, crop1_group.target)).scale(0.5),
            MoveToTarget(crop1_group),
            FadeIn(cls_t, cls_label),
        )
        self.play(self.cf.animate.restore())
        crop2_group.generate_target().scale(0.5).arrange(RIGHT, buff=0.05).next_to(
            vit2, DOWN, buff=0.5
        )
        cls_s = Square(
            0.12,
            fill_color=BLUE_A,
            fill_opacity=0.9,
            stroke_width=2,
            stroke_color=GREY_B,
        ).next_to(crop2_group.target[0], LEFT, buff=0.15)
        cls_label2 = (
            Words("CLS Token(student)", font="Noto Sans KR", font_size=48)
            .scale(0.25)
            .next_to(cls_s, DOWN, buff=0.05)
        )
        self.cf.save_state()
        self.playw(
            self.cf.animate.move_to(Group(vit2, crop2_group.target)).scale(0.5),
            MoveToTarget(crop2_group),
            FadeIn(cls_s, cls_label2),
        )
        self.play(self.cf.animate.restore().shift(UP))

        t_in = Group(cls_t, *crop1_group, cls_label)
        s_in = Group(cls_s, *crop2_group, cls_label2)
        self.play(
            t_in.animate.next_to(vit1, UP, buff=0.5),
            s_in.animate.next_to(vit2, UP, buff=0.5),
        )
        lines_t = VGroup(
            *[
                ArcBetweenPoints(
                    start=t_in[0].get_top(),
                    end=t_in[j].get_top(),
                    angle=-PI / 4,
                    stroke_width=1.5,
                    color=BLUE_C,
                ).set_stroke(opacity=random() * 0.5)
                for j in range(len(t_in) - 1)
            ]
        )
        lines_s = VGroup(
            *[
                ArcBetweenPoints(
                    start=s_in[0].get_top(),
                    end=s_in[j].get_top(),
                    angle=-PI / 4,
                    stroke_width=1.5,
                    color=BLUE_C,
                ).set_stroke(opacity=random() * 0.5)
                for j in range(len(s_in) - 1)
            ]
        )
        self.playw(FadeIn(lines_t), FadeIn(lines_s))

        clst = VGroup(cls_t, cls_label)
        clss = VGroup(cls_s, cls_label2)
        clss_ = clss.copy()
        self.play(FadeOut(vit1, vit2, t_in[1:-1], s_in[1:-1], lines_t, lines_s))
        self.play(
            VGroup(clst, clss).animate.arrange(RIGHT, buff=3),
            self.cf.animate.scale(0.5).move_to(ORIGIN),
        )

        mlp_t = Rectangle(
            width=2,
            height=1,
            color=YELLOW_A,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        ).set_z_index(1)
        mlp_text_t = (
            Words("MLP", font="Noto Sans KR", color=YELLOW_A).move_to(mlp_t).scale(0.5)
        ).set_z_index(2)
        mlpt = VGroup(mlp_t, mlp_text_t).next_to(clst, UP, buff=0.5)
        mlp_s = Rectangle(
            width=2,
            height=1,
            color=BLUE_A,
            stroke_width=2,
            fill_opacity=1,
            fill_color=BLACK,
        ).set_z_index(1)
        mlp_text_s = (
            Words("MLP", font="Noto Sans KR", color=BLUE_A).move_to(mlp_s).scale(0.5)
        ).set_z_index(2)
        mlps = VGroup(mlp_s, mlp_text_s).next_to(clss, UP, buff=0.5)
        self.playwl(FadeIn(mlpt, mlps), self.cf.animate.shift(UP * 0.5), lag_ratio=0.1)

        outt = MLP(3, 8).rotate(PI / 2).next_to(mlpt, UP, buff=-0.5)
        outt[0].set_opacity(0)
        idxt = VGroup()
        for i, o in enumerate(outt[-1]):
            idxt.add(Text(f"{i}", font=MONO_FONT, font_size=16).move_to(o))
            o.set_stroke(color=YELLOW_A, width=2)
        tarr = Arrow(
            cls_t.get_top(),
            mlp_t.get_bottom(),
            buff=0.05,
            stroke_width=2,
            tip_length=0.2,
        )
        self.playwl(
            GrowArrow(tarr),
            FadeIn(outt, idxt),
            self.cf.animate.shift(UP),
            lag_ratio=0.2,
        )
        outs = MLP(3, 8).rotate(PI / 2).next_to(mlps, UP, buff=-0.5)
        outs[0].set_opacity(0)
        idxs = VGroup()
        for i, o in enumerate(outs[-1]):
            idxs.add(Text(f"{i}", font=MONO_FONT, font_size=16).move_to(o))
            o.set_stroke(color=BLUE_A, width=2)
        sarr = Arrow(
            cls_s.get_top(),
            mlp_s.get_bottom(),
            buff=0.05,
            stroke_width=2,
            tip_length=0.2,
        )
        self.playwl(GrowArrow(sarr), FadeIn(outs, idxs), lag_ratio=0.2)

        ifn = lambda x, c: Indicate(x, scale_factor=1.2, color=c)
        self.playwl(
            *[
                AnimationGroup(ifn(ot, rc := random_color()), ifn(os, rc))
                for ot, os in zip(outt[-1], outs[-1])
            ],
        )
        self.play(
            AnchorToPoint(
                Group(
                    vit2.set_opacity(0),
                    clss_.set_opacity(0),
                ),
                dest=clss,
                anchor=clss_,
            )
        )
        self.play(
            FadeOut(clst, mlpt, outt, idxt, tarr),
        )
        self.playwl(vit2.animate.set_opacity(1), self.cf.animate.move_to(vit2).scale(1.5))

class multicropeffect(Scene2D):
    def construct(self):
        # 고양이 이미지 로드 (dinomulticropexample에서 재사용)
        cat_img = Image.open(cat_path)
        cat_array = np.array(cat_img)
        cat_img_resized = cat_img.resize((100, 100), Image.LANCZOS)
        cat_array = np.array(cat_img_resized)

        # patch 단위로 자르기
        patch_h = 10
        patch_w = 10
        scale_factor = 0.5
        img = (
            Group(
                *[
                    ImageMobject(
                        cat_array[
                            i * patch_h : (i + 1) * patch_h,
                            j * patch_w : (j + 1) * patch_w,
                            :,
                        ]
                    ).scale(scale_factor)
                    for i in range(10)
                    for j in range(10)
                ]
            )
            .arrange_in_grid(10, 10, buff=0.000)
            .scale(4)
        )

        patches = img.submobjects

        # 1-6. 전체 이미지 → local view 강조
        full_img = img.copy().scale(0.8)
        self.playw(FadeIn(full_img))

        # 귀 부분 crop 영역 표시
        ear_crop_indices = [
            i * 10 + j
            for i in range(0, 3)
            for j in range(2, 8)
        ]
        ear_rect = SurroundingRectangle(
            Group(*[full_img.submobjects[i] for i in ear_crop_indices]),
            color=YELLOW,
            buff=0,
            stroke_width=4
        )
        self.playw(FadeIn(ear_rect))

        # 귀 부분만 확대
        ear_patches = [patches[i].copy() for i in ear_crop_indices]
        ear_group = Group(*ear_patches).arrange_in_grid(3, 6, buff=0.0).scale(2.5).shift(RIGHT*3.5)

        self.play(full_img.animate.shift(LEFT*3.5).scale(0.7), FadeOut(ear_rect))
        self.playw(FadeIn(ear_group))

        # 7-8. 귀만 보고 전체 유추 (화살표)
        arrow = Arrow(ear_group.get_left(), full_img.get_right(), buff=0.2, stroke_width=4, color=GREEN_A)
        self.playw(FadeIn(arrow))

        # 전체 이미지 강조
        full_img_glow = SurroundingRectangle(full_img, color=GREEN, buff=0.1, stroke_width=5)
        self.playw(FadeIn(full_img_glow))
        self.play(FadeOut(arrow), FadeOut(full_img_glow), FadeOut(full_img))

        # 9-12. 두 가지 지식 - 귀 특징 분석
        ear_group.generate_target()
        ear_group.target.shift(LEFT*3 + UP*0.5)
        self.play(MoveToTarget(ear_group))

        # 지식 1: 고양이 귀 특징 강조
        feature_circles = VGroup(
            *[Circle(radius=0.2, color=GREEN_A, stroke_width=4).move_to(ear_patches[i])
              for i in [2, 5, 8, 11, 14]]
        )
        self.playw(FadeIn(feature_circles))
        self.playw(feature_circles.animate.set_stroke(width=6).scale(1.15))
        self.play(feature_circles.animate.set_stroke(width=4).scale(1/1.15))

        # 지식 2: 다른 동물 귀와 대비
        other_ear = VGroup(
            *[Square(0.3, fill_color=interpolate_color(GREY_D, GREY_B, random()),
                     fill_opacity=0.8, stroke_width=1, stroke_color=GREY_C)
              for _ in range(18)]
        ).arrange_in_grid(3, 6, buff=0.0).scale(2.5).shift(RIGHT*3 + UP*0.5)

        self.playw(FadeIn(other_ear))

        # 대비 표시
        ne_mark = Text("≠", font_size=72, color=RED_A).move_to((ear_group.get_center() + other_ear.get_center())/2)
        self.playw(FadeIn(ne_mark, scale=1.5))

        # 13-15. Student(local) vs Teacher(global) → general 학습
        self.play(FadeOut(ear_group), FadeOut(other_ear), FadeOut(feature_circles), FadeOut(ne_mark))

        # Local view (student) - 작은 crop
        local_crop_indices = [
            i * 10 + j
            for i in range(3, 7)
            for j in range(3, 7)
        ]
        local_patches = [patches[i].copy() for i in local_crop_indices]
        local_group = Group(*local_patches).arrange_in_grid(4, 4, buff=0.05).scale(1.5).shift(RIGHT*3.5)

        # Global view (teacher) - 큰 crop
        global_crop_indices = [i for i in range(100) if i % 2 == 0]
        global_patches = [patches[i].copy() for i in global_crop_indices]
        global_group = Group(*global_patches).arrange_in_grid(5, 10, buff=0.02).scale(0.9).shift(LEFT*3.5)

        local_box = SurroundingRectangle(local_group, color=BLUE_A, buff=0.2, stroke_width=4)
        global_box = SurroundingRectangle(global_group, color=YELLOW_A, buff=0.2, stroke_width=4)

        self.playw(FadeIn(global_group), FadeIn(global_box))
        self.playw(FadeIn(local_group), FadeIn(local_box))

        # Student가 Teacher 따라가기 (화살표)
        arrows = VGroup(
            *[Arrow(local_box.get_left(), global_box.get_right(),
                    buff=0.1, stroke_width=3, color=GREEN_A).shift(UP*offset)
              for offset in [-0.2, 0, 0.2]]
        )
        self.playw(FadeIn(arrows))

        # 결과: general 학습 표현 (여러 이미지 샘플)
        result_samples = Group(
            global_group.copy().scale(0.4),
            local_group.copy().scale(0.4),
            global_group.copy().scale(0.4)
        ).arrange(RIGHT, buff=0.5).set_opacity(0.5).next_to(Group(global_group, local_group), DOWN, buff=1)

        self.playw(FadeIn(result_samples, shift=UP*0.5))

        # 전체 강조
        result_glow = SurroundingRectangle(result_samples, color=GREEN_A, buff=0.2, stroke_width=5)
        self.playw(FadeIn(result_glow))

        self.wait(2)
