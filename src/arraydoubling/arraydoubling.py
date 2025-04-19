from manim import *
from random import randint
import math
_box_buf = 0.4
class NumText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
    
    @property
    def num(self):
        return float(self.text)

def NumBox(text, text_config={}, box_config={}):
    text = NumText(text, **text_config)
    rect = Square(**box_config).surround(text)
    return VGroup(text, rect)

class ArrayDoubling(MovingCameraScene):
    def construct(self):
        self.num_numbers = 45
        self.init_size = 10
        self.doubling_ratio = 2

        self.nums_list = [i for i in range(self.num_numbers)]
        box_group_now, rect_now = self.init_and_fill()
        num_realloc = int(math.log(self.num_numbers/self.init_size) / math.log(self.doubling_ratio)) + 1
        for i in range(num_realloc):
            box_group_now, rect_new = self.appear_and_move_to_new_memory(box_group_now, rect_now, i)
            box_group_now = self.reappend(box_group_now, i)
            self.playw(FadeOut(rect_now))
            rect_now = rect_new


    def init_and_fill(self):
        box_list = []
        for i in range(self.init_size):
            nb = NumBox(f"{self.nums_list[i]:02}", text_config={"font": "Consolas"}, box_config={"color": YELLOW_B})
            if i: nb.next_to(box_list[i-1], RIGHT*2)
            box_list.append(nb)
        box_group = VGroup(*box_list)
        
        rect = Rectangle(color=PURE_GREEN,
                         width=box_group.width+_box_buf,
                         height=box_group.height+_box_buf
        ).move_to(box_group)
        self.play(self.camera.frame.animate.move_to(box_group.get_center()).set(width=box_group.width*1.5), run_time=0.1)

        self.playw(FadeIn(rect))
        self.playw(LaggedStart(*[FadeIn(item) for item in box_group], lag_ratio=0.3))
        return box_group, rect

    def appear_and_move_to_new_memory(self, box_group_now, rect_now, idx):
        memory_now = self.init_size * self.doubling_ratio ** idx
        memory_new = self.init_size * self.doubling_ratio ** (idx+1)
        box_target_list = []
        for i in range(len(box_group_now)):
            box_group_now[i].generate_target()
            box_group_now[i].target.shift(DOWN).shift(DOWN)
            box_target_list.append(box_group_now[i].target)

        
        rect_new = rect_now.copy().move_to(VGroup(*box_target_list))
        rect_new = rect_new.stretch_about_point(memory_new/memory_now, 0, rect_new.get_left())
        self.play(self.camera.frame.animate.move_to(rect_new.get_center()).set(width=rect_new.width+4))
        self.playw(FadeIn(rect_new))

        self.playw(LaggedStart(*[MoveToTarget(box_group_now[i]) for i in range(len(box_group_now))], lag_ratio=0.3))

        return box_group_now, rect_new

    def reappend(self, box_group_now, idx):
        start_idx = self.init_size * self.doubling_ratio ** idx
        end_idx = min(self.init_size * self.doubling_ratio ** (idx+1), len(self.nums_list))
        newly_append_nums = self.nums_list[start_idx:end_idx]
        for i in range(len(newly_append_nums)):
            nb = NumBox(f"{newly_append_nums[i]:02}", text_config={"font": "Consolas"}, box_config={"color": YELLOW_B})
            nb.next_to(box_group_now[-1], RIGHT*2)
            box_group_now.add(nb)
        
        self.playw(LaggedStart(*[FadeIn(box_group_now[i], scale=2) for i in range(start_idx, end_idx)], lag_ratio=0.3))
        return box_group_now

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class ArrayEqualSpace(MovingCameraScene):
    def construct(self):
        self.num_numbers = 45
        self.init_size = 10
        self.space_delta = 10

        self.nums_list = [i for i in range(self.num_numbers)]
        box_group_now, rect_now = self.init_and_fill()
        num_realloc = (self.num_numbers-1 - self.init_size) // self.space_delta + 1
        for i in range(num_realloc):
            box_group_now, rect_new = self.appear_and_move_to_new_memory(box_group_now, rect_now, i)
            box_group_now = self.reappend(box_group_now, i)
            self.playw(FadeOut(rect_now))
            rect_now = rect_new


    def init_and_fill(self):
        box_list = []
        for i in range(self.init_size):
            nb = NumBox(f"{self.nums_list[i]:02}", text_config={"font": "Consolas"}, box_config={"color": YELLOW_B})
            if i: nb.next_to(box_list[i-1], RIGHT*2)
            box_list.append(nb)
        box_group = VGroup(*box_list)
        
        rect = Rectangle(color=PURE_GREEN,
                         width=box_group.width+_box_buf,
                         height=box_group.height+_box_buf
        ).move_to(box_group)
        self.play(self.camera.frame.animate.move_to(box_group.get_center()).set(width=box_group.width*1.5), run_time=0.1)

        self.playw(FadeIn(rect))
        self.playw(LaggedStart(*[FadeIn(item) for item in box_group], lag_ratio=0.3))
        return box_group, rect

    def appear_and_move_to_new_memory(self, box_group_now, rect_now, idx):
        memory_now = self.init_size + idx * self.space_delta
        memory_new = self.init_size + (idx+1) * self.space_delta
        box_target_list = []
        for i in range(len(box_group_now)):
            box_group_now[i].generate_target()
            box_group_now[i].target.shift(DOWN).shift(DOWN)
            box_target_list.append(box_group_now[i].target)

        
        rect_new = rect_now.copy().move_to(VGroup(*box_target_list))
        rect_new = rect_new.stretch_about_point(memory_new/memory_now, 0, rect_new.get_left())
        self.play(self.camera.frame.animate.move_to(rect_new.get_center()).set(width=rect_new.width+4))
        self.playw(FadeIn(rect_new))

        self.playw(LaggedStart(*[MoveToTarget(box_group_now[i]) for i in range(len(box_group_now))], lag_ratio=0.3))

        return box_group_now, rect_new

    def reappend(self, box_group_now, idx):
        start_idx = self.init_size + idx * self.space_delta
        end_idx = min(self.init_size + (idx+1) * self.space_delta, len(self.nums_list))
        newly_append_nums = self.nums_list[start_idx:end_idx]
        for i in range(len(newly_append_nums)):
            nb = NumBox(f"{newly_append_nums[i]:02}", text_config={"font": "Consolas"}, box_config={"color": YELLOW_B})
            nb.next_to(box_group_now[-1], RIGHT*2)
            box_group_now.add(nb)
        
        self.playw(LaggedStart(*[FadeIn(box_group_now[i], scale=2) for i in range(start_idx, end_idx)], lag_ratio=0.3))
        return box_group_now

        

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])