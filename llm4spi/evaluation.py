#
# Contain functions for performing the LLM evaluation towards the pre-/post-conditions
# tasks.
#

from typing import Dict
import textwrap
import data
from collections import Counter
import myconfig

def compare_results(expected: list, predicted: list) -> str:
    """
    Returns a judgement after comparising the predicted results (results from running the function produced
    by AI) with of the expected results.
    Note: None as a prediction will be interpreted as 'making no prediction', and
          will be excluded from judgement.
          However, if all predications are None, a 'failed' judgement is returned.

    Judgement:
    (1) 'accepted' if all predictions (excluding None-values) match the expected values.
    (2) 'failed' if AI solution crashed, or it produces a value that is not even a boolean,
        or if all predications are None.
    (3) 'too_weak' if for every not-None prediction p and the corresponding expected value e
                   we have e ==> p
    (4) 'too_strong' if for every not-None prediction p and the corresponding expected value e
                   we have p ==> e
    (5) 'rejected' if none of the above is the case. 

    """
    
    # filter first the None-predictions
    zz = [ (e,p) for (e,p) in zip(expected,predicted) if p != None ]
    if len(zz) == 0:
        # if all predictions are None, we declare "fail":
        return "failed"
    # only inspect the expecteds and predictions for which the predictions are not None:
    expected   = [ e for (e,p) in zz ]
    predicted = [ p for (e,p) in zz ]

    #print(f">>> evaluated expecteds: {expected}")
    #print(f">>> evaluated predictions: {predicted}")

    if any((prediction == "failed") |  (type(prediction) != bool) for prediction in predicted):
        return "failed"
    
    if expected == predicted:
        return "accepted"
    
    any_false_negative = False
    any_false_positive = False

    for (expectation,prediction) in zip(expected,predicted):
        any_false_negative = any_false_negative or (expectation and (not prediction))
        any_false_positive = any_false_positive or ((not expectation) and prediction)
    
    if any_false_negative & any_false_positive:
        return "rejected"
    if any_false_negative:
        return "too_strong"
    if any_false_positive:
        return "too_weak"
    
    return "failed"
    

def try_check_pre(test_case, task_id):
    try:
        result = eval(f"check_pre_{task_id}(*test_case)")
    except:
        return "failed"
    return result


def try_check_post(test_case, task_id):
    try:
        result = eval(f"check_post_{task_id}(*test_case)")
    except:
        return "failed"
    return result


def listSplit(s:list, sep): 
    """
    split the list s into segments which are separated by sep
    """
    segments = []
    z = []
    for x in s:
        if x==sep:
            segments.append(z)
            z = []
        else:
            z.append(x)
    segments.append(z)
    return segments

