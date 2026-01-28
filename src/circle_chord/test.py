import numpy as np


def check_cross(angles):
    chord1 = sorted([angles[0], angles[1]])
    chord2 = sorted([angles[2], angles[3]])
    point1_between = chord1[0] < chord2[0] < chord1[1]
    point2_between = chord1[0] < chord2[1] < chord1[1]
    return point1_between != point2_between


def test():
    intersect_count = 0
    non_intersect_count = 0

    for _ in range(1000000):
        angles = np.random.uniform(0, 2 * np.pi, 4)
        if check_cross(angles):
            intersect_count += 1
        else:
            non_intersect_count += 1

    probability = intersect_count / 1000000

    return probability


def main():
    prob = test()
    print(f"Probability of crossing: {prob:.4f}")

if __name__ == "__main__":
    main()
