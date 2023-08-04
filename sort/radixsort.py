from manim import *
from random import sample

class RadixSort(MovingCameraScene):
    def construct(self):
        # Phase 1. numbers
        v = locals()
        num_number = 30
        nums = sample(range(200), num_number)
        for i in range(num_number):
            v[f"int{i}"]=nums[i]
            v[f"num{i}"] = Text(f"{v[f'int{i}']:02}", font="Consolas")
            v[f"circle{i}"] = Square(side_length=1, color=YELLOW_B).surround(v[f"num{i}"])
            v[f"group{i}"] = VGroup(v[f"num{i}"], v[f"circle{i}"])
            if nums[i] >= 100: v[f"group{i}"] = v[f"group{i}"].scale(2/3)
            if i > 0:
                v[f"group{i}"] = v[f"group{i}"].next_to(v[f"group{i-1}"], RIGHT*1)
        total_num_group = VGroup(*[v[f"group{i}"] for i in range(num_number)]).move_to(ORIGIN)
        # Playing Phase 1.
        self.play(self.camera.frame.animate.move_to(total_num_group).set(width=total_num_group.width*1.1))
        self.play(LaggedStart(*[FadeIn(v[f"group{i}"]) for i in range(num_number)], lag_ratio=0.15, run_time=2))
        self.wait(0.1)
        self.play(total_num_group.animate.shift(UP*max(5, num_number/7)))
        
        # Phase 2. ten index boxes 
        num_digits = 10
        for i in range(num_digits):
            v[f"u{i}"] = VMobject().set_points_as_corners([UL+UP*3, DL, DR, UR+UP*3])
            if i > 0:
                v[f"u{i}"] = v[f"u{i}"].next_to(v[f"u{i-1}"], RIGHT*1)
            v[f"idx{i}"] = Text(f"{i}", font="Consolas").next_to(v[f"u{i}"], DOWN)
        total_u_group = VGroup(*([v[f"u{i}"] for i in range(num_digits)] + [v[f"idx{i}"] for i in range(num_digits)])).move_to(ORIGIN+DOWN*3)

        # Phase 3. First-digit sort
        buf = [2]*10
        box_list = [list() for _ in range(num_digits)]
        num_list = [list() for _ in range(num_digits)]
        for i in range(num_number):
            idx = str(v[f"int{i}"])[-1]
            v[f"group{i}"].generate_target()
            v[f"group{i}"].target.next_to(v[f"u{idx}"], 0)
            v[f"group{i}"].target.shift(DOWN*buf[int(idx)])
            buf[int(idx)] -= 1
            box_list[int(idx)].append(v[f"group{i}"])
            num_list[int(idx)].append(v[f"int{i}"])
        
        # Playing Phase 2 and 3.
        self.play(FadeIn(total_u_group)) # Phase 2
        self.play(LaggedStart(*[MoveToTarget(v[f"group{i}"]) for i in range(num_number)], lag_ratio=0.15, run_time=5))
        self.wait(0.3)
        self.play(FadeOut(total_u_group))
        self.play(total_num_group.animate.shift(UP*max(7, num_number/4)))

        # Phase 4. ten index boxes
        for i in range(num_digits):
            v[f"usec{i}"] = VMobject().set_points_as_corners([UL+UP*3, DL, DR, UR+UP*3])
            if i > 0:
                v[f"usec{i}"] = v[f"usec{i}"].next_to(v[f"usec{i-1}"], RIGHT*1)
            v[f"idxsec{i}"] = Text(f"{i*10:02}", font="Consolas").next_to(v[f"usec{i}"], DOWN)
        total_uu_group = VGroup(*([v[f"usec{i}"] for i in range(num_digits)] + [v[f"idxsec{i}"] for i in range(num_digits)])).move_to(ORIGIN+DOWN*3)

        # Phase 5. Second-digit sort
        buf = [2]*10
        box_list2 = [list() for _ in range(num_digits)]
        num_list2 = [list() for _ in range(num_digits)]
        for i in range(num_digits):
            for j in range(len(box_list[i])):
                item = box_list[i][j]
                num = num_list[i][j]
                idx = f"{num:02}"[-2]
                item.generate_target()
                item.target.next_to(v[f"usec{idx}"], 0)
                item.target.shift(DOWN*buf[int(idx)])
                buf[int(idx)] -= 1
                box_list2[int(idx)].append(item)
                num_list2[int(idx)].append(num)
        
        # Playing Phase 4 and 5.
        self.play(FadeIn(total_uu_group)) # Phase 4
        for i in range(num_digits):
            self.play(LaggedStart(*[MoveToTarget(item) for item in box_list[i]], lag_ratio=0.15, run_time=1 + 0.15*len(num_list[i])))
        self.play(FadeOut(total_uu_group))
        self.play(total_num_group.animate.shift(UP*8))


        # Phase Final. sort.
        idx = 0
        sorted_list = []
        target_list = []
        for box in box_list2:
            for item in box:
                item.generate_target()
                if idx > 0:
                    item.target.next_to(sorted_list[-1].target, RIGHT)
                sorted_list.append(item)
                target_list.append(item.target)
                idx+=1
        total_num_group = VGroup(*target_list).move_to(ORIGIN)
        
        self.play(LaggedStart(*[MoveToTarget(item) for item in sorted_list], lag_ratio=0.15, run_time=num_number/7))
        
            



        self.wait(1)