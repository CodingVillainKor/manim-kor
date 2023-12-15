from manim import *
from manimdef import NumText, rect, NumBox, texbox, DefaultManimClass
from math import e

_dist_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

class TranslationScene(DefaultManimClass):
    def construct(self):
        # self.camera.frame.save_state()
        # self.sceneA()
        # self.clear()
        # self.camera.frame.move_to(ORIGIN)
        # encdec = self.sceneB()
        # mode = 2 # 0, 1, 2
        # if mode == 0:
        #     encdec = self.sceneC(encdec)
        #     encdec = self.sceneD(encdec)
        #     encdec = self.sceneE(encdec)
        # elif mode == 1:
        #     encdec = self.sceneE2(encdec)
        # else:
        #     encdec = self.sceneE3(encdec)
        # self.clear()
        # self.camera.frame.restore()
        self.sceneF()
        # # Question about translation
        # question = Tex("What is translation?")
        # self.playw(Write(question))
        # self.playw(FadeOut(question))

        # # Explanation of Translation
        # explanation = Tex("It's converting a sentence from language A to language B")
        # self.playw(Write(explanation))
        # self.playw(FadeOut(explanation))

        # # Setting aside AI and learning complexities
        # note = Tex("Let's set aside AI and learning for now")
        # self.playw(Write(note))
        # self.playw(FadeOut(note))

        # # Introduction to the translation process
        # process_intro = Tex("Let's think about the translation process")
        # self.playw(Write(process_intro))
        # self.playw(FadeOut(process_intro))

        # # Example sentence
        # korean_sentence = Tex(r'"아 퇴사 하고 싶다"')
        # self.playw(Write(korean_sentence))

        # # Placeholder for English translation
        # english_placeholder = Tex("Translating to English...")
        # self.playw(Transform(korean_sentence, english_placeholder))

        # # Indicate unknown translated sentence
        # unknown = Tex("The exact English translation is not yet known")
        # self.playw(Write(unknown))
        # self.playw(FadeOut(unknown, english_placeholder))

        # # Information about original sentence
        # original_info = Tex("But all information of the original sentence is known")
        # self.playw(Write(original_info))
        # self.playw(FadeOut(original_info))

    def sceneA(self):
        # Introduction of Transformer's basic operation
        hotdog_kor = Tex(r'핫도그 세 개 주세요', color=GOLD)
        self.playw(Write(hotdog_kor))
        hotdog_eng = Tex(r'Please Hotdog World', color=GREEN)
        self.playw(FadeTransform(hotdog_kor, hotdog_eng))
        self.clear()

        quitjob_kor = Tex(r'아 퇴사 하고 싶다', color=GOLD)
        self.playw(Write(quitjob_kor))
        quitjob_eng = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=GREEN,
                          arg_separator=" ").next_to(quitjob_kor, buff = _dist_buf*4)
        quitjob = VGroup(quitjob_kor, quitjob_eng)
        self.playw(FadeIn(quitjob_eng), self.camera.frame.animate.move_to(quitjob).scale(1.3))

        quitjob_eng.generate_target()
        quitjob_eng.target.set_opacity(0.3)
        self.playw(MoveToTarget(quitjob_eng))
        quitjob_kor.save_state()
        self.play(quitjob_kor.animate.scale(1.4), run_time=0.7)
        self.playw(Restore(quitjob_kor), run_time=0.7)

        self.playw(FadeOut(quitjob_eng))
        self.playw(FadeIn(quitjob_eng[3]))
        self.playw(FadeOut(quitjob_eng[3]))

        self.playw(FadeIn(quitjob_eng[0]))
        self.playw(quitjob_eng[0].animate.set_opacity(1.0))
        self.playw(FadeIn(quitjob_eng[1]))
        self.playw(quitjob_eng[1].animate.set_opacity(1.0))
        self.playw(FadeIn(quitjob_eng[2]))
        self.playw(quitjob_eng[2].animate.set_opacity(1.0))
        self.playw(FadeIn(quitjob_eng[3]))
        self.playw(quitjob_eng[3].animate.set_opacity(1.0))
        self.playw(FadeIn(quitjob_eng[4]))
        self.playw(quitjob_eng[4].animate.set_opacity(1.0))
        self.playw(FadeIn(quitjob_eng[5]))
        self.playw(quitjob_eng[5].animate.set_opacity(1.0))
        self.playw(FadeIn(quitjob_eng[6]))
        self.playw(quitjob_eng[6].animate.set_opacity(1.0))
        self.playw(FadeOut(quitjob_eng))

        
        self.playw(FadeIn(quitjob_eng[3]))
        self.playw(FadeIn(quitjob_eng[5]))
        self.playw(FadeOut(quitjob_eng[3], quitjob_eng[5]))

        
        self.play(FadeIn(quitjob_eng[0]))
        self.play(FadeIn(quitjob_eng[1]))
        self.play(FadeIn(quitjob_eng[2]))
        self.play(FadeIn(quitjob_eng[3]))
        self.play(FadeIn(quitjob_eng[4]))
        self.play(FadeIn(quitjob_eng[5]))
        self.play(FadeIn(quitjob_eng[6]))

        quitjob_kor.save_state()
        self.play(quitjob_kor.animate.scale(1.4), run_time=0.7)
        self.playw(Restore(quitjob_kor), run_time=0.7)
        
    def sceneB(self):
        # Load your image
        image = ImageMobject("attentionisallyouneed.png")  # Replace 'your_image.png' with your file name

        image.scale(1.3)  # Adjust the scale as needed
        image.shift(UP*0.3)

        # Add the image to the scene
        self.playw(FadeIn(image))

        enc = rect(height=2.2, width=1.5, color=TEAL)
        dec = rect(height=3.1, width=1.5, color=ORANGE).next_to(enc, buff=_dist_buf).align_to(enc, DOWN)
        encdec = VGroup(enc, dec).move_to(ORIGIN).shift(UP*0.3)
        self.playw(FadeOut(image), FadeIn(encdec))

        quitjob_eng = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=PURE_GREEN,
                    arg_separator=" ").scale(0.7).next_to(dec, UP, buff=_dist_buf*1.5)

        for i in [3, 2, 1, 0, 4, 5, 6]:
            self.play(FadeIn(quitjob_eng[i], target_position=dec.get_corner(UP)))
        self.wait()
        self.playw(FadeOut(quitjob_eng))

        for i in range(7):
            self.play(FadeIn(quitjob_eng[i], target_position=dec.get_corner(UP)))
        self.wait()
        self.playw(FadeOut(quitjob_eng))

        quitjob_kor = Tex(r'아', r'퇴사', r'하고', r'싶다', color=GOLD,
                          arg_separator=" ").scale(0.7).next_to(enc, DOWN, buff=_dist_buf*1.5)
        self.playw(Write(quitjob_kor))
        self.playw(FadeOut(quitjob_kor, target_position=enc.get_corner(DOWN), scale=0.3))

        colors_ = [TEAL_E, RED_D, YELLOW_C, BLUE_D]
        quitjob_kor_enc = Tex(r'아', r'퇴사', r'하고', r'싶다',
                          arg_separator=" ").scale(0.5).next_to(enc, UP, buff=_dist_buf*1.5).set_color_by_gradient(*colors_)
        self.playw(FadeIn(quitjob_kor_enc, target_position=enc.get_corner(UP), scale=0.3))
        enc_out = VGroup(*[rect() for i in range(4)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*colors_).next_to(enc, UP, buff=_dist_buf*1.5)
        self.playw(LaggedStart(*[FadeTransform(quitjob_kor_enc[i], enc_out[i]) for i in range(len(enc_out))]))
        self.playw(FadeIn(image))
        self.playw(FadeIn(enc_out))
        self.playw(FadeOut(image))


        quitjob_eng_input = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        
        self.playw(FadeIn(quitjob_eng[2]))
        self.playw(Write(quitjob_eng_input[:2]), FadeOut(quitjob_eng[2]))
        self.playw(FadeOut(quitjob_eng_input[:2], scale=0.5, target_position=dec.get_corner(DOWN)))
        dec_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, DARK_BLUE, PURPLE]
        dec_out = VGroup(*[rect() for i in range(7)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        self.playw(FadeIn(dec_out[:2], scale=0.5, target_position=dec.get_corner(UP)))
        quitjob_eng[2].save_state()
        quitjob_eng[2].next_to(dec_out[1], UP)
        self.playw(FadeIn(quitjob_eng[2], scale=0.5, target_position=dec_out[1]))
        self.playw(FadeOut(quitjob_eng[2], dec_out[:2]))
        quitjob_eng[2].restore()

        quitjob_eng_input_sos = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        self.playw(FadeIn(quitjob_eng[0]))
        self.playw(Write(quitjob_eng_input_sos[0]), FadeOut(quitjob_eng[0]))
        self.playw(FadeOut(quitjob_eng_input_sos[0], scale=0.5, target_position=dec.get_corner(DOWN)))
        self.playw(FadeIn(dec_out[0], scale=0.5, target_position=dec.get_corner(UP)))
        quitjob_eng[0].save_state()
        quitjob_eng[0].next_to(dec_out[0], UP)
        self.playw(FadeIn(quitjob_eng[0], scale=0.5, target_position=dec_out[0]))
        self.playw(FadeOut(quitjob_eng[0], dec_out[0]))
        quitjob_eng[0].restore()

        quitjob_eng_eos = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', r'[EOS]', color=PURE_GREEN,
                    arg_separator=" ").scale(0.5).next_to(dec, UP, buff=_dist_buf*1.5)
        dec_out_eos = VGroup(*[rect() for i in range(8)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        self.playw(FadeIn(quitjob_eng_eos[-1]))
        self.playw(Write(quitjob_eng_input_sos), FadeOut(quitjob_eng_eos[-1]))
        self.playw(FadeOut(quitjob_eng_input_sos, scale=0.5, target_position=dec.get_corner(DOWN)))
        self.playw(FadeIn(dec_out_eos, scale=0.5, target_position=dec.get_corner(UP)))
        quitjob_eng_eos[-1].save_state()
        quitjob_eng_eos[-1].next_to(dec_out_eos[-1], UP)
        self.playw(FadeIn(quitjob_eng_eos[-1], scale=0.5, target_position=dec_out_eos[-1]))
        self.playw(FadeOut(quitjob_eng_eos[-1], dec_out_eos))
        quitjob_eng_eos[-1].restore()
        
        self.playw(FadeOut(enc_out))

        return encdec

    def sceneC(self, encdec):
        enc, dec = encdec
        quitjob_kor_in = Tex(r'아', r'퇴사', r'하고', r'싶다', color=GOLD,
                             arg_separator=" ").scale(0.5).next_to(enc, DOWN, buff=_dist_buf*1.5)
        quitjob_eng_in = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                             arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        enc_colors = [TEAL_E, RED_D, YELLOW_C, BLUE_D]
        dec_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, DARK_BLUE, PURPLE]
        enc_out = VGroup(*[rect() for i in range(4)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*enc_colors).next_to(enc, UP, buff=_dist_buf*1.5)
        dec_out = VGroup(*[rect() for i in range(8)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        quitjob_kor_out = Tex(r'아', r'퇴사', r'하고', r'싶다',
                              arg_separator=" ").scale(0.5).next_to(enc_out, UP, buff=_dist_buf).set_color_by_gradient(*enc_colors)
        quitjob_eng_out = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', r'[EOS]', color=PURE_GREEN,
                              arg_separator=" ").scale(0.5).next_to(dec_out, UP, buff=_dist_buf)

        #for i in range(len(quitjob_eng_in)):
        for i in range(2):
            self.playw(Write(quitjob_kor_in))
            self.playw(FadeOut(quitjob_kor_in, scale=0.5, target_position=enc.get_corner(DOWN)))
            self.playw(FadeIn(enc_out, scale=0.5, target_position=enc.get_corner(UP)))
            self.play(FadeIn(quitjob_kor_out))
            self.playw(FadeOut(quitjob_kor_out))
            self.playw(Write(quitjob_eng_in[:i+1]))
            self.playw(FadeOut(quitjob_eng_in[:i+1], scale=0.5, target_position=dec.get_corner(DOWN)))
            self.playw(FadeIn(dec_out[:i+1], scale=0.5, target_position=dec.get_corner(UP)))
            self.playw(Write(quitjob_eng_out[i]))
            self.playw(FadeOut(quitjob_eng_out[i], scale=0.5, target_position=dec_out[i]))
            self.playw(FadeOut(enc_out, dec_out[:i+1]))

        return encdec
    
    def sceneD(self, encdec):
        enc, dec = encdec
        quitjob_eng_in_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        quitjob_eng_in_aft = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        dec_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, DARK_BLUE, PURPLE]
        dec_out = VGroup(*[rect() for i in range(8)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        quitjob_eng_out_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        quitjob_eng_out_aft = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', r'[EOS]', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        
        self.playw(FadeIn(quitjob_eng_in_bef))
        self.playw(TransformMatchingTex(quitjob_eng_in_bef, quitjob_eng_in_aft))
        self.playw(FadeOut(quitjob_eng_in_aft, scale=0.5, target_position=dec.get_corner(DOWN)))

        self.playw(FadeIn(dec_out, scale=0.5, target_position=dec.get_corner(UP)))
        self.playw(FadeIn(quitjob_eng_out_bef))
        self.playw(TransformMatchingTex(quitjob_eng_out_bef, quitjob_eng_out_aft))

        self.playw(LaggedStart(*[FadeOut(quitjob_eng_out_aft[i], scale=0.8, target_position=dec_out[i]) for i in range(len(dec_out))], lag_ratio=0.2))
        self.playw(FadeOut(dec_out))
        return encdec

    def sceneE(self, encdec):
        enc, dec = encdec
        quitjob_kor = Tex(r'아', r'퇴사', r'하고', r'싶다', color=GOLD,
                          arg_separator=" ").scale(0.7).next_to(enc, DOWN, buff=_dist_buf*1.5)
        self.playw(Write(quitjob_kor))
        self.playw(FadeOut(quitjob_kor, target_position=enc.get_corner(DOWN), scale=0.3))

        enc_colors = [TEAL_E, RED_D, YELLOW_C, BLUE_D]
        quitjob_kor_enc = Tex(r'아', r'퇴사', r'하고', r'싶다',
                          arg_separator=" ").scale(0.5).next_to(enc, UP, buff=_dist_buf*1.5).set_color_by_gradient(*enc_colors)
        self.playw(FadeIn(quitjob_kor_enc, target_position=enc.get_corner(UP), scale=0.3))
        enc_out = VGroup(*[rect() for i in range(4)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*enc_colors).next_to(enc, UP, buff=_dist_buf*1.5)
        self.playw(LaggedStart(*[FadeTransform(quitjob_kor_enc[i], enc_out[i]) for i in range(len(enc_out))], lag_ratio=0.1))

        quitjob_eng_in_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        quitjob_eng_in_aft = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        dec_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, DARK_BLUE, PURPLE]
        dec_out = VGroup(*[rect() for i in range(8)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        quitjob_eng_out_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        quitjob_eng_out_aft = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', r'[EOS]', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        
        self.playw(FadeIn(quitjob_eng_in_bef))
        self.playw(TransformMatchingTex(quitjob_eng_in_bef, quitjob_eng_in_aft))
        self.playw(FadeOut(quitjob_eng_in_aft, scale=0.5, target_position=dec.get_corner(DOWN)))

        self.playw(FadeIn(dec_out, scale=0.5, target_position=dec.get_corner(UP)))
        self.playw(FadeIn(quitjob_eng_out_bef))
        self.playw(TransformMatchingTex(quitjob_eng_out_bef, quitjob_eng_out_aft))

        self.playw(LaggedStart(*[FadeOut(quitjob_eng_out_aft[i], scale=0.8, target_position=dec_out[i]) for i in range(len(dec_out))], lag_ratio=0.2))

        quitjob_eng_out_aft[0].save_state()
        self.playw(FadeIn(quitjob_eng_out_aft[0]))
        self.play(quitjob_eng_out_aft[0].animate.scale(1.4))
        self.playw(Restore(quitjob_eng_out_aft[0]))
        
        selfattn_color = interpolate_color(ORANGE, WHITE, 0.2)
        selfattn = dec.copy().set_color(selfattn_color).set_stroke_color(WHITE).stretch_to_fit_height(dec.get_height()*0.5).align_to(dec, DOWN)
        self.playw(Transform(dec, selfattn),
                   enc_out.animate.set_opacity(0.2),
                   enc.animate.set_opacity(0.2),
                   dec_out[1:].animate.set_opacity(0.2),
                   self.camera.frame.animate.scale(0.5).move_to(selfattn))
        quitjob_eng_in_aft_selfattn = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                          arg_separator=" ").scale(0.25).next_to(dec, DOWN, buff=_dist_buf)
        small_rect_height = quitjob_eng_in_aft_selfattn[0].height
        ds = []
        for i in range(8):
            d = rect(height=small_rect_height, width=small_rect_height, stroke_width=DEFAULT_STROKE_WIDTH/8, color=random_color())
            d.move_to(quitjob_eng_in_aft_selfattn[i])
            if i:
                d.align_to(ds[0], DOWN)
            ds.append(d)
        ds_v = VGroup(*ds)
        self.playw(Write(quitjob_eng_in_aft_selfattn))
        self.playw(Transform(quitjob_eng_in_aft_selfattn, ds_v, replace_mobject_with_target_in_scene=True))

        selfattn_out = ds[0].copy().next_to(selfattn, UP).align_to(ds_v[0], LEFT).set_color(random_color()).set_stroke_color(WHITE)
        futures = surround_rect(Rectangle(PURE_GREEN, stroke_width=DEFAULT_STROKE_WIDTH/7), ds_v[1:], 0.05)
        ds_v_in = ds_v.copy()
        self.add(ds_v_in)
        self.playw(Transform(ds_v, selfattn_out, replace_mobject_with_target_in_scene=True))
        self.playw(Write(futures))
        self.playw(ds_v_in[1:].animate.set_opacity(0.4))
        
        return encdec

    def sceneE2(self, encdec):
        enc, dec = encdec
        quitjob_kor = Tex(r'아', r'퇴사', r'하고', r'싶다', color=GOLD,
                          arg_separator=" ").scale(0.7).next_to(enc, DOWN, buff=_dist_buf*1.5)
        self.playw(Write(quitjob_kor))
        self.playw(FadeOut(quitjob_kor, target_position=enc.get_corner(DOWN), scale=0.3))

        enc_colors = [TEAL_E, RED_D, YELLOW_C, BLUE_D]
        quitjob_kor_enc = Tex(r'아', r'퇴사', r'하고', r'싶다',
                          arg_separator=" ").scale(0.5).next_to(enc, UP, buff=_dist_buf*1.5).set_color_by_gradient(*enc_colors)
        self.playw(FadeIn(quitjob_kor_enc, target_position=enc.get_corner(UP), scale=0.3))
        enc_out = VGroup(*[rect() for i in range(4)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*enc_colors).next_to(enc, UP, buff=_dist_buf*1.5)
        self.playw(LaggedStart(*[FadeTransform(quitjob_kor_enc[i], enc_out[i]) for i in range(len(enc_out))], lag_ratio=0.1))

        quitjob_eng_in_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        quitjob_eng_in_aft = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        dec_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, DARK_BLUE, PURPLE]
        dec_out = VGroup(*[rect() for i in range(8)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        quitjob_eng_out_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        quitjob_eng_out_aft = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', r'[EOS]', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        
        self.playw(FadeIn(quitjob_eng_in_bef))
        self.playw(TransformMatchingTex(quitjob_eng_in_bef, quitjob_eng_in_aft))
        self.playw(FadeOut(quitjob_eng_in_aft, scale=0.5, target_position=dec.get_corner(DOWN)))

        self.playw(FadeIn(dec_out, scale=0.5, target_position=dec.get_corner(UP)))
        self.playw(FadeIn(quitjob_eng_out_bef))
        self.playw(TransformMatchingTex(quitjob_eng_out_bef, quitjob_eng_out_aft))

        self.playw(LaggedStart(*[FadeOut(quitjob_eng_out_aft[i], scale=0.8, target_position=dec_out[i]) for i in range(len(dec_out))], lag_ratio=0.2))

        quitjob_eng_out_aft[0].save_state()
        self.playw(FadeIn(quitjob_eng_out_aft[0]))
        self.play(quitjob_eng_out_aft[0].animate.scale(1.4))
        self.playw(Restore(quitjob_eng_out_aft[0]))
        
        selfattn_color = interpolate_color(ORANGE, WHITE, 0.2)
        selfattn = dec.copy().set_color(selfattn_color).set_stroke_color(WHITE).stretch_to_fit_height(dec.get_height()*0.5).align_to(dec, DOWN)
        self.playw(Transform(dec, selfattn),
                   enc_out.animate.set_opacity(0.2),
                   enc.animate.set_opacity(0.2),
                   dec_out[1:].animate.set_opacity(0.2),
                   self.camera.frame.animate.scale(0.5).move_to(selfattn))
        quitjob_eng_in_aft_selfattn = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                          arg_separator=" ").scale(0.25).next_to(dec, DOWN, buff=_dist_buf)
        small_rect_height = quitjob_eng_in_aft_selfattn[0].height
        ds = []
        for i in range(8):
            d = rect(height=small_rect_height, width=small_rect_height, stroke_width=DEFAULT_STROKE_WIDTH/8, color=random_color())
            d.move_to(quitjob_eng_in_aft_selfattn[i])
            if i:
                d.align_to(ds[0], DOWN)
            ds.append(d)
        ds_v = VGroup(*ds).arrange(RIGHT, buff=_dist_buf*0.3).move_to(quitjob_eng_in_aft_selfattn)
        self.playw(Write(quitjob_eng_in_aft_selfattn))
        self.playw(Transform(quitjob_eng_in_aft_selfattn, ds_v, replace_mobject_with_target_in_scene=True))

        for i in range(3):
            selfattn_out = ds[i].copy().next_to(selfattn, UP).align_to(ds_v[i], LEFT).set_color(random_color()).set_stroke_color(WHITE)
            futures = surround_rect(Rectangle(PURE_GREEN, stroke_width=DEFAULT_STROKE_WIDTH/7), ds_v[i+1:], 0.05)
            ds_v_in = ds_v.copy()
            self.playw(FadeIn(ds_v_in))
            self.remove(ds_v)
            self.playw(ds_v_in[i+1:].animate.set_opacity(0.4))
            self.playw(Transform(ds_v_in[:i+1], selfattn_out, replace_mobject_with_target_in_scene=True))
            self.playw(Write(futures))
            self.playw(FadeOut(futures, ds_v_in[i+1:]))

        return encdec
    
    def sceneE3(self, encdec):
        enc, dec = encdec
        quitjob_kor = Tex(r'아', r'퇴사', r'하고', r'싶다', color=GOLD,
                          arg_separator=" ").scale(0.7).next_to(enc, DOWN, buff=_dist_buf*1.5)
        self.playw(Write(quitjob_kor))
        self.playw(FadeOut(quitjob_kor, target_position=enc.get_corner(DOWN), scale=0.3))

        enc_colors = [TEAL_E, RED_D, YELLOW_C, BLUE_D]
        quitjob_kor_enc = Tex(r'아', r'퇴사', r'하고', r'싶다',
                          arg_separator=" ").scale(0.5).next_to(enc, UP, buff=_dist_buf*1.5).set_color_by_gradient(*enc_colors)
        self.playw(FadeIn(quitjob_kor_enc, target_position=enc.get_corner(UP), scale=0.3))
        enc_out = VGroup(*[rect() for i in range(4)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*enc_colors).next_to(enc, UP, buff=_dist_buf*1.5)
        self.playw(LaggedStart(*[FadeTransform(quitjob_kor_enc[i], enc_out[i]) for i in range(len(enc_out))], lag_ratio=0.1))

        quitjob_eng_in_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        quitjob_eng_in_aft = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                 arg_separator=" ").scale(0.5).next_to(dec, DOWN, buff=_dist_buf*1.5)
        dec_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, DARK_BLUE, PURPLE]
        dec_out = VGroup(*[rect() for i in range(8)]).arrange(RIGHT, buff=_dist_buf*0.4).set_color_by_gradient(*dec_colors).next_to(dec, UP, buff=_dist_buf*1.5)
        quitjob_eng_out_bef = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        quitjob_eng_out_aft = Tex(r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', r'[EOS]', color=PURE_GREEN,
                                  arg_separator=" ").scale(0.45).next_to(dec_out, UP, buff=_dist_buf)
        
        self.playw(FadeIn(quitjob_eng_in_bef))
        self.playw(TransformMatchingTex(quitjob_eng_in_bef, quitjob_eng_in_aft))
        self.playw(FadeOut(quitjob_eng_in_aft, scale=0.5, target_position=dec.get_corner(DOWN)))

        self.playw(FadeIn(dec_out, scale=0.5, target_position=dec.get_corner(UP)))
        self.playw(FadeIn(quitjob_eng_out_bef))
        self.playw(TransformMatchingTex(quitjob_eng_out_bef, quitjob_eng_out_aft))

        self.playw(LaggedStart(*[FadeOut(quitjob_eng_out_aft[i], scale=0.8, target_position=dec_out[i]) for i in range(len(dec_out))], lag_ratio=0.2))

        quitjob_eng_out_aft[0].save_state()
        self.playw(FadeIn(quitjob_eng_out_aft[0]))
        self.play(quitjob_eng_out_aft[0].animate.scale(1.4))
        self.playw(Restore(quitjob_eng_out_aft[0]))
        
        selfattn_color = interpolate_color(ORANGE, WHITE, 0.2)
        selfattn = dec.copy().set_color(selfattn_color).set_stroke_color(WHITE).stretch_to_fit_height(dec.get_height()*0.5).align_to(dec, DOWN)
        self.playw(Transform(dec, selfattn),
                   enc_out.animate.set_opacity(0.2),
                   enc.animate.set_opacity(0.2),
                   dec_out[1:].animate.set_opacity(0.2),
                   self.camera.frame.animate.scale(0.5).move_to(selfattn))
        quitjob_eng_in_aft_selfattn = Tex(r'[SOS]', r'Oh',  r'I', r'want', r'to', r'quit', r'my', r'job', color=WHITE,
                                          arg_separator=" ").scale(0.25).next_to(dec, DOWN, buff=_dist_buf)
        small_rect_height = quitjob_eng_in_aft_selfattn[0].height
        ds = []
        for i in range(8):
            d = rect(height=small_rect_height, width=small_rect_height, stroke_width=DEFAULT_STROKE_WIDTH/8, color=random_color())
            d.move_to(quitjob_eng_in_aft_selfattn[i])
            if i:
                d.align_to(ds[0], DOWN)
            ds.append(d)
        ds_v = VGroup(*ds).arrange(RIGHT, buff=_dist_buf*0.3).move_to(quitjob_eng_in_aft_selfattn)
        self.playw(Write(quitjob_eng_in_aft_selfattn))
        self.playw(Transform(quitjob_eng_in_aft_selfattn, ds_v, replace_mobject_with_target_in_scene=True))

        for i in range(3):
            selfattn_out = ds[i].copy().next_to(selfattn, UP).align_to(ds_v[i], LEFT).set_color(random_color()).set_stroke_color(WHITE)
            ds_v_in = ds_v.copy()
            self.playw(FadeIn(ds_v_in))
            self.remove(ds_v)
            #self.playw(ds_v_in[i+1:].animate.set_opacity(1.0))
            self.playw(Transform(ds_v_in, selfattn_out, replace_mobject_with_target_in_scene=True))
        
        return encdec

    def sceneF(self):
        self.playw(self.camera.frame.animate.scale(1.7))
        query = rect(0.5, 0.5)
        keys = VGroup(
            rect(0.5, 0.5, color=random_color()), 
            rect(0.5, 0.5, color=random_color()),
            rect(0.5, 0.5, color=random_color()),
            rect(0.5, 0.5, color=random_color()), 
            rect(0.5, 0.5, color=random_color()), 
            rect(0.5, 0.5, color=random_color()),
            rect(0.5, 0.5, color=random_color()),
            rect(0.5, 0.5, color=random_color())
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
        
        tbq = texbox("$W_q$", box_config={"color": BLACK, "opacity":1.0}).next_to(query, UP).shift(UP).shift(UP).shift(UP).shift(UP)
        tbk = texbox("$W_k$", box_config={"color": BLACK, "opacity":1.0}).move_to((keys.get_x(), tbq.get_y(), 0))
        self.playw(Write(tbq), Write(tbk))

        query.generate_target()
        keys.generate_target()
        query.target.next_to(tbq, UP).shift(UP).shift(UP).shift(UP)
        keys.target.next_to(tbk, UP).shift(UP)
        self.playw(MoveToTarget(query), MoveToTarget(keys), self.camera.frame.animate.shift(UP*3)\
                   .set(width=self.camera.frame_width*1.5))
        
        self.playw(VGroup(tbq, tbk, query, keys).animate.shift(LEFT).shift(LEFT))

        tbv = texbox("$W_v$", box_config={"color": BLACK, "opacity":1.0}).move_to((values.get_x(), tbq.get_y(), 0))
        self.playw(Write(tbv))

        values.generate_target()
        values.target.next_to(tbv, UP).shift(UP)
        for i in range(len(values)):
            values.target[i].set_color(interpolate_color(values.target[i].get_color(), BLACK, 0.6)).set_stroke_color(WHITE)
        
        self.playw(MoveToTarget(values))

        qt.next_to(query, UP)
        kt.next_to(keys, UP)
        vt = Text("Values", font_size=DEFAULT_FONT_SIZE*0.7).next_to(values, UP)
        self.playw(self.camera.frame.animate.move_to(VGroup(tbq, tbk, tbv, query, keys, values).get_center()).scale(0.7))
        self.playw(Write(qt))
        self.playw(Write(kt))
        self.playw(Write(vt))
        self.playw(FadeOut(qt, kt, vt))

        ls = [1.7, -1.3, 3.9, 4.1, -1.5, 3.0, -3.7, 2.3]
        logits = []
        for i, logit in enumerate(ls):
            logit = Text(f"{logit:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[i])
            query.save_state()
            self.play(query.animate.move_to(keys[i]))
            self.playw(query.animate.restore(), FadeTransform(keys[i], logit))
            logits.append(logit)
        
        # Masking: logit to -inf
        masked = [3, 4, 5, 6, 7]
        for i in masked:
            ls[i] = -999_999_999
            logit_m = Text(f"{ls[i]:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[i])
            self.playw(FadeTransform(logits[i], logit_m))
            logits[i] = logit_m
        # l3, l4 = -999_999_999, -999_999_999
        # logit3_m = Text(f"{l3:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[2])
        # logit4_m = Text(f"{l4:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[3])
        # self.playw(FadeTransform(logit3, logit3_m))
        # self.playw(FadeTransform(logit4, logit4_m))

        els = [e**l for l in ls]
        weights = []
        for i, el in enumerate(els):
            w = Text(f"{el:.1f}", font="Consolas",
                     color=WHITE if i not in masked else RED,
                     font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[i])
            self.play(FadeTransform(logits[i], w))
            weights.append(w)
        self.wait()
        # w1 = Text(f"{el1:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[0])
        # w2 = Text(f"{el2:.1f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[1])
        # w3 = Text(f"{el3:.1f}", font="Consolas", color=RED, font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[2])
        # w4 = Text(f"{el4:.1f}", font="Consolas", color=RED, font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[3])
        # self.play(FadeTransform(logit1, w1))
        # self.play(FadeTransform(logit2, w2))
        # self.play(FadeTransform(logit3_m, w3))
        # self.playw(FadeTransform(logit4_m, w4))

        sum_el = sum(els)
        probs = []
        for i, el in enumerate(els):
            p = Text(f"{el/sum_el:.2f}", font="Consolas",
                     color=WHITE if i not in masked else RED,
                     font_size=DEFAULT_FONT_SIZE*0.7).move_to(keys[i])
            self.play(FadeTransform(weights[i], p))
            probs.append(p)
        self.wait()

        # sum_el = el1 + el2 + el3 + el4
        # p1 = Text(f"{el1/sum_el:.3f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[0])
        # p2 = Text(f"{el2/sum_el:.3f}", font="Consolas", font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[1])
        # p3 = Text(f"{el3/sum_el:.3f}", font="Consolas", color=RED, font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[2])
        # p4 = Text(f"{el4/sum_el:.3f}", font="Consolas", color=RED, font_size=DEFAULT_FONT_SIZE*0.6).move_to(keys[3])
        # self.play(FadeTransform(w1, p1))
        # self.play(FadeTransform(w2, p2))
        # self.play(FadeTransform(w3, p3))
        # self.playw(FadeTransform(w4, p4))

        times = [Tex("$\\times$").move_to(VGroup(probs[i], values[i]).get_center()) for i in range(len(probs))]
        # time1 = Tex("$\\times$").move_to(VGroup(p1, values[0]).get_center())
        # time2 = Tex("$\\times$").move_to(VGroup(p2, values[1]).get_center())
        # time3 = Tex("$\\times$").move_to(VGroup(p3, values[2]).get_center())
        # time4 = Tex("$\\times$").move_to(VGroup(p4, values[3]).get_center())
        self.playw(LaggedStart(*[Write(t) for t in times], lag_ratio=0.3))
        
        qt.next_to(query, UP)
        sm_qkt = Tex("softmax($QK^T$)", font_size=DEFAULT_FONT_SIZE*0.7).next_to(probs[0], UP)
        vt.next_to(values, UP)
        self.playw(Write(qt))
        self.playw(Write(sm_qkt))
        self.playw(Write(vt))
        self.playw(FadeOut(qt, sm_qkt, vt))

        qkvs = [VGroup(probs[i], times[i], values[i]) for i in range(len(probs))]
        # qkv1 = VGroup(p1, time1, values[0])
        # qkv2 = VGroup(p2, time2, values[1])
        # qkv3 = VGroup(p3, time3, values[2])
        # qkv4 = VGroup(p4, time4, values[3])
        all_qkv = VGroup(*qkvs)
        center_point = all_qkv.get_center()
        for i, qkv in enumerate(qkvs):
            qkv.generate_target()
            qkv.target.move_to(center_point)
        # qkv1.generate_target()
        # qkv2.generate_target()
        # qkv3.generate_target()
        # qkv4.generate_target()
        # qkv1.target.move_to(center_point)
        # qkv2.target.move_to(center_point)
        # qkv3.target.move_to(center_point)
        # qkv4.target.move_to(center_point)
        final_qkv = rect(0.5, 0.5, color=[GRAY, GOLD]).move_to(center_point)
        final_qkv.move_to([final_qkv.get_x(), query.get_y(), 0])
        wst = Text("Weighted sum", font_size=DEFAULT_FONT_SIZE*0.7, color=YELLOW).move_to(center_point)
        self.playw(
            *[MoveToTarget(qkv) for qkv in qkvs],
            # MoveToTarget(qkv1), 
            # MoveToTarget(qkv2), 
            # MoveToTarget(qkv3), 
            # MoveToTarget(qkv4), 
            FadeTransform(all_qkv, final_qkv),
            FadeOut(wst, scale=1.5)
        )

        arrow_qqkv = Arrow(query.get_right(), final_qkv.get_left(), buff=0.3, color=GOLD)
        self.playw(
            Write(arrow_qqkv)
        )


def surround_rect(rect, mob, buf=0.4):
    return rect.stretch_to_fit_height(mob.height + buf*2).stretch_to_fit_width(mob.width + buf*2).move_to(mob)