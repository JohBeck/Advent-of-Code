import numpy as np
import time

def connect_junctions(data: np.ndarray, num_connections: int = -1):
    """
    Find connections between junctions based on their pairwise distances.
    Either fit a given number of connections or connect all junctions into a single circuit.
    
    :param data: array of 3D junction coordinates -> shape (num_junctions, 3)
    :type data: np.ndarray
    :param num_connections: num of connections applied to the input. If -1, connections are applied, until all junctions are within the same circuit.
    :type num_connections: int
    """
    # Calculate all pairwise distances
    # As shorter distances are more relevant, indices contains a list of junction-pairs that is sorted by distance. Attention, that self-distances (0) are also included!
    distance_vecs = data[:, None, :] - data[None, :, :]    
    distance_norms = np.linalg.norm(distance_vecs, axis = 2)
    indices = np.array(np.unravel_index(np.argsort(distance_norms, axis=None), distance_norms.shape)).T[::2,:]

    # Initialize the circuits. Initially, each junction is its own circuit.
    # circuits stores a list of junction for each circuit
    # junctions stores the circuit index for each junction
    # This allow bidirectional access between junctions and circuits
    circuits = {}
    for i in range( len(data)):
        circuits[i] = list([i])
    junctions = np.arange(len(data))  # each point is its own junction initially

    # iterate over the sorted distances but drop self-distances (idx_x == idx_y), as these are always zero!
    connections_count = 0
    
    for i in range(len(indices)):
        # Stop if the requested number of connections is reached or if all junctions are connected
        if num_connections > 0 and connections_count >= num_connections:
            break
        if len(circuits) <= 1:
            break

        # Get the next closest pair of junctions and ignore self-distances (idx_x == idx_y) 
        idx_x = indices[i, 0] 
        idx_y = indices[i, 1]
        if idx_x == idx_y:
            continue

        min_j = min(junctions[idx_x], junctions[idx_y])
        max_j = max(junctions[idx_x], junctions[idx_y])  
        connections_count += 1

        # Skip connections if there junctions are already connected via other connections
        if min_j == max_j:
            continue

        # Merge the two circuits
        circuits[min_j] += circuits[max_j]
        for idx in circuits[max_j]:
            junctions[idx] = min_j
        circuits.pop(max_j)
        
    # sort circuits by size to find the largest ones.
    circuit_sizes = np.sort([len(circuit) for circuit in circuits.values()])        

    # Return: 
    # Task 1 - multiply sizes of the three largest circuits    
    # Task 2 - Return the product of the final junctions x-coordinates
    return np.prod(circuit_sizes[-3:]) , data[idx_x, 0] * data[idx_y, 0]


def connect_junctions_from_file(filename: str, num_connections: int = -1):
    """
    Load data from the specified file and find connections between junctions.
    
    :param filename: name of the input file
    :type filename: str
    :param num_connections: num of connections applied to the input. If -1, connections are applied, until all junctions are within the same circuit.
    :type num_connections: int
    """  
    with open(filename, 'r') as f:
        data = f.read().strip().splitlines()
        data = np.array([s.split(',') for s in data], dtype=int)
        return connect_junctions(data, num_connections)


if __name__ == "__main__":
    assert connect_junctions_from_file('./2025/day_08_test.txt', 10)[0] == 40
    start_time = time.time()
    print(f"Part 1: {connect_junctions_from_file('./2025/day_08_input.txt', 1000)[0]} -> t = {time.time() - start_time} seconds.")

    assert connect_junctions_from_file('./2025/day_08_test.txt')[1] == 25272
    start_time = time.time()
    print(f"Part 2: {connect_junctions_from_file('./2025/day_08_input.txt')[1]} -> t = {time.time() - start_time} seconds.")