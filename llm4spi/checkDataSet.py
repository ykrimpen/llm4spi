#
# For checking that given data-set is structurally correct
#
import data

def printPrograms_InDataSet(data_file: str, whichProblem:str) -> None :
   """
   Print the programs in the dataset.
   """
   problems = data.read_problems(data_file)
   if whichProblem != None :
      problems = { whichProblem : problems[whichProblem] }

   for p in problems:
      P = problems[p]
      print("")
      print(f"** Problem {p} **")
      print(P["program"])
      print(P["pre_condition_solution"])
      print(P["post_condition_solution"])

def checkPrePostSolutions_InDataSet(data_file: str) -> None :
   """
   Check if the pre- and post-conditions in the given data set can be
   read by Python, and then if the corresponding test-cases of these
   pre-/post-conditions can be executed without crashing.
   """
   problems = data.read_problems(data_file)
   print(f"** Checking {len(problems)} problems...")
   for p in problems:
      P = problems[p]
      preSolution = P["pre_condition_solution"]
      postSolution = P["post_condition_solution"]
      problemId = p
      print(f"** Problem {problemId}:")
      try:
         exec(preSolution,globals())
      except:
         print(f">>> OUCH pre-cond problem {p} has a problem.")
         print(preSolution)
      try:
         test_cases = [ data.prepTestCase(tc) for tc in P["pre_condition_tests"]]
         #print(test_cases)
         solution_results = [eval(f"check_pre_solution_{problemId}(*test_case)") for test_case in test_cases]
         print(f"   precond test results:{solution_results}")
      except:
         print(f">>> OUCH pre-cond problem {p} has a crashing test")
         raise Exception("OUCH")

         
      try:
         exec(postSolution,globals())
      except:
         print(f">>> OUCH post-cond problem {p} has a problem.")
         print(postSolution)
         raise Exception("OUCH")
      try:
         test_cases = [ data.prepTestCase(tc) for tc in P["post_condition_tests"] ]
         solution_results = [eval(f"check_post_solution_{problemId}(*test_case)") for test_case in test_cases]
         print(f"   postcond test results:{solution_results}")
      except:
         print(f">>> OUCH post-cond problem {p} has a crashing test")
         raise Exception("OUCH")


   print("** All seem to be good.")

if __name__ == '__main__':
   checkPrePostSolutions_InDataSet(data.ZEROSHOT_DATA)
   #printPrograms_InDataSet(data.ZEROSHOT_DATA, whichProblem="3")
