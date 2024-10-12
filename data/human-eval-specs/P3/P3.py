#@ task_id:P3

"""@ program-desc:
You are given a string s.
If s[i] is a letter, reverse its case from lower to upper or vice versa, 
otherwise keep it as it is.
If the string contains no letters, reverse the string.
The function should return the resulted string.

Examples:
  solve("1234") = "4321"
  solve("ab") = "AB"
  solve("#a@C") = "#A@c"

"""

#< program:
def program_P3(s):
    flg = 0
    idx = 0
    new_str = list(s)
    for i in s:
        if i.isalpha():
            new_str[idx] = i.swapcase()
            flg = 1
        idx += 1
    s = ""
    for i in new_str:
        s += i
    if flg == 0:
        return s[len(s)::-1]
    return s
#>



"""@ pre_condition:
It checks that s is a non-empty string.
"""
#< pre_condition_solution:
def check_pre_solution_P3(s: str) -> bool:
    return len(s) > 0
#>

"""@ post_condition: 
It checks that retval is the reverse of s, if s contains no letters. 
Else, it checks that retval is as s, but for each s[i] which 
is a lower case letter, retval[i] is the upper case, vice versa, 
and else retval[i] is as s[i].

Examples:
  check_post_P3("4321","1234") = True
  check_post_P3("AB","ab") = True
  check_post_P3("#A@c","#a@C") = True

"""
#< post_condition_solution:
def check_post_solution_P3(retval: str, s: str) -> bool:
  if all([ not c.isalpha() for c in s]):
      return retval == s[::-1]
  if len(retval) != len(s):
      return False
  check =  [ (r == x.swapcase()) if x.isalpha() else (r==x) for (r,x) in zip(retval,s) ]
  return all(check)
#>

#< pre_condition_tests:
pre_condition_tests_P3 = [[""],["t3st"],["1234"],["ab"],["#a@c"]]
#>

#< post_condition_tests:
post_condition_tests_P3 = [["T3ST","t3st"],["1234","4321"],["AB","ab"],["#A@C","#a@c"],["tesT","TESt"],["TEStEST","tesTest"],["test","test"]]
#>

if __name__ == '__main__':
    # some tests
    print(f"** Pre-tests : {pre_condition_tests_P3}")
    print(f"               {[ check_pre_solution_P3(*tc) for tc in pre_condition_tests_P3 ]}")
    print(f"** Post-tests: {post_condition_tests_P3}")
    print(f"               {[ check_post_solution_P3(*tc) for tc in post_condition_tests_P3]}")
    prgInputs = [tc[1:] for tc in post_condition_tests_P3]
    print(f"** Program-tests: {prgInputs}")
    print(f"                  {[ program_P3(*tc) for tc in prgInputs]}")

