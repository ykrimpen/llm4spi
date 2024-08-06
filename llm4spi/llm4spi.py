from gpt4all import GPT4All
from typing import Dict

from llm4spi.data import ZEROSHOT_DATA, read_problems, stream_jsonl, write_jsonl


def generate_task_result(
        model: GPT4All,
        task: Dict[str, Dict]
) -> Dict:
    pre_condition = task["pre_condition"]
    pre_condition_incomplete = task["pre_condition_incomplete"]
    pre_condition_prompt = f"Complete the following Python code such that it checks this: {pre_condition}\n{pre_condition_incomplete}"        
    pre_condition_completion = model.generate(pre_condition_prompt, max_tokens=1024)
    
    post_condition = task["post_condition"]
    post_condition_incomplete = task["post_condition_incomplete"]
    post_condition_prompt = f"Complete the following Python code such that it checks this: {post_condition}\n{post_condition_incomplete}"        
    post_condition_completion = model.generate(post_condition_prompt, max_tokens=1024)
    
    return {"task_id": task["task_id"], "pre_condition_completion": pre_condition_completion, "post_condition_completion": post_condition_completion}


def generate_results(model: GPT4All) -> None:
    problems = read_problems(ZEROSHOT_DATA)

    with model.chat_session():
        results = [generate_task_result(model, problems[problem]) for problem in problems]

    write_jsonl("samples.jsonl", results)
    return

if __name__ == '__main__':
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", model_path="/root/models", device="GPU 1")
    generate_results(model)