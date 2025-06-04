from concurrent.futures import ProcessPoolExecutor

def fn(x):
    return x * x

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(fn, n) for n in range(10)]
        for future in futures:
            print(future.result())
