from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        broadcasting = Text("Broadcasting", font_size=60).set_color_by_gradient(
            RED_B, RED_E
        )

        self.playw(
            LaggedStart(*[FadeIn(c) for c in broadcasting], lag_ratio=0.1), wait=3
        )

        mat32 = Matrix([[1, 2], [3, 4], [5, 6]], h_buff=0.5)
        mat32t = CodeText("x.shape = (3, 2)", font_size=18, color=YELLOW_B).next_to(
            mat32, UP, buff=0.5
        )
        self.play(
            LaggedStart(
                broadcasting.animate.next_to(self.cf, UP), FadeIn(mat32), lag_ratio=0.5
            )
        )
        self.playw(FadeIn(mat32t))

        vec3 = Matrix([[1, 2, 3]], h_buff=0.5).set_color(GREEN)
        vec2 = Matrix([[1, 2]], h_buff=0.5).set_color(GREEN)
        vecs = VGroup(vec3, vec2).arrange(DOWN, buff=1.5).shift(RIGHT * 3)
        vec3t = CodeText("y.shape = (3, )", font_size=18, color=YELLOW_B).next_to(
            vec3, UP
        )
        vec2t = CodeText("y.shape = (2, )", font_size=18, color=YELLOW_B).next_to(
            vec2, UP
        )
        p3 = CodeText("+", font_size=36).next_to(vec3, LEFT, buff=0.3)
        p2 = CodeText("+", font_size=36).next_to(vec2, LEFT, buff=0.3)

        mat32 = VGroup(mat32, mat32t)
        self.playw(mat32.animate.shift(LEFT * 3), FadeIn(vec3, p3, vec3t))
        self.playw(FadeIn(vec2, p2, vec2t))

        self.cf.save_state()
        self.playw(self.cf.animate.shift(RIGHT * 3), mat32.animate.set_opacity(0.2))

        self.playw(vec3.animate.set_color(PURE_RED), vec2.animate.set_color(PURE_GREEN))

        self.playw(
            Restore(self.cf),
            mat32.animate.set_opacity(0.1),
            vecs.animate.set_opacity(0.1),
            VGroup(p3, p2, vec3t, vec2t).animate.set_opacity(0.1),
        )

        formula1 = Text("Matching Dimensions", font_size=48).set_color_by_gradient(
            BLUE_B, BLUE_E
        )
        formula2 = Text("Number of elements", font_size=48).set_color_by_gradient(
            BLUE_B, BLUE_E
        )
        formulas = VGroup(formula1, formula2).arrange(DOWN, buff=1)
        self.play(FadeIn(formula1))
        self.playw(FadeIn(formula2))

        circus1 = CodeText("shape (7, 1, 4, 1)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        circus2 = CodeText("shape (8, 4, 6)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        circuses = VGroup(circus1, circus2).arrange(DOWN, buff=1, aligned_edge=LEFT)
        pc = Text("+", font_size=36, color=RED).next_to(circus2, LEFT, buff=0.3)
        self.play(FadeOut(formulas))
        self.playw(LaggedStart(FadeIn(circus1), FadeIn(circus2, pc), lag_ratio=0.5))


class matchingDim(Scene3D):
    def construct(self):
        # intro
        shape1 = CodeText("shape (2, 3, 4)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shape2 = CodeText("shape (3, 4)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shapes = VGroup(shape1, shape2).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        shapes.save_state()
        shape2_ = (
            CodeText("shape (1, 3, 4)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape2)
            .align_to(shape2, LEFT)
        )

        self.playw(FadeIn(shape1, shape2))
        self.playw(
            shape2[:5].animate.become(shape2_[:5]),
            shape2[5].animate.become(shape2_[5:8]),
            shape2[6:].animate.become(shape2_[8:]),
        )

        self.playw(shape2.animate.set_opacity(0))

        mat0 = MobjectMatrix(
            [
                [Matrix([[0, 1, 2, 3]])],
                [Matrix([[4, 5, 6, 7]])],
                [Matrix([[8, 9, 10, 11]])],
            ],
            v_buff=1.3,
        )
        mat1 = MobjectMatrix(
            [
                [Matrix([[12, 13, 14, 15]])],
                [Matrix([[16, 17, 18, 19]])],
                [Matrix([[20, 21, 22, 23]])],
            ],
            v_buff=1.3,
        )
        mats = VGroup(mat0, mat1).arrange(OUT, buff=6)
        self.play(shape1.animate.shift(UP * 2.5))
        shape1.set_z_index(1)
        self.move_camera_horizontally(
            45,
            added_anims=[
                shape1.animate.rotate(-45 * DEGREES, UP).shift(UP),
                FadeIn(mats),
            ],
            zoom=0.7,
        )

        for i in [-2, -4, -6]:
            shape1[i].save_state()
        mats.save_state()
        vec = mats[0][0][0].copy()
        mat = mats[0].copy()
        self.playw(
            VGroup(shape1[-2], shape1[-4], shape1[-6])
            .animate.set_color(YELLOW)
            .scale(1.1),
            mats.animate.set_opacity(0.3),
        )

        self.play(shape1[6:-2].animate.set_opacity(0), Restore(shape1[-2]))
        self.playw(
            mats.animate.set_opacity(0),
            vec.animate.move_to(ORIGIN).rotate(-45 * DEGREES, UP),
        )
        self.play(mats.animate.set_opacity(1), FadeOut(vec), run_time=0.3)
        self.play(
            Restore(shape1[-4]),
            shape1[-3].animate.set_opacity(1),
        )
        self.playw(
            mats.animate.set_opacity(0),
            mat.animate.move_to(ORIGIN).rotate(-45 * DEGREES, UP),
        )
        self.play(mats.animate.set_opacity(1), FadeOut(mat), run_time=0.3)
        self.play(
            Restore(shape1[-6]),
            shape1[-5].animate.set_opacity(1),
        )
        self.playw_return(mats.animate.set_color(GREEN).scale(1.1))

        self.play(FadeOut(mats))
        self.move_camera_horizontally(0, zoom=1, added_anims=[Restore(shapes)])

        self.playw(
            LaggedStart(Indicate(shape1[5:]), Indicate(shape2[5:]), lag_ratio=0.5)
        )
        shape2_ = (
            CodeText("shape (1, 3, 4)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape2)
            .align_to(shape2, LEFT)
        )
        self.playw(
            shape2[:5].animate.become(shape2_[:5]),
            shape2[5].animate.become(shape2_[5:8]),
            shape2[6:].animate.become(shape2_[8:]),
        )
        self.play(FadeOut(shapes))

        shape1 = CodeText("shape (2, 3, 4, 5)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shape2 = CodeText("shape (4, 5)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shapes = VGroup(shape1, shape2).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        self.playw(FadeIn(shapes))
        shape2_ = (
            CodeText("shape (1, 1, 4, 5)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape2)
            .align_to(shape2, LEFT)
        )
        self.playw(
            shape2[:5].animate.become(shape2_[:5]),
            shape2[5].animate.become(shape2_[5:10]),
            shape2[6:].animate.become(shape2_[10:]),
        )


class numElements(Scene3D):
    def construct(self):
        shape1 = CodeText("shape (3, 2)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shape2 = CodeText("shape (3, 1)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shapes = VGroup(shape1, shape2).arrange(DOWN, buff=1.5)
        vec1 = Matrix([[1, 2], [3, 4], [5, 6]], h_buff=0.5).set_color(GREEN).scale(0.8)
        vec2 = Matrix([[7], [8], [9]], h_buff=0.5).set_color(GREEN).scale(0.8)

        self.playw(FadeIn(shapes))
        first = VGroup(shape1[6], shape2[6])
        first.save_state()
        second = VGroup(shape1[8], shape2[8])
        second.save_state()
        self.play(
            Circumscribe(first),
            first.animate.set_color(YELLOW),
        )
        self.playw(Restore(first))
        self.play(
            Circumscribe(second),
            second.animate.set_color(YELLOW),
        )
        self.playw(Restore(second))

        self.play(shapes.animate.shift(LEFT * 2))
        vecs = (
            VGroup(vec1, vec2).arrange(DOWN, buff=1, aligned_edge=LEFT).shift(RIGHT * 2)
        )
        self.playw(FadeIn(vecs))

        first0, first1 = shape1[6], shape1[8]
        second0, second1 = shape2[6], shape2[8]
        first0.save_state()
        first1.save_state()
        second0.save_state()
        second1.save_state()

        eq = CodeText("==", font_size=36).set_opacity(0).move_to(shapes)
        first0.generate_target()
        second0.generate_target()
        eq.generate_target()
        VGroup(first0.target, eq.target, second0.target).arrange(
            RIGHT, buff=0.5
        ).move_to(shapes.get_center()).set_opacity(1)
        self.playw(
            LaggedStart(
                *[MoveToTarget(c) for c in [first0, second0, eq]], lag_ratio=0.2
            )
        )
        self.playw(Restore(first0), Restore(second0), FadeOut(eq))

        eq10 = CodeText("== 1", font_size=36).set_opacity(0).move_to(shapes)
        eq11 = CodeText("== 1", font_size=36).set_opacity(0).move_to(shapes)
        ortext = (
            CodeText("or", font_size=28, color=PURPLE).set_opacity(0).move_to(shapes)
        )
        first1.generate_target()
        second1.generate_target()
        eq10.generate_target()
        eq11.generate_target()
        ortext.generate_target()
        VGroup(
            first1.target, eq10.target, ortext.target, second1.target, eq11.target
        ).arrange(RIGHT, buff=0.5).move_to(shapes.get_center()).set_opacity(1)

        self.playw(
            LaggedStart(
                *[MoveToTarget(c) for c in [first1, second1, eq10, ortext, eq11]],
                lag_ratio=0.2,
            )
        )

        self.playw(
            *[Restore(c) for c in [first1, second1]],
            FadeOut(eq10),
            FadeOut(eq11),
            FadeOut(ortext),
        )
        vec2_ = (
            Matrix([[7, 7], [8, 8], [9, 9]], h_buff=0.5)
            .set_color(GREEN)
            .scale(0.8)
            .move_to(vec2)
            .align_to(vec2, LEFT)
        )
        vec2.save_state()
        self.playw(vec2.animate.become(vec2_))
        pluss = CodeText("+", font_size=36).move_to(shapes)
        plusv = CodeText("+", font_size=36).move_to(vecs)
        self.playw(Restore(vec2), FadeIn(pluss, plusv))
        self.playw_return(
            vec1[0][0:2].animate.set_color(YELLOW).scale(1.2),
            vec2[0][0].animate.set_color(YELLOW).scale(1.2),
            run_time=1,
            wait=0.1,
        )
        self.playw_return(
            vec1[0][2:4].animate.set_color(PURPLE).scale(1.2),
            vec2[0][2].animate.set_color(PURPLE).scale(1.2),
            run_time=1,
            wait=0.1,
        )
        self.playw_return(
            vec1[0][4:6].animate.set_color(PURE_RED).scale(1.2),
            vec2[0][4].animate.set_color(PURE_RED).scale(1.2),
            run_time=1,
            wait=0.1,
        )

        self.play(Circumscribe(shape2[-2]))
        vec2_ = (
            Matrix([[7, 7], [8, 8], [9, 9]], h_buff=0.5)
            .set_color(GREEN)
            .scale(0.8)
            .move_to(vec2)
            .align_to(vec2, LEFT)
        )
        self.playw(vec2.animate.become(vec2_))
        self.play(
            FadeOut(plusv), vec1.animate.move_to(vecs), vec2.animate.move_to(vecs)
        )
        vec_result = (
            Matrix([[8, 9], [11, 12], [14, 15]], h_buff=0.8)
            .set_color(GREEN)
            .move_to(vecs)
        )
        self.playw(
            vec1.animate.become(vec_result),
            FadeOut(vec2),
            # Transform(VGroup(vec1[0], vec2[0]), vec_result[0], replace_mobject_with_target_in_scene=True),
            # Transform(VGroup(vec1[1], vec2[1]), vec_result[1], replace_mobject_with_target_in_scene=True),
            # Transform(VGroup(vec1[2], vec2[2]), vec_result[2], replace_mobject_with_target_in_scene=True),
        )


class whatisBroadcasting(Scene2D):
    def construct(self):
        shape1 = CodeText("shape (2, 4)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shape2 = CodeText("shape (1, 4)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        vec1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8]]).set_color(GREEN)
        vec2 = Matrix([[9, 10, 11, 12]]).set_color(GREEN)

        arr1 = VGroup(shape1, vec1).arrange(DOWN, buff=0.5)
        arr2 = VGroup(shape2, vec2).arrange(DOWN, buff=0.5)
        arrs = VGroup(arr1, arr2).arrange(RIGHT, aligned_edge=UP, buff=1.5)
        plus = CodeText("+", font_size=36).move_to(arrs)
        self.play(FadeIn(arr1))
        self.playw(FadeIn(arr2, plus))
        self.play(Circumscribe(shape1[6]))
        self.mouse.next_to(shape2[6], DR, buff=0)
        self.play(Circumscribe(shape2[6]))
        self.playw(FadeIn(self.mouse, shift=DOWN * 2))
        vec2_ = (
            Matrix([[9, 10, 11, 12], [9, 10, 11, 12]])
            .set_color(GREEN)
            .move_to(vec2)
            .align_to(vec2, UP)
        )
        shape2_ = (
            CodeText("shape (2, 4)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape2)
            .align_to(shape2, LEFT)
        )
        self.playw(
            vec2[1].animate.become(vec2_[1]),
            vec2[2].animate.become(vec2_[2]),
            vec2[0][0].animate.become(VGroup(vec2_[0][0], vec2_[0][4])),
            vec2[0][1].animate.become(VGroup(vec2_[0][1], vec2_[0][5])),
            vec2[0][2].animate.become(VGroup(vec2_[0][2], vec2_[0][6])),
            vec2[0][3].animate.become(VGroup(vec2_[0][3], vec2_[0][7])),
            shape2.animate.become(shape2_),
        )
        self.playw(Group(arrs, plus, self.mouse).animate.next_to(self.cf, LEFT))

        shape3 = CodeText("shape (3, 1, 4)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shape4 = CodeText("shape (4, )", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shapes = VGroup(shape3, shape4).arrange(RIGHT, buff=1.5)
        plus = CodeText("+", font_size=36).move_to(
            shape3.get_right() * 0.5 + shape4.get_left() * 0.5
        )
        self.playw(LaggedStart(*[FadeIn(item) for item in [shape3, plus, shape4]]))


class recap1(Scene2D):
    def construct(self):
        leftshape = (
            CodeText("shape (3, 2)", font_size=36)
            .set_color_by_gradient(ORANGE, YELLOW_C)
            .shift(LEFT * 2.5)
        )
        shape1 = CodeText("shape (3, )", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shape2 = CodeText("shape (2, )", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        )
        shapes = (
            VGroup(shape1, shape2)
            .arrange(DOWN, buff=0.75, aligned_edge=LEFT)
            .shift(RIGHT * 2.5)
        )
        self.playw(FadeIn(leftshape))
        self.playw(FadeIn(shape1))
        self.playw(FadeIn(shape2))

        formula1 = (
            Text("Matching Dimensions", font_size=48)
            .set_color_by_gradient(BLUE_B, BLUE_E)
            .shift(UP * 2)
        )
        self.playw(LaggedStart(*[FadeIn(c) for c in formula1], lag_ratio=0.1))
        shape1_ = (
            CodeText("shape (1, 3)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape1)
            .align_to(shape1, LEFT)
        )
        shape2_ = (
            CodeText("shape (1, 2)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape2)
            .align_to(shape2, LEFT)
        )
        self.playw(
            LaggedStart(
                AnimationGroup(
                    Transform(
                        shape1[:5],
                        shape1_[:5],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        shape1[5],
                        shape1_[5:8],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        shape1[6:],
                        shape1_[8:],
                        replace_mobject_with_target_in_scene=True,
                    ),
                ),
                AnimationGroup(
                    Transform(
                        shape2[:5],
                        shape2_[:5],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        shape2[5],
                        shape2_[5:8],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    Transform(
                        shape2[6:],
                        shape2_[8:],
                        replace_mobject_with_target_in_scene=True,
                    ),
                ),
                lag_ratio=0.5,
            )
        )
        self.playw(FadeOut(formula1))
        formula2 = (
            Text("Number of elements", font_size=48)
            .set_color_by_gradient(BLUE_B, BLUE_E)
            .shift(UP * 2)
        )
        self.playw(LaggedStart(*[FadeIn(c) for c in formula2], lag_ratio=0.1))

        first = VGroup(shape1_[6], shape2_[6], leftshape[6]).copy()
        self.add(first)
        self.playw(VGroup(shape1_, shape2_, leftshape).animate.set_opacity(0.2))
        self.playw(
            LaggedStart(
                *[Indicate(c, color=PURE_RED) for c in first[:2]], lag_ratio=0.5
            )
        )
        three = lambda: CodeText("3", font_size=36).set_color_by_gradient(RED_C)
        self.playw(
            LaggedStart(
                *[Transform(c, three().move_to(c)) for c in first[:2]], lag_ratio=0.5
            )
        )
        self.playw(first.animate.set_opacity(0.0))
        second = VGroup(shape1_[8], shape2_[8], leftshape[8]).copy()
        self.playw(second.animate.set_opacity(1))
        self.mouse.next_to(leftshape[8], DR, buff=0)
        self.playw(FadeIn(self.mouse, shift=LEFT * 2))
        self.playw(self.mouse.animate.next_to(shape1_[8], DR, buff=0))
        self.playw(self.mouse.animate.next_to(shape2_[8], DR, buff=0))
        second[0].save_state()
        self.playw(
            LaggedStart(
                self.mouse.animate.next_to(shape1_[8], DR, buff=0),
                second[0].animate.set_color(PURE_RED).scale(1.3),
                lag_ratio=0.5,
            )
        )
        self.playw(
            Restore(second[0]), self.mouse.animate.next_to(shape2_[8], DR, buff=0)
        )

        self.playw(
            FadeOut(second, self.mouse),
            VGroup(shape1_, shape2_, leftshape).animate.set_opacity(1),
        )
        self.playw(shape1_.animate.set_color(PURE_RED))
        self.playw(shape2_.animate.set_color(PURE_GREEN))


class recap2(Scene2D):
    def construct(self):
        leftshape = (
            CodeText("shape (7, 1, 4, 1)", font_size=36)
            .set_color_by_gradient(ORANGE, YELLOW_C)
            .shift(LEFT * 3)
        )
        shape1 = CodeText("shape (8, 4, 6)", font_size=36).set_color_by_gradient(
            RED_B, RED_D
        ).shift(RIGHT * 3)
        plus = CodeText("+", font_size=36).next_to(shape1, LEFT, buff=0.5)
        self.playw(FadeIn(leftshape))
        self.playw(FadeIn(shape1, plus))
        self.wait(3)
        

        shape1_ = (
            CodeText("shape (1, 8, 4, 6)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape1)
            .align_to(shape1, LEFT)
        )
        self.playw(
            LaggedStart(
                AnimationGroup(
                    Transform(
                        shape1[:5],
                        shape1_[:5],
                        replace_mobject_with_target_in_scene=True,
                    ),
                    AnimationGroup(
                        Transform(
                            shape1[5],
                            shape1_[5:8],
                            replace_mobject_with_target_in_scene=True,
                        ),
                        Transform(
                            shape1[6:],
                            shape1_[8:],
                            replace_mobject_with_target_in_scene=True,
                        ),
                    ),
                    lag_ratio=0.5,
                )
            )
        )
        pshape1 = VGroup(shape1_, plus)
        self.playw(VGroup(leftshape, pshape1).animate.arrange(DOWN, buff=0.5, aligned_edge=RIGHT))

        first_circum = [6, 8, 12]
        second_circum = [10]
        self.playw(*[Circumscribe(VGroup(leftshape[i], shape1_[i]), color=GREEN_D) for i in first_circum])
        self.playw(*[Circumscribe(VGroup(leftshape[i], shape1_[i]), color=BLUE_D) for i in second_circum])

        leftshape_ = (
            CodeText("shape (7, 8, 4, 6)", font_size=36)
            .set_color_by_gradient(ORANGE, YELLOW_C)
            .move_to(leftshape)
            .align_to(leftshape, LEFT)
        ).next_to(leftshape, RIGHT, buff=0.75)
        shape1__ = (
            CodeText("shape (7, 8, 4, 6)", font_size=36)
            .set_color_by_gradient(RED_B, RED_D)
            .move_to(shape1_)
            .align_to(shape1_, LEFT)
        ).next_to(shape1_, RIGHT, buff=0.75)
        self.play(LaggedStart(Transform(leftshape.copy(), leftshape_), self.cf.animate.move_to(VGroup(leftshape_, shape1__)), lag_ratio=0.3))
        self.playw(Transform(shape1_.copy(), shape1__), VGroup(leftshape, shape1_).animate.set_opacity(0.2))
