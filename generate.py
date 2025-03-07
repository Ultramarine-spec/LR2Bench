import os
import pdb
import json
import time
import copy
import torch
import pprint
import argparse
from tqdm import tqdm
from openai import OpenAI
import google.generativeai as genai
from loguru import logger
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

from openai_api import *

model_root = "YOUR_MODEL_DIR"
model_root = "/public/zhangjiajun/jhchen/huggingface/pretrained_model"

model_dict = {
    "llama-3.1-8b": f"{model_root}/meta-llama/Meta-Llama-3.1-8B-Instruct",
    "llama-3.1-70b": f"{model_root}/meta-llama/Meta-Llama-3.1-70B-Instruct",
    "llama-3.3-70b": f"{model_root}/meta-llama/Llama-3.3-70B-Instruct",
    
    "qwen-2.5-7b": f"{model_root}/Qwen/Qwen2.5-7B-Instruct",
    "qwen-2.5-32b": f"{model_root}/Qwen/Qwen2.5-32B-Instruct",
    "qwq-32b": f"{model_root}/Qwen/QwQ-32B-Preview",
    "qwq-32b-release": f"{model_root}/Qwen/QwQ-32B",
    "qwen-2.5-72b": f"{model_root}/Qwen/Qwen2.5-72B-Instruct",

    "mistral-7b": f"{model_root}/mistralai/Mistral-7B-Instruct-v0.3",
    "mistral-small": f"{model_root}/mistralai/Mistral-Small-Instruct-2409",
    "mistral-large": f"{model_root}/mistralai/Mistral-Large-Instruct-2411",
    
    "openai-gpt-4o-mini": "gpt-4o-mini",
    "openai-gpt-4o": "gpt-4o-2024-08-06",
    "openai-o1-preview": "o1-preview-2024-09-12",
    "openai-o1-mini": "o1-mini-2024-09-12",
    
    "gemini-2.0-exp": "gemini-2.0-flash-exp",
    "gemini-2.0-thinking": "gemini-2.0-flash-thinking-exp-1219",
}


def arg_parser():
    parser = argparse.ArgumentParser()
    # --model choice
    parser.add_argument("--model", choices=model_dict.keys(), default="llama-3.1-8b")
    parser.add_argument("--task_path", type=str, default=None)
    parser.add_argument("--prompt_name", type=str, default="prompt.json")
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top_p", type=float, default=0.9)
    
    parser.add_argument("--repetition_penalty", type=float, default=1.0)
    parser.add_argument("--max_tokens", type=int, default=4096)
    parser.add_argument("--drop_zero_shot", action="store_true")
    
    parser.add_argument("--vllm", action="store_true")
    parser.add_argument("--test", action="store_true")
    return parser.parse_args()


