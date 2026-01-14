from manim import *
from raenim import *
from random import random, seed
from pathlib import Path
from torchvision.datasets import MNIST, CIFAR100
from PIL import Image


seed(48)
np.random.seed(42)
mnist_path = Path(__file__).parent.parent
mnist = MNIST(root=mnist_path, download=False)
cifar100 = CIFAR100(root=mnist_path, download=True)
cat = np.array(Image.open(mnist_path / "vecatable.jpg"))


class whatiscollapse(Scene3D):
    def construct(self):
        gan_g = TextBox(
            text="Generator",
            text_kwargs={"font_size": 36, "color": GREY_A, "font": "Noto Sans KR"},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.8,
                "buff": 1,
                "stroke_width": 2,
                "stroke_color": BLUE_E,
            },
        )
        gan_d = TextBox(
            text="Discriminator",
            text_kwargs={"font_size": 24, "color": GREY_B, "font": "Noto Sans KR"},
            box_kwargs={
                "fill_color": BLACK,
                "fill_opacity": 0.8,
                "buff": 0.5,
                "stroke_width": 2,
                "stroke_color": RED_E,
            },
        )
        gan_g.rotate(-PI / 3, axis=RIGHT).shift(DOWN * 0.8)
        gan_d.shift(RIGHT * 4 + UP).set_z_index(1)
        self.addw(gan_g, gan_d)

        m0, l0 = mnist[2]
        m0 = np.array(m0)
        img = (
            ImageMobject(m0)
            .scale(3)
            .rotate(-PI / 3, axis=RIGHT)
            .next_to(gan_g, UP, buff=1)
            .set_z_index(-3)
        )

        def get_noise():
            noise = np.random.uniform(0, 256, (28, 28)).astype(np.uint8)
            return (
                ImageMobject(noise)
                .scale(3)
                .rotate(-PI / 3, axis=RIGHT)
                .next_to(gan_g, DOWN, buff=0.4)
                .set_z_index(-3)
            )

        def get_t(idx):
            img = Text(f"Noise {idx}", font_size=24, color=GREY_B).set_z_index(-3)
            img[-1].set_color(YELLOW)
            return img

        noise = get_noise()
        t_noise = get_t(1).next_to(noise, RIGHT, buff=0.1)
        self.play(FadeIn(noise, t_noise, shift=UP * 0.3))
        self.play(
            Transform(noise, img, replace_mobject_with_target_in_scene=True),
            FadeOut(t_noise, shift=UP * 2),
        )
        self.playw(img.animate.rotate(PI / 3, axis=RIGHT))

        c1 = (
            Text("✔", font_size=24, color=GREEN)
            .next_to(gan_d, RIGHT, buff=0.3)
            .set_z_index(-3)
        )
        self.playw(FadeTransform(img.copy(), c1))
        self.play(FadeOut(img, c1))

        for i in range(2, 5):
            img = (
                ImageMobject(m0)
                .scale(3)
                .rotate(-PI / 3, axis=RIGHT)
                .next_to(gan_g, UP, buff=1)
                .set_z_index(-3)
            )
            noise = get_noise()
            t_noise = get_t(i).next_to(noise, RIGHT, buff=0.1)
            self.play(FadeIn(noise, t_noise, shift=UP * 0.3))
            self.play(
                Transform(noise, img, replace_mobject_with_target_in_scene=True),
                FadeOut(t_noise, shift=UP * 2),
            )
            self.play(img.animate.rotate(PI / 3, axis=RIGHT))

            c1 = (
                Text("✔", font_size=24, color=GREEN)
                .next_to(gan_d, RIGHT, buff=0.3)
                .set_z_index(-3)
            )
            self.play(FadeTransform(img.copy(), c1))
            self.play(FadeOut(img, c1))
        self.wait()

        nump = NumberPlane(
            x_range=[0, 8, 1],
            y_range=[0, 8, 1],
            background_line_style={"stroke_color": GREY_D, "stroke_opacity": 0},
            x_length=4,
            y_length=3,
        ).shift(UP * 2)
        nump.x_axis.set_color(GREY_B)
        nump.y_axis.set_color(GREY_B)
        label_x = (
            Text("iter.", font_size=18, color=GREY_B, font="Noto Sans KR")
            .next_to(nump.x_axis, DOWN, buff=0.05)
            .align_to(nump.x_axis, RIGHT)
        )
        label_y = (
            Text("loss", font_size=18, color=GREY_B, font="Noto Sans KR")
            .next_to(nump.y_axis, LEFT, buff=0.05)
            .align_to(nump.y_axis, UP)
            .set_z_index(-1)
        )
        self.playw(
            FadeIn(VGroup(nump, label_x, label_y), target_position=gan_g, scale=0.7),
            FadeOut(gan_d, shift=RIGHT),
        )

        def loss_func(x):
            base = 8 * np.exp(-0.3 * x)
            oscillation = 0.6 * np.sin(5 * x) * np.exp(-0.2 * x) + 0.3 * np.sin(
                10 * x
            ) * np.exp(-0.1 * x)
            return base + oscillation

        loss_graph = nump.plot(
            loss_func,
            x_range=[0.1, 10],
            color=YELLOW_B,
            stroke_width=3,
        )

        self.playw(Create(loss_graph), run_time=3, rate_func=rush_from)

        noise = get_noise().next_to(gan_g, LEFT, buff=0.4)
        img = (
            ImageMobject(m0)
            .scale(3)
            .rotate(-PI / 3, axis=RIGHT)
            .next_to(gan_g, RIGHT, buff=1)
            .set_z_index(-3)
        )
        self.play(FadeIn(noise, shift=RIGHT * 0.3))
        self.playw(
            Transform(noise, img, replace_mobject_with_target_in_scene=True),
            loss_graph.animate.set_color(RED),
        )


