from manim import *
from raenim import *
from random import seed

from strings import *

seed(41)
np.random.seed(41)

"""
- Claude, ChatGPT는 LLM(Large Language Model)이다. Language Model은 뭘까
- Language model은 확률 모델임, 확률 모델은 뭘까
- Language model은 어떤 확률 모델일까
- Autoregressive 생성이 대세고 대부분 이 방법을 씀
- 다음 영상에서는 Diffusion Language Model에 대해 알아볼 예정
"""


class intro(Scene2D):
    def construct(self):
        claude_icon = ImageMobject("assets/claude.png").scale(0.2)
        chatgpt_icon = ImageMobject("assets/chatgpt.png").scale(0.2)
        icons = (
            Group(claude_icon, chatgpt_icon)
            .arrange(RIGHT, buff=5.5)
            .shift(LEFT * 3 + UP * 3)
        )

        claude_string = (
            Words(CLAUDE_STRING, line_spacing=0.9, font="Noto Sans KR", color=GREY_A)
            .scale(0.3)
            .next_to(claude_icon, RIGHT, buff=0.5)
            .align_to(claude_icon, UP)
        )

        chatgpt_string = (
            Words(CHATGPT_STRING, line_spacing=0.9, font="Noto Sans KR", color=GREY_A)
            .scale(0.3)
            .next_to(chatgpt_icon, RIGHT, buff=0.5)
            .align_to(chatgpt_icon, UP)
        )
        self.play(FadeIn(claude_icon))
        self.playw(FadeIn(chatgpt_icon))
        self.playwl(*[FadeIn(item) for item in claude_string.words])
        self.playwl(*[FadeIn(item) for item in chatgpt_string.words])

        self.play(FadeOut(claude_string, chatgpt_string))
        self.playw(icons.animate.arrange(RIGHT))
        llm_diagram = VGroup()
        llm_rect = Rectangle(width=4, height=2.5, color=GREEN, stroke_width=3)
        llm_text = (
            Text("LLM(Large Language Model)", font="Noto Sans KR")
            .scale(0.35)
            .next_to(llm_rect, UP, buff=0.05)
            .align_to(llm_rect, LEFT)
        )
        llm_diagram.add(llm_text)
        llm_diagram.add(llm_rect)

        self.playw(FadeIn(llm_diagram))

        lm_diagram = VGroup()
        lm_rect = Rectangle(width=7, height=4, color=BLUE, stroke_width=3)
        lm_text = (
            Text("Language Model", font="Noto Sans KR")
            .scale(0.4)
            .next_to(lm_rect, UP, buff=0.05)
            .align_to(lm_rect, LEFT)
        )
        lm_diagram.add(lm_text)
        lm_diagram.add(lm_rect)
        self.playw(FadeIn(lm_diagram), wait=2)

        pm_diagram = VGroup()
        pm_rect = Rectangle(width=10, height=6, color=PURPLE, stroke_width=3)
        pm_text = (
            Text("Probabilistic Model", font="Noto Sans KR")
            .scale(0.4)
            .next_to(pm_rect, UP, buff=0.05)
            .align_to(pm_rect, LEFT)
        )
        pm_diagram.add(pm_text)
        pm_diagram.add(pm_rect)
        self.playw(FadeIn(pm_diagram.shift(UP * 0.4)))

        self.playw(FadeOut(icons, llm_diagram, lm_diagram))


