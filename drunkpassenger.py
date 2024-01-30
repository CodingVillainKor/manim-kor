from manimdef import DefaultManimClass, PythonCode
from manim import *

_seat_num = [0]

class DrunkPassenger(DefaultManimClass):
    def construct(self):
        self.camera.frame.scale(2.5)
        seats = self.build_seats()
        self.playw(Write(seats))

        skewed_nums = [14, 25, 98, 100]
        line_start = 0
        passenger_num = 0
        for i in range(100):
            passenger = self.generate_passenger(passenger_num:=passenger_num+1)\
                .next_to(seats, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*3)
            self.playw(Write(passenger))
            if i == 0:
                self.add_foreground_mobjects(passenger[1])
                self.playw(passenger[0].animate.set_fill([PURE_RED, PURPLE_E], opacity=1.0))
                skewed_num = skewed_nums.pop(0)
                seat_number = skewed_num
                run_time = 1
                draw_line, line_end = True, seat_number-1
            elif i+1 != skewed_num:
                seat_number = i+1
                run_time = 0.2
                draw_line = False
            elif i+1 == skewed_num:
                skewed_num = skewed_nums.pop(0) if skewed_nums else 1
                seat_number = skewed_num
                self.playw(seats[i//6][i%6][0].animate.set_fill(PURE_BLUE, opacity=1.0), 
                          FadeIn(exclm:=Text("!", font="Consolas").next_to(passenger, UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.5), scale=2.0))
                self.playw(seats[i//6][i%6][0].animate.set_fill(BLACK, opacity=0.0), FadeOut(exclm))
                run_time = 1
                draw_line, line_end = True, seat_number-1
            self.playw(passenger.animate.move_to(seats[(seat_number-1)//6].get_center()), run_time=run_time)
            try:
                self.playw(passenger.animate.scale(0.6).move_to(seats[(seat_number-1)//6][(seat_number-1)%6][0]), run_time=run_time)
            except:
                breakpoint()
            if draw_line:
                line = Line(seats[line_start//6][line_start%6][0].get_center(), seats[line_end//6][line_end%6][0].get_center(), color=RED_C)
                self.playw(Write(line))
                line_start = line_end
            
        self.playw(self.camera.frame.animate.scale(0.5).move_to(seats[99//6][99%6]))

    def build_seats(self):
        _square_len = 1.
        lines_list = [self.build_line() for i in range(16)]
        last_line = VGroup(*[self.numbered_square(_seat_num, side_length=_square_len) for _ in range(4)]).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5)
        last_line[2:].next_to(last_line[1], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10)
        lines = VGroup(*lines_list, last_line).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)

        return lines

    def build_line(self, _square_len=1.):
        line = VGroup(*[self.numbered_square(_seat_num, side_length=_square_len) for _ in range(6)]).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5)
        line[3:].next_to(line[2], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10)
        return line
    
    def generate_passenger(self, passenger_num):
        circle = Circle(radius=0.5).set_fill(BLACK, opacity=1.0)
        num_text = Text(f"{passenger_num}", font="Consolas", font_size=36).move_to(circle)
        self.add_foreground_mobjects(num_text)
        return VGroup(circle, num_text)
    
    def numbered_square(self, num, side_length):
        square = Square(side_length=side_length)
        num[0] += 1
        text = Text(f"{num[0]}", font="Consolas", font_size=30).move_to(square)\
            .next_to(square, UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.2).align_to(square, LEFT)
        self.add_foreground_mobjects(text)
        return VGroup(square, text)
    

class DPCode(DefaultManimClass):
    def construct(self):
        c = PythonCode("dp.py")
        self.camera.frame.scale(1.6)
        self.playw(FadeIn(c.frame))
        self.playw(Write(c.code[:11]), run_time=1.5)

        self.playw(self.camera.frame.animate.scale(0.6).move_to(c.code[3:5]))
        self.playw(Write(highlight:=c.code[3].copy().set_color("#FFFF00")))
        self.wait(2)
        si, ei = c.find_text(4, "[False] * 100")
        self.playw(FadeOut(highlight), Write(highlight2:=c.code[3][si:ei].copy().set_color("#FFFF00")))
        self.playw(FadeOut(highlight2))

        self.playw(Write(highlight:=c.code[4].copy().set_color("#FFFF00")))
        self.playw(FadeOut(highlight))
        si_lc, ei_lc = c.find_text(5, "[i for i in range(100)]")
        replacement = Text("[0, 1, 2, 3, ..., 99]", font="Consolas", font_size=24)\
            .move_to(c.code[4][si_lc:ei_lc]).align_to(c.code[4][si_lc:ei_lc], LEFT)
        self.playw(FadeOut(c.code[4][si_lc:ei_lc]), FadeIn(replacement))
        c.code[4] = c.code[4][:si_lc] + replacement

        self.play(Write(highlight:=c.code[5].copy().set_color("#FFFF00")),
                  self.camera.frame.animate.scale(1.6).move_to(c.frame))
        self.playw(FadeOut(highlight))
        self.wait(2)

        # drunk passenger: if i==0
        si_if, ei_if = c.find_text(7, "if i==0")
        si_ch, ei_ch = c.find_text(7, "choice(seat_remainder)")
        si_se, ei_se = c.find_text(7, "seat_num")
        self.playw(Write(highlight:=c.code[6][si_if:ei_if].copy().set_color("#FFFF00")))
        self.playw(Write(highlight2:=c.code[6][si_ch:ei_ch].copy().set_color("#FFFF00")))
        self.playw(FadeOut(highlight), FadeOut(highlight2, target_position=c.code[6][si_se:ei_se], scale=0.5))

        self.playw(Write(highlight:=c.code[3].copy().set_color("#FFFF00")))
        self.playw(Write(highlight2:=c.code[7].copy().set_color("#FFFF00")))
        self.wait()
        self.playw(FadeOut(highlight, highlight2))

        self.playw(Write(highlight:=c.code[4].copy().set_color("#FFFF00")))
        self.playw(Write(highlight2:=c.code[8].copy().set_color("#FFFF00")))
        
        self.playw(VGroup(replacement[7:9], highlight[-1][7:9]).animate.set_fill(BLACK, 0.0))
        self.playw(FadeOut(highlight, highlight2))

        # non-drunk passenger
        si_i0, ei_i0 = c.find_text(7, "i==0")
        self.playw(Write(highlight:=c.code[6][si_i0:ei_i0].copy().set_color(PURE_RED)))
        ft = Text("False", font="Consolas", font_size=24)\
            .move_to(c.code[6][si_i0:ei_i0]).align_to(c.code[6][si_i0:ei_i0], LEFT)
        ft.stretch_to_fit_width(ft.width*3/5)
        self.playw(FadeOut(highlight), c.code[6][si_i0:ei_i0].animate.set_fill(BLACK, 0.0), FadeIn(ft))
        si_io, ei_io = c.find_text(7, "or")
        self.playw(FadeOut(ft), c.code[6][si_io:ei_io].animate.set_fill(BLACK, 0.0))

        si_oc, ei_oc = c.find_text(7, "occupied[i] == True")
        self.playw(Write(highlight:=c.code[6][si_oc:ei_oc].copy().set_color("#FFFF00")))
        self.playw(FadeOut(highlight))
        self.playw(c.code[6].animate.set_fill(WHITE, 1.0))
        self.wait(2)
        self.playw(self.camera.frame.animate.move_to(ORIGIN))

        # final seat_num: 99th passenger's seat number
        si_sn, ei_sn = c.find_text(11, "if seat_num == 99")
        self.playw(Write(highlight:=c.code[10][si_sn:ei_sn].copy().set_color(PURE_RED)))
        self.wait(3)
        self.playw(FadeOut(highlight))
        self.wait(2)

        # function call loop
        self.playw(Write(c.code[12:]), run_time=1.)
        self.playw(Write(highlight:=c.code[15].copy().set_color(PURE_GREEN)))
