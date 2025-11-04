from manim import *
from raenim import *
from random import seed

from torchvision.datasets import MNIST
import torchvision
import torch

data = MNIST(
    root="media/data", download=True, transform=torchvision.transforms.ToTensor()
)

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        sentence = Words(
            "We use exponential moving averages in our model.",
            font="Noto Sans KR",
            font_size=36,
            color=GREY_B,
        )
        sentence.words[2:5].set_color(GREEN)
        self.playwl(*[FadeIn(word) for word in sentence.words], lag_ratio=0.1, wait=0.5)
        self.playw(
            ApplyWave(sentence.words[2:5]),
            VGroup(sentence.words[:2], sentence.words[5:]).animate.set_color(GREY_D),
        )
        ema = sentence.words[2:5]
        num_list = [10, 18, 13, 24, 28, 20, 35, 40, 32, 45]
        nums = VGroup(
            *[
                DecimalNumber(num, font_size=36, color=GREY_B, num_decimal_places=0)
                for num in num_list
            ]
        )

        def _join():
            _j = Text(",..", font_size=24)
            _j[1:].set_opacity(0)
            return _j

        nums = Joiner(*nums, join=_join).arrange(RIGHT, aligned_edge=DOWN, buff=0.1)
        self.playw(
            ema.animate.move_to(ORIGIN).to_edge(UP, buff=0.5),
            VGroup(sentence.words[:2], sentence.words[5:])
            .animate.move_to(ORIGIN)
            .to_edge(UP, buff=0.5)
            .set_opacity(0),
            FadeIn(nums, shift=UP),
            wait=0.5,
        )

        nump = NumberPlane(
            x_range=[0, len(num_list) + 1, 1],
            y_range=[0, 50, 5],
            x_length=13,
            y_length=6,
            axis_config={"font_size": 24, "color": GREY_B},
            background_line_style={"stroke_opacity": 0.2},
        ).scale(0.7)
        num_dots = VGroup(
            *[
                Dot(
                    nump.c2p(i + 1, num_list[i]),
                    color=GREY_B,
                    radius=0.04,
                )
                for i in range(len(num_list))
            ]
        )
        num_lines = VGroup()
        for i in range(1, len(num_list)):
            line = Line(
                nump.c2p(i, num_list[i - 1]),
                nump.c2p(i + 1, num_list[i]),
                color=GREY_B,
                stroke_width=2,
            )
            num_lines.add(line)
        num_graph = VGroup(num_lines, num_dots)
        nums, commas = nums[0::2], nums[1::2]
        nums.generate_target()
        for i, n in enumerate(nums):
            nums.target[i].scale(0.85).move_to(nump.c2p(i + 1, num_list[i]) + UP * 0.3)
        self.playw(FadeIn(nump, num_graph), MoveToTarget(nums), FadeOut(commas))

        ema_nums_list = []
        alpha = 0.4
        for i, num in enumerate(num_list):
            if i == 0:
                ema_num = num
            else:
                ema_num = alpha * num + (1 - alpha) * ema_nums_list[-1]
            ema_nums_list.append(ema_num)
        ema_nums = VGroup(
            *[
                DecimalNumber(
                    num,
                    font_size=36,
                    color=GREEN,
                    num_decimal_places=1,
                )
                .scale(0.85)
                .move_to(nump.c2p(i + 1, ema_nums_list[i]) + DOWN * 0.3)
                for i, num in enumerate(ema_nums_list)
            ]
        )
        ema_dots = VGroup(
            *[
                Dot(
                    nump.c2p(i + 1, ema_nums_list[i]),
                    color=GREEN,
                    radius=0.06,
                )
                for i in range(len(ema_nums_list))
            ]
        )
        ema_lines = BrokenLine(
            *[nump.c2p(i + 1, ema_nums_list[i]) for i in range(len(ema_nums_list))],
            color=GREEN,
        )
        ema_lines.set_color(GREEN).set_stroke(width=3)
        self.playw(
            Create(ema_lines, run_time=2),
            AnimationGroup(*[FadeIn(dot) for dot in ema_dots], lag_ratio=0.13),
            AnimationGroup(*[FadeIn(num) for num in ema_nums], lag_ratio=0.13),
            wait=2,
        )

        get_model_box = lambda: Rectangle(
            height=6.0, width=4.6, stroke_width=3, color=GREY_B
        )
        model_box = get_model_box()
        model_box.next_to(nump, RIGHT, buff=10)
        get_module = lambda: Rectangle(
            height=1.2, width=3.3, stroke_width=2, color=YELLOW_B
        )
        get_modulet = lambda: Text(
            "nn.Linear", font_size=24, font=MONO_FONT, color=YELLOW_A
        )
        mlp = (
            VGroup(
                *[
                    VGroup((_m := get_module()), get_modulet().move_to(_m))
                    for _ in range(3)
                ]
            )
            .arrange(DOWN, buff=0.7)
            .move_to(model_box)
        )
        self.add(model_box, mlp)
        self.playw(self.cf.animate.move_to(model_box).shift(DOWN * 0.5))

        def get_wb():
            weight = Mat.randn(4, 4)
            bias = Mat.randn(4, 1)

            wb = VGroup(weight, bias).arrange(RIGHT, buff=0.5)
            return wb

        wbs = VGroup(
            *[get_wb().scale(0.5).move_to(mlp[i]).set_color(YELLOW_A) for i in range(3)]
        )
        self.playw(*[FadeTransform(mlp[i], wbs[i]) for i in range(3)])

        self.playw(
            wbs.animate.set_color(YELLOW_B).scale(1.05),
            model_box.animate.become(
                get_model_box().move_to(model_box).scale(1.1).set_color(GREY_E)
            ),
        )
        numbers = VGroup(
            *wbs[0][0][0],
            *wbs[0][1][0],
            *wbs[1][0][0],
            *wbs[1][1][0],
            *wbs[2][0][0],
            *wbs[2][1][0],
        )
        self.playwl(
            *[Indicate(num, scale_factor=1.1) for num in numbers], lag_ratio=0.02
        )

        model = VGroup(model_box, wbs)
        tilt_angle = PI / 3
        self.play(
            model.animate.rotate(tilt_angle, axis=UP),
            self.cf.animate.shift(OUT * 5 + DOWN * 0.6 + RIGHT * 5),
        )

        line = Arrow(
            model.get_bottom() + DOWN * 0.7,
            model.get_bottom() + DOWN * 0.7 + RIGHT * 12,
            color=GREY_B,
            buff=0,
            stroke_width=2,
            tip_length=0.2,
        )
        traint = Text("training...", font_size=24, color=GREY_B).next_to(
            line.get_start(), DOWN, buff=0.1
        )
        self.playw(GrowArrow(line), FadeIn(traint))

        def get_model():
            box = (
                get_model_box().scale(1.1).set_color(GREY_E).set_fill(BLACK, opacity=1)
            )
            wbs = VGroup(
                *[
                    get_wb().scale(0.5 * 1.05).move_to(mlp[i]).set_color(YELLOW_B)
                    for i in range(3)
                ]
            ).move_to(box)
            return VGroup(box, wbs)

        models = (
            VGroup(
                *[
                    get_model()
                    .rotate(tilt_angle * (1.1 - 0.05 * i), axis=UP)
                    .set_z_index(i)
                    for i in range(1, 7 + 1)
                ]
            )
            .arrange(RIGHT, buff=-0.8)
            .next_to(model, RIGHT, buff=-0.8)
        )
        for i, m in enumerate(models):
            if i:
                m.next_to(models[i - 1], RIGHT, buff=-0.8 - 0.15 * i)
        models = VGroup(model, *models)
        modelsc = VGroup(models[0].set_z_index(-1))
        for i, (m, _m) in enumerate(zip(models, models[1:])):
            mc = m.copy()
            self.play(mc.animate.become(_m))
            modelsc.add(mc.set_z_index(i))
        self.wait()

        models_num0 = VGroup(*[modelsc[i][1][0][0][0][0] for i in range(len(modelsc))])
        models_num_ = VGroup(
            *[
                VGroup(
                    modelsc[i][1][0][0][0][1:],
                    modelsc[i][1][0][1][0],
                    modelsc[i][1][1][0][0],
                    modelsc[i][1][1][1][0],
                    modelsc[i][1][2][0][0],
                    modelsc[i][1][2][1][0],
                )
                for i in range(len(modelsc))
            ]
        )
        self.playw(
            *[item.animate.scale(1.2).set_color(YELLOW) for item in models_num0],
            models_num_.animate.set_opacity(0.3),
        )
        line_ = line.copy().set_color(YELLOW)
        trained = Text("trained!", font_size=24, color=YELLOW).next_to(
            line_.get_end(), DOWN, buff=0.1
        )
        self.play(Create(line_))
        self.playw(FadeIn(trained))

        def get_models_numi(i):
            models_numi = VGroup(
                *[modelsc[j][1][0][0][0][i] for j in range(len(modelsc))],
                *[modelsc[j][1][1][0][0][i] for j in range(len(modelsc))],
                *[modelsc[j][1][2][0][0][i] for j in range(len(modelsc))],
            )
            return models_numi

        self.playwl(
            *[
                AnimationGroup(
                    *[
                        Transform(
                            item,
                            item.copy().set_opacity(1).set_z_index(item.get_z_index()),
                            rate_func=there_and_back,
                        )
                        for item in get_models_numi(i)
                    ]
                )
                for i in range(1, len(modelsc[0][1][0][0][0]))
            ]
        )


