import os
import json

rules = '''
An acrostic puzzle is a word game that consists of two main parts: a grid and a set of clues. The objective is to fill in the grid with letters from the answers to the clues, forming a hidden quotation or sentence. Here's a detailed explanation of how the game works:
1. Understand the Grid Layout
The grid is made up of numbers, hashtags ("#"), and punctuations. Hashtag ("#") acts as space separator between words. Each number corresponds to a specific letter in a word. The hidden quotation or sentence is formed by filling in the grid with the correct letters.

2. Read the Clues
Each clue is made up of a string of numbers and a clue text. The clue text is usually a short definition, synonym or phrase related to the answer word or phrase. The number of words and letters of the answer are given in brackets after the clue text. The string of numbers provided indicates the specific position of each letter of the answer in the grid.

3. Solve the Puzzle
Think of answers that fit the clue and match the number of words and letters specified. For example, if a clue says "Animal that barks (1 word, 3 letters)", you might guess "DOG" because it has 3 letters. When getting the answer, double-check that it fits the clue, both in meaning and the number of letters. If you make a mistake, just try again! As you fill in the letters of answers, these letters can be part of the hidden word in the grid, thus providing hints for the left letters of this word. This mechanism can help both verify your answers and solve difficult clues. For example, if the puzzle looks like this: "... # 5 6 7 # ..." and you have already got {5: 'A', 7: 'D'}, you can guess that the word is "AND" and get {6: 'N'} without its corresponding clue. Don’t be afraid to skip a tough clue and come back to it later. As you fill in the grid, you will reveal part of the hidden words. Use this information to help solve the remaining clues.
'''
rules = rules.strip()

requests = '''
Please solve the Acrostic Puzzle according to the provided rules. Please also follow the requests below to present your analysis and solutions:
1. Analyze the clue carefully to understand its meaning and potential word associations. Be open to the possibility of wordplay or puns that might lead to unexpected solutions. The filled-in words will help you infer the answers to the subsequent clues.
2. Provide the final answer for each clue. The final answer should be presented after "Answer:". 
3. Create a python dictionary mapping in a single line that links the number positions in the clues to the corresponding letters in the final answer. Note that the blank spaces and punctuation should be omitted in the mapping. The python dictionary should be presented after "Mapping:".
4. Please wrap all the analysis of each clue with <n-CLUE> and </n-CLUE> tags, where n is the label of the clue. For example, the first clue should be wrapped with <A-CLUE> and </A-CLUE> tags. The second clue should be wrapped with <B-CLUE> and </B-CLUE> tags, and so on.
5. After solving all the clues, please gather all the mappings and place them in order between the <Answer> and </Answer> tags. The gathered mapping should look like {'1': 'LETTER1', '2': 'LETTER2', ...}.
6. Please generate your response without redundant and repeating content.
'''
requests = requests.strip()



# 1019
example1 = '''
Here is an acrostic puzzle:
GRID:
1 2 3 4 5 # 6 7 8 9 10 # 11 12 # 13 14 15 # 16 17 18 19 20 # 21 22 23 24 25 26 27 28 29 , 30 31 32 # 33 34 35 # 36 37 38 # 39 40 41 42 43 # 44 45 46 47 # 48 49 50 # 51 52 53 54 55 56 57 # 58 59 60 61 # 62 63 64 65 66 67 68 69 70 # 71 72 73 74 # 75 # 76 77 78 79 # 80 81 82 # 83 84 85 # 86 87 88 89 90 91 92 .

CLUES:
A
58 86 92 3 60 49 57 46 70 40
Cosmetics magnate (3 words, 10 letters)
B
52 34 44 54 84 67 11 36 25 18 62
Nonphysical assets (1 word, 11 letters)
C
76 45 35 88 56 81 43 41 68 71
Religious schools of opinion (1 word, 10 letters)
D 
48 37 16 24 82 85 30 63 73
Cancer stick (1 word, 9 letters)
E
10 32 2 74 22 23 75 79 39 5 64
Establish a home base (1 word, 11 letters)
F
59 9 14 69 83 53 28
"____ is only a bench covered in velvet" (quote by Napoleon) (2 words, 7 letters)
G
55 26 38 31 20 21 87 91 6
___ up (became less serious) (1 word, 9 letters)
H
4 17 61 65 13 90 77 29
Rest (1 word, 8 letters)
I
33 80 51 15 66 27 7 12
Infractions (1 word, 8 letters)
J
1 19 50 72 8 89 47 78 42
Whisky-vermouth cocktail (1 word, 9 letters)
'''
example1 = example1.strip()

