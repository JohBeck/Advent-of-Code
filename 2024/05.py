import numpy as np
import time
import re

def is_conform_to_norm(sequence: str, norm) -> bool:
    """
    Test if the sequence conforms to the given norm. The sequence conforms to the norm if the specified numbers are in the same order as in the norm.
    
    :param sequence: input sequence to test
    :param norm: array containing the two numbers to check the sequence against
    :return: True / False
    """
    key = F".*{norm[1]}.*{norm[0]}.*"
    if re.match(key, sequence):
        return False
    return True


def is_conform_to_norms(sequence: str, key) -> bool:
    """
    Check whether the sequence conforms to all the norms defined by the regex key.
    
    :param sequence: input sequence to test
    :param key: regex pattern to check the sequence against
    :return: True / False
    """    
    if re.match(key, sequence):
        return False
    return True


def part1(filename: str):
    # Implementation for part 1
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        cutoff = np.where(data == '')[0][0]
        norms = [list(map(int, line.split('|'))) for line in data[:cutoff]]
        sequences = data[cutoff+1:]
        sequences_split = []

        #  Build regex key for all norms to test all at once
        key = F".*{norms[0][1]}.*{norms[0][0]}.*"
        for i in norms:
            key += F"|.*{i[1]}.*{i[0]}.*"

        # Test all sequences and keep only those that conform to all norms
        for seq in sequences:
            if not is_conform_to_norms(seq, key):
                continue

            sequences_split.append(seq.split(','))
        
        # Return the sum of the middle elements of all conforming sequences
        results = [int(a[(len(a))//2]) for a in sequences_split]
    return sum(results)


def make_conform(seq: str, norms) -> str:
    """
    Update the sequence to conform to the given norms by swapping elements until all norms are met.
    
    :param seq: Input sequence to be modified
    :param norms: List of norms to apply
    :return: Modified sequence 
    """
    # Iteratively fix the sequence until all norms are matched
    i = 0
        
    while i < len(norms):
        n = norms[i]
        a = seq.find(F"{n[0]}")
        b = seq.find(F"{n[1]}")
        if b == -1 or a == -1:
            i += 1
            continue
        if b < a:
            seq = seq[:b] + F"{n[0]}," + seq[b:a] + seq[a+len(F"{n[0]},"):]
            i = 0
        else:
            i += 1
    
    if  seq [-1] == ',':
        seq = seq[:-1]
    return seq 


def part2(filename: str):
    # Implementation for part 2
    with open(filename, 'r') as file:
        data = np.array([line.strip() for line in file.readlines()])
        cutoff = np.where(data == '')[0][0]
        norms = [list(map(int, line.split('|'))) for line in data[:cutoff]]
        sequences = data[cutoff+1:]
        failed_sequences = []
        
        # Build regex key for all norms to test all at once
        key = F".*{norms[0][1]}.*{norms[0][0]}.*"
        for i in norms:
            key += F"|.*{i[1]}.*{i[0]}.*"

        # Test all sequences and modify those that do not conform to all norms.
        # Only store the modified sequences.
        for seq in sequences:
            if not is_conform_to_norms(seq, key):
                seq = make_conform(seq, norms) 
                failed_sequences.append(seq.split(','))
        
        # Return the sum of the middle elements of all modified sequences
        results = [int(a[(len(a))//2]) for a in failed_sequences]
    return sum(results)          
    

if __name__ == "__main__":
    assert part1('./2024/05_test.txt') == 143
    start_time = time.time()
    print(f"Part 1 - Input: {part1('./2024/05_input.txt')} -> t = {time.time() - start_time} seconds.")    
    
    assert part2('./2024/05_test.txt') == 123
    start_time = time.time()
    print(f"Part 2 - Input: {part2('./2024/05_input.txt')} -> t = {time.time() - start_time} seconds.")