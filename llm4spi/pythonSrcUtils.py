#
# Contain functions for pre-processing strings containing Python code.
#  


def extractFunctionBody(pythonStr:str) -> str :
    """
    This assumes the given txt contains the definition of a single function F.
    The body of F is extracted and returned. F's header and any leading lines
    before the header will be stripped off.
    """
    lines =  pythonStr.split('\n')
    body = []
    leadingPart = True
    foundBody = False
    for z in lines:
        if foundBody:
            body.append(z)      
        elif z.startswith('def'):
            foundBody = True

    if foundBody:
        return '\n'.join(body)
    else:
        return pythonStr
  

if __name__ == '__main__':
    # some tests
    txt = """#some comment
#more comment
def foo(x):
  y = x+1
  return y
#trailing stuff
"""
    print(extractFunctionBody(txt))
     