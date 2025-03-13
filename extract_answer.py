import os
import re
import json
import argparse

default_answer_dict = {
    "crossword": "{}",
    "acrostic": "{}",
    "logic": "[]",
    "cryptogram": "{}",
    "sudoku": "[[]]",
    "drop": "[[]]"
}

pattern_dict = {
    "crossword": r'\{.*?\}',
    "acrostic": r'\{.*?\}',
    "logic": r'\[.*?\]',
    "cryptogram": r'\{.*?\}',
    "sudoku": r'\[\s*\[.*?\]\s*\]',
    "drop": r'\[\s*\[.*?\]\s*\]'
}


def extract(file_dir, task_name):
    file_path = f"{file_dir}/response.jsonl"
    level = file_path.split("/outputs")[0].split("/")[-1]
    
    all_outputs = []
    with open(file_path, "r") as f:
        for line in f:
            all_outputs.append(json.loads(line))
    
    answer_list = []
    default_answer = default_answer_dict[task_name]
    final_answer_pattern = r"<Answer>(.*?)</Answer>" if task_name != "cryptogram" else r"<Mapping>(.*?)</Mapping>"
    pattern = pattern_dict[task_name]
    
    for output in all_outputs:
        tag = output["tag"]
        model_response = output["response"]
        
        final_answer = re.findall(final_answer_pattern, model_response, re.IGNORECASE | re.DOTALL)
        if not final_answer:
            final_answer = default_answer
        else:
            final_answer = final_answer[-1].strip()
            pattern = pattern_dict[task_name]
            final_answer = re.findall(pattern, final_answer, re.IGNORECASE | re.DOTALL)
            if not final_answer:
                final_answer = default_answer
            else:
                final_answer = final_answer[-1].strip()
        answer_list.append({
            "level": level,
            "tag": tag,
            "answer": final_answer
        })
    
    with open(f"{file_dir}/answer.json", "w") as f:
        json.dump(answer_list, f, indent=4)
        
            

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs_root", type=str, default=None)
    parser.add_argument("--task", choices=["crossword", "acrostic", "logic", "cryptogram", "sudoku", "drop"], default=None)

    return parser.parse_args()

args = arg_parser()

# import pdb; pdb.set_trace()
for output_dir in sorted(os.listdir(args.outputs_root)):
    if os.path.isfile(f"{args.outputs_root}/{output_dir}"):
        continue
    print(f"Processing {args.outputs_root}/{output_dir}")
    extract(f"{args.outputs_root}/{output_dir}", args.task)
