def turn (pos: int, distance: str) -> int:
    max_pos = 99

    if(distance.startswith('R')):
        distance = int(distance[1:])
    else:
        distance = -int(distance[1:])
    new_pos = pos + distance

    # Part B
    zero_crossing = int(abs(new_pos) / 100)
    if(pos > 0 and new_pos <= 0):
        zero_crossing += 1
    
    # Part A:
    new_pos = (new_pos + max_pos + 1) % (max_pos + 1)


    return new_pos, zero_crossing

def eval_file(filename: str):
    positions = [50] # all resting positions of the wheel
    total_zc = 0  # Total zero crossings

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            val, zc  = turn(positions[-1], line.strip())
            positions.append(val)
            total_zc += zc

        print(f"File {filename}: \t Final pos {positions[-1]} \t --- \t NOFzeros: {positions.count(0)} \t --- \t NOFzc: {total_zc}")

if __name__ == "__main__":
    # Tests
    assert turn(50, 'R10') == (60, 0)
    assert turn(50, 'R60') == (10, 1)
    assert turn(50, 'L1000') == (50, 10)
    assert turn(0, 'L100') == (0, 1)
    assert turn(99, 'R1') == (0, 1)
    assert turn(10, 'L220') == (90, 3)
    assert turn(0, 'R100') == (0, 1)
    assert turn(0, 'R200') == (0, 2)
    assert turn(99, 'R101') == (0, 2)

    # Actual eval

    eval_file("day_01_test.txt")
    eval_file("day_01_input.txt")