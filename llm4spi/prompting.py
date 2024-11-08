from typing import Dict


def create_prompt(task: Dict, condition_type: str, prompt_type: str) -> str:
    
    # check first if the condition-type (pre/post) exists in the task:
    if not (condition_type + "_condition") in task: return None
    condition = task[condition_type + "_condition"]
    if condition == None or condition == "": return None
    
    condition_incomplete = task[condition_type + "_condition_incomplete"]

    # get the prgram desc, program name etc, if it if given:
    if 'program' in task:
        programSrc = task['program']
        z = programSrc.split('(')[0].strip()
        # remove "def"
        programName = z.split()[1].strip()
        programDesc = task['program-desc']
        # get the name of the param representing retval
        zz = condition_incomplete.split('(')[1].split(',')[0]
        if ':' in zz :
            retvalParamName = zz.split(':')[0].strip()
        elif ')' in zz :
            retvalParamName = zz.split(')')[0].strip()
        else:
            retvalParamName = zz.strip()
        
    if prompt_type == 'usePrgDesc' and condition_type == 'post':
        if not('program' in task) : return None 
        #condition_prompt = f"Complete the following Python code such that it checks this: {condition}\n{condition_incomplete}. Give only the code that is needed to complete the function in your answer in plain text, so without markdown."        
        prompt = f"Consider a program {programName} with the following description. {programDesc}\n\nGive the post-condition of  {programName}. Give this post-condtion as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\nOnly give the function. Do not explain.\n\n{condition_incomplete}"

    elif prompt_type == 'cot1' and condition_type == 'post':
        if not('program' in task) : return None 
        prompt = f"Consider a program {programName} with the following description. {programDesc}\nObtain the post-condition of  {programName} (in English).\nThen, reformulate the post-condition as clauses, where each clause is of the form \"if condition1 then condition1\".\nThen, give this post-condtion as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\n\n{condition_incomplete}"

    elif prompt_type == 'cot2' and condition_type == 'post':
        if not('program' in task) : return None 
        prompt = f"Consider a program {programName} with the following description. {programDesc}\nObtain the post-condition of  {programName} (in English).\nThen, reformulate the post-condition as clauses, where each clause is of the form \"if condition1 then condition1\".\nThen, reformulate each clause as a Horn clause.\nThen, give this post-condtion as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\n\n{condition_incomplete}"

    elif prompt_type == "usePredDesc":
        z = condition_incomplete.split('(')[0].strip()
         # remove "def"
        poscFunctionName = z.split()[1].strip()
        prompt = f"Consider a program {poscFunctionName} with the following description. {condition}\n\nThe header of {poscFunctionName} is given below. Please complete the code. Only give the code. Do not explain.\n\n{condition_incomplete}."        
    
    return prompt  