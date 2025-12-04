import numpy as np
import time

def find_joltage_in_line(input: str, joltage_length:int) -> int:
    if(len(input) < joltage_length):
        return 0 # Not enough digits to form a joltage of the requested length
    digits = np.array(list(input), dtype=str)  # Split the string into individual characters for easy indexing
    positions = np.arange(len(input) - joltage_length, len(input))  # Initialize the solution at the end of the line and work backwards
    positions[0] = np.argmax(digits[0:positions[0] + 1])  # Find the first max in the range from start to the first position
    for i in range(1, len(positions)):
        # Find the next maximum in between the previous position and the current position
        positions[i] = positions[i-1] +1 + np.argmax(digits[positions[i-1]+1:positions[i]+1])  # Offset by previous max position +1 as the argmax is using local indexing
    return int(''.join(digits[positions]))  # return as joined integer


def get_joltages_from_file(filename: str, joltage_length :int = 12) -> int:
    joltages = []  # Store all joltages found in the file (as we only need the sum at the end it would be more efficient to sum directly, but this is clearer to keep track of intermediate results)
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            joltages.append(find_joltage_in_line(line.strip(), joltage_length))
    return joltages


if __name__ == "__main__":
    # Part 1: joltage length 2
    print ("Part 1: joltage length 2")
    start_time = time.time()
    print(f"Test data: {sum(get_joltages_from_file('./2025/day_03_test.txt', 2))}, -> t = {time.time() - start_time:.4f} seconds!")
    start_time = time.time()
    print(f"Input data: {sum(get_joltages_from_file('./2025/day_03_input.txt', 2))}, -> t = {time.time() - start_time:.4f} seconds!")

    # Part 2: joltage length 12
    print ("\nPart 2: joltage length 12")
    start_time = time.time()
    print(f"Test data: {sum(get_joltages_from_file('./2025/day_03_test.txt', 12))}, -> t = {time.time() - start_time:.4f} seconds!")
    start_time = time.time()
    print(f"Input data: {sum(get_joltages_from_file('./2025/day_03_input.txt', 12))}, -> t = {time.time() - start_time:.4f} seconds!")