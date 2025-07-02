from pathlib import Path

for p in Path("data/").rglob("*"):
    if p.suffix in [".jpg", ".png"]:
        print(str(p))

