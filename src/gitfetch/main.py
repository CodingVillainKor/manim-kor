from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class intro(Scene3D):
    def construct(self):
        # --- Entity Definitions ---
        tilt_degree = 50
        rot = lambda m: m.rotate(angle=tilt_degree * DEGREES, axis=RIGHT)

        # === Remote Repository ===
        remote_box = RoundedRectangle(
            width=3.5, height=2, corner_radius=0.15, color=BLUE_C, stroke_width=2
        ).shift(LEFT * 4.5 + UP * 2.5)
        remote_label = (
            Words("Remote", font="Noto Sans KR")
            .scale(0.5)
            .next_to(remote_box, UP, buff=0.2)
            .align_to(remote_box, LEFT)
            .set_color(BLUE_C)
        )

        # Remote main branch (4 commits, ahead of local)
        remote_main = branch(n_commits=4)
        remote_main.scale(0.5).move_to(remote_box.get_center())
        remote_main_label = (
            Text("main", font=MONO_FONT)
            .scale(0.4)
            .next_to(remote_main, UP, buff=0.25)
            .set_color(BLUE_C)
        )

        # === Local Repository ===
        local_box = RoundedRectangle(
            width=4.5, height=4, corner_radius=0.15, color=GREEN_C, stroke_width=2
        ).shift(DOWN)
        local_label = (
            Words("Local", font="Noto Sans KR")
            .scale(0.55)
            .next_to(local_box, UP, buff=0.2)
            .align_to(local_box, LEFT)
            .set_color(GREEN_C)
        )

        # Local main branch (2 commits, behind remote)
        local_main = branch(n_commits=2)
        local_main.scale(0.5).move_to(local_box.get_center()).shift(UP)
        local_main_label = (
            Text("main", font=MONO_FONT)
            .scale(0.4)
            .next_to(local_main, UP, buff=0.25)
            .set_color(GREEN_C)
        )

        # .git hidden area (심오한 어딘가)
        git_area = (
            DashedVMobject(
                RoundedRectangle(
                    width=3.8, height=1.4, corner_radius=0.2, stroke_width=2
                ),
                num_dashes=40,
            )
            .move_to(local_box.get_center() + DOWN * 0.9)
            .set_color(YELLOW_B)
        )
        git_area_label = (
            Folder(".git/refs/remotes/")
            .scale(0.7)
            .next_to(git_area, UP, buff=0.1)
            .align_to(git_area, LEFT)
            .set_color(YELLOW_B)
        )

        # === Git Commands ===
        fetch_cmd = Words("git fetch origin main", font=MONO_FONT).scale(0.5)
        merge_cmd = rot(Words("git merge origin/main", font=MONO_FONT).scale(0.4))
        rebase_cmd = rot(Words("git rebase origin/main", font=MONO_FONT).scale(0.4))

        # --- Animation Sequence ---

        # ========== Section 1: git fetch 소개 (lines 1-6) ==========

        # "git fetch는요 쉽게 말해서 remote에서 다운로드만 해서요"
        fetch_cmd.move_to(ORIGIN)
        self.playwlfin(*fetch_cmd.words, lag_ratio=0.3)
        self.wait(0.5)

        download_label = (
            Words("다운로드만", font="Noto Sans KR").scale(0.6).set_color(YELLOW_B)
        )

        # "그래서 현재 코드 상태에는 변화가 없는 명령입니다"
        no_change = (
            Words("코드 변화 없음", font="Noto Sans KR").scale(0.55).set_color(GREEN)
        )
        VGroup(download_label, no_change).arrange(RIGHT, buff=0.5).next_to(
            fetch_cmd, DOWN, buff=0.4
        )
        self.playw(FadeIn(download_label, shift=DOWN * 0.3))
        self.play(FadeIn(no_change, shift=DOWN * 0.3))
        self.playw(RWiggle(no_change))
        self.wait(0.5)

        # "그러면 이게 무슨 의미일까요? 한번 볼게요"
        self.play(FadeOut(download_label), FadeOut(no_change), FadeOut(fetch_cmd))
        self.tilt_camera_vertical(tilt_degree)
        self.playw(FadeIn(local_box, local_label, local_main, local_main_label))
        # ========== Section 2: fetch 동작 시각화 (lines 7-17) ==========
        fetch_cmd = (
            rot(fetch_cmd).scale(0.8).move_to(ORIGIN).shift(DOWN * 1.5 + RIGHT * 4.5)
        )
        # "방금 말한대로 git fetch를 하면 remote에서 다운로드를 합니다"
        self.playwlfin(*fetch_cmd.words, lag_ratio=0.1, wait=0)

        self.play(
            FadeIn(remote_box),
            FadeIn(remote_label),
            FadeIn(remote_main),
            FadeIn(remote_main_label),
        )
        rml_origin = (
            Text("origin/main", font=MONO_FONT)
            .scale(0.4)
            .move_to(remote_main_label)
            .align_to(remote_main_label, RIGHT)
            .set_color(BLUE_C)
        )
        rml_origin[:-4].set_opacity(0)
        rb = VGroup(remote_main.copy(), rml_origin)
        rb.generate_target()
        rb.target.move_to(git_area.get_center())
        rb.target[1].set_opacity(1)

        self.playw(FadeIn(git_area), MoveToTarget(rb))

        # "그런데 다운로드한 위치가요 git 관리 폴더 속 심오한 어딘가입니다"
        self.playw(FadeIn(git_area_label))

        # "이 심오한 위치, 그리고 여기서 어떻게 가져오는지를 몰라서요"
        # "git fetch를 처음 써보면 좀 당황스럽습니다"
        self.play(git_area_label.animate.rotate(tilt_degree * DEGREES, axis=RIGHT))
        self.play(RWiggle(git_area_label, amp=(0.1, 0.1, 0.1)), run_time=3)
        self.playw(git_area_label.animate.rotate(-tilt_degree * DEGREES, axis=RIGHT))

        # "이 부분이 fetch의 핵심이자 제일 헷갈리는 부분입니다"
        ol = self.overlay
        VGroup(git_area, git_area_label, rb).set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))

        # ========== Section 3: origin/main 위치 설명 (lines 18-24) ==========

        # "그러면 fetch로 가져온 코드는 어디에 있는 걸까요?"
        # "바로 <remote 별명>/<branch 이름>입니다"
        naming = rot(
            Text("<remote>/<branch>", font=MONO_FONT)
            .scale(0.5)
            .next_to(rb[1], LEFT, buff=1.5)
            .set_z_index(ol.z_index + 2)
        )
        anim1 = Transformr(rb[1][:6].copy(), naming[:8])
        anim2 = Transformr(rb[1][6].copy(), naming[8])
        anim3 = Transformr(rb[1][7:].copy(), naming[9:])
        self.playwl(anim1, anim2, anim3, lag_ratio=0.5)

        # "예를 들어서 git fetch origin main을 했다고 하면은요"
        fetch_cmd2 = fetch_cmd.copy().set_z_index(ol.z_index + 1)
        self.play(FadeIn(fetch_cmd2))
        self.remove(fetch_cmd)
        fetch_cmd = fetch_cmd2
        self.wait()

        # "가져온 코드는 내 로컬 디렉토리의 origin/main 브랜치에 있습니다"
        origin_main = rb[0]
        origin_main_label = rml_origin
        self.playw(ReplacementTransform(naming, origin_main_label))

        # ========== Section 4: main ≠ origin/main (lines 25-34) ==========

        # "여기서 헷갈리는 게 있는데요"
        # "내 로컬의 main 브랜치랑 이 origin/main은 다릅니다"
        lmsc = VGroup(local_main, local_main_label).copy().set_z_index(ol.z_index + 1)
        self.play(FadeIn(lmsc))
        self.remove(VGroup(local_main, local_main_label).shift(RIGHT * 20))
        self.wait()

        # "origin/main은요 remote에 있던 main 브랜치를"
        # "내 컴퓨터에 받아둔 공간이라고 생각하면 됩니다"
        local_origin_ref = VGroup(rb, git_area, git_area_label)
        local_origin_ref.save_state()
        self.playw(local_origin_ref.animate.rotate(tilt_degree * DEGREES, axis=RIGHT))

        # "그래서 fetch를 해도 내 로컬 main 브랜치는 그대로인 겁니다"
        self.play(
            Restore(local_origin_ref),
            lmsc.animate.rotate(tilt_degree * DEGREES, axis=RIGHT),
            run_time=0.6,
        )
        self.playw(RWiggle(lmsc, amp=(0.1, 0.1, 0.1)), run_time=2)

        # ========== Section 5: merge / rebase (lines 35-40) ==========

        # "그래서 이걸 내 코드에 반영하려면은요 merge나 rebase를 써서"
        self.play(FadeOut(fetch_cmd))

        merge_cmd.next_to(fetch_cmd, UP, buff=1.5).set_z_index(ol.z_index + 1)
        rebase_cmd.next_to(merge_cmd, DOWN, buff=0.4).set_z_index(ol.z_index + 1)
        self.play(FadeIn(merge_cmd))
        self.playw(FadeIn(rebase_cmd))

        # "git merge origin/main 혹은 git rebase origin/main 을 하면 됩니다"
        new_local_main = (
            rot(branch(n_commits=4))
            .scale(0.5)
            .move_to(lmsc[0])
            .set_z_index(ol.z_index + 1)
        )
        self.playw(
            Transform(lmsc[0], new_local_main[: len(lmsc[0])]),
            Transformr(rb[0][len(lmsc[0]) :].copy(), new_local_main[len(lmsc[0]) :]),
        )

        # --- End Animation Sequence ---


