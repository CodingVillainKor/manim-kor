from manim import *
from manimdef import NumText, rect, NumBox, texbox, DefaultManimClass, Codes

class TrueAndTrue(DefaultManimClass):
    def construct(self):
        true_and_true = Tex(r"True\quad ", r"and\quad ", r"True")
        true_and_true[1].set_color(GREEN)
        result_true = Tex(r"True")
        self.playw(Write(true_and_true))
        
        true_and_true[0].generate_target()
        true_and_true[2].generate_target()

        true_and_true[0].target.move_to(true_and_true[2])
        true_and_true[2].target.move_to(true_and_true[0])

        self.playw(MoveToTarget(true_and_true[0], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)), 
                   MoveToTarget(true_and_true[2], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)))
        self.playw(FadeTransform(true_and_true, result_true))
        
class FalseAndFalse(DefaultManimClass):
    def construct(self):
        false_and_false = Tex(r"False\quad ", r"and\quad ", r"False")
        false_and_false[1].set_color(GREEN)
        result_false = Tex(r"False")
        self.playw(Write(false_and_false))
        
        false_and_false[0].generate_target()
        false_and_false[2].generate_target()

        false_and_false[0].target.move_to(false_and_false[2])
        false_and_false[2].target.move_to(false_and_false[0])

        self.playw(MoveToTarget(false_and_false[0], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)), 
                   MoveToTarget(false_and_false[2], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)))
        self.playw(FadeTransform(false_and_false, result_false))

class TrueAndFalse(DefaultManimClass):
    def construct(self):
        true_and_false = Tex(r"True\quad ", r"and\quad ", r"False")
        true_and_false[1].set_color(GREEN)
        result_false = Tex(r"False")
        self.playw(Write(true_and_false))
        
        true_and_false[0].generate_target()
        true_and_false[2].generate_target()

        true_and_false[0].target.move_to(true_and_false[2])
        true_and_false[2].target.move_to(true_and_false[0])

        self.playw(MoveToTarget(true_and_false[0], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)), 
                   MoveToTarget(true_and_false[2], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)))
        self.playw(FadeTransform(true_and_false, result_false))


class FalseAndTrue(DefaultManimClass):
    def construct(self):
        false_and_true = Tex(r"False\quad ", r"and\quad ", r"True")
        false_and_true[1].set_color(GREEN)
        result_false = Tex(r"False")
        self.playw(Write(false_and_true))
        
        false_and_true[0].generate_target()
        false_and_true[2].generate_target()

        false_and_true[0].target.move_to(false_and_true[2])
        false_and_true[2].target.move_to(false_and_true[0])

        self.playw(MoveToTarget(false_and_true[0], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)), 
                   MoveToTarget(false_and_true[2], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)))
        self.playw(FadeTransform(false_and_true, result_false))


class TrueOrFalse(DefaultManimClass):
    def construct(self):
        true_or_false = Tex(r"True\quad ", r"or\quad ", r"False")
        true_or_false[1].set_color(GREEN)
        result_true = Tex(r"True")
        self.playw(Write(true_or_false))
        
        true_or_false[0].generate_target()
        true_or_false[2].generate_target()

        true_or_false[0].target.move_to(true_or_false[2])
        true_or_false[2].target.move_to(true_or_false[0])

        self.playw(MoveToTarget(true_or_false[0], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)), 
                   MoveToTarget(true_or_false[2], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)))
        self.playw(FadeTransform(true_or_false, result_true))

class FalseOrTrue(DefaultManimClass):
    def construct(self):
        false_or_true = Tex(r"False\quad ", r"or\quad ", r"True")
        false_or_true[1].set_color(GREEN)
        result_true = Tex(r"True")
        self.playw(Write(false_or_true))
        
        false_or_true[0].generate_target()
        false_or_true[2].generate_target()

        false_or_true[0].target.move_to(false_or_true[2])
        false_or_true[2].target.move_to(false_or_true[0])

        self.playw(MoveToTarget(false_or_true[0], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)), 
                   MoveToTarget(false_or_true[2], path_func = utils.paths.path_along_arc(-TAU * 1 / 3)))
        self.playw(FadeTransform(false_or_true, result_true))

