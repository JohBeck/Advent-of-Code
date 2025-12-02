import re


# Task 1: Exactly 2 occurences of any digit sequnence
# Check that the id fully consists of a sequence of digits recurring 2 times using regular expressions
# The regex checks for recurring sequences that both start AND end the string.
# 
# e.G 123123 -> valid, 123123123 -> invalid, 123456 -> valid
regex_task_1 = r'^(\d+)\1$'  # Part 1: Exactly 2 Occurences


# Task 2: At least 2 occurences of any digit sequnence
# Check for a sequence of digits recurring multiple times using regular expressions
# 
# e.G 123123 -> invalid, 123123123 -> invalid, 123456 -> valid
regex_task_2 = r'^(\d+)\1+$' # Part 2: At least 2 Occurences


def is_valid_id(id:int) -> bool:
    # Convert to string to use regex.
    # Leading zeros are already removed by str -> int -> str conversion.
    # The regex checks for recurring sequences that both start AND end the string.
    if re.search(regex_task_2, str(id)):  # TODO: Change between "regex_task_1" for Part 1 and "regex_task_2" for Part 2
        return False
    return True


def get_invalid_ids_in_range(start:int, end:int) -> list[int]:    
    return [entry for entry in range(start, end + 1) if not is_valid_id(entry)]  # Return invalid IDs


def get_invalid_ids_from_file(filename: str) -> list[int]:
    invalid_ids = []
    with open(filename, "r") as file:
        data = file.read().strip().split(",")
        for id_str in data:
            start, end = id_str.split("-")
            invalid_ids.extend(get_invalid_ids_in_range(int(start), int(end)))
    return invalid_ids


if __name__ == "__main__":
    # Tests (Both Tasks):
    assert is_valid_id(123123) == False
    assert is_valid_id(123456) == True
    assert is_valid_id(111222) == True
    assert is_valid_id(1231232) == True

    # Tests (Task 1):
    # assert is_valid_id(123123123) == True

    # Tests (Task 2):
    # assert is_valid_id(123123123) == False

    print("Test data:", sum(get_invalid_ids_from_file("day_02_test.txt")))
    print("Input data:", sum(get_invalid_ids_from_file("day_02_input.txt")))