solution1_with_ref = '''
Let's start solving the acrostic puzzle step by step.

<A-CLUE>
A
58 86 92 3 60 49 57 46 70 40
Cosmetics magnate (3 words, 10 letters)

The clue "Cosmetics magnate" suggests a well-known figure in the beauty industry, likely a founder or prominent leader of a cosmetics company, and the answer is "Estée Lauder." However, "Estée Lauder" has only two words, so it doesn't fit the clue's requirement of three words. Perhaps I need to look at other clues for now.
</A-CLUE>

<B-CLUE>
B
52 34 44 54 84 67 11 36 25 18 62
Nonphysical assets (1 word, 11 letters)

The clue "Nonphysical assets" refers to intangible items that hold value but have no physical form. The answer is "Intangibles."
Answer: INTANGIBLES.
Mapping: {'52': 'I', '34': 'N', '44': 'T', '54': 'A', '84': 'N', '67': 'G', '11': 'I', '36': 'B', '25': 'L', '18': 'E', '62': 'S'}
</B-CLUE>

<C-CLUE>
C
76 45 35 88 56 81 43 41 68 71
Religious schools of opinion (1 word, 10 letters)

The clue "Religious schools of opinion" suggests a broad study or system of religious beliefs, aptly encapsulated by the term "theologies," which refers to the systematic and comprehensive study of concepts of God and religious beliefs.
Answer: THEOLOGIES.
Mapping: {'76': 'T', '45': 'H', '35': 'E', '88': 'O', '56': 'L', '81': 'O', '43': 'G', '41': 'I', '68': 'E', '71': 'S'}
</C-CLUE>

<D-CLUE>
D 
48 37 16 24 82 85 30 63 73
Cancer stick (1 word, 9 letters)

The term "cancer stick" colloquially refers to a cigarette, highlighting its well-known health risks due to its association with causing cancer.
Answer: CIGARETTE.
Mapping: {'48': 'C', '37': 'I', '16': 'G', '24': 'A', '82': 'R', '85': 'E', '30': 'T', '63': 'T', '73': 'E'}
</D-CLUE>
'''

