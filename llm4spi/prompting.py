from typing import Dict


def create_prompt(task: Dict, condition_type: str, prompt_type: str) -> str:
    condition = task[condition_type + "_condition"]
    condition_incomplete = task[condition_type + "_condition_incomplete"]

    if prompt_type == "zshot":
        #condition_prompt = f"Complete the following Python code such that it checks this: {condition}\n{condition_incomplete}. Give only the code that is needed to complete the function in your answer in plain text, so without markdown."        
        condition_prompt = f"Complete the following Python code such that: {condition}\n\n{condition_incomplete}\n\nGive only the code that is needed to complete the function in your answer in plain text, so without markdown."        
    elif prompt_type == "cot":
        #condition_prompt = f"Complete the following Python code such that it checks this: {condition}. Solve the problem step by step.\n{condition_incomplete}. Give only the code that is needed to complete the function in your answer in plain text, so without markdown."        
        condition_prompt = f"Complete the following Python code such that: {condition}.\n\n Solve the problem step by step.\n\n{condition_incomplete}\n\n Give only the code that is needed to complete the function in your answer in plain text, so without markdown."        
    
    return condition_prompt  