class ema_naive(Scene3D):
    def construct(self):
        fs = 36

        def ema_term_naive(i):
            if i == 0:
                return MathTex(r"\alpha \cdot", r"x_T", font_size=fs)
            if i == 1:
                return MathTex(r"\alpha (1 - \alpha) \cdot", r"x_{T-1}", font_size=fs)
            else:
                return MathTex(
                    rf"\alpha (1 - \alpha)^{{{i}}} \cdot",
                    r"x_{T-" + str(i) + r"}",
                    font_size=fs,
                )

        terms = Joiner(
            *[ema_term_naive(i) for i in range(5)],
            Text("...", font_size=fs, color=GREY_B),
            join=lambda: MathTex("+", font_size=fs),
        ).arrange(RIGHT, buff=0.1)
        coeffs = VGroup(*[term[0] for term in terms[0:-1:2]], terms[-1])
        rest = VGroup(*[term[1] for term in terms[0:-1:2]], *terms[1::2])
        self.playwl(*[FadeIn(term) for term in terms], lag_ratio=0.1)
        get_model_box = lambda: Rectangle(
            height=6.0, width=4.6, stroke_width=3, color=GREY_E
        )

        def get_wb():
            weight = Mat.randn(4, 4)
            bias = Mat.randn(4, 1)

            wb = VGroup(weight, bias).arrange(RIGHT, buff=0.5)
            return wb

        def get_model():
            box = (
                get_model_box().scale(1.1).set_color(GREY_E).set_fill(BLACK, opacity=1)
            )
            wbs_ = (
                VGroup(
                    *[get_wb().scale(0.5 * 1.05).set_color(YELLOW_B) for i in range(3)]
                )
                .arrange(DOWN)
                .move_to(box)
            )
            return VGroup(box, wbs_)

        models = (
            VGroup(get_model().set_z_index(-i) for i in range(20))
            .arrange(IN, buff=1.2)
            .align_to(ORIGIN, OUT)
        )
        models.generate_target().shift(OUT * 5)
        arrow = (
            Arrow(
                models[-1].get_right() + RIGHT,
                models[0].get_right() + RIGHT,
                color=GREY_B,
                buff=0,
                stroke_width=2,
                tip_length=0.2,
            )
            .set_opacity(0)
            .set_z_index(-100)
        )
        arrow.generate_target().set_opacity(1)
        arrow.target.put_start_and_end_on(
            models[-1].get_right() + RIGHT + OUT * 5,
            models[0].get_right() + RIGHT + OUT * 5,
        )
        self.playw(
            FadeIn(models, arrow),
            *[
                coeffs[i]
                .animate.next_to(models[i], LEFT, buff=1)
                .align_to(models[i], UP)
                .shift(DOWN * i * 0.5)
                for i in range(len(coeffs))
            ],
            FadeOut(rest),
        )
        coeffs.generate_target().set_color(RED)
        for i in range(len(coeffs)):
            coeffs.target[i].rotate(-PI / 4, RIGHT).next_to(
                models.target[i], LEFT, buff=1
            ).align_to(models[i], UP)
        coeffs.target[-1].rotate(PI / 2, UP)
        self.move_camera_vertically(
            -45,
            zoom=0.5,
            added_anims=[
                MoveToTarget(models),
                MoveToTarget(arrow),
                MoveToTarget(coeffs),
            ],
        )

        self.wait(2)

        terms_following = VGroup()
        for i in range(5, 15):
            term = ema_term_naive(i)[0].set_color(RED)
            term.next_to(models[i], LEFT, buff=1).align_to(models[i], UP)
            term.rotate(-PI / 4, RIGHT)
            terms_following.add(term)
        self.playwl(
            FadeOut(coeffs[-1]),
            *[FadeIn(term) for term in terms_following],
            lag_ratio=0.1,
        )

        model_size_text = lambda: Text("300MB", font_size=36, color=RED)
        model_sizes = VGroup()
        for i in range(len(models)):
            size_text = model_size_text()
            size_text.next_to(models[i], RIGHT, buff=1).align_to(models[i], UP)
            model_sizes.add(size_text)
        self.playw(FadeOut(arrow), FadeIn(model_sizes[0]))
        self.playwl(
            *[FadeIn(model_sizes[i]) for i in range(1, len(models))], lag_ratio=0.1
        )


