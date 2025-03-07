import os
import json

rules = '''
Logic puzzles require the solver to deduce the relationships between different people, places and things based on a limited number of clues given in the puzzle. Remember: every item belongs to one and only one person, no item will ever be shared. Using only the clues provided and simple deductive logic and reasoning.
'''
rules = rules.strip()

requests = '''
Please solve the Logic Puzzle according to the provided rules. Please also follow the requests below to present your analysis and solutions:
1. Read and understand each clue in the context of the puzzle. Apply each clue one by one to deduce the correct arrangement of different variables.
2. Use logical reasoning to figure out the relationships between the variables based on the clues provided.
3. After solving the puzzle, present your final solution using JSON Format and wrap it with the <Answer> and </Answer> tags. For example:
<Answer>
[
    {
        "Variable1": "Value1",
        "Variable2": "Value2",
        ...
    },
    {
        "Variable1": "Value3",
        "Variable2": "Value4",
        ...
    },
    ...
]
</Answer>
4. Please generate your response without redundant and repeating content.
'''
requests = requests.strip()


example1 = '''
Here is a logic puzzle:
{
    "variables": {
        "names": [
            "Fiona",
            "Tobias",
            "Leanne"
        ],
        "main dishes": [
            "Beef Wellington",
            "Gado Gado",
            "Shrimp Ceviche"
        ],
        "desserts": [
            "Creme Brulee",
            "Raspberry Tiramisu",
            "French Apple Cake"
        ]
    },
    "clues": {
        "1": "The three people are Tobias, the one who brought the Gado Gado, and the one who brought the Raspberry Tiramisu.",
        "2": "Fiona did not bring the Beef Wellington.",
        "3": "The Shrimp Ceviche was brought by either Tobias or the person who brought the Creme Brulee.",
    }
}

Please complete the following blank based on your final solution:
[
    {
        "names": "Fiona",
        "main dishes": "____",
        "desserts": "____",
    },
    {
        "names": "Tobias",
        "main dishes": "____",
        "desserts": "____",
    },
    {
        "names": "Leanne",
        "main dishes": "____",
        "desserts": "____",
    }
]
'''
example1 = example1.strip()

solution1 = '''
Let's start solving the logic puzzle step by step.


Participants and Dishes
Names: Fiona, Tobias, Leanne
Main Dishes: Beef Wellington, Gado Gado, Shrimp Ceviche
Desserts: Crème Brûlée, Raspberry Tiramisu, French Apple Cake


Interpreting Clue 1:
    Roles:
        Tobias: Did not bring Gado Gado or Raspberry Tiramisu.
        Gado Gado Bringer: Not Tobias.
        Raspberry Tiramisu Bringer: Not Tobias.

    Conclusion:
        Fiona and Leanne must be the ones who brought Gado Gado and Raspberry Tiramisu, respectively (or vice versa).


Applying Clue 2:
    Fiona did not bring Beef Wellington.
    Therefore, Fiona must have brought Gado Gado or Shrimp Ceviche.


Applying Clue 3:
    Shrimp Ceviche was brought by either:
        Tobias, or The person who brought Creme Brulee.

    Since Tobias cannot bring Gado Gado or Raspberry Tiramisu, if he brought Shrimp Ceviche, it aligns with Clue 3.


Determining Assignments:
    Case 1: Fiona Brought Gado Gado
        Fiona: Gado Gado + ?
        Leanne: Beef Wellington + Raspberry Tiramisu
        Tobias: Shrimp Ceviche + French Apple Cake
        Dessert Assignments:
            Fiona must bring Creme Brulee or French Apple Cake. However, since Tobias brings French Apple Cake, Fiona brings Creme Brulee.
    Case 2: Fiona Brought Shrimp Ceviche
        This scenario leads to a contradiction with Clue 3 because Shrimp Ceviche would then be brought by Fiona, not Tobias or the Creme Brulee bringer.
        Conclusion: Case 2 is invalid.


Final Answer:
Fiona:
    Main Dish: Gado Gado
    Dessert: Creme Brulee
Tobias:
    Main Dish: Shrimp Ceviche
    Dessert: French Apple Cake
Leanne:
    Main Dish: Beef Wellington
    Dessert: Raspberry Tiramisu


Final Answer in JSON Format:
<Answer>
[
    {
        "names": "Fiona",
        "main dishes": "Gado Gado",
        "desserts": "Creme Brulee",
    },
    {
        "names": "Tobias",
        "main dishes": "Shrimp Ceviche",
        "desserts": "French Apple Cake",
    },
    {
        "names": "Leanne",
        "main dishes": "Beef Wellington",
        "desserts": "Raspberry Tiramisu",
    }
]
</Answer>
'''
solution1 = solution1.strip()


