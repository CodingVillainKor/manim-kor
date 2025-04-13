from manim import *
from raenim import *
from random import seed, random

seed(41)


def get_vector():
    v = [[random() * 3] for _ in range(3)]
    return v


def vector2matrix(v):
    mv = DecimalMatrix(
        v,
        element_to_mobject_config={"num_decimal_places": 2},
    )
    return mv


def normalize(x, axis):
    x_mean = x.mean(axis=axis, keepdims=True)
    x_std = x.std(axis=axis, keepdims=True)
    return (x - x_mean) / (x_std + 1e-6)


class normvsstd(Scene2D):
    def construct(self):
        normt = Text(
            "Normalization", font="Noto Serif", font_size=36
        ).set_color_by_gradient(GREEN, TEAL)
        stdt = Text(
            "Standardization", font="Noto Serif", font_size=36
        ).set_color_by_gradient(RED, ORANGE)
        VGroup(normt, stdt).arrange(RIGHT, buff=2)

        self.play(FadeIn(normt))
        norm = MathTex(r"y = \frac{x - \min(x)}{\max(x) - \min(x)}").move_to(normt)
        self.playw(
            LaggedStart(normt.animate.shift(UP * 2), FadeIn(norm), lag_ratio=0.5)
        )

        self.play(FadeIn(stdt))
        std = MathTex(r"y = \frac{x - \mu(x)}{\sigma(x)}").move_to(stdt)
        self.playw(LaggedStart(stdt.animate.shift(UP * 2), FadeIn(std), lag_ratio=0.5))

        batcht = (
            Text("Batch", font_size=36)
            .set_color_by_gradient(BLUE, PURPLE)
            .next_to(normt, LEFT)
        )
        layert = (
            Text("Layer", font_size=36)
            .set_color_by_gradient(BLUE, PURPLE)
            .next_to(normt, LEFT)
        )

        self.playw(FadeIn(batcht))
        self.playw(FadeTransform(batcht, layert))
        self.playw(Circumscribe(normt, color=TEAL))
        self.playw(LaggedStart(FadeOut(norm), std.animate.move_to(norm), lag_ratio=0.3))

        self.wait()

        self.playw(Circumscribe(VGroup(layert, normt)))


class normalization(Scene2D):
    def construct(self):
        normt = (
            Text("Normalization", font="Noto Serif", font_size=36)
            .set_color_by_gradient(GREEN, TEAL)
            .shift(UP * 2)
        )
        norm = MathTex("x")
        norm2 = MathTex("x", "-", r"\mu(x)")
        norm3 = MathTex("y", "=", r"{", "x", "-", r"\mu(x)", r"\over", r"\sigma(x)}")

        self.playw(FadeIn(normt, norm))
        self.playw(TransformMatchingTex(norm, norm2))
        self.playw(TransformMatchingTex(norm2, norm3))

        muy = (
            MathTex(r"\mu(y)", "=", r"0", color=YELLOW)
            .next_to(norm[0], DOWN, buff=0.5)
            .shift(LEFT * 1.3)
        )
        sigmay = MathTex(r"\sigma(y)", "=", r"1", color=YELLOW).next_to(
            muy, RIGHT, buff=1
        )

        self.play(norm3[0].animate.set_color(YELLOW), FadeIn(muy))
        self.playw(FadeIn(sigmay))


