from typing import Dict

def create_prompt(task: Dict, condition_type: str, prompt_type: str) -> str:
    
    # check first if the condition-type (pre/post) exists in the task:
    if not (condition_type + "_condition") in task: return None
    condition = task[condition_type + "_condition"]
    if condition == None or condition == "": return None
    
    condition_incomplete = task[condition_type + "_condition_incomplete"]

    # get the program desc and program name, if given:
    if 'program' in task:
        programSrc = task['program']
        z = programSrc.split('(')[0].strip()
        # remove "def"
        programName = z.split()[1].strip()
        programDesc = task['program-desc']
    else:
        programName = "unknown"
        programDesc = "unknown"

    # get the name of the param representing retval
    if condition_type == 'post':
        zz = condition_incomplete.split('(')[1].split(',')[0]
        if ':' in zz :
            retvalParamName = zz.split(':')[0].strip()
        elif ')' in zz :
            retvalParamName = zz.split(')')[0].strip()
        else:
            retvalParamName = zz.strip()
    
    # get the function name for usePredDesc, xcot1, and xcot2 prompts
    poscFunctionName = task.get('poscFunctionName', 'unknown_function')

    base_prompts = {
        'usePrgDesc': "Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the {condition_type}-condition of {programName} (in English). \n(2) Then, code this {condition_type}-condition as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\nDo not explain. If a helper function is needed, define it as an inner function. Import packages, if needed, locally within the function.\n\n{condition_incomplete}",
        'cot1': "Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the {condition_type}-condition of {programName} (in English).\n(2) reformulate the {condition_type}-condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(3) Finally, translate these clauses to a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\n\n{condition_incomplete}",
        'cot2': "Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the {condition_type}-condition of {programName} (in English).\n(2) reformulate the {condition_type}-condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(3) Then, reformulate each clause as implicative Horn clauses of the form \"c1 and c2 ... implies ck\".\n(4) Finally, code these Horn clauses as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\n\n{condition_incomplete}",
        'usePredDesc': "Consider a Python function {poscFunctionName} with header:\n\n{condition_incomplete}\n\nThe function checks if the following condition holds. {condition}\n\nINSTRUCTION: please complete the code. Only give the code. Do not explain. If a helper function is needed, define it as an inner function. Import packages, if needed, locally within the function.",
        'xcot1': "Consider a Python function {poscFunctionName} with the header:\n\n{condition_incomplete}\n\nThe function checks if the following condition is true. {condition}\n\nINSTRUCTION:\n(1) reformulate the mentioned condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(2) translate the clauses to Python code to complete the code of {poscFunctionName}.",
        'xcot2': "Consider a Python function {poscFunctionName} with the header:\n\n{condition_incomplete}.\n\nThe function checks if the following condition is true. {condition}\n\nINSTRUCTION:\n(1) reformulate the mentioned condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(2) Then, reformulate each clause as implicative Horn clauses of the form \"c1 and c2 ... implies ck\".\n(3) Finally, translate the Horn clauses to Python code to complete the code of {poscFunctionName}."
    }

    mbti_descriptions = [
        "Please generate a function as a programmer with the following MBTI description: INTJ.",
        "Please generate a function as a programmer with the following MBTI description: INTP."
    ]

    if prompt_type in base_prompts:
        prompt = base_prompts[prompt_type].format(
            programName=programName,
            programDesc=programDesc,
            condition_type=condition_type,
            retvalParamName=retvalParamName,
            condition_incomplete=condition_incomplete,
            condition=condition,
            poscFunctionName=poscFunctionName
        )
    else:
        base_prompt_type = prompt_type.split('_')[0]
        mbti_description = mbti_descriptions[int(prompt_type.split('_')[1])]
        prompt = f"{mbti_description}\n\n" + base_prompts[base_prompt_type].format(
            programName=programName,
            programDesc=programDesc,
            condition_type=condition_type,
            retvalParamName=retvalParamName,
            condition_incomplete=condition_incomplete,
            condition=condition,
            poscFunctionName=poscFunctionName
        )
    return prompt

# Example usage:
# prompt = create_prompt(task, 'post', 'usePrgDesc')
# prompt = create_prompt(task, 'post', 'usePrgDesc_0')  # INTJ
# prompt = create_prompt(task, 'post', 'usePrgDesc_1')  # INTP