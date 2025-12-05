import numpy as np
import time


'''
Part 1:
Idea: Merge interavls into array of transition numbers, so that the look like this:
endX is always increased by one to distinguish between entries and exits -> end1 = val1 + 1.
This way entries are inclusive and exits are exclusive, allowing a separation using <= and < comparisons.

start1, end1, start2, end2, ...

To test an ingredient find the closest lower bond and see if it is a start or an end.
start -> even number -> inside interval
end -> odd number -> outside interval

Part 2:

use the difference between start and end points to count the number of fresh ingredients.
sum(end - start) over all merged intervals.
'''


def merge_intervals(intervals:np.ndarray) -> np.ndarray:
    '''
    Merge overlapping intervals into a list of unique intervals.

    :param intervals: input intervals as array of strings ["start1-end1", "start2-end2", ...]
    :type intervals: np.ndarray
    :return: Unique merged intervals as array of numbers [start1, end1, start2, end2, ...]
    :rtype: ndarray[(-1,), dtype[int]]
    '''
    intervals = np.append(np.array([i.split('-') for i in intervals]).astype(int), values=[[np.inf, np.inf]], axis=0)  # add np.inf as end-of-lne tokens.

    merged = []
    set_in = np.sort(intervals[:, 0])
    set_out = np.sort(intervals[:, 1]) + 1  # increase end by one to distinguish between entries and exits
    # Iterate all entries and count the number of open intervals. 
    # Numbers in the "set_in" increase the number of open intervals, numbers in the "set_out" decrease it.
    # reducing the count to zero means that all intervals are closed, so we can add the current number as an end of the current interval.
    # Similarly, increasing the count from zero means that a new interval is opened, so we need to add the current number as a start of a merged interval.
    count = 0
    idx_in = 1
    idx_out = 1
    next_in = set_in[0]
    next_out = set_out[0]
    while next_in != np.inf or next_out != np.inf:
        if next_in <= next_out:
            count += 1

            if count == 1:
                merged = np.append(merged, next_in)
            
            next_in = set_in[idx_in]
            idx_in += 1


        else:
            count -= 1

            if count == 0:
                merged = np.append(merged, next_out)
            
            next_out = set_out[idx_out]
            idx_out += 1

    return merged


def test_ingredient(ingredient:int, intervals:np.ndarray) -> bool:
    '''
    Test if an ingredient is fresh (inside any of the intervals) or spoiled (outside all intervals).
    :param ingredient: ingredient number to test
    :type ingredient: int
    :param intervals: merged intervals as array of numbers [start1, end1, start2, end2, ...]
    :type intervals: np.ndarray
    :return: True if ingredient is fresh, False if spoiled
    :rtype: bool
    '''
    tmp = np.sum(intervals < ingredient) % 2
    return np.sum(intervals < ingredient) % 2


def part1(filename: str):
    # Combine all ranges and test ingredients against the combined ranges to find out which are fresh and which are spoiled.
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        cutoff = np.where(data == '')[0][0]
        intervals = merge_intervals(data[:cutoff])
        results = [test_ingredient(int(i), intervals) for i in data[cutoff+1:]]

    return np.sum(results)


def part2(filename: str):
    # count the number of fresh ingredients
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        cutoff = np.where(data == '')[0][0]
        intervals = merge_intervals(data[:cutoff]).reshape(-1, 2)
    return int(np.sum(intervals[:, 1] - intervals[:, 0]))


if __name__ == "__main__":
    test_range = np.array([3, 5, 10, 15, 20, 25])
    assert merge_intervals(np.array(['1-4', '2-6', '8-10', '15-18'])) .tolist() == np.array([1, 7, 8, 11, 15, 19]).tolist()
    assert merge_intervals(np.array(['1-4', '6-6', '8-10', '15-18'])) .tolist() == np.array([1, 5, 6, 7, 8, 11, 15, 19 ]).tolist()
    assert merge_intervals(np.array(['1-4', '5-6', '8-10', '15-18'])) .tolist() == np.array([1, 7, 8, 11, 15, 19 ]).tolist()
    
    assert test_ingredient(4, test_range) == True
    assert test_ingredient(2, test_range) == False
    assert test_ingredient(6, test_range) == False
    assert test_ingredient(12, test_range) == True

    start_time = time.time()
    print(f"Part 1: {part1('./2025/day_05_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 1: {part1('./2025/day_05_input.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2025/day_05_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2025/day_05_input.txt')} -> t = {time.time() - start_time} seconds.")