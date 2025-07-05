data = [f"img{i}.png" for i in range(1000)]

with ProcessPoolExecutor() as executor:
    futures = [executor.submit(process, d) for d in data]
    results = [future.result() for future in futures]

print("Done")