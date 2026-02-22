from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene2D):
    def construct(self):
        # --- Entity Definitions ---

        # 1. git pull = fetch + merge
        git_pull = Words("git pull", font="Noto Sans KR", font_size=36, color=BLUE)
        eq = Text("=", font_size=36)
        fetch_merge = Words("fetch + merge", font="Noto Sans KR", font_size=36)
        fetch_merge.words[0].set_color(GREEN)
        fetch_merge.words[1].set_color(GREY_C)
        fetch_merge.words[2].set_color(PURPLE)

        pull_eq = VGroup(git_pull, eq, fetch_merge).arrange(RIGHT, buff=0.3)
        pull_eq.to_edge(DOWN, buff=1.5)

        # 2. Remote: main (위쪽) — 커밋 하나 더 있음
        r_c0 = get_commit()
        r_c1, rl1 = new_commit(r_c0)
        r_c2, rl2 = new_commit(r_c1)
        r_c3, rl3 = new_commit(r_c2)  # remote에만 있는 커밋
        remote_branch = VGroup(r_c0, rl1, r_c1, rl2, r_c2, rl3, r_c3)
        VGroup(rl3, r_c3).set_color(GREEN)
        r_c3.set_fill(opacity=0)
        remote_branch.shift(UP * 1.2)

        remote_label = Text("main", font_size=24, color=GREEN).next_to(
            r_c3, RIGHT, buff=0.3
        )
        remote_tag = Text("Remote", font_size=20, color=GREY_B).next_to(
            remote_branch, LEFT, buff=0.5
        )

        # 3. Local: main (아래쪽) — 커밋 하나 적음
        l_c0 = get_commit()
        l_c1, ll1 = new_commit(l_c0)
        l_c2, ll2 = new_commit(l_c1)
        local_branch = VGroup(l_c0, ll1, l_c1, ll2, l_c2)
        local_branch.shift(DOWN * 0.5)

        main_label = Text("main", font_size=24, color=BLUE).next_to(
            l_c2, RIGHT, buff=0.3
        )
        local_tag = Text("Local", font_size=20, color=GREY_B).next_to(
            local_branch, LEFT, buff=0.5
        )

        # 4. origin/main: fetch로 remote에서 가져온 상태 (local 영역)
        oc, ol = new_commit(l_c2, direction=UR, buff=0.5)
        origin_commit = VGroup(oc, ol)
        origin_branch = origin_commit
        origin_label = Text("origin/main", font_size=24, color=GREEN).next_to(
            origin_branch[0], RIGHT, buff=0.3
        )

        # 전체 브랜치 그래프
        branch_graph = VGroup(
            remote_branch,
            remote_label,
            remote_tag,
            local_branch,
            main_label,
            local_tag,
            origin_branch,
            origin_label,
        )
        branch_graph.move_to(UP * 0.3)

        # 5. divergent 경고 메시지
        warning = CodeText(
            "hint: Diverging branches can't be reconciled.",
            font_size=20,
        ).set_color(RED)
        warning.to_edge(DOWN, buff=0.8)

        # --- End Entity Definitions ---

        # 이걸 이해하려면 git pull의 동작을 알아야해서 먼저 볼게요
        git_pull.save_state()
        git_pull.move_to(ORIGIN)
        self.playw(*[FadeIn(item) for item in git_pull.words])
        self.play(Restore(git_pull))
        self.playw(FadeIn(eq))
        # git pull은요 두 단계를 한 번에 실행하는 명령입니다. 첫 번째는 fetch,
        self.playw(FadeIn(fetch_merge.words[1]))
        self.playw(FadeIn(fetch_merge.words[0]))
        # remote에 있는 코드를 가져오는 단계구요
        self.play(FadeIn(remote_branch, remote_label, remote_tag))
        self.playw(
            FadeIn(local_branch, main_label, local_tag),
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
        )
        # 두 번째는 가져온 코드를 내 branch에 합치는 단계입니다
        self.playw(FadeIn(fetch_merge.words[2]))
        l_c3, ll3 = new_commit(l_c2)
        self.playwl(
            main_label.animate.next_to(l_c3, RIGHT, buff=0.3),
            AnimationGroup(Transformr(oc.copy(), l_c3), Transformr(ol.copy(), ll3)),
            lag_ratio=0.2,
        )

        # 그런데 문제는요 remote랑 내 local branch의 최신 commit, 이 head가 갈라져 있을 때 생깁니다
        self.playw(
            FadeOut(l_c3, ll3, shift=DOWN * 0.5), FadeOut(origin_branch, origin_label)
        )
        l_c3, ll3 = new_commit(l_c2)
        l_c3.set_color(YELLOW_B).set_fill(opacity=0)
        ll3.set_color(YELLOW_B)
        self.playw(FadeIn(l_c3, ll3))

        # 이게 무슨 말이냐면요 나도 local에서 commit을 했고
        self.playw(Flash(l_c3.get_corner(UL), line_length=0.15, num_lines=15))
        # remote에도 commit이 올라와있어서요
        self.playw(Flash(r_c3.get_corner(UL), line_length=0.15, num_lines=15))

        # 두 branch가 서로 다른 방향으로 뻗어나간 상태입니다
        overlay = self.overlay
        VGroup(l_c3, ll3, r_c3, rl3).set_z_index(overlay.z_index + 1)
        self.playw(FadeIn(overlay))

        # 이 상태에서 git pull을 하면은요
        self.play(FadeOut(overlay))
        self.playw(Flash(git_pull.get_corner(UL)))
        # fetch로 가져오긴 했는데
        oc.set_color(GREEN).set_fill(opacity=0)
        ol.set_color(GREEN)
        self.playw(
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
        )
        # 합치는 방법을 안 정해줘서 못 하겠다 라는 뜻의 경고가 뜨고,
        # 이게 divergent한 상태입니다
        update_fn = lambda m: m.put_start_and_end_on(
            l_c2.point_at_angle(
                np.arctan2(
                    oc.get_center()[1] - l_c2.get_center()[1],
                    oc.get_center()[0] - l_c2.get_center()[0],
                )
            ),
            oc.point_at_angle(
                np.arctan2(
                    l_c2.get_center()[1] - oc.get_center()[1],
                    l_c2.get_center()[0] - oc.get_center()[0],
                )
            ),
        )
        ol.add_updater(update_fn)
        ocorig = oc.get_center()
        self.play(
            oc.animate.next_to(l_c3, UL, buff=-0.07), run_time=0.6, rate_func=rush_into
        )
        oc.set_color(PURE_RED).set_fill(opacity=0)
        ol.set_color(RED)
        self.playw(oc.animate.move_to(ocorig), run_time=0.6, rate_func=rush_from)
        ol.remove_updater(update_fn)

        # 그러니까 문제는 pull 자체가 아니라요
        self.play(fetch_merge.words.animate.set_opacity(0.3))
        # 합치는 전략을 git이 모른다는 점입니다
        self.play(fetch_merge.words[2].animate.set_opacity(1))
        self.playw(Indicate(fetch_merge.words[2], color=RED))

        # 그러면 이 상황에서 합치는 방법은 왜 여러 개가 필요한 걸까요?
        overlay2 = self.overlay.copy().set_z_index(overlay.z_index + 2).scale(1.2)
        fetch_merge.words[2].set_z_index(overlay2.z_index + 1)
        self.play(FadeIn(overlay2))
        self.playw(Indicate(fetch_merge.words[2], color=RED))


