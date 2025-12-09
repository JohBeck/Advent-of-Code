import numpy as np
import time


def find_largest_rect(positions: np.ndarray):
    # Find all unique pairs of positions
    unique_idcs = np.triu_indices(len(positions), k=1)

    # Calculate distances between all unique pairs
    distances = np.abs(positions[:, None, :] - (positions[None, :, :] ))+ 1
    unique_distances = distances[unique_idcs]

    # Calculate areas of rectangles formed by each unique pair
    areas = np.multiply(unique_distances[:, 0], unique_distances[:, 1])

    return max(areas)


def part1(filename: str):
    # Implementation for part 1
    # Data Loading + Processing
    with open(filename, 'r') as file:
        data = file.readlines()
        data = np.array([line.strip().split(',') for line in data], dtype=int)
        return find_largest_rect(data)


def rect_is_in_area(area: list[np.ndarray], area_offset: int, min_x: int, min_y: int, max_x: int, max_y: int) -> bool:
    """
    Test if Rectangle (min_x, min_y) to (max_x, max_y) is fully inside the area defined by 'area'
    
    :param area: List of sequences defining the area. Each entry lists the y-intervals for a given x. (start0, end0, start1, end1, ...)
    :type area: list[np.ndarray]
    :param area_offset: offset between area index and actual x-coordinate
    :type area_offset: int
    :param min_x: lower x-bound of the rectangle
    :type min_x: int
    :param min_y: lower y-bound of the rectangle
    :type min_y: int
    :param max_x: upper x-bound of the rectangle
    :type max_x: int
    :param max_y: upper y-bound of the rectangle
    :type max_y: int
    :return: True if the rectangle is fully inside the area, False otherwise
    :rtype: bool
    """
    for x in range(min_x, max_x):
        arr = area[x - area_offset] 

        idx = arr.searchsorted(min_y, side="right") - 1  # y0_in

        # If min_y is not inside an interior interval
        if idx < 0 or idx+1 >= len(arr) or idx % 2 != 0:
            return False

        interval_end = arr[idx+1]

        # Entire vertical span must be inside the same interval
        if max_y > interval_end:
            return False
    return True


def find_largest_rect_restricted(positions: np.ndarray):
    # Find all unique pairs of positions similar to part 1
    unique_idcs = np.triu_indices(len(positions), k=1)
    distances = np.abs(positions[:, None, :] - (positions[None, :, :] ))+ 1
    unique_distances = distances[unique_idcs]
    areas = np.multiply(unique_distances[:, 0], unique_distances[:, 1])

    # find all red and green rectangles -> aka the area circumscribed by the initial data points
    # The final area is encoded in marked_area as a list of lists. Each list contains the ranges of y-values for a given x. (start0, end0, start1, end1, ...)
    # the x-values are offset by min_x to reduce memory usage. (Only store the area between min_x and max_x of the input points)
    min_x, max_x = np.min(positions[:, 0]), np.max(positions[:, 0])
    marked_area = [[] for i in range(max_x + 1 - min_x)]
    horizontal_lines = []  # list of (x, y_start, y_end)

    # First, process all vertical lines and store horizontal lines for later processing
    for idx in range(len(positions)):
        x0, y0 = positions[idx - 1]
        x1, y1 = positions[idx]
        if x0 == x1:
            horizontal_lines.append((x0, min(y0, y1), max(y0, y1)))
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                marked_area[x - min_x].append(y0)

    [m.sort() for m in marked_area]
    
    """
    Process horizontal lines to finalize the area marking
    All start and endpoints are already part of the lists due to vertical line processing
    BUT: In some cases we need to remove certain end-points to ensure correct area marking
    e.g.
    * * * * * * * * * * * * * # # # 00 
    * * * * # # # # * * * * * # - # 01 
    * * * * # - - # * * * * * # - # 02 
    # # * * # - - # * * * * * # - # 03 
    # # # # # - - # # # # # # # - # 04 
    # - - - - - - - - - - - - - - # 05 
    # # # # # # # # # # # # # # # # 06
    0         5         10        15

    Here, line 4 should span the entire width, hence the horizontal lines at y = (1, 4, 7, 13) need to be removed.
    """
    for hline in horizontal_lines:
        x = hline[0]
        y0 = min(hline[1], hline[2])
        y1 = max(hline[1], hline[2])
        line = np.array(marked_area[x - min_x])

        y0_loc = np.where(line <= y0)[0][-1]

        if y0_loc % 2 == 1:
            marked_area[x - min_x].remove(y0)

        # check entries above and below y0 and y1. If either above or below has 2x outside we have a "hill-top", hence we keep y1. else we remove it, as we are still in the same volume.
        if x != min_x and x != max_x:
            y1_above = -1 + np.sum(np.array(marked_area[x - min_x - 1]) <= y1) % 2 == 0
            y1_below = -1 + np.sum(np.array(marked_area[x - min_x + 1]) <= y1) % 2 == 0

            # If both values above and below y1 are inside the volume, y1 cannot end the volume here, hence we remove it.
            if y1_below and y1_above:            
                marked_area[x - min_x].remove(y1)    
    
    # Now check all rectangles defined by unique position pairs, starting from the largest area
    # Once a match is found it is returned. Dure to the sorting this is guaranteed to be the largest possible rectangle.
    count = 0
        
    marked_area = [np.array(m, dtype=int) for m in marked_area]
    sorted_area_idcs = np.argsort(areas)[::-1]
    for idx in sorted_area_idcs:
        point_1 = positions[unique_idcs[0][ idx]]
        point_2 = positions[unique_idcs[1][ idx]]
        if rect_is_in_area(marked_area, min_x, min(point_1[0], point_2[0]), min(point_1[1], point_2[1]), max(point_1[0], point_2[0]), max(point_1[1], point_2[1])):
            return areas[idx]    
        
        # Progress Tracker to review search progress and estimate remaining time
        count += 1
        if count % 5000 == 0:
            print(f"Checked {count} rectangles... Current area: {areas[idx]}")


def part2(filename: str):
    # Implementation for part 2
    # Data Loading + Processing
    with open(filename, 'r') as file:
        data = file.readlines()
        data = np.array([line.strip().split(',') for line in data], dtype=int)
        return find_largest_rect_restricted(data)


if __name__ == "__main__":
    assert part1('./2025/day_09_test.txt') == 50
    start_time = time.time()
    print(f"Part 1: {part1('./2025/day_09_input.txt')} -> t = {time.time() - start_time} seconds.")

    print("Starting Part 2 Tests... \n Execution times may vary significantly based on input size. During my experiments the actual data took around 3 minutes to compute.")
    assert part2('./2025/day_09_test.txt') == 24
    """
    Self Generated Test Case: Target 45
    3,0
    3,1
    4,1
    4,4
    1,4
    1,7
    4,7
    4,13
    0,13
    0,15
    6,15
    6,0

    assert part2('./2025/day_09_test_1.txt') == 45 
    """
    start_time = time.time()
    print(f"Part 2: {part2('./2025/day_09_input.txt')} -> t = {time.time() - start_time} seconds.")