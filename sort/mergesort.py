from manim import *
from random import sample

class NumText(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
    
    @property
    def num(self):
        return float(self.text)

def merge(list1, list2, key=None):
    merged = []
    while list1 or list2: # until both are empty:
        if not list1: # list1 empty:
            merged.extend(list2)
            list2.clear()
        elif not list2: # list2 empty:
            merged.extend(list1)
            list1.clear()
        else: # both not empty:
            if key is not None:
                merged.append(list1.pop(0) if key(list1[0]) < key(list2[0]) else list2.pop(0))
            else:
                merged.append(list1.pop(0) if list1[0] < list2[0] else list2.pop(0))
    return merged


class MergeSort(MovingCameraScene):
    CONFIG = {
        "camera_config":{"background_color":"#000000"}
    }
    def construct(self):
        # Phase 1. numbers
        num_item = 6
        self.item_buf = 2
        nums = self.get_numbers(num_item, max_num=200)
        self.initialize_numbers(nums)
        self.sort_one_session(0)
        self.sort_one_session(1)
        self.sort_one_session(2)
        #self.sort_one_session(3)
        #self.sort_one_session(4)


    def initialize_numbers(self, nums, play=True): # Phase 1 - 숫자 선언 및 영상 표시
        self.items = []
        for i in range(len(nums)):
            t = NumText(f"{nums[i]:02}", font="Consolas") # 숫자
            s = Square(side_length=1, color=YELLOW_B).surround(t) # 숫자에 노란 박스
            item = VGroup(t, s) # 숫자-박스를 묶어서 하나의 item
            if nums[i] >= 100: item = item.scale(2/3)
            if i>0:
                item = item.next_to(self.items[i-1], RIGHT*self.item_buf) # item 오른쪽에 다음 item
            self.items.append(item)
        self.items_group = VGroup(*self.items).move_to(ORIGIN) # 모든 item을 묶어서 가운데 정렬
        self.play(self.camera.frame.animate.move_to(self.items_group).set(width=self.items_group.width*3)) # 카메라 시점을 아이템에 맞춤(개수에 따라 줌을 다르게)
        self.now_sorted = [[item] for item in self.items] # 정렬을 수행할 리스트, 시작은 len 1짜리 리스트로 구성된 리스트

        if play:
            self.play(LaggedStart(*[FadeIn(item) for item in self.items], lag_ratio=0.15, run_time=2)) # 아이템 나타남
            self.wait(0.1)

    def sort_one_session(self, level, play=True): # 한 번의 merge, level-0: first sort, level-1 : second sort, ...
        # 1) 정렬을 위한 box 준비
        box_size = 2**level # 리스트 길이
        boxes = [list() for _ in range(0, len(self.items), box_size)] # 정렬을 수행할 리스트의 리스트
        box_buf = 0.4 # Rectangle 크기를 위한 변수
        rects = [] # Rectangle들을 모을 리스트
        for i, idx in enumerate(range(0, len(self.items), box_size)): # idx: 각 박스의 시작 인덱스, i: boxes의 리스트 인덱스
            boxes[i].extend(self.items[idx:idx+box_size]) # box_size 단위로 묶어서 boxes 구성, ex. level 1, [1, 2, 3, 4] -> [[1, 2], [3, 4]]
            box_group = VGroup(*boxes[i]) # 각 박스의 그룹
        
            rect = Rectangle(color=BLUE_C, 
                            width=box_group.width+box_buf, 
                            height=box_group.height+box_buf
            ).move_to(box_group) # 영상 내 파란 Rectangle, 박스를 감싸는 사각형
            rects.append(rect)

        if play:
            self.play(FadeIn(*rects)) # 파란 사각형 렌더링
            self.play(self.camera.frame.animate.shift(DOWN*3)) # 카메라 시점을 내림 -> 모든 아이템들이 올라가는 효과
        

        # 2) 정렬 수행 준비, 정렬될 박스 렌더링, 다음 박스는 준비된 박스보다 두 배 큰 사이즈
        next_box_size = 2**(level+1) # 정렬된 결과를 모을 박스의 크기
        next_boxes = [list() for _ in range(0, len(self.items), next_box_size)] # 정렬된 결과를 모을 박스들을 담을 리스트
        next_rects = [] # 정렬된 결과를 표시할 Rectangle들의 리스트
        for i, idx in enumerate(range(0, len(self.items), next_box_size)): # idx: 각 박스의 시작 인덱스, i: boxes의 리스트 인덱스
            next_boxes[i].extend(self.items[idx:idx+next_box_size]) # box_size 단위로 묶어서 next_boxes 구성, ex. level 1, [1, 2, 3, 4] -> [[1, 2, 3, 4]]
            box_group = VGroup(*next_boxes[i])

            rect = Rectangle(color=RED_B,
                             width=box_group.width+box_buf,
                             height=box_group.height+box_buf
            ).move_to(box_group) # 정렬될 박스
            next_rects.append(rect)
        next_rects_group = VGroup(*next_rects).move_to(self.camera.frame)
        if play:
            self.play(FadeIn(next_rects_group)) # 정렬될 박스 렌더링

        # 3) 정렬 실행
        next_sorted = [list() for _ in range(0, len(self.now_sorted), 2)]
        for i, idx in enumerate(range(0, len(self.now_sorted), 2)):
            if idx == len(self.now_sorted)-1:
                next_sorted[i] = self.now_sorted[idx]
            else:
                next_sorted[i] = merge(self.now_sorted[idx], self.now_sorted[idx+1], key=lambda x: x[0].num)
        
        # 4) 정렬 렌더링
        next_sorted_unpack = [item for box in next_sorted for item in box]
        for i in range(len(next_sorted_unpack)):
            if i==0: # 첫 번째 아이템은 일단 카메라 중간 지점으로
                item_now = next_sorted_unpack[i]
                item_now.generate_target()
                item_now.target.move_to(self.camera.frame)
            else: # 두 번째 아이템부터는 직전 아이템 오른쪽에 배치 // 이렇게 하면 화면 상에서 최소값이 중간에 오니까 아래에 target_group에서 다시 타겟 그룹들 위치 재설정
                item_now, item_prev = next_sorted_unpack[i], next_sorted_unpack[i-1]
                item_now.generate_target()
                item_now.target.next_to(item_prev.target, RIGHT*self.item_buf)
        target_group = VGroup(*[item.target for item in next_sorted_unpack]).move_to(self.camera.frame) # 렌더링할 정렬 결과를 현재 카메라 위치로 가져옴
        if play:
            for i in range(0, len(next_sorted_unpack), next_box_size):
                self.play(LaggedStart(*[MoveToTarget(item) for item in next_sorted_unpack[i:i+next_box_size]], lag_ratio=0.9, run_time=2))
            self.wait(0.1)
            self.play(FadeOut(*rects))
            self.play(FadeOut(*next_rects_group))
        self.items = next_sorted_unpack # 정렬 세션 완료, 다음 정렬을 위해 정렬 결과를 self.items로
        self.now_sorted = next_sorted # 정렬 세션 완료, 다음 정렬을 위해 정렬 결과를 self.items로
        self.prev_rects_group = next_rects_group

    def get_numbers(self, num, max_num=100):
        return sample(range(max_num), num)
    
class MergeExample(ZoomedScene):
    def construct(self):
        # Phase 1. numbers
        self.item_buf = 10
        nums = [72, 11, 33, 47]
        self.initialize_numbers(nums)
        self.play(self.camera.frame.animate.shift(DOWN*3.5))
        self.wait()
        
        # First Round 
        self.play(self.items[0].animate.scale(2))
        self.play(self.items[0].animate.scale(0.5), self.items[1].animate.scale(2))
        self.wait(1)
        self.play(self.items[0].animate.scale(2), self.items[1].animate.scale(0.5))
        self.wait(1)
        #self.items[0].scale(0.5)
        first_sorted = [self.items[1], self.items[0], self.items[2], self.items[3]]
        self.sort_items_internal(first_sorted)
        self.play(MoveToTarget(first_sorted[0]))
        self.wait()
        self.play(MoveToTarget(first_sorted[1]))
        self.wait(1)

        self.play(self.items[2].animate.scale(2))
        self.play(self.items[2].animate.scale(0.5), self.items[3].animate.scale(2))
        self.wait(1)
        self.sort_items_internal(first_sorted)
        self.play(MoveToTarget(first_sorted[2]))
        self.wait()
        self.play(MoveToTarget(first_sorted[3]))
        self.wait()
        self.play(self.camera.frame.animate.shift(DOWN*3.5))
        self.wait()
        self.play(first_sorted[1].animate.scale(0.5), first_sorted[3].animate.scale(0.5))
        self.wait()
        self.items = first_sorted
        # Second round
        self.play(self.items[0].animate.scale(2))
        self.play(self.items[0].animate.scale(0.5), self.items[2].animate.scale(2))
        self.wait(1)
        self.play(self.items[2].animate.scale(6/5))
        self.play(self.items[2].animate.scale(5/6))
        self.wait(1)
        second_sorted = [self.items[0], self.items[2], self.items[3], self.items[1]]
        self.sort_items_internal(second_sorted)
        self.play(MoveToTarget(second_sorted[0]))
        self.wait()
        self.play(self.items[2].animate.scale(0.5))
        self.wait()
        self.play(self.items[1].animate.scale(2))
        self.play(self.items[1].animate.scale(0.5), self.items[2].animate.scale(2))
        self.wait()
        self.play(self.items[1].animate.scale(2), self.items[2].animate.scale(0.5))
        self.wait(0.5)
        self.sort_items_internal(second_sorted)
        self.play(MoveToTarget(second_sorted[1]))
        self.wait()
        self.play(self.items[1].animate.scale(0.5))
        self.wait()
        self.play(self.items[1].animate.scale(2))
        self.play(self.items[3].animate.scale(2), self.items[1].animate.scale(0.5))
        self.play(self.items[1].animate.scale(2), self.items[3].animate.scale(0.5))
        self.wait(0.5)
        self.sort_items_internal(second_sorted)
        self.play(MoveToTarget(second_sorted[2]))
        self.wait()
        self.play(self.items[1].animate.scale(0.5))
        self.wait()
        self.sort_items_internal(second_sorted)
        self.play(MoveToTarget(second_sorted[3]))
        self.wait()

    def sort_items_internal(self, sorted_result):
        for i, item in enumerate(sorted_result):
            item.generate_target()
            if i>0:
                item.target.next_to(sorted_result[i-1].target, RIGHT*self.item_buf)
        targets = [item.target for item in sorted_result]
        VGroup(*targets).move_to(self.camera.frame)


        

    def initialize_numbers(self, nums, play=True): # Phase 1 - 숫자 선언 및 영상 표시
        self.items = []
        for i in range(len(nums)):
            t = NumText(f"{nums[i]:02}", font="Consolas") # 숫자
            s = Square(side_length=1, color=YELLOW_B).surround(t) # 숫자에 노란 박스
            item = VGroup(t, s) # 숫자-박스를 묶어서 하나의 item
            if i>0:
                item = item.next_to(self.items[i-1], RIGHT*self.item_buf) # item 오른쪽에 다음 item
            self.items.append(item)
        self.items_group = VGroup(*self.items).move_to(ORIGIN) # 모든 item을 묶어서 가운데 정렬
        self.play(self.camera.frame.animate.move_to(self.items_group).set(width=self.items_group.width*2)) # 카메라 시점을 아이템에 맞춤(개수에 따라 줌을 다르게)
        self.now_sorted = [[item] for item in self.items] # 정렬을 수행할 리스트, 시작은 len 1짜리 리스트로 구성된 리스트

        if play:
            self.play(LaggedStart(*[FadeIn(item) for item in self.items], lag_ratio=0.15, run_time=1.0)) # 아이템 나타남
            self.wait(0.1)
