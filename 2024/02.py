import numpy as np
import time


def test_line(line: str) -> bool:
    if line.strip() == '':
        return False
    data = np.fromstring(line, dtype=int, sep=' ')
    steps = data[1:] - data[:-1]
    if (np.all(steps > 0) or np.all(steps < 0)) and np.max(np.abs(steps)) <= 3 :
        return True
    return False


def test_line_dampened(line: str) -> bool:
    # First check if it passes the normal test
    if test_line(line):
        return True
    
    # Else try if it can pass with one dampened step
    data = np.fromstring(line, dtype=int, sep=' ')
    steps = data[1:] - data[:-1]
    checks_decreasing_fail = np.any([steps >= 0, steps < -3], axis=0)
    checks_increasing_fail = np.any([steps <= 0, steps > 3], axis=0)
    if np.sum(checks_decreasing_fail) > 2 and np.sum(checks_increasing_fail) > 2:
        return False
    elif np.sum(checks_decreasing_fail) < np.sum(checks_increasing_fail):
        idx = np.where(checks_decreasing_fail)[0][0]
    else:
        idx = np.where(checks_increasing_fail)[0][0]
    
    # Every conflict could be caused by either of the two neighboring entries.
    # Testing both allows to resolve cases where one entry causes two conflicts, which are resolved by its removal.
    # Create a new line-string without the first conflicting entry and retry the validation
    new_line = ' '.join(data[:idx].astype(str)) + ' ' + ' '.join(data[idx+1:].astype(str))
    if test_line(new_line):
        return True
    
    # Try removing the next entry instead. 
    idx += 1
    new_line = ' '.join(data[:idx].astype(str)) + ' ' + ' '.join(data[idx+1:].astype(str))

    # Any further conflicts cannot be resolved with a single removal.
    return test_line(new_line)


def part1(filename: str):
    # Task 1: Find the number ofvalid lines in the file without any deletion.
    with open(filename, 'r') as file:
        data = file.readlines()
        res = [test_line(line) for line in data]
    return np.sum(res)

def part2(filename: str):
    # Task 2: Find the number of valid lines in the file with at most one deletion.
    with open(filename, 'r') as file:
        data = file.readlines()
        res = [test_line_dampened(line) for line in data]
    return np.sum(res)

if __name__ == "__main__":

    assert test_line_dampened("1 4 7 10 7 4 1 ") == False
    assert test_line_dampened("1 4 7 7 10") == True
    assert test_line_dampened("9 1 4 5 6 7") == True
    assert test_line_dampened("9 1 4 5 5 7") == False
    assert test_line_dampened("1 4 5 6 7 7") == True
    assert test_line_dampened("1 5 6 7 7") == False
    assert test_line_dampened("1 4 5 4 8") == True


    start_time = time.time()
    print(f"Part 1: {part1('./2024/02_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 1: {part1('./2024/02_input.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2024/02_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {part2('./2024/02_input.txt')} -> t = {time.time() - start_time} seconds.")  # -> 683 is to low