class tensorAxis(Scene3D):
    def construct(self):
        np.random.seed(41)
        tilt_degree = 65
        self.tilt_camera_horizontal(tilt_degree)

        B, L, D = 3, 4, 5
        x = np.random.randn(B, L, D)[..., None]
        x_norm = normalize(x, axis=0)
        x_m = VGroup(
            *[
                VGroup(*[vector2matrix(v).scale(0.7) for v in x[b]]).arrange(RIGHT)
                for b in range(B)
            ]
        ).arrange(OUT, buff=4)
        BLDt = (
            Text("[B, L, D]", font_size=36, color=GREY_B)
            .rotate(-tilt_degree * DEGREES, UP)
            .shift(UP * 3)
        )
        x_m[1].shift(OUT)
        self.playw(FadeIn(x_m, BLDt))

        zoom_coeff = np.tan(tilt_degree * DEGREES)
        zoom = 2
        self.cf.save_state()
        self.playw(
            self.cf.animate.shift(UP * 2 + IN * zoom + RIGHT * zoom_coeff * zoom),
            x_m.animate.set_opacity(0.3),
        )
        bt, lt, dt = [BLDt[i] for i in [1, 3, 5]]
        bt3, lt4, dt5 = [
            Text(str(num), font_size=36, color=GREY_B)
            .rotate(-tilt_degree * DEGREES, UP)
            .move_to(m)
            for m, num in zip([bt, lt, dt], [B, L, D])
        ]
        self.playw(
            LaggedStart(
                *[
                    string.animate.become(num)
                    for string, num in zip([bt, lt, dt], [bt3, lt4, dt5])
                ],
                lag_ratio=0.3
            )
        )
        self.playw(Restore(self.cf), x_m.animate.set_opacity(1))

        self.playw(LaggedStart(*[Indicate(m) for m in x_m], lag_ratio=0.5))

        anims = []
        for l in range(L):
            lelem = VGroup(*[x_m[b][l] for b in range(B)])
            anims.append(AnimationGroup(*[Indicate(lelem[i]) for i in range(B)]))
        self.playw(LaggedStart(*anims, lag_ratio=0.5))

        x_norm_m = (
            VGroup(
                *[
                    VGroup(*[vector2matrix(v).scale(0.7) for v in x_norm[b]]).arrange(
                        RIGHT
                    )
                    for b in range(B)
                ]
            )
            .arrange(OUT, buff=4)
            .set_color(GREEN)
        )
        x_norm_m[1].shift(OUT)

        lines = [
            Line(
                x_m[0][j][0][i].get_center(),
                x_m[2][j][0][i].get_center(),
                color=GREEN,
                stroke_width=2,
            ).set_opacity(0.8 - j * 0.15)
            for i in range(D)
            for j in range(L)
        ]
        line_in = []
        norms = []
        line_out = []
        idx = 0
        x_m.save_state()
        for i in range(D):
            for j in range(L):
                line_in.append(FadeIn(lines[idx]))
                batch_axis = VGroup(*[x_m[b][j][0][i] for b in range(B)])
                target_axis = VGroup(*[x_norm_m[b][j][0][i] for b in range(B)])
                norms.append(Transform(batch_axis, target_axis))
                line_out.append(FadeOut(lines[idx]))
                idx += 1
        line_in.append(None)
        line_in.append(None)
        norms.insert(0, None)
        norms.append(None)
        line_out.insert(0, None)
        line_out.insert(0, None)
        anims = []
        for i in range(len(line_in)):
            anim = []
            if line_in[i] is not None:
                anim.append(line_in[i])
            if norms[i] is not None:
                anim.append(norms[i])
            if line_out[i] is not None:
                anim.append(line_out[i])
            anims.append(AnimationGroup(*anim))
        for i, anim in enumerate(anims):
            self.play(anim)
            if i == 0:
                self.wait()

        self.playw(Restore(x_m))
        x_norml = normalize(x, axis=1)
        x_norm_m = (
            VGroup(
                *[
                    VGroup(*[vector2matrix(v).scale(0.7) for v in x_norml[b]]).arrange(
                        RIGHT
                    )
                    for b in range(B)
                ]
            )
            .arrange(OUT, buff=4)
            .set_color(GREEN)
        )
        x_norm_m[1].shift(OUT)

        lines = [
            Line(
                x_m[b][0][0][i].get_center(),
                x_m[b][3][0][i].get_center(),
                color=GREEN,
                stroke_width=2,
            ).set_opacity(0.8 - b * 0.15)
            for i in range(D)
            for b in range(B)
        ]
        line_in = []
        norms = []
        line_out = []
        idx = 0
        x_m.save_state()
        for i in range(D):
            for b in range(B):
                line_in.append(FadeIn(lines[idx]))
                batch_axis = VGroup(*[x_m[b][j][0][i] for j in range(L)])
                target_axis = VGroup(*[x_norm_m[b][j][0][i] for j in range(L)])
                norms.append(Transform(batch_axis, target_axis))
                line_out.append(FadeOut(lines[idx]))
                idx += 1
        line_in.append(None)
        line_in.append(None)
        norms.insert(0, None)
        norms.append(None)
        line_out.insert(0, None)
        line_out.insert(0, None)
        anims = []
        for i in range(len(line_in)):
            anim = []
            if line_in[i] is not None:
                anim.append(line_in[i])
            if norms[i] is not None:
                anim.append(norms[i])
            if line_out[i] is not None:
                anim.append(line_out[i])
            anims.append(AnimationGroup(*anim))
        for i, anim in enumerate(anims):
            self.play(anim)
            if i == 0:
                self.wait()

        self.playw(Restore(x_m))
        x_normd = normalize(x, axis=2)
        x_norm_m = (
            VGroup(
                *[
                    VGroup(*[vector2matrix(v).scale(0.7) for v in x_normd[b]]).arrange(
                        RIGHT
                    )
                    for b in range(B)
                ]
            )
            .arrange(OUT, buff=4)
            .set_color(GREEN)
        )
        x_norm_m[1].shift(OUT)

        lines = [
            Line(
                x_m[b][l][0][0].get_center(),
                x_m[b][l][0][4].get_center(),
                color=GREEN,
                stroke_width=2,
            ).set_opacity(0.8 - b * 0.15)
            for b in range(B)
            for l in range(L)
        ]
        line_in = []
        norms = []
        line_out = []
        idx = 0
        x_m.save_state()
        for b in range(B):
            for l in range(L):
                line_in.append(FadeIn(lines[idx]))
                batch_axis = VGroup(*[x_m[b][l][0][i] for i in range(D)])
                target_axis = VGroup(*[x_norm_m[b][l][0][i] for i in range(D)])
                norms.append(Transform(batch_axis, target_axis))
                line_out.append(FadeOut(lines[idx]))
                idx += 1
        line_in.append(None)
        line_in.append(None)
        norms.insert(0, None)
        norms.append(None)
        line_out.insert(0, None)
        line_out.insert(0, None)
        anims = []
        for i in range(len(line_in)):
            anim = []
            if line_in[i] is not None:
                anim.append(line_in[i])
            if norms[i] is not None:
                anim.append(norms[i])
            if line_out[i] is not None:
                anim.append(line_out[i])
            anims.append(AnimationGroup(*anim))
        for i, anim in enumerate(anims):
            self.play(anim)
            if i == 0:
                self.wait()

