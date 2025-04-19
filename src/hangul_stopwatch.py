from manimdef import PythonCode, DefaultManimClass
from manim import *

class HangulUnicode(DefaultManimClass):
    def construct(self):
        start_ga, start_num = "가", ord("가")
        texts_g = []
        ords_g = []
        for i in range(21):
            uni_ga = VGroup(*[Text(chr(start_num +i*28 + j), font_size=24) for j in range(28)])\
                .arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.8)
            if i: uni_ga.stretch_to_fit_width(texts_g[0].width)
            ord_ga = VGroup(*[Text(f"{ord('가')+i*28+j}", font="Consolas", font_size=24) for j in range(28)])\
                .arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.8).move_to(uni_ga).stretch_to_fit_width(uni_ga.width)
            texts_g.append(uni_ga)
            ords_g.append(ord_ga)
        total_text_g = VGroup(*texts_g).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.8)
        for i in range(21):
            ords_g[i].move_to(texts_g[i])
            total_ords_g = VGroup(*ords_g)
        self.camera.frame.move_to(texts_g[3][4])
        

        text_n = []
        for i in range(21):
            uni_gag = VGroup(*[Text(chr(start_num +28*21+i*28 + j), font_size=24) for j in range(28)])\
                .arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.8)
            if i: uni_gag.stretch_to_fit_width(text_n[0].width)
            text_n.append(uni_gag)
        total_text_n = VGroup(*text_n).arrange(DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*0.8).next_to(total_text_g, RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)
        total_text_n[0][0].set_color(YELLOW_E)
        self.playw(FadeIn(total_text_g))
        self.playw(FadeOut(total_text_g), FadeIn(total_ords_g))
        self.playw(FadeOut(total_ords_g), FadeIn(total_text_g))
        self.playw(FadeIn(total_text_n))

        self.playw(self.camera.frame.animate.move_to(total_text_g[3][-1]), run_time=2)
        self.playw(self.camera.frame.animate.move_to(total_text_g[-1][-1]), run_time=2)
        self.playw(self.camera.frame.animate.move_to(total_text_n[3][4]), run_time=2)
        self.playw(self.camera.frame.animate.move_to(total_text_n[3][-1]), run_time=2)

class StopWatch(DefaultManimClass):
    def construct(self):
        hhmm_colon = Text(":", font="Consolas")
        mmss_colon = Text(":", font="Consolas")
        second, minute, hour = 55, 0, 0
        s_text, m_text, h_text = [self.get_twodigit_text(item) for item in [second, minute, hour]]
        self.playw(FadeIn(VGroup(h_text, hhmm_colon, m_text, mmss_colon, s_text).arrange(RIGHT)))
        self.wait(1)
        for _ in range(10):
            anims = []
            second+=1
            if second%60==0:
                second=0
                minute += 1
                if minute == 60:
                    hour += 1
                    anims.append(FadeOut(h_text, shift=UP))
                    h_text = self.get_twodigit_text(hour).move_to(h_text)
                    anims.append(FadeIn(h_text, shift=UP))
                    minute=0
                anims.append(FadeOut(m_text, shift=UP))
                m_text = self.get_twodigit_text(minute).move_to(m_text)
                anims.append(FadeIn(m_text, shift=UP))
            anims.append(FadeOut(s_text, shift=UP))
            s_text = self.get_twodigit_text(second).move_to(s_text)
            anims.append(FadeIn(s_text, shift=UP))
            self.play(*anims, run_time=0.5)
            self.wait(0.5)
            
    def get_twodigit_text(self, num):
        return Text(f"{num:02d}", font="Consolas")
    
_cho  = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
_jung = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
_jong = "xㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
class StopWatchCJJ(DefaultManimClass):
    def construct(self):
        hhmm_colon = Text("+", font="Consolas", fill_opacity=0.0)
        mmss_colon = Text("+", font="Consolas", fill_opacity=0.0)
        second, minute, hour = len(_jong)-4, len(_jung)-1, 0
        s_text = self.get_jong_text(second)
        m_text = self.get_jung_text(minute)
        h_text = self.get_cho_text(hour)
        self.playw(FadeIn(VGroup(h_text, hhmm_colon, m_text, mmss_colon, s_text).arrange(RIGHT)))
        self.wait(1)
        for _ in range(12):
            anims = []
            second+=1
            if second%len(_jong)==0:
                second=0
                minute += 1
                if minute == len(_jung):
                    hour += 1
                    anims.append(FadeOut(h_text, shift=UP))
                    h_text = self.get_cho_text(hour).move_to(h_text)
                    anims.append(FadeIn(h_text, shift=UP))
                    minute=0
                anims.append(FadeOut(m_text, shift=UP))
                m_text = self.get_jung_text(minute).move_to(m_text)
                anims.append(FadeIn(m_text, shift=UP))
            anims.append(FadeOut(s_text, shift=UP))
            s_text = self.get_jong_text(second).move_to(s_text)
            anims.append(FadeIn(s_text, shift=UP))
            self.play(*anims, run_time=0.5)
            self.wait(0.5)
            
    def get_cho_text(self, num):
        return Text(f"{_cho[num]}")
    def get_jung_text(self, num):
        return Text(f"{_jung[num]}")
    def get_jong_text(self, num):
        return Text(f"{_jong[num]}")