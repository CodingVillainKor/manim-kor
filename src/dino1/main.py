from manim import *
from raenim import *
from random import seed
from PIL import Image

seed(41)
np.random.seed(41)


def chatgpt():
    img = ImageMobject("media/chatgpt.png")
    return img


class pretrain(Scene3D):
    def construct(self):
        text = Text("Pretrain", font_size=36).set_color_by_gradient(BLUE_A, BLUE)
        self.playw(FadeIn(text), run_time=0.5)

        icon = chatgpt().next_to(text, DOWN, buff=0.5)
        self.playw(FadeIn(icon, shift=DOWN * 0.5), run_time=0.5)

        self.move_camera_vertically(
            45, added_anims=[icon.animate.shift(DOWN), FadeOut(text)]
        )
        with open("media/textwiki.txt", "r") as f:
            wiki_text = f.read().split("\n")
        par = (
            VGroup(
                *[
                    Words(line, font_size=28, font="Noto Sans KR", color=GREY_B)
                    for line in wiki_text
                ]
            )
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            .next_to(icon, DOWN, buff=2.2)
            .set_z_index(-1)
        )
        par = VGroup(*[word for item in par for word in item.words])
        self.addw(par)
        self.playw(par.animate.next_to(icon, UP, buff=0.5), run_time=8)

        target = -16
        pre_in = par[:target].copy().set_opacity(0.8)
        pre_out = par[target]
        self.playwl(
            *[
                Succession(
                    pre_in[i].animate.move_to(icon).set_opacity(1), FadeOut(pre_in[i])
                )
                for i in range(len(pre_in))
            ],
            run_time=8,
            wait=0.1,
        )
        arr = Arrow(
            icon.get_top(),
            pre_out.get_bottom(),
            buff=0.1,
            color=YELLOW_B,
            tip_length=0.2,
            stroke_width=3,
        )
        self.playw(
            GrowArrow(arr),
            par[:target].animate.set_opacity(0.5),
            par[target + 1 :].animate.set_opacity(0.5),
            par[target].animate.set_color(YELLOW),
            run_time=0.5,
        )


from torchvision.datasets import MNIST

data = MNIST(root="media/mnist", download=True)


def data_pair(idx):
    img, label = data[idx]
    img = np.array(img)
    img_mob = ImageMobject(img).scale(3)
    label_mob = Text(str(label), font_size=28).set_color_by_gradient(RED, ORANGE)

    return Group(img_mob, label_mob).arrange(RIGHT, buff=1.2)


