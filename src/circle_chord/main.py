from manim import *
from raenim import *
import numpy as np
import random


class answerIntro(Scene2D):
    def construct(self):
        nl = NumberLine([0, 1, 0.3333], length=8)

        n3 = Integer(3).next_to(nl.n2p(0), DOWN).set_color(GREY_B)
        n333 = (
            MathTex(r"{{10}", "\over", r"{3}}")
            .scale(0.7)
            .next_to(nl.n2p(0.3333), DOWN)
            .set_color(YELLOW_C)
        )
        n4 = Integer(4).next_to(nl.n2p(1), DOWN).set_color(GREY_B)
        self.addw(nl, n3, n333, n4, wait=2)

        self.playw(
            RWiggle(n3, amp=(0.1, 0.1, 0.1)),
            RWiggle(n4, amp=(0.1, 0.1, 0.1)),
            run_time=3,
        )

        px3 = (
            MathTex(r"p(X=3)", "=", "{{2}", "\over", r"{3}}")
            .scale(0.7)
            .next_to(nl.n2p(0), UP)
        )
        px4 = (
            MathTex(r"p(X=4)", "=", "{{1}", "\over", r"{3}}")
            .scale(0.7)
            .next_to(nl.n2p(1), UP)
        )
        px3[-3:].set_color(GREEN)
        px4[-3:].set_color(GREEN)
        self.play(FadeIn(px3, shift=UP * 0.3))
        self.playw(FadeIn(px4, shift=UP * 0.3))


def cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]


def sign_nonzero(x, eps=1e-9):
    if x >= eps:
        return 1
    if x <= -eps:
        return -1
    return 1


def angle_of(p):
    ang = np.arctan2(p[1], p[0])
    return ang + TAU if ang < 0 else ang


def line_intersection(p1, p2, p3, p4, eps=1e-9):
    """Intersection point of infinite lines p1-p2 and p3-p4 (assumes not parallel)."""
    r = p2 - p1
    s = p4 - p3
    denom = cross2(r, s)
    if abs(denom) < eps:
        return None
    t = cross2(p3 - p1, s) / denom
    return p1 + t * r


def arc_points(center, R, a0, a1, n=48):
    """CCW arc points from angle a0 to a1, with wrap."""
    a0 %= TAU
    a1 %= TAU
    da = (a1 - a0) % TAU
    angles = [a0 + da * (i / (n - 1)) for i in range(n)]
    return [center + R * np.array([np.cos(a), np.sin(a), 0.0]) for a in angles]


def make_filled_vm(points, color, opacity=0.75):
    """points: list of R3 points, should be closed or will be closed."""
    pts = list(points)
    if np.linalg.norm(pts[0] - pts[-1]) > 1e-7:
        pts.append(pts[0])
    vm = VMobject()
    vm.set_points_as_corners(pts)
    vm.set_stroke(width=0)
    vm.set_fill(color, opacity=opacity)
    return vm


def centroid(points):
    pts = np.array(points)
    return np.mean(pts, axis=0)


