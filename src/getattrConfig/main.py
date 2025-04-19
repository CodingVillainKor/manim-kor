from manim import *
from raenim import *
from random import seed

seed(41)


class intro(Scene2D):
    def construct(self):
        data, model, train = [Text(item, font_size=36) for item in ["Data", "Model", "Train"]]
        VGroup(data, model, train).arrange(DOWN, buff=2).shift(UP)
        data1, data2 = [Text(item, font_size=28, color=GREY_B) for item in ["name: \"MNIST\"", "path: \"/data/mnist\""]]
        VGroup(data1, data2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(data, DOWN, buff=0.25).align_to(data, LEFT).shift(RIGHT)
        model1, model2 = [Text(item, font_size=28, color=GREY_B) for item in ["name: \"ConvNet\"", "dim: 256"]]
        VGroup(model1, model2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(model, DOWN, buff=0.25).align_to(model, LEFT).shift(RIGHT)
        train1, train2 = [Text(item, font_size=28, color=GREY_B) for item in ["optim_name: \"Adam\"", "lr: 0.001"]]
        VGroup(train1, train2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(train, DOWN, buff=0.25).align_to(train, LEFT).shift(RIGHT)


        self.playw(LaggedStart(*[FadeIn(item) for item in [data, model, train]], lag_ratio=0.5))
        self.playw(LaggedStart(*[FadeIn(item) for item in [VGroup(data1, data2), VGroup(model1, model2), VGroup(train1, train2)]], lag_ratio=0.5))

        entire = VGroup(data, model, train, data1, data2, model1, model2, train1, train2)
        self.playw(entire.animate.set_opacity(0.5))

        config_text = lambda string: Text(string, font_size=48).set_color_by_gradient(BLUE, TEAL).shift(LEFT*3)
        config = config_text("config.json")
        self.playw(FadeIn(config))
        self.playw(config.animate.become(config_text("config.yaml")))
        self.playw(config.animate.become(config_text("config.py")))

        self.cf.save_state()
        self.play(self.cf.animate.align_to(self.cf.get_top(), DOWN))
        problem_code = Text("from torch.optim import \"Adam\"?", font="Noto Mono", font_size=36).move_to(self.cf.get_center()).set_color_by_gradient(RED_B, RED_E)
        self.playw(FadeIn(problem_code), config.animate.set_opacity(0.5))
        self.playw(LaggedStart(FadeOut(problem_code), Restore(self.cf), lag_ratio=0.5))
        self.playw(Circumscribe(train1), train1.animate.set_opacity(1).set_color(YELLOW))

        entire.add(config)

        code = PythonCode("src/intro.py")
        self.playw(entire.animate.set_opacity(0.0), train1.copy().animate.set_opacity(1), FadeIn(code))
        self.playw(Circumscribe(code.text_slice(1, "Adam")))
        self.playw(Circumscribe(code.text_slice(1, "torch.optim")))
        self.playw(Create(underline:=Underline(code.code)))

        json = Code("src/config.json", language="json").next_to(code, UP)
        self.playw(LaggedStart(FadeIn(json), self.cf.animate.scale(1.5).shift(UP), lag_ratio=0.3))
        self.playw(json.code_lines[10][-7:-1].animate.move_to(code.text_slice(1, "Adam")))

class whatisgetattr(Scene2D):
    def construct(self):
        meaning = CodeText("obj.att", font_size=36).set_color_by_gradient(GREEN_B, GREEN_E)
        self.playw(FadeIn(meaning[:4]))
        self.playw(FadeIn(meaning[4:]))
        getattr_code = CodeText("getattr(obj, \"att\")", font_size=36).set_color_by_gradient(YELLOW_B, YELLOW_E)
        
        self.playw(LaggedStart(meaning.animate.shift(UP), FadeIn(getattr_code), lag_ratio=0.2))
        self.playw_return(getattr_code[:8].animate.shift(LEFT*0.1), getattr_code[8:11].animate.scale(1.5), getattr_code[11].animate.shift(RIGHT*0.3))
        self.playw_return(getattr_code[-6:-1].animate.scale(1.5), getattr_code[-1].animate.shift(RIGHT*0.3))