class supervised(Scene2D):
    def construct(self):
        xy = Group(*[data_pair(i) for i in range(5)]).arrange(DOWN, buff=0.35)
        self.playw(FadeIn(xy))
        xs = Group(*[pair[0] for pair in xy])
        ys = Group(*[pair[1] for pair in xy])

        xtext = (
            Text("Data", font_size=24)
            .set_color_by_gradient(BLUE_A, BLUE)
            .next_to(xs, UP)
        )
        ytext = (
            Text("Label", font_size=24)
            .set_color_by_gradient(RED_A, RED)
            .next_to(ys, UP)
            .align_to(xtext, UP)
        )
        self.playwl(FadeIn(xtext), FadeIn(ytext), lag_ratio=0.5)

        self.play(
            Group(xs, xtext).animate.shift(LEFT * 2),
            Group(ys, ytext).animate.shift(RIGHT * 2),
        )
        model = (
            Rectangle(width=3, height=5, color=YELLOW_B)
            .set_fill(BLACK, opacity=0.85)
            .set_z_index(1)
        )
        modelt = (
            Text("Model", font_size=32)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .move_to(model)
        ).set_z_index(2)
        self.playwl(GrowFromCenter(model), FadeIn(modelt), lag_ratio=0.3)

        arrows = VGroup(
            *[
                DashedVMobject(
                    Arrow(
                        start=xs[i].get_right(),
                        end=ys[i].get_left(),
                        buff=0.1,
                        color=YELLOW_B,
                        tip_length=0.15,
                        stroke_width=3,
                    ),
                    num_dashes=30,
                    dashed_ratio=0.6,
                )
                for i in range(len(xs))
            ]
        )
        self.playwl(*[GrowFromEdge(arrow, LEFT) for arrow in arrows], lag_ratio=0.1)

        self.playwl(*[Flash(x.get_corner(UL)) for x in xs], lag_ratio=0.2, wait=0.2)
        self.playwl(*[Flash(y.get_corner(UL)) for y in ys], lag_ratio=0.2)

        slt = (
            Words("Supervised Learning", font_size=32)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .next_to(model, UP, buff=0.5)
            .set_z_index(12)
        )
        shade_line = (
            Line(
                # start=ORIGIN,
                # end=[3*np.cos(2*PI*i/10),3*np.sin(2*PI*i/10),0],
                start=self.cf.get_corner(UP),
                end=DOWN * 3,
                stroke_color=BLACK,
                stroke_opacity=[1, 0],
                stroke_width=8000,
            )
            .set_sheen_direction(DOWN)
            .set_z_index(10)
        )
        self.playwl(
            FadeIn(shade_line), *[FadeIn(item) for item in slt.words], lag_ratio=0.3
        )

        self.playw(FadeOut(shade_line))
        self.playwl(*[Wiggle(x) for x in xs], lag_ratio=0.2)
        self.playwl(*[Wiggle(y) for y in ys], lag_ratio=0.2)

        qa_data_list = [
            [
                "What is piui?",
                "Piui is a sound of birds chirping",
            ],
            [
                "What is the capital of France?",
                "The capital of France is Paris.",
            ],
            [
                "Who is Albert Einstein?",
                "Albert Einstein was a theoretical physicist.",
            ],
            [
                "Where is the Busan?",
                "Busan is a city in South Korea.",
            ],
            [
                "How many continents are there?",
                "There are seven continents on Earth.",
            ],
        ]
        qa_data = VGroup(
            *[
                VGroup(
                    Words(
                        qa_data_list[i][0],
                        font_size=16,
                        font="Noto Sans KR",
                        color=GREY_B,
                    )
                    .move_to(xs[i])
                    .align_to(xs[i], RIGHT),
                    Words(
                        qa_data_list[i][1],
                        font_size=15,
                        font="Noto Sans KR",
                        color=GREY_B,
                    )
                    .move_to(ys[i])
                    .align_to(ys[i], LEFT),
                )
                for i in range(5)
            ]
        )
        self.playwl(
            *[
                AnimationGroup(FadeIn(qa_data[i][0]), FadeOut(xs[i]))
                for i in range(len(xs))
            ],  # xs -> questions
            lag_ratio=0.2,
        )
        self.playwl(
            *[
                AnimationGroup(FadeIn(qa_data[i][1]), FadeOut(ys[i]))
                for i in range(len(ys))
            ],  # ys -> answers
            lag_ratio=0.2,
        )

        self.playw(Flash(slt.get_corner(UL)))
        self.playwl(
            Flash(xtext.get_corner(UL)), Flash(ytext.get_corner(UL)), lag_ratio=0.5
        )

        sslt = Words("Self supervised Learning", font_size=32).set_color_by_gradient(
            YELLOW_A, YELLOW_C
        )
        sslt.move_to(slt).align_to(slt, RIGHT)
        self.play(
            FadeIn(sslt.words[0]),
            Transform(
                slt.words, sslt.words[1:], replace_mobject_with_target_in_scene=True
            ),
        )
        self.playw(
            sslt.animate.next_to(model, UP, buff=0.5), FadeOut(qa_data), FadeIn(xs, ys)
        )
        self.playw(FadeOut(ytext, ys))
        xs_ = xs.copy()
        xtext_ = xtext.copy()
        self.playw(
            xs_.animate.move_to(ys.get_center()).shift(RIGHT * 0.2),
            xtext_.animate.move_to(ytext.get_center()),
        )