class centering(Scene3D):
    def construct(self):
        title = (
            Text("Centering", font="Noto Sans KR", font_size=28)
            .set_color_by_gradient(BLUE_A, BLUE_B)
            .set_z_index(2)
        )
        self.playwl(*[FadeIn(item) for item in title], wait=0)
        self.playw(Indicate(title, scale_factor=1.1, color=BLUE_C))

        box = SurroundingRectangle(
            title,
            buff=1.0,
            stroke_color=GREY_B,
            stroke_width=3,
            fill_opacity=1,
            fill_color=BLACK,
        ).set_z_index(1)
        self.play(FadeIn(box, scale=1.1))

        before = Square(side_length=1.5, color=GREY_D).next_to(box, LEFT, buff=1)
        after = Square(side_length=1.5, color=GREY_D).next_to(box, RIGHT, buff=1)
        arr = Arrow(
            before.get_right(),
            after.get_left(),
            buff=0.1,
            stroke_width=3,
            color=GREY_B,
            tip_length=0.2,
        )
        # orig_scene = VGroup(title, box, before, after, arr).set_z_index(-1)
        # orig_scene.save_state()
        self.playwl(FadeIn(before), FadeIn(after), GrowArrow(arr), lag_ratio=0.5)
        self.playw(self.cf.animate.move_to(before).shift(IN * 19))

        pre_origin = before.get_center() + IN * 19
        VGroup(title, box, before, after, arr).set_opacity(0)

        model = (
            TextBox(
                text="Model",
                text_kwargs={"font_size": 24, "color": GREY_B, "font": "Noto Sans KR"},
                box_kwargs={
                    "fill_color": BLACK,
                    "fill_opacity": 1,
                    "buff": 0.5,
                    "stroke_width": 2,
                    "stroke_color": BLUE_E,
                },
            )
            .move_to(pre_origin)
            .set_z_index(2)
        )
        img = (
            ImageMobject(cat)
            .move_to(pre_origin)
            .scale(0.25)
            .shift(LEFT * 7)
            .set_z_index(-3)
        )
        logit = (
            Linear(3, 8)
            .scale(0.75)
            .next_to(model, RIGHT, buff=-0.5)  # .set_z_index(-3)
        )
        logitt = (
            Text("logits", font_size=18, color=GREY_B, font="Noto Sans KR").next_to(
                logit[-1], UP, buff=0.1
            )
            # .set_z_index(-1)
        )
        for o in logit[-1]:
            o.set_stroke(width=2)
        self.play(FadeIn(model, img))
        self.play(img.animate.shift(RIGHT * 3).scale(0.3))
        self.remove(img)
        self.playwl(FadeIn(logit), FadeIn(logitt), lag_ratio=0.3)
        logitt.set_z_index(-1)
        logit.set_z_index(-3)
        sm = (
            Text("softmax()", font="Noto Sans KR", font_size=18, color=GREY_B)
            .next_to(logit, DOWN, buff=0.3)
            .shift(RIGHT * 1.4)
        )
        out = Tensor(8, shape="square").scale(0.75).next_to(logit, RIGHT, buff=1.5)
        arrs = VGroup(
            *[
                Arrow(
                    l.get_right(),
                    m.get_left(),
                    buff=0.05,
                    stroke_width=2,
                    tip_length=0.1,
                    color=GREY_B,
                )
                for l, m in zip(logit[-1], out)
            ]
        )
        self.play(FadeIn(sm), *[GrowArrow(a) for a in arrs])
        self.playw(FadeIn(out))

        students = VGroup(model, logit, logitt, sm, out, arrs)
        self.playw(students.animate.shift(LEFT * 5))

        tmodel = (
            TextBox(
                text="Teacher model",
                text_kwargs={"font_size": 24, "color": GREY_B, "font": "Noto Sans KR"},
                box_kwargs={
                    "fill_color": BLACK,
                    "fill_opacity": 1,
                    "buff": 0.6,
                    "stroke_width": 2,
                    "stroke_color": RED_E,
                },
            )
            .move_to(pre_origin + RIGHT * 4)
            .set_z_index(2)
        )
        tlogit = (
            Linear(8, 3).scale(0.75).next_to(tmodel, LEFT, buff=-0.5).set_z_index(-3)
        )
        tlogitt = (
            Text("logits", font_size=18, color=GREY_B, font="Noto Sans KR")
            .next_to(tlogit[0], UP, buff=0.1)
            .set_z_index(-1)
        )
        for o in tlogit[0]:
            o.set_stroke(width=2)
        tout = Tensor(8, shape="square").scale(0.75).next_to(tlogit, LEFT, buff=1.5)
        tarrs = VGroup(
            *[
                Arrow(
                    l.get_left(),
                    m.get_right(),
                    buff=0.05,
                    stroke_width=2,
                    tip_length=0.1,
                    color=GREY_B,
                )
                for l, m in zip(tlogit[0], tout)
            ]
        )
        self.play(FadeIn(tmodel, tlogit, tlogitt))
        tsm = (
            Text("softmax()", font="Noto Sans KR", font_size=18, color=GREY_B)
            .next_to(tlogit, DOWN, buff=0.3)
            .shift(LEFT * 1.4)
        )
        self.play(FadeIn(tsm), *[GrowArrow(a) for a in tarrs])
        self.playw(FadeIn(tout))

        models = (
            VGroup(*[model.copy().set_z_index(1 - i) for i in range(20)])
            .arrange(UL + LEFT * 0.5, buff=-1.15)
            .next_to(model, UL + LEFT * 0.5, buff=-1.15)
        )
        modelsc = models.copy()
        self.play(FadeIn(models))

        tmodelc = tmodel.copy()
        self.playw(Transform(models, tmodelc, path_arc=-PI / 2))
        self.remove(models)
        out.generate_target().set_fill(color=GREY_C, opacity=1)
        out.target[2].set_fill(color=YELLOW, opacity=1)
        tout.generate_target().set_fill(color=GREY_C, opacity=1)
        tout.target[2].set_fill(color=YELLOW, opacity=1)
        self.playw(MoveToTarget(tout), MoveToTarget(out))

        outv = VGroup(
            *[
                Text(
                    f"0.99" if i == 2 else "0.00",
                    font_size=18,
                    color=YELLOW_C if i == 2 else GREY_B,
                )
                .move_to(out[i])
                .align_to(out[i], LEFT)
                for i in range(8)
            ]
        )
        toutv = VGroup(
            *[
                Text(
                    f"0.99" if i == 2 else "0.00",
                    font_size=18,
                    color=YELLOW_C if i == 2 else GREY_B,
                )
                .move_to(tout[i])
                .align_to(tout[i], RIGHT)
                for i in range(8)
            ]
        )
        self.playw(
            Transform(tout, toutv, replace_mobject_with_target_in_scene=True),
            Transform(out, outv, replace_mobject_with_target_in_scene=True),
        )

        self.playw(self.cf.animate.shift(OUT * 3))

        def get_cifar100(idx):
            return PixelImage(np.array(cifar100[idx][0])).scale(0.3).move_to(pre_origin)

        m_in, t_in = get_cifar100(0).next_to(model, LEFT), get_cifar100(0).next_to(
            tmodel, RIGHT
        )
        self.play(FadeIn(m_in, t_in))
        self.play(
            FadeOut(m_in, target_position=model), FadeOut(t_in, target_position=tmodel)
        )
        self.playw(
            Indicate(outv, scale_factor=1.0, color=RED),
            Indicate(toutv, scale_factor=1.0, color=RED),
        )
        vbox = DashedVMobject(
            SurroundingRectangle(
                VGroup(outv, toutv),
                buff=0.25,
                stroke_color=YELLOW,
                stroke_width=2,
            ),
            num_dashes=60,
        )
        loss = (
            Text("Loss ↓", font_size=24, color=YELLOW_C)
            .next_to(vbox, UP, buff=0.2)
            .set_z_index(2)
        )
        self.playwl(FadeIn(vbox), FadeIn(loss), lag_ratio=0.3)
        for i in range(1, 4):
            m_in, t_in = get_cifar100(i).next_to(model, LEFT), get_cifar100(i).next_to(
                tmodel, RIGHT
            )
            self.play(
                FadeIn(m_in, t_in),
                *([] if i != 1 else [FadeOut(loss, vbox)]),
                run_time=0.5,
            )
            self.play(
                FadeOut(m_in, target_position=model),
                FadeOut(t_in, target_position=tmodel),
                run_time=0.5,
            )
            self.play(
                Indicate(outv, scale_factor=1.0, color=RED),
                Indicate(toutv, scale_factor=1.0, color=RED),
                run_time=0.5,
            )
        self.playw(FadeIn(modelsc))
        tmodelc = tmodel.copy()
        self.playw(Transform(modelsc, tmodelc, path_arc=-PI / 2))
        self.remove(modelsc)

        ct = (
            Text("Centering", font_size=36, font="Noto Serif KR", color=BLUE_B)
            .set_z_index(2)
            .move_to(pre_origin)
            .shift(UP * 3)
            .set_color_by_gradient(BLUE_A, BLUE_B)
        )
        self.playw(FadeIn(ct, shift=UP * 0.5))
        self.play(FadeOut(students, outv))
        students.shift(LEFT * 10)
        teachers = VGroup(tlogit[1:], tarrs, toutv, tmodel)

        tl = tlogit[0].set_z_index(1)
        tl.generate_target().move_to(pre_origin).shift(LEFT)
        self.playw(
            teachers.animate.rotate(-PI / 2.5, axis=RIGHT)
            .move_to(pre_origin)
            .shift(DOWN * 2.5),
            FadeOut(tsm),
            MoveToTarget(tl),
            tlogitt.animate.next_to(tl.target, UP, buff=0.1),
        )

        c = tlogit[0].copy().shift(RIGHT * 2)
        for item in c:
            item.set_stroke(color=random_color())
            item.set_fill(color=BLACK, opacity=1)
        mns = Text("-", font=MONO_FONT, font_size=36).move_to(VGroup(tl, c))
        self.playw(FadeIn(c, mns))

        cs = []
        for i in range(len(c)):
            cs.append(
                VGroup(
                    *[
                        c[i].copy().set_z_index(-4 - j).set_stroke(color=random_color())
                        for j in range(3)
                    ]
                )
                .arrange(UR, buff=-0.2)
                .next_to(c[i], UR, buff=-0.2)
            )
        cs = VGroup(*cs)
        csl = cs.copy().shift(LEFT * 2)
        for j, item in enumerate(zip(*csl)):
            for sitem in item:
                sitem.set_z_index(-4 - j)
        tl.set_fill(color=BLACK, opacity=1)
        c.set_z_index(1)
        tl.generate_target()
        for item in tl.target:
            item.set_stroke(color=random_color())
        self.playw(
            FadeIn(cs),
            FadeIn(csl),
            MoveToTarget(tl),
            tlogitt.animate.shift(LEFT * 0.4),
            mns.animate.shift(RIGHT * 0.1),
        )

        meanb = Brace(
            cs[0], UL, buff=0.1, stroke_width=0, color=GREEN, sharpness=3
        ).set_opacity(0)
        meant = (
            Text("mean(dim=0)", font=MONO_FONT, color=GREEN, font_size=18)
            .rotate(PI / 4)
            .next_to(meanb, UL, buff=-0.55)
            .set_opacity(0)
        )
        self.playw(VGroup(meanb, meant).animate.set_opacity(1))
        c.save_state()
        self.play(
            FadeOut(cs, meanb, meant),
            AnimationGroup(
                c.animate.set_stroke(color=YELLOW), rate_func=there_and_back
            ),
        )
        c.restore()
        self.wait()

        temp_ = Text(
            "centering EMA", font_size=24, color=GREY_B, font="Noto Sans KR"
        ).move_to(pre_origin + RIGHT * 3)
        self.addw(temp_)
        self.remove(temp_)
        self.wait()

        mlogitt = (
            Text("mean(logits, dim=0)", font=MONO_FONT, color=GREEN, font_size=18)
            .rotate(-PI / 2)
            .next_to(c, RIGHT, buff=0.1)
        )
        self.playwl(
            *[FadeIn(item) for item in [mlogitt[:4], mlogitt[4:12], mlogitt[12:]]],
            lag_ratio=0.5,
        )

        tl.generate_target()
        csl.generate_target()
        c.generate_target()
        for i in range(len(tl)):
            if i == 2:
                tl.target[i].set_stroke(color=YELLOW)
                csl.target[i].set_stroke(color=YELLOW)
                c.target[i].set_stroke(color=YELLOW)
            else:
                tl.target[i].set_stroke(color=GREY_C)
                csl.target[i].set_stroke(color=GREY_C)
                c.target[i].set_stroke(color=GREY_C)

        self.playw(MoveToTarget(tl), MoveToTarget(csl), FadeOut(mlogitt))

        self.playwl(
            FadeOut(VGroup(tl, csl).copy(), shift=RIGHT), MoveToTarget(c), lag_ratio=0.5
        )
        centered = c.copy().next_to(c, RIGHT, buff=0.75).set_stroke(color=GREY_D)
        eq = (
            Text("=", font_size=36, color=GREY_B)
            .move_to(VGroup(c, centered))
            .set_z_index(2)
        )
        self.playwl(FadeIn(eq), FadeIn(centered, shift=RIGHT * 0.5), lag_ratio=0.5)

        self.playw(
            FadeOut(VGroup(eq, c, tlogitt, csl, tl, mns), shift=LEFT * 3),
            centered.animate.align_to(tl, LEFT),
        )
        self.playw(
            teachers.animate.rotate(PI / 2.5, axis=RIGHT).shift(UP * 2.5),
        )
        teachers = VGroup(*teachers, centered)
        aligned = VGroup(students, teachers)
        aligned.generate_target().arrange(RIGHT, buff=1).move_to(pre_origin)
        aligned.target[1].align_to(aligned.target[0][1], UP)
        self.playw(MoveToTarget(aligned))

        arrsc = tarrs.copy().set_color(GREY_C)
        toutv_new = VGroup(
            *[
                Text(f"0.12" if i % 2 else "0.13", font_size=18, color=GREY_B)
                .move_to(toutv[i])
                .align_to(toutv[i], RIGHT)
                for i in range(8)
            ]
        )
        self.playw(
            FadeOut(tarrs),
            AnimationGroup(*[GrowArrow(arrsc[i]) for i in range(len(arrsc))]),
            Transform(toutv, toutv_new),
        )
        loss_arrs = VGroup(
            *[
                Arrow(
                    toutv[i].get_left(),
                    outv[i].get_right(),
                    buff=0.1,
                    stroke_width=2,
                    tip_length=0.1,
                    color=RED,
                )
                for i in range(8)
            ]
        )
        self.playw(*[GrowArrow(arr) for arr in loss_arrs])


