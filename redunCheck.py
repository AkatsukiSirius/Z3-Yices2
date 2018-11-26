#! /usr/bin/env python
from yices import *

def redunCheck(s, newCond):
    '''
    :param s: literals in body
    :param nfmal: the new constraint to check
    :return: res
    '''

    s.push()
    s.assert_formulas([newCond])
    status0 = ctx.check_context() == Status.SAT
    s.pop()
    s.push()
    s.assert_formulas([Terms.ynot(newCond)])
    status1 = ctx.check_context() == Status.SAT
    s.pop()
    if status0 and status1:
        res = 'Non - redundant'
    else:
        res = 'Redundant'
    return res


# Example 1. Real Arithmetic
cfg = Config()
cfg.default_config_for_logic('QF_LRA')
ctx = Context(cfg)  # type: Context

real_t = Types.real_type()
x = Terms.new_uninterpreted_term(real_t, 'x')
y = Terms.new_uninterpreted_term(real_t, 'y')

f0 = Terms.parse_term('(> (+ (* 2 x) y) 1)')  # type: object # x + y > 0
f1 = Terms.parse_term('(or (< x 0) (< y 0))')  # x < 0 or y < 0

ctx.push()
ctx.assert_formulas([f0, f1])

# Case 1. Redundant Constraint
newCond = Terms.parse_term('(> (+ (* 2 x) y) 1)')

print(redunCheck(ctx, newCond))

# Case 2. Non Redundant Constraint
newCond = Terms.parse_term('(< x 1)')
print(redunCheck(ctx, newCond))

# Example 2. Bit-Vector

cfg = Config()
cfg.default_config_for_logic('QF_BV')
ctx = Context(cfg)

bv32_t = Types.bv_type(32)
x = Terms.new_uninterpreted_term(bv32_t, 'x')
y = Terms.new_uninterpreted_term(bv32_t, 'y')
z = Terms.new_uninterpreted_term(bv32_t, 'z')

constant = Terms.bvconst_integer(32, 5)
f0 = Terms.bvgt_atom(Terms.bvadd(Terms.bvadd(x, y), z), constant)
f1 = Terms.bvgt_atom(x, Terms.bvconst_integer(32, 1))
f2 = Terms.bvgt_atom(y, Terms.bvconst_integer(32, 1))
f3 = Terms.bvgt_atom(z, Terms.bvconst_integer(32, 1))

ctx.push()
ctx.assert_formulas([f0, f1, f2, f3])

# Case 1. Redundant Constraint
newCond = Terms.bvgt_atom(x, Terms.bvconst_integer(32, 0))

print(redunCheck(ctx, newCond))

# Case 2. Non Redundant Constraint
newCond = Terms.bvgt_atom(y, Terms.bvconst_integer(32, 3))
print(redunCheck(ctx, newCond))

