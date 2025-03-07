import os
import json

rules = '''
A Drop Quote Puzzle consists of two parts: a grid and a set of given letters that "drop" into specific columns of the grid. The goal is to fill in the grid with a meaningful quote or statement.

Key Features:
    Grid Layout:
        The grid contains numbers, "#" symbols (representing spaces between words), and already placed punctuation.
        Words may break across lines, starting at the end of one line and continuing to the beginning of the next. Words end only at "#" blocks or the end of the puzzle.
    Given Letters:
        The letters are organized by column number and are given in alphabetical order. These letters need to be placed into the grid.
        Each letter drops into a specific column, and your task is to identify the correct placement for each letter based on the grid structure. Do not simply fill the columns in the order they are listed. Instead, consider where each letter fits contextually within the puzzle to form words that make sense in the final quote or statement.

Rules:
    The "#" symbols indicate where spaces between words should be.
    Column labels (e.g., Column 1: O T) indicate the letters that will drop into the grid for Column 1, listed in alphabetical order. For example, in Column 1, the letters "O" and "T" must be placed in the appropriate grid positions.
    Fill the grid with the letters in such a way that they form a meaningful statement or quotation.


'''
rules = rules.strip()

requests = '''
Please solve the Drop Quote Puzzle according to the provided rules. Please also follow the requests below to present your analysis and solutions:
1. Isolated boxes are usually, but not always, the words A or I. Similarly, when you have a 2-letter word, see what words you can make and then see what letters that leaves you over with for other lines. The most common 2-letter words are: OF, TO, IN, IT, IS, BE, AS, AT, SO, WE, HE, BY, OR, ON, DO, IF, ME, MY, UP, AN, GO, NO, US, AM.
2. The letters in a column with fewer letters can be placed quickly by noticing which letters must be consonants and vowels, or by eliminating the possibility of a letter appearing in a certain spot.
3. If you have an uncommon letter such as a J, K, Q, X, or Z, think about what letters might go before or after it. Similarly, look for common consonant pairs such as TH, ND, NT, ST, as well as doubled letters.
4. Be alert for common prefixes such as DE-, MIS-, RE-, and UN-, as well as common suffixes such as -ABLE, -ED, -ING, -LY, -NESS, and -TION.
5. Every time you fill in a letter, it means that you've eliminated some letters that can go elsewhere. Frequently, this means that you can immediately fill in some additional letters.
6. Please provide step by step analysis and present the final answer as the same json format of the input grid. Wrapping the final answer in <Answer> and </Answer> tags.
7. Please generate your response without redundant and repeating content.
'''
requests = requests.strip()


example1 = '''
Here is a drop quote puzzle:
[['1', '2', '3', '4', '#', '6', '7'],
 ['#', '2', '3', '4', '5', '6', '.']]

Column 1: T
Column 2: I M
Column 3: M O
Column 4: E N
Column 5: E
Column 6: I Y
Column 7: S
'''
example1 = example1.strip()

solution1 = '''
Let's start solving the sudoku puzzle step by step.

We first focus on Columns with single letters:
    "T" for Row 1, Column 1
    "E" for Row 2, Column 5
    "S" for Row 1, Column 7

Then, we check the word ['6', '7'] in Row 1:
    The candidates for Column 6 are "I" and "Y", and for Column 7, it is "S". The only word that fits is "IS". So, place "I" in Row 1, Column 6 and "Y" in Row 2, Column 6.

Let's check the current grid:
[['T', '2', '3', '4', '#', 'I', 'S'],
 ['#', '2', '3', '4', 'E', 'Y', '.']]

For Column 2 (I M):
    Since "I" is more likely come after "T", we can place "I" in Row 1, Column 2 and "M" in Row 2, Column 2.

Updated Grid:
[['T', 'I', '3', '4', '#', 'I', 'S'],
 ['#', 'M', '3', '4', 'E', 'Y', '.']]

For Column 3 (M O):
    Row 1 now contains "TI", and Row 2 starts with "M", which suggests that "M" should be placed in Row 1, Column 3 and "O" in Row 2, Column 3.

Updated Grid:
[['T', 'I', 'M', '4', '#', 'I', 'S'],
 ['#', 'M', 'O', '4', 'E', 'Y', '.']]

For Column 4 (E N):
    We can infer that the word in Row 1 is "TIME" and in Row 2 is "MONEY". So, place "E" in Row 1, Column 4 and "N" in Row 2, Column 4.

Now we get the hidden quote:
"TIME IS MONEY"

Here is the final answer gird:
<Answer>
[['T', 'I', 'M', 'E', '#', 'I', 'S'],
 ['#', 'M', 'O', 'N', 'E', 'Y', '.']]
</Answer>
'''
solution1 = solution1.strip()