def evaluate_task_result(task: Dict, condition: str):
    """
    Given a single task, described in a dictionary, this function builds the solution 
    and predicted pre or post condition function-definitions that corresponds
    to the task. E.g. it constructs definitions 'def f1_solution...' and 'def f1_predicted...'.

    The condition argument is either 'pre' or 'post'.

    After the defs are constructred, the function evaluates the predicted 
    function's performance.

    The evaluation results are added/updated as entries in the given
    task dictionary (side-effect).
    """

    # we first handle the case when the task pre- or post-condition
    # does not exists:
    task[f"{condition}_condition_baseEvaluation"] = None
    task[f"{condition}_condition_evaluation"] = None
    task[f"{condition}_condition_baseEvaluations"] = None
    task[f"{condition}_condition_evaluations"] = None
    if not (f"{condition}_condition" in task) : 
        return
    conditionDesc = task[f"{condition}_condition"]
    if conditionDesc==None or conditionDesc=="":
        return

    # The task pre-/post- exists, we proceed with its evaluation:

    solution_function = task[f"{condition}_condition_solution"]
    # executing the solution-function def; not expecting it to fail
    #complete_solution_function = task[f"{condition}_condition_incomplete"] + "\n" + indented_solution_function_body
    try:
        exec(solution_function,globals())
    except:
        print(">>>>>> The def of the solution function crashed!")
        print(solution_function)
        return

    # if the test-cases are marked with a split token, this indicates that
    # they consists of two groups: base-group and validation-group.
    # We separate them:
    splitToken = '==='
    test_cases0 = eval(task[f"{condition}_condition_tests"])
    test_suites = listSplit(test_cases0,splitToken)
    test_casesBase = test_suites[0]
    if len(test_suites) == 1:
        test_casesValidation = []
    elif len(test_suites) == 2:
        test_casesValidation = test_suites[1]
    else: # then we have at least three suites
        if myconfig.CONFIG_USE_SECOND_TESTSUITE_AS_BASETESTS_TOO:
            test_casesBase.extend(test_suites[1])
            test_casesValidation = []
            for suite in test_suites[2:] : test_casesValidation.extend(suite)
        else:
            test_casesValidation = []
            for suite in test_suites[1:] : test_casesValidation.extend(suite)
    
    # executing the test-cases on the solution-function, also not expecting these
    # to fail:
    if (condition == "pre"):
        solution_resultsBase = [eval(f"check_pre_solution_{task["task_id"]}(*test_case)") for test_case in test_casesBase]
        solution_resultsValidation = [eval(f"check_pre_solution_{task["task_id"]}(*test_case)") for test_case in test_casesValidation]
    else:
        solution_resultsBase = [eval(f"check_post_solution_{task["task_id"]}(*test_case)") for test_case in test_casesBase]
        solution_resultsValidation = [eval(f"check_post_solution_{task["task_id"]}(*test_case)") for test_case in test_casesValidation]

    print(f"task: {task["task_id"]}, condition: {condition}")
    print(solution_function)
    print(f"Base: {solution_resultsBase}")
    print(f"Validation: {solution_resultsValidation}")

    # get all the AI-completions, indent each one of them as well:
    AI_completions = [ textwrap.indent(body,'    ') for body in task[f"{condition}_condition_completions"] ]
    # now, evaliate each candidate-completion:
    baseEvaluationz = []
    fullEvaluationz = []

    for k in range(len(AI_completions)):
        indented_function_body = AI_completions[k]
        complete_function = task[f"{condition}_condition_incomplete"] + "\n" + indented_function_body
        dummy_function = task[f"{condition}_condition_incomplete"] + "\n   raise(\"dummy function invoked!\")"
        
        print(f"** running tests on candidate {k}")
    
        # executing the def. of the AI's function; it may fail (e.g. if AI's code is not even syntax correct)
        try:
            exec(dummy_function,globals())
            exec(complete_function,globals())
        except:
            print(f">>>>>> The def of completion-proposal crashed!")
            print(f">>>>>> src:\n {complete_function}")
            baseEvaluationz.append('NOT accepted')
            fullEvaluationz.append('failed')
            continue
    
        # running the test-cases on the AI's function; this may fail too:
        if (condition == "pre"):
            completion_resultsBase = [try_check_pre(test_case, task["task_id"]) for test_case in test_casesBase]
            completion_resultsValidation = [try_check_pre(test_case, task["task_id"]) for test_case in test_casesValidation]
        else:
            completion_resultsBase = [try_check_post(test_case, task["task_id"]) for test_case in test_casesBase]
            completion_resultsValidation = [try_check_post(test_case, task["task_id"]) for test_case in test_casesValidation]

        print(complete_function)

        rawBaseEvalResult = compare_results(solution_resultsBase, completion_resultsBase)
        verdictBaseTest = 'accepted' if rawBaseEvalResult == 'accepted' else 'NOT accepted'
        if test_casesValidation == []:   
          verdictFullTest = rawBaseEvalResult
        else:
          verdictFullTest = compare_results(solution_resultsBase   + solution_resultsValidation, 
                                            completion_resultsBase + completion_resultsValidation)
        baseEvaluationz.append(verdictBaseTest)
        fullEvaluationz.append(verdictFullTest)
        print(f"Base ({verdictBaseTest}): {completion_resultsBase}")
        print(f"Validation ({verdictFullTest}): {completion_resultsValidation}")
    
    task[f"{condition}_condition_baseEvaluations"] = baseEvaluationz
    task[f"{condition}_condition_evaluations"] = fullEvaluationz
    task[f"{condition}_condition_baseEvaluation"] = 'accepted' if 'accepted' in baseEvaluationz else 'NOT accepted'
    task[f"{condition}_condition_evaluation"] = 'accepted' if 'accepted' in fullEvaluationz else 'NOT accepted'
    
