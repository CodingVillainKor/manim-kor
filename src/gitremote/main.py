from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)


class remoteABC(Scene2D):
    def construct(self):
        # Remote repo (GitHub) - 상단 중앙
        remote_box = RoundedRectangle(
            width=5, height=2, corner_radius=0.2, color=WHITE
        ).shift(UP * 2.5)
        remote_label = (
            Text("GitHub", font="Noto Serif KR", font_size=28)
            .next_to(remote_box, LEFT, buff=0.1)
            .align_to(remote_box, UP)
        )
        remote = VGroup(remote_box, remote_label)

        # Local repos - 하단에 3개 배치
        def create_local(name, position):
            box = RoundedRectangle(
                width=2.2, height=1.5, corner_radius=0.2, color=BLUE
            ).move_to(position)
            label = (
                Text(name, font="Noto Serif KR", font_size=24)
                .next_to(box, LEFT, buff=0.1)
                .align_to(box, UP)
            )
            local_label = (
                Text("Local Repo.", font_size=18).move_to(box).shift(DOWN * 0.3)
            )
            return VGroup(box, label, local_label)

        local_a = create_local("팀원 A", LEFT * 4 + DOWN * 1)
        local_b = create_local("팀원 B", DOWN * 1)
        local_c = create_local("팀원 C", RIGHT * 4 + DOWN * 1)

        # 연결선 (양방향 화살표)
        def create_connection(local_repo, remote_repo):
            start = local_repo[0].get_top()
            end = remote_repo[0].get_bottom()
            # 약간 오프셋 주어 양방향 화살표 표현
            line = Line(start, end, color=GRAY, stroke_width=2)
            return line

        conn_a = create_connection(local_a, remote)
        conn_b = create_connection(local_b, remote)
        conn_c = create_connection(local_c, remote)

        # 애니메이션 시작
        # 1. Remote repo 등장
        self.play(FadeIn(remote))
        self.playw(RWiggle(remote, amp=(0.07, 0.07, 0.07)))

        # 2. 팀원 A, B, C 등장
        self.playw(FadeIn(local_a[0]), FadeIn(local_b[0]), FadeIn(local_c[0]))
        self.playwl(
            FadeIn(local_a[1]), FadeIn(local_b[1]), FadeIn(local_c[1]), lag_ratio=0.15
        )
        self.playwl(
            FadeIn(local_a[2]), FadeIn(local_b[2]), FadeIn(local_c[2]), lag_ratio=0.15
        )

        # 3. 연결선 등장
        self.playw(Create(conn_a), Create(conn_b), Create(conn_c))

        self.wait(0.5)

        main_remote = (
            branch(n_commits=2, buff=0.5)
            .scale(0.75)
            .move_to(remote_box.get_center())
            .shift(LEFT * 1.2)
        )

        # local a
        branch_a = branch(n_commits=2, buff=0.5).scale(0.75).move_to(local_a[0])
        self.play(FadeIn(branch_a))
        self.playw(
            Transform(
                branch_a.copy(), main_remote, replace_mobject_with_target_in_scene=True
            )
        )

        # local b, c

        branch_b = branch(n_commits=2, buff=0.5).scale(0.75).move_to(local_b[0])
        branch_c = branch(n_commits=2, buff=0.5).scale(0.75).move_to(local_c[0])
        self.playwl(
            Transform(
                main_remote.copy(), branch_b, replace_mobject_with_target_in_scene=True
            ),
            Transform(
                main_remote.copy(), branch_c, replace_mobject_with_target_in_scene=True
            ),
            lag_ratio=0.15,
        )

        #

        ol = self.overlay
        VGroup(local_a, branch_a).set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))

        self.play(
            local_a[0].animate.stretch_to_fit_width(2.8).align_to(local_a[0], LEFT)
        )
        nc_a = (
            VGroup(*new_commit(branch_a[-1][0], direction=RIGHT, buff=0.5))
            .scale(0.75)
            .next_to(branch_a[-1], RIGHT, buff=0.0)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(nc_a))

        remotec = VGroup(remote, main_remote).copy().set_z_index(ol.z_index + 1)
        self.play(FadeIn(remotec))
        self.remove(remote, main_remote)
        self.wait()

        gitpush = (
            Words("git push", font_size=36, font=MONO_FONT, color=GREEN)
            .scale(0.75)
            .set_z_index(ol.z_index + 1)
            .next_to(local_a, DOWN, buff=0.1)
        )
        self.playwl(*[FadeIn(item) for item in gitpush.words], lag_ratio=0.1, wait=0.2)
        self.playw(RWiggle(gitpush), run_time=3)


