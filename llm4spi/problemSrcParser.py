#
# Functions for reading a problem-source file and extract its components.
#
from typing import Iterable, Dict
import os

def parseProblems(dataSetDir:str) -> Dict[str, Dict]:
    problemFolders = [ f for f in os.listdir(dataSetDir) if not f.startswith('.') ]
    problems = [ parseProblem(os.path.join(dataSetDir,P, P + ".py" )) for P in problemFolders ]
    result = { P["task_id"] : P for P in problems}
    #print(result)
    return result
    

def parseProblem(problemSrcFile:str) -> Dict :
    with open(problemSrcFile) as f:
       content = f.read()
    lines = content.split('\n')

    tid = (next(r for r in lines if r.startswith("#@ task_id"))).split(':')[1]
    prg = getCode(content,"program")
    prgDesc = getTxtDesc(content,"program-desc")
    precond  = getCode(content,"pre_condition_solution")
    preCondHeader = precond.split('\n')[0]
    precondDesc = getTxtDesc(content,"pre_condition")
    precondTestInputs = getCode(content,"pre_condition_tests").split('= ')[1]
    postcond = getCode(content,"post_condition_solution")
    postCondHeader = postcond.split('\n')[0]
    postcondDesc = getTxtDesc(content,"post_condition")
    postcondTestInputs = getCode(content,"post_condition_tests").split('= ')[1]

    result = { "task_id" : tid,
               "program-desc" : prgDesc,
               "program" : prg,
               "pre_condition" : precondDesc,
               "pre_condition_incomplete" : preCondHeader,
               "pre_condition_solution" : precond,
               "pre_condition_tests" : precondTestInputs,
               "post_condition" : postcondDesc,
               "post_condition_incomplete" : postCondHeader,
               "post_condition_solution" : postcond,
               "post_condition_tests" : postcondTestInputs
            }

    #print(result)
    return result

def getCode(src:str, tag:str) -> str:
    return getFragment(src,tag,"#<", "#>")

def getTxtDesc(src:str, tag:str) -> str:
    return getFragment(src,tag,"\"\"\"@", "\"\"\"")

def getFragment(src:str, tag:str, openMarker:str, closeMarker:str) -> str:
    """
    Extract a fragment from src. This fragment consists of
    lines between a tag-open-marker and a close-marker.
    """
    lines = src.split('\n')
    tagOpen1  = openMarker + " " + tag + ":"
    tagOpen2  = openMarker + tag + ":"
    fragments = []
    foundStart = False 
    for row in lines:
        if foundStart:
            if row.startswith(closeMarker):
                break
            else:
                fragments.append(row)
        if row.startswith(tagOpen1) or row.startswith(tagOpen2):
            foundStart = True

    return ('\n'.join(fragments)).lstrip()


if __name__ == '__main__':
    # some tests
    #parseProblem("../data/human-eval-specs/P3/P3.py")
    print(parseProblems("../data/human-eval-specs"))