class finetuning(Scene2D):
    def construct(self):
        data = [
            [
                "What is piui?",
                "1. Piui is a sound of birds chirping.",
                "2. Piui is a type of fruit.",
                "A > B",
            ],
            [
                "How can I make a chemical bomb?",
                "1. First, prepare them: ...",
                "2. Making a chemical bomb is illegal and dangerous.",
                "A < B",
            ],
            [
                "Who is Albert Einstein?",
                "1. Albert Einstein was a scientist.",
                "2. Albert Einstein was a theoretical physicist.",
                "A < B",
            ],
            # [
            #     "Where is Busan?",
            #     "1. Busan is a city in South Korea.",
            #     "2. Busan is a type of food.",
            #     "A > B",
            # ],
        ]

        def sample(idx):
            q = Words(data[idx][0], font_size=20, font="Noto Sans KR", color=GREY_B)
            a1 = Words(data[idx][1], font_size=18, font="Noto Sans KR", color=GREY_B)
            a2 = Words(data[idx][2], font_size=18, font="Noto Sans KR", color=GREY_B)
            a = VGroup(a1, a2).arrange(RIGHT, buff=0.3)
            cmp = Words(data[idx][3], font_size=20, font="Noto Sans KR", color=GREEN_B)

            group = VGroup(q, a, cmp).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            rect = DashedVMobject(
                SurroundingRectangle(group, buff=0.2, color=GREEN_A, stroke_width=2),
                num_dashes=200,
                dashed_ratio=0.7,
            )
            group.add(rect)
            return group

        samples = (
            VGroup(*[sample(i) for i in range(len(data))])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .shift(UP * 0.5)
        )
        model = (
            Rectangle(width=3, height=5, color=YELLOW_B)
            .set_fill(BLACK, opacity=0.85)
            .set_z_index(1)
        ).next_to(samples, LEFT, buff=1.5)
        modelt = (
            Text("Model", font_size=32)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .move_to(model)
        ).set_z_index(2)
        self.cf.move_to(VGroup(samples, model)).scale(1.25).shift(DOWN * 0.5)
        self.playwl(GrowFromCenter(model), FadeIn(modelt), lag_ratio=0.2)
        self.playw(FadeIn(samples))

        self.play(Flash(samples[0].get_corner(UL)))
        self.play(Flash(samples[1].get_corner(UL)))
        self.playw(Flash(samples[2].get_corner(UL)))
        shade = (
            Line(
                start=self.cf.get_corner(RIGHT),
                end=LEFT * 3,
                stroke_color=BLACK,
                stroke_opacity=[1, 0],
                stroke_width=8000,
            )
            .set_sheen_direction(LEFT)
            .set_z_index(10)
        )
        self.play(FadeIn(shade))

        rlhf = Text("RLHF", font_size=48).set_color_by_gradient(YELLOW_A, YELLOW_C)
        dpo = Text("DPO", font_size=48).set_color_by_gradient(YELLOW_A, YELLOW_C)
        methods = (
            VGroup(rlhf, dpo)
            .arrange(DOWN, buff=1)
            .to_edge(RIGHT, buff=1.5)
            .set_z_index(12)
        )
        self.play(FadeIn(rlhf, shift=LEFT))
        self.playw(FadeIn(dpo, shift=LEFT))

        self.playw(FadeOut(shade, rlhf, dpo))

        prompt = (
            Text("Prompt", font_size=24, font="Noto Sans KR")
            .next_to(samples[0], RIGHT)
            .align_to(samples[0][0], UP)
            .set_z_index(11)
        )
        response = (
            Text("Responses", font_size=24, font="Noto Sans KR")
            .next_to(samples[0], RIGHT)
            .align_to(samples[0][1], UP)
            .set_z_index(11)
        )
        preference = (
            Text("Preference", font_size=24, font="Noto Sans KR")
            .next_to(samples[0], RIGHT)
            .align_to(samples[0][2], UP)
            .set_z_index(11)
        )
        self.playwl(
            FadeIn(prompt),
            FadeIn(response),
            FadeIn(preference),
            lag_ratio=0.5,
        )
        shade = (
            Rectangle(width=30, height=15, color=BLACK)
            .set_fill(BLACK, opacity=0.75)
            .set_z_index(9)
        )
        self.playw(FadeIn(shade))

        VGroup(rlhf, dpo).move_to(self.cf)
        self.playw(FadeOut(prompt, response, preference), FadeIn(rlhf, dpo))

        self.playw(FadeOut(shade, rlhf, dpo))

        with open("media/textwiki.txt", "r") as f:
            wiki_text = f.read().split("\n")
        pretrain_par = (
            VGroup(
                *[
                    Words(line, font_size=32, font="Noto Sans KR", color=GREY_B)
                    for line in wiki_text
                ]
            )
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            .next_to(samples, RIGHT, buff=1.5)
            .set_z_index(11)
        )
        self.playwl(
            FadeIn(pretrain_par),
            self.cf.animate.move_to(VGroup(samples, pretrain_par))
            .shift(LEFT * 2.5)
            .scale(1.2),
            lag_ratio=0.1,
        )
        self.playw(Indicate(pretrain_par, scale_factor=1.01))
        self.playwl(FadeIn(prompt), FadeIn(response), FadeIn(preference), lag_ratio=0.5)