class RemoteRepoIntro(Scene2D):
    """
    스크립트:
    - 지금까지 다룬 git은요
    - 내 컴퓨터 안에서 버전을 만들었었죠?
    - 이걸 local repository, local repo라고 합니다
    - local repo의 작업을 github이나 gitlab같은
    - remote repo에 올려서요
    - 프로젝트 협업에 사용합니다
    """

    def construct(self):
        # === 지금까지 다룬 git은요 ===
        my_computer = RoundedRectangle(
            width=6, height=3.5, corner_radius=0.3, color=BLUE
        )
        my_computer_label = Text(
            "내 컴퓨터", font="Noto Sans KR", font_size=28
        ).next_to(my_computer, UP, buff=0.2)

        self.playw(FadeIn(my_computer), FadeIn(my_computer_label))

        # === 내 컴퓨터 안에서 버전을 만들었었죠? ===
        local_commits = branch(n_commits=4, buff=0.6).move_to(my_computer.get_center())

        self.playwl(*[FadeIn(c) for c in local_commits], lag_ratio=0.2)

        # === 이걸 local repository, local repo라고 합니다 ===
        local_repo_label = Words(
            "Local Repository", font_size=24, color=YELLOW_B, font="Noto Sans KR"
        ).next_to(my_computer, DOWN, buff=0.3)

        self.playwl(*[FadeIn(word) for word in local_repo_label.words], lag_ratio=0.2)

        # === local repo의 작업을 github이나 gitlab같은 ===
        local_group = VGroup(my_computer, my_computer_label, local_commits, local_repo_label)

        # 카메라 시야 넓히면서 local을 왼쪽으로
        remote_box = RoundedRectangle(
            width=5, height=3, corner_radius=0.3, color=WHITE
        ).shift(RIGHT * 5)
        github_label = Text(
            "GitHub", font="Noto Sans KR", font_size=32
        ).next_to(remote_box, UP, buff=0.2)

        self.playw(
            self.cf.animate.scale(1.5),
            local_group.animate.shift(LEFT * 3),
        )
        self.playw(FadeIn(remote_box), FadeIn(github_label))

        # === remote repo에 올려서요 ===
        remote_repo_label = Words(
            "Remote Repository", font_size=24, color=GREEN, font="Noto Sans KR"
        ).next_to(remote_box, DOWN, buff=0.3)

        self.playwl(*[FadeIn(word) for word in remote_repo_label.words], lag_ratio=0.2)

        # push 화살표
        arrow = Arrow(
            my_computer.get_right(), remote_box.get_left(),
            color=YELLOW_B, buff=0.3, stroke_width=3
        ).shift(UP*0.3)
        branch_remote = branch(n_commits=4, buff=0.6).move_to(remote_box.get_center())
        self.playw(GrowArrow(arrow), Transform(local_commits.copy(), branch_remote, replace_mobject_with_target_in_scene=True))

class branches(Scene2D):
    def construct(self):
        self.cf.scale(1.2).shift(DOWN*0.3)
        # Local repo 영역
        local_box = RoundedRectangle(
            width=6, height=2.5, corner_radius=0.2, color=BLUE
        ).shift(DOWN * 1.5)
        local_label = Text(
            "Local Repo.", font="Noto Sans KR", font_size=24, color=YELLOW_B
        ).next_to(local_box, UP, buff=0.1).align_to(local_box, LEFT).shift(RIGHT * 0.2)

        # Remote repo 영역
        remote_box = RoundedRectangle(
            width=7, height=2.5, corner_radius=0.2, color=WHITE
        ).shift(UP * 2)
        remote_label = Text(
            "Remote Repo.", font="Noto Sans KR", font_size=24, color=GREEN
        ).next_to(remote_box, UP, buff=0.1).align_to(remote_box, LEFT).shift(RIGHT * 0.2)

        # Local branches
        lb1 = branch(n_commits=4, buff=0.5)
        lb1t = Text("main", font="Noto Sans KR").scale(0.4).next_to(lb1[-1], RIGHT, buff=0.1)
        lb2 = branch(start=lb1[-3][0], n_commits=3, buff=0.5)
        lb2t = Text("piui", font="Noto Sans KR", color=YELLOW_B).scale(0.4).next_to(lb2[-1], RIGHT, buff=0.1)
        local = VGroup(lb1, lb2).move_to(local_box.get_center())
        lb1t.next_to(lb1[-1], RIGHT, buff=0.1)
        lb2t.next_to(lb2[-1], RIGHT, buff=0.1)

        # Remote branches
        rb1 = branch(n_commits=4, buff=0.5)
        rb1t = Text("main", font="Noto Sans KR").scale(0.4)
        rb2 = branch(start=rb1[-2][0], n_commits=4, buff=0.5)
        rb2[1:].set_stroke(color=RED_B)
        rb2t = Text("feature/login", font="Noto Sans KR", color=RED_B).scale(0.4)
        remote = VGroup(rb1, rb2).move_to(remote_box.get_center())
        rb1t.next_to(rb1[-1], RIGHT, buff=0.1)
        rb2t.next_to(rb2[-1], UP, buff=0.1)

        self.playw(FadeIn(local_box), FadeIn(local_label), FadeIn(remote_box), FadeIn(remote_label))
        self.playw(FadeIn(local, lb1t))
        self.playw(FadeIn(rb1, rb1t))

        self.playw(FadeIn(lb2t))
        self.playw(RWiggle(VGroup(rb1, rb1t)))

        self.playw(FadeIn(rb2, rb2t))

        self.playw(RWiggle(VGroup(local, lb1t, lb2t)))