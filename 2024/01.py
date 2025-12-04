import numpy as np
import time

def part1(filename: str):
    # Implementation for part 1
    with open(filename, 'r') as file:
        data = np.array([line.strip().split() for line in file.readlines()]).astype(int)
        left = np.sort(data[:, 0])
        right = np.sort(data[:, 1])        

        return np.sum(np.abs(right - left))

def part2(filename: str):
    # Implementation for part 2
    with open(filename, 'r') as file:
        data = np.array([line.strip().split() for line in file.readlines()]).astype(int)
        occurrences = np.array([len(np.where(data[:,1] == v)[0]) for v in data[:, 0]])
        return np.dot(data[:, 0], occurrences)
    
if __name__ == "__main__":
    start_time = time.time()
    print(f"Part 1: {part1('./2024/01_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 1: {part1('./2024/01_input.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2024/01_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2024/01_input.txt')} -> t = {time.time() - start_time} seconds.")