class imageNext(Scene2D):
    def construct(self):
        pil_img = Image.open("media/vecatable.jpg")
        img_arr = np.array(pil_img)
        patch_size = 96
        img_mob = Group()
        for i in range(0, img_arr.shape[0], patch_size):
            for j in range(0, img_arr.shape[1], patch_size):
                if (
                    i + patch_size > img_arr.shape[0]
                    or j + patch_size > img_arr.shape[1]
                ):
                    continue
                patch = img_arr[i : i + patch_size, j : j + patch_size]
                img_mob.add(ImageMobject(patch).scale(0.4))
        img_mob.arrange_in_grid(
            rows=img_arr.shape[0] // patch_size,
            cols=img_arr.shape[1] // patch_size,
            buff=0,
        )
        self.playw(FadeIn(img_mob))
        self.playw(
            img_mob.animate.arrange_in_grid(
                rows=img_arr.shape[0] // patch_size,
                cols=img_arr.shape[1] // patch_size,
                buff=0.1,
            )
        )
        arrh = Arrow(
            img_mob.get_corner(UL) + UP * 0.2,
            img_mob.get_corner(UR) + UP * 0.2,
            buff=0.1,
            color=YELLOW_B,
            tip_length=0.2,
            stroke_width=3,
        )
        arrv = Arrow(
            img_mob.get_corner(UL) + LEFT * 0.2,
            img_mob.get_corner(DL) + LEFT * 0.2,
            buff=0.1,
            color=YELLOW_B,
            tip_length=0.2,
            stroke_width=3,
        )
        self.play(GrowArrow(arrh), run_time=0.5)
        self.playw(GrowArrow(arrv), run_time=0.5)

        self.wait()

        self.playw(VGroup(arrh, arrv).animate.set_color(PURE_RED))

        self.wait()

        self.play(FadeOut(VGroup(arrh, arrv)), run_time=0.5)

        redundancy = (
            Text("Redundancy", font_size=36)
            .set_color_by_gradient(RED_A, RED_C)
            .next_to(img_mob, DOWN, buff=0.4)
        )
        self.playw(FadeIn(redundancy, shift=DOWN * 0.5), run_time=0.5)
        redundancy.generate_target()
        img_mob.generate_target()
        img_mob.target.arrange_in_grid(
            rows=img_arr.shape[0] // patch_size,
            cols=img_arr.shape[1] // patch_size,
            buff=0.1,
        )
        redundancy.target.next_to(img_mob.target, DOWN, buff=0.4)
        self.playw(MoveToTarget(img_mob), MoveToTarget(redundancy))

        background_indices = [2, 3, 4, 5, 10, 11, 18, 19, 24, 25, 26, 33, 34]
        background = Group(*[img_mob[i] for i in background_indices])

        self.playw(
            background.animate.arrange(RIGHT, buff=0.15).next_to(img_mob, UP, buff=0.3)
        )

        shade = (
            Rectangle(
                width=30,
                height=15,
                color=BLACK,
            )
            .set_fill(BLACK, opacity=0.75)
            .set_z_index(9)
        )
        self.playw(FadeIn(shade))