def print_acceptance_rate(tasks: Dict[str,Dict]):
    
    pre_condition_baseEvaluations = [ task["pre_condition_baseEvaluation"] for task in tasks.values()]
    pre_condition_evaluations = [ task["pre_condition_evaluation"] for task in tasks.values()]
    pre_condition_baseEvaluations = [ r for r in pre_condition_baseEvaluations if r != None]
    pre_condition_evaluations = [ r for r in pre_condition_evaluations if r != None]

    post_condition_baseEvaluations = [ task["post_condition_baseEvaluation"] for task in tasks.values()]
    post_condition_evaluations = [ task["post_condition_evaluation"] for task in tasks.values()]
    post_condition_baseEvaluations = [ r for r in post_condition_baseEvaluations if r != None]
    post_condition_evaluations = [ r for r in post_condition_evaluations if r != None]
    
    preCounterB = Counter(pre_condition_baseEvaluations)
    preCounter = Counter(pre_condition_evaluations)
    postCounterB = Counter(post_condition_baseEvaluations)
    postCounter = Counter(post_condition_evaluations)

    print("** Evaluation result:")
    if preCounterB.total() > 0 :
        tot = preCounterB.total()
        print(f"   #pre-cond checked with base-tests = {tot}")
        for (state, count) in preCounterB.items():
            print(f"   {state}: {count} ({count/tot*100}%)")
    if preCounter.total() > 0 :
        tot = preCounter.total()
        print(f"   #pre-cond checked with all-tests = {tot}")
        for (state, count) in preCounter.items():
            print(f"   {state}: {count} ({count/tot*100}%)")
    if postCounterB.total() > 0 :
        tot = postCounterB.total()
        print(f"   #post-cond checked with base-tests = {tot}")
        for (state, count) in postCounterB.items():
            print(f"   {state}: {count} ({count/tot*100}%)")
    if postCounter.total() > 0 :
        tot = postCounter.total()
        print(f"   #post-cond checked with all-tests = {tot}")
        for (state, count) in postCounter.items():
            print(f"   {state}: {count} ({count/tot*100}%)")

def write_evaluation_report(tasks: Dict[str,Dict], reportfile:str):
    if reportfile == None: return
    with open(reportfile,'w') as f:
        for tId in tasks:
            task = tasks[tId]
            precondBaseEval = task["pre_condition_baseEvaluation"]
            if precondBaseEval != None:
                f.write(f"{tId}-pre (base tests): {precondBaseEval}\n")
            precondEval = task["pre_condition_evaluation"]
            if precondEval != None:
                f.write(f"{tId}-pre (all tests): {precondEval}\n")
            postcondBaseEval =  task["post_condition_baseEvaluation"]
            if postcondBaseEval != None:
                f.write(f"{tId}-post (base tests): {postcondBaseEval}\n")
            postcondEval =  task["post_condition_evaluation"]
            if postcondEval != None:
                f.write(f"{tId}-post (all tests): {postcondEval}\n")

def evaluate_tasks_results(tasks: Dict[str,Dict], reportfile:str) -> None:
    for task in tasks:
        task_dict = tasks[task]
        evaluate_task_result(task_dict, "pre")
        evaluate_task_result(task_dict, "post")

    if reportfile != None:
        write_evaluation_report(tasks,reportfile)

    print_acceptance_rate(tasks)