def openai(args):
    model = model_dict[args.model]
    print(f"Using model: {model}")
    prompt_path = f"{args.task_path}/{args.prompt_name}"
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt_dict = json.load(f)
    
    if args.drop_zero_shot:
        prompt_dict.pop("zero_shot")
    
    data_path = f"{args.task_path}/data.jsonl"
    data_list = []
    with open(data_path, "r", encoding='utf-8') as f:
        for line in f:
            data_list.append(json.loads(line.strip()))
    
    if args.test:
        data_list = data_list[:10]
    
    outputs_path = f"{args.task_path}/outputs/{args.prompt_name}/{args.model}"
    os.makedirs(outputs_path, exist_ok=True)
    
    # pdb.set_trace()
    for setting in prompt_dict.keys():
        print(f"==Running inference on: {setting}_t{args.temperature}_top-p{args.top_p}==")
        os.makedirs(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}", exist_ok=True)

        if os.path.exists(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}/response.jsonl"):
            print(f"{setting}_t{args.temperature}_top-p{args.top_p} already exists, skipping...")
            continue

        logger.remove()
        log_file = logger.add(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}/output.log", mode="w")
        logger.info(f"==Running inference on: {setting}_t{args.temperature}_top-p{args.top_p}==")
        
        messages_template = prompt_dict[setting]
        if messages_template[0]["role"] == "system":
            messages_template = messages_template[1:]
        if messages_template[-1]["role"] == "assistant":
            messages_template = messages_template[:-1]
        
        messages_dict = {}
        for d in data_list:
            messages = copy.deepcopy(messages_template)
            if "<example>" not in messages[-1]["content"]:
                raise ValueError("Last message should contain <example>")
            messages[-1]["content"] = messages[-1]["content"].replace("<example>", d["example_text"])
            key = d["tag"] if "tag" in d else d["date"]
            messages_dict[key] = messages

            # break
        
        if len(messages_dict) != 50:
            print(f"Only {len(messages_dict)} examples for {setting}")
            exit()
        

        outputs_dict = openai_async_gen(messages_dict, model, args.temperature, args.top_p, args.max_tokens)
        
        all_outputs = []
        for d in data_list:
            output_dict = {}
            key = d["tag"] if "tag" in d else d["date"]
            response = outputs_dict[key]


            if isinstance(response, str):
                output_dict["error"] = response
                output_dict["response"] = ""
                print("Error:", response)
            else:
                output_dict["output_info"] = str(response)
                output_dict["response"] = response.choices[0].message.content.strip()
                output_dict["response_length"] = response.usage.completion_tokens
                output_dict["prompt_length"] = response.usage.prompt_tokens
            
            output_dict["setting"] = setting
            output_dict["prompt"] = messages_dict[key]
            
            logger.info("Prompt:\n{}".format('\n\n<ROLE>\n\n'.join([x['content'] for x in output_dict["prompt"]])))
            logger.info(f"Response:\n{output_dict['response']}")
            
            output_dict = d | output_dict
            all_outputs.append(output_dict)
        
        with open(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}/response.jsonl", "w", encoding='utf-8') as f:
            for output in all_outputs:
                f.write(json.dumps(output) + "\n")
        


def gemini(args):
    # pdb.set_trace()
    genai.configure(api_key="YOUR_KEY")
    model = model_dict[args.model]
    gemini_model = genai.GenerativeModel(model)
    generation_config = genai.GenerationConfig(temperature=args.temperature, top_p=args.top_p)
    print(f"Using model: {model}")
    prompt_path = f"{args.task_path}/{args.prompt_name}"
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt_dict = json.load(f)
    
    if args.drop_zero_shot:
        prompt_dict.pop("zero_shot")
    
    data_path = f"{args.task_path}/data.jsonl"
    data_list = []
    with open(data_path, "r", encoding='utf-8') as f:
        for line in f:
            data_list.append(json.loads(line.strip()))
    
    if args.test:
        data_list = data_list[:10]
        
    outputs_path = f"{args.task_path}/outputs/{args.prompt_name}/{args.model}"
    os.makedirs(outputs_path, exist_ok=True)
    
    for setting in prompt_dict.keys():
        print(f"==Running inference on: {setting}_t{args.temperature}_top-p{args.top_p}==")
        os.makedirs(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}", exist_ok=True)
        
        if os.path.exists(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}/response.jsonl"):
            print(f"{setting}_t{args.temperature}_top-p{args.top_p} already exists, skipping...")
            continue
        
        logger.remove()
        log_file = logger.add(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}/output.log", mode="w")
        logger.info(f"==Running inference on: {setting}_t{args.temperature}_top-p{args.top_p}==")
        
        messages_template = prompt_dict[setting]
        assert len(messages_template) == 1
        assert messages_template[0]["role"] == "user"
        messages_template = messages_template[0]['content']
        
        all_outputs = []
        for d in tqdm(data_list):
            output_dict = {}
            if "<example>" not in messages_template:
                raise ValueError("Last message should contain <example>")
            messages = messages_template.replace("<example>", d["example_text"])
            
            max_retry = 5
            retry_count = 0
            response = None
            while retry_count < max_retry:
                try: 
                    response = gemini_model.generate_content(messages, generation_config=generation_config)
                    break
                except Exception as e:
                    print("Error:", e)
                
                retry_count += 1
                time.sleep(60)
                
            if response is None:
                print(f"Failed to generate response for {setting} with example: {d['example_text']}")
                continue
            response_dict = response.to_dict()
            
            output_dict["setting"] = setting
            output_dict["prompt"] = messages
            output_dict["response_dict"] = response_dict
            output_dict["response"] = response.text
            output_dict["response_length"] = response_dict['usage_metadata']['candidates_token_count']
            output_dict["prompt_length"] = response_dict['usage_metadata']['prompt_token_count']
            
            logger.info(f"Prompt:\n{messages}")
            logger.info(f"Response:\n{output_dict['response']}")
            
            output_dict = d | output_dict
            all_outputs.append(output_dict)
            
            
        with open(f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}/response.jsonl", "w", encoding='utf-8') as f:
            for output in all_outputs:
                f.write(json.dumps(output) + "\n")
        