class AFunction(DefaultManimClass):
    def construct(self):
        c = Code("afunc.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(Write(c[:2]), Write(c[2][0::2]))
        self.playw(FadeIn(c[2][1], scale=2))

class BFunction(DefaultManimClass):
    def construct(self):
        c = Code("bfunc.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(Write(c[:2]), Write(c[2][0::2]))
        self.playw(FadeIn(c[2][1], scale=2))

class AandB(DefaultManimClass):
    def construct(self):
        c = Code("aandb.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2]), lag_ratio=0.3))
        a_func = c[2][8][6:9]
        b_func = c[2][8][14:17]

        a_func.generate_target()
        b_func.generate_target()
        a_func.target.move_to(b_func)
        b_func.target.move_to(a_func)

        self.playw(MoveToTarget(a_func, path_func=utils.paths.path_along_arc(-TAU * 1 / 3)),
                   MoveToTarget(b_func, path_func=utils.paths.path_along_arc(-TAU * 1 / 3)))
        
class AandBDifferent(DefaultManimClass):
    def construct(self):
        c = Code("different.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2]), lag_ratio=0.5))
        aandb = c[2][0]
        banda = c[2][2]
        
        banda_band = banda[:-3]
        banda_a = banda[-3:]
        self.playw(aandb.animate.set_color(PURE_GREEN))
        self.playw(banda_band.animate.set_color(PURE_GREEN), FadeOut(banda_a))

class TrueAndFalseDetail(DefaultManimClass):
    def construct(self):
        c = Codes("True ", "and ", "False", buf=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        arr = Arrow(c[0].get_left(), c[2].get_right(), color=GOLD).shift(UP)
        self.playw(Write(c.ob))
        self.playw(Write(arr))
        self.wait(10)

class FalseAndTrueDetail(DefaultManimClass):
    def construct(self):
        c = Codes("False ", "and ", "True", buf=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        result = Text("False", font="Consolas")
        arr = Arrow(c[0].get_left(), c[2].get_right(), color=GOLD).shift(UP)
        self.playw(Write(c.ob))
        self.playw(Write(arr))
        self.wait(2)
        self.playw(Transform(c.ob, result), FadeOut(arr))

class AorB(DefaultManimClass):
    def construct(self):
        c = Code("aorb.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2][:-1]), lag_ratio=0.5))
        self.wait(2)
        self.playw(Write(c[2][-1]))

class TrueOrFalseDetail(DefaultManimClass):
    def construct(self):
        c = Codes("True ", "or ", "False", buf=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
        c[1].set_color(GREEN)
        result = Text("True", font="Consolas", color=GOLD)
        arr = Arrow(c[0].get_left(), c[2].get_right(), color=GOLD).shift(UP)
        self.playw(Write(c.ob))
        self.playw(Write(arr))
        self.wait(2)
        self.playw(Transform(c.ob, result), FadeOut(arr))


class DivZeroDifferent(DefaultManimClass):
    def construct(self):
        c = Code("dividezeros.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2][:-2]), lag_ratio=0.5))
        aor = c[2][-2]
        band = c[2][-1]
        
        error_aor = aor[-4:-1].set_color(PURE_RED)
        error_aor_complement = VGroup(aor[:-4], aor[-1])
        error_band = band[-4:-1].set_color(PURE_RED)
        error_band_complement = VGroup(band[:-4], band[-1])
        self.playw(FadeIn(error_aor), FadeIn(error_band))
        self.playw(Write(error_aor_complement))
        self.playw(Write(error_band_complement))
        
        arrow_aor = Arrow(error_aor_complement[0][0].get_left(), error_aor_complement[0][-1].get_right(), color=PURE_BLUE, buff=0).set_opacity(0.7)
        arrow_band = Arrow(error_band_complement[0][0].get_left(), error_band_complement[0][-1].get_right(), color=PURE_BLUE, buff=0).set_opacity(0.7)
        self.playw(LaggedStart(Write(arrow_aor), FadeOut(error_aor), lag_ratio=0.5))
        self.playw(LaggedStart(Write(arrow_band), FadeOut(error_band), lag_ratio=0.5))


class ListOfList(DefaultManimClass):
    def construct(self):
        c = Code("listinlist.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2][0]), lag_ratio=0.5))
        out_list_code = c[2][0]
        for_code = c[2][2]
        self.playw(Write(for_code))

        if_code = c[2][3]
        self.playw(Write(if_code))
        in_lists = [out_list_code[12:24].copy().add_background_rectangle(BLACK, opacity=0.9), 
                    out_list_code[26:35].copy().add_background_rectangle(BLACK, opacity=0.9), 
                    out_list_code[37:39].copy().add_background_rectangle(BLACK, opacity=0.9), 
                    out_list_code[41:47].copy().add_background_rectangle(BLACK, opacity=0.9)]
        for il in in_lists: il.generate_target(); il.target.move_to(for_code[4:11]).scale(0.8)
        for i, il in enumerate(in_lists[:3]):
            self.playw(MoveToTarget(il))
            il.generate_target()
            il.target.move_to(if_code[7:15])
            self.playw(MoveToTarget(il))
            if i != 2:
                self.playw(FadeOut(il))
            else:
                self.playw(il.background_rectangle.animate.set_color(PURE_RED))
        
class ListOfListSol1(DefaultManimClass):
    def construct(self):
        c = Code("listinlist_sol1.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2][0]), lag_ratio=0.5))
        out_list_code = c[2][0]
        for_code = c[2][2]
        if_code = c[2][3]
        elif_code = c[2][4]
        self.playw(Write(for_code))
        self.playw(Write(if_code))
        self.playw(Write(elif_code))
        

class ListOfListSol2(DefaultManimClass):
    def construct(self):
        c = Code("listinlist_sol2.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.playw(LaggedStart(FadeIn(c[:2]), Write(c[2][0]), lag_ratio=0.5))
        out_list_code = c[2][0]
        for_code = c[2][2]
        if_code = c[2][3]
        last_code = c[2][-1]
        self.playw(Write(for_code))
        self.playw(Write(if_code))
        self.playw(Write(last_code))

class ListOfListSol3(DefaultManimClass):
    def construct(self):
        c = Code("listinlist_sol2.py", language="python", tab_width=4, font="Consolas", background="window", line_spacing=0.7)
        self.add(c)
        not_eq_zero = c[2][3][16:19]
        len_func = VGroup(c[2][3][4:8], c[2][3][15])
        self.wait(2)
        self.playw(FadeOut(not_eq_zero, shift=UP))
        self.playw(FadeOut(len_func, shift=UP))
        