class merge(Scene2D):
    def construct(self):
        # --- Entity Definitions ---

        # title
        title = CodeText("pull.rebase false", font_size=28)
        title.to_edge(UP, buff=0.5)

        # Remote: main
        r_c0 = get_commit()
        r_c1, rl1 = new_commit(r_c0)
        r_c2, rl2 = new_commit(r_c1)
        r_c3, rl3 = new_commit(r_c2)
        remote_branch = VGroup(r_c0, rl1, r_c1, rl2, r_c2, rl3, r_c3)
        VGroup(rl3, r_c3).set_color(GREEN)
        r_c3.set_fill(opacity=0)
        remote_branch.shift(UP * 1.2)

        remote_label = Text("main", font_size=24, color=GREEN).next_to(
            r_c3, RIGHT, buff=0.3
        )
        remote_tag = Text("Remote", font_size=20, color=GREY_B).next_to(
            remote_branch, LEFT, buff=0.5
        )

        # Local: main (divergent — 내 커밋 포함)
        l_c0 = get_commit()
        l_c1, ll1 = new_commit(l_c0)
        l_c2, ll2 = new_commit(l_c1)
        l_c3, ll3 = new_commit(l_c2)
        local_branch = VGroup(l_c0, ll1, l_c1, ll2, l_c2, ll3, l_c3)
        VGroup(ll3, l_c3).set_color(YELLOW_B)
        l_c3.set_fill(opacity=0)
        local_branch.shift(DOWN * 0.5)

        main_label = Text("main", font_size=24, color=BLUE).next_to(
            l_c3, RIGHT, buff=0.3
        )
        local_tag = Text("Local", font_size=20, color=GREY_B).next_to(
            local_branch, LEFT, buff=0.5
        )

        # origin/main: fetch로 가져온 상태
        oc, ol = new_commit(l_c2, direction=UR, buff=0.5)
        oc.set_color(GREEN).set_fill(opacity=0)
        ol.set_color(GREEN)
        origin_branch = VGroup(oc, ol)
        origin_label = Text("origin/main", font_size=24, color=GREEN).next_to(
            oc, RIGHT, buff=0.3
        )

        branch_graph = VGroup(
            remote_branch,
            remote_label,
            remote_tag,
            local_branch,
            main_label,
            local_tag,
            origin_branch,
            origin_label,
        )
        branch_graph.move_to(UP * 0.3)

        # --- End Entity Definitions ---

        # 먼저 pull.rebase false, 즉 merge 방식부터 볼게요
        self.playw(FadeIn(title))
        self.play(FadeIn(remote_branch, remote_label, remote_tag))
        self.playw(FadeIn(local_branch, main_label, local_tag))

        # merge는 가져온 commit들이 내 local 상태에 주는 변화를요
        self.playw(
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
        )
        # 최신 HEAD에 merge commit으로 얹습니다
        merge_c, merge_l = new_commit(l_c3)
        merge_c.set_color(GREEN).set_fill(opacity=0)
        merge_l.set_color(GREEN)
        merge_l2 = DashedLine(
            oc.get_right(),
            merge_c.get_left(),
            color=GREEN,
            stroke_width=2,
            dash_length=0.1,
            dashed_ratio=0.7,
        )
        self.playwl(
            main_label.animate.next_to(merge_c, RIGHT, buff=0.3),
            AnimationGroup(FadeIn(merge_c, merge_l, merge_l2)),
            lag_ratio=0.2,
        )

        # 그래서 내 commit들이랑 remote commit들을 그대로 두고
        self.playw(
            Flash(l_c3.get_corner(UL), line_length=0.15, num_lines=15),
            Flash(oc.get_corner(UL), line_length=0.15, num_lines=15),
        )
        # 새 commit이 하나 만들어집니다
        self.playw(
            Flash(merge_c.get_corner(UL), line_length=0.15, num_lines=15, color=GREEN)
        )


