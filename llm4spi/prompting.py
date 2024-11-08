from typing import Dict


def create_prompt(task: Dict, condition_type: str, prompt_type: str) -> str:
    
    # check first if the condition-type (pre/post) exists in the task:
    if not (condition_type + "_condition") in task: return None
    condition = task[condition_type + "_condition"]
    if condition == None or condition == "": return None
    
    condition_incomplete = task[condition_type + "_condition_incomplete"]

    if prompt_type == 'usePrgDesc' and condition_type == 'post':
        if not('program' in task) : return None
        programSrc = task['program']
        z = programSrc.split('(')[0].strip()
        # remove "def"
        programName = z.split()[1].strip()
        programDesc = task['program-desc']
        # get the name of the param representing retval
        zz = condition_incomplete.split('(')[1].split(',')[0]
        if ':' in zz :
            revalParamName = zz.split(':')[0].strip()
        elif ')' in zz :
            revalParamName = zz.split(')')[0].strip()
        else:
            revalParamName = zz.strip()
        
        #condition_prompt = f"Complete the following Python code such that it checks this: {condition}\n{condition_incomplete}. Give only the code that is needed to complete the function in your answer in plain text, so without markdown."        
        prompt = f"Consider a program {programName} with the following description. {programDesc}\n\nGive the post-condition of  {programName}. Give this post-condtion as a Python function with the header shown below, where the parameter {revalParamName} represents {programName}'s return value.\nOnly give the function. Do not explain.\n\n{condition_incomplete}"

    elif prompt_type == "usePredDesc":
        z = condition_incomplete.split('(')[0].strip()
         # remove "def"
        poscFunctionName = z.split()[1].strip()
        prompt = f"Consider a program {poscFunctionName} with the following description. {condition}\n\nThe header of {poscFunctionName} is given below. Please complete the code. Only give the code. Do not explain.\n\n{condition_incomplete}."        
    
    return prompt  