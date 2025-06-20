def fn1(n):
    h = n ** 2
    breakpoint()
    result = fn2(h)

    return result

def fn2(v):
    nums = [v, v*5, v*7]

    return sum(nums)

def main():
    num = 3
    result = fn1(num)
    print(f"Result: {result}")

main()