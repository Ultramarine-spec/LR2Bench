import os
import json

rules = '''
Sudoku is a logic-based, combinatorial number-placement puzzle. The puzzle consists of an n^2 x n^2 grid, partially filled with numbers from 1 to n^2 and 0 (empty cells). The objective is to fill the grid so that each row, each column, and each n x n subgrid must contain every number from 1 to n^2 exactly once.
'''
rules = rules.strip()

requests = '''
Please solve the Sudoku Puzzle according to the provided rules. Please also follow the requests below to present your analysis and solutions:
1. For each empty cell, try to deduce which numbers are allowed based on the existing numbers in its row, column, and subgrid.
2. If you reach a point where no obvious choices are available, you may need to backtrack. Try filling in a number and see if it leads to a valid solution. If it causes a contradiction, backtrack to a previous decision and try a different path.
3. Please provide step by step analysis and present the final answer as the same json format of the input grid. Wrapping the final answer with <Answer> and </Answer> tags.
4. Please generate your response without redundant and repeating content.
'''
requests = requests.strip()


example1 = '''
Here is a 4 x 4 sudoku puzzle:
[[0, 3, 4, 0],
 [4, 0, 0, 2],
 [1, 0, 0, 3],
 [0, 2, 1, 0]]
'''
example1 = example1.strip()

solution1 = '''
Let's start solving the sudoku puzzle step by step.

Step 1: Analyze the Puzzle Constraints
Row Analysis
Row 1: 0 3 4 0
    Numbers already used: 3, 4
    Remaining possible numbers: 1, 2
Row 2: 4 0 0 2
    Numbers already used: 4, 2
    Remaining possible numbers: 1, 3
Row 3: 1 0 0 3
    Numbers already used: 1, 3
    Remaining possible numbers: 2, 4
Row 4: 0 2 1 0
    Numbers already used: 2, 1
    Remaining possible numbers: 3, 4

Column Analysis
Column 1: 0 4 1 0
    Numbers already used: 4, 1
    Remaining possible numbers: 2, 3
Column 2: 3 0 0 2
    Numbers already used: 3, 2
    Remaining possible numbers: 1, 4
Column 3: 4 0 0 1
    Numbers already used: 4, 1
    Remaining possible numbers: 2, 3
Column 4: 0 2 3 0
    Numbers already used: 2, 3
    Remaining possible numbers: 1, 4

Subgrid Analysis
Top-left Subgrid (cells 1,1 to 2,2):
    Already filled: 0, 3, 4, 0 (remaining: 1, 2)
Top-right Subgrid (cells 1,3 to 2,4):
    Already filled: 4, 0, 0, 2 (remaining: 1, 3)
Bottom-left Subgrid (cells 3,1 to 4,2):
    Already filled: 1, 0, 0, 2 (remaining: 3, 4)
Bottom-right Subgrid (cells 3,3 to 4,4):
    Already filled: 0, 3, 1, 0 (remaining: 2, 4)

Step 2: Start Filling in Obvious Numbers
Cell (1,1): From the analysis above, the only possible numbers are 1 and 2. However, since 1 is already in the first column, this cell must be 2.
Cell (1,4): The only possible number left in row 1 is 1.
Cell (2,2): The possible numbers here are 1 and 3. Given that 3 is already in column 2, this cell must be 1.
Cell (2,3): The only remaining number for this cell in row 2 is 3.
Cell (3,2): The possible numbers here are 2 and 4. Given that 2 is already in column 2, this cell must be 4.
Cell (3,3): The only possible number left here is 2.
Cell (4,1): The only possible number left in row 4 and column 1 is 3.
Cell (4,4): The only remaining number for this cell in row 4 and column 4 is 4.

Step 3: Fill in the Grid
Here is the final answer:
<Answer>
[[2, 3, 4, 1],
 [4, 1, 3, 2],
 [1, 4, 2, 3],
 [3, 2, 1, 4]]
</Answer>
'''
solution1 = solution1.strip()


example2 = '''
Here is a 4 x 4 sudoku puzzle:
[[2, 0, 0, 0],
 [0, 0, 3, 0],
 [0, 4, 0, 0],
 [0, 0, 0, 1]]
'''
example2 = example2.strip()