class rebase(Scene2D):
    def construct(self):
        # --- Entity Definitions ---

        # title
        title = CodeText("pull.rebase true", font_size=28)
        title.to_edge(UP, buff=0.5)

        # Remote: main
        r_c0 = get_commit()
        r_c1, rl1 = new_commit(r_c0)
        r_c2, rl2 = new_commit(r_c1)
        r_c3, rl3 = new_commit(r_c2)
        remote_branch = VGroup(r_c0, rl1, r_c1, rl2, r_c2, rl3, r_c3)
        VGroup(rl3, r_c3).set_color(GREEN)
        r_c3.set_fill(opacity=0)
        remote_branch.shift(UP * 1.2)

        remote_label = Text("main", font_size=24, color=GREEN).next_to(
            r_c3, RIGHT, buff=0.3
        )
        remote_tag = Text("Remote", font_size=20, color=GREY_B).next_to(
            remote_branch, LEFT, buff=0.5
        )

        # Local: main (divergent — 내 커밋 포함)
        l_c0 = get_commit()
        l_c1, ll1 = new_commit(l_c0)
        l_c2, ll2 = new_commit(l_c1)
        l_c3, ll3 = new_commit(l_c2)
        local_branch = VGroup(l_c0, ll1, l_c1, ll2, l_c2, ll3, l_c3)
        VGroup(ll3, l_c3).set_color(YELLOW_B)
        l_c3.set_fill(opacity=0)
        local_branch.shift(DOWN * 0.5)

        main_label = Text("main", font_size=24, color=BLUE).next_to(
            l_c3, RIGHT, buff=0.3
        )
        local_tag = Text("Local", font_size=20, color=GREY_B).next_to(
            local_branch, LEFT, buff=0.5
        )

        # origin/main: fetch로 가져온 상태
        oc, ol = new_commit(l_c2, direction=UR, buff=0.5)
        oc.set_color(GREEN).set_fill(opacity=0)
        ol.set_color(GREEN)
        origin_branch = VGroup(oc, ol)
        origin_label = Text("origin/main", font_size=24, color=GREEN).next_to(
            oc, RIGHT, buff=0.3
        )

        branch_graph = VGroup(
            remote_branch,
            remote_label,
            remote_tag,
            local_branch,
            main_label,
            local_tag,
            origin_branch,
            origin_label,
        )
        branch_graph.move_to(UP * 0.3)

        # --- End Entity Definitions ---

        # 다음은 pull.rebase true, rebase 방식입니다
        self.playw(FadeIn(title))
        self.play(FadeIn(remote_branch, remote_label, remote_tag))
        self.playw(FadeIn(local_branch, main_label, local_tag))
        # 이 방식은 내 commit을 remote의 변경 뒤에 다시 쌓는 방법입니다
        self.playw(
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
        )
        # 이게 무슨 말이냐면요
        # remote와 local에서 공통 조상 즉 branch의 갈라져나온 commit을 우선 찾습니다
        self.playw(Indicate(l_c2, color=RED))

        # 그 다음에 local에서 갈라져나온 이후 commit 변화들을 들어내서요
        self.playw(VGroup(l_c3, ll3, main_label).animate.shift(DR * 0.9))

        # remote의 commit들을 얹은 다음
        l_cb, llb = new_commit(l_c2)
        l_cb.set_color(GREEN).set_fill(opacity=0)
        llb.set_color(GREEN)
        self.playw(
            Transformr(oc.copy(), l_cb),
            Transformr(ol.copy(), llb),
        )

        # 그 위에다가 들어낸 local 변화를 얹습니다
        self.playw(VGroup(l_c3, ll3, main_label).animate.next_to(l_cb, RIGHT, buff=0.0))


