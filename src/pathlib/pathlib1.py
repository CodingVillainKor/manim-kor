from pathlib import Path

p = Path("data/")

for item in p.rglob("*"):
    print(str(item))

