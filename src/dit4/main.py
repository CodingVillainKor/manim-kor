from manim import *
from raenim import *
from random import seed
from cv2 import imread

seed(41)
np.random.seed(41)

Pixel = lambda color: Square(
    side_length=0.15,
    fill_color=color,
    fill_opacity=1,
    stroke_width=1,
    stroke_color=GREY_E,
)


class x_embedder(Scene2D):
    def construct(self):
        img_np = imread("mnist.png")[..., :1]
        img = VGroup(
            *[
                VGroup(
                    *[
                        Pixel(
                            color=interpolate_color(
                                BLACK, WHITE, img_np.astype(float)[i, j] / 255
                            )
                        )
                        for j in range(img_np.shape[1])
                    ]
                ).arrange(RIGHT, buff=0)
                for i in range(img_np.shape[0])
            ]
        ).arrange(DOWN, buff=0)
        self.addw(img)

        # patchfy
        patch_size = 2
        patches = VGroup()
        for i in range(0, img_np.shape[0], patch_size):
            for j in range(0, img_np.shape[1], patch_size):
                patch = VGroup()
                for di in range(patch_size):
                    for dj in range(patch_size):
                        if i + di < img_np.shape[0] and j + dj < img_np.shape[1]:
                            patch.add(img[i + di][j + dj])
                patches.add(patch)

        self.play(self.cf.animate.scale(0.3).move_to(patches[7]))
        self.playw(patches.animate.arrange_in_grid(14, 14, buff=0.1))

        for item in patches:
            item.generate_target().scale(0.7)
        VGroup(*[item.target for item in patches]).arrange(RIGHT, buff=0.05)
        self.playwl(
            AnimationGroup(
                *[MoveToTarget(item) for item in patches], lag_ratio=0.1, run_time=5
            ),
            self.cf.animate.scale(3.33 * 3.5).move_to(ORIGIN).shift(UP * 2),
            lag_ratio=0.1,
            wait=0,
        )

        x_emb = TextBox(
            text="x_embedder",
            text_kwargs=dict(font_size=240, color=BLUE),
            box_kwargs=dict(color=WHITE, buff=2),
        ).next_to(patches, UP, buff=3)
        x_emb.text.set_color_by_gradient(BLUE_A, BLUE_D)
        self.playw(FadeIn(x_emb))


class pos_embed(Scene2D):
    def construct(self):
        img_np = imread("mnist.png")[..., :1]
        img = VGroup(
            *[
                VGroup(
                    *[
                        Pixel(
                            color=interpolate_color(
                                BLACK, WHITE, img_np.astype(float)[i, j] / 255
                            )
                        )
                        for j in range(img_np.shape[1])
                    ]
                ).arrange(RIGHT, buff=0)
                for i in range(img_np.shape[0])
            ]
        ).arrange(DOWN, buff=0)
        self.addw(img)

        # patchfy
        patch_size = 2
        patches = VGroup()
        for i in range(0, img_np.shape[0], patch_size):
            for j in range(0, img_np.shape[1], patch_size):
                patch = VGroup()
                for di in range(patch_size):
                    for dj in range(patch_size):
                        if i + di < img_np.shape[0] and j + dj < img_np.shape[1]:
                            patch.add(img[i + di][j + dj])
                patches.add(patch)

        self.playw(patches.animate.arrange_in_grid(14, 14, buff=0.4), self.cf.animate.scale(1.4))

        pos_rects = VGroup(*[DashedVMobject(SurroundingRect(stroke_width=2, color=GREY_B).surround(patch)) for patch in patches])
        self.play(FadeIn(pos_rects))

        pos_idxs = VGroup()
        for idx, patch in enumerate(patches):
            row = idx // 14
            col = idx % 14
            pos_idx = Text(f"{row},{col}", font_size=20, color=GREY_B).move_to(patch)
            pos_idxs.add(pos_idx)
        self.play(FadeIn(pos_idxs), run_time=3)
        self.playw(self.cf.animate.scale(0.3).move_to(patches[0]))
        self.playw(self.cf.animate.move_to(patches[13]))
        self.playw(self.cf.animate.move_to(patches[-13]))
