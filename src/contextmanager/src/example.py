from time import perf_counter
from contextlib import contextmanager

@contextmanager
def elapsed_time():
    start_time = perf_counter()
    yield
    end_time = perf_counter()
    time = end_time - start_time
    print(f"Elapsed time: {time:.6f} seconds")

with elapsed_time():
    ...
...