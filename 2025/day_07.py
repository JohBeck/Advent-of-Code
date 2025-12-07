import numpy as np
import time


def split_rays(current_rays: np.ndarray, splitter_positions: np.ndarray) -> np.ndarray:
    # Split all current rays '|' if they hit a splitter '^'.
    #  |            |
    #  ^    ->     |^|
    if current_rays.shape != splitter_positions.shape:
        raise ValueError("Current rays and splitter positions must have the same shape.")
    hits = np.where((current_rays == '|') & (splitter_positions == '^'))[0]
    for hit in hits:
        if hit < current_rays.shape[0] - 1:
            current_rays[hit + 1] = '|'
        if hit > 0:
            current_rays[hit - 1] = '|'
        current_rays[hit] = '^'
    return current_rays, len(hits)


def part1(filename: str):
    # Return the total number of times, the initial ray is split.
    total_hits = 0
    with open(filename, 'r') as f:
        data = np.array(f.read().strip().splitlines())
        # Read the initial rays and process each layer of splitters.
        rays = np.frombuffer(data[0], dtype='S4').astype(str)
        rays[rays == 'S'] = '|'
        for line in data[1:]:
            splitter = np.frombuffer(line, dtype='S4').astype(str)
            rays, nof_hits = split_rays(rays, splitter)
            total_hits += nof_hits
    return total_hits


def count_timelines(data: np.ndarray) -> int:
    # Starting at the final output layer, we can count the number of possible timelines backwards.
    # If there is a plitter, a ray hitting it ould cause two new rays in the deeper layer. 
    # Hence the current position is causing the number of rays of the neighboring positions in the deeper layers.
    # Adding this up allows us to directlyy extract the number of total timelines for every starting position
    timelines = np.ones(data.shape[1], dtype=int)
    for layer in reversed(range(data.shape[0] - 2)):
        splitter = np.where(data[layer + 1, :] == '^')[0]
        for s in splitter:
            tl_old = timelines.copy()
            timelines[s] = 0
            if s > 0:
                timelines[s] += tl_old[s - 1]
            if s < timelines.shape[0] - 1:
                timelines[s] += tl_old[s + 1]

    # The total number of timelines is given by the sum of all initial rays 'S'. 
    # In this case, there is just a single starting point, but in theory multiple are possible.            
    return timelines[np.where(data ==  'S')[1]].sum()


def part2(filename: str):
    # Count the number of posible ways a ray can travel through the splitters from start to end.
    with open(filename, 'r') as f:
        data = np.array(f.read().strip().splitlines())
        rays = np.array([np.frombuffer(d, dtype='S4').astype(str) for d in data])
        total_timelines = count_timelines(rays)
    return total_timelines

if __name__ == "__main__":
    assert part1('./2025/day_07_test.txt') == 21
    start_time = time.time()
    print(f"Part 1: {part1('./2025/day_07_input.txt')} -> t = {time.time() - start_time} seconds.")

    assert part2('./2025/day_07_test.txt') == 40
    start_time = time.time()
    print(f"Part 2: {part2('./2025/day_07_input.txt')} -> t = {time.time() - start_time} seconds.")