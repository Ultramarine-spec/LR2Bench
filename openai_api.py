import os
import json
import time
import asyncio
from tqdm import tqdm
from loguru import logger
from openai import OpenAI, AsyncOpenAI


GPT_API_KEY = "YOUR_KEY"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", GPT_API_KEY))
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", GPT_API_KEY))

async def gpt(sem, tag, model, messages, temperature, top_p, max_tokens):
    async with sem:
        max_retry = 5
        retry_count = 0
        error = None

        while retry_count < max_retry:
            try:
                response = await async_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens,
                    n=1,
                    seed=42
                )
                return {tag: response}
            except Exception as e:
                error = str(e)
                print(f"Error: {e}. Retry count: {retry_count}")
        
        return {tag: error}


async def o1(sem, tag, model, messages, temperature, top_p, max_tokens):
    async with sem:
        max_retry = 5
        retry_count = 0
        error = None
        
        while retry_count < max_retry:
            try:
                response = await async_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_completion_tokens=max_tokens,
                    n=1,
                    seed=42
                )
                
                return {tag: response}
            except Exception as e:
                error = str(e)
                print(f"Error: {e}. Retry count: {retry_count}")
            
            retry_count += 1
            await asyncio.sleep(1)
    
    return {tag: error}
            


def openai_async_gen(messages_dict, model, temperature, top_p, max_tokens):
    sem = asyncio.Semaphore(100)
    
    if "o1" in model:
        func = o1
    else:
        func = gpt
    tasks = [asyncio.ensure_future(func(sem, tag, model, messages, temperature, top_p, max_tokens)) for tag, messages in messages_dict.items()]
    print(len(tasks))
    
    loop = asyncio.get_event_loop()
    outputs_dict = {}
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Processing"):
        output = loop.run_until_complete(task)
        outputs_dict.update(output)
    
    return outputs_dict


def openai_gen(messages_dict, model, temperature, top_p, max_tokens):
    outputs_dict = {}
    for tag, messages in messages_dict.items():
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            n=1,
            seed=42
        )
        
        outputs_dict[tag] = response
    
    return outputs_dict



def test():
    model = "gpt-4o-mini"
    temperature = 0.0
    top_p = 1.0
    max_tokens = 10
    messages_dict = {
        "1": [
            {"role": "user", "content": "How are you?"},
        ],
        "2": [
            {"role": "user", "content": "How are you?"},
        ],
        "3": [
            {"role": "user", "content": "What is your name?"},
        ],
    }

    start_time = time.time()
    # response = openai_async_gen(messages_dict, model, temperature, top_p, max_tokens)
    response = openai_gen(messages_dict, model, temperature, top_p, max_tokens)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")
    print(response)

# test()