class probmodel(Scene3D):
    def construct(self):
        pm_diagram = VGroup()
        pm_rect = Rectangle(width=10, height=6, color=PURPLE, stroke_width=3)
        pm_text = (
            Text("Probabilistic Model", font="Noto Sans KR")
            .scale(0.4)
            .next_to(pm_rect, UP, buff=0.05)
            .align_to(pm_rect, LEFT)
        )
        pm_diagram.add(pm_text)
        pm_diagram.add(pm_rect)
        self.addw(pm_diagram.shift(UP * 0.4))
        self.play(pm_diagram.animate.scale(1.5))
        self.remove(pm_diagram)
        self.wait()

        pm_eq = MathTex(
            "p(x)",
            "=",
            "p(",
            "x_1",
            ",",
            "x_2",
            ", ...,",
            "x_n",
            ")",
        )
        self.playw(FadeIn(pm_eq), wait=2)

        get_rock = lambda: ImageMobject("assets/rock.png").scale(0.12)
        get_paper = lambda: ImageMobject("assets/paper.png").scale(0.12)
        get_scissors = lambda: ImageMobject("assets/scissors.png").scale(0.12)
        get_prock = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_rock(), MathTex(")").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        get_ppaper = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_paper(), MathTex(")").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        get_pscissors = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_scissors(), MathTex(")").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        rock = get_rock()
        paper = get_paper()
        scissors = get_scissors()

        rsp = (
            Group(rock, paper, scissors)
            .arrange(RIGHT, buff=0.1)
            .next_to(pm_eq[0], DOWN)
        )
        self.playw(FadeIn(rsp))
        question = (
            Text("Unknown pattern", font="Noto Sans KR", color=RED)
            .scale(0.5)
            .next_to(rsp, RIGHT)
        )
        self.playw(FadeIn(question, shift=RIGHT * 0.2))

        table = Group()
        for i in range(2):
            for j in range(3):
                cell = Rectangle(width=1.7, height=0.8, color=GREY, stroke_width=1)
                if i == 0:
                    cell_item = [get_prock(), get_ppaper(), get_pscissors()][j]
                else:
                    cell_item = Text(
                        ["0.3", "0.4", "0.3"][j], font="Noto Sans KR"
                    ).scale(0.5)
                table.add(Group(cell, cell_item))

        table.arrange_in_grid(3, 3, buff=0.1).next_to(pm_eq[0], DOWN)
        table[0][1][1].set_opacity(0)
        table[1][1][1].set_opacity(0)
        table[2][1][1].set_opacity(0)
        rock.generate_target().move_to(table[0][1][1])
        paper.generate_target().move_to(table[1][1][1])
        scissors.generate_target().move_to(table[2][1][1])

        self.playwl(
            AnimationGroup(*[MoveToTarget(item) for item in rsp], FadeOut(question)),
            FadeIn(table),
            lag_ratio=0.5,
        )

        self.play(
            pm_eq[:3].animate.shift(LEFT * 0.2),
            pm_eq[4:].animate.shift(RIGHT * 0.2),
            Indicate(pm_eq[3]),
        )
        self.play(Indicate(pm_eq[5]), pm_eq[6:].animate.shift(RIGHT * 0.2))
        self.playw(Indicate(pm_eq[-2]), pm_eq[-1].animate.shift(RIGHT * 0.2))

        x1_scissor = get_scissors().next_to(pm_eq[3], UP)
        x2_paper = get_paper().next_to(pm_eq[5], UP)
        x3_paper = get_paper().next_to(pm_eq[-2], UP)
        self.playwl(
            FadeIn(x1_scissor, shift=UP * 0.5),
            FadeIn(x2_paper, shift=UP * 0.5),
            FadeIn(x3_paper, shift=UP * 0.5),
            lag_ratio=0.2,
        )

        x_brace = Brace(Group(x1_scissor, x2_paper, x3_paper), UP, color=GREY_B).scale(
            0.9
        )
        x_bracet = (
            Text("n steps", font="Noto Sans KR", color=GREY_A)
            .scale(0.4)
            .next_to(x_brace, UP)
        )
        self.playw(FadeIn(x_brace, x_bracet))

        self.playw(FadeOut(x1_scissor, x2_paper, x3_paper, x_brace, x_bracet))
        self.playw(
            Circumscribe(
                table, fade_in=True, fade_out=True, stroke_width=3, color=PURPLE
            ),
            wait=4,
        )

        pxi_sample = MathTex("p(x_i) = ").scale(0.7).next_to(table, LEFT, buff=0.3)
        total_px = (
            MathTex("p(x_1)p(x_2)...p(x_n)").scale(0.7).next_to(table, RIGHT, buff=0.3)
        )
        self.playw(FadeIn(pxi_sample))
        self.play(FadeIn(total_px, shift=RIGHT * 0.5, scale=0.6))
        self.playw(total_px.animate.next_to(pm_eq, RIGHT, buff=0.2))

        self.playw(FadeOut(pxi_sample, total_px))

        table2 = Group()
        get_prock2 = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_rock(), MathTex("|x_{i-1})").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        get_ppaper2 = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_paper(), MathTex("|x_{i-1})").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        get_pscissors2 = lambda: Group(
            MathTex("p(x_i=").scale(0.6),
            get_scissors(),
            MathTex("|x_{i-1})").scale(0.6),
        ).arrange(RIGHT, buff=0.1)
        for i in range(2):
            for j in range(3):
                cell = Rectangle(width=2.5, height=0.8, color=GREY, stroke_width=1)
                if i == 0:
                    cell_item = [get_prock2(), get_ppaper2(), get_pscissors2()][j]
                else:
                    cell_item = Text(
                        ["...", "...", "..."][j], font="Noto Sans KR"
                    ).scale(0.5)
                table2.add(Group(cell, cell_item))
        table2.arrange_in_grid(3, 3, buff=0.1).next_to(pm_eq[0], DOWN)
        table2[0][1][1].set_opacity(0)
        table2[1][1][1].set_opacity(0)
        table2[2][1][1].set_opacity(0)
        rock.generate_target().move_to(table2[0][1][1])
        paper.generate_target().move_to(table2[1][1][1])
        scissors.generate_target().move_to(table2[2][1][1])

        self.playw(Transformr(table, table2), *[MoveToTarget(item) for item in rsp])
        pxi_sample = (
            MathTex("p(x_i|x_{i-1}) = ")
            .scale(0.7)
            .next_to(table2, UP, buff=0.1)
            .align_to(table2, LEFT)
        )
        total_px = (
            MathTex("p(x_1)p(x_2|x_1)...p(x_n|x_{n-1})")
            .scale(0.6)
            .next_to(table2, RIGHT, buff=0.3)
        )
        self.playw(FadeIn(pxi_sample))
        self.play(FadeIn(total_px, shift=RIGHT * 0.5, scale=0.6))
        self.playw(total_px.animate.next_to(pm_eq, RIGHT, buff=0.2))
        self.playw(FadeOut(pxi_sample, total_px))

        table22 = Group()
        get_prock22 = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_rock(), MathTex("|x_{i-2})").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        get_ppaper22 = lambda: Group(
            MathTex("p(x_i=").scale(0.6), get_paper(), MathTex("|x_{i-2})").scale(0.6)
        ).arrange(RIGHT, buff=0.1)
        get_pscissors22 = lambda: Group(
            MathTex("p(x_i=").scale(0.6),
            get_scissors(),
            MathTex("|x_{i-2})").scale(0.6),
        ).arrange(RIGHT, buff=0.1)
        for i in range(2):
            for j in range(3):
                cell = Rectangle(width=2.5, height=0.8, color=GREY, stroke_width=1)
                if i == 0:
                    cell_item = [get_prock22(), get_ppaper22(), get_pscissors22()][j]
                else:
                    cell_item = Text(
                        ["...", "...", "..."][j], font="Noto Sans KR"
                    ).scale(0.5)
                table22.add(Group(cell, cell_item))
        table22.arrange_in_grid(3, 3, buff=0.1).next_to(pm_eq[0], DOWN)
        table22[0][1][1].set_opacity(0)
        table22[1][1][1].set_opacity(0)
        table22[2][1][1].set_opacity(0)
        rock.generate_target().move_to(table22[0][1][1])
        paper.generate_target().move_to(table22[1][1][1])
        scissors.generate_target().move_to(table22[2][1][1])
        self.playw(Transformr(table2, table22), *[MoveToTarget(item) for item in rsp])

        get_p23 = lambda: MathTex(
            "p(x_i, x_{i+1}, x_{i+2}| x_{i-1})", color=GREEN
        ).scale(0.9)
        p23 = get_p23().next_to(pm_eq[0], DOWN)

        self.playw(FadeOut(table22, rsp))
        self.playw(FadeIn(p23))
        self.playw(FadeOut(p23))

        eq = (
            MathTex(r"p(", r"\mathrm{to\,predict}", r"|", r"\mathrm{condition)")
            .scale(0.8)
            .next_to(pm_eq[0], DOWN, buff=0.3)
        )
        eq[1].set_color(PURPLE)
        eq[3].set_color(YELLOW_B)
        self.play(FadeIn(eq[0]))
        self.playw(FadeIn(eq[1]))
        self.playw(FadeIn(eq[2:]))
        self.playw(FadeOut(eq))

        self.play(FadeIn(table22, rsp))
        table3 = Group()
        get_prock3 = lambda: Group(
            MathTex("p(x_i=").scale(0.6),
            get_rock(),
            MathTex("|x_{i-1};", "\\theta", ")").scale(0.6),
        ).arrange(RIGHT, buff=0.1)
        get_ppaper3 = lambda: Group(
            MathTex("p(x_i=").scale(0.6),
            get_paper(),
            MathTex("|x_{i-1};", "\\theta", ")").scale(0.6),
        ).arrange(RIGHT, buff=0.1)
        get_pscissors3 = lambda: Group(
            MathTex("p(x_i=").scale(0.6),
            get_scissors(),
            MathTex("|x_{i-1};", "\\theta", ")").scale(0.6),
        ).arrange(RIGHT, buff=0.1)
        for i in range(2):
            for j in range(3):
                cell = Rectangle(width=3, height=0.8, color=GREY, stroke_width=1)
                if i == 0:
                    cell_item = [get_prock3(), get_ppaper3(), get_pscissors3()][j]
                else:
                    cell_item = Text(
                        ["...", "...", "..."][j], font="Noto Sans KR"
                    ).scale(0.5)
                table3.add(Group(cell, cell_item))
        table3.arrange_in_grid(3, 3, buff=0.1).next_to(pm_eq[0], DOWN)
        table3[0][1][1].set_opacity(0)
        table3[1][1][1].set_opacity(0)
        table3[2][1][1].set_opacity(0)
        rock.generate_target().move_to(table3[0][1][1])
        paper.generate_target().move_to(table3[1][1][1])
        scissors.generate_target().move_to(table3[2][1][1])
        self.playw(Transformr(table22, table3), *[MoveToTarget(item) for item in rsp])

        ol = self.overlay
        table3[0][1][-1][-2].set_z_index(ol.z_index + 1)
        table3[1][1][-1][-2].set_z_index(ol.z_index + 1)
        table3[2][1][-1][-2].set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))

        pc1 = table3[0][1].copy().set_z_index(ol.z_index + 1)
        rockc = rock.copy().set_z_index(ol.z_index + 1)
        pc2 = table3[1][1].copy().set_z_index(ol.z_index + 1)
        paperc = paper.copy().set_z_index(ol.z_index + 1)
        pc3 = table3[2][1].copy().set_z_index(ol.z_index + 1)
        scissorc = scissors.copy().set_z_index(ol.z_index + 1)
        self.playw(FadeIn(pc1, pc2, pc3, rockc, paperc, scissorc))
        origs = Group(table3[0][1], table3[1][1], table3[2][1], rock, paper, scissors)
        origs.save_state()
        for item in origs:
            if isinstance(item, Group):
                for subitem in item:
                    subitem.set_opacity(0)
                continue
            item.set_opacity(0)
        copys = Group(pc1, pc2, pc3, rockc, paperc, scissorc)

        tilt_degree = 50
        self.move_camera_vertically(
            tilt_degree,
            added_anims=[copys.animate.rotate(tilt_degree * DEGREES, axis=RIGHT)],
        )
        mlp = (
            MLP(3, 8, 3)
            .scale(0.8)
            .rotate(PI / 2)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .next_to(table3, UP, buff=3)
            .set_z_index(ol.z_index + 1)
        )
        text_in = (
            VGroup(
                Text("Input:", color=GREY_A, font="Noto Sans KR").scale(0.35),
                MathTex(r"x_{i-1}").scale(0.7),
            )
            .arrange(RIGHT, buff=0.1)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .next_to(mlp[0])
        )
        text_out = (
            VGroup(
                Text("Output:", color=GREY_A, font="Noto Sans KR").scale(0.35),
                MathTex(r"p(x_{i})").scale(0.7),
            )
            .arrange(RIGHT, buff=0.1)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .next_to(mlp[-1])
        )
        theta0 = (
            MathTex("\\theta")
            .scale(0.6)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .next_to(mlp[1], buff=-0.2)
        )
        theta1 = (
            MathTex("\\theta")
            .scale(0.6)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .next_to(mlp[3], buff=-0.2)
        )
        self.playw(FadeIn(mlp, text_in, text_out, theta0, theta1))




