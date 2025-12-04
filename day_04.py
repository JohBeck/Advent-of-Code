import numpy as np
from scipy import signal
import time

def remove_boxes_once(data: np.ndarray, max_neighbors:int) -> np.ndarray:
    # Convolution kernel to count all neighboring boxes
    kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])

    # Convolution is applied to all data including empty spaces and is subsequently filtered
    convolution = signal.convolve2d(data.astype(int), kernel, mode='same', boundary='fill', fillvalue=0)
    filtered = convolution[np.where(data)]

    # Remove possible boxes from the data-grid
    data[np.where(convolution < max_neighbors)] = False

    return data, np.sum(filtered < max_neighbors)

def remove_boxes(filename: str, max_iter: int = -1):
    nof_boxes_removed = 0
    iteration = 0
    with open(filename) as file:
        # Load data and convert it to an 2D grid of individual tokens. 
        # For better processing all entries are converted to booleans. Boxes are True, empty spaces are False
        data = np.array([line.strip() for line in file.readlines()])
        data = np.array(np.frombuffer(data, dtype='S4'), dtype=str).reshape(len(data[0]), -1) == '@'
        
        # Remove Boxes until no more can be removed or the iteration limit is reached
        while True:
            data, num_removed = remove_boxes_once(data, 4)
            nof_boxes_removed += num_removed
            iteration += 1
            if num_removed == 0 or (max_iter > 0 and iteration >= max_iter):
                break
    
    return nof_boxes_removed

if __name__ == "__main__":
    start_time = time.time()
    print(f"Part 1: {remove_boxes('day_04_test.txt', 1)} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 1: {remove_boxes('day_04_input.txt', 1)} -> t = {time.time() - start_time} seconds.")

    start_time = time.time()
    print(f"Part 2: {remove_boxes('day_04_test.txt')} -> t = {time.time() - start_time} seconds.")
    start_time = time.time()
    print(f"Part 2: {remove_boxes('day_04_input.txt')} -> t = {time.time() - start_time} seconds.")