example2 = '''
Here is a drop quote puzzle:
[['1', '2', '#', '4', '5', '#', '7', '8', '#', '10'],
 ['1', '2', '#', '4', '5', '#', '7', '8', '.', '#']]

Column 1: O T
Column 2: O T
Column 4: B T
Column 5: E O
Column 7: B O
Column 8: E R
Column 10: N
'''
example2 = example2.strip()

solution2 = '''
Let's start solving the sudoku puzzle step by step.

Start with Column 10 (N):
    The only letter for Column 10 is "N", which will fit into the grid's placeholder at Row 1, Column 10. So, place "N" in that position.

Column 1 (O T) and Column 2 (O T):
    ['1', '2'] in Row 1 forms a single word. Considering the combination of "O" and "T", the only valid word that fits is "TO". So, place "T" in Row 1, Column 1 and "O" in Row 1, Column 2. Similarly, ["10", "1", "2"] crosses Row 1 and Row 2 forming the word "NOT". So, place "O" in Row 2, Column 1 and "T" in Row 2, Column 2.

Column 4 (B T) and Column 5 (E O):
    ["4", "5"] in Row 1 and Row 2 constructs two words. The valid words should be "BE" and "TO". Since the word in ['1', '2'] in Row 1 is "TO", we should place "BE" in Row 1, Column 4 and Row 1, Column 5, "TO" in Row 2, Column 4 and Row 2, Column 5.

Check the current grid:
[['T', 'O', '#', 'B', 'E', '#', '7', '8', '#', 'N'],
 ['O', 'T', '#', 'T', 'O', '#', '7', '8', '.', '#']]

Now, reading through this arrangement, the most likely quote that forms is:
"TO BE OR NOT TO BE"

We further check the remaining columns Column 7 (B O) and Column 8 (E R):
    ["7", "8"] in Row 1 and Row 2 can form the words "OR" and "BE". This fits the quote we have identified.

Column 7 (B O) and Column 8 (E R):
    ["7", "8"] in Row 1 and Row 2 constructs two words. The valid words should be "BE" and "OR". So, place "B" in Row 1, Column 7, "E" in Row 1, Column 8, "O" in Row 2, Column 7, and "R" in Row 2, Column 8.

Here is the final answer:
<Answer>
[['T', 'O', '#', 'B', 'E', '#', 'O', 'R', '#', 'N'],
 ['O', 'T', '#', 'T', 'O', '#', 'B', 'E', '.', '#']]
</Answer>
'''
solution2 = solution2.strip()


example = "<example>"

shot_dict = {}


shot_dict['zero_shot'] = [
    {"role": "system", "content": "You are an expert drop quote puzzle solver."},
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"},
]


shot_dict['two_shot'] = [
    {"role": "system", "content": "You are an expert drop quote puzzle solver."},
    {"role": "user", "content": f"{rules}\n\n{example1}\n\n{requests}"},
    {"role": "assistant", "content": solution1},
    {"role": "user", "content": f"{example2}\n\n{requests}"},
    {"role": "assistant", "content": solution2},
    {"role": "user", "content": f"{example}\n\n{requests}"},
]


for setting in ['easy', 'hard']:
    with open(f"./{setting}/prompt.json", "w", encoding="utf-8") as f:
        json.dump(shot_dict, f, indent=4)

api_shot_dict = {}

api_shot_dict['zero_shot'] = [
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"}
]

api_shot_dict['two_shot'] = [
    {"role": "user", "content": f"{rules}\n\nExample Puzzle 1:\n\n{example1}\n\nSolution 1:\n\n{solution1}\n\nExample Puzzle 2:\n\n{example2}\n\nSolution 2:\n\n{solution2}\n\nNow please solve the following puzzle:\n\n{example}\n\n{requests}"}
]


for setting in ['easy', 'hard']:
    with open(f"./{setting}/prompt_api.json", "w", encoding="utf-8") as f:
        json.dump(api_shot_dict, f, indent=4)