class DLM(Scene2D):
    def construct(self):
        pxi = MathTex("p(x_i|x_{<i}; \\theta)").scale(0.6).scale(1.3)
        self.addw(pxi)

        pxt = (
            MathTex("p(x", "_t", "|", "x", "_{t+1}", "; \\theta)")
            .scale(0.6)
            .scale(1.3)
            .shift(DOWN)
        )
        self.playw(FadeIn(pxt, shift=DOWN * 0.5))
        self.playw(VGroup(pxt[1], pxt[4]).animate.set_color(RED))


class wellvsbad(Scene2D):
    def construct(self):
        mlp = MLP(3, 8, 3).scale(0.8).rotate(PI / 2)
        input_t = (
            MathTex(r"\mathrm{input}\,\,\, x_{i-1}")
            .scale(0.6)
            .next_to(mlp[0], RIGHT, buff=0.2)
        )
        output_t = (
            MathTex(r"\mathrm{output}\,\,\, p(x_i)")
            .scale(0.6)
            .next_to(mlp[-1], RIGHT, buff=0.2)
        )
        theta = MathTex(r"\theta").scale(0.6).next_to(mlp[1], RIGHT, buff=0.1)
        self.playw(FadeIn(mlp, input_t, output_t, theta))

        self.playw(
            Circumscribe(
                mlp[0], color=GREEN_C, stroke_width=3, fade_in=True, fade_out=True
            )
        )

        rock = (
            ImageMobject("assets/rock.png").scale(0.12).next_to(mlp[0], LEFT, buff=0.2)
        )
        get_prock = lambda: Group(
            MathTex("p(x_i=").scale(0.6),
            rock.copy(),
            MathTex(")\, =\, 0.97").scale(0.6),
        ).arrange(RIGHT, buff=0.1)
        prock = get_prock().next_to(mlp[-1], UP, buff=0.5)
        self.playw(FadeIn(prock, shift=UP * 0.7), Indicate(mlp[-1], scale_factor=1.1))

        real_rock = (
            Group(Text("실제 낸 것: ", font="Noto Sans KR").scale(0.4), rock.copy())
            .arrange(RIGHT, buff=0.2)
            .next_to(prock, RIGHT, buff=0.8)
        )
        self.playw(FadeIn(real_rock, shift=LEFT * 0.5))

        self.playw(Flash(prock.get_corner(UL)), Flash(real_rock.get_corner(UL)))

        self.play(self.cf.animate.shift(RIGHT * 2.5))

        ol = self.overlay
        first = VGroup(
            Text("1.", font="Noto Sans KR").scale(0.6),
            MathTex("p(x_i)").scale(0.6),
            Text("가 정말", font="Noto Sans KR").scale(0.5),
            MathTex(r"x_{i-1}").scale(0.6),
            Text("에만 의존적임", font="Noto Sans KR").scale(0.5),
        ).arrange(RIGHT, buff=0.1)
        second = VGroup(
            Text("2.", font="Noto Sans KR").scale(0.5),
            MathTex("\\theta").scale(0.6),
            Text("가 잘 학습되었음", font="Noto Sans KR").scale(0.5)
        ).arrange(RIGHT, buff=0.1)
        VGroup(first, second).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(RIGHT*6).set_z_index(ol.z_index + 1)
        self.playw(FadeIn(first[0]), FadeIn(ol))
        self.playw(*[FadeIn(item) for item in first[1:]])
        self.playw(FadeIn(second[0]))
        self.playw(*[FadeIn(item) for item in second[1:]])

        self.playw(self.cf.animate.shift(LEFT*2.5), FadeOut(first, second, ol))

        real_paper = (
            Group(Text("실제 낸 것: ", font="Noto Sans KR").scale(0.4), ImageMobject("assets/paper.png").scale(0.12))
            .arrange(RIGHT, buff=0.2)
            .next_to(prock, RIGHT, buff=0.8)
        )
        
        self.playw(Flash(prock.get_corner(UL)))
        self.playw(FadeIn(real_paper, shift=LEFT * 0.5), FadeOut(real_rock, shift=UP))
        self.playw(Flash(prock.get_corner(UL), color=PURE_RED), Flash(real_paper.get_corner(UL), color=PURE_RED))

        first = VGroup(
            Text("1.", font="Noto Sans KR").scale(0.6),
            MathTex("p(x_i)").scale(0.6),
            Text("의 조건을 잘못 설정", font="Noto Sans KR").scale(0.5)
        ).arrange(RIGHT, buff=0.1)
        second = VGroup(
            Text("2.", font="Noto Sans KR").scale(0.6),
            MathTex("\\theta").scale(0.6),
            Text("가 잘못 학습되었음", font="Noto Sans KR").scale(0.5)
        ).arrange(RIGHT, buff=0.1)
        VGroup(first, second).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(RIGHT*6).set_z_index(ol.z_index + 1)
        self.play(FadeIn(ol), self.cf.animate.shift(RIGHT * 2.5))
        self.playw(FadeIn(first[0]))
        self.playw(*[FadeIn(item) for item in first[1:]])
        self.playw(FadeIn(second[0]))
        self.playw(*[FadeIn(item) for item in second[1:]])

        self.playw(*[Indicate(item, color=RED) for item in [first, second]])


