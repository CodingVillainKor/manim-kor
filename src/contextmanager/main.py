from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        _scale = 0.65
        c = PythonCode("src/example.py").scale(_scale).shift(UP * 0.5)
        c.code[:2].set_opacity(0.3)
        c.code[5:10].set_opacity(0.3)
        c.code[-3].set_opacity(0)
        c.code[-1].set_opacity(0)
        to_eval = c.code[-2][4:]
        to_eval.save_state()
        to_eval.align_to(c.code[-1], LEFT)

        time_code = VGroup(c.code[5], c.code[7], c.code[8], c.code[9])

        self.addw(c)
        c.frame.set_z_index(-1)
        self.playwl(
            time_code.animate.shift(
                c.code[-2].get_center() - time_code[:2].get_center()
            )
            .align_to(c.code[-2], LEFT)
            .set_opacity(1),
            c.frame.animate.stretch_to_fit_height(5.5).align_to(c.frame, UP),
            self.cf.animate.shift(DOWN).scale(0.9),
            lag_ratio=0.15,
        )

        model_out = (
            Code(code_string="out = model.generate()", language="python")
            .code_lines[0]
            .scale(_scale)
            .move_to(to_eval)
            .shift(UP * 0.07)
            .align_to(to_eval, LEFT)
            .set_color(YELLOW)
        )
        model_out = VGroup(model_out[:3], model_out[3], model_out[4:])
        self.playw(to_eval.animate.become(model_out))

        clones = VGroup()
        for i in range(2):
            clone_tc = time_code.copy()
            clone_te = to_eval.copy()
            clones.add(VGroup(clone_tc, clone_te))
        total = VGroup(VGroup(time_code, to_eval), *clones)
        total.generate_target().arrange(DOWN, buff=0.05).align_to(total, UP)
        fns = VGroup()
        for i in range(1, 4):
            fn = (
                Code(code_string=f"fn{i}()", language="python")
                .code_lines[0]
                .move_to(total.target[i - 1][1])
                .scale(_scale)
                .align_to(total.target, LEFT)
                .set_color(YELLOW)
            )
            fns.add(fn)
            total.target[i - 1][1].become(fn)

        self.playwl(
            MoveToTarget(total),
            self.cf.animate.shift(DOWN * 3),
            c.frame.animate.stretch_to_fit_height(9).align_to(c.frame, UP),
            lag_ratio=0.1,
        )


def get_time_code():
    c = PythonCode("src/example.py")
    c.code[6].set_opacity(0)
    time_code = c.code[5:10]
    time_code.arrange(DOWN, aligned_edge=LEFT, buff=-0.15)
    return time_code


class when2use(Scene2D):
    def construct(self):
        def cline(code_string):
            w = Words(code_string, font=MONO_FONT, color=GREY_A, font_size=24)
            w.words[-1].set_color(YELLOW)
            return w

        example1 = VGroup(
            cline("model = Model()"),
            cline("out = model.generate()"),
        ).arrange(DOWN, aligned_edge=LEFT)
        self.playw(FadeIn(example1))

        self.playw(example1.animate.arrange(DOWN, aligned_edge=LEFT, buff=2.3))

        tc1 = get_time_code()
        tc1.shift(example1[0].get_center() - tc1[1][4].get_center()).align_to(
            example1[0], LEFT
        )
        self.playwl(FadeIn(tc1), self.cf.animate.shift(RIGHT), lag_ratio=0.3)

        tc2 = get_time_code()
        tc2.shift(example1[1].get_center() - tc2[1][4].get_center()).align_to(
            example1[1], LEFT
        )
        self.playwl(FadeIn(tc2), self.cf.animate.shift(DOWN), lag_ratio=0.3)

        self.playw(*[item.animate.set_color(PURE_RED) for item in [tc1, tc2]])
        self.playw(example1.animate.set_opacity(0.1))

        cm = (
            PythonCode("src/example.py")
            .code[3:11]
            .move_to(ORIGIN)
            .shift(RIGHT * 1.25 + DOWN * 0.5)
        )

        self.playw(
            VGroup(example1, tc1, tc2).animate.shift(LEFT * 13),
            FadeIn(cm, shift=LEFT * 5),
        )
        self.cf.save_state()
        self.play(self.cf.animate.scale(1.6).move_to(VGroup(cm, example1).get_center()))
        tc1r = DashedVMobject(
            SurroundingRectangle(VGroup(tc1[0][4:], tc1[-1]), color=GREEN, buff=0.1),
            num_dashes=60,
            dashed_ratio=0.6,
        )
        tc1l = DashedLine(cm[1].get_left(), tc1r.get_right(), color=GREEN, buff=0.1)
        tc2r = DashedVMobject(
            SurroundingRectangle(VGroup(tc2[0][4:], tc2[-1]), color=GREEN, buff=0.1),
            num_dashes=60,
            dashed_ratio=0.6,
        )
        tc2l = DashedLine(cm[1].get_left(), tc2r.get_right(), color=GREEN, buff=0.1)
        self.playwl(
            FadeIn(tc1l, tc2l),
            AnimationGroup(
                GrowFromEdge(tc1r, RIGHT),
                GrowFromEdge(tc2r, RIGHT),
            ),
            lag_ratio=0.5,
            wait=0.1,
        )
        self.playw(FadeOut(tc1r, tc2r, tc1l, tc2l, tc1, tc2))
        self.playw(Restore(self.cf))

        context = cm[0][1:8]
        manager = cm[0][8:]
        self.playw(
            context.animate.scale(1.2).set_color(PURE_GREEN).shift(UP * 0.3),
            cm[1:].animate.set_opacity(0.2),
        )
        self.playw(
            manager.animate.scale(1.2)
            .set_color(PURE_GREEN)
            .shift(UP * 0.3)
            .align_to(manager, LEFT),
            context.animate.scale(1 / 1.2).set_color(GREY_A).shift(DOWN * 0.3),
        )
        self.playw(
            manager.animate.scale(1 / 1.2)
            .set_color(GREY_A)
            .shift(DOWN * 0.3)
            .align_to(manager, LEFT)
        )