class ema_online(Scene2D):
    def construct(self):
        text = Words("Online update", font_size=36).set_color_by_gradient(
            BLUE_A, BLUE_C
        )
        self.playw(FadeIn(text))

        fs = 48

        def ema_term_online(i):
            if i == 0:
                return MathTex(r"w_{\mathrm{latest}}", "=", r"w_T", font_size=int(fs))
            else:
                return MathTex(
                    r"w_{\mathrm{latest}}",
                    "=",
                    r"\alpha \cdot",
                    r"w_T",
                    r"+",
                    r"(1 - \alpha) \cdot",
                    r"w_{\mathrm{latest}}",
                    font_size=fs,
                )

        terms = VGroup(ema_term_online(0))
        self.playw(FadeOut(text, shift=UP), FadeIn(terms[0], shift=UP))

        terms.add(ema_term_online(1))
        self.playw(terms[0].animate.shift(UP), FadeIn(terms[1], shift=UP))

        self.play(
            terms.animate.scale(0.7)
            .set_color(GREY_B)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .to_corner(UL, buff=0.5)
        )

        def ema_term_naive(i):
            def get_coeff(i, first):
                if i == 0:
                    return r"\alpha \cdot"
                elif i == 1:
                    return r"\alpha (1 - \alpha) \cdot"
                else:
                    return (
                        rf"(1 - \alpha)^{{{i}}} \cdot"
                        if first
                        else rf"\alpha (1 - \alpha)^{{{i}}} \cdot"
                    )

            coeffs = [
                MathTex(get_coeff(j, j == i), font_size=fs) for j in range(1, i + 1)
            ]
            ws = [
                MathTex(r"w_{" + str(i - j) + r"}", font_size=fs)
                for j in range(1, i + 1)
            ]
            terms = [
                VGroup(*[coeffs[i], ws[i]]).arrange(RIGHT, aligned_edge=DOWN, buff=0.05)
                for i in range(len(coeffs))
            ]
            terms_join = Joiner(
                *terms,
                join=lambda: MathTex("+", font_size=fs),
            ).arrange(RIGHT, buff=0.1)
            return terms_join

        def ema_term_i(i):
            if i == 0:
                return MathTex(r"w^{\mathrm{EMA}}_0", "=", r"w_0", font_size=fs)
            else:
                return MathTex(
                    r"w^{\mathrm{EMA}}_{" + str(i) + r"}",
                    "=",
                    r"\alpha \cdot",
                    rf"w_{i}",
                    r"+",
                    r"(1 - \alpha) \cdot",
                    r"w^{\mathrm{EMA}}_{" + str(i - 1) + r"}",
                    font_size=fs,
                )

        ema0 = ema_term_i(0)
        self.playw(FadeIn(ema0))
        ema1 = ema_term_i(1)

        ema0.generate_target().shift(UP).align_to(ema1[-1], LEFT)
        ema0.target[0].set_color(RED)
        ema1[-1].set_color(RED)
        self.play(MoveToTarget(ema0), FadeIn(ema1, shift=UP))
        self.playw(
            ema0[-1].animate.align_to(ema1[-1], DOWN).align_to(ema1[-1], LEFT),
            FadeOut(ema0[:-1]),
            ema1[-1].animate.set_opacity(0),
        )
        ema1 = VGroup(*ema1, ema0[-1])

        ema2 = ema_term_i(2)
        ema1.generate_target().shift(UP).align_to(ema2[-1], LEFT)
        ema1.target[0].set_color(RED)
        ema2[-1].set_color(RED)
        self.play(
            self.cf.animate.scale(1.2).align_to(self.cf, LEFT).align_to(self.cf, UP),
            MoveToTarget(ema1),
            FadeIn(ema2, shift=UP),
        )
        self.play(
            ema1[2:].animate.align_to(ema2[-1], DOWN).align_to(ema2[-1], LEFT),
            FadeOut(ema1[:2]),
            ema2[-1].animate.set_opacity(0),
        )
        ema2 = VGroup(*ema2, ema1[2:])
        _par = VGroup(
            Text("(", font_size=fs * 0.7), Text(")", font_size=fs * 0.7)
        ).set_color(YELLOW)
        _par[0].next_to(ema1[2:], LEFT, buff=0.03)
        _par[1].next_to(ema1[-1], RIGHT, buff=0.05).align_to(_par[0], DOWN)
        self.playw(FadeIn(_par))
        eman2 = ema_term_naive(2).align_to(ema2[-3:], LEFT)
        self.playw(FadeTransform(VGroup(ema2[-3:], _par), eman2))

        ema3 = ema_term_i(3)
        ema2 = VGroup(*ema2[:-3], *eman2)
        ema2.generate_target().shift(UP).align_to(ema3[-1], LEFT)
        ema2.target[0].set_color(RED)
        ema3[-1].set_color(RED)
        self.play(
            self.cf.animate.scale(1.15).align_to(self.cf, LEFT).align_to(self.cf, UP),
            MoveToTarget(ema2),
            FadeIn(ema3, shift=UP),
        )
        self.play(
            ema2[2:].animate.align_to(ema3[-1], DOWN).align_to(ema3[-1], LEFT),
            FadeOut(ema2[:2]),
            ema3[-1].animate.set_opacity(0),
        )
        ema3 = VGroup(*ema3, ema2[2:])
        _par = VGroup(
            Text("(", font_size=fs * 0.7), Text(")", font_size=fs * 0.7)
        ).set_color(YELLOW)
        _par[0].next_to(ema2[2:], LEFT, buff=0.03)
        _par[1].next_to(ema2[-1], RIGHT, buff=0.05).align_to(_par[0], DOWN)
        self.playw(FadeIn(_par))
        eman3 = ema_term_naive(3).align_to(ema3[-4:], LEFT)
        self.playw(FadeTransform(VGroup(ema3[-4:], _par), eman3))


