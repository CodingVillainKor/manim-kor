from concurrent.futures import ProcessPoolExecutor
from time import sleep

data = [1, 2, 3, 4, 5, 6]

def func(x):
    sleep(5)
    print(x)
    return x * 2

with ProcessPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(func, i) for i in data]
    breakpoint()
    results = [future.result() for future in futures]