example2 = '''
Here is a logic puzzle:
{
    "variables": {
        "names": [
            "Max",
            "Kylie",
            "Emma"
        ],
        "ages": [
            "3 years",
            "4 years",
            "5 years"
        ],
        "toys": [
            "Train",
            "Dinosaur",
            "Plush Dog"
        ]
    },
    "clues": {
        "1": "Max, the youngest of the three, does not have a plush dog toy.",
        "2": "Kylie was comforted by her dinosaur toy.",
        "3": "The 4 year old was not dropped off with a plush dog toy."
    }
}

Please complete the following blank based on your final solution:
[
    {
        "names": "Max",
        "ages": "____",
        "toys": "____"
    },
    {
        "names": "Kylie",
        "ages": "____",
        "toys": "____"
    },
    {
        "names": "Emma",
        "ages": "____",
        "toys": "____"
    },
]
'''
example2 = example2.strip()

solution2 = '''
Let's start solving the logic puzzle step by step.


Participants and Attributes
Names: Max, Kylie, Emma
Ages: 3 years, 4 years, 5 years
Toys: Train, Dinosaur, Plush Dog



Determining Max's Age and Toy:
    Clue 1 states that Max is the youngest, so Max is 3 years old.
    Max does not have the Plush Dog toy.
    Toys available: Train, Dinosaur.
    Clue 2 indicates that Kylie has the Dinosaur toy, so Max must have the Train.

Assigning Kylie's Attributes:
    Clue 2 states that Kylie has the Dinosaur toy.
    Ages available: 4 years, 5 years.
    Clue 3 indicates that the 4-year-old does not have the Plush Dog.
    If Kylie were 5 years old, Emma would have to be 4 years old with the Plush Dog, which contradicts Clue 3.
    Therefore, Kylie must be 4 years old.

Assigning Emma's Attributes:
    Remaining age: 5 years.
    Remaining toy: Plush Dog.

    
Final Answer:
Max is 3 years old and has a Train toy.
Kylie is 4 years old and has a Dinosaur toy.
Emma is 5 years old and has a Plush Dog toy.


Final Answer in JSON Format:
<Answer>
[
    {
        "names": "Max",
        "ages": "3 years",
        "toys": "Train"
    },
    {
        "names": "Kylie",
        "ages": "4 years",
        "toys": "Dinosaur"
    },
    {
        "names": "Emma",
        "ages": "5 years",
        "toys": "Plush Dog"
    },
]
</Answer>
'''
solution2 = solution2.strip()



example = "<example>"

shot_dict = {}


shot_dict['zero_shot'] = [
    {"role": "system", "content": "You are an expert logic puzzle solver."},
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"},
    {"role": "assistant", "content": f"Let's start solving the logic puzzle step by step."},
]


shot_dict['two_shot'] = [
    {"role": "system", "content": "You are an expert logic puzzle solver."},
    {"role": "user", "content": f"{rules}\n\n{example1}\n\n{requests}"},
    {"role": "assistant", "content": solution1},
    {"role": "user", "content": f"{example2}\n\n{requests}"},
    {"role": "assistant", "content": solution2},
    {"role": "user", "content": f"{example}\n\n{requests}"},
    {"role": "assistant", "content": f"Let's start solving the logic puzzle step by step."},
]


for setting in ['4_4', '4_5', '4_6', '4_7']:
    with open(f"./{setting}/prompt.json", "w", encoding="utf-8") as f:
        json.dump(shot_dict, f, indent=4)

api_shot_dict = {}

api_shot_dict['zero_shot'] = [
    {"role": "user", "content": f"{rules}\n\n{example}\n\n{requests}"}
]

api_shot_dict['two_shot'] = [
    {"role": "user", "content": f"{rules}\n\nExample Puzzle 1:\n\n{example1}\n\nSolution 1:\n\n{solution1}\n\nExample Puzzle 2:\n\n{example2}\n\nSolution 2:\n\n{solution2}\n\nNow please solve the following puzzle:\n\n{example}\n\n{requests}"}
]

for setting in ['4_4', '4_5', '4_6', '4_7']:
    with open(f"./{setting}/prompt_api.json", "w", encoding="utf-8") as f:
        json.dump(api_shot_dict, f, indent=4)
        