import os
import json
import argparse
from collections import defaultdict

level_dict = {
    "crossword": ["5_5", "10_10", "15_15"],
    "acrostic": ["easy", "hard"],
    "logic": ["4_4", "4_5", "4_6", "4_7"],
    "cryptogram": ["easy", "hard"],
    "sudoku": ["4_4_easy", "4_4_hard", "9_9_easy", "9_9_hard"],
    "drop": ["easy", "hard"]
}

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default=None)
    parser.add_argument("--link", type=str, default=None)
    parser.add_argument("--params", type=int, default=None)
    parser.add_argument("--show_on_leaderboard", action="store_true")
    parser.add_argument("--path_template", type=str, default="/public/zhangjiajun/jhchen/2410/data/{task}/{level}/outputs/prompt_deepseek.json/R1")
    parser.add_argument("--output_dir", type=str, default="/public/zhangjiajun/jhchen/2410/submission/prompt_deepseek.json/R1")

    return parser.parse_args()

args = arg_parser()

config_dict = {
    "model_name": args.model_name,
    "link": args.link,
    "Params": args.params,
    "show_on_leaderboard": args.show_on_leaderboard
}

setting_results_dict = defaultdict(lambda: defaultdict(list))

for i, task in enumerate(level_dict):
    for level in level_dict[task]:
        file_dir = args.path_template.format(task=f"{i}-{task}", level=level)
        for setting in os.listdir(file_dir):
            file_path = f"{file_dir}/{setting}/answer.json"
            with open(file_path, "r") as f:
                answer_list = json.load(f)
            setting_results_dict[setting][task].extend(answer_list)

for setting in setting_results_dict:
    results_dict = setting_results_dict[setting]
    submission_dict = {
        "config": config_dict,
        "results": results_dict
    }

    os.makedirs(f"{args.output_dir}/{setting}", exist_ok=True)

    with open(f"{args.output_dir}/{setting}/submission.json", "w") as f:
        json.dump(submission_dict, f, indent=4)