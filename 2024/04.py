import numpy as np
import time

def find_xmas(data_grid: np.ndarray) -> list[tuple[int, int]]:
    # find all XMAS occurrences in the data grid
    # Orientation can be horizontal, vertical and diagonal in both directions

    # Find all locations of X, M, A, S
    x_loc = data_grid == 'X'
    m_loc = data_grid == 'M'
    a_loc = data_grid == 'A'
    s_loc = data_grid == 'S'

    # Check all orientations
    ltr = x_loc[:, :-3] & m_loc[:, 1:-2] & a_loc[:, 2:-1] & s_loc[:, 3:]
    rtl = s_loc[:, :-3] & a_loc[:, 1:-2] & m_loc[:, 2:-1] & x_loc[:, 3:]

    ttb = x_loc[:-3, :] & m_loc[1:-2, :] & a_loc[2:-1, :] & s_loc[3:, :]
    btt = s_loc[:-3, :] & a_loc[1:-2, :] & m_loc[2:-1, :] & x_loc[3:, :]

    tlbtr = x_loc[:-3, :-3] & m_loc[1:-2, 1:-2] & a_loc[2:-1, 2:-1] & s_loc[3:, 3:]
    brttl = s_loc[:-3, :-3] & a_loc[1:-2, 1:-2] & m_loc[2:-1, 2:-1] & x_loc[3:, 3:]

    blttr = x_loc[3:, :-3] & m_loc[2:-1, 1:-2] & a_loc[1:-2, 2:-1] & s_loc[:-3, 3:]
    trtbl = s_loc[3:, :-3] & a_loc[2:-1, 1:-2] & m_loc[1:-2, 2:-1] & x_loc[:-3, 3:]

    return np.sum(ltr) + np.sum(rtl) + np.sum(ttb) + np.sum(btt) + np.sum(tlbtr) + np.sum(brttl) + np.sum(blttr) + np.sum(trtbl)

def find_x_mas(data_grid: np.ndarray) -> list[tuple[int, int]]:
    # find all X-MAS occurrences in the data grid
    # Orientation can be rotated in 90° steps
    # 
    # Pattern:
    # M S
    #  A
    # M S

    # Find all locations of M, A, S
    m_loc = data_grid == 'M'
    a_loc = data_grid == 'A'
    s_loc = data_grid == 'S'

    # Order: TL, TR, C, BL, BR

    # 0°
    deg_000 = m_loc[:-2, :-2] & s_loc[:-2, 2:] & a_loc[1:-1, 1:-1] & m_loc[2:, :-2] & s_loc[2:, 2:]

    # 90°
    deg_090 = m_loc[:-2, :-2] & m_loc[:-2, 2:] & a_loc[1:-1, 1:-1] & s_loc[2:, :-2] & s_loc[2:, 2:]

    # 180°
    deg_180 = s_loc[:-2, :-2] & m_loc[:-2, 2:] & a_loc[1:-1, 1:-1] & s_loc[2:, :-2] & m_loc[2:, 2:]

    # 270°
    deg_270 = s_loc[:-2, :-2] & s_loc[:-2, 2:] & a_loc[1:-1, 1:-1] & m_loc[2:, :-2] & m_loc[2:, 2:]


    return np.sum(deg_000) + np.sum(deg_090) + np.sum(deg_180) + np.sum(deg_270)

def part1(filename: str):
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        data = np.array(np.frombuffer(data, dtype='S4'), dtype=str).reshape(len(data[0]), -1)
        nof_occurences = find_xmas(data)
        return nof_occurences


def part2(filename: str):
    # Implementation for part 2
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        data = np.array(np.frombuffer(data, dtype='S4'), dtype=str).reshape(len(data[0]), -1)
        nof_occurences = find_x_mas(data)
        return nof_occurences


if __name__ == "__main__":
    assert part1('./2024/04_test.txt') == 18
    start_time = time.time()
    print(f"Part 1 - Input: {part1('./2024/04_input.txt')} -> t = {time.time() - start_time} seconds.")    
    
    assert part2('./2024/04_test.txt') == 9
    start_time = time.time()
    print(f"Part 2 - Input: {part2('./2024/04_input.txt')} -> t = {time.time() - start_time} seconds.")