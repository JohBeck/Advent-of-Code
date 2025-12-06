import numpy as np
import time
import re


def find_all_matches(string: str):
    # Use Regex to find all occurrences of mul(x,y)
    target = r'mul\(\d*,\d*\)'
    return re.findall(target, string)


def find_all_enabled_matches(string: str):
    # Use Regex to find all occurrences of "mul(x,y)", "don't", and "do" as non-capturing groups.
    target = r'(?:mul\(\d*,\d*\))|(?:don\'t)|(?:do)'
    return re.findall(target, string)


def part1(filename: str):
    # Task 1: Find all valid multiplications and sum their products.
    with open(filename, 'r') as file:
        data = file.read().strip()
        matches = find_all_matches(data)
        matches = np.array([re.findall(r'\d+', m) for m in matches] ).astype(int)
    return np.dot(matches[:, 0], matches[:,1])


def part2(filename: str):
    result = 0
    # Task 2: Find all valid multiplications, but only apply those that are "enabled". "Do" and "Don't" enable and disable the multiplications.
    with open(filename, 'r') as file:
        data = file.read().strip()
        matches = find_all_enabled_matches(data)
        active = True
        for i, m in enumerate(matches):
            if m == "don't":
                active = False
            elif m == "do":
                active = True
            elif active:
                nums = re.findall(r'\d+', m)
                result += int(nums[0]) * int(nums[1]) 

    return result


if __name__ == "__main__":
    assert part1('./2024/03_test.txt') == 161
    assert part2('./2024/03_test.txt') == 48

    start_time = time.time()
    print(f"Part 1: {part1('./2024/03_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 1: {part1('./2024/03_input.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2024/03_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2024/03_input.txt')} -> t = {time.time() - start_time} seconds.")