class sharpening(Scene3D):
    def construct(self):
        model = (
            TextBox(
                text="Model",
                text_kwargs={"font_size": 24, "color": GREY_B, "font": "Noto Sans KR"},
                box_kwargs={
                    "fill_color": BLACK,
                    "fill_opacity": 1,
                    "buff": 0.5,
                    "stroke_width": 2,
                    "stroke_color": BLUE_E,
                },
            )
            .move_to(ORIGIN)
            .set_z_index(2)
        )
        tmodel = (
            TextBox(
                text="Teacher model",
                text_kwargs={"font_size": 24, "color": GREY_B, "font": "Noto Sans KR"},
                box_kwargs={
                    "fill_color": BLACK,
                    "fill_opacity": 1,
                    "buff": 0.6,
                    "stroke_width": 2,
                    "stroke_color": RED_E,
                },
            )
            .move_to(RIGHT * 4)
            .set_z_index(2)
        )
        tlogit = Linear(8, 3).scale(0.75).next_to(tmodel, LEFT, buff=-0.5)
        tlogit[-1].set_opacity(0)
        tlogit[0].set_stroke(width=2).set_fill(color=BLACK, opacity=1)
        logit = Linear(3, 8).scale(0.75).next_to(model, RIGHT, buff=-0.5)
        logit[0].set_opacity(0)
        logit[-1].set_stroke(width=2).set_fill(color=BLACK, opacity=1)

        student = VGroup(logit, model)
        teacher = VGroup(tlogit, tmodel)
        VGroup(student, teacher).arrange(RIGHT, buff=4)

        logitt = Text(
            "logits", font_size=18, color=GREY_B, font="Noto Sans KR"
        ).next_to(logit[-1], DOWN, buff=0.1)
        tlogitt = Text(
            "logits", font_size=18, color=GREY_B, font="Noto Sans KR"
        ).next_to(tlogit[0], DOWN, buff=0.1)
        self.addw(model, tmodel, logit, tlogit, logitt, tlogitt)

        tl = tlogit[0].set_z_index(1)
        tlogit[1].set_z_index(0.9)
        l = logit[-1].set_z_index(1)
        csl = []

        for i in range(len(tl)):
            csl.append(
                VGroup(
                    *[
                        tl[i]
                        .copy()
                        .set_stroke(color=tl[0].stroke_color)
                        .set_z_index(0.8 - 0.1 * j)
                        .set_fill(color=BLACK, opacity=1)
                        for j in range(3)
                    ]
                )
                .arrange(UL, buff=-0.2)
                .next_to(tl[i], UL, buff=-0.2)
            )
        csl = VGroup(*csl)
        lcsl = []
        for i in range(len(l)):
            lcsl.append(
                VGroup(
                    *[
                        l[i]
                        .copy()
                        .set_stroke(color=l[0].stroke_color)
                        .set_z_index(0.8 - 0.1 * j)
                        .set_fill(color=BLACK, opacity=1)
                        for j in range(3)
                    ]
                )
                .arrange(UR, buff=-0.2)
                .next_to(l[i], UR, buff=-0.2)
            )
        lcsl = VGroup(*lcsl)
        self.playw(FadeIn(csl), FadeIn(lcsl))

        l_s = VGroup(*[VGroup(l[i], *lcsl[i]) for i in range(len(l))])
        tl_s = VGroup(*[VGroup(tl[i], *csl[i]) for i in range(len(tl))])
        self.playw(
            l_s.animate.set_stroke(color=GREY_C),
            tl_s.animate.set_stroke(color=GREY_C),
        )

        tl_outs = VGroup(
            *[
                VGroup(
                    *[
                        Text(
                            f"0.12" if i % 2 else "0.13",
                            font_size=18,
                            color=GREY_B,
                        ).next_to(tl_s[i][j], LEFT, buff=0.75)
                        for j in range(4)
                    ]
                )
                for i in range(8)
            ]
        )

        tl_arrs = VGroup(
            *[
                VGroup(
                    *[
                        Arrow(
                            tl_s[i][j].get_left(),
                            tl_outs[i][j].get_right(),
                            buff=0.0,
                            stroke_width=2,
                            tip_length=0.1,
                            color=GREY_B,
                        ).set_z_index(3)
                        for j in range(4)
                    ]
                )
                for i in range(8)
            ]
        )
        self.playwl(
            AnimationGroup(*[GrowArrow(tl_arrs[i][0]) for i in range(8)]),
            FadeIn(*[tl_outs[i][0] for i in range(8)]),
            lag_ratio=0.5,
            wait=0,
        )
        self.playwl(
            FadeOut(
                *[tl_outs[i][0] for i in range(8)],
                *[tl_arrs[i][0] for i in range(8)],
                run_time=0.5,
            ),
            AnimationGroup(*[GrowArrow(tl_arrs[i][1]) for i in range(8)]),
            FadeIn(*[tl_outs[i][1] for i in range(8)]),
            lag_ratio=0.5,
            wait=0,
        )
        self.playwl(
            FadeOut(
                *[tl_outs[i][1] for i in range(8)],
                *[tl_arrs[i][1] for i in range(8)],
                run_time=0.5,
            ),
            AnimationGroup(*[GrowArrow(tl_arrs[i][2]) for i in range(8)]),
            FadeIn(*[tl_outs[i][2] for i in range(8)]),
            lag_ratio=0.5,
            wait=0,
        )
        self.playwl(
            FadeOut(
                *[tl_outs[i][2] for i in range(8)],
                *[tl_arrs[i][2] for i in range(8)],
                run_time=0.5,
            ),
            AnimationGroup(*[GrowArrow(tl_arrs[i][3]) for i in range(8)]),
            FadeIn(*[tl_outs[i][3] for i in range(8)]),
            lag_ratio=0.5,
            wait=1,
        )

        l_outs = VGroup(
            *[
                VGroup(
                    *[
                        Text(
                            f"0.12" if i % 2 else "0.13",
                            font_size=18,
                            color=GREY_B,
                        ).next_to(l_s[i][j], RIGHT, buff=0.75)
                        for j in range(4)
                    ]
                )
                for i in range(8)
            ]
        )

        l_arrs = VGroup(
            *[
                VGroup(
                    *[
                        Arrow(
                            l_s[i][j].get_right(),
                            l_outs[i][j].get_left(),
                            buff=0.0,
                            stroke_width=2,
                            tip_length=0.1,
                            color=GREY_B,
                        ).set_z_index(3)
                        for j in range(4)
                    ]
                )
                for i in range(8)
            ]
        )
        self.playwl(
            AnimationGroup(*[GrowArrow(l_arrs[i][0]) for i in range(8)]),
            FadeIn(*[l_outs[i][0] for i in range(8)]),
            lag_ratio=0.5,
            wait=0,
        )
        self.playwl(
            FadeOut(
                *[l_outs[i][0] for i in range(8)],
                *[l_arrs[i][0] for i in range(8)],
                run_time=0.5,
            ),
            AnimationGroup(*[GrowArrow(l_arrs[i][1]) for i in range(8)]),
            FadeIn(*[l_outs[i][1] for i in range(8)]),
            lag_ratio=0.5,
            wait=0,
        )
        self.playwl(
            FadeOut(
                *[l_outs[i][1] for i in range(8)],
                *[l_arrs[i][1] for i in range(8)],
                run_time=0.5,
            ),
            AnimationGroup(*[GrowArrow(l_arrs[i][2]) for i in range(8)]),
            FadeIn(*[l_outs[i][2] for i in range(8)]),
            lag_ratio=0.5,
            wait=0,
        )
        self.playwl(
            FadeOut(
                *[l_outs[i][2] for i in range(8)],
                *[l_arrs[i][2] for i in range(8)],
                run_time=0.5,
            ),
            AnimationGroup(*[GrowArrow(l_arrs[i][3]) for i in range(8)]),
            FadeIn(*[l_outs[i][3] for i in range(8)]),
            lag_ratio=0.5,
            wait=1,
        )

        box = DashedVMobject(
            SurroundingRectangle(
                VGroup(
                    VGroup(*[tl_outs[i][3] for i in range(8)]),
                    VGroup(*[l_outs[i][3] for i in range(8)]),
                ),
                buff=0.15,
                stroke_color=YELLOW,
                stroke_width=2,
            ),
            num_dashes=60,
        )
        losst = (
            Text("Loss ↓", font_size=20, color=YELLOW_C, font="Noto Sans KR")
            .next_to(box, UP, buff=0.2)
            .set_z_index(2)
        )
        self.playw(FadeIn(box, losst), scale=1.1)

        self.play(FadeOut(box, losst))
        teacher.add(tlogitt)
        teacher = VGroup(teacher[0][1:], *teacher[1:])
        self.playw(
            teacher.animate.rotate(-PI / 2.5, axis=UP).shift(RIGHT * 11),
            VGroup(*[csl[i] for i in range(8)], tlogit[0]).animate.shift(RIGHT * 7),
            self.cf.animate.shift(RIGHT * 9),
        )

        c = tlogit[0].copy().shift(RIGHT * 2)
        mns = Text("-", font=MONO_FONT, font_size=36, color=GREY_B).move_to(
            VGroup(tlogit[0], c)
        )
        self.playw(FadeIn(c, mns, shift=RIGHT * 0.3))

        self.playw(
            Indicate(VGroup(tlogit[0], csl), scale_factor=1.0, color=GREY_D),
            FadeOut(mns, c),
        )