solution1 = '''
Let's start solving the acrostic puzzle step by step.

<A-CLUE>
A
58 86 92 3 60 49 57 46 70 40
Cosmetics magnate (3 words, 10 letters)

The clue "Cosmetics magnate" succinctly encapsulates Mary Kay Ash's pioneering role in establishing a direct sales empire in the beauty industry.
Answer: MARYKAYASH.
Mapping: {'58': 'M', '86': 'A', '92': 'R', '3': 'Y', '60': 'K', '49': 'A', '57': 'Y', '46': 'A', '70': 'S', '40': 'H'}
</A-CLUE>

<B-CLUE>
B
52 34 44 54 84 67 11 36 25 18 62
Nonphysical assets (1 word, 11 letters)

"Nonphysical assets" aptly refers to intangibles, highlighting assets like intellectual property and goodwill that lack physical form but possess significant business value.
Answer: INTANGIBLES.
Mapping: {'52': 'I', '34': 'N', '44': 'T', '54': 'A', '84': 'N', '67': 'G', '11': 'I', '36': 'B', '25': 'L', '18': 'E', '62': 'S'}
</B-CLUE>

<C-CLUE>
C
76 45 35 88 56 81 43 41 68 71
Religious schools of opinion (1 word, 10 letters)

The clue "Religious schools of opinion" suggests a broad study or system of religious beliefs, aptly encapsulated by the term "theologies," which refers to the systematic and comprehensive study of concepts of God and religious beliefs.
Answer: THEOLOGIES.
Mapping: {'76': 'T', '45': 'H', '35': 'E', '88': 'O', '56': 'L', '81': 'O', '43': 'G', '41': 'I', '68': 'E', '71': 'S'}
</C-CLUE>

<D-CLUE>
D 
48 37 16 24 82 85 30 63 73
Cancer stick (1 word, 9 letters)

The term "cancer stick" colloquially refers to a cigarette, highlighting its well-known health risks due to its association with causing cancer.
Answer: CIGARETTE.
Mapping: {'48': 'C', '37': 'I', '16': 'G', '24': 'A', '82': 'R', '85': 'E', '30': 'T', '63': 'T', '73': 'E'}
</D-CLUE>

<E-CLUE>
E
10 32 2 74 22 23 75 79 39 5 64
Establish a home base (1 word, 11 letters)

The clue "Establish a home base" succinctly encapsulates the term "headquarter" as it embodies the creation of a central location for operations or management.
Answer: HEADQUARTER.
Mapping: {'10': 'H', '32': 'E', '2': 'A', '74': 'D', '22': 'Q', '23': 'U', '75': 'A', '79': 'R', '39': 'T', '5': 'E', '64': 'R'}
</E-CLUE>

<F-CLUE>
F
59 9 14 69 83 53 28
"____ is only a bench covered in velvet" (quote by Napoleon) (2 words, 7 letters)

The phrase "a throne is only a bench covered in velvet" reflects Napoleon's belief that power is constructed and the majesty of a throne derives merely from its perception and decoration.
Answer: ATHRONE.
Mapping: {'59': 'A', '9': 'T', '14': 'H', '69': 'R', '83': 'O', '53': 'N', '28': 'E'}
</F-CLUE>

<G-CLUE>
G
55 26 38 31 20 21 87 91 6
___ up (became less serious) (1 word, 9 letters)

The clue suggests a shift towards a less serious or more carefree state, which is succinctly captured by the word "lightened," indicating a reduction in weight or severity.
Answer: LIGHTENED.
Mapping: {'55': 'L', '26': 'I', '38': 'G', '31': 'H', '20': 'T', '21': 'E', '87': 'N', '91': 'E', '6': 'D'}
</G-CLUE>

<H-CLUE>
H
4 17 61 65 13 90 77 29
Rest (1 word, 8 letters)

The word "breather" suggests a short break or moment of rest, aligning well with the concept of a "rest" in the context of taking a pause or catching one's breath.
Answer: BREATHER.
Mapping: {'4': 'B', '17': 'R', '61': 'E', '65': 'A', '13': 'T', '90': 'H', '77': 'E', '29': 'R'}
</H-CLUE>

<I-CLUE>
I
33 80 51 15 66 27 7 12
Infractions (1 word, 8 letters)

The clue "Infractions" suggests violations or breaches of rules, and "offenses", an 8-letter word, directly aligns as it also means actions that break laws or rules.
Answer: OFFENSES.
Mapping: {'33': 'O', '80': 'F', '51': 'F', '15': 'E', '66': 'N', '27': 'S', '7': 'E', '12': 'S'}
</I-CLUE>

<J-CLUE>
J
1 19 50 72 8 89 47 78 42
Whisky-vermouth cocktail (1 word, 9 letters)

The clue suggests a cocktail made with whisky and vermouth. The answer "Manhattan" aligns with this description, as it's a classic cocktail primarily composed of whiskey and vermouth.
Answer: MANHATTAN.
Mapping: {'1': 'M', '19': 'A', '50': 'N', '72': 'H', '8': 'A', '89': 'T', '47': 'T', '78': 'A', '42': 'N'}
</J-CLUE>

Now let's gather all the mappings in order:
<Answer>
{'1': 'M', '2': 'A', '3': 'Y', '4': 'B', '5': 'E', '6': 'D', '7': 'E', '8': 'A', '9': 'T', '10': 'H', '11': 'I', '12': 'S', '13': 'T', '14': 'H', '15': 'E', '16': 'G', '17': 'R', '18': 'E', '19': 'A', '20': 'T', '21': 'E', '22': 'Q', '23': 'U', '24': 'A', '25': 'L', '26': 'I', '27': 'S', '28': 'E', '29': 'R', '30': 'T', '31': 'H', '32': 'E', '33': 'O', '34': 'N', '35': 'E', '36': 'B', '37': 'I', '38': 'G', '39': 'T', '40': 'H', '41': 'I', '42': 'N', '43': 'G', '44': 'T', '45': 'H', '46': 'A', '47': 'T', '48': 'C', '49': 'A', '50': 'N', '51': 'F', '52': 'I', '53': 'N', '54': 'A', '55': 'L', '56': 'L', '57': 'Y', '58': 'M', '59': 'A', '60': 'K', '61': 'E', '62': 'S', '63': 'T', '64': 'R', '65': 'A', '66': 'N', '67': 'G', '68': 'E', '69': 'R', '70': 'S', '71': 'S', '72': 'H', '73': 'E', '74': 'D', '75': 'A', '76': 'T', '77': 'E', '78': 'A', '79': 'R', '80': 'F', '81': 'O', '82': 'R', '83': 'O', '84': 'N', '85': 'E', '86': 'A', '87': 'N', '88': 'O', '89': 'T', '90': 'H', '91': 'E', '92': 'R'}
</Answer>
'''
solution1 = solution1.strip()


