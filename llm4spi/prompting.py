from typing import Dict


def create_prompt(task: Dict, condition_type: str, prompt_type: str) -> str:
    
    # check first if the condition-type (pre/post) exists in the task:
    if not (condition_type + "_condition") in task: return None
    condition = task[condition_type + "_condition"]
    if condition == None or condition == "": return None
    
    condition_incomplete = task[condition_type + "_condition_incomplete"]

    # get the prgram desc and program name , if given:
    if 'program' in task:
        programSrc = task['program']
        z = programSrc.split('(')[0].strip()
        # remove "def"
        programName = z.split()[1].strip()
        programDesc = task['program-desc']

    # get the name of the param representing retval
    if condition_type == 'post':
        zz = condition_incomplete.split('(')[1].split(',')[0]
        if ':' in zz :
            retvalParamName = zz.split(':')[0].strip()
        elif ')' in zz :
            retvalParamName = zz.split(')')[0].strip()
        else:
            retvalParamName = zz.strip()
        
    if prompt_type == 'usePrgDesc' :
        if not('program' in task) : return None 
        if condition_type == 'post':
            prompt = f"Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the post-condition of {programName} (in English). \n(2) Then, code this post-condtion as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\nDo not explain.\n\n{condition_incomplete}"
        else:
            prompt = f"Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the pre-condition of {programName} (in English). \n(2) Then, code this pre-condtion as a Python function with the header shown below.\n Do not explain.\n\n{condition_incomplete}"

    elif prompt_type == 'cot1' :
        if not('program' in task) : return None 
        if condition_type == 'post':
            prompt = f"Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the post-condition of {programName} (in English).\n(2) reformulate the post-condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(3) Finally, translate these clauses to a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\n\n{condition_incomplete}"
        else:
            prompt = f"Consider a program {programName}. {programDesc}\n\nnINSTRUCTION:\n(1) Extract the pre-condition of {programName} (in English).\n(2) reformulate the pre-condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(3) Finally, translate these clauses to a Python function with the header shown below.\n\n{condition_incomplete}"

    elif prompt_type == 'cot2' :
        if not('program' in task) : return None 
        if condition_type == 'post' :
            prompt = f"Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the post-condition of {programName} (in English).\n(2) reformulate the post-condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(3) Then, reformulate each clause as implicative Horn clauses of the form \"c1 and c2 ... implies ck\".\n(4) Finally, code these Horn clauses as a Python function with the header shown below, where the parameter {retvalParamName} represents {programName}'s return value.\n\n{condition_incomplete}"
        else:
            prompt = f"Consider a program {programName}. {programDesc}\n\nINSTRUCTION:\n(1) Extract the pre-condition of {programName} (in English).\n(2) reformulate the pre-condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(3) Then, reformulate each clause as implicative Horn clauses of the form \"c1 and c2 ... implies ck\".\n(4) Finally, code these Horn clauses as a Python function with the header shown below.\n\n{condition_incomplete}"

    elif prompt_type == "usePredDesc":
        z = condition_incomplete.split('(')[0].strip()
         # remove "def"
        poscFunctionName = z.split()[1].strip()
        prompt = f"Consider a Python function {poscFunctionName} with header:\n\n{condition_incomplete}\n\nThe function checks if the following condition holds. {condition}\n\nINSTRUCTION: please complete the code. Only give the code. Do not explain."        

    elif prompt_type == "xcot1":
        z = condition_incomplete.split('(')[0].strip()
         # remove "def"
        poscFunctionName = z.split()[1].strip()
        prompt = f"Consider a Python function {poscFunctionName} with the header:\n\n{condition_incomplete}\n\nThe function checks if the following condition is true. {condition}\n\nINSTRUCTION:\n(1) reformulate the mentioned condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(2) translate the clauses to Python code to complete the code of {poscFunctionName}."        

    elif prompt_type == "xcot2":
        z = condition_incomplete.split('(')[0].strip()
         # remove "def"
        poscFunctionName = z.split()[1].strip()
        prompt = f"Consider a Python function {poscFunctionName} with the header:\n\n{condition_incomplete}.\n\nThe function checks if the following condition is true. {condition}\n\nnINSTRUCTION:\n(1) reformulate the mentioned condition as clauses, where each clause is of the form \"if condition1 then condition2\".\n(2) Then, reformulate each clause as implicative Horn clauses of the form \"c1 and c2 ... implies ck\".\n(3) Finally, translate the Horn clauses to Python code to complete the code of {poscFunctionName}."        

    return prompt  