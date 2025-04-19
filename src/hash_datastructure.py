from manimdef import DefaultManimClass, SRect
from manim import *

_dist_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

class HashTableVisualizer(DefaultManimClass):
    def construct(self):
        table_size = 11
        hash_list = [None] * table_size
        self.use_chain = True
        if self.use_chain: self.chain = [1] * table_size
        dict_keys = ["다은쓰", "원남쓰", "나연쓰", "김김김", "이이이"]
        hash_function_dict = {
            "len()": len,
            "%11": lambda x: int(x)%11
        }
        hash_table = self.build_hash_table(table_size)
        self.playw(hash_table.animate.scale(0.7))
        keys_items = self.prepare_dict_keys(dict_keys)
        self.playw(keys_items.animate.scale(0.7).align_to(hash_table, LEFT).shift(LEFT).shift(LEFT))
        keys_process = keys_items.copy()
        functions = self.prepare_hash_function(hash_function_dict)
        for i, key in enumerate(keys_process):
            key, key_idx = self.process_hash_function(key, functions)
            is_collision = hash_list[key_idx] is not None
            hash_list[key_idx] = keys_items[i]
            self.goto_hash_table(keys_items[i], key_idx, hash_table)
            self.playw(FadeOut(key))
            if not self.use_chain and is_collision:
                self.fatal_error_hash(key_idx, hash_table)

    def build_hash_table(self, table_size):
        hash_table = VGroup(*[Square(side_length=1.0, color=random_color()) for i in range(table_size)]).arrange(RIGHT)
        hash_indices = VGroup(*[Text(f"[{i}]", font="Consolas", font_size=20).move_to(hash_table[i]) for i in range(table_size)])
        self.playw(Write(hash_table))
        self.playw(Write(hash_indices))
        prepare_ = [hash_indices[i].animate.next_to(hash_table[i], UP if self.use_chain else DOWN) for i in range(table_size)]
        self.playw(LaggedStart(*prepare_, lag_ratio=0.2))
        total_table = VGroup(hash_table, hash_indices)
        self.playw(total_table.animate.shift(UP).shift(UP).shift(UP))
        return total_table

    def prepare_dict_keys(self, dict_keys):
        texts = VGroup(*[Text(f"{t}", font_size=28) for t in dict_keys]).arrange(DOWN, buff=_dist_buf*2)
        key_rects = VGroup(*[SRect(color=random_bright_color()).surround(texts[i]) for i in range(len(dict_keys))])
        items = VGroup(*[VGroup(texts[i], key_rects[i]) for i in range(len(dict_keys))])
        for item in items:
            self.play(Write(item))
        self.wait(2)
        return items

    def prepare_hash_function(self, function_dict):
        f_names = VGroup(*[Text(f"{k}", font="Consolas", font_size=24) for k in function_dict]).arrange(RIGHT, buff=_dist_buf*6)
        f_rects = VGroup(*[SRect(color=random_bright_color()).surround(f_names[i]).set_fill(BLACK, opacity=1.0) for i in range(len(function_dict))])
        
        items = VGroup(*[VGroup(f_rects[i], f_names[i]) for i in range(len(f_names))])
        for item in items:
            self.play(Write(item))
        self.wait(2)
        name_func = [{"name": f_names[i], "mobject": items[i], "func":function_dict[f_names[i].text]} for i in range(len(f_names))]
        return name_func

    def process_hash_function(self, key, functions):
        functions_group = VGroup(*[f["mobject"] for f in functions])
        self.bring_to_front(functions[0]["mobject"])
        self.playw(key.animate.next_to(functions[0]["mobject"], LEFT, buff=_dist_buf*2))
        for i in range(1, len(functions)+1):
            func = functions[i-1]["func"]
            if i == len(functions):
                midpoint = functions_group[i-1].get_right() + RIGHT
            else:
                midpoint = (functions_group[i-1].get_right() + functions_group[i].get_left()) / 2
            key_new = VGroup(t:=Text(f"{func(key[0].text)}", font_size=24), SRect(color=GREEN).surround(t)).move_to(midpoint)
            self.playw(ReplacementTransform(key, key_new))
            key = key_new
        key_idx = key[0].text
        return key, int(key_idx)

    def goto_hash_table(self, key, key_idx, hash_table):
        reduce_scale = hash_table[0][0].width / key.width
        if self.use_chain:
            self.playw(key.animate.next_to(hash_table[0][key_idx], DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*1.5*self.chain[key_idx]).scale(reduce_scale),
                FadeOut(key[1]))
        else:
            self.playw(key.animate.move_to(hash_table[0][key_idx]).scale(reduce_scale),
                    FadeOut(key[1], target_position=hash_table[0][key_idx]))
        self.chain[key_idx] += 1


    def fatal_error_hash(self, key_idx, hash_table):
        self.playw(hash_table[0][key_idx].animate.set_fill(PURE_RED, 1.0))


class ListIndex(DefaultManimClass):
    def construct(self):
        arr = [9, 8, 7]
        arr_0 = Text("arr[0]", color=GREEN, font="Consolas", font_size=24)
        arr_txt = VGroup(*[Text(f"{i}", font="Consolas", font_size=24) for i in arr]).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*5).shift(UP).shift(UP).shift(RIGHT).shift(RIGHT).shift(RIGHT)
        boxes = VGroup(*[SRect(stroke_width=1).surround(arr_txt[0], buf_width=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*5).align_to(arr_txt[i], RIGHT).shift(RIGHT*0.1) for i in range(len(arr))])
        self.playw(FadeIn(arr_0, arr_txt, boxes))
        arrow_0 = Arrow(arr_0[4], boxes[0].get_bottom(), stroke_width=2, color=GOLD)
        self.playw(GrowArrow(arrow_0))

        arr_1 = Text("arr[1]", color=PURE_GREEN, font="Consolas", font_size=24)
        arrow_1 = Arrow(arr_1[4], boxes[1].get_bottom(), stroke_width=2, color=GOLD)
        self.playw(FadeOut(arr_0[4]), FadeIn(arr_1[4], scale=5), Transform(arrow_0, arrow_1))

class DictIndex(DefaultManimClass):
    def construct(self):
        arr = [13, 30]
        arr_0 = Text("name_age[\"다은쓰\"]", color=GREEN, font_size=24)
        arr_txt = VGroup(*[Text(f"{i}", font="Consolas", font_size=24) for i in arr]).arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*5).shift(UP).shift(UP).shift(RIGHT).shift(RIGHT).shift(RIGHT)
        boxes = VGroup(*[SRect(stroke_width=1).surround(arr_txt[0], buf_width=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*5).align_to(arr_txt[i], RIGHT).shift(RIGHT*0.1) for i in range(len(arr))])
        self.playw(FadeIn(arr_0, arr_txt, boxes))
        arrow_0 = Arrow(arr_0[-5], boxes[0].get_bottom(), stroke_width=2, color=GOLD)
        self.playw(GrowArrow(arrow_0))

        arr_1 = Text("name_age[\"원남쓰\"]", color=PURE_GREEN, font_size=24)
        arrow_1 = Arrow(arr_1[-5], boxes[1].get_bottom(), stroke_width=2, color=GOLD)
        self.playw(FadeOut(arr_0[-5:-2]), FadeIn(arr_1[-5:-2], scale=4), Transform(arrow_0, arrow_1))