# -------------------------
# Scene
# -------------------------
class ChordPartitionAlwaysRedraw(Scene2D):
    def construct(self):
        num_intro = 17
        num_problem1 = 17
        num_problem2 = 25
        random.seed(num_problem2)
        np.random.seed(7)

        R = 2.5
        center = ORIGIN

        circle = Circle(radius=R).set_stroke(width=3, color=GREY_A)

        # Trackers: A,B,C,D
        trackers = [ValueTracker(random.random() * TAU) for _ in range(4)]

        def P(theta):
            return center + R * np.array([np.cos(theta), np.sin(theta), 0.0])

        def get_pts():
            A = P(trackers[0].get_value())
            B = P(trackers[1].get_value())
            C = P(trackers[2].get_value())
            D = P(trackers[3].get_value())
            return A, B, C, D

        # Dots
        dot_colors = [BLUE_E, GREEN_E, ORANGE, PURPLE_E]
        dots = VGroup(
            *[
                always_redraw(
                    lambda i=i: Dot(
                        P(trackers[i].get_value()), radius=0.1, color=dot_colors[i]
                    )
                )
                for i in range(4)
            ]
        )

        # Chords
        chord1 = always_redraw(
            lambda: Line(get_pts()[0], get_pts()[1]).set_stroke(width=2, color=GREY_B)
        )
        chord2 = always_redraw(
            lambda: Line(get_pts()[2], get_pts()[3]).set_stroke(width=2, color=GREY_B)
        )

        # Stable label colors
        label_order = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        label_to_color = {
            (1, 1): BLUE_E,
            (1, -1): GREEN_E,
            (-1, 1): ORANGE,
            (-1, -1): PURPLE_E,
        }

        faces = VGroup().set_z_index(-1)

        def build_regions():
            A, B, C, D = get_pts()

            # Sort points on circle by angle
            items = [("A", A), ("B", B), ("C", C), ("D", D)]
            items_sorted = sorted(items, key=lambda kv: angle_of(kv[1]))
            keys = [k for k, _ in items_sorted]
            pts = {k: p for k, p in items_sorted}
            idx = {k: i for i, k in enumerate(keys)}

            def is_adj(i, j):
                return (i - j) % 4 in (1, 3)

            # Intersect iff both chords connect non-adjacent vertices in this cyclic order.
            AB_inter = not is_adj(idx["A"], idx["B"])
            CD_inter = not is_adj(idx["C"], idx["D"])
            crossing = AB_inter and CD_inter

            # Helper: CCW arc from u to v following circle order (u->v along CCW)
            def arc_u_to_v(u, v, n=48):
                return arc_points(center, R, angle_of(pts[u]), angle_of(pts[v]), n=n)

            # Build raw region boundaries as sampled points (closed later)
            region_boundaries = []

            if crossing:
                # chords must be (k0-k2) and (k1-k3) in this order
                # intersection point P
                P0 = line_intersection(A, B, C, D)
                if P0 is None:
                    # degenerate fallback: no regions
                    region_boundaries = []
                else:
                    # For each consecutive pair along circle (ki -> k(i+1)):
                    # boundary = arc(ki->k(i+1)) + line(k(i+1)->P) + line(P->ki)
                    for i in range(4):
                        u = keys[i]
                        v = keys[(i + 1) % 4]
                        boundary = []
                        boundary += arc_u_to_v(u, v, n=48)
                        boundary += [P0]  # from v to P0 (straight)
                        boundary += [
                            pts[u]
                        ]  # close via straight P0->u (we'll close explicitly later)
                        region_boundaries.append(boundary)

            else:
                # Non-crossing: AB and CD must each be adjacent in the cyclic order.
                # Find which adjacent pair is AB and which is CD.
                # Determine oriented adjacency for AB
                iA, iB = idx["A"], idx["B"]
                if (iA + 1) % 4 == iB:
                    AB_u, AB_v = "A", "B"  # A->B is CCW-adjacent
                else:
                    AB_u, AB_v = "B", "A"  # B->A is CCW-adjacent

                iC, iD = idx["C"], idx["D"]
                if (iC + 1) % 4 == iD:
                    CD_u, CD_v = "C", "D"
                else:
                    CD_u, CD_v = "D", "C"

                # Cap regions:
                # cap for chord (u,v): arc(u->v) (short, adjacent) + line(v->u)
                cap1 = arc_u_to_v(AB_u, AB_v, n=48) + [
                    pts[AB_u]
                ]  # close with straight AB_v->AB_u via corners
                # But we must include the chord explicitly: arc + (v->u) line is implied by corners,
                # so we add the chord endpoint as last segment start:
                cap1 = arc_u_to_v(AB_u, AB_v, n=48) + [
                    pts[AB_u]
                ]  # VMobject corners will connect last to first

                cap2 = arc_u_to_v(CD_u, CD_v, n=48) + [pts[CD_u]]

                # Middle region:
                # line(AB_u->AB_v) + arc(AB_v->CD_u) + line(CD_u->CD_v) + arc(CD_v->AB_u)
                mid = []
                mid += [pts[AB_u], pts[AB_v]]  # chord AB
                mid += arc_u_to_v(AB_v, CD_u, n=48)[
                    1:
                ]  # arc to CD_u (skip duplicate start)
                mid += [pts[CD_v]]  # chord CD from CD_u->CD_v (implicit via corners)
                mid += arc_u_to_v(CD_v, AB_u, n=48)[1:]
                region_boundaries = [cap1, cap2, mid]

            # Convert boundaries -> face VMobjects, label by (s1,s2)
            AB_vec = B - A
            CD_vec = D - C

            faces_by_label = {}

            for boundary in region_boundaries:
                # ensure we have enough points
                if len(boundary) < 3:
                    continue

                core = centroid(boundary)
                s1 = sign_nonzero(cross2(AB_vec, core - A))
                s2 = sign_nonzero(cross2(CD_vec, core - C))
                lab = (s1, s2)

                col = label_to_color.get(lab, GREY_B)
                faces_by_label[lab] = make_filled_vm(boundary, col, opacity=0.75)

            # Always return 4 slots to reduce flicker when 3<->4 changes
            out = VGroup()
            for lab in label_order:
                if lab in faces_by_label:
                    out.add(faces_by_label[lab])
                else:
                    # transparent placeholder
                    tiny = [
                        center + 1e-6 * RIGHT,
                        center + 1e-6 * UP,
                        center + 1e-6 * LEFT,
                        center + 1e-6 * RIGHT,
                    ]
                    ph = make_filled_vm(tiny, label_to_color[lab], opacity=0.0)
                    out.add(ph)
            return out

        # intro
        # self.playw(GrowFromCenter(circle))
        # self.playw(FadeIn(dots[0], scale=4), FadeIn(dots[1], scale=4))
        # self.playw(Create(chord1))
        # self.playw(FadeIn(dots[2], scale=4), FadeIn(dots[3], scale=4))
        # self.playw(Create(chord2))

        # self.addw(faces)
        # faces.add_updater(lambda m: m.become(build_regions()).set_z_index(-1))

        # num_region = always_redraw(
        #     lambda: Text(
        #         f"영역 개수: {len([f for f in faces if f.get_fill_opacity() > 0.1])}",
        #         font="Noto Sans KR",
        #         color=GREY_B,
        #     ).scale(0.7)
        #     .to_corner(LEFT)
        #     .set_z_index(10)
        # )
        # self.add(num_region)

        # self.playw(
        #     trackers[0].animate.set_value(trackers[0].get_value()),
        #     trackers[1].animate.set_value(trackers[1].get_value()),
        #     trackers[2].animate.set_value(trackers[2].get_value()),
        #     trackers[3].animate.set_value(trackers[3].get_value()),
        #     rate_func=smooth,
        #     wait=1,
        # )
        # self.playw(
        #     trackers[0].animate.set_value(trackers[0].get_value() - 2),
        #     trackers[1].animate.set_value(trackers[1].get_value()),
        #     trackers[2].animate.set_value(trackers[2].get_value()),
        #     trackers[3].animate.set_value(trackers[3].get_value()),
        #     run_time=3,
        #     rate_func=smooth,
        # )
        # /intro

        # moving four dots and expectation
        # self.playw(
        #     trackers[0].animate.set_value(trackers[0].get_value() + 2),
        #     trackers[1].animate.set_value(trackers[1].get_value() + 1.5),
        #     trackers[2].animate.set_value(trackers[2].get_value() + 12),
        #     trackers[3].animate.set_value(trackers[3].get_value() + 15),
        #     run_time=10,
        #     rate_func=smooth,
        # )

        # self.play(self.cf.animate.shift(LEFT), FadeOut(num_region[4:]))
        # expectation_open = MathTex(r"\mathbb{E}[").next_to(num_region, LEFT, buff=0.1)
        # expectation_close = MathTex(r"]").next_to(num_region[3], buff=0.1)
        # self.playw(FadeIn(expectation_open), FadeIn(expectation_close))
        # /moving four dots and expectation

        # describe problem
        # uniform_random = MathTex(
        #     r"X_1",
        #     ",",
        #     r"X_2",
        #     ",",
        #     r"X_3",
        #     ",",
        #     r"X_4",
        #     r"\sim",
        #     r"\mathrm{Uniform}(0, 2\pi)",
        # )
        # self.playwl(
        #     *[
        #         FadeIn(item)
        #         for item in [
        #             uniform_random[:-2],
        #             uniform_random[-2],
        #             uniform_random[-1],
        #         ]
        #     ],
        #     lag_ratio=0.3,
        # )
        # indices = [0, 2, 4, 6]
        # nums = VGroup(
        #     *[
        #         DecimalNumber(num, num_decimal_places=2).scale(0.7)
        #         for num in [trackers[i].get_value() for i in range(4)]
        #     ]
        # )
        # for j in range(4):
        #     nums[j].move_to(uniform_random[indices[j]])
        # self.play(
        #     *[
        #         Transform(
        #             uniform_random[i],
        #             nums[j],
        #             replace_mobject_with_target_in_scene=True,
        #         )
        #         for j, i in enumerate(indices)
        #     ],
        #     *[
        #         FadeOut(uniform_random[i])
        #         for i in range(len(uniform_random))
        #         if i not in indices
        #     ],
        # )
        # self.playwl(
        #     AnimationGroup(
        #         *[
        #             Transform(
        #                 nums[j], dots[j], replace_mobject_with_target_in_scene=True
        #             )
        #             for j in range(4)
        #         ]
        #     ),
        #     FadeIn(circle),
        #     lag_ratio=0.4,
        #     wait=0,
        # )
        # self.playw(Create(chord1), Create(chord2))
        # face = build_regions()
        # self.play(FadeIn(face.set_z_index(-1)))
        # num_region = (
        #     Text(
        #         f"영역 개수: {len([f for f in face if f.get_fill_opacity() > 0.1])}",
        #         font="Noto Sans KR",
        #         color=GREY_B,
        #     )
        #     .scale(0.7)
        #     .to_corner(LEFT)
        #     .set_z_index(10)
        # )
        # self.playw(FadeIn(num_region))
        # /describe problem

        # solution
        self.addw(circle, wait=2)
        self.play(FadeIn(dots))
        self.playw(
            trackers[0].animate.set_value(trackers[0].get_value() + 2),
            trackers[1].animate.set_value(trackers[1].get_value() + 1.5),
            trackers[2].animate.set_value(trackers[2].get_value() + 12),
            trackers[3].animate.set_value(trackers[3].get_value() + 15),
            run_time=5,
            rate_func=smooth,
        )
        self.play(FadeIn(VGroup(chord1, chord2).set_opacity(0)), run_time=0.1)
        self.remove(chord1, chord2)
        VGroup(chord1, chord2).set_opacity(1)
        self.play(Create(chord1), Create(chord2))
        self.playw(
            *[Indicate(dot, scale_factor=3, color=PURE_RED) for dot in dots],
            run_time=1.5,
        )
        self.playw(FadeOut(chord1), FadeOut(chord2))

        self.playwl(
            *[Indicate(dot, color=PURE_GREEN, scale_factor=2) for dot in dots],
            lag_ratio=0.25,
        )

        line_pairs = [
            [(0, 1), (2, 3)],
            [(0, 2), (1, 3)],
            [(0, 3), (1, 2)],
            [(1, 2), (0, 3)],
            [(1, 3), (0, 2)],
            [(2, 3), (0, 1)],
        ]
        chords_pairs = VGroup()
        for (i1, j1), (i2, j2) in line_pairs:
            chord_a = Line(get_pts()[i1], get_pts()[j1]).set_stroke(width=3, color=BLUE)
            chord_b = Line(get_pts()[i2], get_pts()[j2]).set_stroke(width=3, color=RED)
            chords_pairs.add(VGroup(circle.copy(), chord_a, chord_b))

        chords_pairs.generate_target()
        for item in chords_pairs.target:
            item[0].set_stroke(width=1, color=GREY_C)
            item.scale(0.4)
        chords_pairs.target.arrange_in_grid(2, 3, buff=0.8).next_to(
            circle, RIGHT, buff=2.5
        )
        self.play(FadeIn(chords_pairs))
        self.cf.save_state()
        self.playwl(
            MoveToTarget(chords_pairs),
            self.cf.animate.scale(1.6).align_to(self.cf, LEFT),
        )

        c42 = (
            MathTex(r"_4C_2", "=", "6", color=GREEN)
            .scale(1.2)
            .next_to(chords_pairs, DOWN, buff=0.5)
        )
        self.playw(FadeIn(c42, shift=DOWN * 0.3))

        ol = Overlay().update_coverage(chords_pairs[1:-1])
        chords_pairs[0].set_z_index(ol.z_index + 1)
        chords_pairs[-1].set_z_index(ol.z_index + 1)
        self.play(FadeIn(ol), run_time=0.5)
        self.play(
            RWiggle(chords_pairs[0], amp=(0.13, 0.13, 0.13)),
            RWiggle(chords_pairs[-1], amp=(0.13, 0.13, 0.13)),
            run_time=3,
        )
        self.play(FadeOut(ol), run_time=0.5)
        ol = Overlay().update_coverage(VGroup(chords_pairs[0], chords_pairs[-1]))
        chords_pairs[1:-1].set_z_index(ol.z_index + 1)
        self.play(FadeIn(ol), run_time=0.5)
        self.play(
            RWiggle(chords_pairs[1], amp=(0.13, 0.13, 0.13)),
            RWiggle(chords_pairs[2], amp=(0.13, 0.13, 0.13)),
            RWiggle(chords_pairs[3], amp=(0.13, 0.13, 0.13)),
            RWiggle(chords_pairs[4], amp=(0.13, 0.13, 0.13)),
            run_time=3,
        )
        self.play(FadeOut(chords_pairs, c42), run_time=0.5)
        self.remove(ol)
        self.playw(Restore(self.cf), circle.animate.set_stroke(width=2, color=GREY_D))

        four_lines = VGroup()
        pairs = [(0, 2), (0, 3), (1, 2), (1, 3)]

        def get_partial_fn(i, j):
            def fn():
                return Line(get_pts()[i], get_pts()[j]).set_stroke(
                    width=3, color=GREY_B
                )

            return fn

        for i, j in pairs:
            # line = Line(get_pts()[i], get_pts()[j]).set_stroke(width=3, color=GREY_B)
            line = always_redraw(get_partial_fn(i, j))
            four_lines.add(line)
        self.playw(FadeIn(four_lines, chord1, chord2))
        self.playw(
            trackers[0].animate.set_value(trackers[0].get_value() - 2),
            trackers[1].animate.set_value(trackers[1].get_value() - 1.5),
            trackers[2].animate.set_value(trackers[2].get_value() - 12),
            trackers[3].animate.set_value(trackers[3].get_value() - 15),
            run_time=5,
            rate_func=smooth,
        )

        nl = (
            NumberLine([0, 1, 0.3333], length=6)
            .next_to(circle, RIGHT, buff=1.5)
            .shift(DOWN)
        )
        n3 = Integer(3).next_to(nl.n2p(0), DOWN).set_color(GREY_B)
        n333 = (
            MathTex(r"{{10}", "\over", r"{3}}")
            .scale(0.7)
            .next_to(nl.n2p(0.3333), DOWN)
            .set_color(YELLOW_C)
        )
        n4 = Integer(4).next_to(nl.n2p(1), DOWN).set_color(GREY_B)
        cases = VGroup()
        for lp in line_pairs:
            (i1, j1), (i2, j2) = lp
            case_chord1 = Line(get_pts()[i1], get_pts()[j1]).set_stroke(
                width=2, color=GREY_B
            )
            case_chord2 = Line(get_pts()[i2], get_pts()[j2]).set_stroke(
                width=2, color=GREY_B
            )
            cases.add(
                VGroup(
                    circle.copy().set_opacity(0),
                    dots.copy().set_opacity(0),
                    case_chord1,
                    case_chord2,
                )
            )
        self.remove(four_lines, chord1, chord2)
        self.addw(cases)

        cross_idx = [0, 5]
        cross_cases = VGroup(*[cases[i] for i in cross_idx])
        noncross_cases = VGroup(
            *[cases[i] for i in range(len(cases)) if i not in cross_idx]
        )
        cross_cases.generate_target().scale(0.3)
        cross_cases[0][0].set_stroke(opacity=1)
        for item in cross_cases.target:
            item[0].set_stroke(opacity=1)
            item[1].set_opacity(1)
        cross_cases.target.arrange(DOWN).next_to(nl.n2p(1), UP, buff=0.5)
        noncross_cases.generate_target().scale(0.3)
        for item in noncross_cases.target:
            item[0].set_stroke(opacity=1)
            item[1].set_opacity(1)
        noncross_cases.target.arrange(DOWN).next_to(nl.n2p(0), UP, buff=0.5)

        self.playw(
            MoveToTarget(cross_cases),
            self.cf.animate.scale(1.5).align_to(self.cf, LEFT).shift(UP),
            MoveToTarget(noncross_cases),
            FadeIn(nl, n3, n333, n4),
        )

        finalr = MathTex(r"{2 \over 6}", r"\times", "4").next_to(cross_cases[-2], LEFT, buff=0.2)
        finall = MathTex(r"{4 \over 6}", r"\times", "3").next_to(noncross_cases[-2], RIGHT, buff=0.2)
        self.playw(FadeIn(finalr, shift=LEFT * 0.3))
        self.playw(FadeIn(finall, shift=RIGHT * 0.3))
        final = MathTex(r"{{20}", "\over", r"{6}}").move_to(VGroup(finalr, finall).get_center())
        self.play(FadeTransform(VGroup(finalr, finall), final), run_time=1.5)
        self.play(Transform(final, n333.copy()))
        self.remove(final)
        self.wait()