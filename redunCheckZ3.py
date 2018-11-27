#! /usr/bin/env python
from z3 import *
import re

def redunCheckZ3(s, newCond):
    '''
    Description: pass through a set of constrains s,
    check the redundecny of new constraint newCond
    :type z3.z3.Solver: s
    :type z3.z3.BoolRef: newCond
    :rtype: string
    '''
    res = ''
    # Add the new constriant to existing set
    s.push()
    s.add(newCond)
    r1 = (s.check()==sat)
    # Remove the new constraint
    s.pop()
    # Add the negation of new constraint
    s.push()
    s.add(Not(newCond))
    r2 = (s.check()==sat)
    # Remove the constraint just added
    s.pop()
    # Check the redundency
    if r1 == True and r2 == True:
        res = 'Non-redundant'
    else:
        res = 'Redundant'
    return res

# Example 1 - Arithmetic Operations
x = Int('x')
y = Int('y')

# Create an empty constraints set
s = Solver()

# Define the function t = (x+y)^2
t = simplify((x + y)**2, som=True)

# Add first constraint to body
s.push()

s.add(t>10)

# Display the body
s.assertions()
# Add other constraints, x > 10, y > 10
s.push()
s.add(x>10,y>10)


# Case 1. Redundant Constraint
# Define first new constraint, x > 0
f = x > 0
# Check the redundency
print(redunCheckZ3(s, f))

# Case 2. Non Redundant Constraint
# Define first new constraint, x > 0
g = x < 100
# Check the redundency
print(redunCheckZ3(s, g))


# Example 2 - Machine Arithmetic
x = BitVec('x', 16)
y = BitVec('y', 16)
s = Solver()
t = (x + y == 10)
s.push()
s.add(t)
s.push()
s.add(x >= 3, y >= 3)

# Case 1. Redundant Constraint
f = x > 1
print(redunCheckZ3(s, f))

# Case 2. Non Redundant Constraint
g = x > 3
print(redunCheckZ3(s, g))