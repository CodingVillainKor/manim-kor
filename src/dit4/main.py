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

        self.playw(
            patches.animate.arrange_in_grid(14, 14, buff=0.4),
            self.cf.animate.scale(1.4),
        )

        pos_rects = VGroup(
            *[
                DashedVMobject(
                    SurroundingRect(stroke_width=2, color=GREY_B).surround(patch)
                )
                for patch in patches
            ]
        )
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


class finalLayer(Scene2D):
    def construct(self):
        model = (
            TextBox(
                text="DiT",
                text_kwargs=dict(font_size=48, color=YELLOW),
                box_kwargs=dict(color=WHITE, buff=1, stroke_width=3),
            )
            .shift(UP)
            .set_z_index(1)
        )
        model.box.stretch_to_fit_width(11).stretch_to_fit_height(3.5).set_fill(
            BLACK, 0.7
        )
        model.text.next_to(model, LEFT, buff=0.1).align_to(model, UP)
        self.addw(model)

        img_np = imread("mnist.png")[..., :1]
        noise = np.random.randint(0, 256, img_np.shape)
        img_np_clean = img_np.copy()
        img_np = (img_np.astype(float) * 0.4 + noise.astype(float) * 0.6).astype(
            np.uint8
        )
        img = (
            VGroup(
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
            )
            .arrange(DOWN, buff=0)
            .scale(0.3)
            .next_to(model, DOWN)
            .shift(LEFT * 2)
        )
        self.playw(FadeIn(img))

        # patchfy
        patch_size = 4
        patches = VGroup()
        for i in range(0, img_np.shape[0], patch_size):
            for j in range(0, img_np.shape[1], patch_size):
                patch = VGroup()
                for di in range(patch_size):
                    for dj in range(patch_size):
                        if i + di < img_np.shape[0] and j + dj < img_np.shape[1]:
                            patch.add(img[i + di][j + dj])
                patches.add(patch)
        model_in = patches.copy()
        self.play(patches.animate.arrange(RIGHT, buff=0.02).shift(UP))
        self.play(Indicate(patches, scale_factor=1.1, color=RED))

        img_clean = (
            VGroup(
                *[
                    VGroup(
                        *[
                            Pixel(
                                color=interpolate_color(
                                    BLACK, WHITE, img_np_clean.astype(float)[i, j] / 255
                                )
                            )
                            for j in range(img_np_clean.shape[1])
                        ]
                    ).arrange(RIGHT, buff=0)
                    for i in range(img_np_clean.shape[0])
                ]
            )
            .arrange(DOWN, buff=0)
            .scale(0.3)
            .next_to(model, DOWN)
            .shift(RIGHT * 3)
        )

        # patchfy
        patches_clean = VGroup()
        for i in range(0, img_np_clean.shape[0], patch_size):
            for j in range(0, img_np_clean.shape[1], patch_size):
                patch = VGroup()
                for di in range(patch_size):
                    for dj in range(patch_size):
                        if (
                            i + di < img_np_clean.shape[0]
                            and j + dj < img_np_clean.shape[1]
                        ):
                            patch.add(img_clean[i + di][j + dj])
                patches_clean.add(patch)

        self.playw(Transform(patches, patches_clean))

        self.play(FadeIn(model_in))
        in_text = Text("model input", font_size=24, color=GREEN).next_to(
            model_in, DOWN, buff=0.1
        )
        out_text = Text("model output", font_size=24, color=GREEN).next_to(
            patches_clean, DOWN, buff=0.1
        )
        self.playw(FadeIn(in_text), FadeIn(out_text))


class gate(Scene2D):
    def construct(self):
        line = Words(
            "x = x + gate_msa * self.attn(...)", font_size=48, font=MONO_FONT
        ).set_color(GREY_B)
        line.words[4].set_color(YELLOW)
        line.words[6].set_color(GREEN_B)
        mlp = Text("self.amlp(...)", font_size=48, font=MONO_FONT)
        mlp[5].set_opacity(0)
        mlp[6:].align_to(mlp[5], LEFT)
        self.addw(line)
        self.playw(
            line.words[-1]
            .animate.become(mlp)
            .set_color(GREEN_B)
            .align_to(line.words[-1], LEFT)
        )
        line.words[-1][5].shift(RIGHT*30)

        gate_val = ValueTracker(1.0)
        gate_text = DecimalNumber(
            gate_val.get_value(),
            num_decimal_places=2,
            font_size=48,
            color=YELLOW,
        ).next_to(line.words[4], DOWN, buff=0.3)
        self.playw(FadeIn(gate_text))
        gate_text.add_updater(lambda m: m.set_value(gate_val.get_value()))
        self.playw(
            gate_val.animate.set_value(0.0), line.words[-2:].animate.set_opacity(0.1)
        )
        self.playw(
            gate_val.animate.set_value(2.0),
            line.words[-1].animate.set_opacity(1).set_color(PURE_GREEN),
            line.words[-2].animate.set_opacity(1),
        )

class modulate(Scene2D):
    def construct(self):
        line = Words("x * (1+scale) + shift", font=MONO_FONT, font_size=60)

        self.addw(line)

        self.playwl(
            Flash(line.words[1:3].get_top()+UP*0.1, color=YELLOW),
            line.words[1:3].animate.set_color(YELLOW),
            Flash(line.words[3:].get_top()+UP*0.1, color=RED),
            line.words[3:].animate.set_color(RED),
            lag_ratio=0.3
        )
        self.playw(Circumscribe(line.words[1:3]))

        self.wait(2)

        self.playw(FadeOut(line.words[2][2:-1], line.words[3:]))