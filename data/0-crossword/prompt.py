import os
import json

rules = '''
A crossword puzzle is a word game that consists of a grid, with clues given for words that fit into the grid both across (horizontally) and down (vertically). Your goal is to fill in the grid with words based on the clues provided. Here's a detailed explanation of how the game works:
1. Understand the Grid Layout
The grid is made up of numbers, hashtags ("#"), and question marks ("?"). Hashtag ("#") acts as separator between words. Number represents the starting points of Across and Down words. Question mark ("?") represents part of words but don't start a new word.

2. Read the Clues
Clues are provided for each word to be filled into the grid, split into two categories: Across clues (these are for words that go horizontally in the grid) and Down clues (these are for words that go vertically in the grid). The number in brackets after the clue indicates the length of the word. Clues are often short definitions, synonyms, or phrases related to the word. Some clues may involve wordplay, anagrams, or puns, depending on the puzzle's difficulty and style.

3. Solve the Puzzle
Think of words that fit the clue and match the number of letters specified. For example, if a clue says "Animal that barks (3)", you might guess "DOG" because it has 3 letters. When getting the answer, double-check that it fits the clue, both in meaning and the number of letters. If you make a mistake, just try again! As you fill in answers, they will help you solve other clues, since words intersect and share letters in the grid. This cross-checking mechanism helps in verifying correct answers.
'''
rules = rules.strip()

requests = '''
Please solve the Crossword Puzzle according to the provided rules. Please also follow the requests below to present your analysis and solutions:
1. Analyze each clue carefully to understand its meaning and potential word associations. Be open to the possibility of wordplay or puns that might lead to unexpected solutions. The filled-in words will help you infer the answers to the subsequent clues.
2. Provide the final answer for each clue. The final answer should be presented after "Answer:".
3. Please wrap all the analysis of each clue with <n-Across> and </n-Across> or <n-Down> and </n-Down> tags, where n is the clue number. For example, the Across clue 1 should be wrapped with <1-Across> and </1-Across> tags. The Down clue 1 should be wrapped with <1-Down> and </1-Down> tags, and so on.
4. After solving all the clues, please summarize all the answer words in following json format and warp them with <Answer> and </Answer> tags:
<Answer>
{"1-Across": "ANSWER1", "2-Across": "ANSWER2", ... "1-Down": "ANSWER3", "2-Down": "ANSWER4", ...}
</Answer>
5. Please generate your response without redundant and repeating content.
'''
requests = requests.strip()


example1 = '''
Here is a crossword puzzle:
GRID:
# 1 2 3 4
5 ? ? ? ?
6 ? ? ? ?
7 ? ? ? ?
# 8 ? ? #

CLUES:
Across:
1 "More ___ you'll ever know" (4)
5 Divine favor, in Christianity (5)
6 Sisters who might be sitters (5)
7 Portly-sounding beer (5)
8 Cool and stylish (3)

Down:
1 "The ___ will set you free. But not until it is finished with you": David Foster Wallace (5)
2 Capital of Vietnam (5)
3 Misbehave (5)
4 Prepare for a new baby, say (4)
5 Fuel for some stoves (3)
'''
example1 = example1.strip()

solution1 = '''
Let's start solving the crossword puzzle step by step.

Across Clues:

<1-Across>
1-Across: "More ___ you'll ever know" (4)

The clue is a reference to a popular phrase, "More than you'll ever know," suggesting the answer is "than".
Answer: THAN.
</1-Across>

<5-Across>
5-Across: Divine favor, in Christianity (5)

The clue refers to a concept of God's blessing or grace, and the answer is "grace".
Answer: GRACE.
</5-Across>

<6-Across>
6-Across: Sisters who might be sitters (5)

The clue plays on the dual meaning of "sisters" as female relatives and "sitters" as those who might care for children, leading to the answer "aunts."
Answer: AUNTS.
</6-Across>

<7-Across>
7-Across: Portly-sounding beer (5)

The clue "Portly-sounding beer" is a play on words where "portly" refers to something stout (a synonym for fat), and "beer" refers to the type of drink, leading to the answer "stout."
Answer: STOUT.
</7-Across>

<8-Across>
8-Across: Cool and stylish (3)

The clue "Cool and stylish" suggests a slang term for something fashionable or trendy. The answer is likely "hip".
Answer: HIP.
</8-Across>


Down Clues:

<1-Down>
1-Down: "The ___ will set you free. But not until it is finished with you": David Foster Wallace (5)

This quote from David Foster Wallace refers to the transformative yet challenging nature of truth. The answer is "truth".
Answer: TRUTH.
</1-Down>

<2-Down>
2-Down: Capital of Vietnam (5)

The capital of Vietnam is Hanoi.
Answer: HANOI.
</2-Down>

<3-Down>
3-Down: Misbehave (5)

For a 5-letter answer to "Misbehave," the likely solution is "act up."
Answer: ACTUP.
</3-Down>

<4-Down>
4-Down: Prepare for a new baby, say (4)

This clue suggests an action associated with getting ready for a new baby, and the answer is likely "nest" (as in "nesting," the common term for preparing for a new baby).
Answer: NEST.
</4-Down>

<5-Down>
5-Down: Fuel for some stoves (3)

This clue refers to a type of fuel commonly used in stoves, and the answer is likely "gas".
Answer: GAS.
</5-Down>

Here is the final grid after finishing all the clues:
<Answer>
{"1-Across": "THAN", "5-Across": "GRACE", "6-Across": "AUNTS", "7-Across": "STOUT", "8-Across": "HIP", "1-Down": "TRUTH", "2-Down": "HANOI", "3-Down": "ACTUP", "4-Down": "NEST", "5-Down": "GAS"}
</Answer>
'''
solution1 = solution1.strip()


