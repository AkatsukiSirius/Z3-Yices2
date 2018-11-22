from z3 import *
import re

def assertions2Array(assertions):
    results = []
    for assertion in assertions:
        results.append(str(assertion))
    return results

def extractCmp(newCondition):
    result = ''
    cmp_syb = ">|<|=|>=|<="
    if len(re.findall(cmp_syb,newCondition)) ==2:
        for cmp in re.findall(cmp_syb,newCondition):
            result += cmp
    else:
        result = re.findall(cmp_syb,newCondition)[0]
    return result

def ineqSol(ineq1, cmp1, ineq2, cmp2):
    if cmp1 == cmp2:
        if cmp1 == '>' or cmp1 == '>=':
            if int(ineq1.split('>')[1]) > int(ineq2.split('>')[1]):
                redun = False
            else:
                redun = True
        elif cmp1 == '<' or cmp1 == '<=':
            if int(ineq1.split('<')[1]) < int(ineq2.split('<')[1]):
                redun = False
            else:
                redun = True
        elif cmp1 == '=' or cmp1 == '!=':
            redun = True
    else:
        redun = True
    return redun

def redundencyChecking(assertions, newCondition):
    cmp = extractCmp(newCondition)
    for assertion in assertions:
        assCmp = extractCmp(assertion)
        if ineqSol(assertion, assCmp, cmp, newCondition):
            print('Redundant')
        else:
            print('Non Redundant')


# Add original conditions to body literals
x = Int('x')
y = Int('y')
s = Solver()
s.add(x>5) # Now, we have x>5 in body

assertions = assertions2Array(s.assertions()) # convert the constriants in body to strings
newCondition = 'x > 1' # Define a new constraint
redundencyChecking(assertions, newCondition) # Check whether the new constraint is redundant via function redundencyChecking
