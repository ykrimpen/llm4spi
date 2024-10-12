def solve(s):
    """You are given a string s.
    if s[i] is a letter, reverse its case from lower to upper or vice versa, 
    otherwise keep it as it is.
    If the string contains no letters, reverse the string.
    The function should return the resulted string.
    Examples
    solve("1234") = "4321"
    solve("ab") = "AB"
    solve("#a@C") = "#A@c"
    """
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

def check_pre_solution_3(s: str) -> bool:
    return len(s) > 0

def check_post_solution_3(retval: str, s: str) -> bool:
  if all([ not c.isalpha() for c in s]):
      return retval == s[::-1]
  if len(retval) != len(s):
      return False
  check =  [ (r == x.swapcase()) if x.isalpha() else (r==x) for (r,x) in zip(retval,s) ]
  return all(check)

if __name__ == '__main__':
    # some tests
    print(check_post_solution_3("T3ST","t3st"))
    print(check_post_solution_3("1234","4321"))
    print(check_post_solution_3("@!","!@"))
    print(check_post_solution_3("AB","ab"))

