import numpy as np
import time

def part1(filename: str):
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        data = np.array(np.frombuffer(data, dtype='S4'), dtype=str).reshape(len(data[0]), -1)
        pos = np.where(data == '^')
        pos  = np.array((pos[0][0], pos[1][0]))
        dir = 'up'
        obstacles_rows = np.where(data == '#')
        sorted_indices = np.argsort(obstacles_rows[1])
        obstacles_cols = [obstacles_rows[i][sorted_indices] for i in range(len(obstacles_rows))]
        obs_per_col = [np.array([obstacles_cols[0][obstacles_cols[1] == i]]) for i in range(data.shape[1])]
        obs_per_row = [np.array([obstacles_rows[1][obstacles_rows[0] == i]]) for i in range(data.shape[0])]
        while True:
            # dir = 'up'
            obs = obs_per_col[pos[1]][obs_per_col[pos[1]] < pos[0]]
            if len(obs) == 0:
                data[0: pos[0] + 1, pos[1]] = 'X'
                break
            else:
                data[obs[-1] + 1:pos[0] + 1, pos[1]] = 'X'
                pos[0] = obs[-1] + 1
            # dir = 'right'
            obs = obs_per_row[pos[0]][obs_per_row[pos[0]] > pos[1]]
            if len(obs) == 0:
                data[pos[0], pos[1]:] = 'X'
                break
            else:
                data[pos[0], pos[1]: obs[0]] = 'X'
                pos[1] = obs[0] - 1
            # dir = 'down'
            obs = obs_per_col[pos[1]][obs_per_col[pos[1]] > pos[0]]
            if len(obs) == 0:
                data[pos[0]:, pos[1]] = 'X'
                break
            else:
                data[pos[0]: obs[0], pos[1]] = 'X'
                pos[0] = obs[0] - 1
        # dir = 'left'
            obs = obs_per_row[pos[0]][obs_per_row[pos[0]] < pos[1]]
            if len(obs) == 0:
                data[pos[0], 0: pos[1] + 1] = 'X'
                break
            else:
                data[pos[0], obs[-1] + 1: pos[1] + 1] = 'X'
                pos[1] = obs[-1] + 1
    return np.sum(data == 'X')

def part2(filename: str):
    # Implementation for part 2
    pass

if __name__ == "__main__":
    assert part1('./2024/06_test.txt') == 41
    start_time = time.time()
    print(f"Part 1 - Input: {part1('./2024/06_input.txt')} -> t = {time.time() - start_time} seconds.")    
    
    assert part2('./2024/06_test.txt') == 'TODO'
    start_time = time.time()
    print(f"Part 2 - Input: {part2('./2024/06_input.txt')} -> t = {time.time() - start_time} seconds.")