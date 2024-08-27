from datetime import datetime
from gpt4all import GPT4All
from typing import Dict
import time

from data import ZEROSHOT_DATA, read_problems, write_jsonl
from prompting import create_prompt
from evaluation import evaluate_task_results


def generate_task_result(
        model: GPT4All,
        task: Dict,
        prompt_type: str
) -> Dict:
    """
    Creates completion prompts for the pre- and post-condition of a task, 
    generates model responses using those prompts
    and returns the generated responses
    """
    pre_condition_prompt = create_prompt(task, condition_type="pre", prompt_type=prompt_type)
    pre_condition_completion = model.generate(pre_condition_prompt, max_tokens=1024)
    
    post_condition_prompt = create_prompt(task, condition_type="post", prompt_type=prompt_type)
    post_condition_completion = model.generate(post_condition_prompt, max_tokens=1024)
    
    task["pre_condition_completion"] = pre_condition_completion
    task["post_condition_completion"] = post_condition_completion
    return task


def generate_results(
        model: GPT4All,
        prompt_type: str
        ) -> None:
    """
    Reads the zero shot data, generates results for all data entries
    and writes results to a file
    """
    tasks = read_problems(ZEROSHOT_DATA)

    with model.chat_session():
        for task in tasks:
            generate_task_result(model, tasks[task], prompt_type=prompt_type)

    evaluate_task_results(tasks)

    results = [{
        "task_id": tasks[task]["task_id"],
        "pre_condition_completion": tasks[task]["pre_condition_completion"],
        "post_condition_completion": tasks[task]["post_condition_completion"],
        "pre_condition_evaluation": tasks[task]["pre_condition_evaluation"],
        "post_condition_evaluation": tasks[task]["post_condition_evaluation"]
    } for task in tasks]
    
    current_date = (datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
    write_jsonl(f"model_responses_{prompt_type}_{current_date}.jsonl", results)
    return


if __name__ == '__main__':
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", model_path="/root/models", device="cuda:NVIDIA A16") #device is specific to cluster's GPU, change accordingly when run on a different computer

    #start = time.time()
    generate_results(model, prompt_type="zshot")
    #end = time.time()
    #print("Processing time: " + str(end - start))

    generate_results(model, prompt_type="cot")