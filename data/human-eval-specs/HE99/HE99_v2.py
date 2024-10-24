#@ task_id:HE99

"""@ program-desc:
Create a function that takes a string input v representing a number
and returns the closest integer to it. If the number is equidistant
from two integers, round it away from zero.

Examples
   program_HE99("10") = 10
   program_HE99("15.3") = 15
   program_HE99("14.5") = 15
   program_HE99("-14.5") = -15


Note:
Rounding away from zero means that if the given number is equidistant
from two integers, the one you should return is the one that is the
farthest from zero. For example program_HE99("14.5") should
return 15 and program_HE99("-14.5") should return -15.

"""

#< program:
def program_HE99(v:str) :

    from math import floor, ceil

    if v.count('.') == 1:
        # remove trailing zeros
        while (v[-1] == '0'):
            v = v[:-1]

    num = float(v)
    if v[-2:] == '.5':
        if num > 0:
            res = ceil(num)
        else:
            res = floor(num)
    elif len(v) > 0:
        res = int(round(num))
    else:
        res = 0

    return res
#>

"""@ pre_condition:
It checks that the string v represents a number (float or int).
"""

#< pre_condition_solution:
def check_pre_solution_HE99(v: str) -> bool:
    try:
        float(v)
    except:
        return False
    return True
#>

"""@ post_condition:
It checks that retval is equal to the integer r closests to the nummeric value n
represented by the string v.
However, if n is equidistant from its two closest integers, retval should be 
equal to the integer closest to n but furthest from zero.

Examples:
   check_post_HE99(10,"10") = True
   check_post_HE99(15,"15.3") = True
   check_post_HE99(15,"14.5") = True
   check_post_HE99(-15,"-14.5") = True

"""

#< post_condition_solution:
def check_post_solution_HE99(retval: int, v: str) -> bool:
    from math import floor, ceil
    x = float(v)
    x0 = floor(x)
    x1 = ceil(x)
    r = round(x)
    if abs(x - x0) != abs(x - x1):
        return retval == r
    else :
        return retval == (x1 if x >= 0 else x0)
 #>

#< pre_condition_tests:
pre_condition_tests_HE99 = [[""],["10"],["15.3"],["-3.12542"],["5.0.0"],["test"],["18-18"]]
#>

#< post_condition_tests:
post_condition_tests_HE99 = [[0,"0"],[10,"10"],[15,"15.3"],[15,"14.5"],[8,"8.50"],[-15,"-14.5"],[-3,"-3.12542"],[0,"0.10000"],[16,"15.3"],[14,"14.5"],[-4,"-3.12542"]]
#>

if __name__ == '__main__':
    # some tests
    print(f"** Pre-tests: {pre_condition_tests_HE99}")
    print(f"               {[ check_pre_solution_HE99(*tc) for tc in pre_condition_tests_HE99]}")
    print(f"** Post-tests: {post_condition_tests_HE99}")
    print(f"               {[ check_post_solution_HE99(*tc) for tc in post_condition_tests_HE99]}")
    prgInputs = [tc[1:] for tc in post_condition_tests_HE99]
    print(f"** Program-tests: {prgInputs}")
    print(f"                  {[ program_HE99(*tc) for tc in prgInputs]}")