# 1118
example2 = '''
Here is an acrostic puzzle:
GRID:
1 2 # 3 4 5 # 6 7 8 # 9 10 11 12 13 14 # 15 16 17 18 # 19 20 # 21 22 # 23 24 25 ' 26 # 27 28 29 30 31 32 33 # 34 35 36 # 37 38 39 # 40 41 42 43 44 45 46 47 48 49 # 50 51 52 # 53 54 55 # 56 57 58 59 60 61 62 63 . 64 65 66 # 67 68 # 69 70 71 72 # 73 74 75 76 77 # 78 79 # 80 81 82 83 # 84 85 # 86 87 # 88 89 90 91 92 93 # 94 95 96 97 98 99 100 101 .

CLUES:
A
23 50 49 38 57 90 64 25
Role played by Julie Newmar and Halle Berry (1 word, 8 letters)
B
81 24 12 85 1 59 54
Foolish person (1 word, 7 letters)
C
99 8 26 36 82 60 30 84 75 10 86 41 46 3 93
Wolf-whistle target, usually (2 words, 15 letters)
D
77 68 56 44 97 79 15
Censure (1 word, 7 letters)
E
72 94 42 92 6 40 69 53 58 33
Advanced health care directive (2 words, 10 letters)
F
89 100 83 74 9 70 29
Join (2 words, 7 letters)
G
14 37 35 88 62 32 45
"I'll take that bet" (2 words, 7 letters)
H
16 18 96 47 21 87 52
Continued a subscription (1 word, 7 letters)
I
22 11 31 63 34 20 27 7 4 73
Husked items in the produce aisle (3 words, 10 letters)
J
43 19 78 5 98 66 28 67 48
Duck product (1 word, 9 letters)
K
55 61 13 2 65 101
"____ Night" (1 word, 6 letters)
L
76 39 80 91 51 95 71 17
Complicate (1 word, 8 letters)
'''
example2 = example2.strip()