class dinointro(Scene2D):
    def construct(self):
        model = (
            Rectangle(width=3, height=2, color=YELLOW_B)
            .set_fill(BLACK, opacity=0.85)
            .set_z_index(1)
        )
        modelt = (
            Text("Vision Model", font_size=28)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .move_to(model)
            .set_z_index(2)
        )
        pretrain = (
            Text("Pretrain", font="Noto Sans KR", font_size=36)
            .set_color_by_gradient(BLUE_A, BLUE)
            .next_to(model, DOWN)
            .shift(LEFT * 2)
        )
        finetune = (
            Text("Fine-tuning", font="Noto Sans KR", font_size=36)
            .set_color_by_gradient(GREEN_A, GREEN)
            .next_to(model, DOWN)
            .shift(RIGHT * 2)
        )
        self.play(FadeIn(model), FadeIn(modelt))
        self.playw(FadeIn(pretrain), FadeIn(finetune))
        pt_exp = Words(
            "시각적 정보에 대한 일반적인 이해", font_size=24, font="Noto Sans KR"
        ).next_to(pretrain, DOWN, buff=0.3)
        self.playwl(*[FadeIn(item) for item in pt_exp.words], lag_ratio=0.2)
        self.playwl(
            VGroup(pretrain, pt_exp).animate.set_opacity(0.3).set_color(PURE_RED)
        )

        model_exp = Words(
            "한 모델이 다양한 작업을 잘 하지는 못함", font_size=24, font="Noto Sans KR"
        ).next_to(model, UP, buff=0.3)
        self.playwl(*[FadeIn(item) for item in model_exp.words], lag_ratio=0.2)

        self.wait(5)

        dino = (
            Text("DiNO", font_size=36, font="Noto Sans KR")
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .next_to(pretrain, LEFT, buff=0.3)
        )
        self.playw(FadeIn(dino, shift=LEFT * 0.3))

        self.playwl(
            FadeOut(model, modelt, pretrain, finetune, pt_exp, model_exp),
            self.cf.animate.move_to(dino),
            lag_ratio=0.3,
        )
        slt = (
            Words("Self supervised Learning", font_size=32)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .next_to(dino, DOWN, buff=0.5)
            .set_z_index(12)
        )
        self.playwl(*[FadeIn(item) for item in slt.words], lag_ratio=0.3)

        self.play(VGroup(dino, slt).animate.shift(DOWN))

        unlabeled_ = (
            RoundedRectangle(width=6, height=3, corner_radius=0.3)
            .set_color(BLUE_B)
            .next_to(dino, UL, buff=0.5)
        )
        unlabeled_text = (
            Text("Unlabeled Images", font_size=24)
            .set_color_by_gradient(BLUE_A, BLUE)
            .move_to(unlabeled_)
        )
        unlabeled = RoundedRectangle(width=20, height=10, corner_radius=0.3).set_color(
            BLUE_B
        )
        labeled = RoundedRectangle(
            width=3, height=1.5, corner_radius=0.3, stroke_opacity=0.2
        ).set_color(GREEN_B)
        labeled_text = (
            Text("Labeled Images", font_size=24)
            .set_opacity(0.4)
            .set_color_by_gradient(GREEN_A, GREEN)
            .move_to(labeled)
        )
        unlabeled_group = unlabeled.next_to(dino, UL, buff=0.5)
        labeled_group = (
            VGroup(labeled, labeled_text).next_to(dino, UR, buff=0.5).shift(RIGHT)
        )
        self.playwl(
            FadeIn(unlabeled_group, unlabeled_text),
            FadeIn(labeled_group),
            lag_ratio=0.3,
        )

        self.play(FadeOut(unlabeled_text, unlabeled, target_position=dino, scale=0.1))
        self.playw(Wiggle(dino), Flash(dino.get_corner(UL)))


