import os
import argparse

STARTING_SCRIPT = \
"""from manim import *
from raenim import *
from random import seed

seed(41)
np.random.seed(41)

class intro(Scene2D):
    def construct(self):
        pass
"""

def generate_project(project_name: str) -> None:    
    # make directory for the project
    prj_dirname = os.path.join("src", project_name)
    if os.path.exists(prj_dirname):
        print(f"Project {project_name} already exists in {prj_dirname}")
        return
    os.makedirs(prj_dirname, exist_ok=True)

    # create main.py in the project directory
    main_script_path = os.path.join(prj_dirname, "main.py")
    with open(main_script_path, "w") as f:
        f.write(STARTING_SCRIPT)
    
    # print finish
    print(f"Project {project_name} created successfully in {prj_dirname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new manim project")
    parser.add_argument("--name", required=True, type=str, help="Name of the project")
    args = parser.parse_args()

    generate_project(args.name)