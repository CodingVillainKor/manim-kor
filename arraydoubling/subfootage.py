from manim import *
from random import randint

class NumText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
    
    @property
    def num(self):
        return float(self.text)
    
_box_buf = 0.4
class Proportional(MovingCameraScene):
    def construct(self):
        append_num = 41
        group = self.play_full_memory(12)
        self.play_append(append_num)
        self.play(self.camera.frame.animate.move_to(group.get_center()).set(width=group.width*2.5).shift(DOWN))
        self.play_realloc_new_memory(group, append_num)

    def play_full_memory(self, num_box):
        num_list = [randint(1, 99) for _ in range(num_box)]
        box_group = self.list_to_box_group(num_list)
        self.playw(FadeIn(box_group))
        return box_group

    def play_append(self, num):
        text = Text(f"data.append({num})", font="Consolas").shift(UP).shift(UP)
        self.play(FadeIn(text, scale=0.5), run_time=0.7)
        self.playw(FadeOut(text, scale=3), run_time=0.7)
    
    def play_realloc_new_memory(self, full_group, append_num):
        new_group = full_group.copy().shift(DOWN).shift(DOWN).shift(RIGHT).shift(DOWN).shift(DOWN).shift(RIGHT)
        new_rect = new_group[0]
        new_rect[0].stretch_about_point(9/8, 0, new_rect.get_left())
        self.play(FadeIn(new_rect))

        for i in range(len(full_group[1])):
            full_group[1][i].generate_target()
            full_group[1][i].target.move_to(new_group[1][i])

        for i in range(len(full_group[1])):
            self.play(MoveToTarget(full_group[1][i]), run_time=0.5)
        
        t = NumText(f"{append_num:02}", font="Consolas")
        s = Square(side_length=1, color=YELLOW_B).surround(t)
        new_append = VGroup(t, s).next_to(full_group[1][i], RIGHT*2)
        self.wait()
        self.play(FadeIn(new_append, scale=3))

    def list_to_box_group(self, num_list):
        box_list = []
        for i in range(len(num_list)):
            t = NumText(f"{num_list[i]:02}", font="Consolas")
            s = Square(side_length=1, color=YELLOW_B).surround(t)
            item = VGroup(t, s)
            if i > 0:
                item = item.next_to(box_list[i-1], RIGHT*2)
            box_list.append(item)
        box_group = Group(*box_list)
        rect = Rectangle(color=PURE_RED,
                         width=box_group.width+_box_buf,
                         height=box_group.height+_box_buf
                         ).move_to(box_group)
        total_group = Group(rect, box_group).move_to(ORIGIN)
        self.play(self.camera.frame.animate.move_to(total_group.get_center()).set(width=total_group.width*1.5))
        return total_group
    
    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])


class SameInterval(MovingCameraScene):
    def construct(self):
        append_num = 41
        group = self.play_full_memory(10)
        self.play_append(append_num)
        self.play(self.camera.frame.animate.move_to(group.get_center()).set(width=group.width*3.).shift(DOWN))
        return_group = self.play_realloc_new_memory(group, append_num)
        self.play(self.camera.frame.animate.move_to(return_group.get_center()).set(width=return_group.width*2.2).shift(DOWN))
        return_group = self.play_realloc_new_memory(return_group, 99, scale=3/2)

    def play_full_memory(self, num_box):
        num_list = [randint(1, 99) for _ in range(num_box)]
        box_group = self.list_to_box_group(num_list)
        self.playw(FadeIn(box_group))
        return box_group

    def play_append(self, num):
        text = Text(f"data.append({num})", font="Consolas").shift(UP).shift(UP)
        self.play(FadeIn(text, scale=0.5), run_time=0.7)
        self.playw(FadeOut(text, scale=3), run_time=0.7)
    
    def play_realloc_new_memory(self, full_group, append_num, scale=2):
        new_group = full_group.copy().shift(DOWN).shift(DOWN).shift(DOWN).shift(DOWN)
        new_rect = new_group[0]
        new_rect[0].stretch_about_point(scale, 0, new_rect.get_left())
        self.playw(FadeIn(new_rect))

        return_box = []
        for i in range(len(full_group[1])):
            full_group[1][i].generate_target()
            full_group[1][i].target.move_to(new_group[1][i])

        for i in range(len(full_group[1])):
            self.play(MoveToTarget(full_group[1][i]), run_time=0.5)
            return_box.append(full_group[1][i])
        
        t = NumText(f"{append_num:02}", font="Consolas")
        s = Square(side_length=1, color=YELLOW_B).surround(t)
        new_append = VGroup(t, s).next_to(full_group[1][i], RIGHT*2)
        self.wait()
        self.play(FadeIn(new_append, scale=3))
        return_box.append(new_append)

        return_group = VGroup(new_rect, VGroup(*return_box))
        return return_group

    def list_to_box_group(self, num_list):
        box_list = []
        for i in range(len(num_list)):
            t = NumText(f"{num_list[i]:02}", font="Consolas")
            s = Square(side_length=1, color=YELLOW_B).surround(t)
            item = VGroup(t, s)
            if i > 0:
                item = item.next_to(box_list[i-1], RIGHT*2)
            box_list.append(item)
        box_group = Group(*box_list)
        rect = Rectangle(color=PURE_RED,
                         width=box_group.width+_box_buf,
                         height=box_group.height+_box_buf
                         ).move_to(box_group)
        total_group = Group(rect, box_group).move_to(ORIGIN)
        self.play(self.camera.frame.animate.move_to(total_group.get_center()).set(width=total_group.width*1.5))
        return total_group
    
    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class ProportionalOnlyMemory(MovingCameraScene):
    def construct(self):
        init_width=10
        rect1 = Rectangle(color=RED,
                          width=init_width,
                          height=0.7)
        self.play(self.camera.frame.animate.move_to(rect1.get_center()).set(width=rect1.width*2.).shift(DOWN))
        self.playw(FadeIn(rect1))
        rect2 = rect1.copy().stretch_about_point(2, 0, rect1.get_left()).shift(DOWN).shift(DOWN)
        self.play(self.camera.frame.animate.move_to(rect2.get_center()).set(width=rect2.width*1.5).shift(DOWN))
        self.playw(FadeIn(rect2))
        rect3 = rect2.copy().stretch_about_point(2, 0, rect2.get_left()).shift(DOWN).shift(DOWN)
        self.play(self.camera.frame.animate.move_to(rect3.get_center()).set(width=rect3.width*1.2).shift(DOWN))
        self.playw(FadeIn(rect3))
    
    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

class SameIntervalOnlyMemory(MovingCameraScene):
    def construct(self):
        init_width=10
        rect1 = Rectangle(color=RED,
                          width=init_width,
                          height=0.7)
        self.play(self.camera.frame.animate.move_to(rect1.get_center()).set(width=rect1.width*2.).shift(DOWN))
        self.playw(FadeIn(rect1))
        rect2 = rect1.copy().stretch_about_point(2, 0, rect1.get_left()).shift(DOWN).shift(DOWN)
        self.play(self.camera.frame.animate.move_to(rect2.get_center()).set(width=rect2.width*1.5).shift(DOWN))
        self.playw(FadeIn(rect2))
        rect3 = rect2.copy().stretch_about_point(3/2, 0, rect2.get_left()).shift(DOWN).shift(DOWN)
        self.play(self.camera.frame.animate.move_to(rect3.get_center()).set(width=rect3.width*1.2).shift(DOWN))
        self.playw(FadeIn(rect3))
    
    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])