class howsharpening(Scene3D):
    def construct(self):
        teacher = (
            TextBox(
                text="Teacher model",
                text_kwargs={"font_size": 48, "color": GREY_B, "font": "Noto Sans KR"},
                box_kwargs={
                    "fill_color": BLACK,
                    "fill_opacity": 1,
                    "buff": 1.5,
                    "stroke_width": 2,
                    "stroke_color": RED_E,
                },
            )
            .move_to(ORIGIN)
            .rotate(-PI / 2.8, axis=RIGHT)
            .shift(DOWN * 3)
            .set_z_index(2)
        )
        teacher.text.shift(UP * 0.5)
        logit = (
            Linear(3, 8)
            .scale(1.5)
            .rotate(PI / 2)
            .rotate(-PI / 2.8, axis=RIGHT)
            .next_to(teacher, UP, buff=-0.2)
            .set_z_index(1)
        )
        logit[-1].set_stroke(width=2)
        logit[0].set_opacity(0)
        self.addw(teacher.box, logit)

        st = Text(
            "Sharpening", font_size=36, font="Noto Sans KR"
        ).set_color_by_gradient(GREEN_A, GREEN_B)
        self.playwl(*[FadeIn(item) for item in st], lag_ratio=0.1)
        self.play(FadeIn(teacher.text), st.animate.shift(UP * 3).set_opacity(0.7))

        rand_vals = [random() * 12 - 3 for _ in range(8)]
        rands = (
            VGroup(
                *[
                    Text(f"{val:.1f}", font_size=24, color=GREEN_B, font="Noto Sans KR")
                    for val in rand_vals
                ]
            )
            .arrange(RIGHT, buff=0.5)
            .next_to(logit, UP, buff=0.75)
        )
        boxes = VGroup(
            *[
                SurroundingRectangle(r, buff=0.2, stroke_color=GREY_C, stroke_width=3)
                for r in rands
            ]
        )
        lines = VGroup(
            *[
                DashedLine(
                    logit[-1][i].get_top(),
                    boxes[i].get_bottom(),
                    stroke_color=GREY_C,
                    stroke_width=2,
                    dash_length=0.1,
                )
                for i, r in enumerate(rands)
            ]
        )
        self.playwl(
            AnimationGroup(*[Create(line) for line in lines]),
            FadeIn(boxes),
            FadeIn(rands),
            lag_ratio=0.3,
            wait=0,
        )
        bc = BarChart(
            values=rand_vals,
            bar_names=["" for i in range(8)],
            y_range=[-3, 12, 20],
            x_length=7.75,
            y_length=2,
            bar_colors=[GREEN_B for _ in range(8)],
            bar_width=0.5,
            x_axis_config={"stroke_opacity": 0},
        ).next_to(boxes, UP, buff=0.4)
        xline = Line(bc.c2p(0, 0), bc.c2p(8, 0), stroke_color=GREY_C, stroke_width=1)

        bc.y_axis.set_opacity(0)
        self.playw(FadeIn(bc, xline))
        div = Text("÷ 0.04", font_size=24, color=BLUE_B, font="Noto Sans KR").next_to(
            boxes, RIGHT, buff=0.3
        )
        mul = Text("× 25", font_size=24, color=BLUE_B, font="Noto Sans KR").next_to(
            boxes, RIGHT, buff=0.3
        )
        self.playw(FadeIn(div, shift=RIGHT * 0.3))
        self.playw(Transform(div, mul, replace_mobject_with_target_in_scene=True))

        rand_vals_sharp = [val * 25 for val in rand_vals]
        rands_sharp = VGroup(
            *[
                Text(
                    f"{val:.1f}",
                    font_size=20,
                    color=BLUE_B,
                    font="Noto Sans KR",
                ).move_to(rands[i])
                for i, val in enumerate(rand_vals_sharp)
            ]
        )
        bc_sharp = (
            BarChart(
                values=rand_vals_sharp,
                bar_names=["" for i in range(8)],
                y_range=[-75, 300, 20],
                x_length=7.75,
                y_length=3,
                bar_colors=[BLUE_C for _ in range(8)],
                bar_width=0.5,
                x_axis_config={"stroke_opacity": 0},
            )
            .next_to(boxes, UP, buff=0.4)
            .shift(LEFT * 0.43 + DOWN * 0.2)
        )
        bc_sharp.y_axis.set_opacity(0)
        self.playw(
            FadeOut(mul),
            Transform(rands, rands_sharp, replace_mobject_with_target_in_scene=True),
            Transform(bc, bc_sharp, replace_mobject_with_target_in_scene=True),
        )

        sm = Text(
            "softmax()", font_size=24, color=PURPLE_B, font="Noto Sans KR"
        ).next_to(boxes, RIGHT, buff=0.3)
        self.playw(FadeIn(sm, shift=RIGHT * 0.3))

        def softmax_robust_with_temp(vals, temp=1.0):
            max_val = max(vals)
            exp_vals = [np.exp((val - max_val) / temp) for val in vals]
            sum_exp = sum(exp_vals)
            return [val / sum_exp for val in exp_vals]

        sharp_vals = softmax_robust_with_temp(rand_vals_sharp, temp=70)
        rands_sharped = VGroup(
            *[
                Text(
                    f"{val:.2f}",
                    font_size=20,
                    color=PURPLE_B,
                    font="Noto Sans KR",
                ).move_to(rands_sharp[i])
                for i, val in enumerate(sharp_vals)
            ]
        )
        bc_sharped = (
            BarChart(
                values=sharp_vals,
                bar_names=["" for i in range(8)],
                y_range=[0, 0.75, 0.2],
                x_length=7.75,
                y_length=4,
                bar_colors=[PURPLE_C for _ in range(8)],
                bar_width=0.5,
                x_axis_config={"stroke_opacity": 0},
            )
            .next_to(boxes, UP, buff=0.4)
            .shift(LEFT * 0.34 + UP * 0.32)
        )
        bc_sharped.y_axis.set_opacity(0)
        self.playwl(
            FadeOut(st),
            AnimationGroup(
                Transform(
                    rands_sharp,
                    rands_sharped,
                    replace_mobject_with_target_in_scene=True,
                ),
                Transform(
                    bc_sharp, bc_sharped, replace_mobject_with_target_in_scene=True
                ),
            ),
            lag_ratio=0.5,
        )