class model_online(Scene3D):
    def construct(self):
        def get_wb():
            weight = Mat.randn(4, 4)
            bias = Mat.randn(4, 1)

            wb = VGroup(weight, bias).arrange(RIGHT, buff=0.5)
            return wb

        def model_box():
            box = Rectangle(
                height=6.0, width=4.6, stroke_width=3, color=GREY_E
            ).set_fill(BLACK, opacity=1)
            wbs_ = (
                VGroup(
                    *[get_wb().scale(0.5 * 1.05).set_color(YELLOW_B) for i in range(3)]
                )
                .arrange(DOWN)
                .move_to(box)
            )
            return VGroup(box, wbs_)

        models = (
            VGroup(*[model_box().set_z_index(-i) for i in range(10)])
            .arrange(IN, buff=1.2)
            .align_to(ORIGIN, OUT)
        )
        models[:-1].set_opacity(0)
        models.generate_target().shift(OUT * 3)
        arrow = Arrow(
            models[-1].get_right() + RIGHT + IN * 5,
            models[0].get_right() + RIGHT,
            color=GREY_B,
            buff=0,
            stroke_width=2,
            tip_length=0.2,
        ).set_opacity(0)
        arrow.generate_target().set_opacity(1)
        arrow.target.put_start_and_end_on(
            models[-1].get_right() + RIGHT + IN * 2,
            models[0].get_right() + RIGHT + OUT * 3,
        )
        self.playw(FadeIn(models), FadeIn(arrow))
        self.move_camera_vertically(
            -45,
            zoom=0.5,
            added_anims=[
                MoveToTarget(models),
                MoveToTarget(arrow),
            ],
        )
        ema_model = models[-1].copy()
        ema_modelt = Text("EMA", font_size=24, color=GREEN)
        self.play(ema_model.animate.next_to(models[-1], LEFT, buff=2))
        ema_model_coeff = (
            Text("(1-α) ·", font_size=48, color=GREEN)
            .next_to(ema_model, LEFT, buff=0.1)
            .set_opacity(0)
        )
        ema_modelt.next_to(ema_model, LEFT, buff=0.1).align_to(
            ema_model, UP
        ).set_opacity(0)

        model = models[-1]
        modelt = (
            Text("Model", font_size=24, color=YELLOW_B)
            .next_to(model, UP, buff=0.1)
            .align_to(model, RIGHT)
            .set_opacity(0)
        )
        model_coeff = (
            Text("α ·", font_size=48, color=YELLOW_B)
            .next_to(model, LEFT, buff=0.1)
            .set_opacity(0)
        )
        self.playw(
            ema_modelt.animate.set_opacity(1),
            modelt.animate.set_opacity(1),
            model_coeff.animate.set_opacity(1),
            ema_model_coeff.animate.set_opacity(1),
        )
        ema_modelt.add_updater(
            lambda m: m.next_to(ema_model, LEFT, buff=0.1).align_to(ema_model, UP)
        )
        modelt.add_updater(
            lambda m: m.next_to(model, UP, buff=0.1).align_to(model, RIGHT)
        )
        model_coeff.add_updater(lambda m: m.next_to(model, LEFT, buff=0.1))
        ema_model_coeff.add_updater(lambda m: m.next_to(ema_model, LEFT, buff=0.1))

        for i in range(len(models) - 2, -1, -1):
            model_ = models[i].copy().set_opacity(1)
            self.play(model.animate.become(model_))
            ema_model_ = model_box().next_to(model_, LEFT, buff=2)
            self.play(
                ema_model.animate.become(ema_model_),
                model.copy().animate.move_to(ema_model_).set_opacity(0),
            )
        self.wait(2)


