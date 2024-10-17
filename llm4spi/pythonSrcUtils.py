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
    foundBody = False
    for z in lines:
        if foundBody:
            body.append(z)      
        elif z.strip().startswith('def'):
            foundBody = True

    if foundBody:
        return '\n'.join(body)
    else:
        return pythonStr
  

def extractPythonFunctionDef_fromMarkDownQuote(pythonStr:str) -> str :
    """
    To extract a Python function definition which is written inside a Markdown quote,
    e.g.:

    ```
    def foo(x): return x+1
    ```
    
    We then extract the code inside the quote.

    The same string is returned if there is no quotation in the string.
    """
    if pythonStr.find("```") < 0:
        # no quotation is found
        return pythonStr
    
    lines =  pythonStr.split('\n')
    functionDef = []
    startQuoteFound = False
    startFunctionFound = False
    for z in lines:
        if not startFunctionFound and z.strip().startswith('```'):
            # start quote found
            startQuoteFound = True
            # will assume that the next line is the start of the python-code
            startFunctionFound = True
            continue
        #if not startFunctionFound and z.strip().startswith('def'):
        #    if not startQuoteFound:
        #        # well then the function is not packed between quotes
        #        return pythonStr
        #    startFunctionFound = True
        #    functionDef.append(z)
        #    continue
        if startFunctionFound:
            if z.strip().startswith('```'):
                # end of quote is found
                break
            functionDef.append(z)

    return '\n'.join(functionDef)


if __name__ == '__main__':
    # some tests
    txt = """#some comment
#more comment
def foo(x):
  y = x+1
  return y
#trailing stuff
"""

    txt2 = """
```python
def foo(x):
  y = x+1
  return y
```
"""
    print(extractFunctionBody(txt))
    print(extractPythonFunctionDef_fromQuote(txt2))
    print(extractFunctionBody(extractPythonFunctionDef_fromQuote(txt2)))
     