solution2 = '''
Let's start solving the acrostic puzzle step by step.

<A-CLUE>
A
23 50 49 38 57 90 64 25
Role played by Julie Newmar and Halle Berry (1 word, 8 letters)

The clue "Role played by Julie Newmar and Halle Berry" refers to the character of Catwoman, as both actresses portrayed this iconic superhero/villain in different adaptations of the Batman series.
Answer: CATWOMAN.
Mapping: {'23': 'C', '50': 'A', '49': 'T', '38': 'W', '57': 'O', '90': 'M', '64': 'A', '25': 'N'}
</A-CLUE>

<B-CLUE>
B
81 24 12 85 1 59 54
Foolish person (1 word, 7 letters)

The clue "Foolish person" suggests a term that refers to someone lacking intelligence or judgment, and the answer "halfwit", a 7-letter word, fits this description as it denotes a person of limited mental capacity.
Answer: HALFWIT.
Mapping: {'81': 'H', '24': 'A', '12': 'L', '85': 'F', '1': 'W', '59': 'I', '54': 'T'}
</B-CLUE>

<C-CLUE>
C
99 8 26 36 82 60 30 84 75 10 86 41 46 3 93
Wolf-whistle target, usually (2 words, 15 letters)

The clue "Wolf-whistle target, usually" refers to a common phrase describing the typical target of a wolf whistle, often someone who is perceived as attractive, which leads to the final answer: "Attractive Woman".
Answer: ATTRACTIVEWOMAN.
Mapping: {'99': 'A', '8': 'T', '26': 'T', '36': 'R', '82': 'A', '60': 'C', '30': 'T', '84': 'I', '75': 'V', '10': 'E', '86': 'W', '41': 'O', '46': 'M', '3': 'A', '93': 'N'}
</C-CLUE>

<D-CLUE>
D
77 68 56 44 97 79 15
Censure (1 word, 7 letters)

The clue "Censure" suggests a word meaning to express strong disapproval or reprimand, and a 7-letter word that fits this definition is "Reproof".
Answer: REPROOF.
Mapping: {'77': 'R', '68': 'E', '56': 'P', '44': 'R', '97': 'O', '79': 'O', '15': 'F'}
</D-CLUE>

<E-CLUE>
72 94 42 92 6 40 69 53 58 33
Advanced health care directive (2 words, 10 letters)

An "advanced health care directive" is a legal document that outlines a person's preferences for medical treatment in case they become unable to communicate, and "Living Will" fits this definition as a two-word phrase with 10 letters in total.
Answer: LIVINGWILL.
Mapping: {'72': 'L', '94': 'I', '42': 'V', '92': 'I', '6': 'N', '40': 'G', '69': 'W', '53': 'I', '58': 'L', '33': 'L'}
</E-CLUE>

<F-CLUE>
F
89 100 83 74 9 70 29
Join (2 words, 7 letters)

Based on the clue "Join (2 words, 7 letters)" the final answer is likely "enter in" — a two-word phrase meaning to join or connect things together.
Answer: ENTERIN.
Mapping: {'89': 'E', '100': 'N', '83': 'T', '74': 'E', '9': 'R', '70': 'I', '29': 'N'}
</F-CLUE>

<G-CLUE>
G
14 37 35 88 62 32 45
"I'll take that bet" (2 words, 7 letters)

The clue "I'll take that bet" suggests someone accepting a wager or agreeing to a challenge, which leads to the answer "You’re on".
Answer: YOUREON.
Mapping: {'14': 'Y', '37': 'O', '35': 'U', '88': 'R', '62': 'E', '32': 'O', '45': 'N'}
</G-CLUE>

<H-CLUE>
H
16 18 96 47 21 87 52
Continued a subscription (1 word, 7 letters)

The clue "Continued a subscription" suggests the act of renewing or maintaining an ongoing subscription, leading to the answer "renewed".
Answer: RENEWED.
Mapping: {'16': 'R', '18': 'E', '96': 'N', '47': 'E', '21': 'W', '87': 'E', '52': 'D'}
</H-CLUE>

<I-CLUE>
I
22 11 31 63 34 20 27 7 4 73
Husked items in the produce aisle (3 words, 10 letters)

The clue "Husked items in the produce aisle" refers to items that have been husked, and "ears of corn" fits the description as a common produce item found in the aisle, typically husked to reveal the edible corn.
Answer: EARSOFCORN.
Mapping: {'22': 'E', '11': 'A', '31': 'R', '63': 'S', '34': 'O', '20': 'F', '27': 'C', '7': 'O', '4': 'R', '73': 'N'}
</I-CLUE>

<J-CLUE>
J
43 19 78 5 98 66 28 67 48
Duck product (1 word, 9 letters)

The clue "Duck product" refers to a product derived from ducks, and "eiderdown," a type of soft down feathers from the eider duck, fits the given length and the description of a duck-related product.
Answer: EIDERDOWN.
Mapping: {'43': 'E', '19': 'I', '78': 'D', '5': 'E', '98': 'R', '66': 'D', '28': 'O', '67': 'W', '48': 'N'}
</J-CLUE>

<K-CLUE>
K
55 61 13 2 65 101
"____ Night" (1 word, 6 letters)

The phrase "____ Night" likely refers to a commonly known expression or title that fits the pattern of a 6-letter word, which suggests "Silent Night," a famous Christmas carol.
Answer: SILENT.
Mapping: {'55': 'S', '61': 'I', '13': 'L', '2': 'E', '65': 'N', '101': 'T'}
</K-CLUE>

<L-CLUE>
L
76 39 80 91 51 95 71 17
Complicate (1 word, 8 letters)

The word "complicate" suggests something that makes a situation more complex, and the final answer, based on the clue of being 8 letters long, is likely "entangle".
Answer: ENTANGLE.
Mapping: {'76': 'E', '39': 'N', '80': 'T', '91': 'A', '51': 'N', '95': 'G', '71': 'L', '17': 'E'}
</L-CLUE>


Now let's gather all the mappings in order:
<Answer>
{'1': 'W', '2': 'E', '3': 'A', '4': 'R', '5': 'E', '6': 'N', '7': 'O', '8': 'T', '9': 'R', '10': 'E', '11': 'A', '12': 'L', '13': 'L', '14': 'Y', '15': 'F', '16': 'R', '17': 'E', '18': 'E', '19': 'I', '20': 'F', '21': 'W', '22': 'E', '23': 'C', '24': 'A', '25': 'N', '26': 'T', '27': 'C', '28': 'O', '29': 'N', '30': 'T', '31': 'R', '32': 'O', '33': 'L', '34': 'O', '35': 'U', '36': 'R', '37': 'O', '38': 'W', '39': 'N', '40': 'G', '41': 'O', '42': 'V', '43': 'E', '44': 'R', '45': 'N', '46': 'M', '47': 'E', '48': 'N', '49': 'T', '50': 'A', '51': 'N', '52': 'D', '53': 'I', '54': 'T', '55': 'S', '56': 'P', '57': 'O', '58': 'L', '59': 'I', '60': 'C', '61': 'I', '62': 'E', '63': 'S', '64': 'A', '65': 'N', '66': 'D', '67': 'W', '68': 'E', '69': 'W', '70': 'I', '71': 'L', '72': 'L', '73': 'N', '74': 'E', '75': 'V', '76': 'E', '77': 'R', '78': 'D', '79': 'O', '80': 'T', '81': 'H', '82': 'A', '83': 'T', '84': 'I', '85': 'F', '86': 'W', '87': 'E', '88': 'R', '89': 'E', '90': 'M', '91': 'A', '92': 'I', '93': 'N', '94': 'I', '95': 'G', '96': 'N', '97': 'O', '98': 'R', '99': 'A', '100': 'N', '101': 'T'}
</Answer>
'''
solution2 = solution2.strip()




example = "<example>"

shot_dict = {}

shot_dict['zero_shot'] = [
    {"role": "system", "content": "You are an expert acrostic solver."},
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"},
    {"role": "assistant", "content": f"Let's start solving the acrostic puzzle step by step."},
]



shot_dict['two_shot'] = [
    {"role": "system", "content": "You are an expert acrostic solver."},
    {"role": "user", "content": f"{rules}\n\n{example1}\n\n{requests}"},
    {"role": "assistant", "content": solution1},
    {"role": "user", "content": f"{example2}\n\n{requests}"},
    {"role": "assistant", "content": solution2},
    {"role": "user", "content": f"{example}\n\n{requests}"},
    {"role": "assistant", "content": f"Let's start solving the acrostic puzzle step by step."},
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