class langmodel(Scene2D):
    def construct(self):
        prob_diagram = VGroup()
        prob_rect = Rectangle(width=10, height=6, color=PURPLE, stroke_width=3)
        prob_text = (
            Text("Probabilistic Model", font="Noto Sans KR")
            .scale(0.4)
            .next_to(prob_rect, UP, buff=0.05)
            .align_to(prob_rect, LEFT)
        )
        prob_diagram.add(prob_text)
        prob_diagram.add(prob_rect)
        prob_diagram.shift(UP * 0.4)
        prob_diagram.save_state()
        self.add(prob_diagram.scale(1.5))
        self.playw(Restore(prob_diagram), wait=2)

        lm_diagram = VGroup()
        lm_rect = Rectangle(width=7, height=4, color=BLUE, stroke_width=3)
        lm_text = (
            Text("Language Model", font="Noto Sans KR")
            .scale(0.4)
            .next_to(lm_rect, UP, buff=0.05)
            .align_to(lm_rect, LEFT)
        )
        lm_diagram.add(lm_text)
        lm_diagram.add(lm_rect)
        self.playw(FadeIn(lm_diagram))
        self.playw(Indicate(VGroup(lm_diagram, prob_diagram), scale_factor=1.0))

        self.cf.save_state()
        self.play(self.cf.animate.move_to(lm_rect).scale(0.45))
        self.remove(lm_diagram, prob_diagram)
        self.playw(Restore(self.cf))

        lm_eq = MathTex(
            "p(x)",
            "=",
            "p(",
            "x_1",
            ",",
            "x_2",
            ", ...,",
            "x_n",
            ")",
            "=",
            "p(x_1)",
            "p(x_2|x_1)",
            "p(x_3|x_1,x_2)",
            "...",
            "p(x_n|x_1,...,x_{n-1})",
        ).scale(0.7)
        self.playw(FadeIn(lm_eq))
        lm_eq2 = MathTex(
            "p(x)",
            "=",
            "p(",
            "x_1",
            ",",
            "x_2",
            ", ...,",
            "x_n",
            "; \\theta",
            ")",
        ).scale(0.7)
        self.playw(
            Transformr(lm_eq[:8], lm_eq2[:8]),
            FadeIn(lm_eq2[8], shift=RIGHT * 4),
            Transformr(lm_eq[8], lm_eq2[9]),
            FadeOut(lm_eq[9:], shift=UP),
        )

        words = (
            Words("piui가 뭐냐면 ... 입니다", font="Noto Sans KR", color=GREY_A)
            .scale(0.5)
            .next_to(lm_eq2[2:], DOWN)
        )
        self.playwl(
            *[
                Transformr(
                    lm_eq2[i].copy().set_z_index(-1).set_color(GREY_C), words.words[j]
                )
                for i, j in zip([3, 5, 6, 7], [0, 1, 2, 3])
            ],
            lag_ratio=0.6,
        )
        self.play(Flash(lm_eq2[3].get_corner(UL)))
        self.play(Flash(lm_eq2[5].get_corner(UL)))
        self.playw(Flash(lm_eq2[7].get_corner(UL)))

        vocab_list = [
            "나는",
            "그는",
            "오늘",
            "혹시",
            "안녕",
            "아니",
            "진짜",
            "...",
            "piui가",
            "...",
            "뭐냐면",
            "...",
            "입니다",
            "...",
        ]
        idx_dict = {"piui가": 8, "뭐냐면": 10, "입니다": 12}
        vocab = VGroup(
            *[
                VGroup(
                    MathTex("p(x_i=").scale(0.4),
                    Text(word, font="Noto Sans KR").scale(0.25),
                    MathTex(")").scale(0.4),
                ).arrange(RIGHT, buff=0.02)
                for word in vocab_list
            ]
        )
        table = VGroup()
        for i in range(2):
            for j in range(len(vocab_list)):
                cell = Rectangle(width=1.2, height=0.6, color=GREY, stroke_width=1)
                if i == 0:
                    cell_item = vocab[j]
                else:
                    cell_item = Text(
                        ["..." for _ in range(len(vocab_list))][j],
                        font="Noto Sans KR",
                    ).scale(0.3)
                table.add(VGroup(cell, cell_item))
        table.arrange_in_grid(2, len(vocab_list), buff=0.05).next_to(
            words, DOWN, buff=0.3
        )
        self.playw(FadeIn(table), wait=4)

        uniforms = VGroup()
        for i in range(len(vocab_list)):
            cell = Rectangle(width=1.2, height=0.6, color=GREY, stroke_width=1).move_to(
                table[len(vocab_list) + i]
            )
            cell_item = (
                Text(f"{1/len(vocab_list):.2f}", font="Noto Sans KR")
                .scale(0.3)
                .move_to(cell)
            )
            uniforms.add(VGroup(cell, cell_item))
        self.playw(Transformr(table[len(vocab_list) :], uniforms))
        table = VGroup(*table[: len(vocab_list)], *uniforms)

        self.playw(
            *[uniforms[i][1].animate.set_color(PURE_RED) for i in range(len(uniforms))]
        )

        vocab2 = VGroup(
            *[
                VGroup(
                    MathTex("p(x_i=").scale(0.4),
                    Text(word, font="Noto Sans KR").scale(0.25),
                    MathTex(r"|x_{:i}; \theta)").scale(0.4),
                ).arrange(RIGHT, buff=0.02)
                for word in vocab_list
            ]
        )
        table2 = VGroup()
        for i in range(2):
            for j in range(len(vocab_list)):
                cell = Rectangle(width=1.7, height=0.6, color=GREY, stroke_width=1)
                if i == 0:
                    cell_item = vocab2[j]
                else:
                    cell_item = Text(
                        ["..." for _ in range(len(vocab_list))][j],
                        font="Noto Sans KR",
                    ).scale(0.3)
                table2.add(VGroup(cell, cell_item))
        table2.arrange_in_grid(2, len(vocab_list), buff=0.05).next_to(
            words, DOWN, buff=0.3
        )
        self.playw(Transformr(table, table2))

        mlp = MLP(16, 9, 9, 9, 16, layer_distance=8).scale(0.4).shift(UP * 2)

        self.playw(FadeOut(words), FadeIn(mlp), lm_eq2.animate.shift(DOWN * 0.7))

        pxi = (
            MathTex("p(x_i|x_{<i}; \\theta)")
            .scale(0.6)
            .next_to(mlp[-1], DOWN, buff=0.1)
        )
        self.playw(FadeIn(pxi))

        forward_prop(mlp, self)
        self.play(Indicate(pxi, scale_factor=1.1))
        text_list = ["piui가", "뭐냐면", "..."]
        texts = (
            VGroup(
                *[
                    Text(t, font="Noto Sans KR", color=GREY_A).scale(0.4)
                    for t in text_list
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(mlp, RIGHT, buff=1.5)
        )
        self.playw(Transformr(pxi.copy(), texts[0]))
        forward_prop(mlp, self)
        self.play(Indicate(pxi, scale_factor=1.1))
        self.playw(Transformr(pxi.copy(), texts[1]))
        forward_prop(mlp, self)
        self.play(Indicate(pxi, scale_factor=1.1))
        self.playw(Transformr(pxi.copy(), texts[2]))



class autoregressive(Scene2D):
    def construct(self):
        mlp = MLP(16, 9, 9, 9, 16, layer_distance=8).scale(0.4).shift(UP * 2)
        pxi = (
            MathTex("p(x_i|", "x_{<i}", "; \\theta)")
            .scale(0.6)
            .next_to(mlp[-1], DOWN, buff=0.1)
        )

        self.addw(mlp, pxi)
        self.playw(VGroup(mlp, pxi).animate.move_to(ORIGIN))

        question = Text("?", color=RED).scale(0.5).next_to(mlp[0], LEFT)
        self.play(
            Circumscribe(mlp[0], color=RED, stroke_width=3, fade_in=True, fade_out=True)
        )
        self.playw(Create(question))

        xlti = MathTex(r"x_{<i}").scale(0.6).next_to(mlp[0], LEFT, buff=0.3)
        path = BrokenLine(
            pxi[1].get_center(),
            pxi[1].get_center() + DOWN,
            xlti.get_center() + DOWN * 2,
            xlti.get_center(),
            smooth=True,
        )
        pathpxi = pxi[1].copy()
        self.play(
            MoveAlongPath(pathpxi, path),
            FadeOut(question),
            run_time=2,
            rate_func=linear,
        )
        self.remove(pathpxi)
        self.addw(xlti)

        mlp.generate_target().rotate(PI / 2)
        pxi.generate_target().next_to(mlp.target[-1], RIGHT, buff=0.2)
        xlti.generate_target().next_to(mlp.target[0], RIGHT, buff=0.2)
        self.playw(
            MoveToTarget(mlp),
            MoveToTarget(pxi),
            MoveToTarget(xlti),
        )
        self.playw(Circumscribe(pxi, fade_in=True, fade_out=True, stroke_width=3, color=GREEN))

        theta = MathTex("\\theta").scale(0.8).next_to(mlp[1]).shift(UL*0.25)
        self.playw(Transformr(pxi[-1].copy(), theta))
        self.playw(theta.animate.next_to(mlp[-2]).shift(DL * 0.25), rate_func=linear)
        self.playw(FadeOut(theta))

        prompt_texts = ["piui가", "뭐야?"]
        words = (
            Words(" ".join(prompt_texts), font="Noto Sans KR", color=GREY_A)
            .scale(0.4)
            .next_to(mlp, DOWN, buff=0.4)
            .set_z_index(-1)
        )
        self.playw(FadeIn(words), wait=3)
        self.playw(Flash(words.get_corner(UL)))
        self.play(FadeOut(words.copy(), shift=UP * 2))
        get_p = (
            lambda: MathTex("p(x_i)", color=GREEN_A)
            .scale(0.6)
            .next_to(mlp, UP, buff=0.4)
        )
        p = get_p()
        self.playw(FadeIn(p, shift=UP))

        answer_texts = ["piui는", "뭐냐면", "...", "입니다"]
        answer = (
            Text(answer_texts[0], font="Noto Sans KR", color=GREEN_A)
            .scale(0.4)
            .next_to(mlp, UP, buff=0.4)
            .set_z_index(-1)
        )
        self.playw(FadeTransform(p, answer))

        path = BrokenLine(
            answer.get_center(),
            pxi.get_right() + RIGHT + UP * 0.5,
            words.get_right() + RIGHT * 2,
            words.get_right() + RIGHT * 0.5,
            smooth=False,
        )
        self.playw(MoveAlongPath(answer, path), run_time=1.5)

        words = VGroup(words, answer)
        self.play(FadeOut(words.copy(), shift=UP * 2))
        p = get_p()
        self.playw(FadeIn(p, shift=UP))

        answer = (
            Text(answer_texts[1], font="Noto Sans KR", color=GREEN_A)
            .scale(0.4)
            .next_to(mlp, UP, buff=0.4)
            .set_z_index(-1)
        )
        self.playw(FadeTransform(p, answer))
        path = BrokenLine(
            answer.get_center(),
            pxi.get_right() + RIGHT + UP * 0.5,
            words.get_right() + RIGHT * 2,
            words.get_right() + RIGHT * 0.5,
            smooth=False,
        )
        self.playw(MoveAlongPath(answer, path), run_time=1.5)
        words = VGroup(*words, answer)
        self.play(words.animate.arrange(RIGHT).next_to(mlp, DOWN, buff=0.4))
        self.play(FadeOut(words.copy(), shift=UP * 2))
        p = get_p()
        self.playw(FadeIn(p, shift=UP))
        answer = (
            Text(answer_texts[2], font="Noto Sans KR", color=GREEN_A)
            .scale(0.4)
            .next_to(mlp, UP, buff=0.4)
            .set_z_index(-1)
        )
        self.playw(FadeTransform(p, answer))

        ol = self.overlay
        pxi.set_z_index(ol.z_index + 1)
        self.playw(
            FadeIn(ol),
            pxi.animate.scale(1.3).move_to(ORIGIN + RIGHT * 6),
            self.cf.animate.shift(RIGHT * 6),
        )

        pxic = (
            MathTex("p(", "x_i", "|", "x_{<i}", ";", "\\theta", ")")
            .scale(0.6)
            .scale(1.3)
            .set_z_index(ol.z_index + 1)
            .move_to(pxi)
        )
        self.remove(pxi)
        self.addw(pxic)

        self.playw(Circumscribe(pxic[3], stroke_width=3, fade_in=True, fade_out=True))
        self.playw(Circumscribe(pxic[5], stroke_width=3, fade_in=True, fade_out=True))
        self.playw(Circumscribe(pxic[1], stroke_width=3, fade_in=True, fade_out=True))