class fastforward(Scene2D):
    def construct(self):
        # --- Entity Definitions ---

        # title
        title = CodeText("fast-forward", font_size=28)
        title.to_edge(UP, buff=0.5)

        # Remote: main
        r_c0 = get_commit()
        r_c1, rl1 = new_commit(r_c0)
        r_c2, rl2 = new_commit(r_c1)
        r_c3, rl3 = new_commit(r_c2)
        remote_branch = VGroup(r_c0, rl1, r_c1, rl2, r_c2, rl3, r_c3)
        VGroup(rl3, r_c3).set_color(GREEN)
        r_c3.set_fill(opacity=0)
        remote_branch.shift(UP * 1.2)

        remote_label = Text("main", font_size=24, color=GREEN).next_to(
            r_c3, RIGHT, buff=0.3
        )
        remote_tag = Text("Remote", font_size=20, color=GREY_B).next_to(
            remote_branch, LEFT, buff=0.5
        )

        # Local: main (NO divergence — local 커밋 없음)
        l_c0 = get_commit()
        l_c1, ll1 = new_commit(l_c0)
        l_c2, ll2 = new_commit(l_c1)
        local_branch = VGroup(l_c0, ll1, l_c1, ll2, l_c2)
        local_branch.shift(DOWN * 0.5)

        main_label = Text("main", font_size=24, color=BLUE).next_to(
            l_c2, RIGHT, buff=0.3
        )
        local_tag = Text("Local", font_size=20, color=GREY_B).next_to(
            local_branch, LEFT, buff=0.5
        )

        # origin/main: fetch 결과 (RIGHT — divergent 아니므로 직선)
        oc, ol = new_commit(l_c2, direction=UR, buff=0.5)
        oc.set_color(GREEN).set_fill(opacity=0)
        ol.set_color(GREEN)
        origin_branch = VGroup(oc, ol)
        origin_label = Text("origin/main", font_size=24, color=GREEN).next_to(
            oc, RIGHT, buff=0.3
        )

        branch_graph = VGroup(
            remote_branch,
            remote_label,
            remote_tag,
            local_branch,
            main_label,
            local_tag,
            origin_branch,
            origin_label,
        )
        branch_graph.move_to(UP * 0.3)

        # --- End Entity Definitions ---

        # 그러면 이제 fast-forward는 뭘까요?
        self.playw(FadeIn(title))
        # 사실 fast-forward는요 divergent 상태에서 합치는 전략이 아닙니다
        # fast-forward란 합칠 필요가 없는 상황에서 업데이트만 하고요
        # HEAD를 쭉 밀기만 하겠다는 의미입니다
        # → 간단한 시각화: HEAD가 앞으로 밀리는 모습
        demo_c0 = get_commit()
        demo_c1, demo_l1 = new_commit(demo_c0)
        demo_c2, demo_l2 = new_commit(demo_c1)
        demo_c2.set_color(GREEN).set_fill(opacity=0)
        demo_l2.set_color(GREEN)
        demo_branch = VGroup(demo_c0, demo_l1, demo_c1, demo_l2, demo_c2)
        demo_branch.move_to(ORIGIN)
        demo_head = Text("HEAD", font_size=22, color=YELLOW).next_to(
            demo_c1, UP, buff=0.2
        )
        demo_arrow = Arrow(
            demo_head.get_right() + RIGHT * 0.3,
            demo_c2.get_top() + UP * 0.3,
            color=YELLOW,
            stroke_width=3,
        )
        self.play(FadeIn(demo_branch, demo_head))
        self.playw(
            demo_head.animate.next_to(demo_c2, UP, buff=0.2),
            GrowArrow(demo_arrow),
            run_time=1.2,
        )
        self.playw(FadeOut(demo_branch, demo_head, demo_arrow))

        # 이게 무슨 말이냐면요
        # 내가 commit을 하나도 안 하고 remote만 업데이트가 있는 상태를 생각해보면은요
        self.play(FadeIn(remote_branch, remote_label, remote_tag))
        self.playw(FadeIn(local_branch, main_label, local_tag))

        # 그러면 그냥 remote가 앞에 있는 거죠?
        self.playw(Flash(r_c3.get_corner(UL), line_length=0.15, num_lines=15))

        # 이 때는 merge도 rebase도 필요가 없이요
        # remote 브랜치의 상태를 가져와서
        self.playw(
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
        )

        # 내 branch의 head를 remote가 앞서간만큼
        # 앞으로 옮기기만 하면 됩니다
        # 이 과정이 fast-forward입니다
        l_c3, ll3 = new_commit(l_c2)
        l_c3.set_color(GREEN).set_fill(opacity=0)
        ll3.set_color(GREEN)
        self.playwl(
            main_label.animate.next_to(l_c3, RIGHT, buff=0.3),
            AnimationGroup(Transformr(oc.copy(), l_c3), Transformr(ol.copy(), ll3)),
            lag_ratio=0.2,
        )
        self.playw(
            Flash(main_label.get_corner(UL), line_length=0.15, num_lines=15, color=BLUE)
        )


