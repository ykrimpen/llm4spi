#@ task_id:HE108

"""@ program-desc:
Write a function program_HE108 which takes an array of integers and returns
the number of elements which has a sum of digits > 0.
If a number is negative, then its first signed digit will be negative:
e.g. -123 has signed digits -1, 2, and 3.

Examples:
    program_HE108([]) = 0
    program_HE108([-1, 11, -11]) = 1
    program_HE108([1, 1, 2]) = 3

"""

#< program:
def program_HE108(arr) :
    def digits_sum(n):
        neg = 1
        if n < 0: n, neg = -1 * n, -1 
        n = [int(i) for i in str(n)]
        n[0] = n[0] * neg
        return sum(n)
    return len(list(filter(lambda x: x > 0, [digits_sum(i) for i in arr])))
#>


"""@ post_condition:
It checks that retval is equal to the number of elements x in arr (an array of int) 
satisfying the following criterion:

     if x is non-negative, the sum of the digits in x should be > 0
     else, check_post_HE108  returns None.

Examples:
   check_post_HE108(0,[]) = True
   check_post_HE108(1,[-1, 11, -11]) = True
   check_post_HE108(3,[1, 1, 2]) = True

"""

#< post_condition_solution:
def check_post_solution_HE108(retval,arr) -> bool:
    def mysum(x:int) -> int :
        z = [ int(digit) for digit in str(abs(x)) ]
        if x<0 :
            z0 = z[0] * -1
            z.pop(0)
            z.append(z0)
        return sum(z)
    
    return retval == len([x for x in arr if mysum(x)>0])      
 #>


#< post_condition_tests:
post_condition_tests_HE108 = [[0,[]],[1,[-1, 11, -11]],[3,[1, 1, 2]],[2,[0,100,1]],[0,[-321, 0, -401]],[2,[13,-12,-622]],[3,[123,1]],[1,[18,-199]],[2,[0,-810211]]]

#>

if __name__ == '__main__':
    # some tests
    print(f"** Post-tests: {post_condition_tests_HE108}")
    print(f"               {[ check_post_solution_HE108(*tc) for tc in post_condition_tests_HE108]}")
    prgInputs = [tc[1:] for tc in post_condition_tests_HE108]
    print(f"** Program-tests: {prgInputs}")
    print(f"                  {[ program_HE108(*tc) for tc in prgInputs]}")