def my_generate(input_list, llm, sampling_params, data_list, target_path, logger):
    os.makedirs(target_path, exist_ok=True)
    if os.path.exists(f"{target_path}/response.jsonl"):
        print('+' * 50)
        print(f"{target_path} already exists, skipping...")
        print('+' * 50)
        return

    logger.remove()
    log_file = logger.add(f"{target_path}/output.log", mode="w")
    logger.info(f"==Running inference on: {target_path}==")

    outputs = llm.generate(input_list, sampling_params)
    all_outputs = []
    for i, output in enumerate(outputs):
        data_dict = data_list[i]
        output_dict = {}
        
        output_dict["setting"] = setting
        output_dict["prompt"] = output.prompt
        output_dict["prompt_length"] = len(output.prompt_token_ids)
        output_dict["response"] = output.outputs[0].text
        if not output_dict["response"]:
            print(output)
        logger.info(f"Prompt:\n{output.prompt}")
        logger.info(f"Response:\n{output.outputs[0].text}")
        output_dict["response_length"] = len(output.outputs[0].token_ids)
        
        output_dict = data_dict | output_dict
        all_outputs.append(output_dict)
    
    with open(f"{target_path}/response.jsonl", "w", encoding='utf-8') as f:
        for output in all_outputs:
            f.write(json.dumps(output) + "\n")


set_seed(42)

args = arg_parser()

print("+" * 50)
print(args)
print("+" * 50)

if "openai" in args.model:
    openai(args)
elif "gemini" in args.model:
    gemini(args)
else:
    model_path = model_dict[args.model]
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if not tokenizer.pad_token_id:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    llm = LLM(model=model_path, tensor_parallel_size=len(os.environ["CUDA_VISIBLE_DEVICES"].split(',')), enforce_eager=True, disable_custom_all_reduce=True, trust_remote_code=True)
    sampling_params = SamplingParams(temperature=args.temperature, top_p=args.top_p, max_tokens=args.max_tokens, repetition_penalty=args.repetition_penalty)

    # model = AutoModelForCausalLM.from_pretrained(
    #     model_path,
    #     torch_dtype=torch.bfloat16,
    #     device_map="auto",
    #     low_cpu_mem_usage=True,
    #     attn_implementation="flash_attention_2"
    # ).eval()

    # pdb.set_trace()
    prompt_path = f"{args.task_path}/{args.prompt_name}"
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt_dict = json.load(f)

    if args.drop_zero_shot:
        prompt_dict.pop("zero_shot")


    data_path = f"{args.task_path}/data.jsonl"
    data_list = []
    with open(data_path, "r", encoding='utf-8') as f:
        for line in f:
            data_list.append(json.loads(line.strip()))

    outputs_path = f"{args.task_path}/outputs/{args.prompt_name}/{args.model}"
    os.makedirs(outputs_path, exist_ok=True)

    for setting in prompt_dict.keys():
        # pdb.set_trace()
        messages_template = prompt_dict[setting]
        continue_final_message = False
        add_generation_prompt = True
        if messages_template[-1]["role"] == "assistant":
            messages_template = messages_template[:-1]

        input_template = tokenizer.apply_chat_template(
            messages_template,
            tokenize=False,
            continue_final_message=continue_final_message,
            add_generation_prompt=add_generation_prompt
        )


        input_list = [input_template.replace("<example>", d["example_text"]) for d in data_list]
        if args.test:
            input_list = input_list[:10]


        target_path = f"{outputs_path}/{setting}_t{args.temperature}_top-p{args.top_p}"
        if args.repetition_penalty != 1.0:
            target_path += f"_rp{args.repetition_penalty}"
        if args.temperature > 0:
            for sample_num in range(3):
                sampling_params.seed = sample_num
                sample_target_path = f"{target_path}_seed{sample_num}"
                os.makedirs(sample_target_path, exist_ok=True)
                my_generate(input_list, llm, sampling_params, data_list, sample_target_path, logger)
        else:
            my_generate(input_list, llm, sampling_params, data_list, target_path, logger)