solution2 = '''
Let's start solving the sudoku puzzle step by step.

Step1: Analyze Empty Cell in Row 1
Cell (1,2):
    Eliminated Numbers: 2 (already in row), 4 (already in column)
    Possible Numbers: 1, 3
Cell (1,3):
    Eliminated Numbers: 2 (already in row), 3 (already in column)
    Possible Numbers: 1, 4
Cell (1,4):
    Eliminated Numbers: 2 (already in row), 1 (already in column), 3 (already in subgrid)
    Only possible number: 4

Deduction:
Cell (1,4) must be 4.
Cell (1,3) cannot be 4, so it must be 1.
Cell (1,2) cannot be 1, so it must be 3.
Row 1: 2 3 1 4

Grid:
[[2, 3, 1, 4],
 [0, 0, 3, 0],
 [0, 4, 0, 0],
 [0, 0, 0, 1]]

Step 2: Analyze Empty Cell in Row 2
Cell (2,1):
    Eliminated Numbers: 2 (already in column), 3 (already in row)
    Possible Numbers: 1, 4
Cell (2,2):
    Eliminated Numbers: 2 (already in subgrid), 3, 4 (already in column)
    Only possible number: 1
Cell (2,4):
    Eliminated Numbers: 1, 3, 4 (already in subgrid)
    Only possible number: 2

Deduction:
Cell (2,2) must be 1.
Cell (2,4) must be 2.
Cell (2,1) cannot be 1, so it must be 4.
Row 2: 4 1 3 2

Grid:
[[2, 3, 1, 4],
 [4, 1, 3, 2],
 [0, 4, 0, 0],
 [0, 0, 0, 1]]

Step 3: Analyze Empty Cell in Row 3
Cell (3,1):
    Eliminated Numbers: 2, 4 (already in column)
    Possible Numbers: 1, 3
Cell (3,3):
    Eliminated Numbers: 1, 3 (already in column), 4 (already in row)
    Only possible number: 2
Cell (3,4):
    Eliminated Numbers: 1, 2, 4 (already in column)
    Only possible number: 3

Deduction:
Cell (3,3) must be 2.
Cell (3,4) must be 3.
Cell (3,1) cannot be 3, so it must be 1.
Row 3: 1 4 2 3

Grid:
[[2, 3, 1, 4],
 [4, 1, 3, 2],
 [1, 4, 2, 3],
 [0, 0, 0, 1]]

Step 4: Analyze Empty Cell in Row 4
Cell (4,1):
    Eliminated Numbers: 1, 2, 4 (already in column)
    Only possible number: 3
Cell (4,2):
    Eliminated Numbers: 1, 3, 4 (already in column)
    Only possible number: 2
Cell (4,3):
    Eliminated Numbers: 1, 2, 3 (already in column)
    Only possible number: 4
Row 4: 3 2 4 1

Grid:
[[2, 3, 1, 4],
 [4, 1, 3, 2],
 [1, 4, 2, 3],
 [3, 2, 4, 1]]

Step 5: Final Answer
<Answer>
[[2, 3, 1, 4],
 [4, 1, 3, 2],
 [1, 4, 2, 3],
 [3, 2, 4, 1]]
</Answer>
'''
solution2 = solution2.strip()



example = "<example>"

shot_dict = {}


shot_dict['zero_shot'] = [
    {"role": "system", "content": "You are an expert sudoku puzzle solver."},
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"},
]   


shot_dict['two_shot'] = [
    {"role": "system", "content": "You are an expert sudoku puzzle solver."},
    {"role": "user", "content": f"{rules}\n\n{example1}\n\n{requests}"},
    {"role": "assistant", "content": solution1},
    {"role": "user", "content": f"{example2}\n\n{requests}"},
    {"role": "assistant", "content": solution2},
    {"role": "user", "content": f"{example}\n\n{requests}"},
]


for setting in ['4_4_easy', '4_4_hard', '9_9_easy', '9_9_hard']:
    with open(f"./{setting}/prompt.json", "w", encoding="utf-8") as f:
        json.dump(shot_dict, f, indent=4)


api_shot_dict = {}

api_shot_dict['zero_shot'] = [
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"}
]

api_shot_dict['two_shot'] = [
    {"role": "user", "content": f"{rules}\n\nExample Puzzle 1:\n\n{example1}\n\nSolution 1:\n\n{solution1}\n\nExample Puzzle 2:\n\n{example2}\n\nSolution 2:\n\n{solution2}\n\nNow please solve the following puzzle:\n\n{example}\n\n{requests}"}
]


for setting in ['4_4_easy', '4_4_hard', '9_9_easy', '9_9_hard']:
    with open(f"./{setting}/prompt_api.json", "w", encoding="utf-8") as f:
        json.dump(api_shot_dict, f, indent=4)