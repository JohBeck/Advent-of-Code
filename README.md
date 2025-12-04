# Advent of Code Solutions

This repository contains my solutions to **Advent of Code** challenges. I began actively participating in **2025**, and I am gradually working through previous years as well. All solutions are implemented in **Python**.

All challenge descriptions and sample data are available on the official Advent of Code website: <br />
https://adventofcode.com/

## Repository Structure

The repository is organized by year. Each year has its own directory, and within each directory every day’s puzzle solution is provided as a standalone Python file.

├── 2025/<br />
├──── day_01.py<br />
├──── day_02.py<br />
├──── ...<br />
├── 2024/<br />
├──── 01.py<br />
├──── 02.py<br />
├──── ...<br />
├── 2023/<br />
├──── ...<br />
└── README.md<br />


**Conventions:**

- Directory name: `<year>/`
- File name per puzzle day: `day_XX.py` or `XX.py` (zero-padded to two digits)
- Each file contains:
  - Parsing logic for the day’s input format
  - Solution for Part 1
  - Solution for Part 2
  - Any helper functions required for the puzzle

## Running Solutions

Solutions can be executed directly from the command line. For example:

```
python 2025/day_01.py
```

Each script specifies its expected file paths in the main section located at the bottom of the file.

## Requirements

- Python 3.10 or newer
- Numpy
- No external dependencies unless specifically noted in an individual solution

## Purpose

The objective of this repository is to:

- Track progress for the **current year’s** Advent of Code events  
- Backfill and complete **prior years’** challenges at my own pace  
- Maintain a clean, version-controlled history of iterative problem-solving techniques

## License

This repository is provided for educational and reference purposes. Use the code freely; attribution is appreciated but not required.

