from manim import *
from math import e

def rect(height=0.3, width=1.0, opacity=0.8, 
         stroke_width=DEFAULT_STROKE_WIDTH/2,
         color=[BLUE, YELLOW], stroke_color=WHITE,
         **kwargs):
    return Rectangle(
        height=height,
        width=width,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        **kwargs)

def texbox(*msg, tex_config=dict(), box_config=dict()):
    tex = Tex(*msg, **tex_config)
    box = rect(height=tex.height, width=tex.width, 
               stroke_color=GOLD, **box_config).surround(tex)
    return VGroup(box, tex)

class Scene1(MovingCameraScene):
    def construct(self):
        self.sceneA()
        self.clear()
        self.sceneB()
        self.clear()
        self.sceneC()
        self.clear()
        self.sceneD()
        self.clear()
        self.sceneE()

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

    @staticmethod
    def weighted_sum_hex(hexes, coeffs):
        assert len(hexes) == len(coeffs)
        
        return rgb_to_hex(sum([hex_to_rgb(h)*c for h, c in zip(hexes, coeffs)]))

    def sceneA(self):
        tb1 = texbox("$W_1$", box_config={"color": BLACK, "opacity":1.0}).move_to(ORIGIN)
        r1 = rect(0.5, 0.5).next_to(tb1, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)
        t1 = Text("info1", color=GRAY_A, font_size=DEFAULT_FONT_SIZE*0.5).next_to(r1, UP)
        self.playw(Write(r1), run_time=1.5, wait=0.1)
        self.playw(FadeIn(t1, scale=2))
        self.playw(Write(tb1), run_time=1.5)
        self.add_foreground_mobjects(tb1)

        r1.generate_target()
        t1.generate_target()
        r1.target.next_to(tb1, RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2)
        t1.target.next_to(r1.target, UP)
        r1.target.set_color([YELLOW, BLUE])
        t1.target.set_color([YELLOW, BLUE])

        self.playw(MoveToTarget(r1), MoveToTarget(t1))

    def sceneB(self):
        r1 = rect(0.5, 0.5, color="#FF0000", stroke_color=WHITE)
        r2 = rect(0.5, 0.5, color="#0000FF", stroke_color=WHITE)
        vg1 = VGroup(r1, r2).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10).move_to(ORIGIN)
        t1 = Text("info1", color="#FF0000", font_size=DEFAULT_FONT_SIZE*0.5).next_to(r1, UP)
        t2 = Text("info2", color="#0000FF", font_size=DEFAULT_FONT_SIZE*0.5).next_to(r2, UP)

        self.playw(Write(vg1), wait=0.5)
        self.playw(Write(t1), Write(t2))

        cnum = 0.99
        v = Variable(cnum, "", num_decimal_places=3)
        v_tracker = v.tracker

        
        coeff1 = Tex(f"${round(v_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r1, LEFT)
        coeff2 = Tex(f"${round(1-v_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r2, LEFT)
        vg2 = VGroup(r1, r2, coeff1, coeff2)
        plus = Tex("$+$", font_size=DEFAULT_FONT_SIZE*0.7).move_to(vg2.get_center())
        vg3 = VGroup(r1, r2, t1, t2, coeff1, coeff2, plus)
        self.playw(FadeIn(coeff1), FadeIn(coeff2))
        self.playw(FadeIn(plus))
        self.playw(vg3.animate.shift(UP))
        r3 = rect(0.5, 0.5, stroke_color=WHITE, color=self.weighted_sum_hex(["#FF0000", "#0000FF"], [v_tracker.get_value(), 1-v_tracker.get_value()]))
        equal = Tex("$=$").next_to(r3, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5)
        self.playw(FadeIn(r3), FadeIn(equal))
        r3.add_updater(lambda x: x.set_color(self.weighted_sum_hex(["#FF0000", "#0000FF"], [v_tracker.get_value(), 1-v_tracker.get_value()])).set_stroke_color(WHITE))

        coeff1.add_updater(lambda x: x.become(Tex(f"${round(v_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r1, LEFT)))
        coeff2.add_updater(lambda x: x.become(Tex(f"${round(1-v_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r2, LEFT)))
        cnum = 0.01
        self.playw(v_tracker.animate.set_value(cnum), run_time=3)
        cnum = 0.99
        self.playw(v_tracker.animate.set_value(cnum), run_time=3)

    def sceneC(self):
        r1 = rect(0.5, 0.5, color="#FF0000", stroke_color=WHITE)
        r2 = rect(0.5, 0.5, color="#0000FF", stroke_color=WHITE)
        r3 = rect(0.5, 0.5, color="#00FF00", stroke_color=WHITE)
        vg1 = VGroup(r1, r2, r3).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10).move_to(ORIGIN)
        t1 = Text("info1", color="#FF0000", font_size=DEFAULT_FONT_SIZE*0.5).next_to(r1, UP)
        t2 = Text("info2", color="#0000FF", font_size=DEFAULT_FONT_SIZE*0.5).next_to(r2, UP)
        t3 = Text("info3", color="#00FF00", font_size=DEFAULT_FONT_SIZE*0.5).next_to(r3, UP)
        
        self.playw(Write(vg1), wait=0.5)
        self.playw(Write(t1), Write(t2), Write(t3))

        cnum1 = 0.97
        cnum2 = 0.01
        v1 = Variable(cnum1, "", num_decimal_places=3)
        v2 = Variable(cnum2, "", num_decimal_places=3)
        v1_tracker = v1.tracker
        v2_tracker = v2.tracker

        coeff1 = Tex(f"${round(v1_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r1, LEFT)
        coeff2 = Tex(f"${round(v2_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r2, LEFT)
        coeff3 = Tex(f"${round(1-v1_tracker.get_value()-v2_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r3, LEFT)
        vg21 = VGroup(r1, r2, coeff1, coeff2)
        vg22 = VGroup(r2, r3, coeff2, coeff3)
        plus1 = Tex("$+$", font_size=DEFAULT_FONT_SIZE*0.7).move_to(vg21.get_center())
        plus2 = Tex("$+$", font_size=DEFAULT_FONT_SIZE*0.7).move_to(vg22.get_center())
        vg3 = VGroup(r1, r2, r3, t1, t2, t3, coeff1, coeff2, coeff3, plus1, plus2)

        self.playw(Write(VGroup(coeff1, coeff2, coeff3)))
        self.playw(Write(VGroup(plus1, plus2)))
        self.playw(vg3.animate.shift(UP))

        r4 = rect(0.5, 0.5, stroke_color=WHITE, 
                  color=self.weighted_sum_hex(
                      ["#FF0000", "#0000FF", "#00FF00"], 
                      [v1_tracker.get_value(), v2_tracker.get_value(), 1-v1_tracker.get_value()-v2_tracker.get_value()]))
        equal = Tex("$=$").next_to(r4, LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5)
        self.playw(FadeIn(r4), FadeIn(equal))
        r4.add_updater(lambda x: x.set_color(
            self.weighted_sum_hex(
                ["#FF0000", "#0000FF", "#00FF00"], 
                [v1_tracker.get_value(), v2_tracker.get_value(), 1-v1_tracker.get_value()-v2_tracker.get_value()])).set_stroke_color(WHITE))
        coeff1.add_updater(lambda x: x.become(Tex(f"${round(v1_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r1, LEFT)))
        coeff2.add_updater(lambda x: x.become(Tex(f"${round(v2_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r2, LEFT)))
        coeff3.add_updater(lambda x: x.become(Tex(f"${round(1-v1_tracker.get_value()-v2_tracker.get_value(), 3):.3f}\\times$", font_size=DEFAULT_FONT_SIZE*0.7).next_to(r3, LEFT)))

        cnum1 = 0.01
        cnum2 = 0.97
        self.playw(v1_tracker.animate.set_value(cnum1), v2_tracker.animate.set_value(cnum2), run_time=3)
        cnum2 = 0.01
        self.playw(v2_tracker.animate.set_value(cnum2), run_time=3)
        cnum1 = 0.33
        cnum2 = 0.33
        self.playw(v1_tracker.animate.set_value(cnum1), v2_tracker.animate.set_value(cnum2), run_time=3)

    def sceneD(self):
        r1 = rect(0.5, 0.5, color="#FF0000", stroke_color=WHITE)
        r2 = rect(0.5, 0.5, color="#0000FF", stroke_color=WHITE)
        vg1 = VGroup(r1, r2).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10).move_to(ORIGIN)
        title_inprd = Text("Inner Product").next_to(vg1, UP).shift(UP)
        self.playw(Write(vg1))
        self.playw(Write(title_inprd))

        r1.generate_target()
        r2.generate_target()
        r1.target.move_to(ORIGIN)
        r2.target.move_to(ORIGIN)

        self.play(MoveToTarget(r1), MoveToTarget(r2))
        self.playw(Transform(vg1, Text("6.21")))

    def sceneE(self):
        query = rect(0.5, 0.5)
        keys = VGroup(
            rect(0.5, 0.5, color=RED), 
            rect(0.5, 0.5, color=BLUE),
            rect(0.5, 0.5, color=GOLD),
            rect(0.5, 0.5, color=GREEN)
        ).arrange(DOWN).next_to(query, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*10)
        qkg = VGroup(query, keys).move_to(ORIGIN)

        qt = Text("Query", font_size=DEFAULT_FONT_SIZE*0.7).next_to(query, DOWN)
        kt = Text("Keys", font_size=DEFAULT_FONT_SIZE*0.7).next_to(keys, DOWN)

        self.playw(Write(query))
        self.playw(Write(qt))
        self.playw(Write(keys))
        self.playw(Write(kt))
        values = keys.copy()
        self.add(values)

        self.playw(FadeOut(qt), FadeOut(kt))
        
        tbq = texbox("$W_q$", box_config={"color": BLACK, "opacity":1.0}).next_to(query, UP).shift(UP).shift(UP)
        tbk = texbox("$W_k$", box_config={"color": BLACK, "opacity":1.0}).move_to((keys.get_x(), tbq.get_y(), 0))
        self.playw(Write(tbq), Write(tbk))

        query.generate_target()
        keys.generate_target()
        query.target.next_to(tbq, UP).shift(UP).shift(UP)
        keys.target.next_to(tbk, UP).shift(UP)
        self.playw(MoveToTarget(query), MoveToTarget(keys), self.camera.frame.animate.shift(UP*3)\
                   .set(width=self.camera.frame_width*1.5))
        
        self.playw(VGroup(tbq, tbk, query, keys).animate.shift(LEFT).shift(LEFT))

        tbv = texbox("$W_v$", box_config={"color": BLACK, "opacity":1.0}).move_to((values.get_x(), tbq.get_y(), 0))
        self.playw(Write(tbv))

        values.generate_target()
        values.target.next_to(tbv, UP).shift(UP)
        for i in range(len(values)):
            values.target[i].set_color(self.weighted_sum_hex([values.target[i].get_color().hex, "#000000"], [0.6, 0.4])).set_stroke_color(WHITE)
        
        self.playw(MoveToTarget(values))

        qt.next_to(query, UP)
        kt.next_to(keys, UP)
        vt = Text("Values", font_size=DEFAULT_FONT_SIZE*0.7).next_to(values, UP)
        self.playw(self.camera.frame.animate.move_to(VGroup(tbq, tbk, tbv, query, keys, values).get_center()))
        self.playw(Write(qt))
        self.playw(Write(kt))
        self.playw(Write(vt))
        self.playw(FadeOut(qt, kt, vt))

        l1, l2, l3, l4 = 1.7, -1.3, 3.9, 0.3
        logit1 = Text(f"{l1:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[0])
        query.save_state()
        self.play(query.animate.move_to(keys[0]))
        self.playw(query.animate.restore(), FadeTransform(keys[0], logit1))
        logit2 = Text(f"{l2:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[1])
        query.save_state()
        self.play(query.animate.move_to(keys[1]))
        self.playw(query.animate.restore(), FadeTransform(keys[1], logit2))
        logit3 = Text(f"{l3:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[2])
        query.save_state()
        self.play(query.animate.move_to(keys[2]))
        self.playw(query.animate.restore(), FadeTransform(keys[2], logit3))
        logit4 = Text(f"{l4:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[3])
        query.save_state()
        self.play(query.animate.move_to(keys[3]))
        self.playw(query.animate.restore(), FadeTransform(keys[3], logit4))
        
        el1, el2, el3, el4 = e**l1, e**l2, e**l3, e**l4
        w1 = Text(f"{el1:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[0])
        w2 = Text(f"{el2:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[1])
        w3 = Text(f"{el3:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[2])
        w4 = Text(f"{el4:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[3])
        self.play(FadeTransform(logit1, w1))
        self.play(FadeTransform(logit2, w2))
        self.play(FadeTransform(logit3, w3))
        self.playw(FadeTransform(logit4, w4))

        sum_el = el1 + el2 + el3 + el4
        p1 = Text(f"{el1/sum_el:.3f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[0])
        p2 = Text(f"{el2/sum_el:.3f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[1])
        p3 = Text(f"{el3/sum_el:.3f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[2])
        p4 = Text(f"{el4/sum_el:.3f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[3])
        self.play(FadeTransform(w1, p1))
        self.play(FadeTransform(w2, p2))
        self.play(FadeTransform(w3, p3))
        self.playw(FadeTransform(w4, p4))

        time1 = Tex("$\\times$").move_to(VGroup(p1, values[0]).get_center())
        time2 = Tex("$\\times$").move_to(VGroup(p2, values[1]).get_center())
        time3 = Tex("$\\times$").move_to(VGroup(p3, values[2]).get_center())
        time4 = Tex("$\\times$").move_to(VGroup(p4, values[3]).get_center())
        self.playw(LaggedStart(Write(time1), Write(time2), Write(time3), Write(time4), lag_ratio=0.5))
        
        qt.next_to(query, UP)
        sm_qkt = Tex("softmax($QK^T$)", font_size=DEFAULT_FONT_SIZE*0.7).next_to(p1, UP)
        vt.next_to(values, UP)
        self.playw(Write(qt))
        self.playw(Write(sm_qkt))
        self.playw(Write(vt))
        self.playw(FadeOut(qt, sm_qkt, vt))

        qkv1 = VGroup(p1, time1, values[0])
        qkv2 = VGroup(p2, time2, values[1])
        qkv3 = VGroup(p3, time3, values[2])
        qkv4 = VGroup(p4, time4, values[3])
        all_qkv = VGroup(qkv1, qkv2, qkv3, qkv4)
        center_point = all_qkv.get_center()
        qkv1.generate_target()
        qkv2.generate_target()
        qkv3.generate_target()
        qkv4.generate_target()
        qkv1.target.move_to(center_point)
        qkv2.target.move_to(center_point)
        qkv3.target.move_to(center_point)
        qkv4.target.move_to(center_point)
        final_qkv = rect(0.5, 0.5, color=[GRAY, GOLD]).move_to(center_point)
        final_qkv.move_to([final_qkv.get_x(), query.get_y(), 0])
        wst = Text("Weighted sum", font_size=DEFAULT_FONT_SIZE*0.7, color=YELLOW).move_to(center_point)
        self.playw(
            MoveToTarget(qkv1), 
            MoveToTarget(qkv2), 
            MoveToTarget(qkv3), 
            MoveToTarget(qkv4), 
            FadeTransform(all_qkv, final_qkv),
            FadeOut(wst, scale=1.5)
        )

        arrow_qqkv = Arrow(query.get_right(), final_qkv.get_left(), buff=0.3, color=GOLD)
        self.playw(
            Write(arrow_qqkv)
        )



    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)