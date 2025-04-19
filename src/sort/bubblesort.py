from manim import *

def get_num_box(num):
    n = Text(f"{num:02}", font="Consolas")
    b = Square(side_length=1, color=YELLOW_B).surround(n)
    g = VGroup(n, b)

    return g


class StartSort(ZoomedScene):
    def construct(self):
        nums = [33, 11, 44, 22]
        buf = 5
        
        boxes = [get_num_box(num) for num in nums]
        for i, b in enumerate(boxes):
            if i:
                b = b.next_to(boxes[i-1], RIGHT*buf)
        total_group = VGroup(*boxes).move_to(ORIGIN)

        self.play(self.camera.frame.animate.move_to(total_group).set(width=total_group.width*4))
        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15, run_time=2))
        self.wait()
        self.play(total_group.animate.shift(UP*4))
        self.wait()

        # internal sort 1 - 3 - 0 - 2
        order = [1, 3, 0, 2]
        for i, idx in enumerate(order):
            boxes[idx].generate_target()
            if i:
                boxes[idx].target.next_to(boxes[order[i-1]].target, RIGHT*buf)

        target_group = VGroup(*[b.target for b in boxes]).move_to(ORIGIN)
        
        # first move
        box = boxes[order[0]]
        self.play(MoveToTarget(box), run_time=1)
        self.wait()
        box = boxes[order[1]]
        self.play(MoveToTarget(box), run_time=1)
        self.wait()
        box = boxes[order[2]]
        self.play(MoveToTarget(box), run_time=1)
        self.wait()
        box = boxes[order[3]]
        self.play(MoveToTarget(box), run_time=1)
        self.wait()


        