class ffonly(Scene2D):
    def construct(self):
        # --- Entity Definitions ---

        # title
        title = CodeText("pull.ff only", font_size=28)
        title.to_edge(UP, buff=0.5)

        # Remote: main
        r_c0 = get_commit()
        r_c1, rl1 = new_commit(r_c0)
        r_c2, rl2 = new_commit(r_c1)
        r_c3, rl3 = new_commit(r_c2)
        remote_branch = VGroup(r_c0, rl1, r_c1, rl2, r_c2, rl3, r_c3)
        VGroup(rl3, r_c3).set_color(GREEN)
        r_c3.set_fill(opacity=0)
        remote_branch.shift(UP * 1.2)

        remote_label = Text("main", font_size=24, color=GREEN).next_to(
            r_c3, RIGHT, buff=0.3
        )
        remote_tag = Text("Remote", font_size=20, color=GREY_B).next_to(
            remote_branch, LEFT, buff=0.5
        )

        # Local: main (divergent — 내 커밋 포함)
        l_c0 = get_commit()
        l_c1, ll1 = new_commit(l_c0)
        l_c2, ll2 = new_commit(l_c1)
        l_c3, ll3 = new_commit(l_c2)
        local_branch = VGroup(l_c0, ll1, l_c1, ll2, l_c2, ll3, l_c3)
        VGroup(ll3, l_c3).set_color(YELLOW_B)
        l_c3.set_fill(opacity=0)
        local_branch.shift(DOWN * 0.5)

        main_label = Text("main", font_size=24, color=BLUE).next_to(
            l_c3, RIGHT, buff=0.3
        )
        local_tag = Text("Local", font_size=20, color=GREY_B).next_to(
            local_branch, LEFT, buff=0.5
        )

        # origin/main: fetch로 가져온 상태
        oc, ol = new_commit(l_c2, direction=UR, buff=0.5)
        oc.set_color(GREEN).set_fill(opacity=0)
        ol.set_color(GREEN)
        origin_branch = VGroup(oc, ol)
        origin_label = Text("origin/main", font_size=24, color=GREEN).next_to(
            oc, RIGHT, buff=0.3
        )

        branch_graph = VGroup(
            remote_branch,
            remote_label,
            remote_tag,
            local_branch,
            main_label,
            local_tag,
            origin_branch,
            origin_label,
        )
        branch_graph.move_to(UP * 0.3)

        # git pull = fetch + merge (하단)
        git_pull = Words("git pull", font="Noto Sans KR", font_size=36, color=BLUE)
        eq = Text("=", font_size=36)
        fetch_merge = Words("fetch + merge", font="Noto Sans KR", font_size=36)
        fetch_merge.words[0].set_color(GREEN)
        fetch_merge.words[1].set_color(GREY_C)
        fetch_merge.words[2].set_color(PURPLE)
        pull_eq = VGroup(git_pull, eq, fetch_merge).arrange(RIGHT, buff=0.3)
        pull_eq.to_edge(DOWN, buff=1.0)

        # 분리된 명령어
        git_fetch = CodeText("git fetch", font_size=30).set_color(GREEN)
        git_merge_cmd = CodeText("git merge", font_size=30).set_color(PURPLE)
        or_text = Text("or", font_size=24, color=GREY_C)
        git_rebase_cmd = CodeText("git rebase", font_size=30).set_color(YELLOW)

        # --- End Entity Definitions ---

        # divergent branch때는
        self.playw(
            FadeIn(
                title,
                remote_branch,
                remote_label,
                remote_tag,
                local_branch,
                main_label,
                local_tag,
            )
        )

        # fetch와 합치기를 같이하는 pull을 안 하고
        self.play(FadeIn(pull_eq))
        cross = Cross(git_pull, stroke_color=RED, stroke_width=4)
        self.playw(Create(cross))
        self.play(FadeOut(pull_eq, cross), run_time=0.6)

        # 안전하게 fetch와 합치기를 따로따로 해서
        git_fetch.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(git_fetch), run_time=0.6)
        self.playw(
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
        )

        # merge할지 rebase할지
        choice = VGroup(git_merge_cmd, or_text, git_rebase_cmd).arrange(RIGHT, buff=0.5)
        choice.to_edge(DOWN, buff=1.0)
        self.playwl(FadeOut(git_fetch), FadeIn(choice), lag_ratio=0.3)

        # 직접 판단하겠다
        self.playw(
            Indicate(git_merge_cmd, color=PURPLE),
            Indicate(git_rebase_cmd, color=YELLOW),
        )


