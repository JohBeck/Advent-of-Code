import numpy as np
import time
from scipy.optimize import LinearConstraint, milp, Bounds


def find_shortest_path(start: int, end: int, steps: list[int]) -> int:
    # Apply breadth-first search to find the shortest path to the target setting 'end'
    queue = [(start, 0)]  # (current position, number of steps)
    seen = set([start])
    while queue:
        current, depth = queue.pop(0)

        # Add all possible next steps to the end of the queue.
        for step in steps:
            next_pos = current ^ step

            # Return if the end is reached with the next step.
            if next_pos == end:
                return depth + 1
            
            # Skip already seen positions and add new ones to the back of the queue.
            if next_pos in seen:
                continue
            queue.append((next_pos, depth + 1))

    return  np.inf


def part1(filename: str):
    # Implementation for part 1
    # Find the smallest sequence of button presses to achieve the target light configuration for each iteration.
    with open(filename, 'r') as file:
        # Load data and split it into lights, switches and joltages
        data = [line.strip().split() for line in file.readlines()]
        lights = []
        switches = []
        joltages = []
        for line in data:
            lights.append(line[0])
            switches.append(line[1:-1])
            joltages.append(line[-1])
        
        # find the best sequence of button presses for each iteration
        best_sequences = []
        for idx in range(len(lights)):
            # Define start and end states:
            start = 0  # always start with all lights off, therefore start = 0
            end = int(''.join('1' if c == '#' else '0' for c in lights[idx][-1:0:-1]), 2)

            # Create bitmasks:
            masks = []
            for s in switches[idx]:
                step = np.array(s[1:-1].split(','), dtype=int)
                masks.append(np.sum(np.pow(2, step)))

            # Find and store the shortest sequence for this iteration
            best_sequences.append(find_shortest_path(start, end, masks))

    # Return the sum of all best sequences found
    return sum(best_sequences)


def find_min_presses(switch_matrix: np.ndarray, end: np.ndarray) -> np.ndarray:
    # Find the minimal number of button presses needed to achieve the target joltage configuration 'end'
    # As this is an ILP problem, we use scipy's milp solver to find the optimal solution in a reasonable time.
    # My initial manual approach using BFS was not efficient enough for larger inputs, hence it is replaced by MILP.

    # Set parameters for MILP solver
    num_switches = switch_matrix.shape[1]
    bounds = Bounds(lb=np.zeros(num_switches), ub=np.full(num_switches, np.inf))
    c = np.ones(num_switches)
    constraint = LinearConstraint(switch_matrix, end, end)
    integrality = np.ones_like(c)
    
    # Solve MILP problem
    res = milp(
        c=c,
        constraints=constraint,
        integrality=integrality,
        bounds=bounds,
    )

    if not res.success:
        raise RuntimeError("MILP failed to find a solution.")
    return np.rint(res.x).astype(int)


def part2(filename: str):
    # Implementation for part 2
    # Find the minimal number of button presses to achieve the target joltage configuration for each iteration.
    with open(filename, 'r') as file:
        
        # Load data and split it into lights, switches and joltages
        data = [line.strip().split() for line in file.readlines()]
        lights = []
        switches = []
        joltages = []
        for line in data:
            lights.append(line[0])
            switches.append(line[1:-1])
            joltages.append(line[-1])

        # Find the smallest sequence of button presses for each iteration
        num_button_presses = []
        for iteration in range(len(lights)):
            num_switches = len(switches[iteration])
            num_lights = len(lights[iteration]) - 2   # inside [...] pattern

            # All buttons can be modeled in a matrix to solve the linear problem Ax=b.
            # As we are interested in a integer solution, this results in an Integer Linear Programming (ILP) problem.

            # Create the switch matrix
            # rows -> joltage meters; columns -> switches
            switch_matrix = np.zeros((num_lights, num_switches), dtype=int)
            for b, s in enumerate(switches[iteration]):
                idxs = np.fromstring(s[1:-1], sep=",", dtype=int)
                switch_matrix[idxs, b] = 1
            end = np.array(joltages[iteration][1:-1].split(','), dtype=int)   

            # Find the smallest sequence and store its length
            num_button_presses.append(np.sum(find_min_presses(switch_matrix, end)))

        return sum(num_button_presses)


if __name__ == "__main__":
    assert part1('./2025/day_10_test.txt') == 7
    start_time = time.time()
    print(f"Part 1: {part1('./2025/day_10_input.txt')} -> t = {time.time() - start_time} seconds.")

    # Aditional Test-Case: 
    # [#.#####] (2,3,4,6) (2,5) (1,3,4,5,6) (1,2,5,6) (0,5,6) (0,1,2,3,4,6) (1,2,3,5,6) (1,3,4,6) (0,2,3,4,5,6) {23,42,62,53,35,62,74}
    # Expected return: 74
    assert part2('./2025/day_10_test.txt') == 33
    start_time = time.time()
    print(f"Part 2: {part2('./2025/day_10_input.txt')} -> t = {time.time() - start_time} seconds.")