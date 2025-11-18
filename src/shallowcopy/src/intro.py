def second_largest(nums: list[list[int, str]]):
    numsc = nums.copy()
    numsc.sort(key=lambda x: x[0])
    return numsc[-2]
