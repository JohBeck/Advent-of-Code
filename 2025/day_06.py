import numpy as np
import time
import re

def part1(filename: str):
    # Apply sums and products to each collumn of numbers.
    with open(filename, 'r') as file:
        # Read Lines and remove endline characters. Additionally, separate the last line containing the operations.
        data = np.array([line.strip().split() for line in file.readlines()])
        operations = data[-1, :].flatten()
        data = data[:-1, :].astype(int)
        
        # Find locations of sums and products and apply them accordingly to the data.
        location_sum = np.where(operations == '+')[0]
        location_prod = np.where(operations == '*')[0]
        results = np.append(np.sum(data[:, location_sum], axis=0), np.prod(data[:, location_prod], axis=0))
    return np.sum(results)


def part2(filename: str):
    # Apply sums and products to each group of numbers separated by blank columns. Numbers are read column-wise, NOT line-wise.
    with open(filename, 'r') as file:
        # Read Lines and remove endline characters. Additionally, separate the last line containing the operations.
        data = np.array([line[:-1] for line in file.readlines()])
        operations = np.array(data[-1].split())
        
        # Split data by characters to keep the exact location of each digit.
        # Then, all numbers can be read column-wise by joining the individual characters.
        data = np.array(np.frombuffer(data[:-1], dtype='S4'), dtype=str).reshape(-1, len(data[0]))
        data = np.append(np.array([''.join(data[:, idx]) for idx in range(data.shape[1])]), ' ')

        # Find all sepearators (blank columns) and split the data accordingly.
        splits = np.where(np.array([re.search(r'^\s+$', d) for d in data], dtype=bool))[0] + 1
        data = [d[:-1].astype(int) for d in np.split(data, splits)]
        
        # Apply operations to each group of numbers.
        results = np.array([])
        for i in range(operations.shape[0]):
            if operations[i] == '+':
                results = np.append(results, np.sum(data[i]))
            else: # operations[i] == '*'
                results = np.append(results, np.prod(data[i]))
    return np.sum(results, dtype=int)

if __name__ == "__main__":
    assert part1('./2025/day_06_test.txt') == 4277556
    start_time = time.time()
    print(f"Part 1: {part1('./2025/day_06_input.txt')} -> t = {time.time() - start_time} seconds.")

    assert part2('./2025/day_06_test.txt') == 3263827
    start_time = time.time()
    print(f"Part 2: {part2('./2025/day_06_input.txt')} -> t = {time.time() - start_time} seconds.")