class set_ffonly(Scene2D):
    def construct(self):
        # --- Entity Definitions ---

        # Remote: main
        r_c0 = get_commit()
        r_c1, rl1 = new_commit(r_c0)
        r_c2, rl2 = new_commit(r_c1)
        r_c3, rl3 = new_commit(r_c2)
        remote_branch = VGroup(r_c0, rl1, r_c1, rl2, r_c2, rl3, r_c3)
        VGroup(rl3, r_c3).set_color(GREEN)
        r_c3.set_fill(opacity=0)
        remote_branch.shift(UP * 1.2)

        remote_label = Text("main", font_size=24, color=GREEN).next_to(
            r_c3, RIGHT, buff=0.3
        )
        remote_tag = Text("Remote", font_size=20, color=GREY_B).next_to(
            remote_branch, LEFT, buff=0.5
        )

        # Local: main (ff 상태로 시작 — 커밋 3개)
        l_c0 = get_commit()
        l_c1, ll1 = new_commit(l_c0)
        l_c2, ll2 = new_commit(l_c1)
        local_branch = VGroup(l_c0, ll1, l_c1, ll2, l_c2)
        local_branch.shift(DOWN * 0.5)

        main_label = Text("main", font_size=24, color=BLUE).next_to(
            l_c2, RIGHT, buff=0.3
        )
        local_tag = Text("Local", font_size=20, color=GREY_B).next_to(
            local_branch, LEFT, buff=0.5
        )

        # origin/main: fetch 결과
        oc, ol = new_commit(l_c2, direction=UR, buff=0.5)
        oc.set_color(GREEN).set_fill(opacity=0)
        ol.set_color(GREEN)
        origin_branch = VGroup(oc, ol)
        origin_label = Text("origin/main", font_size=24, color=GREEN).next_to(
            oc, RIGHT, buff=0.3
        )

        branch_graph = VGroup(
            remote_branch,
            remote_label,
            remote_tag,
            local_branch,
            main_label,
            local_tag,
            origin_branch,
            origin_label,
        )
        branch_graph.move_to(UP * 0.3)

        # 명령어 텍스트
        git_fetch = CodeText("git fetch", font_size=30).set_color(GREEN)
        git_merge_cmd = CodeText("git merge", font_size=30).set_color(PURPLE)
        or_text = Text("or", font_size=24, color=GREY_C)
        git_rebase_cmd = CodeText("git rebase", font_size=30).set_color(YELLOW)
        choice = VGroup(git_merge_cmd, or_text, git_rebase_cmd).arrange(RIGHT, buff=0.5)
        choice.to_edge(DOWN, buff=2.0)

        # --- End Entity Definitions ---

        # fast-forward가 되는 상황에서는
        self.play(
            FadeIn(
                remote_branch,
                remote_label,
                remote_tag,
                local_branch,
                main_label,
                local_tag,
            )
        )

        # 고민할 필요없이 pull이 되는데요
        l_c3_ff, ll3_ff = new_commit(l_c2)
        l_c3_ff.set_color(GREEN).set_fill(opacity=0)
        ll3_ff.set_color(GREEN)
        self.playwl(
            main_label.animate.next_to(l_c3_ff, RIGHT, buff=0.3),
            AnimationGroup(
                Transformr(r_c3.copy(), l_c3_ff), Transformr(rl3.copy(), ll3_ff)
            ),
            lag_ratio=0.2,
        )

        # 갈라진 상황에서는
        l_c3, ll3 = new_commit(l_c2)
        VGroup(l_c3, ll3).set_color(RED_B)
        l_c3.set_fill(opacity=0)
        self.play(
            Transformr(l_c3_ff, l_c3),
            Transformr(ll3_ff, ll3),
            Flash(l_c3.get_corner(UL), line_length=0.15, num_lines=15, color=RED),
        )

        # merge 혹은 rebase
        self.play(FadeIn(choice))

        # 상황에 따라 필요한 명령이 다릅니다
        self.play(Indicate(git_merge_cmd, color=PURPLE))
        self.playw(
            Indicate(git_rebase_cmd, color=YELLOW),
        )

        # 그래서 divergent때는
        self.play(
            FadeOut(choice),
            Flash(l_c3.get_corner(UL), line_length=0.15, num_lines=15, color=PURE_RED),
            Flash(r_c3.get_corner(UL), line_length=0.15, num_lines=15, color=PURE_RED),
        )

        # 긴장을 해야된다고 생각하고요
        overlay = self.overlay
        VGroup(l_c3, ll3, r_c3, rl3).set_z_index(overlay.z_index + 1)
        self.playw(FadeIn(overlay))

        # 이 때 git fetch를 따로 한 다음에요
        git_fetch.to_edge(DOWN, buff=2.0).set_z_index(overlay.z_index + 1)
        self.play(FadeIn(git_fetch))
        self.play(
            Transformr(r_c3.copy(), oc),
            Transformr(rl3.copy(), ol),
            FadeIn(origin_label),
            FadeOut(overlay),
        )

        # 상황을 보고
        self.play(FadeOut(git_fetch), run_time=0.6)

        # merge를 해야할 것 같으면 merge
        self.playw(FadeIn(git_merge_cmd))

        # rebase를 해야할 것 같으면 rebase
        self.playw(FadeIn(or_text, git_rebase_cmd))

        # 이렇게 직접 선택해서 작업합니다
        self.play(Indicate(git_merge_cmd, color=PURPLE))
        self.playw(
            Indicate(git_rebase_cmd, color=YELLOW),
        )
