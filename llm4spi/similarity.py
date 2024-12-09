#
# Contain function to measure the similarity/difference between two
# programs. This is expressed in terms of the Lehvensein distance
# between the two strings of the programs' code.
#

import edit_distance

def levenshteinDistance(progRef:str, prog2:str):
    """
    Return the lehvenstein distance between the code of two programs.
    The headers are assumed to be the same, so they are ignored. And
    of every line in the code, the leading and trailing spaces are
    ignored as well.

    The function returns a dictionary, containing the distance as well
    as the distance relative to the length of the second program (the 
    lev-distance divided by the length of program-2).

    Todo: ignore comments too.
    """
    # we remove the header-line, and leading and trailing spaces of every line
    p1 = '\n'.join([ line.strip() for line in progRef.splitlines()[1:] ])
    p2 = '\n'.join([ line.strip() for line in prog2.splitlines()[1:] ])
    N2 = len(p2)
    if N2==0: return None
    sm = edit_distance.SequenceMatcher(a=p1, b=p2)
    levenstein = sm.distance()
    R = {
        'distance':levenstein,
        'relativeDistance' : levenstein/(0.0 + N2),
        's1Len': len(p1),
        's2Len': N2
        }
    return R
    

if __name__ == '__main__':
    P1 = "def f1(x):\n  y = x+1\n  return y-1"
    P2 = "def f2(x):\n  y=x+1\n  y=y-1\n  return y"
    print(f">>> {levdDistance(P1,P2)}")
