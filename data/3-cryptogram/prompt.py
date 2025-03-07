import os
import json

rules = '''
A cryptogram is a type of puzzle that consists of a short piece of encrypted text. You will decode a cryptogram that uses a simple substitution cipher, where each letter in the message has been substituted with another letter. The goal is to decode the hidden quote along with its author's name. You may use the author's name to help reduce the difficulty of the decoding process by focusing on common words, letter patterns, and stylistic cues from the author.
'''
rules = rules.strip()

requests = '''
Please follow these steps to solve the Cryptogram:
1. Use the author's name as a clue: Knowing the author's name can help you predict common words or letter combinations typical for this author. For instance, if the author is "Shakespeare," you might anticipate archaic or common Shakespearean phrases (like "thou," "thee," etc.).
2. Analyze the cryptogram: Look at the frequency of letters and common letter patterns, such as double letters or common suffixes and prefixes. Focus on the parts of the cryptogram that seem to match the author's typical writing style or famous phrases.
3. Map common words: If you recognize a word in the cryptogram that matches the author's typical vocabulary, substitute letters based on that.
4. Make educated guesses: Use common English words (such as "the," "and," "of," etc.) and letter pairs (like "th," "he," "in", etc.) to identify possible substitutions. If one assumption doesn't work, try another.
5. Verification: After generating the decoded message, check if the quote and the author's name make logical sense. If needed, revisit the assumptions and adjust the letter mappings.
6. Please provide step by step analysis and create a python dictionary mapping of the fully substitutioin wrapping it between <Mapping> and </Mapping> tag.
7. Please provide the final decoded quote and wrap it between <Answer> and </Answer> tag.
8. Please generate your response without redundant and repeating content.
'''
requests = requests.strip()



example1 = '''
Think step-by-step to decipher the cryptogram:
VOBB XSDO QK IOFFOU FGHD VOBB KHQX.
— Benjamin Franklin
'''
example1 = example1.strip()


solution1 = '''
Let's start solving the cryptogram puzzle step by step.

Step 1: Use the Author's Name as a Clue Benjamin Franklin is known for his concise and wise sayings. Recognizing his style helps anticipate common structures and themes, such as practical advice or moral lessons.

Step 2: Analyze the Cryptogram The cryptogram is:

VOBB XSDO QK IOFFOU FGHD VOBB KHQX. -Benjamin Franklin
Notable features:

"VOBB" appears twice, suggesting a common word with double letters.
The structure of the sentence hints at a proverb or a well-known quote.

Step 3: Map Common Words Assuming "VOBB" is a common four-letter word with double letters, "WELL" is a plausible match:
V = W
O = E
B = L

Step 4: Make Educated Guesses Applying the initial mapping:
"XSDO" could be "DONE":
X = D
S = O
D = N
O = E
"QK" likely translates to "IS":
Q = I
K = S
"IOFFOU" fits "BETTER":
I = B
F = T
U = R
"FGHD" corresponds to "THAN":
F = T
G = H
H = A
D = N
"KHQX" translates to "SAID":
K = S
H = A
Q = I
X = D

Step 5: Verification Substituting all mapped letters:
WELL DONE IS BETTER THAN WELL SAID. -Benjamin Franklin
This is a coherent and well-known Franklin quote, confirming the accuracy of the mapping.

Mapping:
<Mapping>
{ "V": "W", "O": "E", "B": "L", "X": "D", "S": "O", "D": "N", "Q": "I", "K": "S", "I": "B", "F": "T", "U": "R", "G": "H", "H": "A"}
</Mapping>

Answer:
<Answer>
Well done is better than well said.
-Benjamin Franklin
</Answer>
'''
solution1 = solution1.strip()


example2 = '''
Think step-by-step to decipher the cryptogram:
NV CQ, VU JVN NV CQ, NIMN WF NIQ SKQFNWVJ.
— William Shakespeare
'''
example2 = example2.strip()

solution2 = '''
Let's start solving the cryptogram puzzle step by step.

Step-by-Step Decryption
    Recognizing known phrases:
        The structure "NV CQ" looks like it could map to the famous phrase "TO BE" from the well-known Shakespearean line, "TO BE, OR NOT TO BE, THAT IS THE QUESTION."

Mapping the first part:
    From the earlier analysis, we know:
        "NV CQ" = "TO BE"
        So, "N" = "T", "V" = "O", "C" = "B", and "Q" = "E".

Decoding the second part:
    The next part is "VU JVN NV CQ":
        "VU" is guessed as "OR" from the famous phrase.
        "J" is mapped to "N", "V" is "O", and "U" is "R".
        The rest of "JVN" maps to "NOT":
                "J" = "N", "V" = "O", "N" = "T".
        "NV CQ" is already decoded as "TO BE".
        So, "VU JVN NV CQ" = "OR NOT TO BE".

Decoding the third part:
    "NIMN WF NIQ SKQFNWVJ" needs to be deciphered now.
        "NIMN" = "THAT":
            "N" = "T", "I" = "H", "M" = "A", "N" = "T".
        "WF" = "IS":
            "W" = "I", "F" = "S".
        "NIQ" = "THE":
            "N" = "T", "I" = "H", "Q" = "E".
        "SKQFNWVJ" = "QUESTION":
            "S" = "Q", "K" = "U", "Q" = "E", "F" = "S", "N" = "T", "W" = "I", "V" = "O", "J" = "N".

Final Decoded Message:
The cryptogram "NV CQ, VU JVN NV CQ, NIMN WF NIQ SKQFNWVJ" decodes to:

"TO BE, OR NOT TO BE, THAT IS THE QUESTION."

This is a famous line from William Shakespeare's Hamlet.

Mapping:
<Mapping>
{"N": "T", "V": "O", "C": "B", "Q": "E", "U": "R", "J": "N", "I": "H", "M": "A", "W": "I", "S": "Q", "K": "U", "F": "S"}
</Mapping>

Answer:
<Answer>
TO BE, OR NOT TO BE, THAT IS THE QUESTION.
— William Shakespeare
</Answer>
'''
solution2 = solution2.strip()



example = "<example>"

shot_dict = {}


shot_dict['zero_shot'] = [
    {"role": "system", "content": "You are an expert cryptogram solver."},
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"},
]



shot_dict['two_shot'] = [
    {"role": "system", "content": "You are an expert cryptogram solver."},
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