class tensor2Axes(Scene3D):
    def construct(self):
        np.random.seed(41)
        tilt_degree = 65
        self.tilt_camera_horizontal(tilt_degree)

        B, L, D = 3, 4, 5
        x = np.random.randn(B, L, D)[..., None]
        x_norm = normalize(x, axis=(0, 1))
        x_m = VGroup(
            *[
                VGroup(*[vector2matrix(v).scale(0.7) for v in x[b]]).arrange(RIGHT)
                for b in range(B)
            ]
        ).arrange(OUT, buff=4)
        BLDt = (
            Text("[B, L, D]", font_size=36, color=GREY_B)
            .rotate(-tilt_degree * DEGREES, UP)
            .shift(UP * 3)
        )
        x_m[1].shift(OUT)
        self.playw(FadeIn(x_m, BLDt))

        x_norm_m = (
            VGroup(
                *[
                    VGroup(*[vector2matrix(v).scale(0.7) for v in x_norm[b]]).arrange(
                        RIGHT
                    )
                    for b in range(B)
                ]
            )
            .arrange(OUT, buff=4)
            .set_color(GREEN)
        )
        x_norm_m[1].shift(OUT)

        polygons = []
        for d in range(D):
            polygon = Polygon(
                x_m[0][0][0][d].get_center(),
                x_m[0][3][0][d].get_center(),
                x_m[2][3][0][d].get_center(),
                x_m[2][0][0][d].get_center(),
                color=GREEN,
                stroke_width=2,
            ).set_opacity(0.3)
            polygons.append(polygon)
        
        polygon_in = []
        norms = []
        polygon_out = []
        idx = 0
        x_m.save_state()
        for polygon in polygons:
            polygon_in.append(FadeIn(polygon))
            batch_axis = VGroup(*[x_m[b][l][0][idx] for b in range(B) for l in range(L)])
            target_axis = VGroup(*[x_norm_m[b][l][0][idx] for b in range(B) for l in range(L)])
            norms.append(Transform(batch_axis, target_axis))
            polygon_out.append(FadeOut(polygon))
            idx += 1
        polygon_in.append(None)
        polygon_in.append(None)
        norms.insert(0, None)
        norms.append(None)
        polygon_out.insert(0, None)
        polygon_out.insert(0, None)
        anims = []
        for i in range(len(polygon_in)):
            anim = []
            if polygon_in[i] is not None:
                anim.append(polygon_in[i])
            if norms[i] is not None:
                anim.append(norms[i])
            if polygon_out[i] is not None:
                anim.append(polygon_out[i])
            anims.append(AnimationGroup(*anim))
        for i, anim in enumerate(anims):
            self.play(anim)
            if i == 0:
                self.wait()

        self.playw(Restore(x_m))

        x_norm = normalize(x, axis=(0, 2))

        x_norm_m = (
            VGroup(
                *[
                    VGroup(*[vector2matrix(v).scale(0.7) for v in x_norm[b]]).arrange(
                        RIGHT
                    )
                    for b in range(B)
                ]
            )
            .arrange(OUT, buff=4)
            .set_color(GREEN)
        )
        x_norm_m[1].shift(OUT)

        polygons = []
        for l in range(L):
            polygon = Polygon(
                x_m[0][l][0][0].get_center(),
                x_m[0][l][0][4].get_center(),
                x_m[2][l][0][4].get_center(),
                x_m[2][l][0][0].get_center(),
                color=GREEN,
                stroke_width=2,
            ).set_opacity(0.3)
            polygons.append(polygon)

        polygon_in = []
        norms = []
        polygon_out = []
        idx = 0
        x_m.save_state()
        for polygon in polygons:
            polygon_in.append(FadeIn(polygon))
            batch_axis = VGroup(*[x_m[b][idx][0][d] for b in range(B) for d in range(D)])
            target_axis = VGroup(*[x_norm_m[b][idx][0][d] for b in range(B) for d in range(D)])
            norms.append(Transform(batch_axis, target_axis))
            polygon_out.append(FadeOut(polygon))
            idx += 1
        polygon_in.append(None)
        polygon_in.append(None)
        norms.insert(0, None)
        norms.append(None)
        polygon_out.insert(0, None)
        polygon_out.insert(0, None)
        anims = []
        for i in range(len(polygon_in)):
            anim = []
            if polygon_in[i] is not None:
                anim.append(polygon_in[i])
            if norms[i] is not None:
                anim.append(norms[i])
            if polygon_out[i] is not None:
                anim.append(polygon_out[i])
            anims.append(AnimationGroup(*anim))
        for i, anim in enumerate(anims):
            self.play(anim)
            if i == 0:
                self.wait()
        