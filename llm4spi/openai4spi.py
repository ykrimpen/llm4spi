from datetime import datetime
from typing import Dict, List
from openai import OpenAI
import os

from data import ZEROSHOT_DATA, read_problems, write_jsonl
from prompting import create_prompt
from evaluation import evaluate_task_results


def create_completion(
        client: OpenAI,
        prompt: str
) -> str:
    """
    Creates a chat completion using a given OpenAI client and prompt and returns the response 
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content


def generate_task_result(
        client: OpenAI,
        task: Dict,
        prompt_type: str
) -> Dict:
    """
    Creates completion prompts for the pre- and post-condition of a task, 
    generates model responses using those prompts
    and returns the generated responses
    """
    pre_condition_prompt = create_prompt(task, condition_type="pre", prompt_type=prompt_type)
    pre_condition_completion = create_completion(client, pre_condition_prompt)
    
    post_condition_prompt = create_prompt(task, condition_type="post", prompt_type=prompt_type)
    post_condition_completion = create_completion(client, post_condition_prompt)
    
    task["pre_condition_completion"] = pre_condition_completion
    task["post_condition_completion"] = post_condition_completion
    return task


def generate_results(
        client: OpenAI,
        prompt_type: str
        ) -> None:
    """
    Reads the zero shot data, generates results for all data entries
    and writes results to a file
    """
    tasks = read_problems(ZEROSHOT_DATA)

    for task in tasks:
        generate_task_result(client, tasks[task], prompt_type=prompt_type)

    evaluate_task_results(tasks)
   
    results = [{
        "task_id": tasks[task]["task_id"],
        "pre_condition_completion": tasks[task]["pre_condition_completion"],
        "post_condition_completion": tasks[task]["post_condition_completion"],
        "pre_condition_evaluation": tasks[task]["pre_condition_evaluation"],
        "post_condition_evaluation": tasks[task]["post_condition_evaluation"]
    } for task in tasks]
    
    current_date = (datetime.now()).strftime("%d_%m_%Y_%H_%M_%S")
    write_jsonl(f"results/model_responses_{prompt_type}_{current_date}.jsonl", results)
    return


if __name__ == '__main__':
    openai_api_key = os.environ.get('OPENAI_API_KEY') 
    client = OpenAI(api_key=openai_api_key)
    generate_results(client, prompt_type="zshot")
    generate_results(client, prompt_type="cot")
    