class otherBranch(Scene3D):
    def construct(self):
        # --- Entity Definitions ---
        tilt_degree = 50
        rot = lambda m: m.rotate(angle=tilt_degree * DEGREES, axis=RIGHT)

        # === Remote Repository ===
        remote_box = RoundedRectangle(
            width=3.5, height=2.5, corner_radius=0.15, color=BLUE_C, stroke_width=2
        ).shift(LEFT * 4.5 + UP * 2.5)
        remote_label = (
            Words("Remote", font="Noto Sans KR")
            .scale(0.5)
            .next_to(remote_box, UP, buff=0.2)
            .align_to(remote_box, LEFT)
            .set_color(BLUE_C)
        )

        # Remote main branch (2 commits)
        remote_main = branch(n_commits=2)
        remote_main.scale(0.5).move_to(remote_box.get_center()).shift(UP * 0.4)
        remote_main_label = (
            Text("main", font=MONO_FONT)
            .scale(0.35)
            .next_to(remote_main, UP, buff=0.2)
            .set_color(BLUE_C)
        )

        # Remote feature branch (3 commits, made by teammate)
        remote_feature = branch(n_commits=3)
        remote_feature.scale(0.5).move_to(remote_box.get_center()).shift(DOWN * 0.6)
        remote_feature_label = (
            Text("feature", font=MONO_FONT)
            .scale(0.35)
            .next_to(remote_feature, UP, buff=0.2)
            .set_color(ORANGE)
        )

        # === Local Repository ===
        local_box = RoundedRectangle(
            width=4.5, height=5.5, corner_radius=0.15, color=GREEN_C, stroke_width=2
        ).shift(DOWN * 1.0)
        local_label = (
            Words("Local", font="Noto Sans KR")
            .scale(0.55)
            .next_to(local_box, UP, buff=0.2)
            .align_to(local_box, LEFT)
            .set_color(GREEN_C)
        )

        # Local main branch (2 commits, no feature branch yet)
        local_main = branch(n_commits=2)
        local_main.scale(0.5).move_to(local_box.get_center()).shift(UP * 1.9)
        local_main_label = (
            Text("main", font=MONO_FONT)
            .scale(0.35)
            .next_to(local_main, UP, buff=0.2)
            .set_color(GREEN_C)
        )

        # .git hidden area
        git_area = (
            DashedVMobject(
                RoundedRectangle(
                    width=3.8, height=2.4, corner_radius=0.2, stroke_width=2
                ),
                num_dashes=40,
            )
            .move_to(local_box.get_center() + DOWN * 1.2)
            .set_color(YELLOW_B)
        )
        git_area_label = (
            Folder(".git/refs/remotes/")
            .scale(0.7)
            .next_to(git_area, UP, buff=0.1)
            .align_to(git_area, LEFT)
            .set_color(YELLOW_B)
        )

        # === Local feature branch (created by checkout) ===
        local_feature = branch(n_commits=3)
        local_feature.scale(0.5)
        local_feature_label = (
            Text("feature", font=MONO_FONT).scale(0.35).set_color(GREEN_C)
        )

        # === Git Commands ===
        fetch_cmd = Words("git fetch origin feature", font=MONO_FONT).scale(0.5)
        checkout_cmd = Words("git checkout feature", font=MONO_FONT).scale(0.5)

        # === FETCH_HEAD ===
        fetch_head_box = (
            DashedVMobject(
                RoundedRectangle(
                    width=3.0, height=0.7, corner_radius=0.15, stroke_width=2
                ),
                num_dashes=30,
            )
            .move_to(local_box.get_center() + DOWN * 1.6)
            .set_color(PURPLE)
        )
        fetch_head_label = (
            Text("FETCH_HEAD", font=MONO_FONT)
            .scale(0.35)
            .set_color(PURPLE)
            .next_to(fetch_head_box, UP, buff=0.1)
            .align_to(fetch_head_box, LEFT)
        )

        # --- End Entity Definitions ---

        # --- Animation Sequence ---

        # ========== Section 1: 다른 브랜치 fetch 소개 (lines 2-8) ==========
        self.tilt_camera_vertical(tilt_degree)

        # "그런데 만약에 main 브랜치가 아니라요 다른 브랜치를 fetch하면 어떨까요?"
        self.playw(
            FadeIn(remote_box),
            FadeIn(remote_label),
            FadeIn(remote_main),
            FadeIn(remote_main_label),
        )
        self.playw(
            FadeIn(remote_feature),
            FadeIn(remote_feature_label),
        )

        # "예를 들어서 다른 팀원이 feature라는 브랜치를 만들었는데요"
        # "내 local엔 이 브랜치가 없습니다"
        rf = VGroup(remote_feature, remote_feature_label)
        self.playw(rf.animate.rotate(tilt_degree * DEGREES, axis=RIGHT))
        self.playw(
            FadeIn(local_box),
            FadeIn(local_label),
            FadeIn(local_main),
            FadeIn(local_main_label),
        )

        no_feature = rot(
            Words("feature 없음", font="Noto Sans KR").scale(0.45).set_color(RED_C)
        ).next_to(local_main, DOWN, buff=0.6)
        self.playw(FadeIn(no_feature, shift=DOWN * 0.3))

        # "이 때 git fetch origin feature를 하면은요"
        fetch_cmd = (
            rot(fetch_cmd).scale(0.8).move_to(ORIGIN).shift(DOWN * 1.5 + RIGHT * 4.5)
        )
        self.play(FadeOut(no_feature))
        self.playwlfin(*fetch_cmd.words, lag_ratio=0.3, wait=0)

        # "이번에도 origin/feature에 다운로드합니다"
        rfl_origin = (
            Text("origin/feature", font=MONO_FONT)
            .scale(0.35)
            .move_to(remote_feature_label)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .align_to(remote_feature_label, RIGHT)
            .set_color(ORANGE)
        )
        rfl_origin[:-7].set_opacity(0)
        rb = VGroup(remote_feature.copy(), rfl_origin)
        rb.generate_target()
        rb.target.rotate(-tilt_degree * DEGREES, axis=RIGHT)
        rb.target.move_to(git_area.get_center()).shift(UP * 0.6)
        rb.target[1].set_opacity(1)
        rb.target[1].shift(DOWN * 0.15)

        self.playw(FadeIn(git_area), FadeIn(git_area_label), MoveToTarget(rb))

        # ========== Section 2: feature branch 오해 (lines 9-13) ==========

        # "이 때 누군가는 feature branch를 바로 만들 거라 생각할 수도 있지만요"
        wrong_feature = branch(n_commits=3).scale(0.5)
        wrong_feature_label = (
            Text("feature", font=MONO_FONT).scale(0.35).set_color(GREEN_C)
        )
        wrong_feature.move_to(local_box.get_center()).shift(UP * 0.7)
        wrong_feature_label.next_to(wrong_feature, UP, buff=0.2)
        question_mark = rot(
            Text("?", font=MONO_FONT).scale(0.6).set_color(YELLOW_B)
        ).next_to(wrong_feature, RIGHT, buff=0.3)

        # self.play(FadeIn(wrong_feature, shift=UP * 0.3), FadeIn(wrong_feature_label))
        self.play(
            Transformr(remote_feature.copy(), wrong_feature),
            Transformr(remote_feature_label.copy(), wrong_feature_label),
        )
        self.playw(FadeIn(question_mark, shift=RIGHT * 0.3))

        # "실제로는 그렇지 않습니다"
        cross = rot(Cross(wrong_feature, stroke_width=4).set_color(PURE_RED))
        self.play(Create(cross))
        self.playw(FadeOut(question_mark, wrong_feature, wrong_feature_label, cross))

        # "아까 말한대로 origin/feature만 생기구요 내 로컬에는 feature 브랜치가 아직 없습니다"
        self.play(rb.animate.rotate(tilt_degree * DEGREES, axis=RIGHT))
        self.playw(RWiggle(rb, amp=(0.1, 0.1, 0.1)), run_time=3)

        # ========== Section 3: git checkout feature (lines 14-20) ==========

        # "이 때 로컬에 origin/feature로 feature 브랜치를 만들려면은요"
        # "git checkout feature를 하면 됩니다"
        self.play(FadeOut(fetch_cmd))
        checkout_cmd = (
            rot(checkout_cmd).scale(0.8).move_to(ORIGIN).shift(DOWN * 1.5 + RIGHT * 4.5)
        )
        self.playwlfin(*checkout_cmd.words, lag_ratio=0.3)

        # "이 git checkout이 실행될 때요 origin/feature가 이미 있으니까"
        self.play(Flash(checkout_cmd.get_corner(UL), color=YELLOW_B))
        self.playw(Indicate(rb[1], color=ORANGE))

        # "이걸 보고 그 브랜치의 상태로 로컬 브랜치를 만들어줍니다"
        local_feature.move_to(local_box.get_center()).shift(UP * 1.0)
        local_feature_label.next_to(local_feature, UP, buff=0.2)
        rot(local_feature)
        rot(local_feature_label)

        self.playwl(
            Transformr(rb[0].copy(), local_feature),
            FadeIn(local_feature_label),
            lag_ratio=0.7,
        )

        # ========== Section 4: FETCH_HEAD (lines 22-34) ==========

        # "그리고 하나 더 알아둘 게 있는데요 FETCH_HEAD라는 것도 있습니다"
        self.playw(FadeOut(checkout_cmd, rb))
        self.playw(FadeIn(fetch_head_box), FadeIn(fetch_head_label))

        # "이건 또 뭘까요? 예를 들어서 git fetch origin feature를 하면은요"
        fetch_cmd2 = (
            rot(Words("git fetch origin feature", font=MONO_FONT).scale(0.5))
            .scale(0.8)
            .move_to(ORIGIN)
            .shift(DOWN * 1.5 + RIGHT * 4.5)
        )
        self.playwlfin(*fetch_cmd2.words, lag_ratio=0.1, wait=0)

        # "아까 말한 origin/feature에 저장되면서"
        rfl_origin = (
            Text("origin/feature", font=MONO_FONT)
            .scale(0.35)
            .move_to(remote_feature_label)
            # .shift(DOWN*0.3)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .align_to(remote_feature_label, RIGHT)
            .set_color(ORANGE)
        )
        rfl_origin[:-7].set_opacity(0)
        rb2 = VGroup(remote_feature.copy(), rfl_origin)
        rb2.generate_target()
        rb2.target.rotate(-tilt_degree * DEGREES, axis=RIGHT)
        rb2.target.move_to(git_area.get_center()).shift(UP * 0.7)
        rb2.target[1].set_opacity(1)
        # rb2.target[1].shift(DOWN*0.15)
        rb2.target[0].shift(UP * 0.15)
        self.playw(MoveToTarget(rb2))

        # "동시에 FETCH_HEAD라는 곳에도 기록이 됩니다"
        rfl_origin2 = (
            Text("origin/feature", font=MONO_FONT)
            .scale(0.35)
            .move_to(remote_feature_label)
            # .shift(DOWN*0.3)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .align_to(remote_feature_label, RIGHT)
            .set_color(ORANGE)
        )
        rfl_origin2[:-7].set_opacity(0)
        rb3 = VGroup(remote_feature.copy(), rfl_origin2)
        rb3.generate_target()
        rb3.target.rotate(-tilt_degree * DEGREES, axis=RIGHT)
        rb3.target.move_to(fetch_head_box.get_center())
        rb3.target[1].set_opacity(1)
        rb3.target[1].shift(DOWN * 0.05)
        rb3.target[0].shift(UP * 0.15)
        self.playw(MoveToTarget(rb3))

        # "이 FETCH_HEAD는요 가장 최근에 fetch한 결과가 뭔지를 가리키는"
        # "git의 임시 저장소같은 개념입니다"
        ol = self.overlay
        VGroup(fetch_head_box, fetch_head_label, rb3).set_z_index(ol.z_index + 1)
        self.play(FadeIn(ol))
        self.playw(
            RWiggle(VGroup(fetch_head_box, fetch_head_label, rb3), amp=(0.1, 0.1, 0.1)),
            run_time=3,
        )

        # "그래서 나중에 방금 fetch한 걸 확인하거나 merge할 때"
        # "이 FETCH_HEAD를 쓸 수도 있습니다"
        merge_example = (
            rot(Words("git merge FETCH_HEAD", font=MONO_FONT).scale(0.4))
            .move_to(ORIGIN)
            .shift(DOWN * 1.5 + RIGHT * 4.5)
            .set_z_index(ol.z_index + 1)
        )
        merge_example.words[-1].set_color(PURPLE)
        self.play(FadeOut(fetch_cmd2), FadeIn(merge_example))

        # --- End Animation Sequence ---