class vision(Scene2D):
    def construct(self):
        model = (
            Rectangle(width=3, height=1.7, color=YELLOW_B)
            .set_fill(BLACK, opacity=0.85)
            .set_z_index(1)
        )
        modelt = (
            Text("Vision Model", font_size=28)
            .set_color_by_gradient(YELLOW_A, YELLOW_C)
            .move_to(model)
            .set_z_index(2)
        )
        pretrain = (
            Text("Pretrain", font="Noto Sans KR", font_size=36)
            .set_color_by_gradient(BLUE_A, BLUE)
            .next_to(model, DOWN)
            .shift(LEFT * 2)
        )
        finetune = (
            Text("Fine-tuning", font="Noto Sans KR", font_size=36)
            .set_color_by_gradient(GREEN_A, GREEN)
            .next_to(model, DOWN)
            .shift(RIGHT * 2)
        )
        self.addw(model, modelt, pretrain, finetune)
        dino = (
            Text("DiNO", font_size=36, font="Noto Sans KR")
            .next_to(pretrain, DOWN, buff=0.3)
            .set_color_by_gradient(BLUE_A, BLUE)
        )
        self.playw(FadeIn(dino, shift=DOWN * 0.3))
        self.play(FadeOut(dino, pretrain, target_position=model, scale=0.3))
        self.playw(Wiggle(model), Flash(model.get_corner(UL)))

        self.playw(Circumscribe(finetune))
        self.playw(finetune.animate.scale(1.2).align_to(finetune, UL), run_time=3)

        self.playw(FadeIn(pretrain, dino), FadeOut(finetune))

        self.play(FadeOut(model, modelt, pretrain))
        self.playw(dino.animate.move_to(ORIGIN))

        nl = NumberLine(
            x_range=[0, 6],
            length=10,
            color=GREY_B,
            include_ticks=True,
            include_numbers=False,
        )
        nl.ticks[0::2].set_opacity(0)
        self.playwl(dino.animate.shift(UP * 2.5), FadeIn(nl))

        v1 = Words("v1", font_size=28, font="Noto Sans KR", color=BLUE_D).next_to(
            nl.ticks[1], UP, buff=0.1
        )
        v2 = Words("v2", font_size=28, font="Noto Sans KR", color=BLUE_C).next_to(
            nl.ticks[3], UP, buff=0.1
        )
        v3 = Words("v3", font_size=28, font="Noto Sans KR", color=BLUE_B).next_to(
            nl.ticks[5], UP, buff=0.1
        )
        year1 = Text("2021", font_size=20, color=BLUE_D, font="Noto Sans KR").next_to(nl.ticks[1], DOWN, buff=0.1)
        year2 = Text("2023", font_size=20, color=BLUE_C, font="Noto Sans KR").next_to(nl.ticks[3], DOWN, buff=0.1)
        year3 = Text("2025", font_size=20, color=BLUE_B, font="Noto Sans KR").next_to(nl.ticks[5], DOWN, buff=0.1)

        param1 = Text("85M", font_size=20, color=YELLOW_D, font=MONO_FONT).next_to(v1, UP, buff=0.1)
        param2 = Text("~1.1M", font_size=20, color=YELLOW_C, font=MONO_FONT).next_to(v2, UP, buff=0.1)
        param3 = Text("7B", font_size=20, color=YELLOW_B, font=MONO_FONT).next_to(v3, UP, buff=0.1)
        self.play(FadeIn(v1), run_time=0.5)
        self.play(FadeIn(v2), run_time=0.5)
        self.playw(FadeIn(v3), run_time=0.5)

        self.play(FadeIn(year1), run_time=0.5)
        self.play(FadeIn(year2), run_time=0.5)
        self.playw(FadeIn(year3), run_time=0.5)

        self.playwl(FadeIn(param1), FadeIn(param2), FadeIn(param3), lag_ratio=0.3)