class ema_effect(Scene3D):
    def construct(self):
        def model_box():
            box = Rectangle(
                height=4.0, width=4.6, stroke_width=3, color=GREY_E
            ).set_fill(BLACK, opacity=0.9)
            text = Text(
                "Generative Model",
                font_size=24,
                color=interpolate_color(YELLOW_B, GREY_E, 0.5),
            ).move_to(box)
            return VGroup(box, text).set_z_index(200)

        model = model_box().shift(UP * 0.5)
        self.playw(FadeIn(model))
        global data
        noise = torch.rand_like(data[0][0]) * 255
        out = data[0][0] * 255
        noise = PixelImage(noise.permute(1, 2, 0).repeat(1, 1, 3).numpy()).scale(0.3)
        out = (
            PixelImage(out.permute(1, 2, 0).repeat(1, 1, 3).numpy())
            .scale(0.3)
            .next_to(model, RIGHT, buff=1)
        )
        label = Text("5", font_size=48, color=GREY_B)
        model_in = (
            VGroup(noise, label).arrange(DOWN, buff=0.75).next_to(model, LEFT, buff=1)
        )
        self.playw(FadeIn(model_in))

        noise_path = BrokenLine(
            noise.get_center(), model.get_center(), out.get_center()
        )
        label_path = BrokenLine(
            label.get_center(), model.get_center(), out.get_center()
        )
        self.play(
            MoveAlongPath(noise, noise_path, run_time=2),
            MoveAlongPath(label, label_path, run_time=2),
            wait=0.5,
        )
        self.playw(Transform(noise, out), FadeOut(label, scale=1.2))

        self.playw(FadeOut(noise))

        noises = Group(
            *[
                ImageMobject(
                    (torch.randn_like(data[i][0].permute(1, 2, 0)) * 255)
                    .repeat(1, 1, 3)
                    .numpy()
                ).scale(2)
                for i in range(4)
            ]
        ).arrange(DR, buff=-0.2)
        outs = (
            Group(
                *[
                    ImageMobject(
                        (data[i][0].permute(1, 2, 0) * 255).repeat(1, 1, 3).numpy()
                    ).scale(2)
                    for i in range(4)
                ]
            )
            .arrange(DR, buff=-0.2)
            .next_to(model, RIGHT, buff=1)
        )
        nums = VGroup(
            *[
                Text(str(data[i][1]), font_size=36, color=GREY_B)
                .next_to(noises[i], DOWN, buff=0.1)
                .set_z_index(1)
                for i in range(4)
            ]
        ).arrange(DR + RIGHT, buff=-0.0)
        model_in = (
            Group(noises, nums).arrange(DOWN, buff=0.75).next_to(model, LEFT, buff=1)
        )
        self.playwl(*[FadeIn(noises[i], nums[i]) for i in range(4)], lag_ratio=0.6)

        noise_path = BrokenLine(
            noises.get_center(), model.get_center(), outs.get_center()
        )
        nums_path = BrokenLine(nums.get_center(), model.get_center(), outs.get_center())
        self.play(
            MoveAlongPath(noises, noise_path),
            MoveAlongPath(nums, nums_path),
            wait=0.5,
        )
        self.playw(
            *[Transform(noises[i], outs[i]) for i in range(4)],
            *[FadeOut(nums[i], scale=1.2) for i in range(4)],
        )

        self.playw(Wiggle(model[1]))

        datas = (
            Group(
                *[
                    ImageMobject(
                        (data[i][0].permute(1, 2, 0) * 255).repeat(1, 1, 3).numpy()
                    ).scale(2)
                    for i in range(8, 20)
                ]
            )
            .arrange(DR, buff=-0.2)
            .next_to(outs, DR, buff=-0.2)
        )
        self.playwl(*[FadeIn(datas[i]) for i in range(len(datas))], lag_ratio=0.3)

        self.play(noises.animate.shift(UP))

        out_rect = SurroundingRectangle(
            noises, color=YELLOW_B, stroke_width=2, buff=0.1
        )
        self.playw(Create(out_rect))

        backprop = Arrow(
            out_rect.get_left(),
            model.get_right(),
            buff=0.05,
            stroke_width=2,
            tip_length=0.15,
            color=YELLOW_C,
        )
        self.playw(FadeIn(backprop))
        self.playw_return(model[0].animate.set_stroke(width=2, color=YELLOW))
        self.playw(model[0].animate.set_stroke(width=2, color=RED))

        datat = (
            Text("Data", font_size=36, color=GREY_B)
            .next_to(model, RIGHT, buff=1.5)
            .rotate(-PI / 4, axis=RIGHT)
        )
        datas.generate_target().arrange(OUT, buff=0.2).next_to(
            model, RIGHT, buff=1
        ).align_to(model, IN)
        datas_ = (
            Group(
                *[
                    ImageMobject(
                        (data[i][0].permute(1, 2, 0) * 255).repeat(1, 1, 3).numpy()
                    ).scale(2)
                    for i in range(20, 48)
                ]
            )
            .arrange(OUT, buff=0.2)
            .next_to(datas.target, OUT, buff=0.2)
        )
        ema_model = model_box().next_to(model, LEFT, buff=2)
        ema_modelt = (
            Text("EMA", font_size=24, color=GREEN)
            .next_to(ema_model, LEFT, buff=0.1)
            .align_to(ema_model, UP)
        )

        self.move_camera_vertically(
            -45,
            zoom=0.6,
            added_anims=[
                datas.animate.arrange(OUT, buff=0.2)
                .next_to(model, RIGHT, buff=1)
                .align_to(model, IN),
                FadeOut(backprop, noises, out_rect),
                FadeIn(ema_model, ema_modelt),
            ],
            wait=0.1
        )
        self.playw(FadeIn(datat, datas_))


        ema_modelt.add_updater(
            lambda m: m.next_to(ema_model, LEFT, buff=0.1).align_to(ema_model, UP)
        )
        data = Group(*datas, *datas_)

        for i in range(3):
            model.generate_target().shift(OUT)
            model.target[0].set_stroke(width=2, color=random_color())
            self.play(MoveToTarget(model), FadeOut(data[i*8+0:i*8+8], shift=LEFT * 3))
            ema_model.generate_target().next_to(model, LEFT, buff=2)
            ema_model.target[0].set_stroke(
                width=2, color=interpolate_color(random_color(), BLACK, 0.6)
            )
            self.play(
                MoveToTarget(ema_model),
                FadeOut(model.copy(), shift=LEFT * 3),
            )
        self.wait(2)