example2 = '''
Here is a crossword puzzle:
GRID:
1 2 3 4 ?
5 ? ? ? #
6 ? ? ? 7
8 ? ? ? ?
# # 9 ? ?

CLUES:
Across:
1 Rides for brides (5)
5 "Back ___ hour" (shop sign) (4)
6 Comedy sketches by the campfire (5)
8 Letter-shaped opening (5)
9 James Bond, for one (3)

Down:
1 Tilt to one side (4)
2 Tattoo artist's supply (4)
3 Sends off (5)
4 Leading the field (5)
7 Hog haven (3)
'''
example2 = example2.strip()

solution2 = '''
Let's start solving the crossword puzzle step by step.

Across Clues:

<1-Across>
1-Across: Rides for brides (5)

The clue "Rides for brides" suggests a form of transportation typically associated with weddings, and the answer "limos" is a common abbreviation for "limousines," which are often used as elegant vehicles for brides on their wedding day.
Answer: LIMOS.
</1-Across>

<5-Across>
5-Across: "Back ___ hour" (shop sign) (4)

The clue "Back ___ hour" (shop sign) suggests a common phrase used on signs indicating a temporary absence, where "back in an hour" fits the pattern, and the answer shoud be "INAN".
Answer: INAN.
</5-Across>

<6-Across>
6-Across: Comedy sketches by the campfire (5)

"Comedy sketches" is the definition, and "by the campfire" hints at a casual, informal setting where short performances or sketches might take place, such as around a campfire. The answer should be "Skits" which are brief comedic performances.
Answer: SKITS.
</6-Across>

<8-Across>
8-Across: Letter-shaped opening (5)

The clue "Letter-shaped opening" suggests a type of opening or space that is shaped like a letter, and the answer "TSLOT" refers to a T-shaped opening, commonly used in engineering and construction.
Answer: TSLOT.
</8-Across>

<9-Across>
9-Across: James Bond, for one (3)

James Bond is a famous spy, and the term "for one" refers to a spy being an example of such a character.
Answer: SPY.
</9-Across>


Down Clues:

<1-Down>
1-Down: Tilt to one side (4)

The clue "Tilt to one side" suggests a word meaning to lean or incline in a specific direction, and the answer is likely "list" — a verb that means to tilt or lean to one side, often used when describing the slant of an object or surface.
Answer: LIST.
</1-Down>

<2-Down>
2-Down: Tattoo artist's supply (4)

The clue "Tattoo artist's supply" refers to an essential item used by a tattoo artist. A tattoo artist's primary supply for creating tattoos, as ink is the substance used to mark the skin. The answer is likely "inks".
Answer: INKS.
</2-Down>

<3-Down>
3-Down: Sends off (5)

The clue "Sends off" suggests an action of dispatching or transmitting something, where "mails" are both the noun for postal items and the verb meaning to send something.
Answer: MAILS.
</3-Down>

<4-Down>
4-Down: Leading the field (5)

The clue "Leading the field" suggests being at the forefront or in a dominant position, which corresponds to being "on top" of something.
Answer: ONTOP.
</4-Down>

<7-Down>
7-Down: Hog haven (3)

The clue "Hog haven" refers to a place where pigs (hogs) live, and "sty" is a common term for a pig's pen or shelter.
Answer: STY.
</7-Down>

Here is the final grid after finishing all the clues:
<Answer>
{"1-Across": "LIMOS", "5-Across": "INAN", "6-Across": "SKITS", "8-Across": "TSLOT", "9-Across": "SPY", "1-Down": "LIST", "2-Down": "INKS", "3-Down": "MAILS", "4-Down": "ONTOP", "7-Down": "STY"}
</Answer>
'''
solution2 = solution2.strip()



example = "<example>"

shot_dict = {}

shot_dict['zero_shot'] = [
    {"role": "system", "content": "You are an expert crossword solver."},
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"},
    {"role": "assistant", "content": f"Let's start solving the crossword puzzle step by step."},
]

shot_dict['two_shot'] = [
    {"role": "system", "content": "You are an expert crossword solver."},
    {"role": "user", "content": f"{rules}\n\n{example1}\n\n{requests}"},
    {"role": "assistant", "content": solution1},
    {"role": "user", "content": f"{example2}\n\n{requests}"},
    {"role": "assistant", "content": solution2},
    {"role": "user", "content": f"{example}\n\n{requests}"},
    {"role": "assistant", "content": "Let's start solving the crossword puzzle step by step."},
]



for size in ["5_5", "10_10", "15_15"]:
    with open(f"./{size}/prompt.json", "w", encoding="utf-8") as f:
        json.dump(shot_dict, f, indent=4)


api_shot_dict = {}

api_shot_dict['zero_shot'] = [
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"}
]

api_shot_dict['two_shot'] = [
    {"role": "user", "content": f"{rules}\n\nExample Puzzle 1:\n\n{example1}\n\nSolution 1:\n\n{solution1}\n\nExample Puzzle 2:\n\n{example2}\n\nSolution 2:\n\n{solution2}\n\nNow please solve the following puzzle:\n\n{example}\n\n{requests}"}
]

for size in ["5_5", "10_10", "15_15"]:
    with open(f"./{size}/prompt_api.json", "w", encoding="utf-8") as f:
        json.dump(api_shot_dict, f, indent=4)