class how2use(Scene2D):
    def construct(self):
        c = PythonCode("src/example.py").code[3:11]
        c[1:].set_opacity(0.3)

        self.playwl(*[FadeIn(item) for item in c], lag_ratio=0.3)

        self.play(c[1].animate.set_opacity(1))
        self.playw(Indicate(c[1]))

        self.playw(c.animate.shift(LEFT * 2.5).scale(0.8))

        exc = PythonCode("src/snippet.py").code.shift(RIGHT * 3.3).scale(0.8)
        exc[0].set_color(GREEN)
        exc[-1].set_color(GREEN)
        self.playw(FadeIn(exc))
        pre_box = SurroundingRect(color=YELLOW_B, stroke_width=2).surround(
            exc[:2], buff_h=0.1, buff_w=0.1
        )
        post_box = SurroundingRect(color=PURPLE_B, stroke_width=2).surround(
            exc[-2:], buff_h=0.1, buff_w=0.1
        )
        self.playw(Create(pre_box))
        self.playw(Create(post_box))

        pre_boxc = pre_box.copy()
        post_boxc = post_box.copy()
        self.playw(
            pre_boxc.animate.surround(c[2][4:], buff_h=0.1, buff_w=0.15),
            c[2].animate.set_opacity(0.5),
        )
        self.playw(
            post_boxc.animate.surround(c[-3:], buff_h=0.1, buff_w=0.15),
            c[-3:].animate.set_opacity(0.5),
        )

        wc = (
            Words("with elapsed_time():", font=MONO_FONT, font_size=18)
            .next_to(exc[2][4:], UP, buff=0.1)
            .align_to(exc[2], LEFT)
        )
        wc.words[0].set_color(GREEN_D)
        wc.words[-1].set_color(GREY_A)
        self.playw(
            Transform(
                VGroup(pre_box, exc[:2]), wc, replace_mobject_with_target_in_scene=True
            ),
            FadeOut(exc[3:], post_box),
            exc[2].animate.shift(RIGHT * 0.7),
        )
        pre_code = VGroup(c[2].copy(), pre_boxc.copy())
        post_code = VGroup(c[-3:].copy(), post_boxc.copy())
        self.play(
            pre_code.animate.scale(0.5)
            .next_to(exc[2][4:], UP, buff=0.0)
            .align_to(exc[2], LEFT),
            wc.animate.shift(UP * 0.2),
        )
        self.playw(FadeOut(pre_code), wc.animate.shift(DOWN * 0.2))
        self.play(
            post_code.animate.scale(0.5)
            .next_to(exc[2][4:], DOWN, buff=0.0)
            .align_to(exc[2], LEFT)
        )
        self.playw(FadeOut(post_code))
        self.playw(
            FadeOut(exc[2], wc, shift=RIGHT * 2),
            VGroup(c, pre_boxc, post_boxc).animate.center().scale(1.2),
        )
        self.playw(FadeOut(pre_boxc), c[2].animate.set_opacity(1))
        self.playw(FadeOut(post_boxc), c[4:].animate.set_opacity(1))
        self.playw(Flash(c[0]), c[0].animate.set_color(YELLOW))

class outro(Scene3D):
    def construct(self):
        tilt_angle = 60 * DEGREES
        c = PythonCode("src/outro.py").code.rotate(tilt_angle, LEFT).shift(DOWN*6)
        self.addw(c)
        self.playw(c.animate.shift(UP*5))