class summary(Scene3D):
    def construct(self):
        # --- Entity Definitions ---
        tilt_degree = 50
        rot = lambda m: m.rotate(angle=tilt_degree * DEGREES, axis=RIGHT)

        # === Remote Repository (reuse intro/otherBranch layout) ===
        remote_box = RoundedRectangle(
            width=3.5, height=2.5, corner_radius=0.15, color=BLUE_C, stroke_width=2
        ).shift(LEFT * 4.5 + UP * 2.5)
        remote_label = (
            Words("Remote", font="Noto Sans KR")
            .scale(0.5)
            .next_to(remote_box, UP, buff=0.2)
            .align_to(remote_box, LEFT)
            .set_color(BLUE_C)
        )

        # Remote main branch (3 commits)
        remote_main = branch(n_commits=3)
        remote_main.scale(0.5).move_to(remote_box.get_center()).shift(UP * 0.4)
        remote_main_label = (
            Text("main", font=MONO_FONT)
            .scale(0.35)
            .next_to(remote_main, UP, buff=0.2)
            .set_color(BLUE_C)
        )

        # Remote feature branch (2 commits)
        remote_feature = branch(n_commits=2)
        remote_feature.scale(0.5).move_to(remote_box.get_center()).shift(DOWN * 0.6)
        remote_feature_label = (
            Text("feature", font=MONO_FONT)
            .scale(0.35)
            .next_to(remote_feature, UP, buff=0.2)
            .set_color(BLUE_C)
        )

        # === Local Repository ===
        local_box = RoundedRectangle(
            width=4.5, height=5.5, corner_radius=0.15, color=GREEN_C, stroke_width=2
        ).shift(DOWN * 1.0)
        local_label = (
            Words("Local", font="Noto Sans KR")
            .scale(0.55)
            .next_to(local_box, UP, buff=0.2)
            .align_to(local_box, LEFT)
            .set_color(GREEN_C)
        )

        # Local main branch (2 commits, behind remote)
        local_main = branch(n_commits=2)
        local_main.scale(0.5).move_to(local_box.get_center()).shift(UP * 1.9)
        local_main_label = (
            Text("main", font=MONO_FONT)
            .scale(0.35)
            .next_to(local_main, UP, buff=0.2)
            .set_color(GREEN_C)
        )

        # .git hidden area (임시 저장소)
        git_area = (
            DashedVMobject(
                RoundedRectangle(
                    width=3.8, height=2.4, corner_radius=0.2, stroke_width=2
                ),
                num_dashes=40,
            )
            .move_to(local_box.get_center() + DOWN * 1.2)
            .set_color(YELLOW_B)
        )
        git_area_label = (
            Folder(".git/refs/remotes/")
            .scale(0.7)
            .next_to(git_area, UP, buff=0.1)
            .align_to(git_area, LEFT)
            .set_color(YELLOW_B)
        )

        # === Case A: 이미 있는 브랜치 — merge ===
        merge_cmd = rot(Words("git merge origin/main", font=MONO_FONT).scale(0.4))

        # === Case B: 없던 브랜치 — checkout ===
        checkout_cmd = rot(Words("git checkout feature", font=MONO_FONT).scale(0.4))
        local_feature = branch(n_commits=2)
        local_feature.scale(0.5)
        local_feature_label = (
            Text("feature", font=MONO_FONT).scale(0.35).set_color(GREEN_C)
        )

        # === Git Pull formula ===
        pull_cmd = (
            Words("git pull origin main", font=MONO_FONT).scale(0.6).set_color(YELLOW_B)
        )
        fetch_part = Words("git fetch", font=MONO_FONT).scale(0.5)
        plus_sign = Words("+", font=MONO_FONT).scale(0.6)
        merge_part = Words("git merge", font=MONO_FONT).scale(0.5)
        rebase_part = Words("git rebase", font=MONO_FONT).scale(0.5)
        or_text = Words("/", font=MONO_FONT).scale(0.5)
        pull_formula = VGroup(
            fetch_part, plus_sign, merge_part, or_text, rebase_part
        ).arrange(RIGHT, buff=0.3)

        # --- End Entity Definitions ---

        # --- Animation Sequence ---
        self.tilt_camera_vertical(tilt_degree)

        # ========== Section 1: fetch 정리 — 임시 저장소 (lines 1-3) ==========

        # "정리하면 fetch는 local 작업에 가져오는 게 아니라요"
        # "임시 저장소에 가져오는 역할입니다"
        self.addw(
            remote_box,
            remote_label,
            remote_main,
            remote_main_label,
            local_box,
            local_label,
            local_main,
            local_main_label,
        )
        fetch_cmd = rot(
            Words("git fetch origin main", font=MONO_FONT).scale(0.4)
        ).next_to(local_box, RIGHT, buff=0.5)
        fetch_cmd_ = fetch_cmd.copy()
        self.playwlfin(*fetch_cmd.words, lag_ratio=0.3)
        self.play(FadeIn(git_area), FadeIn(git_area_label))

        # fetch 동작: remote → git_area (임시 저장소)
        rml_origin = (
            Text("origin/main", font=MONO_FONT)
            .scale(0.35)
            .move_to(remote_main_label)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .align_to(remote_main_label, RIGHT)
            .set_color(BLUE_C)
        )
        rml_origin[:-4].set_opacity(0)
        rb = VGroup(remote_main.copy(), rml_origin)
        rb.generate_target()
        rb.target.move_to(git_area.get_center()).shift(UP * 0.5)
        rb.target[1].set_opacity(1)
        self.playw(MoveToTarget(rb))

        # ========== Section 2: Case A — 이미 있는 브랜치 → merge (lines 4-6) ==========

        # "만약 임시 저장소에 가져온 브랜치가 내 로컬에도 이미 있는 브랜치면요"
        self.playw(Indicate(rb[1][-4:], color=BLUE_C))
        self.play(
            Indicate(local_main_label, color=GREEN_C),
            Flash(local_main_label.get_corner(UL), color=GREEN_C),
        )

        # "git merge로 합치는 식으로 많이들 작업합니다"
        merge_cmd.next_to(local_main, RIGHT, buff=2)
        self.playw(FadeIn(merge_cmd, shift=RIGHT * 0.3))

        new_local_main = rot(branch(n_commits=3)).scale(0.5).move_to(local_main)
        self.playw(
            Transform(local_main, new_local_main[: len(local_main)]),
            Transformr(
                rb[0][len(local_main) :].copy(), new_local_main[len(local_main) :]
            ),
        )
        self.wait(0.5)

        # ========== Section 3: git pull = fetch + merge (lines 7-8) ==========

        # "이렇게 git fetch와 합치는 작업을 동시에 해주는 게"
        # "git pull 명령이구요"
        ol = self.overlay
        merge_cmd.set_z_index(ol.z_index + 1)
        fetch_cmd.set_z_index(ol.z_index + 1)
        rot(pull_cmd).set_z_index(ol.z_index + 1).next_to(
            merge_cmd, UP, buff=1.5
        ).align_to(merge_cmd, LEFT)
        pull_formula.set_z_index(ol.z_index + 1).next_to(pull_cmd, DOWN, buff=0.5)
        self.play(FadeIn(ol))
        self.playw(FadeIn(pull_cmd, shift=UP * 0.3))

        # ========== Section 4: Case B — 없던 브랜치 → checkout (lines 9-12) ==========

        # "그런데 만약에 내 로컬에는 없던 브랜치를 fetch로 가져오면"
        self.playw(FadeOut(ol, pull_cmd, merge_cmd), FadeIn(remote_feature, remote_feature_label))
        fetch_cmd2 = (
            rot(Words("git fetch origin feature", font=MONO_FONT).scale(0.4))
            .move_to(fetch_cmd).align_to(fetch_cmd, LEFT)
        )
        self.playw(Transformr(fetch_cmd.words, fetch_cmd2.words))

        rfl_origin = (
            Text("origin/feature", font=MONO_FONT)
            .scale(0.35)
            .move_to(remote_feature_label)
            .rotate(tilt_degree * DEGREES, axis=RIGHT)
            .align_to(remote_feature_label, RIGHT)
            .set_color(BLUE_C)
        )
        rfl_origin[:-7].set_opacity(0)
        rb_feat = VGroup(remote_feature.copy(), rfl_origin)
        rb_feat.generate_target()
        rb_feat.target.move_to(git_area.get_center()).shift(DOWN * 0.5)
        rb_feat.target[1].set_opacity(1)
        self.playw(MoveToTarget(rb_feat))

        # "이 때는 git checkout 브랜치 이름을 하면"
        checkout_cmd.next_to(fetch_cmd, DOWN, buff=0.5).align_to(fetch_cmd, LEFT)
        self.playw(FadeIn(checkout_cmd, shift=RIGHT * 0.3), fetch_cmd2.animate.set_opacity(0.3))

        # "가져온 브랜치 상태로 로컬 브랜치가 만들어집니다"
        local_feature.move_to(local_box.get_center()).shift(UP * 0.8)
        local_feature_label.next_to(local_feature, UP, buff=0.2)
        rot(local_feature)
        rot(local_feature_label)

        self.playwl(
            Transformr(rb_feat[0].copy(), local_feature),
            FadeIn(local_feature_label),
            lag_ratio=0.7,
        )
        self.playw(FadeOut(checkout_cmd))

        # ========== Section 5: git pull 공식 정리 (lines 14-20) ==========

        # "그런데 로컬에 이미 있는 브랜치인 경우에요"
        # "fetch하고 합치는 이 두 단계,"
        # "이 두 단계가 아까 git pull이라고 했죠?"
        fetch_cmd_.set_z_index(ol.z_index + 1)
        self.playw(FadeOut(fetch_cmd2.words), FadeIn(fetch_cmd_.words), FadeIn(ol), FadeIn(merge_cmd))
        self.playw(FadeIn(pull_cmd, shift=UP * 0.3), wait=1.5)

        # "그래서 git pull은"
        # "git fetch + git merge 혹은 git rebase라고 생각하시면 됩니다"
        self.clear()
        self.wait(2)
        pull_cmd2 = Words("git pull", font=MONO_FONT).scale(0.8).set_color(YELLOW_B)
        equals_sign = Words("=", font=MONO_FONT).scale(0.7)

        fetch_part2 = Words("git fetch", font=MONO_FONT).scale(0.55).set_color(BLUE_C)
        plus_sign2 = Words("+", font=MONO_FONT).scale(0.6)
        merge_part2 = Words("git merge", font=MONO_FONT).scale(0.55).set_color(GREEN_C)
        or_text2 = Words("( or ", font=MONO_FONT, color=GREY_C).scale(0.55)
        rebase_part2 = (
            Words("git rebase", font=MONO_FONT).scale(0.55).set_color(GREEN_C)
        )

        final_formula = (
            VGroup(
                pull_cmd2,
                equals_sign,
                fetch_part2,
                plus_sign2,
                merge_part2,
                or_text2,
                rebase_part2,
            )
            .arrange(RIGHT, buff=0.3)
            .move_to(ORIGIN)
        )
        or_text2.add(Words(" )", font=MONO_FONT, color=GREY_C).scale(0.55).next_to(rebase_part2, RIGHT, buff=0.1))
        self.tilt_camera_vertical(0)

        self.play(FadeIn(pull_cmd2))
        self.play(FadeIn(equals_sign))
        self.playwl(
            FadeIn(fetch_part2),
            FadeIn(plus_sign2),
            FadeIn(merge_part2),
            lag_ratio=0.4,
            wait=0.6
        )
        self.playwl(
            FadeIn(or_text2),
            FadeIn(rebase_part2),
            lag_ratio=0.4,
        )
        

        # --- End Animation Sequence ---
