#@ task_id:P0

"""@ program-desc: 
The program takes x and y that are non-negative, and it returns the greatest of x and y. 

Examples:
  maxp(0,0) = 0 
  maxp(9,1) = 9 
  maxp(9,10) = 10

""" 

#< program:
def program_P0(x: float, y: float) -> float: 
  return max(x,y)
#>

"""@ pre_condition:
It checks if x and y are non-negative.
"""

#< pre_condition_solution:
def check_pre_solution_P0(x: float, y: float) -> bool: 
    return x>=0 and y>=0
#>

"""@ post_condition: 
It checks if retval is the greatest of x and y.
"""

#< post_condition_solution:
def check_post_solution_P0(retval: float, x: float, y: float) -> bool:
    return (retval==x or retval==y) and retval >=x and retval >= y
#>

#< pre_condition_tests:
pre_condition_tests_P0 = [[0,0],[9,1],[9,10],[-1,1],[5,0],[1,-1],[-9,-9]]
#>

#< post_condition_tests:
post_condition_tests_P0 = [[0,0,0],[9,9,1],[10,9,10],[1,1,1],[0,3,1],[3,5,3],[0,1,1]]
#>